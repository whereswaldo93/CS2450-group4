from config import ALLOWED_PRIORITIES
from models.task import create_task
from utils.file_handler import load_tasks, save_tasks
from datetime import datetime

def validate_due_date(due_date: str | None) -> str | None:
    if not due_date:
        return None

    try:
        datetime.strptime(due_date, "%Y-%m-%d")
    except ValueError:
        raise ValueError("Invalid due date format. Use YYYY-MM-DD.")

    return due_date

def normalize_priority(priority: str) -> str:
    key = priority.strip().lower()
    if key not in ALLOWED_PRIORITIES:
        raise ValueError("Invalid priority. Choose one of: Low, Medium, High.")
    return ALLOWED_PRIORITIES[key]

def next_task_id(tasks: list[dict]) -> int:
    ids = []
    
    for task in tasks:
        try:
            ids.append(int(task.get("id", 0)))
        except (TypeError, ValueError):
            continue
    return (max(ids) if ids else 0) + 1

def add_task(title, description, due_date, priority):
    tasks = load_tasks()

    print("tasks type:", type(tasks))
    if isinstance(tasks, dict):
        for i, item in enumerate(tasks):
            if callable(item):
                print("BAD ITEM at index:", i, item, type(item))
            elif isinstance(item, dict):
                for k, v in item.items():
                    if callable(v):
                        print("BAD VALUE in task:", i, "key", k, v, type(v))

    normalized_title = title.strip()
    if not normalized_title:
        raise ValueError("Title cannot be empty")
    
    task = create_task(
        task_id = next_task_id(tasks),
        title = normalized_title,
        description = description,
        priority = normalize_priority(priority),
        due_date = validate_due_date(due_date)
    )

    tasks.append(task)

    # Debugging: find non-JSON-serializable values (functions/methods)
    for k, v in task.items():
        if callable(v):
            print("CALLABLE FOUND:", k, v, type(v))
    print(task)

    save_tasks(tasks)

    return task

def list_tasks():
    return load_tasks()

def complete_task(task_id: int):
    tasks = load_tasks()

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
            save_tasks(tasks)
            return "completed"
    return "not_found"

def delete_task(task_id: int):
    tasks = load_tasks()

    for i, task in enumerate(tasks):
        try:
            current_id = int(task.get("id"))
        except (TypeError, ValueError):
            continue

        if current_id == task_id:
            del tasks[i]
            save_tasks(tasks)
            return True
        
    return False
