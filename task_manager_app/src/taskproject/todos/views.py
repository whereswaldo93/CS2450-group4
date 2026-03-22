from django.shortcuts import render, redirect
from django.http import HttpResponse
from utils.file_handler import TaskFileRepo
from models.task import Task, TaskStatus
from config import DATA_FILE


def _get_repo() -> TaskFileRepo:
    """Use the same tasks.json path as the CLI (config.DATA_FILE)."""
    return TaskFileRepo(DATA_FILE)


def hello_html_view(request) -> HttpResponse:
    repo = _get_repo()
    tasks = repo.load_tasks()
    return render(request, "todos/hello.html", {"tasks": tasks})


def task_list(request) -> HttpResponse:
    repo = _get_repo()
    tasks = repo.load_tasks()
    return render(request, "todos/tasks_list.html", {"tasks": tasks})


def add_task(request):
    if request.method == "POST":
        title = (request.POST.get("title") or "").strip()
        description = (request.POST.get("description") or "").strip()
        priority = (request.POST.get("priority") or "Medium").strip()
        due_date = (request.POST.get("due_date") or "").strip() or None
        errors = {}
        if not title:
            errors["title"] = "Title is required."
        if errors:
            return render(
                request,
                "todos/add_task.html",
                {
                    "errors": errors,
                    "title": request.POST.get("title"),
                    "description": request.POST.get("description"),
                    "priority": priority,
                    "due_date": request.POST.get("due_date"),
                },
            )
        repo = _get_repo()
        tasks = repo.load_tasks()
        next_id = max((t.task_id for t in tasks), default=0) + 1
        new_task = Task(
            task_id=next_id,
            title=title,
            description=description,
            priority=priority,
            due_date=due_date,
            status=TaskStatus.PENDING,
        )
        tasks.append(new_task)
        repo.save_tasks(tasks)
        return redirect("task_list")
    return render(
        request,
        "todos/add_task.html",
        {
            "errors": {},
            "title": "",
            "description": "",
            "priority": "Medium",
            "due_date": "",
        },
    )


def toggle_task(request, task_id):
    if request.method != "POST":
        return redirect("task_list")
    # TODO: load tasks, toggle status for task_id, save, redirect to task_list
    return redirect("task_list")


def edit_task(request, task_id):
    # TODO: show form to edit task, then save and redirect
    return HttpResponse(f"Edit task {task_id} (to be implemented)")


def delete_task(request, task_id):
    repo = _get_repo()
    tasks = repo.load_tasks()
    for task in tasks:
        if task.task_id == task_id:
            tasks.remove(task)
            break
    repo.save_tasks(tasks)
    return redirect("task_list")


def complete_task(request, task_id):
    repo = _get_repo()
    tasks = repo.load_tasks()
    for task in tasks:
        if task.task_id == task_id:
            task.status = TaskStatus.COMPLETED
            break
    repo.save_tasks(tasks)
    return redirect("task_list")
