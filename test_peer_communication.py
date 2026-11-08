"""Integration test for communication between peers."""

import asyncio
import unittest

from peer import Peer
from protocol import Message


class TestPeerCommunication(unittest.IsolatedAsyncioTestCase):

    async def test_two_peer_message_exchange(self):
        async def handle_client(reader, writer):
            data = await reader.readline()
            writer.write(data)
            await writer.drain()
            writer.close()
            await writer.wait_closed()

        server = await asyncio.start_server(
            handle_client, "127.0.0.1", 0
        )

        host, port = server.sockets[0].getsockname()[:2]
        peer = Peer("peer-1")

        try:
            await peer.connect(host, port)

            message = Message(
                message_type="ping",
                sender="peer-1",
                payload={"message": "Hello"},
            )

            await peer.send(message)
            received = await peer.receive()

            self.assertEqual(received.message_type, "ping")
            self.assertEqual(received.sender, "peer-1")
            self.assertEqual(received.payload["message"], "Hello")

        finally:
            await peer.close()
            server.close()
            await server.wait_closed()


if __name__ == "__main__":
    unittest.main()