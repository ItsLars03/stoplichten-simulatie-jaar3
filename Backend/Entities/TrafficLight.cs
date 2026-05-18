using System.ComponentModel.DataAnnotations;

namespace TrafficController.Entities;

public enum LightState
{
    Red = 0,
    Orange = 1,
    Green = 2,
    GreenRight = 3,
    GreenStraightAndRight = 4
}

public class TrafficLight
{
    public string Id { get; set; }

    // TrafficLight
    public LightState State { get; set; }

    // Sensor
    public bool HasEntity { get; set; }
    public long? TriggeredUnixTimeStamp { get; set; }

    // LightState timing
    public DateTimeOffset? StateChangedAt { get; set; }
    public bool InCycle { get; set; }
}