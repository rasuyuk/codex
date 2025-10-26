"""Tests for the asyncio echo server."""

from __future__ import annotations

import asyncio

import pytest

from echo_server.server import ServerConfig, serve

pytestmark = pytest.mark.asyncio


async def test_echo_roundtrip() -> None:
    """Server should echo every payload byte-for-byte."""
    config = ServerConfig(port=0)  # let OS pick a free port
    async with serve(config) as server:
        sock = server.sockets[0]
        host, port = sock.getsockname()
        reader, writer = await asyncio.open_connection(host, port)

        payloads = [b"hello", b"world", b"!"]
        for payload in payloads:
            writer.write(payload)
            await writer.drain()
            echoed = await asyncio.wait_for(reader.readexactly(len(payload)), timeout=1)
            assert echoed == payload

        writer.close()
        await writer.wait_closed()


async def test_close_by_client_stops_handler() -> None:
    """Server should exit handler cleanly when client disconnects."""
    config = ServerConfig(port=0)
    async with serve(config) as server:
        host, port = server.sockets[0].getsockname()
        reader, writer = await asyncio.open_connection(host, port)

        writer.write(b"ping")
        await writer.drain()
        await asyncio.wait_for(reader.readexactly(4), timeout=1)

        writer.close()
        await writer.wait_closed()

        # Give the server a brief chance to detect closure
        await asyncio.sleep(0.05)
