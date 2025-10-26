"""
Asyncio-powered TCP echo server utilities.

The module exposes two entry points:
* serve: coroutine returning the running asyncio.Server object
* run_server: synchronous helper that runs the server until interrupted
"""

from __future__ import annotations

import asyncio
import logging
from contextlib import asynccontextmanager
from dataclasses import dataclass
from typing import AsyncIterator, Optional

LOG = logging.getLogger(__name__)


@dataclass(frozen=True)
class ServerConfig:
    """Configuration container for the echo server."""

    host: str = "127.0.0.1"
    port: int = 9999
    backlog: int = 100


async def handle_echo(reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
    """Handle a single client by echoing back every chunk received."""
    peer = writer.get_extra_info("peername")
    LOG.info("Accepted connection from %s", peer)

    try:
        while True:
            data = await reader.read(1024)
            if not data:
                LOG.info("Client %s closed connection", peer)
                break
            LOG.debug("Received %d bytes from %s", len(data), peer)
            writer.write(data)
            await writer.drain()
    except asyncio.CancelledError:
        LOG.warning("Connection with %s cancelled", peer)
        raise
    finally:
        writer.close()
        await writer.wait_closed()
        LOG.info("Connection with %s fully closed", peer)


@asynccontextmanager
async def serve(config: ServerConfig) -> AsyncIterator[asyncio.AbstractServer]:
    """
    Start the echo server with provided configuration.

    Yields the running asyncio.Server instance and ensures cleanup afterwards.
    """
    server = await asyncio.start_server(handle_echo, host=config.host, port=config.port, backlog=config.backlog)
    try:
        sockets = ", ".join(str(sock.getsockname()) for sock in server.sockets or [])
        LOG.info("Serving on %s", sockets)
        yield server
    finally:
        LOG.info("Shutting down server")
        server.close()
        await server.wait_closed()


def run_server(config: Optional[ServerConfig] = None) -> None:
    """
    Run the echo server until interrupted via Ctrl+C.

    Example:
        run_server(ServerConfig(host="0.0.0.0", port=8000))
    """
    cfg = config or ServerConfig()

    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")

    async def _runner() -> None:
        async with serve(cfg):
            # Block forever; cancellation happens when the event loop stops.
            await asyncio.Event().wait()

    try:
        asyncio.run(_runner())
    except KeyboardInterrupt:
        LOG.info("Received interrupt, stopping server")
