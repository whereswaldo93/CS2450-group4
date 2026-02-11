import json
from datetime import datetime
from pathlib import Path

import typer

app = typer.Typer(no_args_is_help=True, help="Task Manager CLI")

DATA_FILE = Path(__file__).resolve().parent / "data" / "tasks.json"
ALLOWED_PRIORITIES = {"low": "Low", "medium": "Medium", "high": "High"}


def load_tasks() -> list[dict]:
    if not DATA_FILE.exists() or DATA_FILE.stat().st_size == 0:
        return []

    try:
        raw = DATA_FILE.read_text(encoding="utf-8")
        data = json.loads(raw)
    except json.JSONDecodeError:
        typer.secho(
            f"Could not parse task file: {DATA_FILE}",
            fg=typer.colors.RED,
        )
        raise typer.Exit(code=1)

    if not isinstance(data, list):
        typer.secho(
            f"Invalid task file format in {DATA_FILE}. Expected a JSON array.",
            fg=typer.colors.RED,
        )
        raise typer.Exit(code=1)

    return data


def save_tasks(tasks: list[dict]) -> None:
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    DATA_FILE.write_text(json.dumps(tasks, indent=2), encoding="utf-8")


def validate_due_date(due_date: str | None) -> str | None:
    if not due_date:
        return None

    try:
        datetime.strptime(due_date, "%Y-%m-%d")
    except ValueError:
        typer.secho("Invalid due date. Use YYYY-MM-DD.", fg=typer.colors.RED)
        raise typer.Exit(code=1)

    return due_date


def normalize_priority(priority: str) -> str:
    key = priority.strip().lower()
    if key not in ALLOWED_PRIORITIES:
        typer.secho(
            "Invalid priority. Choose one of: Low, Medium, High.",
            fg=typer.colors.RED,
        )
        raise typer.Exit(code=1)
    return ALLOWED_PRIORITIES[key]


def next_task_id(tasks: list[dict]) -> int:
    ids = []
    for task in tasks:
        try:
            ids.append(int(task.get("id", 0)))
        except (TypeError, ValueError):
            continue
    return (max(ids) if ids else 0) + 1


def print_tasks_table(tasks: list[dict]) -> None:
    if not tasks:
        typer.echo("\n(No tasks found)\n")
        return

    columns = [
        ("ID", lambda t: str(t.get("id", ""))),
        ("Title", lambda t: t.get("title", "")),
        ("Status", lambda t: t.get("status", "")),
        ("Due", lambda t: t.get("due_date", "") or ""),
        ("Priority", lambda t: t.get("priority", "") or ""),
    ]

    widths = []
    for header, getter in columns:
        max_cell = max(len(getter(task)) for task in tasks)
        widths.append(max(len(header), max_cell))

    def format_row(values: list[str]) -> str:
        return " | ".join(value.ljust(width) for value, width in zip(values, widths))

    headers = [header for header, _ in columns]
    typer.echo("\n" + format_row(headers))
    typer.echo("-+-".join("-" * width for width in widths))

    for task in tasks:
        row = [getter(task) for _, getter in columns]
        typer.echo(format_row(row))

    typer.echo("")


@app.command("add")
def add_task(
    title: str = typer.Argument(..., help="Task title."),
    description: str = typer.Option("", "--description", "-d", help="Task details."),
    due_date: str | None = typer.Option(
        None, "--due-date", help="Optional due date in YYYY-MM-DD format."
    ),
    priority: str = typer.Option(
        "Medium", "--priority", "-p", help="Priority: Low, Medium, or High."
    ),
) -> None:
    tasks = load_tasks()
    normalized_title = title.strip()
    if not normalized_title:
        typer.secho("Title cannot be empty.", fg=typer.colors.RED)
        raise typer.Exit(code=1)

    now = datetime.now().isoformat(timespec="seconds")
    task = {
        "id": next_task_id(tasks),
        "title": normalized_title,
        "description": description.strip(),
        "status": "Pending",
        "priority": normalize_priority(priority),
        "due_date": validate_due_date(due_date),
        "created_at": now,
        "updated_at": now,
    }
    tasks.append(task)
    save_tasks(tasks)
    typer.secho(f"Added task #{task['id']}: {task['title']}", fg=typer.colors.GREEN)


@app.command("list")
def list_tasks() -> None:
    tasks = load_tasks()
    print_tasks_table(tasks)


@app.command("complete")
def complete_task(
    task_id: int = typer.Argument(..., help="Task id to mark as complete.")
) -> None:
    tasks = load_tasks()

    for task in tasks:
        try:
            current_id = int(task.get("id"))
        except (TypeError, ValueError):
            continue

        if current_id != task_id:
            continue

        if task.get("status") == "Complete":
            typer.echo(f"Task #{task_id} is already complete.")
            return

        task["status"] = "Complete"
        task["updated_at"] = datetime.now().isoformat(timespec="seconds")
        save_tasks(tasks)
        typer.secho(f"Marked task #{task_id} as complete.", fg=typer.colors.GREEN)
        return

    typer.secho(f"Task #{task_id} was not found.", fg=typer.colors.RED)
    raise typer.Exit(code=1)


if __name__ == "__main__":
    app()
