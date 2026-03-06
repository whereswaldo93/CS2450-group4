from models import task_manager


def add_task(title, description, due_date, priority):
    return task_manager.add_task(title, description, due_date, priority)


def list_tasks():
    return task_manager.list_tasks()


def complete_task(task_id):
    return task_manager.complete_task(task_id)


def delete_task(task_id):
    return task_manager.delete_task(task_id)
