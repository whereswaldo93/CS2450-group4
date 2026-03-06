from datetime import datetime
from dataclasses import dataclass


@dataclass
class Task:
    task_id: int
    title: str
    description: str
    priority: str
    due_date: str | None
    status: str = "Pending"
