import json
from json import JSONDecodeError
from pathlib import Path
from config import DATA_FILE


class TaskFileRepo:
    def __init__(self, path: Path):
        self.path = path

    def load_tasks(self) -> list[dict]:
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

        return data

    def save_tasks(self, tasks: list[dict]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(tasks, f, indent=2)
