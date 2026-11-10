import unittest

from broker import Broker
from worker import Worker
from task import Task, TaskStatus


class TestBroker(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.broker = Broker()
        self.worker = Worker("worker-1")
        self.worker.register_function("add", lambda a, b: a + b)
        self.broker.register_worker(self.worker)

    async def test_task_submission(self):
        task = Task("add", args=(10, 20))
        await self.broker.submit_task(task)

        self.assertEqual(task.status, TaskStatus.COMPLETED)

    async def test_task_result(self):
        task = Task("add", args=(10, 20))
        await self.broker.submit_task(task)

        self.assertEqual(
            self.broker.get_result(task.task_id), 30
        )

    async def test_task_retrieval(self):
        task = Task("add", args=(5, 5))
        await self.broker.submit_task(task)

        self.assertIs(
            self.broker.get_task(task.task_id), task
        )

    async def test_no_workers(self):
        broker = Broker()
        task = Task("add", args=(1, 2))

        with self.assertRaises(RuntimeError):
            await broker.submit_task(task)

    async def test_unknown_task(self):
        with self.assertRaises(KeyError):
            self.broker.get_task("unknown-id")

    async def test_failed_task(self):
        task = Task("unknown_function")
        await self.broker.submit_task(task)

        self.assertEqual(task.status, TaskStatus.FAILED)

        with self.assertRaises(RuntimeError):
            self.broker.get_result(task.task_id)


if __name__ == "__main__":
    unittest.main()