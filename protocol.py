"""Message protocol for MeshWeaver peer-to-peer communication."""

import json
from dataclasses import dataclass
from typing import Any


SUPPORTED_TYPES = {
    "task_submit",
    "task_result",
    "status",
    "error",
    "ping",
    "pong",
}


@dataclass
class Message:
    """A message exchanged between MeshWeaver peers."""

    message_type: str
    sender: str
    payload: dict[str, Any]
    message_id: str = ""
    def __post_init__(self) -> None:
        if not isinstance(self.message_type, str):
            raise ValueError("Message type must be a string.")

        if self.message_type not in SUPPORTED_TYPES:
            raise ValueError(
                f"Unsupported message type: {self.message_type}"
            )

        if not isinstance(self.sender, str) or not self.sender.strip():
            raise ValueError("Sender must be a non-empty string.")

        if not isinstance(self.payload, dict):
            raise ValueError("Payload must be a dictionary.")

        if not isinstance(self.message_id, str):
            raise ValueError("Message ID must be a string.")

    def to_dict(self) -> dict[str, Any]:
        """Convert the message into a dictionary."""
        return {
            "message_type": self.message_type,
            "sender": self.sender,
            "payload": self.payload,
            "message_id": self.message_id,
        }

    def encode(self) -> bytes:
        """Serialize the message into UTF-8 JSON bytes."""
        return json.dumps(self.to_dict()).encode("utf-8")

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Message":
        """Create a message from a dictionary."""
        required = {"message_type", "sender", "payload"}

        if not isinstance(data, dict):
            raise ValueError("Message data must be a dictionary.")

        missing = required - data.keys()
        if missing:
            raise ValueError(
                f"Missing required fields: {sorted(missing)}"
            )

        return cls(
            message_type=data["message_type"],
            sender=data["sender"],
            payload=data["payload"],
            message_id=data.get("message_id", ""),
        )

    @classmethod
    def decode(cls, raw: bytes) -> "Message":
        """Deserialize UTF-8 JSON bytes into a message."""
        try:
            data = json.loads(raw.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError("Invalid message encoding or JSON.") from exc

        return cls.from_dict(data)