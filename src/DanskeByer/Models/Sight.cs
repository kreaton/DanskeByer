namespace DanskeByer.Models;

/// <summary>A tourist sight from wwwroot/data/sights.json.</summary>
public sealed class Sight : IPlace
{
    public string Id { get; init; } = "";
    public string Name { get; init; } = "";
    /// <summary>The nearest town from towns.json (may be null).</summary>
    public string? NearTownId { get; init; }
    public string Place { get; init; } = "";
    public double Lat { get; init; }
    public double Lon { get; init; }
    public string Description { get; init; } = "";
    public string Wiki { get; init; } = "";
}
