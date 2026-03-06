import json
<<<<<<< HEAD
from json import JSONDecodeError
from pathlib import Path

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
            raise ValueError(f"Expected a list of tasks in {self.path}, but got {type(data).__name__}")

        return data

    def save_tasks(self, tasks: list[dict]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(tasks, f, indent=2)

default_repo = TaskFileRepo(DATA_FILE)

def load_tasks() -> list[dict]:
<<<<<<< HEAD
    return default_repo.load_tasks()

def save_tasks(tasks: list[dict]) -> None:
    return default_repo.save_tasks(tasks)
=======
    if not DATA_FILE.exists() or DATA_FILE.stat().st_size == 0:
        return []

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    except JSONDecodeError:
        return []

    if not isinstance(data, list):
        raise ValueError(f"Invalid task file format in {DATA_FILE}. Expected a JSON array.")

    return data

def save_tasks(tasks: list[dict]) -> None:
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(tasks, f, indent=2)
>>>>>>> a170ec02c9e7df3b770643d231a4d766dbdbc343
