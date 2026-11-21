# Generates the app / home-screen icons for Danske Byer: the game's map of Denmark (from
# src\DanskeByer\wwwroot\data\denmark.json, without Bornholm) with red town dots, and a waving Dannebrog
# on a pole standing at Aarhus.
# Run with Windows PowerShell (System.Drawing):  powershell -File tools\make-icons.ps1
param(
    [string]$OutDir = (Join-Path $PSScriptRoot "..\src\DanskeByer\wwwroot\icons"),
    # The front page (KidsGames) shows each game's 512 px icon. Pass its billeder folder to copy it there,
    # e.g. -FrontPageDir ..\KidsGames\billeder
    [string]$FrontPageDir = ""
)

Add-Type -AssemblyName System.Drawing
New-Item -ItemType Directory -Force $OutDir | Out-Null

function Color([string]$hex) { [System.Drawing.ColorTranslator]::FromHtml($hex) }
function Brush([string]$hex) { New-Object System.Drawing.SolidBrush (Color $hex) }
function PointF([float]$x, [float]$y) { New-Object System.Drawing.PointF $x, $y }

# ---- The map: the same outline and projection as the game ----
$shape = Get-Content (Join-Path $PSScriptRoot "..\src\DanskeByer\wwwroot\data\denmark.json") -Raw | ConvertFrom-Json
function MapX([double]$lon) { ($lon - $shape.lon0) * $shape.kx }
function MapY([double]$lat) { ($shape.lat0 - $lat) * $shape.ky }

# Everything east of 13° E is Bornholm; leave it out so the rest of the country can be bigger.
$maxX = MapX 13.0
$rings = @()
foreach ($part in $shape.path.Split('M', [StringSplitOptions]::RemoveEmptyEntries)) {
    $pts = foreach ($xy in $part.TrimEnd('Z').Split('L')) {
        $c = $xy.Split(' ')
        PointF ([float]::Parse($c[0], [Globalization.CultureInfo]::InvariantCulture)) ([float]::Parse($c[1], [Globalization.CultureInfo]::InvariantCulture))
    }
    if (($pts | Measure-Object -Property X -Maximum).Maximum -lt $maxX) { $rings += , [System.Drawing.PointF[]]$pts }
}
$allX = $rings | ForEach-Object { $_ } | ForEach-Object { $_.X } | Measure-Object -Minimum -Maximum
$allY = $rings | ForEach-Object { $_ } | ForEach-Object { $_.Y } | Measure-Object -Minimum -Maximum
$mapW = $allX.Maximum - $allX.Minimum
$mapH = $allY.Maximum - $allY.Minimum

# Towns shown as dots (lon, lat, size) and where the flag pole stands (Aarhus).
$dots = @(
    @(12.5683, 55.6761, 1.25),   # København
    @(10.3883, 55.3959, 1.0),    # Odense
    @(9.9217, 57.0488, 1.0),     # Aalborg
    @(8.4590, 55.4760, 0.9)      # Esbjerg
)
$pole = @(10.2039, 56.1629)

# A rectangle of the flag (in flag units 0..1) mapped onto the waving cloth.
function Map-Cloth([float]$u0, [float]$v0, [float]$u1, [float]$v1, $cloth) {
    $n = 24
    $pts = New-Object System.Collections.Generic.List[System.Drawing.PointF]
    for ($i = 0; $i -le $n; $i++) { $pts.Add((& $cloth ($u0 + ($u1 - $u0) * $i / $n) $v0)) }
    for ($i = 0; $i -le $n; $i++) { $pts.Add((& $cloth $u1 ($v0 + ($v1 - $v0) * $i / $n))) }
    for ($i = $n; $i -ge 0; $i--) { $pts.Add((& $cloth ($u0 + ($u1 - $u0) * $i / $n) $v1)) }
    for ($i = $n; $i -ge 0; $i--) { $pts.Add((& $cloth $u0 ($v0 + ($v1 - $v0) * $i / $n))) }
    return $pts.ToArray()
}

# content: 1.0 = full size, 0.78 = keep inside the maskable safe zone
function Draw-Icon([int]$size, [string]$file, [float]$content = 1.0, [bool]$detail = $true) {
    $S = [float]$size
    $bmp = New-Object System.Drawing.Bitmap $size, $size
    $g = [System.Drawing.Graphics]::FromImage($bmp)
    $g.SmoothingMode = 'AntiAlias'

    # Background: deep sea blue, like the sea on the game's map (full square, iOS applies its own rounded mask)
    $bg = New-Object System.Drawing.Drawing2D.LinearGradientBrush (PointF 0 0), (PointF 0 $S), (Color '#1c7ed6'), (Color '#0b3d6e')
    $g.FillRectangle($bg, 0, 0, $S, $S)

    # Fit the map into the lower left of the icon; the flag waves in the space above Sjælland.
    $box = $S * 0.74 * $content
    $k = $box / [Math]::Max($mapW, $mapH)
    $ox = ($S - $mapW * $k) / 2 - $allX.Minimum * $k - $S * 0.07 * $content
    $oy = ($S - $mapH * $k) / 2 - $allY.Minimum * $k + $S * 0.06 * $content
    $toIcon = { param([float]$x, [float]$y) PointF ($ox + $x * $k) ($oy + $y * $k) }

    $land = New-Object System.Drawing.Drawing2D.GraphicsPath ([System.Drawing.Drawing2D.FillMode]::Alternate)
    foreach ($ring in $rings) {
        $land.AddPolygon([System.Drawing.PointF[]]($ring | ForEach-Object { & $toIcon $_.X $_.Y }))
    }

    $drop = $S * 0.022
    # The favicon is too small for the map's coastline; it shows only the flag, filling the icon.
    if ($detail) {
    # The flat "3D" shadow the games use under cards, then land with its coastline.
    $shadow = $land.Clone()
    $m = New-Object System.Drawing.Drawing2D.Matrix
    $m.Translate(0, $drop)
    $shadow.Transform($m)
    $g.FillPath((New-Object System.Drawing.SolidBrush ([System.Drawing.Color]::FromArgb(56, 59, 42, 99))), $shadow)
    $g.FillPath((Brush '#fff9db'), $land)
    $coast = New-Object System.Drawing.Pen (Color '#c9b458'), ([Math]::Max(1.0, $S * 0.0045))
    $coast.LineJoin = 'Round'
    $g.DrawPath($coast, $land)

    foreach ($d in $dots) {
        $p = & $toIcon (MapX $d[0]) (MapY $d[1])
        $r = $S * 0.027 * $d[2] * $content
        $g.FillEllipse((Brush '#ffffff'), $p.X - $r * 1.35, $p.Y - $r * 1.35, $r * 2.7, $r * 2.7)
        $g.FillEllipse((Brush '#c8102e'), $p.X - $r, $p.Y - $r, 2 * $r, 2 * $r)
    }
    }

    # ---- The flag on its pole ----
    if ($detail) {
        $base = & $toIcon (MapX $pole[0]) (MapY $pole[1])
        $poleH = $S * 0.40 * $content
        $poleW = $S * 0.026 * $content
        $fw = $S * 0.36 * $content
    }
    else {
        $base = PointF ($S * 0.14) ($S * 0.97)
        $poleH = $S * 0.80
        $poleW = $S * 0.07
        $fw = $S * 0.78
    }
    $top = $base.Y - $poleH
    $fh = $fw * 28 / 37
    $amp = $fh * 0.09
    $fx = $base.X + $poleW / 2
    $fy = $top + $S * 0.02 * $content
    # u along the flag (0 at the pole), v down; the wave grows away from the pole.
    $cloth = { param([float]$u, [float]$v) PointF ($fx + $u * $fw) ($fy + $v * $fh + $amp * $u * [Math]::Sin($u * 2 * [Math]::PI * 1.1)) }

    $flagShadow = Map-Cloth 0 0 1 1 $cloth | ForEach-Object { PointF $_.X ($_.Y + $drop) }
    $g.FillPolygon((New-Object System.Drawing.SolidBrush ([System.Drawing.Color]::FromArgb(56, 59, 42, 99))), [System.Drawing.PointF[]]$flagShadow)
    $g.FillPolygon((Brush '#c8102e'), (Map-Cloth 0 0 1 1 $cloth))
    $white = Brush '#ffffff'
    $g.FillPolygon($white, (Map-Cloth (12 / 37) 0 (16 / 37) 1 $cloth))
    $g.FillPolygon($white, (Map-Cloth 0 (12 / 28) 1 (16 / 28) $cloth))

    # Pole with a gold knob and a small foot where it stands in the ground.
    $g.FillEllipse((New-Object System.Drawing.SolidBrush ([System.Drawing.Color]::FromArgb(70, 59, 42, 99))), $base.X - $poleW * 2.2, $base.Y - $poleW * 0.7, $poleW * 4.4, $poleW * 1.4)
    $g.FillRectangle((Brush '#5f5577'), $base.X - $poleW / 2, $top, $poleW, $poleH)
    $knob = $poleW * 1.15
    $g.FillEllipse((Brush '#f59f00'), $base.X - $knob, $top - $knob * 1.6, 2 * $knob, 2 * $knob)
    $g.FillEllipse((Brush '#fcc419'), $base.X - $knob * 0.8, $top - $knob * 1.65, 1.6 * $knob, 1.6 * $knob)

    $g.Dispose()
    $bmp.Save((Join-Path $OutDir $file), [System.Drawing.Imaging.ImageFormat]::Png)
    $bmp.Dispose()
    Write-Host "  $file"
}

Write-Host "Writing icons to $OutDir"
Draw-Icon 180  'apple-touch-icon.png'
Draw-Icon 167  'apple-touch-icon-167.png'
Draw-Icon 152  'apple-touch-icon-152.png'
Draw-Icon 192  'icon-192.png'
Draw-Icon 512  'icon-512.png'
Draw-Icon 1024 'icon-1024.png'
Draw-Icon 512  'icon-512-maskable.png' 0.78
Draw-Icon 32   'favicon-32.png' 1.0 $false

if ($FrontPageDir -and (Test-Path $FrontPageDir)) {
    Copy-Item (Join-Path $OutDir 'icon-512.png') (Join-Path $FrontPageDir 'danskebyer.png')
    Write-Host "Copied icon-512.png to $FrontPageDir\danskebyer.png"
}
