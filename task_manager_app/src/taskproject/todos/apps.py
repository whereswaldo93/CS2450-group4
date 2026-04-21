import os
from django.apps import AppConfig
from django.conf import settings
import logging
import atexit

logger = logging.getLogger("taskproject")

class TodosConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "todos"

    def ready(self):
        # The absoulte path to the database file
        db_path = os.path.join(settings.BASE_DIR, "db.sqlite3")

        # System-wide failure
        if not os.path.exists(db_path):
            logger.critical(f"Database `{db_path}` not found! Please run 'py manage.py migrate' to set up the database.")
        else:
            # Application startup
            logger.info("Task Manager application startup initiated. Application is ready and loaded.")
        atexit.register(self.on_shutdown)

    def on_shutdown(self):
        # Log a message when the app is shutting down
        logger.info("Task Manager is shutting down.")