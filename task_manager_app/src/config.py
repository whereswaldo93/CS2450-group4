from pathlib import Path

DATA_FILE = Path(__file__).resolve().parent / "data" / "tasks.json"

ALLOWED_PRIORITIES = {
    "low": "Low", 
    "medium": "Medium", 
    "high": "High"
    }