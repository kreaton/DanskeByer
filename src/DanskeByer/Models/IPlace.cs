namespace DanskeByer.Models;

/// <summary>Something with a position on the map: a town or a sight.</summary>
public interface IPlace
{
    double Lat { get; }
    double Lon { get; }
}
