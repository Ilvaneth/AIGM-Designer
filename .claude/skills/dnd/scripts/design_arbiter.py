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
   target + action pair that never repeats, `pair`). Usage never stops a draw: when it empties the pool, the
   family waits are dropped first, then every usage exclusion, and the record says so (`usage_fallback`).

Every exclusion is logged with its reason. An exclusion on a public record that names a secret row (a row
rolled secretly, or any row of a table whose roll header says `secret: true`) is moved to the secret side, so
the public dice log never tells the owner, who is also the player, what the secret layer holds.

Conditions (`requires`, `weight_by[].when`) are a mapping whose keys must all hold, or a list of such mappings
of which one must hold:

    requires: {dial: {magic: [medium, high], era: [underground]}}   the dial's value is in the list
    requires: {any_of: [land_thin_place]}                            one of these rows was rolled
    requires: {all_of: [...]} / {none_of: [...]}                     all / none of these rows were rolled
    weight_by: [{when: {dial: {era: [nautical]}}, x: 3}]             weight × 3 while the condition holds
"""

from __future__ import annotations

import os
import random
import sys
from dataclasses import dataclass, field

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import design_tables as dt  # noqa: E402

CONDITION_KEYS = ("dial", "any_of", "all_of", "none_of")
USAGE_ORDER = ("used_elsewhere", "row_wait", "pair", "family_wait")   # family_wait is relaxed first


class EmptyPool(Exception):
    """The constraints left no row: a table fault, never papered over."""


@dataclass
class Context:
    """What a draw is judged against: the dials and every row rolled so far (row id → rolled secretly)."""
    dials: dict = field(default_factory=dict)
    rolled: dict = field(default_factory=dict)

    def add(self, row_id, secret: bool) -> None:
        if row_id:
            self.rolled[row_id] = self.rolled.get(row_id, False) or bool(secret)

    def has(self, row_id) -> bool:
        return row_id in self.rolled


def _condition_ids(cond) -> set:
    if cond is None:
        return set()
    if isinstance(cond, list):
        out: set = set()
        for c in cond:
            out |= _condition_ids(c)
        return out
    return {x for key in ("any_of", "all_of", "none_of") for x in (cond.get(key) or [])}


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
    return True


def weight_of(row: dict, ctx: Context) -> float:
    w = float(row.get("weight", 1))
    for rule in row.get("weight_by") or []:
        if holds(rule.get("when"), ctx):
            w *= float(rule.get("x", 1))
    return w


def constraint_reason(row: dict, ctx: Context, exclude: set, where, why: str, conflicts: dict) -> dict | None:
    """Why the constraints bar `row`, or None."""
    rid = row["id"]
    if rid in exclude:
        return {"row": rid, "why": "caller"}
    if where is not None and not where(row):
        return {"row": rid, "why": why}
    if row.get("forbidden") and not any(ctx.has(x) for x in row.get("allowed_via") or []):
        return {"row": rid, "why": "forbidden"}
    if not holds(row.get("requires"), ctx):
        return {"row": rid, "why": "requires"}
    hits = sorted((x for x in conflicts.get(rid, ()) if ctx.has(x)), key=lambda x: (ctx.rolled.get(x, False), x))
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
    return any(x in secret_ids or ctx.rolled.get(x) for x in named if x)


def arbitrate(ref: str, rows: list[dict], ctx: Context, *, exclude=None, where=None, why: str = "where",
              usage: dict | None = None, secret: bool = False, conflicts: dict | None = None,
              secret_ids=None) -> dict:
    """The pool a draw is thrown on: {'pool', 'weights', 'excluded', 'excluded_secret', 'usage_fallback'}.
    `conflicts` and `secret_ids` default to the committed tables' (tests pass their own)."""
    exclude = set(exclude or ())
    usage = usage or {}
    if conflicts is None or secret_ids is None:
        idx_conflicts, idx_secret = dt.indexes()
        conflicts = idx_conflicts if conflicts is None else conflicts
        secret_ids = idx_secret if secret_ids is None else secret_ids
    barred: list[dict] = []
    allowed: list[dict] = []
    for r in rows:
        reason = constraint_reason(r, ctx, exclude, where, why, conflicts)
        (barred if reason else allowed).append(reason or r)
    if not allowed:
        counts: dict = {}
        for e in barred:
            counts[e["why"]] = counts.get(e["why"], 0) + 1
        detail = ", ".join(f"{k} {v}" for k, v in sorted(counts.items()))
        raise EmptyPool(f"{ref}: no row survives the constraints ({len(rows)} rows: {detail}) — a table fault")
    fallback = None
    for skip in ((), ("family_wait",), USAGE_ORDER):
        spent = [usage_reason(r, usage, skip) for r in allowed]
        pool = [r for r, e in zip(allowed, spent) if e is None]
        if pool:
            if skip:
                fallback = "family waits dropped" if skip == ("family_wait",) else "every usage exclusion dropped"
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
    return {"pool": pool, "weights": [weight_of(r, ctx) for r in pool], "excluded": public,
            "excluded_secret": hidden, "usage_fallback": fallback}


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


def check_forced(row_id: str, ctx: Context, conflicts: dict | None = None) -> None:
    """A forced row is held to the conflicts too: a conflicting row is never kept."""
    conflicts = dt.conflict_index() if conflicts is None else conflicts
    hits = sorted(x for x in conflicts.get(row_id, ()) if ctx.has(x))
    if hits:
        raise EmptyPool(f"the forced row {row_id} conflicts with a row already rolled — a table fault")


def conflicting_pairs(row_ids, conflicts: dict | None = None) -> list[tuple[str, str]]:
    """Every conflicting pair inside a set of rolled rows (the door's recheck and the many-seeds test)."""
    ids = sorted(set(x for x in row_ids if x))
    idx = dt.conflict_index() if conflicts is None else conflicts
    return [(a, b) for i, a in enumerate(ids) for b in ids[i + 1:] if b in idx.get(a, ())]
