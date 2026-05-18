using TrafficController.Config;
using TrafficController.Entities;

namespace TrafficController.Repositories;

public class TrafficLightsRepository
{
    private readonly Dictionary<string, TrafficLight> _trafficLights;

    public TrafficLightsRepository()
    {
        _trafficLights = TrafficLightConfig.GetAllLights()
            .ToDictionary(l => l.Id);
    }

    public IReadOnlyDictionary<string, TrafficLight> GetAll()
    {
        return _trafficLights;
    }

    public void UpdateTrafficLight(string id, Action<TrafficLight> update)
    {
        if (_trafficLights.TryGetValue(id, out var trafficLight))
        {
            update(trafficLight);
        }
    }
}