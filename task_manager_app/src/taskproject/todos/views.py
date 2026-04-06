from datetime import date, datetime

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods

from .models import Task


def _count_overdue(tasks: list) -> int:
    today = date.today()
    n = 0
    for t in tasks:
        if t.status != Task.Status.PENDING or not t.due_date:
            continue
        if t.due_date < today:
            n += 1
    return n


def _summary_stats(tasks: list) -> dict:
    return {
        "total": len(tasks),
        "pending": sum(1 for t in tasks if t.status == Task.Status.PENDING),
        "completed": sum(1 for t in tasks if t.status == Task.Status.COMPLETED),
        "overdue": _count_overdue(tasks),
    }


def _task_list_page_context(request) -> dict:
    qs = Task.objects.filter(user=request.user)
    tasks = list(qs)
    stats = _summary_stats(tasks)

    filter_status = request.GET.get("status", "all")
    filter_priority = request.GET.get("priority", "all")

    if filter_status == "pending":
        tasks = [t for t in tasks if t.status == Task.Status.PENDING]
    elif filter_status == "completed":
        tasks = [t for t in tasks if t.status == Task.Status.COMPLETED]

    if filter_priority == "Low":
        tasks = [t for t in tasks if t.priority == Task.Priority.LOW]
    elif filter_priority == "Medium":
        tasks = [t for t in tasks if t.priority == Task.Priority.MEDIUM]
    elif filter_priority == "High":
        tasks = [t for t in tasks if t.priority == Task.Priority.HIGH]

    sort_by = request.GET.get("sort", "id")
    priority_order = {
        Task.Priority.HIGH: 0,
        Task.Priority.MEDIUM: 1,
        Task.Priority.LOW: 2,
    }

    if sort_by == "priority":
        tasks = sorted(tasks, key=lambda t: priority_order.get(t.priority, 99))
    elif sort_by == "due_date":
        tasks = sorted(tasks, key=lambda t: (t.due_date is None, t.due_date or date.min))
    elif sort_by == "title":
        tasks = sorted(tasks, key=lambda t: t.title.lower())
    else:
        tasks = sorted(tasks, key=lambda t: t.pk, reverse=True)

    return {
        "tasks": tasks,
        "filter_status": filter_status,
        "filter_priority": filter_priority,
        "sort_by": sort_by,
        **stats,
    }


def signup_view(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
        return redirect("task_list")
    if request.method == "POST":
        username = (request.POST.get("username") or "").strip()
        password1 = request.POST.get("password1") or ""
        password2 = request.POST.get("password2") or ""
        errors: list[str] = []
        if not username:
            errors.append("Username is required.")
        if not password1:
            errors.append("Password is required.")
        elif password1 != password2:
            errors.append("Passwords do not match.")
        else:
            try:
                validate_password(password1, User(username=username))
            except ValidationError as e:
                errors.extend(e.messages)
        if User.objects.filter(username=username).exists():
            errors.append("That username is already taken.")
        if errors:
            return render(
                request,
                "todos/signup.html",
                {"errors": errors, "username": username},
            )
        user = User.objects.create_user(username=username, password=password1)
        login(request, user)
        return redirect("task_list")
    return render(request, "todos/signup.html", {"errors": [], "username": ""})


def login_view(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
        return redirect("task_list")
    if request.method == "POST":
        username = (request.POST.get("username") or "").strip()
        password = request.POST.get("password") or ""
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("task_list")
        messages.error(request, "Invalid username or password.")
    return render(request, "todos/login.html")


@login_required
def hello_html_view(request) -> HttpResponse:
    return render(request, "todos/hello.html", _task_list_page_context(request))


@login_required
def task_list(request) -> HttpResponse:
    return render(request, "todos/tasks_list.html", _task_list_page_context(request))


@login_required
def add_task(request):
    if request.method == "POST":
        title = (request.POST.get("title") or "").strip()
        description = (request.POST.get("description") or "").strip()
        priority = (request.POST.get("priority") or "Medium").strip()
        due_date_raw = (request.POST.get("due_date") or "").strip() or None
        notes = (request.POST.get("notes") or "").strip() or None
        errors = {}

        if not title:
            errors["title"] = "Title is required."

        due_date = None
        if due_date_raw:
            try:
                due_date = datetime.strptime(due_date_raw, "%Y-%m-%d").date()
            except ValueError:
                errors["due_date"] = "Invalid date format. Use YYYY-MM-DD."
            if due_date is not None and due_date < date.today():
                errors["due_date"] = "Due date cannot be in the past."

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
                    "notes": notes,
                },
            )

        Task.objects.create(
            user=request.user,
            title=title,
            description=description,
            priority=priority,
            due_date=due_date,
            status=Task.Status.PENDING,
            notes=notes,
        )
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
            "notes": "",
        },
    )


@login_required
@require_http_methods(["POST"])
def toggle_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if task.status == Task.Status.PENDING:
        task.status = Task.Status.COMPLETED
    else:
        task.status = Task.Status.PENDING
    task.save(update_fields=["status"])
    return redirect("task_list")


@login_required
def edit_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)

    if request.method == "POST":
        title = (request.POST.get("title") or "").strip()
        description = (request.POST.get("description") or "").strip()
        priority = (request.POST.get("priority") or "Medium").strip()
        due_date_str = (request.POST.get("due_date") or "").strip() or None
        notes = (request.POST.get("notes") or "").strip() or None

        errors = {}
        if not title:
            errors["title"] = "Title is required."

        if errors:
            return render(
                request,
                "todos/edit_task.html",
                {
                    "errors": errors,
                    "task": task,
                    "title": title,
                    "description": description,
                    "priority": priority,
                    "due_date": due_date_str,
                    "notes": notes,
                },
            )

        due_date = None
        if due_date_str:
            try:
                due_date = datetime.strptime(due_date_str, "%Y-%m-%d").date()
            except ValueError:
                errors["due_date"] = "Invalid date format. Use YYYY-MM-DD."
                return render(
                    request,
                    "todos/edit_task.html",
                    {
                        "errors": errors,
                        "task": task,
                        "title": title,
                        "description": description,
                        "priority": priority,
                        "due_date": due_date_str,
                        "notes": notes,
                    },
                )

        task.title = title
        task.description = description
        task.priority = priority
        task.due_date = due_date
        task.notes = notes
        task.save()
        return redirect("task_list")
    return render(
        request,
        "todos/edit_task.html",
        {
            "errors": {},
            "task": task,
            "title": task.title,
            "description": task.description,
            "priority": task.priority,
            "due_date": task.due_date.isoformat() if task.due_date else "",
            "notes": task.notes or "",
        },
    )


@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    task.delete()
    return redirect("task_list")


@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    task.status = Task.Status.COMPLETED
    task.save(update_fields=["status"])
    return redirect("task_list")


@login_required
def task_stats(request):
    tasks = list(Task.objects.filter(user=request.user))
    total = len(tasks)
    pending = sum(1 for t in tasks if t.status == Task.Status.PENDING)
    completed = sum(1 for t in tasks if t.status == Task.Status.COMPLETED)
    return JsonResponse(
        {
            "total": total,
            "pending": pending,
            "completed": completed,
        }
    )


@login_required
def note_create(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)

    if request.method == "POST":
        notes = request.POST.get("notes", "").strip()
        if notes:
            task.notes = notes
            task.save(update_fields=["notes"])
            return redirect("task_list")
    return render(request, "todos/note_list.html", {"task": task})
