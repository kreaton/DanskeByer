using DanskeByer.Models;

namespace DanskeByer.Services;

public static class Geo
{
    private static readonly string[] Compass =
        ["nord", "nordøst", "øst", "sydøst", "syd", "sydvest", "vest", "nordvest"];

    /// <summary>Compass direction (in Danish) when travelling from one place to another.</summary>
    public static string Direction(IPlace from, IPlace to)
    {
        var dx = (to.Lon - from.Lon) * Math.Cos((from.Lat + to.Lat) / 2 * Math.PI / 180);
        var dy = to.Lat - from.Lat;
        var deg = Math.Atan2(dx, dy) * 180 / Math.PI;   // 0 = north, 90 = east
        var sector = (int)Math.Round(((deg % 360) + 360) % 360 / 45) % 8;
        return Compass[sector];
    }

    /// <summary>Great-circle distance in km (haversine).</summary>
    public static double DistanceKm(IPlace a, IPlace b)
    {
        const double R = 6371;
        static double Rad(double d) => d * Math.PI / 180;
        var dLat = Rad(b.Lat - a.Lat);
        var dLon = Rad(b.Lon - a.Lon);
        var h = Math.Sin(dLat / 2) * Math.Sin(dLat / 2) +
                Math.Cos(Rad(a.Lat)) * Math.Cos(Rad(b.Lat)) * Math.Sin(dLon / 2) * Math.Sin(dLon / 2);
        return 2 * R * Math.Asin(Math.Sqrt(h));
    }

    /// <summary>1.408.600 – Danish thousands separator, no culture data needed.</summary>
    public static string FormatNumber(int n) =>
        n.ToString("N0", System.Globalization.CultureInfo.InvariantCulture).Replace(',', '.');

    /// <summary>Rounded for display, e.g. "ca. 17.600".</summary>
    public static string FormatPopulation(int n) => "ca. " + FormatNumber(n);
}
