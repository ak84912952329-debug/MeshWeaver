"""Worker module for MeshWeaver task execution."""

import inspect
from typing import Callable

from task import Task


class Worker:
    """Execute tasks assigned by the task broker."""

    def __init__(self, worker_id: str):
        if not isinstance(worker_id, str) or not worker_id.strip():
            raise ValueError("Worker ID must be a non-empty string.")

        self.worker_id = worker_id
        self.functions: dict[str, Callable] = {}

    def register_function(self, name: str, function: Callable) -> None:
        """Register a function that the worker can execute."""
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Function name cannot be empty.")

        if not callable(function):
            raise ValueError("Registered object must be callable.")

        self.functions[name] = function

    async def execute(self, task: Task):
        """Execute a task and store its result or error."""
        if not isinstance(task, Task):
            raise ValueError("Expected a Task object.")

        task.mark_running()

        try:
            function = self.functions.get(task.function_name)

            if function is None:
                raise ValueError(
                    f"Function '{task.function_name}' is not registered."
                )

            result = function(*task.args, **task.kwargs)

            if inspect.isawaitable(result):
                result = await result

            task.mark_completed(result)
            return result

        except Exception as error:
            task.mark_failed(error)
            return None