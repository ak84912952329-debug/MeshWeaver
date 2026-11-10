"""Integration between peer communication and task execution."""

import asyncio

from broker import Broker
from peer import Peer
from protocol import Message
from task import Task, TaskStatus


class PeerTaskServer:
    """Receive and execute tasks from remote peers."""

    def __init__(self, peer_id: str, broker: Broker):
        self.peer_id = peer_id
        self.broker = broker
        self.server = None

    async def start(self, host="127.0.0.1", port=0):
        """Start the task receiving server."""
        self.server = await asyncio.start_server(
            self.handle_client, host, port
        )
        return self.server.sockets[0].getsockname()

    async def handle_client(self, reader, writer):
        """Receive a task, execute it, and return the result."""
        try:
            raw = await reader.readline()

            if not raw:
                return

            message = Message.decode(raw.rstrip(b"\r\n"))

            if message.message_type != "task_submit":
                raise ValueError("Expected a task_submit message.")

            payload = message.payload

            task = Task(
                function_name=payload["function_name"],
                args=tuple(payload.get("args", [])),
                kwargs=payload.get("kwargs", {}),
                task_id=payload["task_id"],
            )

            await self.broker.submit_task(task)

            response = Message(
                message_type="task_result",
                sender=self.peer_id,
                payload={
                    "task_id": task.task_id,
                    "status": task.status.value,
                    "result": task.result,
                    "error": task.error,
                },
            )

        except Exception as exc:
            response = Message(
                message_type="error",
                sender=self.peer_id,
                payload={"error": str(exc)},
            )

        try:
            writer.write(response.encode() + b"\n")
            await writer.drain()
        finally:
            writer.close()
            await writer.wait_closed()

    async def close(self):
        """Stop the task receiving server."""
        if self.server is not None:
            self.server.close()
            await self.server.wait_closed()


class PeerTaskClient:
    """Submit tasks to a remote peer."""

    def __init__(self, peer: Peer):
        self.peer = peer

    async def submit_task(self, task: Task):
        """Send a task and receive its execution result."""
        if task.status != TaskStatus.PENDING:
            raise ValueError("Only pending tasks can be submitted.")

        message = Message(
            message_type="task_submit",
            sender=self.peer.peer_id,
            payload={
                "task_id": task.task_id,
                "function_name": task.function_name,
                "args": list(task.args),
                "kwargs": task.kwargs,
            },
        )

        await self.peer.send(message)
        response = await self.peer.receive()

        if response.message_type == "error":
            task.mark_failed(response.payload.get("error", "Unknown error"))
            raise RuntimeError(task.error)

        if response.message_type != "task_result":
            raise ValueError("Unexpected response from remote peer.")

        if response.payload.get("task_id") != task.task_id:
            raise ValueError("Received result for a different task.")

        if response.payload.get("status") == "completed":
            task.mark_completed(response.payload.get("result"))
        else:
            task.mark_failed(
                response.payload.get("error", "Task execution failed.")
            )

        return task