"""Scoring helpers for candidate discrimination."""

from __future__ import annotations

from collections import defaultdict
from typing import Any

from sqlalchemy.orm import Session

from app.curriculum import list_assignments, list_tracks, normalize_track_id
from app.models import Candidate, Role, Score, Submission


def assignment_weight_map() -> dict[str, float]:
    return {a["id"]: float(a.get("weight") or 0) for a in list_assignments()}


def assignment_by_id() -> dict[str, dict]:
    return {a["id"]: a for a in list_assignments()}


def _score_rows_by_assignment(db: Session, candidate_id: int) -> dict[str, list[Score]]:
    scores = db.query(Score).filter(Score.candidate_id == candidate_id).all()
    by_asg: dict[str, list[Score]] = defaultdict(list)
    for s in scores:
        by_asg[s.assignment_id].append(s)
    return by_asg


def _assignment_pct(rows: list[Score]) -> tuple[float, float, float]:
    earned = sum(r.points for r in rows)
    maximum = sum(r.max_points for r in rows) or 1.0
    pct = 100.0 * earned / maximum
    return earned, maximum, pct


def candidate_totals(
    db: Session,
    candidate_id: int,
    *,
    track: str | None = None,
) -> dict:
    """Weighted percent across assignments that have scores.

    Only graded assignments count. Other-track work is allowed and included
    when present. Optional ``track`` limits the total to one discipline.
    """
    by_asg = _score_rows_by_assignment(db, candidate_id)
    weights = assignment_weight_map()
    catalog = assignment_by_id()
    track_norm = normalize_track_id(track) if track else None

    detail = []
    weighted_sum = 0.0
    weight_used = 0.0

    for asg_id, rows in sorted(by_asg.items()):
        meta = catalog.get(asg_id) or {}
        asg_track = normalize_track_id(meta.get("track") or "")
        if track_norm and asg_track != track_norm:
            continue
        earned, maximum, pct = _assignment_pct(rows)
        w = weights.get(asg_id, 0.0)
        detail.append({
            "assignment_id": asg_id,
            "title": meta.get("title") or asg_id,
            "track": asg_track,
            "earned": earned,
            "maximum": maximum,
            "pct": round(pct, 1),
            "weight": w,
        })
        if w > 0:
            weighted_sum += pct * w
            weight_used += w

    overall = round(weighted_sum / weight_used, 1) if weight_used else None
    return {
        "detail": detail,
        "overall_pct": overall,
        "weight_used": weight_used,
        "track": track_norm,
    }


def candidate_track_totals(db: Session, candidate_id: int) -> list[dict]:
    """Per-track weighted averages for a student (only graded work)."""
    rows = []
    for t in list_tracks():
        tid = t["id"]
        tot = candidate_totals(db, candidate_id, track=tid)
        if tot["weight_used"] or tot["detail"]:
            rows.append({
                "track": tid,
                "track_short": t.get("short") or tid.upper(),
                "track_title": t.get("title") or tid,
                "track_color": t.get("color") or tid,
                "overall_pct": tot["overall_pct"],
                "weight_used": tot["weight_used"],
                "graded_count": len(tot["detail"]),
            })
    return rows


def candidate_gradebook(db: Session, candidate_id: int) -> dict[str, Any]:
    """Full gradebook: every catalog assignment, any track, optional scores.

    Students may be scored on any track; ungraded assignments simply do not
    count toward weighted totals.
    """
    by_asg = _score_rows_by_assignment(db, candidate_id)
    subs = {
        s.assignment_id: s
        for s in db.query(Submission).filter(Submission.candidate_id == candidate_id).all()
    }
    tracks = list_tracks()
    track_meta = {t["id"]: t for t in tracks}
    groups: list[dict] = []

    for t in tracks:
        tid = t["id"]
        items = []
        for a in list_assignments(track=tid):
            aid = a["id"]
            rows = by_asg.get(aid) or []
            sub = subs.get(aid)
            if rows:
                earned, maximum, pct = _assignment_pct(rows)
                status = "graded"
            elif sub and sub.status == "submitted":
                earned = maximum = pct = None
                status = "submitted"
            elif sub and (sub.body or "").strip():
                earned = maximum = pct = None
                status = sub.status or "draft"
            else:
                earned = maximum = pct = None
                status = "open"

            items.append({
                "id": aid,
                "title": a.get("title") or aid,
                "weight": float(a.get("weight") or 0),
                "due_session": a.get("due_session") or "",
                "module_id": a.get("module_id") or "",
                "status": status,
                "earned": earned,
                "maximum": maximum,
                "pct": round(pct, 1) if pct is not None else None,
                "submission_id": sub.id if sub else None,
                "has_submission_body": bool(sub and (sub.body or "").strip()),
            })
        track_tot = candidate_totals(db, candidate_id, track=tid)
        groups.append({
            "track": tid,
            "track_short": t.get("short") or tid.upper(),
            "track_title": t.get("title") or tid,
            "track_color": t.get("color") or tid,
            "track_status": t.get("status") or "",
            "overall_pct": track_tot["overall_pct"],
            "weight_used": track_tot["weight_used"],
            "assignments": items,
            "graded_count": sum(1 for i in items if i["status"] == "graded"),
            "submitted_count": sum(1 for i in items if i["status"] == "submitted"),
        })

    overall = candidate_totals(db, candidate_id)
    return {
        "tracks": groups,
        "overall": overall,
        "track_meta": track_meta,
    }


def clear_assignment_scores(db: Session, candidate_id: int, assignment_id: str) -> int:
    """Remove all score rows for one assignment; return count deleted."""
    rows = (
        db.query(Score)
        .filter(
            Score.candidate_id == candidate_id,
            Score.assignment_id == assignment_id,
        )
        .all()
    )
    n = len(rows)
    for r in rows:
        db.delete(r)
    return n


def leaderboard(db: Session, *, include_inactive: bool = False) -> list[dict]:
    q = db.query(Candidate).filter(Candidate.role == Role.student)
    if not include_inactive:
        q = q.filter(Candidate.is_active == True)  # noqa: E712
    students = q.order_by(Candidate.name).all()
    rows = []
    for c in students:
        tot = candidate_totals(db, c.id)
        track_rows = candidate_track_totals(db, c.id)
        primary = normalize_track_id(getattr(c, "primary_track", None) or "se")
        rows.append({
            "id": c.id,
            "name": c.name,
            "email": c.email or "",
            "cohort": c.cohort,
            "primary_track": primary,
            "is_active": bool(c.is_active),
            "overall_pct": tot["overall_pct"],
            "weight_used": tot["weight_used"],
            "recommended": c.recommended,
            "detail": tot["detail"],
            "track_totals": track_rows,
            "graded_count": len(tot["detail"]),
            "submission_count": c.submissions.count(),
            "notes": c.notes or "",
        })
    rows.sort(
        key=lambda r: (
            0 if r["is_active"] else 1,
            -999 if r["overall_pct"] is None else -r["overall_pct"],
            r["name"],
        )
    )
    return rows


def submission_status(db: Session, candidate_id: int, assignment_id: str) -> Submission | None:
    return (
        db.query(Submission)
        .filter(
            Submission.candidate_id == candidate_id,
            Submission.assignment_id == assignment_id,
        )
        .first()
    )
