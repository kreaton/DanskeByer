namespace DanskeByer.Models;

/// <summary>A zoom preset for the map, given as a lon/lat box.</summary>
public sealed record MapView(string Label, double LonMin, double LonMax, double LatMin, double LatMax)
{
    public static readonly MapView Whole = new("Hele Danmark", 7.9, 15.3, 54.5, 57.85);
    public static readonly MapView Jylland = new("Jylland", 8.0, 11.3, 54.75, 57.85);
    public static readonly MapView Islands = new("Fyn & Sjælland", 9.6, 13.0, 54.6, 56.3);
    public static readonly MapView Capital = new("Hovedstaden", 11.6, 13.0, 55.3, 56.2);
    /// <summary>The inner city, so the sights there (Tivoli, Nyhavn, Amalienborg …) do not lie on top of each other.</summary>
    public static readonly MapView Copenhagen = new("København", 12.50, 12.66, 55.648, 55.708);

    public static readonly IReadOnlyList<MapView> All = [Whole, Jylland, Islands, Capital, Copenhagen];
}
