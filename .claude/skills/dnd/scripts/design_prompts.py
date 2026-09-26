#!/usr/bin/env python3
"""
design_prompts.py — renders the designer's agent prompts (plan item 19.1-19.3, slice 1c item 2).

Prompts live in prompts/design/*.md: a front-matter block (phase, role, kind, effort, critics,
schema, template) and a body with {{placeholders}}. `render` fills them from the manifest
(dials, seed, directions), the PUBLIC projection (names, summaries; never the canonical registry),
the phase's rolls and assignments, the entity's read budget, the rubric rows for a critic, and the
shared preamble _common.md. The rendered text is what a Workflow passes to an agent; the agent's
return is the schema in prompts/design/schemas/<schema>.json and nothing else.

CLI:
  design_prompts.py list
  design_prompts.py check                                    every prompt parses, every placeholder is known
  design_prompts.py -c CAMP render NAME [--id ENTITY] [--attempt N] [--critic-order 1|2] [--out FILE]
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import design_manifest as dm  # noqa: E402
import design_tables as dt  # noqa: E402
from design_io import campaign_dir, design_dir, dm_only_dir, parse_front_matter, read_json  # noqa: E402
from paths import skill_root  # noqa: E402

PROMPTS_DIR = skill_root() / "prompts" / "design"
SCHEMAS_DIR = PROMPTS_DIR / "schemas"
ROLES = ("skeleton", "writer", "critic", "phase_critic", "ask")
PLACEHOLDERS = {
    "campaign", "campaign_dir", "skill_dir", "phase", "attempt", "lang", "dials", "scale", "scale_line", "seed",
    "entity_id", "entity_type", "entity_name", "entity_summary", "files", "rolls", "phase_rolls", "directions", "staging_phase",
    "wishes", "template", "prose_path", "mirror_path", "fragment_path", "notes_path", "rubrics", "common",
    "schema", "agent_label", "roster", "party_size", "level_band", "content_mix", "critic_order",
}
PROSE_DIRS = {"npc": "design/npcs", "site": "design/sites", "faction": "design/factions", "region": "design/regions",
              "settlement": "design/settlements", "chapter": "design/chapters", "thread": "design/threads",
              "seedbatch": "design/seeds"}     # each seed batch writes its own file (birth 2: two batches raced on arc.md)
SINGLE_FILES = {"premise": "design/premise.md", "cosmology": "design/cosmology.md", "arc": "design/arc.md",
                "calculus": "design/consequence-calculus.md", "primer": "design/player-primer.md",
                "report": "design/report.md", "session1": "design/session-1.md"}
MIRROR_SINGLE = {"premise": "design/dm-only/premise-secret.md", "cosmology": "design/dm-only/cosmology.md",
                 "arc": "design/dm-only/arc.md", "calculus": "design/dm-only/consequence-calculus.md"}
TEMPLATES = {"npc": "npc.md", "site": "site-skeleton.md", "site_detailed": "site-detailed.md", "faction": "faction.md",
             "region": "region.md", "settlement": "settlement.md", "chapter": "chapter.md", "thread": "thread.md",
             "premise": "premise.md", "cosmology": "cosmology.md", "arc": "arc.md", "calculus": "consequence-calculus.md",
             "primer": "primer.md", "report": "report.md"}


DETAIL_BIRTH_PHASE = {"site": "P6", "settlement": "P3", "npc": "P5", "chapter": "P7"}   # a detail prompt's rolls and rubric

PROMPT_BY_PHASE = {  # phase -> (skeleton prompt, [(id prefix, writer prompt)...]); the first prefix match wins
    "P1": (None, [("premise_", "P1.premise")]),
    "P2": (None, [("doc_cosmology", "P2.cosmos")]),
    "P3": ("P3.skeleton", [("villagebatch_", "P3.villages"), ("region_", "P3.region"), ("settlement_", "P3.settlement")]),
    "P4": ("P4.skeleton", [("calculus_", "P4.calculus"), ("doc_calculus", "P4.calculus"), ("faction_", "P4.faction")]),
    "P5": ("P5.skeleton", [("npcbatch_", "P5.minors"), ("npc_", "P5.npc")]),
    "P6": ("P6.skeleton", [("site_", "P6.site")]),
    "P7": ("P7.skeleton", [("seedbatch_", "P7.seeds"), ("chapter_", "P7.chapter")]),
    "P8": (None, [("primer_", "P8.primer")]),
    "P9": (None, [("doc_session1", "P9.session1"), ("thread_", "P9.thread")]),
    "detail": (None, [("site_", "detail.site"), ("settlement_", "detail.settlement"), ("npc_", "detail.npc"), ("chapter_", "detail.chapter")]),
}


def prompt_for(phase: str, entity_id: str | None) -> str | None:
    """The writer prompt for an entity of a phase, or the phase's skeleton prompt when entity_id is None."""
    skeleton, writers = PROMPT_BY_PHASE.get(phase, (None, []))
    if entity_id is None:
        return skeleton
    for prefix, name in writers:
        if entity_id.startswith(prefix):
            return name
    return None


def critics_for(name: str) -> int:
    fm, _ = load(name)
    return int(fm.get("critics") or 1)


# ── loading ───────────────────────────────────────────────────────────────────

def list_prompts() -> list[str]:
    return sorted(p.stem for p in PROMPTS_DIR.glob("*.md") if not p.name.startswith(("_", "README")))


def load(name: str) -> tuple[dict, str]:
    path = PROMPTS_DIR / f"{name}.md"
    if not path.is_file():
        raise FileNotFoundError(f"design_prompts: no prompt {name!r} under {PROMPTS_DIR}")
    text = path.read_text(encoding="utf-8").replace("\r\n", "\n")
    fm = parse_front_matter(text)
    if "critics" in fm:
        fm["critics"] = int(fm["critics"])
    body = text.split("---", 2)[2].lstrip("\n") if text.startswith("---") else text
    return fm, body


def common_text() -> str:
    path = PROMPTS_DIR / "_common.md"
    text = path.read_text(encoding="utf-8").replace("\r\n", "\n") if path.is_file() else ""
    return text.split("---", 2)[2].strip() if text.startswith("---") else text.strip()


def schema_text(name: str) -> str:
    path = SCHEMAS_DIR / f"{name}.json"
    return path.read_text(encoding="utf-8").strip() if path.is_file() else "{}"


def placeholders_in(text: str) -> set[str]:
    return set(re.findall(r"\{\{([a-z_]+)\}\}", text))


# ── context ───────────────────────────────────────────────────────────────────

def scale_line(manifest: dict, phase: str) -> str:
    sc = dt.scale_row(manifest["dials"]["scale"])
    parts = {
        "P1": f"tensions {sc['tensions']}, trope breaks {sc['trope_breaks']}, signature mechanic chance {sc['signature_mechanic_chance']}%",
        "P2": f"gods {sc['gods']}, planes touched {sc['planes_touched']}, ages {sc['history']['ages']}, dated events {sc['history']['dated_events']} over {sc['history']['years_covered']} years, deep past {sc['history']['deep_past_events']}",
        "P3": f"polities {sc['polities']}, regions {sc['regions']}, settlements {sc['settlements']}",
        "P4": f"factions {sc['factions']['count']} with quota {sc['factions']['quota']}, antagonists {sc['antagonists']}",
        "P5": f"named NPCs {sc['named_npcs']}, tiers {sc['npc_tiers']}",
        "P6": f"sites {sc['sites']['count']} by role {sc['sites']['roles']}, detailed at birth {sc['sites']['detailed_at_birth']}",
        "P7": f"acts {sc['acts']}, chapters {sc['chapters']}, beats {sc['beats']}, quest seeds {sc['quest_seeds']}, sockets per PC {sc['sockets_per_pc']}",
        "P8": "the primer per culture section; the report by script",
        "P9": f"sockets per PC {sc['sockets_per_pc']}, crossings per act {dt.scale_shared()['crossings_per_act']}, imbalance cap {dt.scale_shared()['thread_imbalance_max']}",
    }
    return f"scale {sc['value']}: " + parts.get(phase, "")


def dials_line(manifest: dict) -> str:
    d = manifest["dials"]
    return (f"scale {d['scale']} · tone {d['tone']} · magic {d['magic']} · era {d['era']} · danger {d['danger']} · "
            f"party {d['party_size']} at level {d['start_level']} (band {d['level_band'][0]}-{d['level_band'][1]}) · "
            f"content mix {', '.join(d['content_mix'])} · narration {d['lang']}")


def rolls_for(manifest: dict, phase: str, entity_id: str | None) -> tuple[str, str]:
    """(this entity's rolls, every public roll of the phase) as bullet lines; secret rolls never."""
    phase_recs = [r for r in manifest["dice_log"] if r.get("phase") == phase]
    assignments = (manifest["phases"].get(phase) or {}).get("assignments") or {}
    prefixes = [k for k, v in assignments.items() if v == entity_id] if entity_id else []

    def line(r: dict) -> str:
        if "value" in r and not r.get("row_id"):
            # a count roll: the number to produce is `value`; the die face is only how it was rolled
            how = f" ({r.get('notation')} → {r.get('raw')})" if r.get("raw") is not None else ""
            return f"- `{r['label']}` = **{r['value']}** — produce exactly this many{how}"
        what = r.get("row_id") or r.get("raw")
        extra = f" (forced: {r['forced_by']})" if r.get("forced_by") else ""
        return f"- `{r['label']}` → **{what}**{extra}"
    mine = [line(r) for r in phase_recs if any(r["label"] == p or r["label"].startswith(p + ".") for p in prefixes)]
    return "\n".join(mine) or "- (no rolls assigned to this entity)", "\n".join(line(r) for r in phase_recs) or "- (none)"


def rubric_lines(phase: str, scope: str | None, order: int) -> str:
    rows = [r for r in dt.rows("rubrics.yaml#phase_rubric") if r["phase"] == phase]
    if scope:
        rows = [r for r in rows if r["scope"] == scope] or rows
    rows += [r for r in dt.rows("rubrics.yaml#special") if r["id"] in ("rubric_cliche", "rubric_english_names", "rubric_leak")]
    if order == 2:
        rows = list(reversed(rows))
    out = []
    for r in rows:
        out.append(f"- **{r['id']}** ({r['scope']}, effort {r['effort']}): {r['question']}\n  - fails when: {r['fails_when']}")
    return "\n".join(out)


def entity_paths(entity_id: str | None, kind: str, detailed: bool = False) -> dict:
    etype = entity_id.split("_", 1)[0] if entity_id else kind
    if etype in PROSE_DIRS and entity_id:
        prose = f"{PROSE_DIRS[etype]}/{entity_id}.md"
        mirror = f"design/dm-only/{PROSE_DIRS[etype][7:]}/{entity_id}.md"
    else:
        prose = SINGLE_FILES.get(kind, f"design/{kind}.md")
        mirror = MIRROR_SINGLE.get(kind, "(none)")
    tkey = "site_detailed" if (etype == "site" and detailed) else etype if etype in TEMPLATES else kind
    template = f"templates/design/{TEMPLATES.get(tkey, 'README.md')}"
    return {"prose_path": prose, "mirror_path": mirror, "template": template}


def read_budget(campaign: str, entity_id: str | None) -> list[str]:
    if not entity_id:
        return []
    canonical = (read_json(dm_only_dir(campaign) / "entities.json") or {}).get("entities", {})
    if entity_id not in canonical:
        return []
    return dm.read_budget(campaign, canonical, entity_id)


def render(campaign: str, name: str, entity_id: str | None = None, attempt: int | None = None,
           critic_order: int = 1, question: str | None = None, phase_override: str | None = None) -> str:
    fm, body = load(name)
    manifest = dm.load(campaign)
    phase = str(fm.get("phase") or "")
    projection_early = (read_json(design_dir(campaign) / "entities.json") or {}).get("entities", {})
    etype_early = (projection_early.get(entity_id or "", {}).get("type") or (entity_id or "").split("_", 1)[0])
    staging_phase = None
    if phase == "detail" or phase_override == "detail":
        # a detail prompt (play, slice 1d): the rolls and the rubric are the entity's birth phase, the fragment
        # and the notes go to design/_staging/detail/
        staging_phase = "detail"
        phase = DETAIL_BIRTH_PHASE.get(etype_early, "P6")
    elif phase not in dm.PHASES:
        # an all-phase prompt (the critics) serves the phase the conductor names, else the entity's phase;
        # tuning birth 1 rendered every critic for "Phase all" with the three special rubrics only
        phase = phase_override or str(manifest.get("entities", {}).get(entity_id or "", {}).get("phase") or "")
        if phase not in dm.PHASES and str(fm.get("role") or "") in ("critic", "phase_critic"):
            raise SystemExit(f"design_prompts: {name} is an all-phase prompt; pass --phase PN (entity {entity_id or '-'} has no phase)")
    staging_phase = staging_phase or phase
    kind = str(fm.get("kind") or "")
    role = str(fm.get("role") or "")
    ph = manifest["phases"].get(phase) or {}
    attempt = attempt or int(ph.get("attempt") or 1)
    projection = (read_json(design_dir(campaign) / "entities.json") or {}).get("entities", {})
    ent = projection.get(entity_id or "", {})
    paths = entity_paths(entity_id, kind, detailed=bool(fm.get("detailed")))
    mine, all_rolls = rolls_for(manifest, phase, entity_id)
    files = read_budget(campaign, entity_id)
    d = manifest["dials"]
    scope = str(fm.get("rubric_scope") or "") or None
    directions = "\n".join(f"- {x}" for x in ph.get("directions") or []) or "- (none)"
    erow = manifest.get("entities", {}).get(entity_id or "", {})
    if erow.get("last_error") and role == "writer":
        directions += (f"\n- **Attempt {attempt}:** your previous fragment was refused by the registry — {erow['last_error']} "
                       "Repair exactly that; everything else stays as it was.")
    ctx = {
        "campaign": campaign, "staging_phase": staging_phase, "campaign_dir": str(campaign_dir(campaign)).replace("\\", "/"),
        "skill_dir": str(skill_root()).replace("\\", "/"), "phase": phase, "attempt": str(attempt), "lang": d["lang"],
        "dials": dials_line(manifest), "scale": d["scale"], "scale_line": scale_line(manifest, phase) if phase in dm.PHASES else "",
        "seed": manifest["seed"]["master"], "entity_id": entity_id or "(skeleton)", "entity_type": (entity_id or kind).split("_", 1)[0],
        "entity_name": ent.get("name") or "(not yet named)", "entity_summary": ent.get("summary") or "(no summary yet)",
        "files": "\n".join(f"- {f}" for f in files) or "- (the skeleton decides; read the files it names)",
        "rolls": mine, "phase_rolls": all_rolls, "directions": question if question else directions,
        "wishes": f"must: {', '.join(d['wishes']['must']) or '—'}; must not: {', '.join(d['wishes']['must_not']) or '—'}",
        "template": paths["template"], "prose_path": paths["prose_path"], "mirror_path": paths["mirror_path"],
        "fragment_path": f"design/_staging/{staging_phase}/{entity_id or 'skeleton'}.json",
        "notes_path": f"design/_staging/{staging_phase}/{entity_id or 'skeleton'}.notes.md",
        "rubrics": rubric_lines(phase, scope, critic_order) if role in ("critic", "phase_critic") else "",
        "common": common_text(), "schema": schema_text(str(fm.get("schema") or "writer")),
        "agent_label": f"{phase}.{entity_id or role}.a{attempt}", "roster": ", ".join(ph.get("roster") or []) or "(none yet)",
        "party_size": str(d["party_size"]), "level_band": f"{d['level_band'][0]}-{d['level_band'][1]}",
        "content_mix": ", ".join(d["content_mix"]), "critic_order": str(critic_order),
    }
    text = body
    for key, value in ctx.items():
        text = text.replace("{{" + key + "}}", value)
    left = placeholders_in(text)
    if left:
        raise ValueError(f"design_prompts: unfilled placeholders in {name}: {sorted(left)}")
    return text


def check() -> list[str]:
    problems = []
    for name in list_prompts():
        try:
            fm, body = load(name)
        except Exception as exc:  # pragma: no cover
            problems.append(f"{name}: {exc}")
            continue
        for key in ("phase", "role", "kind", "effort", "schema"):
            if key not in fm:
                problems.append(f"{name}: front matter lacks {key}")
        if fm.get("role") not in ROLES:
            problems.append(f"{name}: role {fm.get('role')!r} not in {ROLES}")
        unknown = placeholders_in(body) - PLACEHOLDERS
        if unknown:
            problems.append(f"{name}: unknown placeholders {sorted(unknown)}")
        if fm.get("schema") and not (SCHEMAS_DIR / f"{fm['schema']}.json").is_file():
            problems.append(f"{name}: schema {fm['schema']} missing")
    return problems


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="render the designer's agent prompts")
    ap.add_argument("-c", "--campaign")
    sub = ap.add_subparsers(dest="verb", required=True)
    sub.add_parser("list")
    sub.add_parser("check")
    r = sub.add_parser("render")
    r.add_argument("name")
    r.add_argument("--id")
    r.add_argument("--attempt", type=int)
    r.add_argument("--critic-order", type=int, default=1)
    r.add_argument("--phase", help="all-phase prompts (the critics): the phase they serve")
    r.add_argument("--question", help="ask prompts: the yes/no question")
    r.add_argument("--out")
    a = ap.parse_args(argv)
    if a.verb == "list":
        for name in list_prompts():
            fm, _ = load(name)
            print(f"  {name:<28} {fm.get('phase', ''):<6} {fm.get('role', ''):<13} {fm.get('kind', ''):<12} effort {fm.get('effort', '')}")
        return 0
    if a.verb == "check":
        problems = check()
        for p in problems:
            print("  " + p)
        print(f"design_prompts: {len(list_prompts())} prompts, {len(problems)} problems")
        return 1 if problems else 0
    if not a.campaign:
        print("design_prompts: render needs -c CAMP", file=sys.stderr)
        return 2
    text = render(a.campaign, a.name, a.id, a.attempt, a.critic_order, a.question, a.phase)
    if a.out:
        Path(a.out).write_text(text, encoding="utf-8", newline="\n")
        print(f"design_prompts: wrote {a.out} ({len(text)} chars)")
    else:
        print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
