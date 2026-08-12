"""SQLAlchemy engine and session."""

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from app.config import DATABASE_URL

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def _sqlite_add_column_if_missing(table: str, column: str, ddl_type: str) -> None:
    """Lightweight SQLite migrate for existing course DBs."""
    if not str(DATABASE_URL).startswith("sqlite"):
        return
    with engine.begin() as conn:
        rows = conn.execute(text(f"PRAGMA table_info({table})")).fetchall()
        names = {r[1] for r in rows}
        if column not in names:
            conn.execute(text(f"ALTER TABLE {table} ADD COLUMN {column} {ddl_type}"))


def init_db():
    from app import models  # noqa: F401

    Base.metadata.create_all(bind=engine)
    # Existing DBs created before primary_track
    _sqlite_add_column_if_missing(
        "candidates", "primary_track", "VARCHAR(40) DEFAULT 'se'"
    )
