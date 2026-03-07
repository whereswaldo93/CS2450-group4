from config import DATA_FILE
from controllers.task_controller import TaskController
from controllers.gui_controller import GUIController
from models.task_manager import TaskManager
from utils.file_handler import TaskFileRepo
from views.gui_view import GUIView

def main() -> None:
    repo = TaskFileRepo(DATA_FILE)
    task_manager = TaskManager(repo)
    task_controller = TaskController(task_manager)
    gui_controller = GUIController(task_controller)
    app = GUIView(gui_controller)
    app.run()

if __name__ == "__main__":
    main()