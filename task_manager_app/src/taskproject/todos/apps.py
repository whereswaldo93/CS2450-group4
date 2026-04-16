from django.apps import AppConfig
import logging
import atexit

logger = logging.getLogger("taskproject.todos")

class TodosConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "taskproject.todos"

    def ready(self):
        # Log a message when the app is ready to confirm it's loaded
        logger.info("Task Manager is ready and loaded.")

        atexit.register(self.on_shutdown)

    def on_shutdown(self):
        # Log a message when the app is shutting down
        logger.info("Task Manager is shutting down.")