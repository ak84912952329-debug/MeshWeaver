import unittest

from protocol import Message


class TestMessageProtocol(unittest.TestCase):

    def test_encode_and_decode(self):
        original = Message(
            message_type="task_submit",
            sender="peer1",
            payload={"task_id": "task-001", "value": 10},
            message_id="msg-001",
        )

        decoded = Message.decode(original.encode())

        self.assertEqual(decoded.message_type, "task_submit")
        self.assertEqual(decoded.sender, "peer1")
        self.assertEqual(decoded.payload["value"], 10)
        self.assertEqual(decoded.message_id, "msg-001")

    def test_invalid_message_type(self):
        with self.assertRaises(ValueError):
            Message(
                message_type="unknown",
                sender="peer1",
                payload={},
            )

    def test_invalid_json(self):
        with self.assertRaises(ValueError):
            Message.decode(b"not valid json")
    def test_empty_sender_is_rejected(self):
        with self.assertRaises(ValueError):
            Message(
                message_type="status",
                sender="   ",
                payload={},
            )

    def test_non_string_message_type_is_rejected(self):
        with self.assertRaises(ValueError):
            Message(
                message_type=123,
                sender="peer1",
                payload={},
            )

    def test_non_string_message_id_is_rejected(self):
        with self.assertRaises(ValueError):
            Message(
                message_type="ping",
                sender="peer1",
                payload={},
                message_id=123,
            )


if __name__ == "__main__":
    unittest.main()