using System.Text;
using Microsoft.JSInterop;

namespace DanskeByer.Services;

/// <summary>
/// Says town and sight names out loud from wwwroot/audio (made with edge-tts). The file name is the
/// name in lower case with æ ø å as ae oe aa and everything else that is not a letter or digit as "_":
/// "H.C. Andersens Hus" → audio/h_c_andersens_hus.mp3. The on/off setting is kept in the browser.
/// </summary>
public sealed class SoundService(IJSRuntime js)
{
    private const string Key = "danskebyer.sound";

    public bool Enabled { get; private set; } = true;

    /// <summary>Reads the saved setting. Call once after the first render (JS is not available before).</summary>
    public async Task LoadAsync()
    {
        try { Enabled = await js.InvokeAsync<string?>("byer.load", Key) != "off"; }
        catch (JSException) { }
    }

    public async Task SetEnabledAsync(bool on)
    {
        Enabled = on;
        try
        {
            await js.InvokeVoidAsync("byer.save", Key, on ? "on" : "off");
            if (!on) await js.InvokeVoidAsync("byer.stop");
        }
        catch (JSException) { }
    }

    /// <summary>Says the name, unless the sound is off (<paramref name="force"/>: say it anyway, for "Hør igen").</summary>
    public async Task SayAsync(string name, bool force = false)
    {
        if (!(Enabled || force) || string.IsNullOrWhiteSpace(name)) return;
        try { await js.InvokeVoidAsync("byer.play", "audio/" + FileName(name) + ".mp3"); }
        catch (JSException) { }
    }

    /// <summary>A short happy chime for a right answer, unless the sound is off. A name said right after waits for it.</summary>
    public async Task CheerAsync()
    {
        if (!Enabled) return;
        try { await js.InvokeVoidAsync("byer.cheer"); }
        catch (JSException) { }
    }

    public static string FileName(string name)
    {
        var sb = new StringBuilder(name.Length + 4);
        var gap = false;
        foreach (var ch in name.ToLowerInvariant())
        {
            var part = ch switch
            {
                'æ' => "ae",
                'ø' => "oe",
                'å' => "aa",
                >= 'a' and <= 'z' or >= '0' and <= '9' => ch.ToString(),
                _ => null,
            };
            if (part is null) { gap = true; continue; }
            if (gap && sb.Length > 0) sb.Append('_');
            gap = false;
            sb.Append(part);
        }
        return sb.ToString();
    }
}
