from controllers.task_controller import TaskController
from models.task import Task

class GUIController:
    # Controller class for the GUI, responsible for handling user interactions and delegating tasks to the TaskController.
    def __init__(self, task_controller: TaskController) -> None:
        # Initialize the GUIController with a TaskController instance, allowing it to perform operations on tasks.
        self.task_controller = task_controller

    def list_tasks(self) -> list[Task]:
        # Retrieve a list of all tasks by delegating the call to the TaskController's list_tasks method.
        return self.task_controller.list_tasks()
    
    def add_task(
        self, 
        title: str, 
        description: str, 
        due_date: str | None, 
        priority: str
    ) -> Task:
    # Add a new task by delegating the call to the TaskController's add_task method, passing the necessary parameters for task creation.
        return self.task_controller.add_task(title, description, due_date, priority)
    
    def complete_task(self, task_id: int) -> str:
        # Mark a task as completed by delegating the call to the TaskController's complete_task method, passing the task ID.
        return self.task_controller.complete_task(task_id)
    
    def delete_task(self, task_id: int) -> bool:
        # Delete a task by delegating the call to the TaskController's delete_task method, passing the task ID and returning the result.
        return self.task_controller.delete_task(task_id)
    
    def get_task(self, task_id: int) -> Task | None:
        # Retrieve a specific task by delegating the call to the TaskController's get_task method, passing the task ID and returning the task if found.
        return self.task_controller.get_task(task_id)
