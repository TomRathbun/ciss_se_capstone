"""Entry point — uv run python run.py [--no-ssl]"""

import argparse
import os

import uvicorn

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CISS SE Capstone Course")
    parser.add_argument("--port", type=int, default=8890)
    parser.add_argument("--no-ssl", dest="ssl", action="store_false", default=False)
    args = parser.parse_args()

    print(f"Starting CISS SE Capstone on http://0.0.0.0:{args.port}")
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=args.port,
        reload=True,
    )
