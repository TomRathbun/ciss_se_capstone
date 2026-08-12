"""Entry point — uv run python run.py

Binds on 0.0.0.0 so LAN/Tailscale clients can connect, but prints
127.0.0.1 / localhost so the terminal URL is Ctrl+Click friendly.

Reload only watches project source (app/, content/), never .venv — watching
site-packages during uv sync caused half-upgraded uvicorn crashes.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import uvicorn

ROOT = Path(__file__).resolve().parent


def main() -> None:
    parser = argparse.ArgumentParser(description="CISS Capstone Course")
    parser.add_argument("--host", default="0.0.0.0", help="Bind address (default 0.0.0.0)")
    parser.add_argument("--port", type=int, default=8890)
    parser.add_argument(
        "--no-reload",
        action="store_true",
        help="Disable auto-reload (more stable if the env is being updated)",
    )
    args = parser.parse_args()

    # 0.0.0.0 is not a usable browser host — print clickable local URLs
    print()
    print("  CISS Capstone")
    print(f"  Local:   http://127.0.0.1:{args.port}")
    print(f"  Local:   http://localhost:{args.port}")
    if args.host in ("0.0.0.0", "::"):
        print(f"  Binding: {args.host}:{args.port}  (all interfaces)")
    else:
        print(f"  Network: http://{args.host}:{args.port}")
    print()

    kwargs: dict = {
        "app": "app.main:app",
        "host": args.host,
        "port": args.port,
    }
    if not args.no_reload:
        kwargs["reload"] = True
        # Only watch our code + curriculum — never .venv or site-packages
        kwargs["reload_dirs"] = [
            str(ROOT / "app"),
            str(ROOT / "content"),
            str(ROOT / "run.py"),
        ]
        kwargs["reload_excludes"] = [
            ".venv/*",
            "**/.venv/**",
            "**/__pycache__/**",
            "**/*.db",
            "**/uv.lock",
        ]

    uvicorn.run(**kwargs)


if __name__ == "__main__":
    main()
