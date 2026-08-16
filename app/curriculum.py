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


def _read_yaml(path: Path) -> Any:
    if not path.exists():
        return None
    with path.open(encoding="utf-8") as f:
        return yaml.safe_load(f)


# catalog.yaml is parsed on almost every page. Re-reading it once per module /
# assignment (via _track_map) froze the single worker after the catalog grew.
_catalog_cache: dict | None = None
_catalog_mtime: float | None = None


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
    for kind, folder in EDITABLE_KINDS.items():
        if not folder.is_dir():
            continue
        for path in sorted(folder.glob("*.md")):
            items.append({
                "kind": kind,
                "id": path.stem,
                "path": f"{kind}/{path.name}",
                "title": path.stem.replace("-", " ").replace("_", " ").title(),
                "bytes": path.stat().st_size,
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
    """Safe path under content/modules|assignments only."""
    if kind not in EDITABLE_KINDS:
        return None
    if not re.fullmatch(r"[a-zA-Z0-9][a-zA-Z0-9_-]{0,80}", content_id or ""):
        return None
    path = EDITABLE_KINDS[kind] / f"{content_id}.md"
    try:
        path.resolve().relative_to(EDITABLE_KINDS[kind].resolve())
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


def load_catalog() -> dict:
    """Load catalog.yaml, reusing the parse until the file's mtime changes."""
    global _catalog_cache, _catalog_mtime
    path = CONTENT_DIR / "catalog.yaml"
    try:
        mtime = path.stat().st_mtime
    except OSError:
        return {}
    if _catalog_cache is not None and _catalog_mtime == mtime:
        return _catalog_cache
    data = _read_yaml(path) or {}
    _catalog_cache = data
    _catalog_mtime = mtime
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
        row["module_count"] = sum(
            1 for m in raw_modules if normalize_track_id(m.get("track")) == tid
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
        )
        out.append(row)
    return out


def get_track(track_id: str) -> dict | None:
    tid = normalize_track_id(track_id)
    return _track_map().get(tid)


def _enrich_module(m: dict, track_map: dict[str, dict] | None = None) -> dict:
    row = dict(m)
    row["track"] = normalize_track_id(row.get("track"))
    track_meta = (track_map if track_map is not None else _track_map()).get(row["track"]) or {}
    row["track_title"] = track_meta.get("title") or row["track"]
    row["track_short"] = track_meta.get("short") or row["track"].upper()
    row["track_color"] = track_meta.get("color") or row["track"]
    row["track_status"] = track_meta.get("status") or "active"
    return row


def list_modules(track: str | None = None) -> list[dict]:
    catalog = load_catalog()
    track_map = _track_map()
    modules = [_enrich_module(m, track_map) for m in (catalog.get("modules") or [])]
    modules = sorted(modules, key=lambda m: m.get("order", 99))
    if track:
        tid = normalize_track_id(track)
        modules = [m for m in modules if m.get("track") == tid]
    return modules


def modules_by_track() -> list[dict]:
    """Tracks with nested modules list (for home / modules index)."""
    all_mods = list_modules()
    result: list[dict] = []
    for t in list_tracks():
        row = dict(t)
        row["modules"] = [m for m in all_mods if m.get("track") == t["id"]]
        result.append(row)
    return result


def get_module(module_id: str) -> dict | None:
    for m in list_modules():
        if m.get("id") == module_id:
            body_path = CONTENT_DIR / "modules" / f"{module_id}.md"
            body_md = body_path.read_text(encoding="utf-8") if body_path.exists() else ""
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

    By default navigates within the same track so multi-track catalogs
    do not jump from SE into military mid-sequence.
    """
    modules = list_modules()
    current = next((m for m in modules if m.get("id") == module_id), None)
    if not current:
        return None, None, 0, 0
    if within_track:
        modules = [m for m in modules if m.get("track") == current.get("track")]
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
    items = sorted(items, key=lambda a: a.get("order", 99))
    if track:
        tid = normalize_track_id(track)
        items = [a for a in items if a.get("track") == tid]
    return items


def assignments_by_track() -> list[dict]:
    all_asg = list_assignments()
    result: list[dict] = []
    for t in list_tracks():
        row = dict(t)
        row["assignments"] = [a for a in all_asg if a.get("track") == t["id"]]
        result.append(row)
    return result


def get_assignment(assignment_id: str) -> dict | None:
    for a in list_assignments():
        if a.get("id") == assignment_id:
            body_path = CONTENT_DIR / "assignments" / f"{assignment_id}.md"
            body_md = body_path.read_text(encoding="utf-8") if body_path.exists() else ""
            a = dict(a)
            a["body_html"] = _md_to_html(body_md)
            a["rubric"] = a.get("rubric") or []
            return a
    return None


def assignments_for_module(module_id: str) -> list[dict]:
    """Catalog assignments attached to a module, in catalog order."""
    return [a for a in list_assignments() if a.get("module_id") == module_id]


def load_schedule() -> dict:
    return _read_yaml(CONTENT_DIR / "schedule" / "cohort.yaml") or {"sessions": []}


def load_glossary() -> list[dict]:
    data = _read_yaml(CONTENT_DIR / "glossary" / "terms.yaml") or {}
    terms = data.get("terms") or []
    return sorted(terms, key=lambda t: t.get("term", "").lower())


def load_selection_criteria() -> dict:
    return _read_yaml(CONTENT_DIR / "selection_criteria.yaml") or {}
