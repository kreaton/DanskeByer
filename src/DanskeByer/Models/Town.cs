namespace DanskeByer.Models;

/// <summary>One of the 75 towns in wwwroot/data/towns.json.</summary>
public sealed class Town : IPlace
{
    public string Id { get; init; } = "";
    public int Rank { get; init; }
    public string Name { get; init; } = "";
    public int Population { get; init; }
    public double Lat { get; init; }
    public double Lon { get; init; }
    public string Region { get; init; } = "";
    /// <summary>The part of the country the town is on: Jylland, Sjælland, Fyn, Bornholm, Lolland-Falster or Mors.</summary>
    public string Area { get; init; } = "";
    /// <summary>Title of the (English) Wikipedia article, used to look up a free photo.</summary>
    public string Wiki { get; init; } = "";
    public string Description { get; init; } = "";
    /// <summary>Description that does not contain the town's name – used in the quiz.</summary>
    public string Clue { get; init; } = "";

    /// <summary>"Region Midtjylland", "Region Hovedstaden" …</summary>
    public string RegionName => "Region " + Region;

    /// <summary>
    /// "i Jylland" but "på Sjælland", "på Fyn", "på Bornholm" …: Jylland is a peninsula,
    /// the other parts of the country are islands.
    /// </summary>
    public string InArea => (Area == "Jylland" ? "i " : "på ") + Area;
}
