"""Scoring helpers for candidate discrimination."""

from __future__ import annotations

from collections import defaultdict

from sqlalchemy.orm import Session

from app.curriculum import list_assignments
from app.models import Candidate, Role, Score, Submission


def assignment_weight_map() -> dict[str, float]:
    return {a["id"]: float(a.get("weight") or 0) for a in list_assignments()}


def candidate_totals(db: Session, candidate_id: int) -> dict:
    """Compute weighted percent across assignments that have scores."""
    scores = db.query(Score).filter(Score.candidate_id == candidate_id).all()
    by_asg: dict[str, list[Score]] = defaultdict(list)
    for s in scores:
        by_asg[s.assignment_id].append(s)

    weights = assignment_weight_map()
    detail = []
    weighted_sum = 0.0
    weight_used = 0.0

    for asg_id, rows in by_asg.items():
        earned = sum(r.points for r in rows)
        maximum = sum(r.max_points for r in rows) or 1.0
        pct = 100.0 * earned / maximum
        w = weights.get(asg_id, 0.0)
        detail.append({
            "assignment_id": asg_id,
            "earned": earned,
            "maximum": maximum,
            "pct": round(pct, 1),
            "weight": w,
        })
        if w > 0:
            weighted_sum += pct * w
            weight_used += w

    overall = round(weighted_sum / weight_used, 1) if weight_used else None
    return {"detail": detail, "overall_pct": overall, "weight_used": weight_used}


def leaderboard(db: Session) -> list[dict]:
    students = (
        db.query(Candidate)
        .filter(Candidate.role == Role.student, Candidate.is_active == True)  # noqa: E712
        .order_by(Candidate.name)
        .all()
    )
    rows = []
    for c in students:
        tot = candidate_totals(db, c.id)
        rows.append({
            "id": c.id,
            "name": c.name,
            "cohort": c.cohort,
            "overall_pct": tot["overall_pct"],
            "recommended": c.recommended,
            "detail": tot["detail"],
            "submission_count": c.submissions.count(),
        })
    rows.sort(key=lambda r: (-999 if r["overall_pct"] is None else -r["overall_pct"], r["name"]))
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
