from config import DATA_FILE
from controllers.cli_controller import create_app
from controllers.task_controller import TaskController
from models.task_manager import TaskManager
from utils.file_handler import TaskFileRepo

repo = TaskFileRepo(DATA_FILE)
task_manager = TaskManager(repo)
task_controller = TaskController(task_manager)
app = create_app(task_controller)

if __name__ == "__main__":
    app()