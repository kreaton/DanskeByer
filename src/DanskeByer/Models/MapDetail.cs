namespace DanskeByer.Models;

/// <summary>
/// A detailed coastline for a small area (from wwwroot/data/details.json, made by tools/gen_detail.py).
/// The country outline is too coarse when the map zooms in on a city, so the map draws this instead
/// when the whole view fits inside the box. The path uses the same projection as <see cref="MapShape"/>.
/// </summary>
public sealed class MapDetail
{
    public string Name { get; init; } = "";
    public double LonMin { get; init; }
    public double LonMax { get; init; }
    public double LatMin { get; init; }
    public double LatMax { get; init; }
    public string Path { get; init; } = "";
    /// <summary>Attribution that must be shown with the map, e.g. OpenStreetMap.</summary>
    public string Credit { get; init; } = "";

    public bool Covers(MapView v) =>
        v.LonMin >= LonMin && v.LonMax <= LonMax && v.LatMin >= LatMin && v.LatMax <= LatMax;
}
