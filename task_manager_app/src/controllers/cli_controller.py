import typer
from controllers.task_controller import TaskController
from views import cli_view

def create_app(task_controller: TaskController) -> typer.Typer:
    app = typer.Typer(no_args_is_help=True, help="Task Manager CLI")

    @app.command("add")
    def add_task(
        title: str = typer.Argument(..., help="Task title."),
        description: str = typer.Option("", "--description", "-d", help="Task details."),
        due_date: str | None = typer.Option(
            None, 
            "--due-date", 
            "-u" , 
            help="Optional due date in YYYY-MM-DD format."
        ),
        priority: str = typer.Option(
            "Medium", 
            "--priority", 
            "-p", 
            help="Priority: Low, Medium, or High."
        ),
        ) -> None:
            try:
                task = task_controller.add_task(title, description, due_date, priority)
                cli_view.success(f"Added task #{task.task_id}: {task.title}")
            except ValueError as e:
                cli_view.error(str(e))
                raise typer.Exit(code=1)

    @app.command("list")
    def list_tasks() -> None:
        tasks = task_controller.list_tasks()
        cli_view.print_tasks_table(tasks)

    @app.command("complete")
    def complete_task(
        task_id: int = typer.Argument(..., help="Task id to mark as complete.")
    ) -> None:
        result = task_controller.complete_task(task_id)

        if result == "completed":
            cli_view.success(f"Marked task #{task_id} as complete.")
        elif result == "already_complete":
            cli_view.info(f"Task #{task_id} is already complete.")
        else:
            cli_view.error(f"Task #{task_id} was not found.")
            raise typer.Exit(code=1)

    @app.command("delete")
    def delete_task(
        task_id: int = typer.Argument(..., help="Task id to delete.")
    ) -> None:
        if task_controller.delete_task(task_id):
            cli_view.success(f"Deleted task #{task_id}.")
        else:
            cli_view.error(f"Task #{task_id} was not found.")
            raise typer.Exit(code=1)
    return app