"""Load curriculum content from content/ (YAML + Markdown)."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

import markdown
import yaml

from app.config import CONTENT_DIR

# Editable content roots (relative to CONTENT_DIR)
EDITABLE_KINDS = {
    "modules": CONTENT_DIR / "modules",
    "assignments": CONTENT_DIR / "assignments",
}

# Frozen pre-Masdar lessons. Live files in EDITABLE_KINDS win on id collision.
ADDITIONAL_KINDS = {
    "modules": CONTENT_DIR / "additional" / "modules",
    "assignments": CONTENT_DIR / "additional" / "assignments",
}

PHASE_ORDER = {
    "foundation": 1,
    "kickoff": 2,
    "depth": 3,
    "capstone": 4,
    "additional": 5,
}

PHASE_LABELS = {
    "foundation": "Foundation · weeks 1–4",
    "kickoff": "Capstone kickoff · week 5",
    "depth": "Depth · week 6+",
    "capstone": "PRSAS capstone",
    "additional": "Additional / archived lessons",
}


def _read_yaml(path: Path) -> Any:
    if not path.exists():
        return None
    with path.open(encoding="utf-8") as f:
        return yaml.safe_load(f)


# catalog.yaml (+ additional/catalog.yaml) is parsed on almost every page.
_catalog_cache: dict | None = None
_catalog_mtime: tuple[float, float] | None = None


def _unescape_code(code: str) -> str:
    return (
        code.replace("&lt;", "<")
        .replace("&gt;", ">")
        .replace("&amp;", "&")
        .replace("&quot;", '"')
        .replace("&#39;", "'")
    )


def _promote_diagram_and_math_blocks(html: str) -> str:
    """Promote fenced mermaid/plantuml/math for client or PlantUML server render."""
    from app.config import PLANTUML_SERVER
    from app.services.plantuml_encode import plantuml_svg_url

    def mermaid_repl(match: re.Match) -> str:
        code = _unescape_code(match.group(1))
        return f'<pre class="mermaid">{code}</pre>'

    def plantuml_repl(match: re.Match) -> str:
        code = _unescape_code(match.group(1)).strip()
        if not code.startswith("@start"):
            code = "@startuml\n" + code + "\n@enduml"
        try:
            url = plantuml_svg_url(code, PLANTUML_SERVER)
        except Exception:
            return f'<pre class="plantuml-source">{code}</pre>'
        return (
            f'<div class="plantuml-render my-4">'
            f'<img src="{url}" alt="PlantUML diagram" loading="lazy" class="max-w-full mx-auto bg-white rounded-lg p-2" />'
            f"</div>"
        )

    def math_block_repl(match: re.Match) -> str:
        code = _unescape_code(match.group(1)).strip()
        return f'<div class="math-display">\\[{code}\\]</div>'

    html = re.sub(
        r'<pre><code class="language-mermaid">(.*?)</code></pre>',
        mermaid_repl,
        html,
        flags=re.DOTALL | re.IGNORECASE,
    )
    html = re.sub(
        r'<pre><code class="language-plantuml">(.*?)</code></pre>',
        plantuml_repl,
        html,
        flags=re.DOTALL | re.IGNORECASE,
    )
    html = re.sub(
        r'<pre><code class="language-(?:math|latex|katex)">(.*?)</code></pre>',
        math_block_repl,
        html,
        flags=re.DOTALL | re.IGNORECASE,
    )
    return html


def _md_to_html(text: str) -> str:
    html = markdown.markdown(
        text or "",
        extensions=["extra", "sane_lists", "tables", "fenced_code", "toc"],
    )
    return _promote_diagram_and_math_blocks(html)


def list_editable_files() -> list[dict]:
    """List markdown files the instructor may edit in-app."""
    items: list[dict] = []
    seen: set[tuple[str, str]] = set()
    scans = (
        (EDITABLE_KINDS, False),
        (ADDITIONAL_KINDS, True),
    )
    for roots, archived in scans:
        for kind, folder in roots.items():
            if not folder.is_dir():
                continue
            for path in sorted(folder.glob("*.md")):
                key = (kind, path.stem)
                if key in seen:
                    continue
                seen.add(key)
                rel = (
                    f"additional/{kind}/{path.name}"
                    if archived
                    else f"{kind}/{path.name}"
                )
                items.append({
                    "kind": kind,
                    "id": path.stem,
                    "path": rel,
                    "title": path.stem.replace("-", " ").replace("_", " ").title(),
                    "bytes": path.stat().st_size,
                    "archived": archived,
                })
    # Prefer catalog titles when available
    title_map = {m["id"]: m["title"] for m in list_modules()}
    for a in list_assignments():
        title_map[a["id"]] = a["title"]
    for it in items:
        if it["id"] in title_map:
            it["title"] = title_map[it["id"]]
    return items


def resolve_editable_path(kind: str, content_id: str) -> Path | None:
    """Safe path under content/modules|assignments (or additional copies)."""
    if kind not in EDITABLE_KINDS:
        return None
    if not re.fullmatch(r"[a-zA-Z0-9][a-zA-Z0-9_-]{0,80}", content_id or ""):
        return None
    primary = EDITABLE_KINDS[kind] / f"{content_id}.md"
    extra = ADDITIONAL_KINDS[kind] / f"{content_id}.md"
    path = primary if primary.is_file() else extra if extra.is_file() else primary
    try:
        if path.is_file():
            path.resolve().relative_to(path.parent.resolve())
        else:
            primary.resolve().relative_to(EDITABLE_KINDS[kind].resolve())
    except ValueError:
        return None
    return path


def read_editable(kind: str, content_id: str) -> str | None:
    path = resolve_editable_path(kind, content_id)
    if not path or not path.is_file():
        return None
    return path.read_text(encoding="utf-8")


def write_editable(kind: str, content_id: str, body: str) -> bool:
    path = resolve_editable_path(kind, content_id)
    if not path:
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    # Normalize newlines
    text = (body or "").replace("\r\n", "\n")
    if not text.endswith("\n"):
        text += "\n"
    path.write_text(text, encoding="utf-8")
    return True


# Legacy catalog used track: ops for military modules.
TRACK_ALIASES = {"ops": "mil"}

# Fallback if catalog has no tracks block.
_DEFAULT_TRACKS: list[dict] = [
    {"id": "se", "order": 1, "short": "SE", "title": "Systems Engineering", "summary": "", "color": "se", "status": "active"},
    {"id": "sw", "order": 2, "short": "SW", "title": "Software Development", "summary": "", "color": "sw", "status": "scaffolding"},
    {"id": "net", "order": 3, "short": "NET", "title": "Networking", "summary": "", "color": "net", "status": "active"},
    {"id": "admin", "order": 4, "short": "ADMIN", "title": "System Administration & Integration", "summary": "", "color": "admin", "status": "scaffolding"},
    {"id": "mil", "order": 5, "short": "MIL", "title": "Military Operations", "summary": "", "color": "mil", "status": "active"},
]


def normalize_phase(raw: str | None, *, default: str = "foundation") -> str:
    p = (raw or default).strip().lower()
    return p if p in PHASE_ORDER else default


def _merge_by_id(primary: list | None, extra: list | None, *, extra_phase: str | None = None) -> list[dict]:
    """Primary catalog rows win on id. Extra rows can be stamped with a phase."""
    by_id: dict[str, dict] = {}
    for row in extra or []:
        if not isinstance(row, dict) or not row.get("id"):
            continue
        item = dict(row)
        if extra_phase:
            item["phase"] = extra_phase
        by_id[item["id"]] = item
    for row in primary or []:
        if not isinstance(row, dict) or not row.get("id"):
            continue
        by_id[row["id"]] = dict(row)
    return list(by_id.values())


def _file_mtime(path: Path) -> float:
    try:
        return path.stat().st_mtime
    except OSError:
        return 0.0


def load_catalog() -> dict:
    """Load live catalog.yaml merged with archived additional/catalog.yaml."""
    global _catalog_cache, _catalog_mtime
    primary_path = CONTENT_DIR / "catalog.yaml"
    extra_path = CONTENT_DIR / "additional" / "catalog.yaml"
    stamp = (_file_mtime(primary_path), _file_mtime(extra_path))
    if _catalog_cache is not None and _catalog_mtime == stamp:
        return _catalog_cache
    primary = _read_yaml(primary_path) or {}
    extra = _read_yaml(extra_path) or {}
    data = dict(primary)
    data["modules"] = _merge_by_id(
        primary.get("modules"), extra.get("modules"), extra_phase="additional"
    )
    data["assignments"] = _merge_by_id(
        primary.get("assignments"), extra.get("assignments"), extra_phase="additional"
    )
    _catalog_cache = data
    _catalog_mtime = stamp
    return data


def normalize_track_id(track: str | None) -> str:
    """Map legacy aliases (e.g. ops → mil) to canonical track ids."""
    t = (track or "se").strip().lower()
    return TRACK_ALIASES.get(t, t)


def _raw_tracks() -> list[dict]:
    """Tracks from catalog (or defaults), no module counts — safe for enrichment."""
    catalog = load_catalog()
    tracks = catalog.get("tracks") or list(_DEFAULT_TRACKS)
    out: list[dict] = []
    for t in tracks:
        row = dict(t)
        row["id"] = normalize_track_id(row.get("id"))
        row["color"] = row.get("color") or row["id"]
        row["short"] = row.get("short") or row["id"].upper()
        out.append(row)
    return sorted(out, key=lambda t: t.get("order", 99))


def _track_map() -> dict[str, dict]:
    return {t["id"]: t for t in _raw_tracks()}


def list_tracks() -> list[dict]:
    """Tracks in catalog order, enriched with module/assignment counts."""
    catalog = load_catalog()
    raw_modules = catalog.get("modules") or []
    raw_assignments = catalog.get("assignments") or []
    out: list[dict] = []
    for t in _raw_tracks():
        tid = t["id"]
        row = dict(t)
        def _is_additional(row: dict) -> bool:
            return normalize_phase(row.get("phase")) == "additional"

        row["module_count"] = sum(
            1
            for m in raw_modules
            if normalize_track_id(m.get("track")) == tid and not _is_additional(m)
        )
        row["additional_count"] = sum(
            1
            for m in raw_modules
            if normalize_track_id(m.get("track")) == tid and _is_additional(m)
        )
        row["assignment_count"] = sum(
            1
            for a in raw_assignments
            if normalize_track_id(
                a.get("track")
                or next(
                    (
                        m.get("track")
                        for m in raw_modules
                        if m.get("id") == a.get("module_id")
                    ),
                    "se",
                )
            )
            == tid
            and not _is_additional(a)
        )
        out.append(row)
    return out


def get_track(track_id: str) -> dict | None:
    tid = normalize_track_id(track_id)
    return _track_map().get(tid)


def _enrich_module(m: dict, track_map: dict[str, dict] | None = None) -> dict:
    row = dict(m)
    row["track"] = normalize_track_id(row.get("track"))
    row["phase"] = normalize_phase(row.get("phase"))
    row["phase_label"] = PHASE_LABELS.get(row["phase"], row["phase"])
    track_meta = (track_map if track_map is not None else _track_map()).get(row["track"]) or {}
    row["track_title"] = track_meta.get("title") or row["track"]
    row["track_short"] = track_meta.get("short") or row["track"].upper()
    row["track_color"] = track_meta.get("color") or row["track"]
    row["track_status"] = track_meta.get("status") or "active"
    return row


def _module_sort_key(m: dict) -> tuple:
    return (
        PHASE_ORDER.get(m.get("phase"), 99),
        m.get("order", 99),
        m.get("id") or "",
    )


def list_modules(track: str | None = None, *, phase: str | None = None) -> list[dict]:
    catalog = load_catalog()
    track_map = _track_map()
    modules = [_enrich_module(m, track_map) for m in (catalog.get("modules") or [])]
    modules = sorted(modules, key=_module_sort_key)
    if track:
        tid = normalize_track_id(track)
        modules = [m for m in modules if m.get("track") == tid]
    if phase:
        want = normalize_phase(phase)
        modules = [m for m in modules if m.get("phase") == want]
    return modules


def group_by_phase(items: list[dict]) -> list[dict]:
    """Group already-enriched modules or assignments by phase, empty phases omitted."""
    buckets: dict[str, list[dict]] = {p: [] for p in PHASE_ORDER}
    for item in items:
        buckets.setdefault(item.get("phase") or "foundation", []).append(item)
    out: list[dict] = []
    for p, rank in sorted(PHASE_ORDER.items(), key=lambda kv: kv[1]):
        group = buckets.get(p) or []
        if not group:
            continue
        out.append({
            "id": p,
            "title": PHASE_LABELS.get(p, p),
            "entries": group,
        })
    return out


def modules_by_track() -> list[dict]:
    """Tracks with nested modules list (for home / modules index)."""
    all_mods = list_modules()
    result: list[dict] = []
    for t in list_tracks():
        row = dict(t)
        live = [m for m in all_mods if m.get("track") == t["id"] and m.get("phase") != "additional"]
        archived = [m for m in all_mods if m.get("track") == t["id"] and m.get("phase") == "additional"]
        row["modules"] = live
        row["additional_modules"] = archived
        row["phases"] = group_by_phase(
            [m for m in all_mods if m.get("track") == t["id"]]
        )
        result.append(row)
    return result


def _markdown_path(kind: str, content_id: str) -> Path:
    primary = CONTENT_DIR / kind / f"{content_id}.md"
    if primary.is_file():
        return primary
    return CONTENT_DIR / "additional" / kind / f"{content_id}.md"


def get_module(module_id: str) -> dict | None:
    for m in list_modules():
        if m.get("id") == module_id:
            body_path = _markdown_path("modules", module_id)
            body_md = body_path.read_text(encoding="utf-8") if body_path.is_file() else ""
            m = dict(m)
            m["body_html"] = _md_to_html(body_md)
            m["body_md"] = body_md
            return m
    return None


def modules_for_export(
    ids: list[str] | None = None,
    track: str | None = None,
) -> list[dict]:
    """Full module bodies in catalog order. Empty ids = all (optionally one track)."""
    catalog_order = list_modules(track=track) if track else list_modules()
    if ids:
        wanted = {i for i in ids if i}
        catalog_order = [m for m in catalog_order if m.get("id") in wanted]
    out: list[dict] = []
    for meta in catalog_order:
        full = get_module(meta["id"])
        if full:
            out.append(full)
    return out


def module_neighbors(
    module_id: str, *, within_track: bool = True
) -> tuple[dict | None, dict | None, int, int]:
    """Return (prev, next, index_1based, total).

    By default navigates within the same track and phase so foundation
    does not jump into archived additional lessons.
    """
    modules = list_modules()
    current = next((m for m in modules if m.get("id") == module_id), None)
    if not current:
        return None, None, 0, 0
    if within_track:
        modules = [
            m
            for m in modules
            if m.get("track") == current.get("track")
            and m.get("phase") == current.get("phase")
        ]
    total = len(modules)
    for i, m in enumerate(modules):
        if m.get("id") == module_id:
            prev_m = modules[i - 1] if i > 0 else None
            next_m = modules[i + 1] if i + 1 < total else None
            return prev_m, next_m, i + 1, total
    return None, None, 0, total


def _enrich_assignment(
    a: dict,
    *,
    module_track_by_id: dict[str, str] | None = None,
    track_map: dict[str, dict] | None = None,
) -> dict:
    row = dict(a)
    track = row.get("track")
    if not track and row.get("module_id"):
        if module_track_by_id is None:
            module_track_by_id = {
                m.get("id"): m.get("track") for m in list_modules()
            }
        track = module_track_by_id.get(row["module_id"])
    row["track"] = normalize_track_id(track)
    row["phase"] = normalize_phase(row.get("phase"))
    row["phase_label"] = PHASE_LABELS.get(row["phase"], row["phase"])
    track_meta = (track_map if track_map is not None else _track_map()).get(row["track"]) or {}
    row["track_title"] = track_meta.get("title") or row["track"]
    row["track_short"] = track_meta.get("short") or row["track"].upper()
    row["track_color"] = track_meta.get("color") or row["track"]
    return row


def list_assignments(track: str | None = None) -> list[dict]:
    catalog = load_catalog()
    track_map = _track_map()
    module_track_by_id = {
        m.get("id"): normalize_track_id(m.get("track"))
        for m in (catalog.get("modules") or [])
    }
    items = [
        _enrich_assignment(
            a, module_track_by_id=module_track_by_id, track_map=track_map
        )
        for a in (catalog.get("assignments") or [])
    ]
    items = sorted(
        items,
        key=lambda a: (
            PHASE_ORDER.get(a.get("phase"), 99),
            a.get("order", 99),
            a.get("id") or "",
        ),
    )
    if track:
        tid = normalize_track_id(track)
        items = [a for a in items if a.get("track") == tid]
    return items


def assignments_by_track() -> list[dict]:
    all_asg = list_assignments()
    result: list[dict] = []
    for t in list_tracks():
        row = dict(t)
        live = [a for a in all_asg if a.get("track") == t["id"] and a.get("phase") != "additional"]
        row["assignments"] = live
        row["additional_assignments"] = [
            a for a in all_asg if a.get("track") == t["id"] and a.get("phase") == "additional"
        ]
        row["phases"] = group_by_phase(
            [a for a in all_asg if a.get("track") == t["id"]]
        )
        result.append(row)
    return result


def get_assignment(assignment_id: str) -> dict | None:
    for a in list_assignments():
        if a.get("id") == assignment_id:
            body_path = _markdown_path("assignments", assignment_id)
            body_md = body_path.read_text(encoding="utf-8") if body_path.is_file() else ""
            a = dict(a)
            a["body_html"] = _md_to_html(body_md)
            a["rubric"] = a.get("rubric") or []
            return a
    return None


def assignments_for_module(module_id: str) -> list[dict]:
    """Catalog assignments attached to a module, in catalog order."""
    return [a for a in list_assignments() if a.get("module_id") == module_id]


def load_schedule() -> dict:
    """Load cohort.yaml and resolve module/assignment ids to titles + tracks.

    New schema uses `lanes` keyed by track id. Old flat `modules:` lists still
    work — they become a single `se` lane so an un-migrated file does not 500.
    """
    raw = _read_yaml(CONTENT_DIR / "schedule" / "cohort.yaml") or {"sessions": []}
    mod_by_id = {m["id"]: m for m in list_modules()}
    asg_by_id = {a["id"]: a for a in list_assignments()}
    track_map = _track_map()

    def _resolve_mod(mid: str) -> dict:
        m = mod_by_id.get(mid) or {}
        tid = normalize_track_id(m.get("track") or "")
        meta = track_map.get(tid) or {}
        return {
            "id": mid,
            "title": m.get("title") or mid,
            "track": tid or "se",
            "track_short": meta.get("short") or (tid or "SE").upper(),
            "track_color": meta.get("color") or tid or "se",
        }

    def _resolve_asg(aid: str) -> dict:
        a = asg_by_id.get(aid) or {}
        tid = normalize_track_id(a.get("track") or "")
        meta = track_map.get(tid) or {}
        return {
            "id": aid,
            "title": a.get("title") or aid,
            "track": tid or "se",
            "track_short": meta.get("short") or (tid or "SE").upper(),
            "track_color": meta.get("color") or tid or "se",
        }

    def _lane(raw_lane: dict, track_id: str) -> dict:
        meta = track_map.get(track_id) or {}
        return {
            "track": track_id,
            "track_short": meta.get("short") or track_id.upper(),
            "track_color": meta.get("color") or track_id,
            "track_title": meta.get("title") or track_id,
            "title": raw_lane.get("title") or "",
            "modules": [_resolve_mod(x) for x in (raw_lane.get("modules") or [])],
            "assignment_assigned": [
                _resolve_asg(x) for x in (raw_lane.get("assignment_assigned") or [])
            ],
            "assignment_due": [
                _resolve_asg(x) for x in (raw_lane.get("assignment_due") or [])
            ],
        }

    sessions: list[dict] = []
    for s in raw.get("sessions") or []:
        row = dict(s)
        audience = row.get("audience") or "track"
        row["audience"] = audience
        row["common"] = audience == "all" or bool(row.get("common"))
        lanes_raw = row.get("lanes")
        if not lanes_raw:
            mods = row.get("modules") or []
            track_id = "se"
            if mods:
                m0 = mod_by_id.get(mods[0]) or {}
                track_id = normalize_track_id(m0.get("track") or "") or "se"
            lanes_raw = {
                track_id: {
                    "modules": mods,
                    "assignment_assigned": row.get("assignment_assigned") or [],
                    "assignment_due": row.get("assignment_due") or [],
                }
            }
        row["lane_list"] = [_lane(v, k) for k, v in lanes_raw.items()]
        sessions.append(row)

    weeks: list[dict] = []
    by_week: dict[int, dict] = {}
    for s in sessions:
        w = int(s.get("week") or 0)
        bucket = by_week.get(w)
        if bucket is None:
            if w <= 4:
                phase = "foundation"
            elif w == 5:
                phase = "kickoff"
            else:
                phase = "depth"
            bucket = {
                "week": w,
                "common": False,
                "phase": phase,
                "sessions": [],
            }
            by_week[w] = bucket
            weeks.append(bucket)
        bucket["sessions"].append(s)
        if s.get("common") or w <= 5:
            bucket["common"] = True

    out = dict(raw)
    out["sessions"] = sessions
    out["weeks"] = weeks
    return out


def filter_schedule(schedule: dict, track_id: str | None) -> dict:
    """Keep one intern's lane plus military (common to every track).

    `audience: all` sessions (military weeks, PRSAS kickoff/demo) stay in full
    so a filtered view still shows the room everyone sits in together.
    """
    if not track_id:
        return schedule
    weeks: list[dict] = []
    for w in schedule.get("weeks") or []:
        sessions: list[dict] = []
        for s in w.get("sessions") or []:
            lanes = s.get("lane_list") or []
            if s.get("common"):
                vis = list(lanes)
            else:
                vis = [
                    lane
                    for lane in lanes
                    if lane.get("track") in {track_id, "mil"}
                ]
            if not vis:
                continue
            row = dict(s)
            row["lane_list"] = vis
            sessions.append(row)
        if not sessions:
            continue
        bucket = dict(w)
        bucket["sessions"] = sessions
        weeks.append(bucket)
    out = dict(schedule)
    out["weeks"] = weeks
    return out


def load_glossary() -> list[dict]:
    data = _read_yaml(CONTENT_DIR / "glossary" / "terms.yaml") or {}
    terms = data.get("terms") or []
    return sorted(terms, key=lambda t: t.get("term", "").lower())


def load_selection_criteria() -> dict:
    return _read_yaml(CONTENT_DIR / "selection_criteria.yaml") or {}
