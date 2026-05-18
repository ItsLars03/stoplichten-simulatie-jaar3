namespace TrafficController.DTOs;

public class SimulationRequestDto
{
    public long CurrentTimestamp { get; set; }
    public long TrainArrivalTimestamp { get; set; }
    public ICollection<TrafficLightSensorDto> TrafficLights { get; set; } = new List<TrafficLightSensorDto>();
}
