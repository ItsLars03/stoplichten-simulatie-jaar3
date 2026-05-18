namespace TrafficController.DTOs;

public class TrafficLightSensorDto
{
    public string Id { get; set; }
    public bool HasEntity { get; set; }
    public long TriggeredTimestamp { get; set; }
}