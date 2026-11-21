namespace DanskeByer.Models;

/// <summary>One question in the quiz: a town, or a sight when the quiz is about sights.</summary>
public sealed class QuizItem : IPlace
{
    private QuizItem(Town? town, Sight? sight, Town? nearTown)
    {
        Town = town;
        Sight = sight;
        NearTown = nearTown;
    }

    public Town? Town { get; }
    public Sight? Sight { get; }
    /// <summary>The town the hint (region, i/på) is taken from: the town itself, or the sight's nearest town.</summary>
    public Town? NearTown { get; }

    public static QuizItem For(Town town) => new(town, null, town);
    public static QuizItem For(Sight sight, Town? nearTown) => new(null, sight, nearTown);

    public bool IsSight => Sight is not null;
    public string Id => Town?.Id ?? Sight!.Id;
    public string Name => Town?.Name ?? Sight!.Name;
    public double Lat => Town?.Lat ?? Sight!.Lat;
    public double Lon => Town?.Lon ?? Sight!.Lon;
    public string Description => Town?.Description ?? Sight!.Description;
    /// <summary>The hard quiz's question: a town's description without its name; a sight's description.</summary>
    public string Clue => Town?.Clue ?? Sight!.Description;
    /// <summary>"Byen" or "Seværdigheden", for "… ligger mod øst herfra".</summary>
    public string Kind => IsSight ? "Seværdigheden" : "Byen";
}
