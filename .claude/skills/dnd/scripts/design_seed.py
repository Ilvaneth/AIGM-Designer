#!/usr/bin/env python3
"""
design_seed.py — idempotent seeding of the play-time stores from merged fragments.

Plan item 19.3 and 19.11; docs/schemas/staging-fragment.md (`graph`, `seeds[]`).

A fragment's `graph` block and `seeds[]` list name calls into the stores the
designer only seeds and never owns: factions.py, goals.py, campaign_graph.py,
channels.py, calendar.py, site_progress.py, name_registry.py. This script
runs those calls through each store's own CLI (so the store stays its single
writer) and records every call it made in design.json's `seeded[]` ledger, so
a rerun of the same phase makes no second call: double run, one result.

Seed entries look like {"store": "goals", "op": "add", "args": {...}}; the
ledger key is <store>:<id>, or graph:node:<id> / graph:edge:<from>:<to>:<type>.
`names` (name_registry add) is written only at phase approval, so the
conductor runs `--stores names` then and everything else right after merge.

CLI:
  design_seed.py -c CAMP --phase PN [--stores factions,goals,graph,channels,calendar,site_progress,names]
                 [--fragment FILE] [--session N] [--dry-run]
Exit codes: 0 every call succeeded or was already seeded · 1 some call failed · 2 usage
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from design_io import design_dir, dm_only_dir, read_json  # noqa: E402
from design_manifest import load as load_manifest, mark_seeded  # noqa: E402

HERE = Path(__file__).resolve().parent
ALL_STORES = ("factions", "goals", "graph", "channels", "calendar", "site_progress", "names")
DEFAULT_STORES = tuple(s for s in ALL_STORES if s != "names")


def flag(name: str) -> str:
    return "--" + name.replace("_", "-")


def argv_for(store: str, op: str, args: dict, campaign: str, session: int | None) -> list[str] | None:
    """Translate a seed entry into the store's CLI argv, or None when unsupported."""
    def kv(exclude=()):
        out: list[str] = []
        for k, v in args.items():
            if k in exclude or v is None or v is False:
                continue
            if v is True:
                out.append(flag(k))
            elif isinstance(v, list):
                if k == "step":
                    for s in v:
                        out += ["--step", str(s)]
                else:
                    out += [flag(k), ";".join(map(str, v)) if store == "factions" else ",".join(map(str, v))]
            else:
                out += [flag(k), str(v)]
        return out

    if store == "factions":
        if op == "add":
            return ["factions.py", "-c", campaign, "add"] + kv()
        if op == "set":
            return ["factions.py", "-c", campaign, "set", str(args["id"])] + kv(exclude=("id",))
        if op == "stance":
            a = dict(args)
            mutual = a.pop("mutual", False)
            return ["factions.py", "-c", campaign, "stance", "--from", str(a["from"]), "--to", str(a["to"]),
                    "--level", str(a["level"])] + (["--mutual"] if mutual else [])
        if op == "op":
            a = dict(args)
            fid = a.pop("id")
            steps = a.pop("steps", a.pop("step", []))
            out = ["factions.py", "-c", campaign, "op", str(fid)]
            for s in steps:
                out += ["--step", str(s)]
            return out + kv_of(a)
        return None
    if store == "goals":
        if op in ("add", "set", "achieve", "status"):
            a = dict(args)
            if session is not None and "session" not in a and op != "status":
                a["session"] = session
            return ["goals.py", op, "--campaign", campaign] + kv_of(a)
        return None
    if store == "channels":
        if op == "add":
            return ["channels.py", "-c", campaign, "add"] + kv_of(args, join=",")
        return None
    if store == "calendar":
        if op == "init":
            return ["calendar.py", "-c", campaign, "init"] + kv_of(args, join=",")
        return None
    if store == "site_progress":
        if op == "open":
            a = dict(args)
            site = a.pop("site")
            return ["site_progress.py", "-c", campaign, "open", str(site)] + kv_of(a, join=",")
        return None
    if store == "names":
        if op == "add":
            a = dict(args)
            a.setdefault("campaign", campaign)
            a.setdefault("session", session if session is not None else 0)
            return ["name_registry.py", "add"] + kv_of(a)
        return None
    return None


def kv_of(args: dict, join: str = ";") -> list[str]:
    out: list[str] = []
    for k, v in args.items():
        if v is None or v is False:
            continue
        if v is True:
            out.append(flag(k))
        elif isinstance(v, list):
            out += [flag(k), join.join(map(str, v))]
        else:
            out += [flag(k), str(v)]
    return out


def key_for(store: str, op: str, args: dict) -> str:
    ident = args.get("id") or args.get("site") or args.get("name") or op
    if store == "factions" and op == "stance":
        ident = f"{args.get('from')}:{args.get('to')}"
    if store == "factions" and op == "op":
        ident = f"{args.get('id')}:op"
    if store == "calendar":
        ident = "init"
    return f"{store}:{ident}"


def graph_calls(campaign: str, block: dict, secret_ids: set) -> list[tuple[str, list[str]]]:
    calls: list[tuple[str, list[str]]] = []
    for n in block.get("nodes", []):
        nid = n.get("id")
        if not nid:
            continue
        name = nid if nid in secret_ids else n.get("name", nid)     # a secret entity's node carries its id
        argv = ["campaign_graph.py", "add-node", "--campaign", campaign, "--type", str(n.get("type", "npc")),
                "--name", name, "--id", nid, "--allow-duplicate-name"]
        if n.get("tags"):
            argv += ["--tags", ",".join(n["tags"])]
        if n.get("summary") and nid not in secret_ids:
            argv += ["--summary", n["summary"]]
        calls.append((f"graph:node:{nid}", argv))
    for e in block.get("edges", []):
        if not (e.get("from") and e.get("to") and e.get("type")):
            continue
        argv = ["campaign_graph.py", "add-edge", "--campaign", campaign, "--from", e["from"], "--to", e["to"],
                "--type", e["type"], "--since", str(e.get("since_session", 0))]
        if e.get("note"):
            argv += ["--note", e["note"]]
        calls.append((f"graph:edge:{e['from']}:{e['to']}:{e['type']}", argv))
    return calls


def run_call(argv: list[str], dry: bool) -> bool:
    script = HERE / argv[0]
    cmd = [sys.executable, str(script)] + argv[1:]
    if dry:
        print("   would run: " + " ".join(json.dumps(a) if " " in a else a for a in argv))
        return True
    proc = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
    if proc.returncode != 0:
        print(f"   ✗ {argv[0]} {argv[1] if len(argv) > 1 else ''}: {(proc.stderr or proc.stdout).strip()[:300]}",
              file=sys.stderr)
        return False
    return True


def seed(campaign: str, phase: str | None, stores: tuple, fragment: str | None, session: int | None,
         dry: bool) -> int:
    manifest = load_manifest(campaign)
    ledger = set(manifest.get("seeded", []))
    canonical = (read_json(dm_only_dir(campaign) / "entities.json") or {}).get("entities", {})
    secret_ids = {eid for eid, e in canonical.items() if e.get("secrecy") == "secret"}

    if fragment:
        fragments = [Path(fragment)]
    else:
        merged = design_dir(campaign) / "_staging" / phase / "merged"
        fragments = sorted(merged.glob("*.json")) if merged.is_dir() else []
    if not fragments:
        print(f"design_seed: no merged fragments for {phase}")
        return 0

    calls: list[tuple[str, list[str]]] = []
    node_calls: list[tuple[str, list[str]]] = []
    edge_calls: list[tuple[str, list[str]]] = []
    unsupported: list[str] = []
    for frag_path in fragments:
        frag = read_json(frag_path) or {}
        if "graph" in stores and frag.get("graph"):
            for key, argv in graph_calls(campaign, frag["graph"], secret_ids):
                (node_calls if key.startswith("graph:node:") else edge_calls).append((key, argv))
        for entry in frag.get("seeds") or []:
            store, op, args = entry.get("store"), entry.get("op"), entry.get("args") or {}
            if store not in stores:
                continue
            argv = argv_for(store, op, args, campaign, session)
            if argv is None:
                unsupported.append(f"{frag.get('id')}: {store}.{op}")
                continue
            calls.append((key_for(store, op, args), argv))

    # birth 2: edges ran in fragment order and named nodes a later fragment (or an earlier phase's registry row)
    # would create; every node call goes first, and an endpoint with no node call is synthesised from the registry
    if edge_calls:
        known_nodes = {k[len("graph:node:"):] for k, _ in node_calls} | {k[len("graph:node:"):] for k in ledger if k.startswith("graph:node:")}
        for key, argv in edge_calls:
            for endpoint in (argv[argv.index("--from") + 1], argv[argv.index("--to") + 1]):
                if endpoint in known_nodes or endpoint not in canonical:
                    continue
                ent = canonical[endpoint]
                name = endpoint if endpoint in secret_ids else str(ent.get("name") or endpoint)
                node_calls.append((f"graph:node:{endpoint}", ["campaign_graph.py", "add-node", "--campaign", campaign,
                                                             "--type", str(ent.get("type", "npc")), "--name", name,
                                                             "--id", endpoint, "--allow-duplicate-name"]))
                known_nodes.add(endpoint)
    calls = node_calls + edge_calls + calls

    done, skipped, failed = 0, 0, 0
    for key, argv in calls:
        if key in ledger:
            skipped += 1
            continue
        ok = run_call(argv, dry)
        if ok:
            done += 1
            if not dry:
                mark_seeded(campaign, [key])
                ledger.add(key)
        else:
            failed += 1
    for u in unsupported:
        print(f"   ! unsupported seed skipped: {u}", file=sys.stderr)
    print(f"design_seed: {phase or fragment}: {done} call(s) made, {skipped} already seeded, {failed} failed"
          + (" (dry run)" if dry else ""))
    return 1 if failed else 0


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description="Seed the play-time stores from merged fragments, idempotently")
    p.add_argument("-c", "--campaign", required=True, metavar="NAME")
    p.add_argument("--phase")
    p.add_argument("--fragment")
    p.add_argument("--stores", default=",".join(DEFAULT_STORES))
    p.add_argument("--session", type=int)
    p.add_argument("--dry-run", action="store_true")
    a = p.parse_args(argv)
    if not a.phase and not a.fragment:
        print("design_seed: give --phase or --fragment", file=sys.stderr)
        return 2
    stores = tuple(s.strip() for s in a.stores.split(",") if s.strip())
    bad = [s for s in stores if s not in ALL_STORES]
    if bad:
        print(f"design_seed: unknown store(s) {', '.join(bad)}", file=sys.stderr)
        return 2
    return seed(a.campaign, a.phase, stores, a.fragment, a.session, a.dry_run)


if __name__ == "__main__":
    sys.exit(main())
