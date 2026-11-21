using System.Text.Json.Serialization;

namespace DanskeByer.Models;

// Source-generated JSON so the app stays trim/AOT friendly in WebAssembly.
[JsonSourceGenerationOptions(PropertyNamingPolicy = JsonKnownNamingPolicy.CamelCase, PropertyNameCaseInsensitive = true)]
[JsonSerializable(typeof(List<Town>))]
[JsonSerializable(typeof(List<Sight>))]
[JsonSerializable(typeof(MapShape))]
[JsonSerializable(typeof(List<MapDetail>))]
[JsonSerializable(typeof(WikiSummary))]
public partial class AppJsonContext : JsonSerializerContext;
