"""
_floor.py — the floor (build item 7c, inspection): roll many seeds of P1 in memory and report each table's smallest
pool after the constraints. For a table whose rows are not drawn again across campaigns (`avoid_used`), a pool under
five is a failure; tables whose rows may repeat (the tie, the time, the palette) are exempt.
"""

import itertools
import sys

from _campaign import SCRIPTS

sys.path.insert(0, str(SCRIPTS))
import design_tables as dt  # noqa: E402
import designer  # noqa: E402

SPAN = {"short": 4, "standard": 11, "epic": 19}
FLOOR = 5


def dial_sets():
    eras = dt.dial_values("era")
    return list(itertools.product(dt.dial_values("scale"), dt.dial_values("magic"), eras, dt.dial_values("tone")))


def smallest_pools(seeds: int = 900, tag: str = "FLOOR") -> dict:
    """{table ref: the smallest pool any draw of it saw after the constraints} over `seeds` in-memory P1 prerolls."""
    combos = dial_sets()
    mixes = list(itertools.permutations(dt.dial_values("content_mix"), 3))
    out: dict = {}
    for i in range(seeds):
        scale, magic, era, tone = combos[i % len(combos)]
        dials = {"scale": scale, "magic": magic, "era": era, "tone": tone, "content_mix": list(mixes[i % len(mixes)]),
                 "party_size": 2, "level_band": [1, 1 + SPAN[scale]]}
        R = designer.Roller.in_memory(f"{tag}-{i}", dials)
        designer.preroll_p1(R, {"dials": dials})
        for ref, n in R.pools.items():
            out[ref] = min(out.get(ref, n), n)
    return out


def unique(ref: str) -> bool:
    """A table whose rows are not drawn again across campaigns."""
    return bool(dt.roll_header(ref).get("avoid_used"))


def under_the_floor(pools: dict) -> dict:
    return {ref: n for ref, n in pools.items() if unique(ref) and n < FLOOR}
