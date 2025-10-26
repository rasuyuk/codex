"""CLI entry point for running the echo server."""

from __future__ import annotations

import argparse

from .server import ServerConfig, run_server


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run a simple asyncio-based TCP echo server.")
    parser.add_argument("--host", default="127.0.0.1", help="Interface to bind to (default: %(default)s)")
    parser.add_argument("--port", type=int, default=9999, help="Port to listen on (default: %(default)s)")
    parser.add_argument("--backlog", type=int, default=100, help="Backlog of pending connections (default: %(default)s)")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_server(ServerConfig(host=args.host, port=args.port, backlog=args.backlog))


if __name__ == "__main__":
    main()
