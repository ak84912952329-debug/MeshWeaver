import unittest

from peer import Peer
from protocol import Message


class TestNetworkErrors(unittest.IsolatedAsyncioTestCase):

    async def test_send_without_connection(self):
        peer = Peer("peer-1")

        message = Message(
            message_type="ping",
            sender="peer-1",
            payload={}
        )

        with self.assertRaises(ConnectionError):
            await peer.send(message)

    async def test_receive_without_connection(self):
        peer = Peer("peer-1")

        with self.assertRaises(ConnectionError):
            await peer.receive()

    async def test_connect_invalid_port(self):
        peer = Peer("peer-1")

        with self.assertRaises(OSError):
            await peer.connect("127.0.0.1", 1)

    async def test_close_without_connection(self):
        peer = Peer("peer-1")

        await peer.close()

        self.assertFalse(peer.connected)


if __name__ == "__main__":
    unittest.main()