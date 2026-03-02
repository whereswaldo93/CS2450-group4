import typer

def success(message: str):
    typer.secho(message, fg=typer.colors.GREEN)

def error(message: str):
    typer.secho(message, fg=typer.colors.RED)

def info(message: str):
    typer.secho(message)    

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