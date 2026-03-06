from models.task_manager import TaskManager
from utils.file_handler import TaskFileRepo
from config import DATA_FILE

task_manager = TaskManager(TaskFileRepo(DATA_FILE))


def add_task(title, description, due_date, priority):
    return task_manager.add_task(title, description, due_date, priority)


def list_tasks():
    return task_manager.list_tasks()


def get_task(task_id):
    return task_manager.get_task(task_id)


def complete_task(task_id):
    return task_manager.complete_task(task_id)


def delete_task(task_id):
    return task_manager.delete_task(task_id)
