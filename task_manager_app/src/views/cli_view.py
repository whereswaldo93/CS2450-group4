import typer
from models.task import Task

def success(message: str) -> None:
    typer.secho(message, fg=typer.colors.GREEN)

def error(message: str) -> None:
    typer.secho(message, fg=typer.colors.RED)

def info(message: str) -> None:
    typer.secho(message)    

def print_tasks_table(tasks: list[Task]) -> None:
    if not tasks:
        typer.echo("\n(No tasks found)\n")
        return

    columns = [
        ("ID", lambda t: str(t.task_id)),
        ("Title", lambda t: t.title),
        ("Description", lambda t: t.description or ""),
        ("Status", lambda t: t.status.value or ""),
        ("Due Date", lambda t: t.due_date or ""),
        ("Priority", lambda t: t.priority.value or ""),
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