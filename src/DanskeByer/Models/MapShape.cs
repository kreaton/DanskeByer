namespace DanskeByer.Models;

/// <summary>Outline of Denmark (SVG path) plus the projection used to place towns on it.</summary>
public sealed class MapShape
{
    public double Width { get; init; }
    public double Height { get; init; }
    public double Lon0 { get; init; }
    public double Lat0 { get; init; }
    public double Kx { get; init; }
    public double Ky { get; init; }
    public string Path { get; init; } = "";

    public double X(double lon) => (lon - Lon0) * Kx;
    public double Y(double lat) => (Lat0 - lat) * Ky;
}
