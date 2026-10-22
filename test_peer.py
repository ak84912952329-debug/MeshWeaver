"""Tests for MeshWeaver peer connection handling."""

import unittest
from unittest.mock import AsyncMock

from peer import Peer


class TestPeer(unittest.TestCase):
    def test_peer_initializes_with_valid_id(self):
        peer = Peer("peer-1")

        self.assertEqual(peer.peer_id, "peer-1")
        self.assertIsNone(peer.reader)
        self.assertIsNone(peer.writer)
        self.assertFalse(peer.connected)

    def test_peer_rejects_empty_id(self):
        with self.assertRaises(ValueError):
            Peer("")

    def test_peer_rejects_whitespace_id(self):
        with self.assertRaises(ValueError):
            Peer("   ")

    def test_peer_rejects_non_string_id(self):
        with self.assertRaises(ValueError):
            Peer(None)

    def test_connected_is_false_when_writer_is_missing(self):
        peer = Peer("peer-1")

        self.assertFalse(peer.connected)

    def test_connected_is_false_when_writer_is_closing(self):
        peer = Peer("peer-1")
        writer = AsyncMock()
        writer.is_closing.return_value = True
        peer.writer = writer

        self.assertFalse(peer.connected)


if __name__ == "__main__":
    unittest.main()