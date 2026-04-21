import os
from django.apps import AppConfig
import logging
import atexit

logger = logging.getLogger("todos")

class TodosConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "todos"

    def ready(self):
        # System-wide failure
        if not os.path.exists("db.sqlite3"):
            logger.critical("Database `db.sqlite3` not found! Please run 'py manage.py migrate' to set up the database.")
        else:
            # Application startup
            logger.info("Task Manager application startup initiated. Application is ready and loaded.")
        atexit.register(self.on_shutdown)

    def on_shutdown(self):
        # Log a message when the app is shutting down
        logger.info("Task Manager is shutting down.")