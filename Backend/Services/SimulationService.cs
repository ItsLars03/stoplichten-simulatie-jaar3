using TrafficController.DTOs;
using TrafficController.Entities;
using TrafficController.Interfaces;
using TrafficController.Repositories;

namespace TrafficController.Services;

public class SimulationService : ISimulationService
{
    private readonly TrafficLightsRepository _repository;
    private readonly IConflictMatrix _conflictMatrix;

    private static readonly TimeSpan GreenDuration = TimeSpan.FromSeconds(7.5);
    private static readonly TimeSpan OrangeDuration = TimeSpan.FromSeconds(3);

    private static readonly TimeSpan TrainOrangeBeforeArrival = TimeSpan.FromSeconds(20);
    private static readonly TimeSpan TrainRedBeforeArrival = TimeSpan.FromSeconds(15);
    private static readonly TimeSpan TrainGreenAfterArrival = TimeSpan.FromSeconds(10);
    private static readonly TimeSpan CrossingSafetyBuffer = TimeSpan.FromSeconds(7);

    private bool _crossingBlocked;
    
    private DateTimeOffset? _activeTrainArrival;

    public SimulationService(TrafficLightsRepository repository, IConflictMatrix conflictMatrix)
    {
        _repository = repository;
        _conflictMatrix = conflictMatrix;
    }

    public SimulationResponseDto ProcessSimulationData(SimulationRequestDto request)
    {
        Console.WriteLine("----------------------------------------------------------------------------------------");
        Console.WriteLine(
            $"Received {request.TrafficLights.Count} traffic lights at {DateTime.Now:HH:mm:ss}");

        // Update sensor data
        foreach (var sensorDto in request.TrafficLights)
        {
            if (sensorDto.Id == "sb")
            {
                continue;
            }

            _repository.UpdateTrafficLight(sensorDto.Id, light =>
            {
                light.HasEntity = sensorDto.HasEntity;
                light.TriggeredUnixTimeStamp =
                    sensorDto.HasEntity
                        ? sensorDto.TriggeredTimestamp
                        : null;
            });
        }

        var now = DateTimeOffset.UtcNow;

        // Advance traffic light cycles
        foreach (var light in _repository.GetAll()
                     .Select(kvp => kvp.Value)
                     .Where(l => l.InCycle))
        {
            var elapsed = now - light.StateChangedAt!.Value;

            if (IsGreenState(light.State) && elapsed >= GreenDuration)
            {
                light.State = LightState.Orange;
                light.StateChangedAt = now;
            }
            
            else if (light.State == LightState.Orange && elapsed >= OrangeDuration)
            {
                light.State = LightState.Red;
                light.StateChangedAt = null;
                light.InCycle = false;
            }
        }

        ProcessTrainLogic(request.CurrentTimestamp, request.TrainArrivalTimestamp);

        AssignGreens(now);

        return new SimulationResponseDto
        {
            TrafficLights = _repository.GetAll().ToDictionary(
                kvp => kvp.Key,
                kvp => kvp.Value.State)
        };
    }

    private static bool IsGreenState(LightState state)
    {
        return state is
            LightState.Green or
            LightState.GreenRight or
            LightState.GreenStraightAndRight;
    }

    private void AssignGreens(DateTimeOffset now)
    {
        var allLights = _repository.GetAll();

        // Do not create a new phase while another phase is active
        if (allLights.Values.Any(l => l.InCycle))
        {
            Console.WriteLine("Skipping light assignment because a cycle is active");
            return;
        }

        Console.WriteLine($"Crossing blocked? {_crossingBlocked}");
        // Oldest waiting traffic light gets priority
        var oldestWaiting = allLights.Values
            .Where(l =>
                l.Id != "sb" &&
                l.HasEntity &&
                l.TriggeredUnixTimeStamp.HasValue &&
                (!_crossingBlocked || !_conflictMatrix.Conflicts("sb", l.Id)
            ))
            .OrderBy(l => l.TriggeredUnixTimeStamp)
            .FirstOrDefault();

        if (oldestWaiting == null)
        {
            return;
        }

        var phaseLights = new List<TrafficLight>
        {
            oldestWaiting
        };

        // Add all compatible traffic lights
        foreach (var light in allLights.Values)
        {
            if (light.Id == "sb")
            {
                continue;
            }

            if (light.Id == oldestWaiting.Id)
            {
                continue;
            }

            // Keep rail-conflicting lights blocked
            if (_crossingBlocked && _conflictMatrix.Conflicts("sb", light.Id))
            {
                continue;
            }

            bool conflicts = phaseLights.Any(existing => _conflictMatrix.Conflicts(existing.Id, light.Id));

            if (!conflicts)
            {
                phaseLights.Add(light);
            }
        }

        // Start synchronized phase
        foreach (var light in phaseLights)
        {
            _repository.UpdateTrafficLight(light.Id, l =>
            {
                l.State = GetGreenState(light.Id);
                l.StateChangedAt = now;
                l.InCycle = true;
            });
        }

        Console.WriteLine(
            $"Started synchronized phase from {oldestWaiting.Id}: " +
            $"{string.Join(", ", phaseLights.Select(l => l.Id))}");
    }

    private static LightState GetGreenState(string lightId) => lightId switch
    {
        "42" => LightState.GreenStraightAndRight,
        _ => LightState.Green
    };

    private void ProcessTrainLogic(long currentTimestamp, long incomingTrainArrivalTimestamp)
    {
        var current = DateTimeOffset.FromUnixTimeMilliseconds(currentTimestamp);

        DateTimeOffset? incomingArrival = incomingTrainArrivalTimestamp  != 0 ? DateTimeOffset.FromUnixTimeMilliseconds(incomingTrainArrivalTimestamp) : null;

        bool currentCycleFinished =
            !_activeTrainArrival.HasValue ||
            current > _activeTrainArrival.Value + TrainGreenAfterArrival + CrossingSafetyBuffer;
        
        // only replace the active train when previous cycle is fully finished
        if (currentCycleFinished)
        {
            _activeTrainArrival = incomingArrival;

            if (_activeTrainArrival.HasValue)
            {
                Console.WriteLine(
                    $"Accepted new active train arrival: {_activeTrainArrival}");
            }
        }

        var activeArrival = _activeTrainArrival;

        var timeUntilTrain =
            activeArrival.HasValue
                ? activeArrival.Value - current
                : (TimeSpan?)null;

        /*
         * Block rail-conflicting traffic from:
         * 20s before arrival
         * until 15s after arrival
         */
        _crossingBlocked =
            timeUntilTrain.HasValue &&
            timeUntilTrain.Value <= TrainOrangeBeforeArrival &&
            timeUntilTrain.Value >=
            -(TrainGreenAfterArrival + CrossingSafetyBuffer);

        _repository.UpdateTrafficLight("sb", light =>
        {
            light.HasEntity = false;
            light.TriggeredUnixTimeStamp = null;
            light.InCycle = false;
            light.StateChangedAt = null;

            // No active train
            if (!activeArrival.HasValue || !timeUntilTrain.HasValue)
            {
                light.State = LightState.Green;

                Console.WriteLine(
                    "Train light GREEN because no active train exists");

                return;
            }

            // More than 20s before arrival
            if (timeUntilTrain.Value > TrainOrangeBeforeArrival)
            {
                light.State = LightState.Green;

                Console.WriteLine(
                    "Train light GREEN because train is far away");

                return;
            }

            // Between 20s and 15s before arrival
            if (timeUntilTrain.Value > TrainRedBeforeArrival)
            {
                light.State = LightState.Orange;

                Console.WriteLine(
                    "Train light ORANGE because train is approaching");

                return;
            }

            // From 15s before arrival until 10s after arrival
            if (timeUntilTrain.Value >= -TrainGreenAfterArrival)
            {
                light.State = LightState.Red;

                Console.WriteLine(
                    "Train light RED because train occupies crossing");

                return;
            }

            // Train cleared
            light.State = LightState.Green;

            Console.WriteLine(
                "Train light GREEN because train cleared");
        });

        var sbLight = _repository.GetAll()
            .GetValueOrDefault("sb");

        Console.WriteLine(
            $"Time until train: " + $"{(timeUntilTrain.HasValue ? timeUntilTrain.Value.ToString(@"hh\:mm\:ss\.ff") : "N/A")}\n" +
            $"Crossing blocked: {_crossingBlocked}\n" +
            $"Train light state: {sbLight?.State}");
    }
}