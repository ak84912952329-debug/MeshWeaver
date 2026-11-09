"""Task broker for MeshWeaver."""

from task import Task, TaskStatus
from worker import Worker


class Broker:
    """Manage task submission and worker execution."""

    def __init__(self):
        self.workers: list[Worker] = []
        self.tasks: dict[str, Task] = {}
        self._next_worker = 0

    def register_worker(self, worker: Worker) -> None:
        """Register a worker with the broker."""
        if not isinstance(worker, Worker):
            raise ValueError("Invalid worker.")

        if any(w.worker_id == worker.worker_id for w in self.workers):
            raise ValueError("Worker already registered.")

        self.workers.append(worker)

    async def submit_task(self, task: Task) -> Task:
        """Submit a task and assign it to a worker."""
        if not isinstance(task, Task):
            raise ValueError("Invalid task.")

        if task.task_id in self.tasks:
            raise ValueError("Task already submitted.")

        if not self.workers:
            raise RuntimeError("No workers available.")

        self.tasks[task.task_id] = task

        worker = self.workers[
            self._next_worker % len(self.workers)
        ]
        self._next_worker += 1

        await worker.execute(task)

        return task

    def get_task(self, task_id: str) -> Task:
        """Retrieve a task by its ID."""
        if task_id not in self.tasks:
            raise KeyError("Task not found.")

        return self.tasks[task_id]

    def get_result(self, task_id: str):
        """Retrieve the result of a completed task."""
        task = self.get_task(task_id)

        if task.status == TaskStatus.FAILED:
            raise RuntimeError(task.error)

        if task.status != TaskStatus.COMPLETED:
            raise RuntimeError("Task is not completed.")

        return task.result

    def list_tasks(self) -> list[Task]:
        """Return all submitted tasks."""
        return list(self.tasks.values())