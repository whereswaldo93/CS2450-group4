import json
from config import DATA_FILE

def load_tasks() -> list[dict]:
    if not DATA_FILE.exists() or DATA_FILE.stat().st_size == 0:
        return []

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, list):
        raise ValueError(f"Invalid task file format in {DATA_FILE}. Expected a JSON array.")

    return data

def save_tasks(tasks: list[dict]) -> None:
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(tasks, f, indent=2)