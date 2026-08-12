"""ORM models — candidates, scores, submissions (selection support)."""

import enum
from datetime import datetime

from sqlalchemy import (
    Boolean, Column, DateTime, Enum, Float, ForeignKey, Integer, String, Text, UniqueConstraint,
)
from sqlalchemy.orm import relationship

from app.database import Base


class Role(str, enum.Enum):
    student = "student"
    instructor = "instructor"


class Candidate(Base):
    """Intern / candidate in the cohort (selection pool)."""

    __tablename__ = "candidates"

    id = Column(Integer, primary_key=True)
    name = Column(String(120), nullable=False)
    email = Column(String(200), default="")
    pin_hash = Column(String(255), nullable=False)
    role = Column(Enum(Role), default=Role.student, nullable=False)
    cohort = Column(String(80), default="2026-UAE")
    # Home discipline track (se/sw/net/admin/mil). Does not block other-track work.
    primary_track = Column(String(40), default="se")
    is_active = Column(Boolean, default=True)
    # Selection dimensions (rolling totals or notes)
    notes = Column(Text, default="")
    recommended = Column(Boolean, default=False)  # instructor flag for main project
    created_at = Column(DateTime, default=datetime.utcnow)

    scores = relationship("Score", back_populates="candidate", lazy="dynamic")
    submissions = relationship("Submission", back_populates="candidate", lazy="dynamic")


class Score(Base):
    """Graded score on an assignment dimension — used to rank candidates."""

    __tablename__ = "scores"
    __table_args__ = (
        UniqueConstraint("candidate_id", "assignment_id", "dimension", name="uq_score_dim"),
    )

    id = Column(Integer, primary_key=True)
    candidate_id = Column(Integer, ForeignKey("candidates.id"), nullable=False)
    assignment_id = Column(String(80), nullable=False, index=True)
    dimension = Column(String(80), nullable=False)  # e.g. clarity, testability, traceability
    points = Column(Float, nullable=False, default=0.0)
    max_points = Column(Float, nullable=False, default=10.0)
    feedback = Column(Text, default="")
    graded_at = Column(DateTime, default=datetime.utcnow)
    graded_by = Column(String(120), default="instructor")

    candidate = relationship("Candidate", back_populates="scores")


class Submission(Base):
    """Student work product (markdown/text) for an assignment."""

    __tablename__ = "submissions"
    __table_args__ = (
        UniqueConstraint("candidate_id", "assignment_id", name="uq_submission"),
    )

    id = Column(Integer, primary_key=True)
    candidate_id = Column(Integer, ForeignKey("candidates.id"), nullable=False)
    assignment_id = Column(String(80), nullable=False, index=True)
    body = Column(Text, default="")
    status = Column(String(40), default="draft")  # draft | submitted | graded
    submitted_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    candidate = relationship("Candidate", back_populates="submissions")


class Progress(Base):
    """Module completion tracking."""

    __tablename__ = "progress"
    __table_args__ = (
        UniqueConstraint("candidate_id", "module_id", name="uq_progress"),
    )

    id = Column(Integer, primary_key=True)
    candidate_id = Column(Integer, ForeignKey("candidates.id"), nullable=False)
    module_id = Column(String(80), nullable=False)
    completed = Column(Boolean, default=False)
    completed_at = Column(DateTime, nullable=True)
