"""
Singleton configuration and shared helpers for the todos application.

Centralises:
  - ``PRIORITY_ORDER`` — the sort-weight mapping for task priority levels
    (was copy-pasted inline inside task_list_page_context on every request).
  - ``db_error_response()`` — a single factory for the repeated
    ``HttpResponse("A database error occurred…", status=500)`` pattern that
    appeared ~6 times across task_view.py.
"""

from django.http import HttpResponse, JsonResponse

from .models import Task


class TaskConfig:
    """Singleton that holds application-wide constants and shared helpers.

    Usage::

        cfg = TaskConfig()
        order = cfg.PRIORITY_ORDER          # smell #1 fix
        resp  = cfg.db_error_response(msg)  # smell #3 fix
    """

    _instance: "TaskConfig | None" = None

    def __new__(cls) -> "TaskConfig":
        if cls._instance is None:
            instance = super().__new__(cls)
            instance._priority_order = {
                Task.Priority.HIGH: 0,
                Task.Priority.MEDIUM: 1,
                Task.Priority.LOW: 2,
            }
            cls._instance = instance
        return cls._instance

    @property
    def PRIORITY_ORDER(self) -> dict:
        """Mapping of :class:`Task.Priority` → sort weight (lower = higher priority)."""
        return self._priority_order

    @staticmethod
    def db_error_response(action: str = "processing your request") -> HttpResponse:
        """Return a consistent 500 response for unexpected database failures.

        Args:
            action: Short description of the operation that failed, e.g.
                    ``"creating the task"`` or ``"deleting the task"``.

        Returns:
            An :class:`~django.http.HttpResponse` with status 500.
        """
        return HttpResponse(
            f"A database error occurred while {action}. Please try again later.",
            status=500,
        )

    @staticmethod
    def db_json_error_response(action: str = "processing your request") -> JsonResponse:
        """Return a consistent JSON 500 response for API/JSON endpoints.

        Args:
            action: Short description of the failing operation.

        Returns:
            A :class:`~django.http.JsonResponse` with status 500.
        """
        return JsonResponse(
            {"error": f"A database error occurred while {action}. Please try again later."},
            status=500,
        )

