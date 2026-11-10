"""Peer communication module for MeshWeaver."""

import asyncio
from typing import Optional

from protocol import Message


class Peer:
    """Manage a connection with another MeshWeaver peer."""

    def __init__(self, peer_id: str) -> None:
        if not isinstance(peer_id, str) or not peer_id.strip():
            raise ValueError("Peer ID must be a non-empty string.")

        self.peer_id = peer_id
        self.reader: Optional[asyncio.StreamReader] = None
        self.writer: Optional[asyncio.StreamWriter] = None

    @property
    def connected(self) -> bool:
        """Return whether the peer has an active connection."""
        return self.writer is not None and not self.writer.is_closing()

    async def connect(self, host: str, port: int) -> None:
        """Connect to another peer over TCP."""
        if self.connected:
            raise ConnectionError("Peer is already connected.")

        try:
            self.reader, self.writer = await asyncio.open_connection(
            host, port
        )
        except (OSError, asyncio.TimeoutError) as exc:
            self.reader = None
            self.writer = None
            raise ConnectionError(
            f"Failed to connect to peer {self.peer_id}: {exc}"
        ) from exc

    async def send(self, message: Message) -> None:
        """Send a valid message to the connected peer."""
        if not self.connected or self.writer is None:
            raise ConnectionError("Peer is not connected.")

        if not isinstance(message, Message):
            raise ValueError("Only Message objects can be sent.")

        self.writer.write(message.encode() + b"\n")
        await self.writer.drain()

    async def receive(self) -> Message:
        """Receive one newline-delimited JSON message."""
        if not self.connected or self.reader is None:
            raise ConnectionError("Peer is not connected.")

        raw = await self.reader.readline()

        if not raw:
            raise ConnectionError("Peer closed the connection.")

        return Message.decode(raw.rstrip(b"\r\n"))

    async def close(self) -> None:
        """Close the connection to the peer."""
        if self.writer is not None:
            self.writer.close()
            try:
                await self.writer.wait_closed()
            finally:
                self.reader = None
                self.writer = None