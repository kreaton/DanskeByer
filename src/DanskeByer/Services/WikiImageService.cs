using System.Net.Http.Json;
using System.Text.RegularExpressions;
using DanskeByer.Models;

namespace DanskeByer.Services;

public sealed record WikiImage(string Url, string FallbackUrl, string PageUrl);

/// <summary>
/// Looks up the lead photo of a Wikipedia article at runtime (Wikipedia's REST API allows
/// cross-origin requests). Only files hosted on Wikimedia Commons are accepted – every file there
/// has a free licence – and a link to the article is returned so the photographer can be credited.
/// </summary>
public sealed partial class WikiImageService(HttpClient http)
{
    private readonly Dictionary<string, Task<WikiImage?>> _cache = new();

    public Task<WikiImage?> GetAsync(string title, string? fallbackTitle = null)
    {
        if (string.IsNullOrWhiteSpace(title)) return Task.FromResult<WikiImage?>(null);
        var key = title + "|" + fallbackTitle;
        if (!_cache.TryGetValue(key, out var task))
            _cache[key] = task = LoadAsync(title, fallbackTitle);
        return task;
    }

    private async Task<WikiImage?> LoadAsync(string title, string? fallbackTitle)
    {
        (string Lang, string Title)[] attempts =
        [
            ("en", title),
            ("da", fallbackTitle ?? title),
        ];

        foreach (var (lang, t) in attempts)
        {
            try
            {
                var url = $"https://{lang}.wikipedia.org/api/rest_v1/page/summary/{Uri.EscapeDataString(t.Replace(' ', '_'))}";
                var s = await http.GetFromJsonAsync(url, AppJsonContext.Default.WikiSummary);
                var src = s?.Thumbnail?.Source;
                if (s is null || s.Type == "disambiguation" || string.IsNullOrEmpty(src)) continue;
                if (!src.Contains("/wikipedia/commons/")) continue;   // skip non-free (local) uploads

                var page = s.ContentUrls?.Desktop?.Page ?? $"https://{lang}.wikipedia.org/wiki/{Uri.EscapeDataString(t.Replace(' ', '_'))}";
                return new WikiImage(Enlarge(src).Replace("'", "%27"), src.Replace("'", "%27"), page);
            }
            catch
            {
                // offline, 404, CORS … – try the next language, then give up quietly
            }
        }
        return null;
    }

    /// <summary>Wikimedia thumbnails are served at any standard width; ask for a sharper one (500 px is one of the standard steps).</summary>
    private static string Enlarge(string thumbUrl) =>
        thumbUrl.Contains("/thumb/") ? WidthRegex().Replace(thumbUrl, "/500px-") : thumbUrl;

    [GeneratedRegex(@"/\d+px-(?=[^/]*$)")]
    private static partial Regex WidthRegex();
}
