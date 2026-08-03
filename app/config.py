"""Application configuration."""

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
CONTENT_DIR = BASE_DIR / "content"
DATABASE_URL = f"sqlite:///{BASE_DIR / 'ciss_se_course.db'}"

SECRET_KEY = os.environ.get("CISS_SE_SECRET", "ciss-se-capstone-dev-key-change-me")
SESSION_COOKIE = "ciss_se_session"
SESSION_MAX_AGE = 12 * 60 * 60  # 12 hours

APP_NAME = "CISS SE Capstone"
APP_TAGLINE = "Systems Engineering · Military Operations · Candidate Assessment"
APP_VERSION = "0.1.0"

# Link to the living ETAS case study (time tracker SE page)
CASE_STUDY_URL = os.environ.get(
    "CISS_CASE_STUDY_URL",
    "http://localhost:8888/systems-engineering",
)
CASE_STUDY_APP_URL = os.environ.get(
    "CISS_CASE_STUDY_APP_URL",
    "http://localhost:8888/login",
)

# Default instructor PIN (change in production)
DEFAULT_INSTRUCTOR_PIN = os.environ.get("CISS_INSTRUCTOR_PIN", "4242")
DEFAULT_STUDENT_PIN = os.environ.get("CISS_STUDENT_PIN", "1234")
