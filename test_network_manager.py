import unittest
from network import Network


class TestNetwork(unittest.TestCase):

    def setUp(self):
        self.network = Network()

    def test_add_peer(self):
        peer = self.network.add_peer("peer-1")
        self.assertEqual(peer.peer_id, "peer-1")

    def test_duplicate_peer(self):
        self.network.add_peer("peer-1")
        with self.assertRaises(ValueError):
            self.network.add_peer("peer-1")

    def test_get_peer(self):
        peer = self.network.add_peer("peer-1")
        self.assertIs(self.network.get_peer("peer-1"), peer)

    def test_remove_peer(self):
        self.network.add_peer("peer-1")
        self.network.remove_peer("peer-1")
        self.assertEqual(self.network.list_peers(), [])

    def test_list_peers(self):
        self.network.add_peer("peer-1")
        self.network.add_peer("peer-2")
        self.assertEqual(
            self.network.list_peers(),
            ["peer-1", "peer-2"]
        )


if __name__ == "__main__":
    unittest.main()