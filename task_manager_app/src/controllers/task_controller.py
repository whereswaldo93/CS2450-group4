from models.task_manager import TaskManager
from models.task import Task

class TaskController:
    def __init__(self, task_manager: TaskManager) -> None:
        self.task_manager = task_manager

    def add_task(
        self, 
        title: str, 
        description: str, 
        due_date: str | None, 
        priority: str
    ) -> Task:
        return self.task_manager.add_task(
            title=title,   
            description=description,
            due_date=due_date,
            priority=priority
        )

    def list_tasks(self) -> list[Task]:
        return self.task_manager.list_tasks()

    def get_task(self, task_id: int) -> Task | None:
        return self.task_manager.get_task(task_id)

    def complete_task(self, task_id: int) -> str:
        return self.task_manager.complete_task(task_id)

    def delete_task(self, task_id: int) -> bool:
        return self.task_manager.delete_task(task_id)