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


def load_catalog() -> dict:
    data = _read_yaml(CONTENT_DIR / "catalog.yaml") or {}
    return data


def list_modules() -> list[dict]:
    catalog = load_catalog()
    modules = catalog.get("modules") or []
    return sorted(modules, key=lambda m: m.get("order", 99))


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


def module_neighbors(module_id: str) -> tuple[dict | None, dict | None, int, int]:
    """Return (prev, next, index_1based, total) in catalog order."""
    modules = list_modules()
    total = len(modules)
    for i, m in enumerate(modules):
        if m.get("id") == module_id:
            prev_m = modules[i - 1] if i > 0 else None
            next_m = modules[i + 1] if i + 1 < total else None
            return prev_m, next_m, i + 1, total
    return None, None, 0, total


def list_assignments() -> list[dict]:
    catalog = load_catalog()
    items = catalog.get("assignments") or []
    return sorted(items, key=lambda a: a.get("order", 99))


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


def load_schedule() -> dict:
    return _read_yaml(CONTENT_DIR / "schedule" / "cohort.yaml") or {"sessions": []}


def load_glossary() -> list[dict]:
    data = _read_yaml(CONTENT_DIR / "glossary" / "terms.yaml") or {}
    terms = data.get("terms") or []
    return sorted(terms, key=lambda t: t.get("term", "").lower())


def load_selection_criteria() -> dict:
    return _read_yaml(CONTENT_DIR / "selection_criteria.yaml") or {}
