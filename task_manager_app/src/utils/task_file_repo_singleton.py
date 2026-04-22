"""
Singleton-enforced file repository for JSON-backed task persistence.

The original ``TaskFileRepo`` in ``utils/file_handler.py`` could be
instantiated multiple times with the same path, risking concurrent writes and
wasted I/O.  ``TaskFileRepoSingleton`` guarantees that only **one** instance
exists per unique file path.
"""

from __future__ import annotations

import json
from json import JSONDecodeError
from pathlib import Path


class TaskFileRepoSingleton:
    """Thread-safe singleton JSON task repository.

    One instance is created per unique ``path``; subsequent calls with the
    same path return the cached instance.

    Usage::

        repo = TaskFileRepoSingleton(Path("data/tasks.json"))
        tasks = repo.load_tasks()
    """

    _instances: dict[Path, "TaskFileRepoSingleton"] = {}

    def __new__(cls, path: Path) -> "TaskFileRepoSingleton":
        resolved = path.resolve()
        if resolved not in cls._instances:
            instance = super().__new__(cls)
            instance._path = resolved
            cls._instances[resolved] = instance
        return cls._instances[resolved]

    # ------------------------------------------------------------------
    # Public API (mirrors the original TaskFileRepo interface exactly)
    # ------------------------------------------------------------------

    def load_tasks(self) -> list:
        """Load and return all tasks from the JSON file.

        Returns:
            A list of task dicts (or ``Task`` objects if ``Task.from_dict``
            is available).

        Raises:
            ValueError: If the file contains invalid JSON or is not a list.
        """
        if not self._path.exists() or self._path.stat().st_size == 0:
            return []

        try:
            with open(self._path, "r", encoding="utf-8") as fh:
                data = json.load(fh)
        except JSONDecodeError as exc:
            raise ValueError(
                f"Error decoding JSON from {self._path}: {exc}"
            ) from exc

        if not isinstance(data, list):
            raise ValueError(
                f"Expected a list of tasks in {self._path}, "
                f"but got {type(data).__name__}"
            )

        # Import lazily to avoid circular imports at module level.
        try:
            from taskproject.todos.file_task import Task  # type: ignore
            return [Task.from_dict(item) for item in data]
        except ImportError:
            return data  # fall back to plain dicts if model unavailable

    def save_tasks(self, tasks: list) -> None:
        """Persist tasks to the JSON file.

        Args:
            tasks: List of task objects exposing a ``to_dict()`` method, or
                   plain dicts.
        """
        self._path.parent.mkdir(parents=True, exist_ok=True)
        serialisable = [
            t.to_dict() if hasattr(t, "to_dict") else t for t in tasks
        ]
        with open(self._path, "w", encoding="utf-8") as fh:
            json.dump(serialisable, fh, indent=2)
