"""Entry point — start the FastAPI server."""

import argparse

import uvicorn


def main() -> None:
    """Start the FastAPI server with optional port argument."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()
    uvicorn.run("app.api:app", host="0.0.0.0", port=args.port, reload=True)


if __name__ == "__main__":
    main()
