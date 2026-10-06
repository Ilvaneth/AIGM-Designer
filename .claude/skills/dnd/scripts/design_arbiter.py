#!/usr/bin/env python3
"""
design_arbiter.py — the script is the only arbiter of conflicts (plan item 25, "Common rules";
docs/p1-foundation-rows.md §13, with the owner's corrections of 2026-09-28).

Every table draw a phase makes is filtered here before the die is thrown; the model arbitrates nothing.

Two classes of exclusion, applied in this order:

1. **Constraints** — a row the caller excludes (`exclude`, a `where` predicate), a `forbidden: true` row that no
   rolled row in its `allowed_via` list admits, a row whose `requires` condition does not hold, a row whose
   total weight is zero, and a row that conflicts with any row rolled before it. Conflicts are symmetric: a row
   A listing B in `conflicts_with` also bars B after A (`design_tables.conflict_index()`). A pool the
   constraints empty is a table fault: `EmptyPool` is raised and the preroll stops; a conflicting row is never
   kept.
2. **Usage** — rows another campaign drew (`used_elsewhere`, the tables' `avoid_used`), rows of a family the last
   N births drew (`family_wait`), rows the last N births drew (`row_wait`), and values a caller marks spent (a
   target + action pair that never repeats, `pair`). Usage never stops a draw: when it empties the pool it is
   relaxed one kind at a time, in FALLBACK_ORDER (family_wait, then used_elsewhere, then row_wait, the pair
   last), stopping as soon as a row is left; the record names what was dropped (`usage_fallback`).

Every exclusion is logged with its reason. An exclusion on a public record that names a secret row (a row
rolled secretly, or any row of a table whose roll header says `secret: true`) is moved to the secret side, so
the public dice log never tells the owner, who is also the player, what the secret layer holds. The die's size
would tell it too: a public record's notation and face are counted over the rows not publicly excluded (the
pool plus the secretly excluded rows, `visible`), and the real size and face go to the secret side
(`public_view`).

Conditions (`requires`, `weight_by[].when`) are a mapping whose keys must all hold, or a list of such mappings
of which one must hold:

    requires: {dial: {magic: [medium, high], era: [underground]}}   the dial's value is in the list
    requires: {any_of: [land_thin_place]}                            one of these rows was rolled
    requires: {all_of: [...]} / {none_of: [...]}                     all / none of these rows were rolled
    requires: {all: [{any_of: [...]}, {any_of: [...]}]}              every sub-condition holds (one of these AND one of those)
    requires: {any: [<condition>, ...]}                              one sub-condition holds
    weight_by: [{when: {dial: {era: [nautical]}}, x: 3}]             weight × 3 while the condition holds

Claims (build item 7c). A rolled row's `claims` enter the context as tokens `claim:<topic>=<value>`; the dial rows'
claims enter when the context is built. A row conflicts with every token whose claim clashes with one of its own
(claims.yaml declares the clashes pair by pair), through the same symmetric conflict index. `any_of`, `all_of`,
`none_of`, `conflicts_with` and `weight_by` may name a token as they name a row. A token set by a secret row is
secret: an exclusion that names it goes to the secret side.
"""

from __future__ import annotations

import os
import random
import sys
from dataclasses import dataclass, field

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import design_tables as dt  # noqa: E402

CONDITION_KEYS = ("dial", "any_of", "all_of", "none_of", "all", "any")
USAGE_ORDER = ("used_elsewhere", "row_wait", "pair", "family_wait")   # the order a row's reason is named in
FALLBACK_ORDER = ("family_wait", "used_elsewhere", "row_wait", "pair")  # the order usage is relaxed in, the pair last


class EmptyPool(Exception):
    """The constraints left no row: a table fault, never papered over."""


# ── the story slots (build item 18a; docs/p1-threat-first.md, "The layers") ─────────────────────────────────
# A story slot accepts only a story or a stage piece. Texture may hang on the story (a scar the move left, a people
# the move displaced, a phenomenon born of the ruin, a trope break explained by the lifeline): the arrow points one
# way only. The arbiter excludes a texture candidate from a slot at the roll and refuses a set that holds one.
STORY_SLOTS = {
    "move_target": "the move's target",
    "contest_prize": "the contest's prize",
    "goal_piece": "the villain's goal piece",
    "lair_where": "the lair's where",
    "world_state_tie": "a world-state trope break's tie",
    "escalation_step": "the escalation's steps",
    "clue_place": "the clues' places",
    "secret_pin": "the secret's pin (a piece of the chain, when no god is pinned)",
}
SLOT_LAYERS = frozenset({"story", "stage"})
# the pieces the rows name by kind (a target's `piece`, a contest's `prize`, a seat on the layout); a row id is
# judged by its own table's layer
PIECE_LAYERS = {
    "heart": "stage", "key_place": "stage", "thin_place": "stage", "disputed_land": "stage", "end": "stage",
    "remnant": "story", "role": "story", "seat": "story", "new": "story",
    "contest": "story", "ruin_source": "story", "break": "story",
    "threat": "story", "hand": "story", "villain": "story",
    "lifeline": "texture", "scar": "texture", "palette": "texture",
    "people": "texture", "institution": "texture", "phenomenon": "texture",
}


def piece_layer(piece) -> str | None:
    """A piece's layer: a kind of the list above, else the layer of the table its row id belongs to."""
    if piece in PIECE_LAYERS:
        return PIECE_LAYERS[piece]
    ref = dt.ref_of_row(str(piece)) if piece else None
    return dt.layer(ref, str(piece)) if ref else None


def slot_accepts(slot: str, piece) -> bool:
    if slot not in STORY_SLOTS:
        raise KeyError(f"design_arbiter: no story slot {slot!r}")
    return piece_layer(piece) in SLOT_LAYERS


def slot_pieces(row: dict) -> list:
    """What a row would put in a slot: a target's `piece`, a contest's `prize` (and the pieces its `prize_with` may
    turn it into), else the row itself."""
    if "piece" in row:
        return [row["piece"]]
    if "prize" in row:
        return [row["prize"], *(row.get("prize_with") or {}).values()]
    return [row["id"]]


def slot_errors(filled) -> list[str]:
    """`filled`: (slot, piece) pairs of a set; one line per texture (or unknown) piece in a story slot."""
    return [f"{STORY_SLOTS[slot]} holds {piece!r}, a {piece_layer(piece) or 'layerless'} piece: a story slot takes "
            f"a story or a stage piece only" for slot, piece in filled if not slot_accepts(slot, piece)]


@dataclass
class Context:
    """What a draw is judged against: the dials, every row rolled so far (row id → rolled secretly) and the tokens
    they set (token → set secretly): the claims of the dial rows and of the rolled rows, a seated contest role's
    claims and the layout's tokens (added by the roller)."""
    dials: dict = field(default_factory=dict)
    rolled: dict = field(default_factory=dict)
    tokens: dict = field(default_factory=dict)

    def __post_init__(self) -> None:
        for dial, value in self.dials.items():
            if isinstance(value, str):
                row = dt.dial_row(dial, value) if dial in dt.DIAL_NAMES else None
                for t in dt.claim_tokens((row or {}).get("claims")):
                    self.add_token(t, False)
        index = dt.row_tokens()
        for row_id, secret in list(self.rolled.items()):
            for t in index.get(row_id, ()):
                self.add_token(t, secret)

    def add(self, row_id, secret: bool) -> None:
        if row_id:
            self.rolled[row_id] = self.rolled.get(row_id, False) or bool(secret)
            for t in dt.row_tokens().get(row_id, ()):
                self.add_token(t, secret)

    def add_token(self, tok: str, secret: bool) -> None:
        """A token set publicly stays public even when a secret row sets it too."""
        self.tokens[tok] = self.tokens[tok] and bool(secret) if tok in self.tokens else bool(secret)

    def has(self, key) -> bool:
        return key in self.rolled or key in self.tokens

    def secret_of(self, key) -> bool:
        """Was this row rolled, or this token set, secretly?"""
        return bool(self.rolled.get(key, False) or self.tokens.get(key, False))

    def clashes(self, claims) -> list[str]:
        """The context's tokens that clash with these claims (a contest role's, judged when the scale seats it)."""
        return sorted(t for t in dt.clashing_tokens(claims) if t in self.tokens)


def _condition_ids(cond) -> set:
    if cond is None:
        return set()
    if isinstance(cond, list):
        out: set = set()
        for c in cond:
            out |= _condition_ids(c)
        return out
    out = {x for key in ("any_of", "all_of", "none_of") for x in (cond.get(key) or [])}
    for key in ("all", "any"):
        out |= _condition_ids(list(cond.get(key) or []))
    return out


def holds(cond, ctx: Context) -> bool:
    """A `requires` / `when` condition against the dials and the rolled rows."""
    if cond is None:
        return True
    if isinstance(cond, list):
        return any(holds(c, ctx) for c in cond)
    if not isinstance(cond, dict):
        raise ValueError(f"design_arbiter: a condition is a mapping or a list of mappings, not {cond!r}")
    unknown = set(cond) - set(CONDITION_KEYS)
    if unknown:
        raise ValueError(f"design_arbiter: unknown condition key(s) {sorted(unknown)}")
    for dial, allowed in (cond.get("dial") or {}).items():
        value = ctx.dials.get(dial)
        values = value if isinstance(value, (list, tuple)) else [value]
        if not set(values) & set(allowed or []):
            return False
    if cond.get("any_of") and not any(ctx.has(x) for x in cond["any_of"]):
        return False
    if any(not ctx.has(x) for x in cond.get("all_of") or []):
        return False
    if any(ctx.has(x) for x in cond.get("none_of") or []):
        return False
    if any(not holds(c, ctx) for c in cond.get("all") or []):
        return False
    if cond.get("any") and not any(holds(c, ctx) for c in cond["any"]):
        return False
    return True


def weight_of(row: dict, ctx: Context) -> float:
    w = float(row.get("weight", 1))
    for rule in row.get("weight_by") or []:
        if holds(rule.get("when"), ctx):
            w *= float(rule.get("x", 1))
    return w


def constraint_reason(row: dict, ctx: Context, exclude: set, where, why: str, conflicts: dict, slot: str | None = None) -> dict | None:
    """Why the constraints bar `row`, or None."""
    rid = row["id"]
    if rid in exclude:
        return {"row": rid, "why": "caller"}
    if slot is not None and not all(slot_accepts(slot, p) for p in slot_pieces(row)):
        return {"row": rid, "why": "texture_in_slot", "slot": slot}
    if where is not None and not where(row):
        return {"row": rid, "why": why}
    if row.get("forbidden") and not any(ctx.has(x) for x in row.get("allowed_via") or []):
        return {"row": rid, "why": "forbidden"}
    if not holds(row.get("requires"), ctx):
        return {"row": rid, "why": "requires"}
    hits = sorted((x for x in conflicts.get(rid, ()) if ctx.has(x)), key=lambda x: (ctx.secret_of(x), x))
    if hits:
        return {"row": rid, "why": "conflict", "with": hits[0]}   # a public reason first, when there is one
    if weight_of(row, ctx) <= 0:
        return {"row": rid, "why": "weight_zero"}
    return None


def usage_reason(row: dict, usage: dict, skip: tuple = ()) -> dict | None:
    rid = row["id"]
    for kind in USAGE_ORDER:
        if kind in skip:
            continue
        if kind == "family_wait":
            fam = row.get("family")
            if fam is not None and fam in (usage.get(kind) or ()):
                return {"row": rid, "why": kind, "family": fam}
        elif rid in (usage.get(kind) or ()):
            return {"row": rid, "why": kind}
    return None


def _names_secret(entry: dict, row: dict, ctx: Context, secret_ids: set) -> bool:
    """Does the reason point at the secret layer (a conflict with, a requirement on, an admission by a secret row)?"""
    named = {"conflict": {entry.get("with")}, "requires": _condition_ids(row.get("requires")),
             "forbidden": set(row.get("allowed_via") or [])}.get(entry["why"], set())
    return any(x in secret_ids or ctx.secret_of(x) for x in named if x)


def arbitrate(ref: str, rows: list[dict], ctx: Context, *, exclude=None, where=None, why: str = "where",
              usage: dict | None = None, secret: bool = False, conflicts: dict | None = None,
              secret_ids=None, weigh=None, slot: str | None = None) -> dict:
    """The pool a draw is thrown on: {'pool', 'weights', 'excluded', 'excluded_secret', 'usage_fallback',
    'visible'}. `visible` are the rows a public record may count (not publicly excluded), in table order.
    `conflicts` and `secret_ids` default to the committed tables' (tests pass their own). `weigh(row, ctx)` replaces
    the rows' own weights for this draw (the people's lineage under a role's weights or inverted homes). `slot` names
    the story slot the draw fills: a row that would put a texture piece in it is barred (build item 18a)."""
    exclude = set(exclude or ())
    usage = usage or {}
    if conflicts is None or secret_ids is None:
        idx_conflicts, idx_secret = dt.indexes()
        conflicts = idx_conflicts if conflicts is None else conflicts
        secret_ids = idx_secret if secret_ids is None else secret_ids
    barred: list[dict] = []
    allowed: list[dict] = []
    for r in rows:
        reason = constraint_reason(r, ctx, exclude, where, why, conflicts, slot)
        (barred if reason else allowed).append(reason or r)
    if not allowed:
        counts: dict = {}
        for e in barred:
            counts[e["why"]] = counts.get(e["why"], 0) + 1
        detail = ", ".join(f"{k} {v}" for k, v in sorted(counts.items()))
        raise EmptyPool(f"{ref}: no row survives the constraints ({len(rows)} rows: {detail}) — a table fault")
    fallback = None
    for n in range(len(FALLBACK_ORDER) + 1):          # nothing dropped, then one more kind at each step
        skip = FALLBACK_ORDER[:n]
        spent = [usage_reason(r, usage, skip) for r in allowed]
        pool = [r for r, e in zip(allowed, spent) if e is None]
        if pool:
            dropped = [k for k in skip if usage.get(k)]
            if dropped:
                fallback = "dropped: " + ", ".join(dropped)
            barred += [e for e in spent if e is not None]
            break
    secret_ids = set(secret_ids)
    public, hidden = [], []
    by_id = {r["id"]: r for r in rows}
    for e in barred:
        if not secret and _names_secret(e, by_id[e["row"]], ctx, secret_ids):
            hidden.append(e)
        else:
            public.append(e)
    shown = {e["row"] for e in public}
    return {"pool": pool, "weights": [(weigh or weight_of)(r, ctx) for r in pool], "excluded": public,
            "excluded_secret": hidden, "usage_fallback": fallback, "allowed": len(allowed),
            "visible": [r for r in rows if r["id"] not in shown]}


def pick(rng: random.Random, pool: list[dict], weights: list[float]) -> dict:
    """One weighted draw; the record fields a roll carries."""
    total = sum(weights)
    raw = rng.uniform(0, total)
    acc, chosen = 0.0, pool[-1]
    for r, w in zip(pool, weights):
        acc += w
        if raw <= acc:
            chosen = r
            break
    return {"notation": f"d{len(pool)}", "raw": pool.index(chosen) + 1, "row_id": chosen["id"],
            "row_label": chosen.get("label")}


def public_view(res: dict, picked: dict) -> tuple[dict, dict | None]:
    """(the fields a public record shows, the real die for the secret side or None). When a secret row took rows
    out of a public pool, the public record counts the die over `visible` (the pool plus the secretly excluded
    rows, in table order), so its size and face give nothing away; the drawn row is the same."""
    if not res["excluded_secret"]:
        return picked, None
    visible = [r["id"] for r in res["visible"]]
    shown = dict(picked, notation=f"d{len(visible)}", raw=visible.index(picked["row_id"]) + 1)
    return shown, {"notation": picked["notation"], "raw": picked["raw"]}


def check_forced(row_id: str, ctx: Context, conflicts: dict | None = None) -> None:
    """A forced row is held to the conflicts too: a conflicting row is never kept."""
    conflicts = dt.conflict_index() if conflicts is None else conflicts
    hits = sorted(x for x in conflicts.get(row_id, ()) if ctx.has(x))
    if hits:
        raise EmptyPool(f"the forced row {row_id} conflicts with a row already rolled — a table fault")


def conflicting_pairs(row_ids, conflicts: dict | None = None, tokens=(), exempt=()) -> list[tuple[str, str]]:
    """Every conflicting pair inside a set of rolled rows (the door's recheck and the many-seeds test). The rows'
    claims are expanded to tokens, and `tokens` adds the ones no row carries (the dials', a seated role's, the
    layout's): a row beside a token its claims clash with is a pair too. `exempt` holds the pairs a forced roll was
    allowed to stand in (the Roller's `exempt`: the scar's prohibition tied to a break still coming)."""
    exempt = {frozenset(p) for p in exempt}
    rows_in = set(x for x in row_ids if x)
    index = dt.row_tokens()
    expanded = set(tokens)
    for r in rows_in:
        expanded |= set(index.get(r, ()))
    ids = sorted(rows_in | expanded)
    idx = dt.conflict_index() if conflicts is None else conflicts
    clash = dt.clash_map()
    return [(a, b) for i, a in enumerate(ids) for b in ids[i + 1:]
            if (b in idx.get(a, ()) or b in clash.get(a, ())) and frozenset((a, b)) not in exempt]
