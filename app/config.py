"""Application configuration."""

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
CONTENT_DIR = BASE_DIR / "content"
DATABASE_URL = f"sqlite:///{BASE_DIR / 'ciss_se_course.db'}"

SECRET_KEY = os.environ.get("CISS_SE_SECRET", "ciss-se-capstone-dev-key-change-me")
SESSION_COOKIE = "ciss_se_session"
SESSION_MAX_AGE = 12 * 60 * 60  # 12 hours

APP_NAME = "CISS Capstone"
APP_TAGLINE = "SE · Software · Networking · SysAdmin · Military · Candidate Assessment"
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

# Uploaded images for curriculum markdown (served under /static/uploads/...)
UPLOAD_DIR = BASE_DIR / "app" / "static" / "uploads" / "content"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
UPLOAD_URL_PREFIX = "/static/uploads/content"
MAX_UPLOAD_BYTES = int(os.environ.get("CISS_MAX_UPLOAD_BYTES", str(5 * 1024 * 1024)))  # 5 MB
ALLOWED_IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg"}

# Lockheed Martin proprietary marking — shown on every module and
# repeated in PDF / print headers and footers.
PROPRIETARY_MARKING = "LOCKHEED MARTIN PROPRIETARY INFORMATION"
PROPRIETARY_NOTICE = (
    "This document contains Lockheed Martin Proprietary Information. "
    "Do not disclose, reproduce, or distribute without written authorization."
)

# PlantUML public render server (override if self-hosting)
PLANTUML_SERVER = os.environ.get(
    "CISS_PLANTUML_SERVER",
    "https://www.plantuml.com/plantuml/svg/",
)

