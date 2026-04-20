import json
from json import JSONDecodeError
from pathlib import Path
from taskproject.todos.file_task import Task

class TaskFileRepo:
    def __init__(self, path: Path) -> None:
        self.path = path

    def load_tasks(self) -> list[Task]:
        if not self.path.exists() or self.path.stat().st_size == 0:
            return []

        try:
            with open(self.path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except JSONDecodeError as e:
            raise ValueError(f"Error decoding JSON from {self.path}: {e}") from e

        if not isinstance(data, list):
            raise ValueError(
                f"Expected a list of tasks in {self.path}, but got {type(data).__name__}"
            )
            
        return [Task.from_dict(item) for item in data]

    def save_tasks(self, tasks: list[Task]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump([task.to_dict() for task in tasks], f, indent=2)

# ---------------------------------------------------------------------------
# Smell #4 fix: enforce singleton — import and re-export the singleton class
# so existing callers can switch to TaskFileRepoSingleton with minimal churn.
# ---------------------------------------------------------------------------
from utils.task_file_repo_singleton import TaskFileRepoSingleton  # noqa: E402
