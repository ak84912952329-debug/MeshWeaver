import unittest

from broker import Broker
from worker import Worker
from peer import Peer
from task import Task, TaskStatus
from peer_integration import PeerTaskServer, PeerTaskClient


class TestPeerIntegration(unittest.IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        self.broker = Broker()
        self.worker = Worker("worker-1")

        self.worker.register_function(
            "add", lambda a, b: a + b
        )

        self.broker.register_worker(self.worker)

        self.server = PeerTaskServer("server-peer", self.broker)
        host, port = await self.server.start()

        self.client_peer = Peer("client-peer")
        await self.client_peer.connect(host, port)

        self.client = PeerTaskClient(self.client_peer)

    async def asyncTearDown(self):
        await self.client_peer.close()
        await self.server.close()

    async def test_remote_task_execution(self):
        task = Task("add", args=(10, 20))

        result = await self.client.submit_task(task)

        self.assertEqual(result.result, 30)
        self.assertEqual(result.status, TaskStatus.COMPLETED)

    async def test_remote_task_failure(self):
        task = Task("unknown_function")

        result = await self.client.submit_task(task)

        self.assertEqual(result.status, TaskStatus.FAILED)

    async def test_task_result_is_stored(self):
        task = Task("add", args=(5, 5))

        await self.client.submit_task(task)

        self.assertEqual(
            self.broker.get_result(task.task_id), 10
        )


if __name__ == "__main__":
    unittest.main()