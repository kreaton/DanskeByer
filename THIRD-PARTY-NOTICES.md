# Third-party notices

**Danske Byer** (DanskeByer) is © 2026 Per Hejndorf and is licensed under the [MIT License](LICENSE), except where stated below. This file lists the third-party components, data and assets it uses, each under its own licence. Licence texts and copyright notices are kept by the upstream projects at the *Source* links; where a licence requires its notice to travel with binaries, the upstream package already carries it.

_Last reviewed: 2026-11-21. Versions are the ones resolved in this repository at that date; Dependabot keeps them current, so check the project files for the exact version of a given release._

## Libraries included in the application

| Library | Version | Licence | Source | Modified |
|---|---|---|---|---|
| .NET runtime and Blazor WebAssembly (shipped in `_framework/`) | 10.0 | MIT | [dotnet/runtime](https://github.com/dotnet/runtime), [dotnet/aspnetcore](https://github.com/dotnet/aspnetcore) | No |
| Microsoft.AspNetCore.Components.WebAssembly | 10.0.12 | MIT | [NuGet](https://www.nuget.org/packages/Microsoft.AspNetCore.Components.WebAssembly/10.0.12) | No |

<details>
<summary>Indirect (transitive) dependencies — 25 packages</summary>

These packages are pulled in by the libraries above and are shipped with the application. All are used unmodified.

| Library | Version | Licence | Source | Modified |
|---|---|---|---|---|
| Microsoft.AspNetCore.Authorization | 10.0.12 | MIT | [NuGet](https://www.nuget.org/packages/Microsoft.AspNetCore.Authorization/10.0.12) | No |
| Microsoft.AspNetCore.Components | 10.0.12 | MIT | [NuGet](https://www.nuget.org/packages/Microsoft.AspNetCore.Components/10.0.12) | No |
| Microsoft.AspNetCore.Components.Forms | 10.0.12 | MIT | [NuGet](https://www.nuget.org/packages/Microsoft.AspNetCore.Components.Forms/10.0.12) | No |
| Microsoft.AspNetCore.Components.Web | 10.0.12 | MIT | [NuGet](https://www.nuget.org/packages/Microsoft.AspNetCore.Components.Web/10.0.12) | No |
| Microsoft.AspNetCore.Metadata | 10.0.12 | MIT | [NuGet](https://www.nuget.org/packages/Microsoft.AspNetCore.Metadata/10.0.12) | No |
| Microsoft.Extensions.Configuration | 10.0.12 | MIT | [NuGet](https://www.nuget.org/packages/Microsoft.Extensions.Configuration/10.0.12) | No |
| Microsoft.Extensions.Configuration.Abstractions | 10.0.12 | MIT | [NuGet](https://www.nuget.org/packages/Microsoft.Extensions.Configuration.Abstractions/10.0.12) | No |
| Microsoft.Extensions.Configuration.Binder | 10.0.12 | MIT | [NuGet](https://www.nuget.org/packages/Microsoft.Extensions.Configuration.Binder/10.0.12) | No |
| Microsoft.Extensions.Configuration.FileExtensions | 10.0.12 | MIT | [NuGet](https://www.nuget.org/packages/Microsoft.Extensions.Configuration.FileExtensions/10.0.12) | No |
| Microsoft.Extensions.Configuration.Json | 10.0.12 | MIT | [NuGet](https://www.nuget.org/packages/Microsoft.Extensions.Configuration.Json/10.0.12) | No |
| Microsoft.Extensions.DependencyInjection | 10.0.12 | MIT | [NuGet](https://www.nuget.org/packages/Microsoft.Extensions.DependencyInjection/10.0.12) | No |
| Microsoft.Extensions.DependencyInjection.Abstractions | 10.0.12 | MIT | [NuGet](https://www.nuget.org/packages/Microsoft.Extensions.DependencyInjection.Abstractions/10.0.12) | No |
| Microsoft.Extensions.Diagnostics | 10.0.12 | MIT | [NuGet](https://www.nuget.org/packages/Microsoft.Extensions.Diagnostics/10.0.12) | No |
| Microsoft.Extensions.Diagnostics.Abstractions | 10.0.12 | MIT | [NuGet](https://www.nuget.org/packages/Microsoft.Extensions.Diagnostics.Abstractions/10.0.12) | No |
| Microsoft.Extensions.FileProviders.Abstractions | 10.0.12 | MIT | [NuGet](https://www.nuget.org/packages/Microsoft.Extensions.FileProviders.Abstractions/10.0.12) | No |
| Microsoft.Extensions.FileProviders.Physical | 10.0.12 | MIT | [NuGet](https://www.nuget.org/packages/Microsoft.Extensions.FileProviders.Physical/10.0.12) | No |
| Microsoft.Extensions.FileSystemGlobbing | 10.0.12 | MIT | [NuGet](https://www.nuget.org/packages/Microsoft.Extensions.FileSystemGlobbing/10.0.12) | No |
| Microsoft.Extensions.Logging | 10.0.12 | MIT | [NuGet](https://www.nuget.org/packages/Microsoft.Extensions.Logging/10.0.12) | No |
| Microsoft.Extensions.Logging.Abstractions | 10.0.12 | MIT | [NuGet](https://www.nuget.org/packages/Microsoft.Extensions.Logging.Abstractions/10.0.12) | No |
| Microsoft.Extensions.Options | 10.0.12 | MIT | [NuGet](https://www.nuget.org/packages/Microsoft.Extensions.Options/10.0.12) | No |
| Microsoft.Extensions.Options.ConfigurationExtensions | 10.0.12 | MIT | [NuGet](https://www.nuget.org/packages/Microsoft.Extensions.Options.ConfigurationExtensions/10.0.12) | No |
| Microsoft.Extensions.Primitives | 10.0.12 | MIT | [NuGet](https://www.nuget.org/packages/Microsoft.Extensions.Primitives/10.0.12) | No |
| Microsoft.Extensions.Validation | 10.0.12 | MIT | [NuGet](https://www.nuget.org/packages/Microsoft.Extensions.Validation/10.0.12) | No |
| Microsoft.JSInterop | 10.0.12 | MIT | [NuGet](https://www.nuget.org/packages/Microsoft.JSInterop/10.0.12) | No |
| Microsoft.JSInterop.WebAssembly | 10.0.12 | MIT | [NuGet](https://www.nuget.org/packages/Microsoft.JSInterop.WebAssembly/10.0.12) | No |

</details>

## Build, test and tooling (not distributed)

Used to build, test or render promotional material only; not part of the shipped application.

| Library | Version | Licence | Source | Modified |
|---|---|---|---|---|
| Microsoft.AspNetCore.Components.WebAssembly.DevServer | 10.0.12 | MIT | [NuGet](https://www.nuget.org/packages/Microsoft.AspNetCore.Components.WebAssembly.DevServer/10.0.12) | No |

## Fonts, data and online services

These are used at run time but are not bundled in this repository. Their own terms apply.

| Service | Used for | Terms | Source |
|---|---|---|---|
| Google Fonts | Web fonts (Fredoka), loaded at run time from Google's CDN; font files are not included in this repository | SIL Open Font License 1.1 | [fonts.google.com](https://fonts.google.com) |
| Wikipedia REST API and Wikimedia Commons | The town and sight photos, looked up at run time by article title and shown only when the image is on Wikimedia Commons (free licence). No photo is stored in this repository; every photo links to its Wikipedia article, where the photographer and licence are given | Each image's own Commons licence; Wikimedia [Terms of Use](https://foundation.wikimedia.org/wiki/Policy:Terms_of_Use) | [wikipedia.org](https://www.wikipedia.org), [commons.wikimedia.org](https://commons.wikimedia.org) |
| edge-tts (Microsoft text-to-speech) | Used once by the author to make the spoken names in `src/DanskeByer/wwwroot/audio/`; not called by the game | Microsoft's terms for its speech service | [rany2/edge-tts](https://github.com/rany2/edge-tts) |

## Map and town data

| Data | Origin | Licence |
|---|---|---|
| `src/DanskeByer/wwwroot/data/denmark.json` (outline of Denmark) | Derived from [Natural Earth](https://www.naturalearthdata.com) admin-0 countries by `tools/gen_data.py` | Public domain |
| `src/DanskeByer/wwwroot/data/details.json` (detailed coastline of central København) | Derived from [OpenStreetMap](https://www.openstreetmap.org) coastline ways (Overpass API) by `tools/gen_detail.py` | © OpenStreetMap contributors, [Open Database License 1.0](https://opendatacommons.org/licenses/odbl/1-0/). **Not covered by the MIT License**: this derived database is available under the ODbL. The game shows the credit under the map whenever this coastline is drawn. |
| Population figures in `towns.json` (rounded) | [Danmarks Statistik](https://www.dst.dk), table BY1 (towns 51–75 as of 1 January 2026) | Free reuse with credit to Danmarks Statistik as the source |
| Town and sight names, coordinates, regions | Public geographic facts | Not copyrightable |
| Descriptions and quiz clues in `towns.json` and `sights.json`, and the generator `tools/gen_data.py` | Written for this project by the author (with AI assistance) | MIT (as part of this project) |

## Icons, images, audio and video

| Asset(s) | Origin | Licence |
|---|---|---|
| `src/DanskeByer/wwwroot/icons/` (8 files: .png) | Drawn by `tools/make-icons.ps1` from the game's own map data (Natural Earth outline) | MIT (as part of this project) |
| `images/banner.png` | Screenshot of the game | MIT (as part of this project) |
| `src/DanskeByer/wwwroot/img/byzone-skilt.svg`, `byzone-skilt.png` | Drawn for this project: a simplified version of the Danish town sign (E 55) | MIT (as part of this project) |
| `src/DanskeByer/wwwroot/img/dannebrog.gif` | [Flag of Denmark-Animated.gif](https://commons.wikimedia.org/wiki/File:Flag_of_Denmark-Animated.gif) by MichaelFrey, Wikimedia Commons; used unmodified (the empty margin is cropped in CSS) | [CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/) (public domain) |
| `src/DanskeByer/wwwroot/audio/` (125 files: .mp3) | Synthetic speech generated by the author with Microsoft text-to-speech via edge-tts | Microsoft's terms: users must be told the voices are synthetic (the game says so at the bottom of the page and on the sound buttons), and the files must not be published or shared as an audio dataset or used to train or improve text-to-speech or voice models. **Not covered by the MIT License.** The same terms are in `audio/README.txt`. |
| The chime for a right answer | Generated in code (Web Audio API) in `wwwroot/js/byer.js`; no audio file | MIT (as part of this project) |

AI-generated text and audio were created for this project by the author. Purely AI-generated material may not be protected by copyright in some jurisdictions; to the extent it is, the licence in the table applies.

## Trademarks

Microsoft, Windows, .NET, Blazor and other Microsoft product names are trademarks of the Microsoft group of companies. Wikipedia and Wikimedia are trademarks of the Wikimedia Foundation. OpenStreetMap is a trademark of the OpenStreetMap Foundation. LEGO and LEGOLAND are trademarks of the LEGO Group. All other product names, logos and brands mentioned in this repository are the property of their respective owners. They are used only to identify the services, tools and places the project works with, and their use does not imply endorsement.
