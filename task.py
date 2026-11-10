"""Task model for MeshWeaver."""

from dataclasses import dataclass, field
from enum import Enum
from uuid import uuid4
from typing import Any


class TaskStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class Task:
    """Represent a task submitted to MeshWeaver."""

    function_name: str
    args: tuple = field(default_factory=tuple)
    kwargs: dict = field(default_factory=dict)
    task_id: str = field(default_factory=lambda: str(uuid4()))
    status: TaskStatus = TaskStatus.PENDING
    result: Any = None
    error: str = ""

    def mark_running(self):
        self.status = TaskStatus.RUNNING

    def mark_completed(self, result):
        self.result = result
        self.status = TaskStatus.COMPLETED

    def mark_failed(self, error):
        self.error = str(error)
        self.status = TaskStatus.FAILED