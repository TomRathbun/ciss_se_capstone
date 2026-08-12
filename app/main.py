"""CISS Capstone Course — FastAPI entry."""

from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.config import APP_NAME, APP_VERSION
from app.database import init_db
from app.routes.pages import router
from app.seed import seed_users

Path("app/static/css").mkdir(parents=True, exist_ok=True)

app = FastAPI(title=APP_NAME, version=APP_VERSION)
app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.include_router(router)


@app.on_event("startup")
async def startup():
    init_db()
    seed_users()
