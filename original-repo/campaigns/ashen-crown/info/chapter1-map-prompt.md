# Chapter 1 Map — Gemini Image Generation Prompt

Research basis: `gazetteer.md`'s Regional Topography table, `campaign-clock.md`'s travel-time table, and explicit compass references scattered across location files (see `system-register.md`, 2026-08-29 entry, for the confidence-flagged research this prompt is built from).

---

## The prompt (paste as-is into Gemini)

```
Create a clean, simple fantasy campaign map in the style of a tabletop RPG reference map — clear and easy to read at a glance, NOT a densely-illustrated parchment map. Top-down view, north at the top, with a compass rose in one corner and a small legend explaining terrain colors.

The map shows five connected regions arranged from south to north, each with a distinct elevation and terrain color band (this is important — use visibly different shading/color per band so elevation is obvious without reading labels):

1. SOUTH — "The Marches": lowland, sea level to low hills. Color: muddy green-brown, marshland texture. A river runs through this region toward a coastline at the southern/southwestern edge. Show a coastal fishing village ("Nettlecombe") near the coast, a river-crossing town ("Sallow Ford") to the west, and the main town ("Gallowmere") as the region's central hub, roughly inland-center. West of Gallowmere, mark a marsh with a ruined tower icon ("The Weeping Tower"). A road runs north from Gallowmere toward the next region.

2. NORTH OF THE MARCHES — "The Thornlands": low rolling hills, farmland color (warm green, hedgerow texture, small farm-plot patterns). Place two settlements very close together near the region's center ("Thornwick" and "Harrowgate," barely half a day apart — draw them near-adjacent). East of Harrowgate, on a ridge, mark a ruined fortified manor ("Shestendeliath Hold"). Between Thornwick and Harrowgate, mark a forest icon ("The Weeping Wood").

3. NORTH OF THE THORNLANDS — "The Cindermoor": a visibly HIGHER elevation plateau — use grey/muted color with contour-line hachures to show the climb up from the Thornlands' green. Treeless, windswept moor texture, with one or two small hidden lake icons. Place an isolated village icon ("Cair Dunnow") and ancient ruin icons for barrows and rocky crags.

4. BEYOND THE CINDERMOOR — "Karsgate": a major walled city, drawn distinctly larger than other settlements, sitting where the elevation drops back DOWN to a river valley (show the contour lines descending from the Cindermoor plateau into this valley). The city sits on a river. Show a handful of small site icons clustered just outside the city walls (representing nearby minor locations).

5. NORTH OF KARSGATE — "The Ashvale": elevation rises AGAIN — pale chalk-white/tan color, chalk downland texture (rolling bare hills, no forest), visibly higher than Karsgate's valley. Place a walled fortress-town icon ("Ironhold") and, further into this region, a large tomb/necropolis icon ("Ashvale Necropolis").

Connect all major settlements with a simple road-line network. Show the overall shape as a south-to-north ascent, descent into the river valley, then ascent again — the elevation shading should make this journey visually obvious even without reading any labels.

Style: clean vector-illustration cartography, muted natural color palette, legible sans-serif labels, minimal decoration, no heavy ornamentation or parchment-aging effects — this is a reference map meant to be read quickly, not a decorative art piece.
```

---

---

## v2 — corrective prompt (after reviewing the first generated map)

The first generation was directionally correct (Sallow Ford west of Gallowmere, Shestendeliath Hold east of Harrowgate, the Weeping Wood between Thornwick and Harrowgate, Karsgate reached by a separate route rather than through the Cindermoor, Ashvale correctly north of Karsgate) but had three real problems: **Millward Crossing was missing entirely** despite being the campaign's current active location, the **legend contradicted the map body** with two invented names ("Gowarn farmland," "The Thornmoor" instead of "The Cindermoor"), and the **Cindermoor's elevation was ambiguous** — its concentric rings could read as a basin instead of the raised plateau it's supposed to be.

Paste this as a fresh generation (not an edit of the old image — safer for a model that doesn't reliably do targeted in-place edits):

```
Create a clean, simple fantasy campaign map in the style of a tabletop RPG reference map — clear and easy to read at a glance, NOT a densely-illustrated parchment map. Top-down view, north at the top, with a compass rose in one corner.

The map shows five connected regions arranged from south to north, each with a distinct elevation and terrain color band (use visibly different shading/color per band so elevation is obvious without reading labels):

1. SOUTH — "The Marches": lowland, sea level to low hills. Color: muddy green-brown, marshland texture. A river runs through this region toward a coastline at the southern/southwestern edge. Show a coastal fishing village ("Nettlecombe") near the coast, a river-crossing town ("Sallow Ford") to the west, and the main town ("Gallowmere") as the region's central hub, roughly inland-center. West of Gallowmere, mark a marsh with a ruined tower icon ("The Weeping Tower"). A road runs north from Gallowmere toward the next region.

2. NORTH OF THE MARCHES — "The Thornlands": low rolling hills, farmland color (warm green, hedgerow texture, small farm-plot patterns). Place two settlements very close together near the region's center ("Thornwick" and "Harrowgate," barely half a day apart — draw them near-adjacent). East of Harrowgate, on a ridge, mark a ruined fortified manor ("Shestendeliath Hold"). Between Thornwick and Harrowgate, mark a forest icon ("The Weeping Wood"). On the road heading northeast from Harrowgate, roughly midway toward Karsgate, mark a small waypoint icon — a lone chapel — labeled "Millward Crossing."

3. NORTH OF THE THORNLANDS — "The Cindermoor": a visibly HIGHER elevation plateau — this must read clearly as land RISING UP, not sinking into a basin. Use a grey/muted color, and draw the contour hachures as short lines radiating outward and downward FROM the plateau's edge toward the lowlands, like a raised tableland or mesa — the opposite of crater/basin shading. Treeless, windswept moor texture on top, with one or two small hidden lake icons. Place an isolated village icon ("Cair Dunnow") and ancient ruin icons for barrows and rocky crags.

4. BEYOND THE CINDERMOOR — "Karsgate": a major walled city, drawn distinctly larger than other settlements, reached by its own road running northeast from Harrowgate/Millward Crossing (a separate route from the Cindermoor, not through it), sitting where the elevation drops back DOWN to a river valley. The city sits on a river. Show a handful of small site icons clustered just outside the city walls.

5. NORTH OF KARSGATE — "The Ashvale": elevation rises AGAIN — pale chalk-white/tan color, chalk downland texture (rolling bare hills, no forest), visibly higher than Karsgate's valley. Place a walled fortress-town icon ("Ironhold") and, further into this region, a large tomb/necropolis icon ("Ashvale Necropolis").

Connect all major settlements with a simple road-line network. Show the overall shape as a south-to-north ascent, descent into the river valley, then ascent again.

Add a small legend box in a corner with exactly these four entries and no others, matching the region names used on the map body exactly: "Marshland" (The Marches' color), "Thornlands Farmland" (The Thornlands' color), "The Cindermoor" (the plateau's color), "Chalk Downland" (The Ashvale's color). Do not invent alternate names for any region — the legend must use the same names as the labels drawn on the map itself.

Style: clean vector-illustration cartography, muted natural color palette, legible sans-serif labels, minimal decoration, no heavy ornamentation or parchment-aging effects — this is a reference map meant to be read quickly, not a decorative art piece.
```

---

---

## v3 — flat map, no topography (after two attempts both dropped Millward Crossing and produced a broken/wrong legend)

Two generations in a row lost the same three things: a "minor" waypoint (Millward Crossing), precise legend text, and any reliable sense of "up vs. down" from contour lines alone. The DM's own read: the topographic instructions may be consuming the model's attention/detail budget at the expense of the things that actually matter more (correct settlements, correct positions). This version drops elevation/topography entirely — flat, simple, direction-accurate only.

```
Create a clean, simple flat fantasy campaign map in the style of a tabletop RPG reference map — top-down view, north at the top, with a clear compass rose (N, E, S, W all labeled) in one corner. Do NOT use elevation shading, contour lines, hachures, or any "raised/lowered terrain" effect — flat, evenly-lit regions only, distinguished by simple flat color fill and a light terrain texture pattern (not by implying height).

Five regions, arranged south to north, each a simple flat color:

1. SOUTH — "The Marches" (muddy green-brown, light marsh-grass texture, flat). A river runs through it to a coastline at the south/southwest edge. Settlements: "Nettlecombe" (small coastal fishing village, near the coast), "Sallow Ford" (river-crossing town, west side of the region), "Gallowmere" (the region's main town, central). West of Gallowmere: a ruined tower icon labeled "The Weeping Tower," in marsh. A road connects Sallow Ford, Gallowmere, and continues north.

2. NORTH OF THE MARCHES — "The Thornlands" (warm green, light farmland/hedgerow texture, flat). Two settlements close together near the center: "Thornwick" and "Harrowgate" (draw them near-adjacent, connected by a very short road). East of Harrowgate: a ruined fortified manor icon labeled "Shestendeliath Hold," connected by road. Between Thornwick and Harrowgate: a forest icon labeled "The Weeping Wood." **On the road heading northeast from Harrowgate toward Karsgate, place a settlement icon of the SAME size and label weight as Thornwick or Sallow Ford — do not make it small or optional — labeled "Millward Crossing."**

3. NORTH OF THE THORNLANDS — "The Cindermoor" (flat grey, light moor/heather texture, no contour lines, no elevation implication — just a different flat color from its neighbors). Settlements/sites: "Cair Dunnow" (isolated village icon), plus small ruin icons for barrows and rocky crags, and one or two small lake icons.

4. BEYOND THE CINDERMOOR — "Karsgate": a major walled city icon, drawn distinctly larger than any other settlement, reached by its own road from Millward Crossing (a separate route from the Cindermoor, not through it). The city sits on a river.

5. NORTH OF KARSGATE — "The Ashvale" (flat pale tan/chalk color, light rolling-hill texture, no elevation implication). Settlements: "Ironhold" (walled fortress-town icon), and further into the region, "Ashvale Necropolis" (large tomb/necropolis icon).

Connect all named settlements with a simple road-line network, matching the connections described above. Every named settlement listed here — including Millward Crossing — must appear as a clearly labeled icon of comparable size to the others; none should be tiny, faint, or omitted.

Keep the legend minimal and simple: five color swatches only, one per region, each labeled with EXACTLY the region name used on the map body ("The Marches," "The Thornlands," "The Cindermoor," "Karsgate," "The Ashvale") — no additional invented categories, no other terrain labels.

Style: clean flat vector-illustration cartography, muted natural color palette, legible sans-serif labels, minimal decoration — a reference map meant to be read quickly.
```

---

## Notes on the research behind this prompt

- **Explicit distances/directions used**: Sallow Ford (2 days west of Gallowmere), the Weeping Tower (west of Gallowmere, marsh), the Ash-Kilns (upriver/north of Gallowmere), Shestendeliath Hold (1 day east of Harrowgate, on a ridge), the Weeping Wood (directly between Thornwick and Harrowgate), Thornwick↔Harrowgate (½ day, drawn near-adjacent).
- **One resolved inconsistency**: Harrowgate→Millward Crossing (on the Karsgate road) is 4-5 days, but Gallowmere→Karsgate direct is only ~7 days total — these don't reconcile if Karsgate is simply "north of Harrowgate," since Gallowmere→Harrowgate alone is already ~5 days via Thornwick. Resolution: the party's actual routes were deliberately indirect (back-roads, avoiding main routes for stealth, confirmed repeatedly in `campaign-clock.md`'s day-by-day log) — the direct road bypasses Harrowgate/Thornwick at an angle. The map reflects the direct/implied road network, not the party's specific longer path.
- **Deliberately simplified for readability**: the full location list has 30+ named sites across five regions (see `gazetteer.md`). Per the DM's own request for a "simple, clear" map, this prompt surfaces only major settlements and a few plot-critical or already-visited sites, not every dungeon/minor site — a full 1:1 map would be unreadably cluttered at this scale.
- **Elevation is the throughline**: `gazetteer.md`'s own Regional Topography table (2026-08-28) explicitly frames Chapter 1 as "a real ascent, not a flat crawl" — lowland Marches → high Cindermoor plateau → river-valley Karsgate → chalk-highland Ashvale. The prompt's repeated instruction to show elevation via color/contour is designed to make this literal shape visible on the map itself.
