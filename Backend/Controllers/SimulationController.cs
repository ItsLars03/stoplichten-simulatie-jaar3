using Microsoft.AspNetCore.Mvc;
using TrafficController.DTOs;
using TrafficController.Interfaces;

namespace TrafficController.Controllers;

[Route("api")]
[ApiController]
public class SimulationController : ControllerBase
{
    private readonly ISimulationService _simulationService;

    public SimulationController(ISimulationService simulationService)
    {
        _simulationService = simulationService;
    }

    // POST: api/data
    [HttpPost("data")]
    public async Task<ActionResult<SimulationResponseDto>> PostData([FromBody] SimulationRequestDto request)
    {
        Console.WriteLine("Test");
        SimulationResponseDto response = _simulationService.ProcessSimulationData(request);
        return Ok(response);
    }
}