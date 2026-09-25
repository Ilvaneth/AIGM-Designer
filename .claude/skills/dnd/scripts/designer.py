#!/usr/bin/env python3
"""
designer.py — the conductor's CLI: the deterministic half of every designer command
(plan item 19, 21.E; 24.6 #6; the slice-1c auto-approve decision of 2026-09-25).

The main session is a blind conductor: it asks the Phase 0 dials, runs these verbs, launches
one Workflow per phase, shows the script-built phase card and records approvals. It never
writes bible prose and never reads design/dm-only/ or design/_staging/; `arm` raises the read
guard so that stays true while a run is live.

CLI:
  designer.py new NAME --scale S --tone T --magic M --era E --danger D --party-size N
              [--start-level 1] --content-mix a,b,c [--must ..] [--must-not ..] [--lang tr]
              [--seed S] [--concurrency 8] [--economy] [--fixture] [--ask-approval] [--session-id ID]
        a dial given as `?` is rolled live (dials.yaml weights, logged); then design_manifest init,
        the arc skeleton, the P0 card, and the guard is armed for `birth`
  designer.py -c CAMP arm --mode birth|detail|playtest [--session-id ID] | disarm
  designer.py -c CAMP preroll --phase PN [--attempt N]      every labelled roll of the phase
  designer.py -c CAMP phase PN begin [--json]               reconcile, arm, roster with read budgets and prompts
  designer.py -c CAMP phase PN merge [--day N]              registry merge + design_seed + statuses
  designer.py -c CAMP phase PN check                        design_check --phase (redacted)
  designer.py -c CAMP phase PN card                         the phase card (design_approval.py)
  designer.py -c CAMP phase PN approve [--card F] [--onay] [--round TEXT --scope S]
                                                             record approval (+ path-scoped commit) or a correction round
  designer.py -c CAMP phase PN rerun --reason TEXT [--reseed]
  designer.py -c CAMP status [--json]
  designer.py -c CAMP abandon --reason TEXT                 retire names and used rows, disarm
  designer.py -c CAMP commit --message TEXT                 design(<campaign>): commit, path-scoped

Auto-approve (owner decision 2026-09-25): a campaign initialised with --fixture or named
`_test-*` carries `_meta.auto_approve: true`; `approve` then needs no `onay` and no `devam`.
`--ask-approval` turns that off for one test birth that should exercise the approval loop
(the campaign stays git-ignored, so nothing is committed).
A real birth requires `--onay` on `approve` (the conductor passes it only after the player
typed the word) and the conductor waits for `devam` before the next `phase begin`.

Exit codes: 0 ok · 1 refused · 2 usage
"""

from __future__ import annotations

import argparse
import json
import os
import random
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dice as dice_mod  # noqa: E402
import design_dice as dd  # noqa: E402
import design_manifest as dm  # noqa: E402
import design_prompts as dp  # noqa: E402
import design_tables as dt  # noqa: E402
from design_io import (campaign_dir, design_dir, dm_only_dir, now_iso, read_json, sha256_file,  # noqa: E402
                       stamp_meta, write_json_atomic)
from paths import runtime_dir  # noqa: E402

SCRIPTS = Path(__file__).resolve().parent
MARKER = "active-design.json"
AGENT_TYPES = ["workflow-subagent", "design-writer", "design-critic", "design-skeleton", "design-merge"]
PLAYTEST_ALLOWLIST = ["design/player-primer.md", "characters/", "design/threads/", "state.md"]
CARD_DIR = "_approval"


# ── helpers ───────────────────────────────────────────────────────────────────

def run_script(name: str, campaign: str, *args: str, check: bool = False) -> subprocess.CompletedProcess:
    proc = subprocess.run([sys.executable, "-X", "utf8", str(SCRIPTS / name), "-c", campaign, *args],
                          capture_output=True, text=True, encoding="utf-8")
    if check and proc.returncode not in (0,):
        raise SystemExit(f"designer: {name} {' '.join(args)} failed ({proc.returncode}):\n{proc.stderr.strip()}")
    return proc


def auto_approve(manifest: dict) -> bool:
    return bool(manifest.get("_meta", {}).get("auto_approve"))


def band(value) -> tuple[int, int]:
    return dt.band(value)


def marker_path() -> Path:
    return runtime_dir() / MARKER


def arm(campaign: str, mode: str, session_id: str | None) -> dict:
    data = {"campaign": campaign, "mode": mode, "session_id": session_id or None,
            "agent_types_allowed": AGENT_TYPES, "playtest_allowlist": PLAYTEST_ALLOWLIST, "armed_at": now_iso()}
    write_json_atomic(marker_path(), data)
    return data


def disarm() -> bool:
    p = marker_path()
    if p.is_file():
        p.unlink()
        return True
    return False


def git_ignored(path: Path, git_root: str | None) -> bool:
    if not git_root:
        return True
    proc = subprocess.run(["git", "check-ignore", "-q", str(path)], cwd=git_root, capture_output=True)
    return proc.returncode == 0


def design_commit(campaign: str, message: str) -> str | None:
    """A path-scoped commit in the enclosing repository (item 19.10); None when nothing to commit."""
    manifest = dm.load(campaign)
    root = manifest["_meta"].get("git_root")
    cdir = campaign_dir(campaign)
    if not root or git_ignored(cdir, root):
        return None
    rel = os.path.relpath(cdir, root).replace("\\", "/")
    subprocess.run(["git", "add", "-A", "--", rel], cwd=root, capture_output=True)
    staged = subprocess.run(["git", "diff", "--cached", "--quiet", "--", rel], cwd=root)
    if staged.returncode == 0:
        return None
    subprocess.run(["git", "commit", "-q", "-m", f"design({campaign}): {message}", "--", rel], cwd=root,
                   capture_output=True, check=True)
    sha = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=root, capture_output=True, text=True).stdout.strip()
    return sha or None


# ── rolling: the same derivation as design_dice, batched ─────────────────────────

class Roller:
    """Batched, labelled, seeded draws; public records go to design.json, secret ones to dm-only."""

    def __init__(self, campaign: str, phase: str, attempt: int = 1):
        self.campaign, self.phase, self.attempt = campaign, phase, attempt
        self.manifest = dm.load(campaign)
        self.master = self.manifest["seed"]["master"]
        self.public: list[dict] = []
        self.secret: list[dict] = []
        self.by_label: dict[str, dict] = {}

    def _record(self, label: str, table: str | None) -> dict:
        return {"phase": self.phase, "table": table or "dice", "label": label, "notation": None, "raw": None,
                "row_id": None, "excluded": [], "attempt": self.attempt, "ts": now_iso()}

    def table(self, label: str, ref: str, secret: bool = False, avoid: bool = True,
              exclude: set | None = None, tries: int = 1) -> dict:
        rows = dt.rows(ref)
        if not rows:
            raise SystemExit(f"designer: no rows in {ref}")
        rng = dd.derive(self.master, self.phase, ref, label, self.attempt if tries == 1 else self.attempt + tries - 1)
        gone = dd.rows_used_elsewhere(self.campaign, ref) if avoid else set()
        rec = self._record(label, ref)
        rec.update(dd.draw(rng, rows, gone, exclude))
        rec["excluded"] = rec.pop("excluded_rows")
        if tries > 1:
            rec["attempt"] = self.attempt + tries - 1
        self._keep(rec, secret)
        return rec

    def table_until(self, label: str, ref: str, ok, secret: bool = False, avoid: bool = True,
                    exclude: set | None = None, max_tries: int = 8) -> dict:
        """Redraw with the attempt suffix until `ok(row)` holds; the last try is kept regardless."""
        rows = {r["id"]: r for r in dt.rows(ref)}
        rec = None
        for t in range(1, max_tries + 1):
            if rec is not None:
                self._drop(rec)
            rec = self.table(label, ref, secret=secret, avoid=avoid, exclude=exclude, tries=t)
            if ok(rows.get(rec["row_id"], {})):
                break
        return rec

    def notation(self, label: str, notation: str, secret: bool = False) -> dict:
        rng = dd.derive(self.master, self.phase, "dice", label, self.attempt)
        rec = self._record(label, None)
        rec.update({"notation": notation, "raw": dice_mod.run(notation, silent=True, rng=rng)})
        self._keep(rec, secret)
        return rec

    def forced(self, label: str, ref: str, row_id: str, reason: str, secret: bool = False) -> dict:
        rec = self._record(label, ref)
        rec.update({"notation": "forced", "raw": None, "row_id": row_id, "forced_by": reason})
        self._keep(rec, secret)
        return rec

    def _keep(self, rec: dict, secret: bool) -> None:
        (self.secret if secret else self.public).append(rec)
        self.by_label[rec["label"]] = rec

    def _drop(self, rec: dict) -> None:
        for lst in (self.public, self.secret):
            if rec in lst:
                lst.remove(rec)
        self.by_label.pop(rec["label"], None)

    def row(self, label: str):
        rec = self.by_label.get(label)
        return rec["row_id"] if rec else None

    def count(self, label: str, value) -> int:
        """A band → an exact count rolled once (d(hi-lo+1)); an exact number → itself."""
        lo, hi = band(value)
        if lo == hi:
            return lo
        rec = self.notation(label, f"d{hi - lo + 1}")
        return lo + int(rec["raw"]) - 1

    def flush(self) -> tuple[int, int]:
        data = dm.load(self.campaign)
        data["dice_log"].extend(self.public)
        if self.secret:
            path = dm_only_dir(self.campaign) / "dice-log.json"
            log = read_json(path) or {"_meta": {"schema_version": 1, "campaign": self.campaign}, "rolls": []}
            log["rolls"].extend(self.secret)
            stamp_meta(log, self.campaign, "designer.py preroll (secret)")
            write_json_atomic(path, log)
            dls = data["dice_log_secret"]
            dls["count"] = len(log["rolls"])
            for rec in self.secret:
                if rec["label"] not in dls["labels"]:
                    dls["labels"].append(rec["label"])
        dm.save(self.campaign, data, f"designer.py preroll --phase {self.phase}")
        return len(self.public), len(self.secret)


def dials_of(manifest: dict) -> dict:
    return manifest["dials"]


def scale_of(manifest: dict) -> dict:
    return dt.scale_row(dials_of(manifest)["scale"])


def rolled_rows(manifest: dict, table_prefix: str) -> list[str]:
    """Row ids already rolled from a table (public log), for cross-phase constraints."""
    return [r["row_id"] for r in manifest["dice_log"] if r.get("table", "").startswith(table_prefix) and r.get("row_id")]


def not_forbidden(row: dict) -> bool:
    return not row.get("forbidden")


# ── preroll plans per phase ───────────────────────────────────────────────────

def preroll_p1(R: Roller, m: dict) -> None:
    sc = scale_of(m)
    R.table("tension.1", "tensions.yaml")
    if R.notation("tension.second", "d2")["raw"] == 2:
        R.table("tension.2", "tensions.yaml", exclude={R.row("tension.1")})
    breaks: list[str] = []
    conflicts: set = set()
    for n in range(1, int(sc["trope_breaks"]) + 1):
        rec = R.table_until(f"break.{n}", "trope-breaks.yaml",
                            lambda row: row.get("id") not in conflicts and row.get("id") not in breaks,
                            exclude=set(breaks))
        breaks.append(rec["row_id"])
        row = dt.row("trope-breaks.yaml", rec["row_id"]) or {}
        conflicts |= set(row.get("conflicts_with") or [])
    for sub in ("phenomenon", "people", "institution"):
        R.table(f"sig_{sub}", f"signatures.yaml#{sub}")
    fams: list[str] = []
    for n in range(1, int(dt.load("naming.yaml")["roll"]["count_by_scale"][dials_of(m)["scale"]]) + 1):
        rec = R.table(f"naming_family.{n}", "naming.yaml#family", exclude=set(fams))
        fams.append(rec["row_id"])
    arche = R.table_until("secret_archetype", "secrets.yaml#archetype",
                          lambda row: not (set(row.get("conflicts_with") or []) & set(breaks)) and row.get("id") not in conflicts,
                          secret=True)
    R.table("secret_twist", "secrets.yaml#twist", secret=True)
    R.table("secret_trail", "secrets.yaml#trail", secret=True)
    chance = int(sc["signature_mechanic_chance"])
    if chance <= 0:
        R.forced("mechanic", "dice", "no", "scale never rolls the signature mechanic")
    elif chance >= 100:
        R.forced("mechanic", "dice", "yes", "scale always rolls the signature mechanic")
    else:
        hit = R.notation("mechanic_gate", "d100")["raw"] <= chance
        R.forced("mechanic", "dice", "yes" if hit else "no", f"d100 against {chance}")


def preroll_p2(R: Roller, m: dict) -> None:
    sc = scale_of(m)
    breaks = rolled_rows(m, "trope-breaks.yaml")
    override = None
    for b in breaks:
        row = dt.row("trope-breaks.yaml", b) or {}
        if (row.get("overrides") or {}).get("pantheon_type"):
            override = (b, row["overrides"]["pantheon_type"])
    if override:
        R.forced("pantheon_type", "pantheon.yaml#type", override[1], f"override by {override[0]}")
    else:
        R.table("pantheon_type", "pantheon.yaml#type", avoid=False)
    R.table("pantheon_presence", "pantheon.yaml#presence", avoid=False)
    for sub in ("source", "constraint", "visibility", "regulator"):
        R.table(f"magic_{sub}", f"magic.yaml#{sub}")
    R.table("magic_taboo.1", "magic.yaml#taboo")
    if R.notation("taboo.second", "d2")["raw"] == 2 and R.row("magic_taboo.1") != "taboo_none":
        R.table("magic_taboo.2", "magic.yaml#taboo", exclude={R.row("magic_taboo.1"), "taboo_none"})
    gate = (dt.dial_row("magic", dials_of(m)["magic"]) or {}).get("effects", {}).get("wild_magic_roll", {})
    raw = R.notation("wild_gate", gate.get("notation", "d6"))["raw"]
    if raw in (gate.get("on") or []):
        R.table("wild_shape", "magic.yaml#wild", avoid=False, exclude={"wild_no"})
    else:
        R.forced("wild_shape", "magic.yaml#wild", "wild_no", f"gate {gate.get('notation', 'd6')}={raw} not in {gate.get('on')}")
    for sub in ("climate", "year_shape", "week", "moon", "start_anchor"):
        R.table(sub, f"calendar.yaml#{sub}", avoid=(sub == "climate"))
    hist = sc["history"]
    ages: list[str] = []
    for n in range(1, R.count("ages_count", hist["ages"]) + 1):
        ages.append(R.table(f"age.{n}", "history.yaml#age_template", exclude=set(ages))["row_id"])
    for n in range(1, R.count("events_count", hist["dated_events"]) + 1):
        R.table(f"event.{n}", "history.yaml#event_type", avoid=False)
        R.table(f"divergence.{n}", "history.yaml#divergence", avoid=False)
        R.table(f"memory.{n}", "history.yaml#memory", avoid=False)
    for n in range(1, R.count("deep_count", hist["deep_past_events"]) + 1):
        R.table(f"deep.{n}", "history.yaml#event_type", avoid=False)
    fests: list[str] = []
    for n in range(1, band(sc["gods"])[1] + 1):
        fests.append(R.table(f"festival.{n}", "calendar.yaml#festival_type", avoid=False, exclude=set(fests))["row_id"])


def preroll_p3(R: Roller, m: dict) -> None:
    sc = scale_of(m)
    climate = None
    for rec in m["dice_log"]:
        if rec.get("label") == "climate":
            climate = rec.get("row_id")
    regions = R.count("regions_count", sc["regions"])
    idents: list[str] = []
    for i in range(1, regions + 1):
        R.table_until(f"region.{i}.biome", "regions.yaml#biome",
                      lambda row: climate is None or climate in (row.get("climates") or []))
        idents.append(R.table(f"region.{i}.identity", "regions.yaml#identity", exclude=set(idents))["row_id"])
        for k in range(1, R.count(f"region.{i}.landmarks_count", [2, 4]) + 1):
            R.table(f"region.{i}.landmark.{k}", "regions.yaml#landmark_kind", avoid=False)
        seen: set = set()
        for k in range(1, 7):
            seen.add(R.table(f"region.{i}.social.{k}", "regions.yaml#social_seed", avoid=False, exclude=set(seen))["row_id"])
        seen = set()
        for k in range(1, 7):
            seen.add(R.table(f"region.{i}.presence.{k}", "regions.yaml#faction_presence", avoid=False, exclude=set(seen))["row_id"])
    j = 0
    kinds = {r["id"]: r for r in dt.rows("settlements.yaml#kind")}
    for kind in ("metropolis", "city", "town", "village"):
        n = R.count(f"{kind}_count", sc["settlements"][kind])
        for _ in range(n):
            j += 1
            R.forced(f"settlement.{j}.kind", "settlements.yaml#kind", f"kind_{kind}", "scale.yaml settlements")
            R.table(f"settlement.{j}.problem", "settlements.yaml#problem")
            if kind == "village":
                continue
            R.table(f"settlement.{j}.fear", "settlements.yaml#fear")
            goods: set = set()
            for k in range(1, R.count(f"settlement.{j}.goods_count", [1, 3]) + 1):
                goods.add(R.table(f"settlement.{j}.goods.{k}", "settlements.yaml#economy_good", avoid=False, exclude=set(goods))["row_id"])
            districts: set = set()
            for k in range(1, R.count(f"settlement.{j}.districts_count", kinds[f"kind_{kind}"]["districts"]) + 1):
                districts.add(R.table(f"settlement.{j}.district.{k}", "settlements.yaml#district_type", avoid=False, exclude=set(districts))["row_id"])


def preroll_p4(R: Roller, m: dict) -> None:
    sc = scale_of(m)
    fac = sc["factions"]
    total = R.count("factions_count", fac["count"])
    quota = fac["quota"]
    slots: list[str] = []
    for arche, cnt in quota.items():
        lo, hi = band(cnt)
        n = lo if lo == hi else R.count(f"quota.{arche}", cnt)
        slots += [f"archetype_{arche}"] * n
    pool = {f"archetype_{a}" for a in (fac.get("pool") or [])}
    for n in range(1, total + 1):
        if n <= len(slots):
            R.forced(f"faction.{n}.archetype", "factions.yaml#archetype", slots[n - 1], "scale.yaml quota")
        elif pool:
            R.table_until(f"faction.{n}.archetype", "factions.yaml#archetype", lambda row: row.get("id") in pool, avoid=False)
        else:
            R.table(f"faction.{n}.archetype", "factions.yaml#archetype", avoid=False)
        R.table_until(f"faction.{n}.fracture", "factions.yaml#fracture", not_forbidden, exclude={"fracture_none"})
        R.table(f"faction.{n}.endgame", "factions.yaml#endgame")
        R.table(f"faction.{n}.secret", "factions.yaml#secret_kind", secret=True)
        if R.row(f"faction.{n}.archetype") == "archetype_cult":
            R.table_until(f"faction.{n}.cult_doctrine", "factions.yaml#cult_doctrine", not_forbidden,
                          exclude={"cultdoc_evil_for_its_own_sake", "cultdoc_unspecified"})
        rungs: list[str] = []
        for k in range(1, R.count(f"faction.{n}.rungs_count", [3, 4]) + 1):
            excl = set(rungs) | ({"rung_war"} if k == 1 else set())
            rungs.append(R.table(f"faction.{n}.rung.{k}", "factions.yaml#provocation_rung", avoid=False, exclude=excl)["row_id"])
        links: list[str] = []
        for k in range(1, R.count(f"faction.{n}.links_count", [2, 4]) + 1):
            links.append(R.table(f"faction.{n}.link.{k}", "factions.yaml#access_link", avoid=False, exclude=set(links))["row_id"])
    # antagonists — every roll secret
    R.table("bbeg_visibility", "antagonists.yaml#visibility", secret=True)
    R.table_until("bbeg_shape", "antagonists.yaml#villain_shape", not_forbidden, secret=True,
                  exclude={"shape_dark_lord", "shape_whispering_advisor", "shape_secretly_evil_ruler"})
    R.table_until("bbeg_origin", "antagonists.yaml#origin", not_forbidden, secret=True, exclude={"origin_awakened_ancient"})
    allowed_religious = set(rolled_rows(m, "secrets.yaml") + rolled_rows(m, "trope-breaks.yaml"))
    secret_rows = [r["row_id"] for r in (read_json(dm_only_dir(R.campaign) / "dice-log.json") or {}).get("rolls", []) if r.get("row_id")]
    allowed_religious |= set(secret_rows)
    bfa_rows = {r["id"]: r for r in dt.rows("antagonists.yaml#bbeg_faction_archetype")}

    def bfa_ok(row: dict) -> bool:
        if not row.get("forbidden"):
            return True
        return bool(set(row.get("allowed_via") or []) & allowed_religious)
    R.table_until("bbeg_faction_archetype", "antagonists.yaml#bbeg_faction_archetype", bfa_ok, secret=True, avoid=False)
    R.table("front_template", "antagonists.yaml#front_template", secret=True)
    R.table("doom_shape", "antagonists.yaml#doom_shape", secret=True)
    roles: list[str] = []
    for n in range(1, R.count("lieutenants_count", sc["antagonists"]["lieutenants"]) + 1):
        roles.append(R.table(f"lieutenant.{n}.role", "antagonists.yaml#lieutenant_role", secret=True, avoid=False, exclude=set(roles))["row_id"])
    R.count("regional_count", sc["antagonists"]["regional"])


def preroll_p5(R: Roller, m: dict) -> None:
    sc = scale_of(m)
    n_npcs = R.count("npcs_count", sc["named_npcs"])
    tic_uses: dict[str, int] = {}
    for n in range(1, n_npcs + 1):
        for axis in ("trust", "ambition", "loyalty", "courage"):
            R.notation(f"npc.{n}.axis.{axis}", "d5")
        R.table(f"npc.{n}.secret", "npcs.yaml#secret", avoid=False)
        spent = {t for t, c in tic_uses.items() if c >= 2}
        rec = R.table(f"npc.{n}.tic", "npcs.yaml#speech_tic", avoid=False, exclude=spent)
        tic_uses[rec["row_id"]] = tic_uses.get(rec["row_id"], 0) + 1
        R.notation(f"npc.{n}.species", "d100")
        R.notation(f"npc.{n}.gender", "d100")


def preroll_p6(R: Roller, m: dict) -> None:
    sc = scale_of(m)
    bands = dt.scale_shared()["room_bands"]
    tele = {d: [r["id"] for r in dt.rows("sites.yaml#telegraph") if r["distance"] == d] for d in ("far", "near", "threshold")}
    n = 0
    for role, cnt in sc["sites"]["roles"].items():
        for _ in range(int(cnt)):
            n += 1
            R.forced(f"site.{n}.role", "sites.yaml#role_band", f"role_{role}", "scale.yaml sites.roles")
            R.table(f"site.{n}.type", "sites.yaml#site_type", avoid=False)
            for d in ("far", "near", "threshold"):
                R.table_until(f"site.{n}.telegraph.{d}", "sites.yaml#telegraph", lambda row, d=d: row.get("distance") == d, avoid=False)
            R.table(f"site.{n}.escape", "sites.yaml#escape", avoid=False)
            R.table(f"site.{n}.attitude", "sites.yaml#attitude", avoid=False)
            R.table(f"site.{n}.payoff", "sites.yaml#payoff", avoid=False)
            R.table(f"site.{n}.never_visited", "sites.yaml#never_visited", avoid=False)
            R.count(f"site.{n}.rooms", bands[role])
            R.table(f"site.{n}.hoard", "loot-budget.yaml#hoard_flavour", avoid=False)


def preroll_p7(R: Roller, m: dict) -> None:
    sc = scale_of(m)
    scale = dials_of(m)["scale"]
    for b in dt.rows("arc.yaml#beat_template"):
        if scale in b["scales"]:
            R.table(f"beat.{b['id']}.change", "arc.yaml#change_kind", avoid=False)
    for ch in m.get("arc_skeleton") or []:
        nodes: list[str] = []
        for k in range(1, R.count(f"{ch['chapter']}.nodes_count", [3, 5]) + 1):
            nodes.append(R.table(f"{ch['chapter']}.node.{k}", "arc.yaml#node", avoid=False, exclude=set(nodes))["row_id"])
    for act in range(1, int(sc["acts"]) + 1):
        for k in range(1, R.count(f"act.{act}.hooks_count", dt.scale_shared()["planted_hooks_per_act"]) + 1):
            R.table(f"act.{act}.hook.{k}", "arc.yaml#planted_hook_kind", avoid=False)
    for k in range(1, R.count("seeds_count", sc["quest_seeds"]) + 1):
        R.table(f"seed.{k}", "arc.yaml#seed_shape", avoid=False)
    R.table_until("opening", "arc.yaml#opening_scene_type", not_forbidden, avoid=False, exclude={"open_tavern", "open_stranger_job"})
    R.table_until("plot_engine", "arc.yaml#plot_engine", not_forbidden, avoid=False, exclude={"engine_prophecy", "engine_collect_pieces"})
    sockets: list[str] = []
    for k in range(1, int(dials_of(m)["party_size"]) * int(sc["sockets_per_pc"]) + 1):
        sockets.append(R.table(f"socket.{k}", "threads.yaml#socket_type", avoid=False, exclude=set(sockets))["row_id"])


def preroll_p8(R: Roller, m: dict) -> None:
    R.count("rumours_count", [3, 5])


def preroll_p9(R: Roller, m: dict) -> None:
    party = int(dials_of(m)["party_size"])
    sc = scale_of(m)
    for n in range(1, party + 1):
        R.table_until(f"pc.{n}.truth", "threads.yaml#truth_kind", not_forbidden, secret=True, avoid=False,
                      exclude={"truth_chosen", "truth_destined", "truth_amnesia"})
        R.table(f"pc.{n}.antagonist", "threads.yaml#antagonist_binding", secret=True, avoid=False)
        R.table_until(f"pc.{n}.mission_verb", "threads.yaml#mission_verb", not_forbidden, avoid=False, exclude={"verb_find_out_who"})
    if party > 1:
        for act in range(1, int(sc["acts"]) + 1):
            R.table(f"crossing.{act}", "threads.yaml#crossing", avoid=False)


PREROLL = {"P1": preroll_p1, "P2": preroll_p2, "P3": preroll_p3, "P4": preroll_p4, "P5": preroll_p5,
           "P6": preroll_p6, "P7": preroll_p7, "P8": preroll_p8, "P9": preroll_p9}


def preroll(campaign: str, phase: str, attempt: int | None) -> int:
    m = dm.load(campaign)
    if phase not in dm.PHASES:
        print(f"designer: unknown phase {phase}", file=sys.stderr)
        return 2
    ph = m["phases"][phase]
    if attempt is None:
        attempt = max(1, int(ph.get("attempt") or 1))
    if any(r.get("phase") == phase and r.get("attempt") == attempt for r in m["dice_log"]):
        print(f"designer: {phase} attempt {attempt} already prerolled ({sum(1 for r in m['dice_log'] if r.get('phase') == phase)} public rolls); "
              "use --attempt N to redraw", file=sys.stderr)
        return 1
    R = Roller(campaign, phase, attempt)
    fn = PREROLL.get(phase)
    if fn:
        fn(R, m)
    n_pub, n_sec = R.flush()
    data = dm.load(campaign)
    if data["phases"][phase]["status"] in ("pending", "stale", "failed"):
        data["phases"][phase]["status"] = "prerolled"
        data["phases"][phase]["attempt"] = attempt
        dm.save(campaign, data, f"designer.py preroll --phase {phase}")
    print(f"designer: {phase} prerolled — {n_pub} public rolls, {n_sec} secret (labels only in design.json)")
    for rec in R.public:
        what = rec.get("row_id") or rec.get("raw")
        print(f"  {rec['label']:<32} {rec['table']:<32} {rec['notation'] or '':<7} → {what}")
    return 0


# ── new ───────────────────────────────────────────────────────────────────────

def roll_blank_dials(seed: str, given: dict) -> tuple[dict, list[dict]]:
    """Blank dials (`?`) are rolled with dials.yaml weights; the records are logged after init."""
    resolved, records = dict(given), []
    for dial in ("scale", "tone", "magic", "era", "danger"):
        if given.get(dial) in (None, "?", ""):
            ref = f"dials.yaml#{dial}"
            rng = dd.derive(seed, "P0", ref, f"dial.{dial}", 1)
            rec = {"phase": "P0", "table": ref, "label": f"dial.{dial}", "attempt": 1, "ts": now_iso(), "excluded": []}
            rec.update(dd.draw(rng, dt.rows(ref)))
            rec.pop("excluded_rows", None)
            resolved[dial] = (dt.row(ref, rec["row_id"]) or {})["value"]
            records.append(rec)
    mix = given.get("content_mix")
    if mix in (None, "?", ""):
        chosen: list[str] = []
        for n in (1, 2, 3):
            ref = "dials.yaml#content_mix"
            rng = dd.derive(seed, "P0", ref, f"content_mix.{n}", 1)
            rec = {"phase": "P0", "table": ref, "label": f"content_mix.{n}", "attempt": 1, "ts": now_iso(), "excluded": []}
            rec.update(dd.draw(rng, dt.rows(ref), exclude=set(chosen)))
            rec.pop("excluded_rows", None)
            chosen.append(rec["row_id"])
            records.append(rec)
        resolved["content_mix"] = ",".join((dt.row("dials.yaml#content_mix", c) or {})["value"] for c in chosen)
    return resolved, records


def p0_card(campaign: str, manifest: dict, records: list[dict]) -> Path:
    d = manifest["dials"]
    lines = [f"# Faz 0 — kadranlar ({campaign})", "",
             f"- **Ölçek:** {d['scale']} · **Ton:** {d['tone']} · **Büyü:** {d['magic']} · **Çağ:** {d['era']} · **Tehlike:** {d['danger']}",
             f"- **Parti:** {d['party_size']} kişi, seviye {d['start_level']} → bant {d['level_band'][0]}-{d['level_band'][1]}",
             f"- **İçerik karışımı:** {', '.join(d['content_mix'])}",
             f"- **Tohum:** `{manifest['seed']['master']}`",
             f"- **Dilekler:** olsun: {', '.join(d['wishes']['must']) or '—'}; olmasın: {', '.join(d['wishes']['must_not']) or '—'}", ""]
    if records:
        lines.append("## Zarlar (boş kadranlar)")
        for r in records:
            lines.append(f"- `{r['label']}` {r['notation']} → {r['raw']} = **{r['row_id']}**")
        lines.append("")
    lines.append("## Ark iskeleti")
    for ch in manifest["arc_skeleton"]:
        lines.append(f"- {ch['chapter']} — perde {ch['act']}, seviye {ch['level_band'][0]}-{ch['level_band'][1]}")
    path = design_dir(campaign) / CARD_DIR / "P0.card.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    return path


def new(a) -> int:
    name = a.name
    seed = a.seed or dm.new_seed(name)
    given = {"scale": a.scale, "tone": a.tone, "magic": a.magic, "era": a.era, "danger": a.danger, "content_mix": a.content_mix}
    resolved, records = roll_blank_dials(seed, given)
    init_args = argparse.Namespace(scale=resolved["scale"], tone=resolved["tone"], magic=resolved["magic"], era=resolved["era"],
                                   danger=resolved["danger"], party_size=a.party_size, start_level=a.start_level,
                                   content_mix=resolved["content_mix"], must=a.must, must_not=a.must_not, lang=a.lang,
                                   seed=seed, concurrency=a.concurrency, economy=a.economy, fixture=a.fixture)
    rc = dm.init(name, init_args)
    if rc != 0:
        return rc
    data = dm.load(name)
    data["_meta"]["auto_approve"] = bool((a.fixture or name.startswith("_test-")) and not a.ask_approval)
    data["dice_log"].extend(records)
    data["phases"]["P0"]["status"] = "awaiting_approval"
    data["phases"]["P0"]["started"] = data["phases"]["P0"].get("started") or now_iso()
    dm.save(name, data, "designer.py new")
    card = p0_card(name, data, records)
    arm(name, "birth", a.session_id)
    for r in records:
        print(f"  zar: {r['label']} {r['notation']} → {r['raw']} = {r['row_id']}")
    print(f"designer: {name} initialised (seed {seed}, auto_approve {data['_meta']['auto_approve']}); guard armed for birth")
    print(f"designer: P0 card {card}")
    if data["_meta"]["auto_approve"]:
        return approve_phase(name, "P0", str(card), onay=True)
    print("designer: P0 awaits `onay`")
    return 0


# ── phase verbs ───────────────────────────────────────────────────────────────

def phase_begin(campaign: str, phase: str, as_json: bool, session_id: str | None) -> int:
    m = dm.load(campaign)
    if m["_meta"].get("mode") != "birth":
        print("designer: manifest mode is not birth; use set-mode birth or `detail`", file=sys.stderr)
        return 1
    prev = dm.PHASES[dm.PHASES.index(phase) - 1] if phase != "P0" else None
    if prev and m["phases"][prev]["status"] != "approved":
        print(f"designer: {prev} is {m['phases'][prev]['status']}, not approved; {phase} cannot begin", file=sys.stderr)
        return 1
    arm(campaign, "birth", session_id)
    dm.reconcile(campaign, quiet=True)
    data = dm.load(campaign)
    ph = data["phases"][phase]
    if ph["status"] in ("pending", "prerolled", "stale", "failed", "partial"):
        ph["status"] = "running"
        ph["started"] = ph.get("started") or now_iso()
        ph["attempt"] = max(1, int(ph.get("attempt") or 1))
    if not ph.get("roster") and dp.prompt_for(phase, None) is None:
        ph["roster"] = document_roster(campaign, phase)
        ph["skeleton"] = {"status": "n/a", "agent": None}
    dm.save(campaign, data, f"designer.py phase {phase} begin")
    out = pending_with_prompts(campaign, phase)
    if as_json:
        print(json.dumps(out, indent=2, ensure_ascii=False))
    else:
        print(f"designer: {phase} attempt {out['attempt']}, skeleton {out['skeleton'].get('status')}, "
              f"{len(out['entities'])} pending of {len(ph.get('roster') or [])}")
        if out["skeleton"].get("prompt"):
            print(f"  skeleton -> {out['skeleton']['prompt_cmd']}")
        for e in out["entities"]:
            print(f"  {e['id']:<28} {e['status']:<8} {e.get('prompt') or '?':<16} files {len(e['files'])}")
    return 0


def document_roster(campaign: str, phase: str) -> list[str]:
    """Single-writer phases have no skeleton: the roster is the document(s) the phase writes."""
    slug = campaign.replace("-", "_")
    proj = (read_json(design_dir(campaign) / "entities.json") or {}).get("entities", {})
    if phase == "P1":
        return [f"premise_{slug}"]
    if phase == "P2":
        return ["doc_cosmology"]
    if phase == "P8":
        cultures = [eid for eid, e in proj.items() if e.get("type") == "polity"]
        return [f"primer_{eid}" for eid in cultures] or ["primer_all"]
    if phase == "P9":
        threads = [f"thread_{eid[3:]}" for eid, e in proj.items() if e.get("type") == "pc"]
        return threads + ["doc_session1"]
    return []


def render_cmd(campaign: str, name: str, entity_id: str | None, attempt: int, order: int = 1) -> str:
    cmd = f"py -X utf8 {SCRIPTS / 'design_prompts.py'} -c {campaign} render {name}"
    if entity_id:
        cmd += f" --id {entity_id}"
    cmd += f" --attempt {attempt}"
    if order != 1:
        cmd += f" --critic-order {order}"
    return cmd


def prompt_bundle(campaign: str, phase: str, name: str, entity_id: str | None, attempt: int) -> dict:
    """The render command, a rendered copy under design/_prompts/ (readable by the conductor) and the critic count."""
    out_dir = design_dir(campaign) / "_prompts" / phase
    out_dir.mkdir(parents=True, exist_ok=True)
    stem = entity_id or "skeleton"
    text = dp.render(campaign, name, entity_id, attempt)
    path = out_dir / f"{stem}.md"
    path.write_text(text, encoding="utf-8", newline="\n")
    fm, _ = dp.load(name)
    bundle = {"prompt": name, "prompt_cmd": render_cmd(campaign, name, entity_id, attempt), "prompt_file": str(path),
              "prompt_chars": len(text), "critics": int(fm.get("critics") or 1), "effort": fm.get("effort", "medium")}
    if entity_id:
        crit = dp.render(campaign, "critic", entity_id, attempt, 1)
        cpath = out_dir / f"{stem}.critic.md"
        cpath.write_text(crit, encoding="utf-8", newline="\n")
        bundle["critic_cmd"] = render_cmd(campaign, "critic", entity_id, attempt)
        bundle["critic_file"] = str(cpath)
        if bundle["critics"] > 1:
            bundle["critic2_cmd"] = render_cmd(campaign, "critic", entity_id, attempt, 2)
    return bundle


def pending_with_prompts(campaign: str, phase: str) -> dict:
    data = dm.load(campaign)
    canonical = (read_json(dm_only_dir(campaign) / "entities.json") or {}).get("entities", {})
    ph = data["phases"][phase]
    attempt = max(1, int(ph.get("attempt") or 1))
    reads = ph.get("reads") or {}
    rows = []
    for eid in ph.get("roster") or []:
        row = data["entities"].get(eid, {"status": "pending", "attempt": 0})
        if dm.ENTITY_RANK.get(row.get("status", "pending"), 0) >= dm.ENTITY_RANK["merged"]:
            continue
        budget = dm.read_budget(campaign, canonical, eid) if eid in canonical else []
        files = list(dict.fromkeys(budget + list(reads.get(eid) or [])))
        entry = {"id": eid, "status": row.get("status", "pending"), "attempt": int(row.get("attempt") or 0),
                 "last_error": row.get("last_error"), "files": files}
        name = dp.prompt_for(phase, eid)
        if name:
            entry.update(prompt_bundle(campaign, phase, name, eid, attempt))
        rows.append(entry)
    skeleton = dict(ph.get("skeleton") or {})
    sk_name = dp.prompt_for(phase, None)
    if sk_name and skeleton.get("status") in (None, "pending"):
        skeleton.update(prompt_bundle(campaign, phase, sk_name, None, attempt))
    phase_critic = {"prompt": "phase_critic", "prompt_cmd": render_cmd(campaign, "phase_critic", None, attempt)}
    wishes_critic = {"prompt": "wishes_critic", "prompt_cmd": render_cmd(campaign, "wishes_critic", None, attempt)}
    return {"campaign": campaign, "phase": phase, "attempt": attempt, "auto_approve": auto_approve(data),
            "skeleton": skeleton, "directions": ph.get("directions", []), "seed": data["seed"]["master"],
            "entities": rows, "phase_critic": phase_critic, "wishes_critic": wishes_critic,
            "workflow": "design-skeleton" if (skeleton.get("prompt") and skeleton.get("status") in (None, "pending")) else "design-fanout"}


def record_critics(campaign: str, phase: str) -> int:
    """Critic returns saved as <id>.critic<N>[.loopK].json in staging go to the manifest, ids and codes only."""
    staging = design_dir(campaign) / "_staging" / phase
    if not staging.is_dir():
        return 0
    merged = staging / "merged"
    n = 0
    for path in sorted(staging.glob("*.critic*.json")):
        m = re.match(r"^(?P<stem>.+?)\.critic(?P<order>\d)(?:\.loop\d+)?\.json$", path.name)
        order = int(m.group("order")) if m else 1
        proc = run_script("design_approval.py", campaign, "critique", "--phase", phase, "--file", str(path), "--critic", str(order))
        if proc.returncode == 0:
            merged.mkdir(exist_ok=True)
            path.replace(merged / path.name)
            n += 1
        else:
            print(f"designer: critic return {path.name} refused: {proc.stderr.strip()}", file=sys.stderr)
    if n:
        print(f"designer: {phase} {n} critic return(s) recorded")
    return n


def phase_merge(campaign: str, phase: str, day: int) -> int:
    record_critics(campaign, phase)
    proc = run_script("registry.py", campaign, "merge", "--phase", phase, "--day", str(day))
    print(proc.stdout.strip())
    if proc.returncode != 0:
        print(proc.stderr.strip(), file=sys.stderr)
        return 1
    seed = run_script("design_seed.py", campaign, "--phase", phase)
    print(seed.stdout.strip())
    if seed.returncode != 0:
        print(seed.stderr.strip(), file=sys.stderr)
        return 1
    absorb_skeleton(campaign, phase)
    dm.reconcile(campaign, quiet=True)
    data = dm.load(campaign)
    ph = data["phases"][phase]
    if ph["status"] in ("running", "generated", "partial"):
        ph["status"] = "merged" if not any(data["entities"].get(e, {}).get("status") in ("pending", "staged", "failed")
                                           for e in ph.get("roster") or []) else "partial"
        dm.save(campaign, data, f"designer.py phase {phase} merge")
    print(f"designer: {phase} {data['phases'][phase]['status']}")
    return 0


def absorb_skeleton(campaign: str, phase: str) -> bool:
    """A skeleton agent's skeleton.json (roster, assignments, reads) becomes the phase's plan; the file moves to merged/."""
    staging = design_dir(campaign) / "_staging" / phase
    src = staging / "skeleton.json"
    if not src.is_file():
        return False
    sk = read_json(src) or {}
    data = dm.load(campaign)
    ph = data["phases"][phase]
    roster = [x for x in (sk.get("roster") or []) if isinstance(x, str)]
    ph["roster"] = roster
    ph["assignments"] = {k: v for k, v in (sk.get("assignments") or {}).items() if isinstance(v, str)}
    ph["reads"] = {k: list(v) for k, v in (sk.get("reads") or {}).items() if isinstance(v, list)}
    ph["skeleton"] = {"status": "merged", "agent": sk.get("agent") or (ph.get("skeleton") or {}).get("agent")}
    for eid in roster:
        data["entities"].setdefault(eid, {"phase": phase, "status": "pending", "attempt": 0, "critique_loops": 0,
                                          "last_error": None, "file": None, "stage_file": None, "agent": None})
    dm.save(campaign, data, f"designer.py phase {phase} merge (skeleton)")
    merged = staging / "merged"
    merged.mkdir(exist_ok=True)
    src.replace(merged / "skeleton.json")
    print(f"designer: {phase} skeleton absorbed - roster {len(roster)}, assignments {len(ph['assignments'])}")
    return True


def phase_check(campaign: str, phase: str) -> int:
    proc = run_script("design_check.py", campaign, "--phase", phase, "--redact", "--json")
    try:
        findings = json.loads(proc.stdout or "[]")
    except json.JSONDecodeError:
        print(proc.stdout.strip())
        print(proc.stderr.strip(), file=sys.stderr)
        return 1
    if not isinstance(findings, list):
        findings = findings.get("findings") or []
    errors = sum(1 for f in findings if f.get("severity") == "error")
    warnings = sum(1 for f in findings if f.get("severity") == "warning")
    result = {"findings": findings}
    data = dm.load(campaign)
    ph = data["phases"][phase]
    ph["validator"] = {"at": now_iso(), "errors": errors, "warnings": warnings}
    if ph["status"] in ("merged", "partial") and errors == 0:
        ph["status"] = "validated"
    dm.save(campaign, data, f"designer.py phase {phase} check")
    print(f"designer: {phase} validator — {errors} errors, {warnings} warnings")
    for f in (result.get("findings") or [])[:40]:
        print(f"  {f.get('severity', '?'):<8} {f.get('module', ''):<9} {f.get('entity', '') or '':<30} {f.get('code', '')}")
    return 0 if errors == 0 else 1


def phase_card(campaign: str, phase: str) -> int:
    script = SCRIPTS / "design_approval.py"
    path = design_dir(campaign) / CARD_DIR / f"{phase}.card.md"
    if script.is_file():
        proc = run_script("design_approval.py", campaign, "card", "--phase", phase, "--out", str(path))
        print(proc.stdout.strip())
        if proc.returncode != 0:
            print(proc.stderr.strip(), file=sys.stderr)
            return 1
    else:
        data = dm.load(campaign)
        ph = data["phases"][phase]
        roster = ph.get("roster") or []
        lines = [f"# {phase} — faz kartı ({campaign})", "", f"- **Durum:** {ph['status']} · **Deneme:** {ph.get('attempt')}",
                 f"- **Varlıklar:** {len(roster)} (" + ", ".join(sorted(roster)) + ")",
                 f"- **Doğrulayıcı:** {ph.get('validator') or '—'}", ""]
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    data = dm.load(campaign)
    ph = data["phases"][phase]
    if ph["status"] in ("validated", "critiqued", "merged"):
        ph["status"] = "awaiting_approval"
        dm.save(campaign, data, f"designer.py phase {phase} card")
    print(f"designer: {phase} card {path}")
    return 0


def approve_phase(campaign: str, phase: str, card: str | None, onay: bool, round_text: str | None = None,
                  scope: str | None = None) -> int:
    m = dm.load(campaign)
    if round_text:
        rc = dm.approve(campaign, argparse.Namespace(phase=phase, card=None, commit=None, round=round_text,
                                                    scope=scope or "fact", affected=None))
        return rc
    if not (auto_approve(m) or onay):
        print("designer: a real birth is approved only with the player's explicit `onay` (pass --onay after they typed it)",
              file=sys.stderr)
        return 1
    if card is None:
        card = str(design_dir(campaign) / CARD_DIR / f"{phase}.card.md")
        if not Path(card).is_file():
            rc = phase_card(campaign, phase)
            if rc != 0:
                return rc
    sha = design_commit(campaign, f"{phase} approved")
    rc = dm.approve(campaign, argparse.Namespace(phase=phase, card=card, commit=sha, round=None, scope=None, affected=None))
    if rc == 0:
        print(f"designer: {phase} approved ({'auto' if auto_approve(m) else 'onay'}; commit {sha or 'none'})")
        if not auto_approve(m):
            print("designer: waiting for `devam` before the next phase")
    return rc


def phase_rerun(campaign: str, phase: str, reason: str, reseed: bool) -> int:
    data = dm.load(campaign)
    ph = data["phases"][phase]
    ph["attempt"] = int(ph.get("attempt") or 1) + 1
    ph["status"] = "pending"
    ph["skeleton"] = {"status": "pending", "agent": None}
    ph.setdefault("directions", []).append(reason)
    if reseed:
        data["seed"]["master"] = dm.new_seed(campaign)
        data["seed"]["reseeded_at"] = now_iso()
    for eid in ph.get("roster") or []:
        data["entities"].pop(eid, None)
    ph["roster"] = []
    dm.save(campaign, data, f"designer.py phase {phase} rerun")
    if phase != dm.PHASES[-1]:
        dm.stale(campaign, argparse.Namespace(from_phase=phase, reason=f"{phase} rerun: {reason}"))
    staging = design_dir(campaign) / "_staging" / phase
    if staging.is_dir():
        k = 1
        while (staging.parent / f"{phase}.attempt-{k}").exists():
            k += 1
        staging.rename(staging.parent / f"{phase}.attempt-{k}")
    print(f"designer: {phase} reset to attempt {ph['attempt']}{' with a new seed' if reseed else ''}; preroll it again")
    return 0


# ── status / abandon / commit ───────────────────────────────────────────────

def status(campaign: str, as_json: bool) -> int:
    m = dm.load(campaign)
    marker = read_json(marker_path()) or None
    out = {"campaign": campaign, "mode": m["_meta"].get("mode"), "auto_approve": auto_approve(m),
           "armed": bool(marker and marker.get("campaign") == campaign), "marker_mode": (marker or {}).get("mode"),
           "seed": m["seed"]["master"], "dials": m["dials"],
           "phases": {p: {"status": v["status"], "attempt": v.get("attempt"), "roster": len(v.get("roster") or [])}
                      for p, v in m["phases"].items()},
           "public_rolls": len(m["dice_log"]), "secret_rolls": m["dice_log_secret"]["count"],
           "tables": len(dt.list_tables())}
    if as_json:
        print(json.dumps(out, indent=2, ensure_ascii=False))
        return 0
    print(f"designer: {campaign} — mode {out['mode']}, auto_approve {out['auto_approve']}, guard {'armed' if out['armed'] else 'unarmed'}, seed {out['seed']}")
    for p, v in out["phases"].items():
        print(f"  {p}  {v['status']:<18} attempt {v['attempt'] or 0}  roster {v['roster']}")
    print(f"  rolls: {out['public_rolls']} public, {out['secret_rolls']} secret · tables {out['tables']}")
    return 0


def abandon(campaign: str, reason: str) -> int:
    data = dm.load(campaign)
    for ph in data["phases"].values():
        if ph["status"] != "approved":
            ph["status"] = "failed"
    data["_meta"]["abandoned"] = {"at": now_iso(), "reason": reason}
    data["_meta"]["mode"] = "abandoned"
    dm.save(campaign, data, "designer.py abandon")
    used = dd.load_used()
    dropped = len(used.get("campaigns", {}).pop(campaign, {}) or {})
    dd.save_used(used)
    retired = 0
    try:
        import name_registry as nr
        for e in list(nr.list_entries(campaign) or []):
            if nr.retire(e.get("name", ""), campaign):
                retired += 1
    except Exception:
        pass
    marker = read_json(marker_path()) or {}
    if marker.get("campaign") == campaign:
        disarm()
    print(f"designer: {campaign} abandoned — {dropped} used.json tables dropped, {retired} names retired, guard disarmed")
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="the conductor's CLI")
    ap.add_argument("-c", "--campaign", metavar="NAME")
    sub = ap.add_subparsers(dest="verb", required=True)

    n = sub.add_parser("new")
    n.add_argument("name")
    for dial in ("scale", "tone", "magic", "era", "danger"):
        n.add_argument(f"--{dial}", default="?")
    n.add_argument("--party-size", type=int, required=True)
    n.add_argument("--start-level", type=int, default=1)
    n.add_argument("--content-mix", default="?")
    n.add_argument("--must", action="append")
    n.add_argument("--must-not", action="append")
    n.add_argument("--lang", default="tr")
    n.add_argument("--seed")
    n.add_argument("--concurrency", type=int, default=8)
    n.add_argument("--economy", action="store_true")
    n.add_argument("--fixture", action="store_true")
    n.add_argument("--ask-approval", action="store_true", help="a test birth that still waits for onay / devam")
    n.add_argument("--session-id")

    ar = sub.add_parser("arm")
    ar.add_argument("--mode", choices=("birth", "detail", "playtest"), required=True)
    ar.add_argument("--session-id")
    sub.add_parser("disarm")

    pr = sub.add_parser("preroll")
    pr.add_argument("--phase", required=True)
    pr.add_argument("--attempt", type=int)

    ph = sub.add_parser("phase")
    ph.add_argument("phase")
    ph.add_argument("step", choices=("begin", "merge", "check", "card", "approve", "rerun"))
    ph.add_argument("--json", action="store_true")
    ph.add_argument("--day", type=int, default=0)
    ph.add_argument("--card")
    ph.add_argument("--onay", action="store_true")
    ph.add_argument("--round", help="approve: record a correction round instead of approving")
    ph.add_argument("--scope", choices=("fact", "entity", "phase", "direction"))
    ph.add_argument("--reason")
    ph.add_argument("--reseed", action="store_true")
    ph.add_argument("--session-id")

    st = sub.add_parser("status")
    st.add_argument("--json", action="store_true")
    ab = sub.add_parser("abandon")
    ab.add_argument("--reason", required=True)
    cm = sub.add_parser("commit")
    cm.add_argument("--message", required=True)

    a = ap.parse_args(argv)
    if a.verb == "new":
        return new(a)
    if not a.campaign:
        print("designer: -c CAMP is required", file=sys.stderr)
        return 2
    c = a.campaign
    if a.verb == "arm":
        arm(c, a.mode, a.session_id)
        print(f"designer: guard armed for {c} ({a.mode})")
        return 0
    if a.verb == "disarm":
        print("designer: guard disarmed" if disarm() else "designer: guard was not armed")
        return 0
    if a.verb == "preroll":
        return preroll(c, a.phase, a.attempt)
    if a.verb == "phase":
        if a.phase not in dm.PHASES:
            print(f"designer: unknown phase {a.phase}", file=sys.stderr)
            return 2
        if a.step == "begin":
            return phase_begin(c, a.phase, a.json, a.session_id)
        if a.step == "merge":
            return phase_merge(c, a.phase, a.day)
        if a.step == "check":
            return phase_check(c, a.phase)
        if a.step == "card":
            return phase_card(c, a.phase)
        if a.step == "approve":
            return approve_phase(c, a.phase, a.card, a.onay, a.round, a.scope)
        if a.step == "rerun":
            if not a.reason:
                print("designer: rerun needs --reason", file=sys.stderr)
                return 2
            return phase_rerun(c, a.phase, a.reason, a.reseed)
    if a.verb == "status":
        return status(c, a.json)
    if a.verb == "abandon":
        return abandon(c, a.reason)
    if a.verb == "commit":
        sha = design_commit(c, a.message)
        print(f"designer: commit {sha}" if sha else "designer: nothing to commit (or the campaign is git-ignored)")
        return 0
    return 2


if __name__ == "__main__":
    sys.exit(main())
