using TrafficController.Entities;

namespace TrafficController.Config;

public class TrafficLightConfig
{
    public static List<TrafficLight> GetAllLights() => new()
    {
        new TrafficLight { Id = "1.1",  State = LightState.Red },
        new TrafficLight { Id = "2.1",  State = LightState.Red },
        new TrafficLight { Id = "5.1",  State = LightState.Red },
        new TrafficLight { Id = "6.1",  State = LightState.Red },
        new TrafficLight { Id = "7.1",  State = LightState.Red },
        new TrafficLight { Id = "8.1",  State = LightState.Red },
        new TrafficLight { Id = "9.1",  State = LightState.Red },
        new TrafficLight { Id = "10.1", State = LightState.Red },
        new TrafficLight { Id = "11.1", State = LightState.Red },
        new TrafficLight { Id = "12.1", State = LightState.Red },
        new TrafficLight { Id = "22",   State = LightState.Red },
        new TrafficLight { Id = "26.1", State = LightState.Red },
        new TrafficLight { Id = "28.1", State = LightState.Red },
        new TrafficLight { Id = "86.1", State = LightState.Red },
        new TrafficLight { Id = "88.1", State = LightState.Red },
        new TrafficLight { Id = "31.1", State = LightState.Red },
        new TrafficLight { Id = "31.2", State = LightState.Red },
        new TrafficLight { Id = "32.1", State = LightState.Red },
        new TrafficLight { Id = "32.2", State = LightState.Red },
        new TrafficLight { Id = "35.1", State = LightState.Red },
        new TrafficLight { Id = "35.2", State = LightState.Red },
        new TrafficLight { Id = "36.1", State = LightState.Red },
        new TrafficLight { Id = "36.2", State = LightState.Red },
        new TrafficLight { Id = "37.1", State = LightState.Red },
        new TrafficLight { Id = "37.2", State = LightState.Red },
        new TrafficLight { Id = "38.1", State = LightState.Red },
        new TrafficLight { Id = "38.2", State = LightState.Red },
        new TrafficLight { Id = "42",   State = LightState.Red },
        new TrafficLight { Id = "sb",   State = LightState.Red }
    };
}