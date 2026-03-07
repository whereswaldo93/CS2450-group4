from controllers.task_controller import TaskController
from models.task import Task

class GUIController:
    def __init__(self, task_controller: TaskController) -> None:
        self.task_controller = task_controller

    def list_tasks(self) -> list[Task]:
        return self.task_controller.list_tasks()
    
    def add_task(
        self, 
        title: str, 
        description: str, 
        due_date: str | None, 
        priority: str
    ) -> Task:
        return self.task_controller.add_task(title, description, due_date, priority)
    
    def complete_task(self, task_id: int) -> str:
        return self.task_controller.complete_task(task_id)
    
    def delete_task(self, task_id: int) -> bool:
        return self.task_controller.delete_task(task_id)
    
    def get_task(self, task_id: int) -> Task | None:
        return self.task_controller.get_task(task_id)