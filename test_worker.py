import unittest
import asyncio

from worker import Worker
from task import Task, TaskStatus


class TestWorker(unittest.IsolatedAsyncioTestCase):

    async def test_successful_execution(self):
        worker = Worker("worker-1")
        worker.register_function("add", lambda a, b: a + b)

        task = Task("add", args=(10, 20))
        result = await worker.execute(task)

        self.assertEqual(result, 30)
        self.assertEqual(task.status, TaskStatus.COMPLETED)

    async def test_unknown_function(self):
        worker = Worker("worker-1")
        task = Task("unknown")

        await worker.execute(task)

        self.assertEqual(task.status, TaskStatus.FAILED)

    async def test_invalid_task(self):
        worker = Worker("worker-1")

        with self.assertRaises(ValueError):
            await worker.execute("invalid")


if __name__ == "__main__":
    unittest.main()