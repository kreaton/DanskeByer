#!/usr/bin/env python3
"""Builds a detailed coastline for a small area (the København zoom) from OpenStreetMap.

The country outline in denmark.json (Natural Earth) is far too coarse when the map zooms in on
the inner city: the harbour is missing and the sights end up in the sea. This turns OSM coastline
ways into land polygons for one box, in the same projection as denmark.json, and writes them to
details.json. The game draws a detail instead of the country outline when the view fits inside it.

1. Fetch the coastline (Overpass), e.g. for København:
     curl -A "DanskeByer-mapdata/1.0" --data-urlencode 'data=[out:json][timeout:90];way["natural"="coastline"](55.60,12.42,55.76,12.74);out geom;' https://overpass-api.de/api/interpreter -o coast.json
2. python tools/gen_detail.py coast.json src/DanskeByer/wwwroot/data

Map data © OpenStreetMap contributors, ODbL 1.0 (https://www.openstreetmap.org/copyright).
"""
import json, math, sys, pathlib

COAST = pathlib.Path(sys.argv[1])
OUT = pathlib.Path(sys.argv[2])

# The box the detail covers (a little larger than the København view, so the letterbox is covered too).
LON_MIN, LON_MAX, LAT_MIN, LAT_MAX = 12.44, 12.72, 55.615, 55.745
TOLERANCE = 0.015   # simplification, in map units (1 unit ≈ 370 m north–south, so ≈ 5 m)

shape = json.loads((OUT / "denmark.json").read_text(encoding="utf-8"))
X = lambda lon: (lon - shape["lon0"]) * shape["kx"]
Y = lambda lat: (shape["lat0"] - lat) * shape["ky"]

# ---- 1. Join the ways into chains (OSM coastline has the land on its left) ----
ways = [w for w in json.loads(COAST.read_text(encoding="utf-8"))["elements"] if w["type"] == "way"]
chains = [(w["nodes"], [(p["lon"], p["lat"]) for p in w["geometry"]]) for w in ways]
merged = True
while merged:
    merged = False
    by_start = {c[0][0]: i for i, c in enumerate(chains)}
    for i, (nodes, pts) in enumerate(chains):
        if nodes[0] == nodes[-1]:
            continue
        j = by_start.get(nodes[-1])
        if j is not None and j != i:
            n2, p2 = chains[j]
            chains[i] = (nodes + n2[1:], pts + p2[1:])
            del chains[j]
            merged = True
            break

# ---- 2. Clip each chain to the box ----
def inside(p):
    return LON_MIN <= p[0] <= LON_MAX and LAT_MIN <= p[1] <= LAT_MAX

def clip_segment(a, b):
    """Liang–Barsky: the part of a→b inside the box, or None."""
    t0, t1 = 0.0, 1.0
    dx, dy = b[0] - a[0], b[1] - a[1]
    for p, q in ((-dx, a[0] - LON_MIN), (dx, LON_MAX - a[0]), (-dy, a[1] - LAT_MIN), (dy, LAT_MAX - a[1])):
        if p == 0:
            if q < 0: return None
        else:
            t = q / p
            if p < 0: t0 = max(t0, t)
            else: t1 = min(t1, t)
    if t0 > t1: return None
    return (a[0] + t0 * dx, a[1] + t0 * dy), (a[0] + t1 * dx, a[1] + t1 * dy), t0 > 0, t1 < 1

rings, pieces = [], []
for nodes, pts in chains:
    closed = nodes[0] == nodes[-1]
    if closed and all(inside(p) for p in pts):
        rings.append(pts)
        continue
    cur = None
    for a, b in zip(pts, pts[1:]):
        c = clip_segment(a, b)
        if c is None:
            continue
        s, e, enters, leaves = c
        if cur is None:
            cur = [s]
        cur.append(e)
        if leaves:
            pieces.append(cur)
            cur = None
    if cur is not None:
        pieces.append(cur)

# A piece that starts or ends inside the box would come from an unclosed chain at the edge of the
# downloaded area; the download is larger than the box, so every piece should run border to border.
for p in pieces:
    for q in (p[0], p[-1]):
        on_edge = min(abs(q[0] - LON_MIN), abs(q[0] - LON_MAX), abs(q[1] - LAT_MIN), abs(q[1] - LAT_MAX)) < 1e-9
        if not on_edge:
            sys.exit(f"ERROR: coastline piece ends inside the box at {q}; download a larger area")

# ---- 3. Close the pieces along the box, counter-clockwise (land stays on the left) ----
W, H = LON_MAX - LON_MIN, LAT_MAX - LAT_MIN
def perimeter(p):
    """Position on the box edge, counter-clockwise from the south-west corner (0..4)."""
    x, y = p
    if abs(y - LAT_MIN) < 1e-9 and x < LON_MAX: return (x - LON_MIN) / W
    if abs(x - LON_MAX) < 1e-9 and y < LAT_MAX: return 1 + (y - LAT_MIN) / H
    if abs(y - LAT_MAX) < 1e-9 and x > LON_MIN: return 2 + (LON_MAX - x) / W
    return 3 + (LAT_MAX - y) / H
CORNERS = [(1, (LON_MAX, LAT_MIN)), (2, (LON_MAX, LAT_MAX)), (3, (LON_MIN, LAT_MAX)), (4, (LON_MIN, LAT_MIN))]

def corners_between(a, b):
    """Box corners passed when walking counter-clockwise from perimeter position a to b."""
    out, t = [], a
    dist = (b - a) % 4
    for k in range(1, 5):
        c = math.floor(a) + k
        if c - a <= 0 or c - a >= dist: continue
        out.append(CORNERS[(c - 1) % 4][1])
    return out

remaining = pieces[:]
while remaining:
    start = remaining.pop(0)
    ring = list(start)
    cur = start
    while True:
        exit_t = perimeter(cur[-1])
        options = remaining + [start]
        nxt = min(options, key=lambda p: ((perimeter(p[0]) - exit_t) % 4) or 4)
        ring += corners_between(exit_t, perimeter(nxt[0]))
        if nxt is start:
            break
        ring += nxt
        remaining.remove(nxt)
        cur = nxt
    rings.append(ring)

# ---- 4. Project, simplify, write ----
def simplify(pts, tol):
    if len(pts) < 3: return pts
    keep = [False] * len(pts); keep[0] = keep[-1] = True
    stack = [(0, len(pts) - 1)]
    while stack:
        i, j = stack.pop()
        (ax, ay), (bx, by) = pts[i], pts[j]
        L = math.hypot(bx - ax, by - ay)
        best, k = -1.0, -1
        for m in range(i + 1, j):
            # A closed ring starts and ends at the same point: measure from that point instead of a line.
            d = (abs((bx - ax) * (ay - pts[m][1]) - (ax - pts[m][0]) * (by - ay)) / L if L > 1e-12
                 else math.hypot(pts[m][0] - ax, pts[m][1] - ay))
            if d > best: best, k = d, m
        if best > tol:
            keep[k] = True
            stack += [(i, k), (k, j)]
    return [p for p, f in zip(pts, keep) if f]

parts, npts = [], 0
for ring in rings:
    pts = simplify([(X(lo), Y(la)) for lo, la in ring], TOLERANCE)
    if len(pts) < 3: continue
    npts += len(pts)
    parts.append("M" + "L".join(f"{x:.2f} {y:.2f}" for x, y in pts) + "Z")

detail = dict(name="København", lonMin=LON_MIN, lonMax=LON_MAX, latMin=LAT_MIN, latMax=LAT_MAX,
              path="".join(parts), credit="Kort: © OpenStreetMap-bidragydere")
(OUT / "details.json").write_text(json.dumps([detail], ensure_ascii=False), encoding="utf-8")
print(f"{len(rings)} land polygons, {npts} points, {len(detail['path'])} bytes")
