from django.shortcuts import render, redirect
from django.http import HttpResponse
from utils.file_handler import TaskFileRepo
from models.task import Task, TaskStatus, TaskPriority
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

    #filter the tasks
    filter_status = request.GET.get("status", "all")
    filter_priority = request.GET.get("priority", "all")

    if filter_status == "pending":
        tasks = [task for task in tasks if task.status == TaskStatus.PENDING]
    elif filter_status == "completed":
        tasks = [task for task in tasks if task.status == TaskStatus.COMPLETED]
    
    if (filter_priority == "Low"):
        tasks = [task for task in tasks if task.priority.value == "Low"]
    elif (filter_priority == "Medium"):
        tasks = [task for task in tasks if task.priority.value == "Medium"] 
    elif (filter_priority == "High"):
        tasks = [task for task in tasks if task.priority.value == "High"]

    #Sorting the tasks
    sort_by = request.GET.get("sort", "id")
    priority_order = {"High": 0, "Medium": 1, "Low": 2}

    if sort_by == "priority":
        tasks = sorted(tasks, key=lambda t: priority_order.get(t.priority.value, 99))
    elif sort_by == "due_date":
        tasks = sorted(tasks, key=lambda t: (t.due_date is None, t.due_date or ""))
    elif sort_by == "title":
        tasks = sorted(tasks, key=lambda t: t.title.lower())
    return render(request, "todos/tasks_list.html", {"tasks": tasks, "filter_status": filter_status, "filter_priority": filter_priority, "sort_by": sort_by})


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
    repo = _get_repo()
    tasks = repo.load_tasks()

    for task in tasks:
        if task.task_id == task_id:
            if task.status == TaskStatus.PENDING:
                task.status = TaskStatus.COMPLETED
            break
    repo.save_tasks(tasks)
    return redirect("task_list")


def edit_task(request, task_id):
    repo = _get_repo()
    tasks = repo.load_tasks()

    task = next((task for task in tasks if task.task_id == task_id), None)
    
    #task not found
    if task is None:
        return redirect("task_list")
    
    #post function
    if request.method == "POST":
        title = (request.POST.get("title") or "").strip()
        description = (request.POST.get("description") or "").strip()
        priority = (request.POST.get("priority")or "Medium").strip()
        due_date = (request.POST.get("due_date") or "").strip() or None

        errors = {}
        if not title:
            errors["Title"] = "Title is required."
        
        if errors:
            return render(request, "todos/edit_task.html", {"errors": errors, "task": task, "title": title, "description": description, "priority": priority, "due_date": due_date})
        
        task.title = title
        task.description = description
        task.priority = TaskPriority.from_value(priority)
        task.due_date = due_date
        
        repo.save_tasks(tasks)
        return redirect("task_list")
    return render(request, "todos/edit_task.html", {"errors": {}, "task": task, "title": task.title, "description": task.description, "priority": task.priority.value, "due_date": task.due_date or "",},)


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
