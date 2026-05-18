using TrafficController.DTOs;

namespace TrafficController.Interfaces;

public interface ISimulationService
{
    SimulationResponseDto ProcessSimulationData(SimulationRequestDto request);
}