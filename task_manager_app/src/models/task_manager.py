from models.task import Task, TaskPriority, TaskStatus
from datetime import datetime
from typing import Protocol

class TaskRepo(Protocol):
    def load_tasks(self) -> list[Task]: 
        ...
    def save_tasks(self, tasks: list[Task]) -> None: 
        ...

class TaskManager:
    def __init__(self, repo: TaskRepo) -> None:
        self.repo = repo

    def validate_due_date(self, due_date: str | None) -> str | None:
        if not due_date:
            return None

        try:
            datetime.strptime(due_date, "%Y-%m-%d")
        except ValueError as e:
            raise ValueError("Invalid due date format. Use YYYY-MM-DD.")

        return due_date
    
    def next_task_id(self, tasks: list[Task]) -> int:
        return (max(task.task_id for task in tasks) if tasks else 0) + 1
    
    def _find_task_index(self, tasks: list[Task], task_id: int) -> int | None:
        for i, task in enumerate(tasks):
            if task.task_id == task_id:
                return i
        return None
    
    def add_task(
        self, 
        title: str, 
        description: str, 
        due_date: str | None, 
        priority: str
    ) -> Task:
        tasks = self.repo.load_tasks()

        normalized_title = title.strip()
        if not normalized_title:
            raise ValueError("Title cannot be empty")

        task = Task(
            task_id=self.next_task_id(tasks),
            title=normalized_title,
            description=description.strip(),
            priority=TaskPriority.from_value(priority),
            due_date=self.validate_due_date(due_date),
        )

        tasks.append(task)
        self.repo.save_tasks(tasks)

        return task

    def list_tasks(self) -> list[Task]:
        return self.repo.load_tasks()

    def get_task(self, task_id: int) -> Task | None:
        tasks = self.repo.load_tasks()
        index = self._find_task_index(tasks, task_id)
        return None if index is None else tasks[index]

    def complete_task(self, task_id: int) -> str:
        tasks = self.repo.load_tasks()
        index = self._find_task_index(tasks, task_id)

        if index is None:
            return "not_found"

        task = tasks[index]
        if task.status == TaskStatus.COMPLETED:
            return "already_complete"

        task.status = TaskStatus.COMPLETED
        self.repo.save_tasks(tasks)

        return "completed"

    def delete_task(self, task_id: int) -> bool:
        tasks = self.repo.load_tasks()
        index = self._find_task_index(tasks, task_id)

        if index is None:
            return False

        del tasks[index]
        self.repo.save_tasks(tasks)
        return True