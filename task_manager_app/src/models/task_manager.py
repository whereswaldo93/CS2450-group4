from config import ALLOWED_PRIORITIES
from models.task import create_task
from datetime import datetime

class TaskManager:
    def __init__(self, repo):
        self.repo = repo

    def validate_due_date(self, due_date: str | None) -> str | None:
        if not due_date:
            return None

        try:
            datetime.strptime(due_date, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Invalid due date format. Use YYYY-MM-DD.")

        return due_date

    def normalize_priority(self, priority: str) -> str:
        key = priority.strip().lower()
        if key not in ALLOWED_PRIORITIES:
            raise ValueError("Invalid priority. Choose one of: Low, Medium, High.")
        return ALLOWED_PRIORITIES[key]

    def next_task_id(self, tasks: list[dict]) -> int:
        ids = []
        
        for task in tasks:
            try:
                ids.append(int(task.get("id", 0)))
            except (TypeError, ValueError):
                continue
        return (max(ids) if ids else 0) + 1

    def add_task(self, title, description, due_date, priority):
        tasks = self.repo.load_tasks()

        normalized_title = title.strip()
        if not normalized_title:
            raise ValueError("Title cannot be empty")
        
        task = create_task(
            task_id = self.next_task_id(tasks),
            title = normalized_title,
            description = description,
            priority = self.normalize_priority(priority),
            due_date = self.validate_due_date(due_date)
        )

        tasks.append(task)
        self.repo.save_tasks(tasks)
        return task

    def list_tasks(self):
        return self.repo.load_tasks()

    def complete_task(self, task_id: int):
        tasks = self.repo.load_tasks()

        for task in tasks:
            try:
                current_id = int(task.get("id"))
            except (TypeError, ValueError):
                continue

            if current_id == task_id:
                if task.get("status") == "Complete":
                    return "already_complete"
                
                task["status"] = "Complete"
                task["updated_at"] = datetime.now().isoformat(timespec="seconds")
                self.repo.save_tasks(tasks)
                return "completed"
        return "not_found"

    def delete_task(self, task_id: int):
        tasks = self.repo.load_tasks()

        for i, task in enumerate(tasks):
            try:
                current_id = int(task.get("id"))
            except (TypeError, ValueError):
                continue

            if current_id == task_id:
                del tasks[i]
                self.repo.save_tasks(tasks)
                return True
            
        return False