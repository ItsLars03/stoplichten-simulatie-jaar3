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
    private static readonly TimeSpan TrainWarningWindow = TimeSpan.FromSeconds(20);
    private static readonly TimeSpan TrainClearanceWindow = TimeSpan.FromSeconds(10);

    public SimulationService(TrafficLightsRepository repository, IConflictMatrix conflictMatrix)
    {
        _repository = repository;
        _conflictMatrix = conflictMatrix;
    }

    public SimulationResponseDto ProcessSimulationData(SimulationRequestDto request)
    {
        Console.WriteLine("----------------------------------------------------------------------------------------");
        Console.WriteLine($"Received {request.TrafficLights.Count} traffic lights at {DateTime.Now:HH:mm:ss};");

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
                light.TriggeredUnixTimeStamp = sensorDto.HasEntity ? sensorDto.TriggeredTimestamp : null;
            });
        }

        var now = DateTimeOffset.UtcNow;

        // Advance state for lights currently in a cycle
        foreach (var light in _repository.GetAll().Select(kvp => kvp.Value).Where(l => l.InCycle))
        {
            var elapsed = now - light.StateChangedAt!.Value;

            if (light.State == LightState.Green && elapsed >= GreenDuration)
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
            TrafficLights = _repository.GetAll()
                .ToDictionary(kvp => kvp.Key, kvp => kvp.Value.State)
        };
    }


    private void AssignGreens(DateTimeOffset now)
    {
        var allLights = _repository.GetAll();
        var sbLight = allLights.GetValueOrDefault("sb");
        var trainActive = sbLight is not null && sbLight.State != LightState.Red;

        // Do not create a new phase while another is active
        if (allLights.Values.Any(l => l.InCycle))
        {
            return;
        }

        // Longest waiting light gets priority
        var oldestWaiting = allLights.Values
            .Where(l =>
                l.Id != "sb" &&
                l.HasEntity &&
                l.TriggeredUnixTimeStamp.HasValue &&
                (!trainActive || !_conflictMatrix.Conflicts("sb", l.Id)))
            .OrderBy(l => l.TriggeredUnixTimeStamp)
            .FirstOrDefault();

        if (oldestWaiting == null)
            return;

        var phaseLights = new List<TrafficLight>
        {
            oldestWaiting
        };

        // Add every other compatible light
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

            if (trainActive && _conflictMatrix.Conflicts("sb", light.Id))
            {
                continue;
            }

            bool conflicts = phaseLights.Any(existing =>
                _conflictMatrix.Conflicts(existing.Id, light.Id));

            if (!conflicts)
            {
                phaseLights.Add(light);
            }
        }

        // Start entire synchronized phase
        foreach (var light in phaseLights)
        {
            _repository.UpdateTrafficLight(light.Id, l =>
            {
                l.State = LightState.Green;
                l.StateChangedAt = now;
                l.InCycle = true;
            });
        }

        Console.WriteLine(
            $"Started synchronized phase from {oldestWaiting.Id}: " +
            $"{string.Join(", ", phaseLights.Select(l => l.Id))}");
    }

    private void ProcessTrainLogic(long currentTimestamp, long trainArrivalTimestamp)
    {
        var current = DateTimeOffset.FromUnixTimeMilliseconds(currentTimestamp);

        DateTimeOffset? arrival = trainArrivalTimestamp != 0
            ? DateTimeOffset.FromUnixTimeMilliseconds(trainArrivalTimestamp)
            : null;

        var timeUntilTrain = arrival.HasValue
            ? arrival.Value - current
            : (TimeSpan?)null;

        _repository.UpdateTrafficLight("sb", light =>
        {
            light.HasEntity = false;
            light.TriggeredUnixTimeStamp = null;
            light.InCycle = false;
            light.StateChangedAt = null;

            if (!arrival.HasValue || !timeUntilTrain.HasValue)
            {
                light.State = LightState.Red;
                Console.WriteLine("sb RED because no train arrival is scheduled");
                return;
            }

            if (timeUntilTrain.Value > TrainWarningWindow)
            {
                light.State = LightState.Red;
                Console.WriteLine("sb RED because the train is outside the warning window");
                return;
            }

            if (timeUntilTrain.Value >= -TrainClearanceWindow)
            {
                light.State = LightState.Orange;
                Console.WriteLine("sb ORANGE because the train is approaching or still clearing");
                return;
            }

            light.State = LightState.Green;
            Console.WriteLine("sb GREEN because the train has cleared and the leave animation can start");
        });

        var sbLight = _repository.GetAll().GetValueOrDefault("sb");

        Console.WriteLine(
            $"Time until train: {(timeUntilTrain.HasValue ? timeUntilTrain.Value.ToString(@"hh\:mm\:ss\.ff") : "N/A")}\n" +
            $"Train light state: {sbLight?.State}"
        );
    }
}
