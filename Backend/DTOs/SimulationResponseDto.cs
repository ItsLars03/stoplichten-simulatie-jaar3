using TrafficController.Entities;

namespace TrafficController.DTOs;

public class SimulationResponseDto
{
    public Dictionary<string, LightState> TrafficLights { get; set; } = new Dictionary<string, LightState>();
}