"""
_corpus.py — the shared many-seed corpus (build item 18f-1): in-memory P1 prerolls, rolled once per test run and read
by every many-seed test whose dials it holds, instead of each test rolling its own 1,500 to 3,000 births.

The i-th birth depends on i alone (its seed `CORPUS-<i>` and its dials), so a test that asks for n births reads the
first n whoever asked first; the corpus grows on demand and lives as long as the test process, never on disk: every
birth is rolled from the tables and the code under test.

The dials go round every scale × magic × era × tone, every content mix of three and every danger; the start level goes
round every level band the scale's span allows (start = 1 + (i // 135) % (20 - span), the band [start, start + span]),
so a test that needs every band sees them. A birth whose pool runs empty is kept as an error, never skipped silently.

The births are shared: a test reads them and never changes them. Each read checks that no earlier reader changed one
(a digest of every birth's records, taken when it was rolled).
"""

import hashlib
import itertools
import json
import sys

from _campaign import SCRIPTS

sys.path.insert(0, str(SCRIPTS))
import design_tables as dt  # noqa: E402
import designer  # noqa: E402

SEEDS = 3000
SPAN = {"short": 4, "standard": 11, "epic": 19}
TAG = "CORPUS"

_births: list = []          # (dials, R); R is None for a birth that stopped on an empty pool
_errors: dict = {}          # i -> the stop's message
_digests: list = []


def _combos():
    return list(itertools.product(dt.dial_values("scale"), dt.dial_values("magic"), dt.dial_values("era"), dt.dial_values("tone")))


def dials(i: int) -> dict:
    """The i-th birth's dials."""
    combos = _combos()
    mixes = list(itertools.permutations(dt.dial_values("content_mix"), 3))
    dangers = dt.dial_values("danger")
    scale, magic, era, tone = combos[i % len(combos)]
    start = 1 + (i // len(combos)) % (20 - SPAN[scale])
    return {"scale": scale, "magic": magic, "era": era, "tone": tone, "danger": dangers[i % len(dangers)],
            "content_mix": list(mixes[i % len(mixes)]), "party_size": 2, "level_band": [start, start + SPAN[scale]]}


def _digest(R) -> str:
    if R is None:
        return ""
    keep = {"foundation": R.foundation, "identity": R.identity, "identity_secret": R.identity_secret, "threat": R.threat,
            "naming": R.naming, "public": R.public, "secret": R.secret, "pools": R.pools,
            "ctx": [R.ctx.rolled, R.ctx.tokens]}
    return hashlib.sha1(json.dumps(keep, sort_keys=True, default=str).encode("utf-8")).hexdigest()


def _check() -> None:
    changed = [i for i, (d, R) in enumerate(_births) if _digest(R) != _digests[i]]
    if changed:
        raise AssertionError(f"_corpus: {len(changed)} shared birth(s) changed by an earlier reader (first: #{changed[0]}); "
                             "a test reads the corpus and never writes into it")


def births(n: int = SEEDS) -> list[tuple[dict, object]]:
    """The first n births as (dials, R), R after `designer.preroll_p1`; the ones that stopped on an empty pool are left
    out (see `errors`)."""
    if _births:
        _check()
    while len(_births) < n:
        i = len(_births)
        d = dials(i)
        R = designer.Roller.in_memory(f"{TAG}-{i}", d)
        try:
            designer.preroll_p1(R, {"dials": d})
        except SystemExit as exc:
            _errors[i] = str(exc)
            R = None
        _births.append((d, R))
        _digests.append(_digest(R))
    return [(d, R) for d, R in _births[:n] if R is not None]


def errors(n: int = SEEDS) -> list[str]:
    """The stops of the first n births (an empty pool), in order."""
    births(n)
    return [e for i, e in sorted(_errors.items()) if i < n]
