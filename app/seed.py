"""Seed instructor + demo students."""

from app.auth import hash_pin
from app.config import DEFAULT_INSTRUCTOR_PIN, DEFAULT_STUDENT_PIN
from app.database import SessionLocal
from app.models import Candidate, Role


def seed_users():
    db = SessionLocal()
    try:
        if db.query(Candidate).count() > 0:
            return
        db.add(Candidate(
            name="Course Instructor",
            email="instructor@ciss.local",
            pin_hash=hash_pin(DEFAULT_INSTRUCTOR_PIN),
            role=Role.instructor,
            cohort="staff",
        ))
        demo_tracks = ["se", "sw", "admin", "mil"]
        for i, name in enumerate([
            "Intern Alpha",
            "Intern Bravo",
            "Intern Charlie",
            "Intern Delta",
        ], start=1):
            db.add(Candidate(
                name=name,
                email=f"intern{i}@ciss.local",
                pin_hash=hash_pin(DEFAULT_STUDENT_PIN),
                role=Role.student,
                cohort="2026-UAE",
                primary_track=demo_tracks[(i - 1) % len(demo_tracks)],
            ))
        db.commit()
        print("Seeded instructor + 4 demo interns")
    finally:
        db.close()
