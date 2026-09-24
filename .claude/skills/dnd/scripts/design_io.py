#!/usr/bin/env python3
"""
design_io.py — shared I/O for the designer's stores (import surface, no CLI).

Every store the designer writes goes through here so the rules in
docs/schemas/README.md hold everywhere: atomic writes (temp file in the same
directory, then os.replace), `_meta` with schema_version / campaign /
written_by / written_at, JSON with indent=2 and ensure_ascii=False, LF line
endings, a trailing newline. Also the small parsers every script shares: the
front-matter block of a bible file, `[[id]]` wiki-links, the overlay record.

    from design_io import (design_dir, dm_only_dir, read_json, write_json_atomic,
                           stamp_meta, front_matter, wiki_links, overlay_set)
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import sys
import tempfile
import unicodedata
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from paths import find_campaign  # noqa: E402

SCHEMA_VERSION = 1

ENTITY_TYPES = (
    "god", "plane", "era", "event", "polity", "region", "settlement", "district", "place",
    "faction", "npc", "site", "item", "creature", "chapter", "node", "seed", "thread",
    "socket", "pc", "premise", "arc", "signature", "break", "beat",
)
SECRECY = ("public", "discoverable", "secret")

# Overlay fields and their closed values (docs/schemas/overlay.md). None = an id.
OVERLAY_FIELDS: dict[str, tuple | None] = {
    "status": ("skeleton", "detailed", "detailed-stale", "played", "played-improvised"),
    "seen_in_play": (True, False),
    "alive": ("alive", "threatened", "wounded", "fled", "captured", "dead"),
    "location": None,
    "ruler": None,
    "control": None,
}
OVERLAY_WRITERS = (
    "factions.py simulate", "factions.py", "site_progress.py", "campaign_graph.py",
    "registry.py play-set", "registry.py merge",
)

WIKI = re.compile(r"\[\[([a-z0-9_]+)\]\]")
FRONT = re.compile(r"\A---\r?\n(.*?)\r?\n---\r?\n", re.DOTALL)


# ── paths ─────────────────────────────────────────────────────────────────────

def campaign_dir(campaign: str) -> Path:
    return Path(str(find_campaign(campaign)))


def design_dir(campaign: str) -> Path:
    return campaign_dir(campaign) / "design"


def dm_only_dir(campaign: str) -> Path:
    return design_dir(campaign) / "dm-only"


def rel(campaign: str, path: Path) -> str:
    """A path relative to the campaign dir, POSIX-style — the form the stores use."""
    return path.resolve().relative_to(campaign_dir(campaign).resolve()).as_posix()


# ── json ──────────────────────────────────────────────────────────────────────

def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def read_json(path: Path, default=None):
    if not path.is_file():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def write_json_atomic(path: Path, data, indent: int = 2) -> None:
    """Write `data` as JSON to `path` through a temp file in the same directory."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(data, indent=indent, ensure_ascii=False) + "\n"
    fd, tmp = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=str(path.parent))
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(text)
            fh.flush()
            os.fsync(fh.fileno())
        os.replace(tmp, path)
    except BaseException:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise


def stamp_meta(data: dict, campaign: str, written_by: str, **extra) -> dict:
    """Set the shared `_meta` keys on a store, keeping whatever else it holds."""
    meta = data.setdefault("_meta", {})
    meta.setdefault("schema_version", SCHEMA_VERSION)
    meta["campaign"] = campaign
    meta["written_by"] = written_by
    meta["written_at"] = now_iso()
    meta.update(extra)
    return data


def sha256_file(path: Path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


# ── ids and names ─────────────────────────────────────────────────────────────

_TR = str.maketrans({"ç": "c", "ğ": "g", "ı": "i", "ö": "o", "ş": "s", "ü": "u",
                     "Ç": "c", "Ğ": "g", "İ": "i", "Ö": "o", "Ş": "s", "Ü": "u"})


def slug(name: str) -> str:
    """ASCII slug for an id: Turkish letters transliterated, everything else folded."""
    s = name.translate(_TR)
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    s = re.sub(r"[^a-z0-9]+", "_", s.lower()).strip("_")
    return s


def id_type(entity_id: str) -> str | None:
    """The type an id's prefix names, or None when the prefix is not an entity type."""
    head = entity_id.split("_", 1)[0]
    return head if head in ENTITY_TYPES else None


# ── bible prose ───────────────────────────────────────────────────────────────

def parse_front_matter(text: str) -> dict:
    """The `key: value` block at the top of a bible file; `[a, b]` values become lists."""
    m = FRONT.match(text)
    if not m:
        return {}
    out: dict = {}
    for line in m.group(1).splitlines():
        if ":" not in line or line.lstrip().startswith("#"):
            continue
        key, _, value = line.partition(":")
        value = value.split("#", 1)[0].strip() if not value.strip().startswith("[") else value.strip()
        if value.startswith("[") and value.endswith("]"):
            out[key.strip()] = [v.strip() for v in value[1:-1].split(",") if v.strip()]
        elif value in ("null", "~", ""):
            out[key.strip()] = None
        else:
            out[key.strip()] = value
    return out


def front_matter(path: Path) -> dict:
    return parse_front_matter(Path(path).read_text(encoding="utf-8"))


def wiki_links(text: str) -> list[str]:
    """Every distinct [[id]] in `text`, in order of first appearance."""
    seen: list[str] = []
    for ref in WIKI.findall(text):
        if ref not in seen:
            seen.append(ref)
    return seen


# ── overlay ───────────────────────────────────────────────────────────────────

def empty_overlay(campaign: str) -> dict:
    return {
        "_meta": {"schema_version": SCHEMA_VERSION, "campaign": campaign, "written_by": "",
                  "written_at": "", "simulated_to_day": 0, "threat_stage": 1,
                  "doom_day": None, "doom_moved": []},
        "entries": {},
        "pending_scenes": [],
        "price_modifiers": {},
    }


def load_overlay(campaign: str) -> dict:
    data = read_json(design_dir(campaign) / "overlay.json")
    if data is None:
        return empty_overlay(campaign)
    data.setdefault("entries", {})
    data.setdefault("pending_scenes", [])
    data.setdefault("price_modifiers", {})
    return data


def save_overlay(campaign: str, data: dict, written_by: str) -> None:
    stamp_meta(data, campaign, written_by)
    write_json_atomic(design_dir(campaign) / "overlay.json", data)


def overlay_set(overlay: dict, entity_id: str, field: str, value, *, writer: str, day: int,
                birth=None, news: str | None = None, reason: str | None = None) -> dict:
    """Set one overlay field in memory; the caller saves. Validates field and closed values."""
    if field not in OVERLAY_FIELDS:
        raise ValueError(f"{field!r} is not an overlay field (allowed: {', '.join(OVERLAY_FIELDS)})")
    allowed = OVERLAY_FIELDS[field]
    if allowed is not None and value not in allowed:
        raise ValueError(f"{field}={value!r} is not one of {allowed}")
    if writer not in OVERLAY_WRITERS:
        raise ValueError(f"{writer!r} may not write the overlay")
    entry = overlay["entries"].setdefault(entity_id, {})
    previous = entry.get(field)
    record = {
        "value": value,
        "birth": previous["birth"] if previous else birth,
        "writer": writer,
        "day": int(day),
        "news": news,
        "reason": reason,
    }
    entry[field] = record
    return record
