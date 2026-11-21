using System.Net.Http.Json;
using DanskeByer.Models;

namespace DanskeByer.Services;

/// <summary>Loads towns.json, sights.json, denmark.json and details.json once.</summary>
public sealed class GameData(HttpClient http)
{
    public IReadOnlyList<Town> Towns { get; private set; } = [];
    public IReadOnlyList<Sight> Sights { get; private set; } = [];
    public MapShape Shape { get; private set; } = new();
    public IReadOnlyList<MapDetail> Details { get; private set; } = [];
    public bool Loaded { get; private set; }

    public async Task LoadAsync()
    {
        if (Loaded) return;
        var towns = await http.GetFromJsonAsync("data/towns.json", AppJsonContext.Default.ListTown) ?? [];
        var sights = await http.GetFromJsonAsync("data/sights.json", AppJsonContext.Default.ListSight) ?? [];
        var shape = await http.GetFromJsonAsync("data/denmark.json", AppJsonContext.Default.MapShape) ?? new MapShape();
        var details = await http.GetFromJsonAsync("data/details.json", AppJsonContext.Default.ListMapDetail) ?? [];
        Towns = towns.OrderBy(t => t.Rank).ToList();
        Sights = sights;
        Shape = shape;
        Details = details;
        Loaded = true;
    }

    /// <summary>The N largest towns. Easy = 10, Medium = 25, Hard = all 75.</summary>
    public IReadOnlyList<Town> TownsFor(Level level) => Towns.Take((int)level).ToList();

    /// <summary>
    /// The sights in the sight quiz: all outside København, whose sights lie too close together
    /// to tell apart except in the København view.
    /// </summary>
    public IReadOnlyList<Sight> QuizSights => Sights.Where(s => s.Place != "København").ToList();

    public Town? TownById(string? id) => id is null ? null : Towns.FirstOrDefault(t => t.Id == id);

    /// <summary>The detailed coastline to draw for a view, if there is one that covers it.</summary>
    public MapDetail? DetailFor(MapView view) => Details.FirstOrDefault(d => d.Covers(view));
}
