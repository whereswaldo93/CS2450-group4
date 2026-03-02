from datetime import datetime

def create_task(task_id: int,
                title: str,
                description: str,
                priority: str,
                due_date: str | None) -> dict:
    now = datetime.now().isoformat(timespec="seconds")

    return {
        "id": task_id,
        "title": title.strip(),
        "description": description.strip(),
        "status": "Pending",
        "priority": priority,
        "due_date": due_date,
        "created_at": now,
        "updated_at": now,
    }