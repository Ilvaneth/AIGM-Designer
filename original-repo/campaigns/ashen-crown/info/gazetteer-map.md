# Gazetteer Map — reference image and prompt

A player-facing regional map, generated externally (Gemini) from confirmed geography in `gazetteer.md` and `campaign-clock.md`'s travel table only — no campaign secrets, no party-specific content. Built 2026-08-25 at the DM's request, for showing to the table when useful.

**Status**: final, corrected prompt below produced a verified-accurate map (checked against every confirmed distance/direction in `gazetteer.md`). If regenerating, use this version — the first draft had Sallow Ford and the Weeping Tower's distances from Gallowmere reversed; this one has them right.

**Image file**: `info/images/Ashen_Crown_MAP.png` — the verified-accurate version, saved 2026-08-25, moved into `info/images/` session 9 (2026-08-30) alongside the new Shestendeliath Hold reference image. Show this when the table asks to see the map; don't regenerate unless the geography changes.

---

## The prompt

A hand-drawn fantasy world map in the style of old parchment cartography — sepia and faded ink tones, compass rose in a corner, decorative border, small illustrated mountains/trees/waves for terrain, aged paper texture.

Layout, south at the bottom of the map, north at the top:

SOUTH (bottom of map):
- A border region called "The Marches" — poor, crowded lowland country along a river. Mark a town called "Gallowmere" as the central settlement of this region, on the river.
- In marshland close to Gallowmere (the nearer of the two western landmarks, roughly half the distance to the next one), mark a small isolated tower labeled "The Weeping Tower."
- Farther west of Gallowmere than the Weeping Tower, mark a river-crossing town called "Sallow Ford."
- A short distance downriver (south) from Gallowmere, mark a ruined mill labeled "The Drowned Mill," and further downriver a small fishing hamlet labeled "Nettlecombe."

NORTH OF THE MARCHES (middle of the map):
- A region of farmland, hedgerows, and small villages called "The Thornlands," directly north of the Marches region.
- Within the Thornlands, mark a village called "Thornwick."
- Close to Thornwick, mark a larger market town called "Harrowgate."

FAR NORTH (top of the map, vaguer/less detailed, fading into unmapped terrain):
- A stretch of chalky highlands labeled "The Ashvale," somewhere north of the central regions.
- Beyond that, wild broken terrain fading into the edge of the map, labeled "The Sundered Reach — beyond the kingdom's writ," drawn with a rougher, less certain linework as if the mapmaker had less information this far out.

Leave the northeast/east portion of the map mostly blank or lightly sketched with "unknown lands" or trailing dotted lines, since a walled city ("Karsgate") and other regions exist somewhere out there but their exact position was never fixed by the mapmaker.

Style notes: no modern elements, no text besides the labels listed above, muted earthy color palette, the overall feel of a well-worn map a traveler would actually carry — detailed and confident in the south near Gallowmere, progressively sparser and more speculative toward the north and east.

---

## What's deliberately left unfixed

Per `gazetteer.md`'s own philosophy ("better to have room than a locked answer"), these were never pinned down and the map correctly leaves them out: Karsgate's exact position and distance from Gallowmere, the Cindermoor's position relative to everything else, Emberhold's position. If any of these get fixed in play later, this file and the prompt should be updated to match before regenerating.
