from datetime import date, datetime

from django.db import models
from dataclasses import dataclass
from enum import Enum

class TaskPriority(str, Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"

    @classmethod
    def from_value(cls, value: str) -> "TaskPriority":
        normalized = value.strip().lower()

        mapping = {
            "low": cls.LOW,
            "medium": cls.MEDIUM,
            "high": cls.HIGH
        }
        if normalized not in mapping:
            raise ValueError("Invalid priority. Choose one of: Low, Medium, High.")
        
        return mapping[normalized]

class TaskStatus(str, Enum):
    PENDING = "Pending"
    COMPLETED = "Completed"

@dataclass
class Task:
    task_id: int
    title: str
    description: str
    priority: str
    due_date: str | None
    status: TaskStatus = TaskStatus.PENDING,
    notes: str | None = None # new field for notes

    def __post_init__(self) -> None:
        # Validate priorty
        if isinstance(self.priority, str): 
            self.priority = TaskPriority.from_value(self.priority)
        
        # Validate status
        if isinstance(self.status, str):
            self.status = TaskStatus(self.status)

        # Validate due date format
        if self.due_date is not None:
            try:
                self.due_date = datetime.strptime(self.due_date, "%Y-%m-%d").date()
            except ValueError:
                raise ValueError("Invalid due date format. Use YYYY-MM-DD.")

    def to_dict(self) -> dict:
        return {
            "task_id": self.task_id,
            "title": self.title,
            "description": self.description,
            "priority": self.priority.value,
            "due_date": self.due_date.isoformat() if isinstance(self.due_date, date) else self.due_date,
            "status": self.status.value, 
            "notes": self.notes #include notes in the dictionary representation
        }
        
    @classmethod
    def from_dict(cls, data: dict) -> "Task":
        return cls(
            task_id=data["task_id"],
            title=data["title"],
            description=data.get("description", ""),
            priority=TaskPriority.from_value(data["priority"]),
            due_date=data.get("due_date"),
            status=TaskStatus(data.get("status", TaskStatus.PENDING.value)),
            notes=data.get("notes") #get notes from the dictionary, default to None if not present
        )