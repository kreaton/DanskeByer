using System.Text.Json.Serialization;

namespace DanskeByer.Models;

/// <summary>The part of Wikipedia's REST "page summary" response that we use.</summary>
public sealed class WikiSummary
{
    public string? Type { get; init; }
    public WikiThumb? Thumbnail { get; init; }
    [JsonPropertyName("content_urls")]
    public WikiContentUrls? ContentUrls { get; init; }
}

public sealed class WikiThumb
{
    public string? Source { get; init; }
}

public sealed class WikiContentUrls
{
    public WikiPageUrl? Desktop { get; init; }
}

public sealed class WikiPageUrl
{
    public string? Page { get; init; }
}
