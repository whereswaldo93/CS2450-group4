import os
from django.apps import AppConfig
import atexit

from todos.app_logger import AppLogger  # noqa: E402  (imported after AppConfig to avoid early Django setup)

logger = AppLogger.get_logger(__name__)


class TodosConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "todos"

    def ready(self):
        # Log a message when the app is ready to confirm it's loaded
        if not os.path.exists("db.sqlite3"):
            logger.critical("Database not found! Please run 'py manage.py migrate' to set up the database.")
        else:
            logger.info("Task Manager application startup initiated. Application is ready and loaded.")

        atexit.register(self.on_shutdown)

    def on_shutdown(self):
        # Log a message when the app is shutting down
        logger.info("Task Manager is shutting down.")
