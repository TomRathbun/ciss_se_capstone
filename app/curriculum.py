"""Load curriculum content from content/ (YAML + Markdown)."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import markdown
import yaml

from app.config import CONTENT_DIR


def _read_yaml(path: Path) -> Any:
    if not path.exists():
        return None
    with path.open(encoding="utf-8") as f:
        return yaml.safe_load(f)


def _md_to_html(text: str) -> str:
    return markdown.markdown(
        text or "",
        extensions=["extra", "sane_lists", "tables", "fenced_code", "toc"],
    )


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
