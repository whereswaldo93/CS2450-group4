"""
Singleton logger for the todos app.

All modules should obtain a logger via AppLogger.get_logger() instead of
calling logging.getLogger() directly.  This ensures every logger in the
application shares the same root name ("todos") and is created exactly once,
eliminating the divergent naming ("todos" vs "taskproject.todos") that existed
across modules.
"""

import logging


class AppLogger:
    """Singleton that provides a shared root logger for the todos application.

    Usage::

        logger = AppLogger.get_logger(__name__)
    """

    _instance: "AppLogger | None" = None
    _root_name: str = "taskproject"

    def __new__(cls) -> "AppLogger":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @classmethod
    def get_logger(cls, name: str = "") -> logging.Logger:
        """Return a logger whose name is rooted under the shared namespace.

        Args:
            name: Typically ``__name__`` of the calling module.  If empty,
                  the root app logger is returned.

        Returns:
            A :class:`logging.Logger` instance.
        """
        # Ensure we always use the singleton instance (creates it if needed).
        cls()

        if not name or name == cls._root_name:
            return logging.getLogger(cls._root_name)

        # Strip any existing "todos" or "taskproject.todos" prefix so callers
        # using __name__ always end up under the canonical root.
        for prefix in (cls._root_name + ".", "taskproject.todos.", "taskproject."):
            if name.startswith(prefix):
                name = name[len(prefix):]
                break

        return logging.getLogger(f"{cls._root_name}.{name}")
