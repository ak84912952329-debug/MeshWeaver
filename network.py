"""Network management for MeshWeaver peers."""

from typing import Dict

from peer import Peer


class Network:
    """Manage connections with multiple peers."""

    def __init__(self) -> None:
        self.peers: Dict[str, Peer] = {}

    def add_peer(self, peer_id: str) -> Peer:
        """Add a new peer to the network."""
        if peer_id in self.peers:
            raise ValueError(f"Peer {peer_id} already exists.")

        peer = Peer(peer_id)
        self.peers[peer_id] = peer
        return peer

    def get_peer(self, peer_id: str) -> Peer:
        """Retrieve a peer by its ID."""
        if peer_id not in self.peers:
            raise KeyError(f"Peer {peer_id} not found.")

        return self.peers[peer_id]

    def remove_peer(self, peer_id: str) -> None:
        """Remove a peer from the network."""
        if peer_id not in self.peers:
            raise KeyError(f"Peer {peer_id} not found.")

        del self.peers[peer_id]

    def list_peers(self) -> list[str]:
        """Return all registered peer IDs."""
        return list(self.peers.keys())

    async def close_all(self) -> None:
        """Close all peer connections."""
        for peer in list(self.peers.values()):
            await peer.close()

        self.peers.clear()