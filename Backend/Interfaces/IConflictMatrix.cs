namespace TrafficController.Interfaces;

public interface IConflictMatrix
{
    bool Conflicts(string lightA, string lightB);
    bool ConflictsWithAny(string lightId, IEnumerable<string> greenLights);
}