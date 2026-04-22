from datetime import date
from typing import Any
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_http_methods
from ..models import Task
from ..app_logger import AppLogger          # Smell #5 fix: singleton logger
from ..task_config import TaskConfig        # Smell #1 & #3 fix: singleton config
from ..date_parser import DateParser        # Smell #2 fix: singleton date parser

# Obtain module logger through the singleton — consistent naming guaranteed.
logger = AppLogger.get_logger(__name__)

# Singleton accessors (one instance shared across the entire process).
_cfg = TaskConfig()
_date_parser = DateParser()


def _count_overdue(tasks: list) -> int:
    today = date.today()
    logger.debug("Checking for overdue tasks relative to today's date %s", today)
    n = 0
    for t in tasks:
        if t.status != Task.Status.PENDING or not t.due_date:
            continue
        if t.due_date < today:
            n += 1
    logger.debug("Found %s overdue tasks out of %s total", n, len(tasks))
    return n


def _summary_stats(tasks: list) -> dict:
    logger.debug("Summary of stats is %s tasks", len(tasks))
    stats = {
        "total": len(tasks),
        "pending": sum(1 for t in tasks if t.status == Task.Status.PENDING),
        "completed": sum(1 for t in tasks if t.status == Task.Status.COMPLETED),
        "overdue": _count_overdue(tasks),
    }
    logger.debug("Stats calculated: %s", stats)
    return stats


def task_list_page_context(request: HttpRequest) -> dict[str, Any | list[Task] | int | str | None]:
    logger.debug("Querying database for task list for user %s", request.user.id)
    qs = Task.objects.filter(user=request.user)  # pylint: disable=no-member
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

    logger.debug(
        "Applied filters for task list retrieval for user %s: status=%s, priority=%s",
        request.user.id, filter_status, filter_priority,
    )

    sort_by = request.GET.get("sort", "id")

    # Smell #1 fix: use the singleton PRIORITY_ORDER instead of an inline dict.
    if sort_by == "priority":
        tasks = sorted(tasks, key=lambda t: _cfg.PRIORITY_ORDER.get(t.priority, 99))
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


@login_required
def hello_html_view(request: HttpRequest) -> HttpResponse:
    logger.debug("User %s accessing hello page", request.user.id)
    return render(request, "todos/hello.html", task_list_page_context(request))


@login_required
def task_list(request: HttpRequest) -> HttpResponse:
    logger.debug("User %s accessing task list page", request.user.id)
    return render(request, "todos/tasks_list.html", task_list_page_context(request))


@login_required
def add_task(request: HttpRequest) -> HttpResponse:
    logger.debug("User %s accessing add task page", request.user.id)

    if request.method == "POST":
        logger.debug("POST data received for new task: %s", request.POST.dict())

        title = (request.POST.get("title") or "").strip()
        description = (request.POST.get("description") or "").strip()
        priority = (request.POST.get("priority") or "Medium").strip()
        due_date_raw = (request.POST.get("due_date") or "").strip() or None
        notes = (request.POST.get("notes") or "").strip() or None
        errors = {}

        if not title:
            errors["title"] = "Title is required."

        # Smell #2 fix: delegate date parsing to the singleton DateParser.
        due_date, date_error = _date_parser.parse(due_date_raw)
        if date_error:
            logger.warning("Invalid date format submitted: %s", due_date_raw)
            errors["due_date"] = date_error
        elif due_date is not None and due_date < date.today():
            logger.warning("Attempted to submit due date in the past: %s", due_date)
            errors["due_date"] = "Due date cannot be in the past."

        if errors:
            logger.warning("Task creation validation failed for user %s: %s", request.user.id, errors)
            return render(request, "todos/add_task.html", {
                "errors": errors,
                "title": request.POST.get("title"),
                "description": request.POST.get("description"),
                "priority": priority,
                "due_date": request.POST.get("due_date"),
                "notes": notes,
            })

        try:
            task = Task.objects.create(  # pylint: disable=no-member
                user=request.user,
                title=title,
                description=description,
                priority=priority,
                due_date=due_date,
                status=Task.Status.PENDING,
                notes=notes,
            )
            logger.info("Task '%s' with ID %d, created successfully for user %s", task.title, task.id, request.user.id)
            return redirect("task_list")
        except Exception as e:
            logger.error("System failure during task creation for user %s: %s", request.user.id, str(e), exc_info=True)
            # Smell #3 fix: use the singleton helper instead of a raw HttpResponse literal.
            return _cfg.db_error_response("creating the task")

    return render(request, "todos/add_task.html", {
        "errors": {}, "title": "", "description": "", "priority": "Medium", "due_date": "", "notes": "",
    })


@login_required
@require_http_methods(["POST"])
def toggle_task(request: HttpRequest, task_id: int) -> HttpResponse:
    logger.debug("Toggle request received for task id %s by user %s", task_id, request.user.id)
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    old_status = task.status

    task.status = Task.Status.COMPLETED if task.status == Task.Status.PENDING else Task.Status.PENDING

    try:
        task.save(update_fields=["status"])
        logger.info("Task %s status changed from %s to %s by user %s", task.id, old_status, task.status, request.user.id)
        return redirect("task_list")
    except Exception as e:
        logger.error("Failed to toggle status for task %s:: %s", task_id, str(e), exc_info=True)
        # Smell #3 fix: use the singleton helper.
        return _cfg.db_error_response("updating the task status")


@login_required
def edit_task(request: HttpRequest, task_id: int) -> HttpResponse:
    logger.debug("User %s attempting to edit task %s", request.user.id, task_id)
    task = get_object_or_404(Task, pk=task_id, user=request.user)

    if request.method == "POST":
        logger.debug("POST data received for task %s: %s", task_id, request.POST.dict())

        title = (request.POST.get("title") or "").strip()
        description = (request.POST.get("description") or "").strip()
        priority = (request.POST.get("priority") or "Medium").strip()
        due_date_str = (request.POST.get("due_date") or "").strip() or None
        notes = (request.POST.get("notes") or "").strip() or None

        errors = {}
        if not title:
            errors["title"] = "Title is required."

        if errors:
            logger.warning("Task update validation failed for task %s by user %s: %s", task_id, request.user.id, errors)
            return render(request, "todos/edit_task.html", {
                "errors": errors, "task": task, "title": title,
                "description": description, "priority": priority, "due_date": due_date_str, "notes": notes,
            })

        # Smell #2 fix: delegate date parsing to the singleton DateParser.
        due_date, date_error = _date_parser.parse(due_date_str)
        if date_error:
            logger.warning("Invalid due date format for task %s: %s", task_id, due_date_str)
            errors["due_date"] = date_error
            return render(request, "todos/edit_task.html", {
                "errors": errors, "task": task, "title": title,
                "description": description, "priority": priority, "due_date": due_date_str, "notes": notes,
            })

        try:
            task.title = title
            task.description = description
            task.priority = priority
            task.due_date = due_date
            task.notes = notes
            task.save()
            logger.info("Task %s ('%s') successfully updated by user %s", task.id, task.title, request.user.id)
            return redirect("task_list")
        except Exception as e:
            logger.error("Failed to update task %s in database: %s", task_id, str(e))
            # Smell #3 fix: use the singleton helper.
            return _cfg.db_error_response("updating the task")

    return render(request, "todos/edit_task.html", {
        "errors": {}, "task": task, "title": task.title, "description": task.description,
        "priority": task.priority, "due_date": task.due_date.isoformat() if task.due_date else "",
        "notes": task.notes or "",
    })


@login_required
def delete_task(request: HttpRequest, task_id: int) -> HttpResponse:
    logger.debug("User %s attempting to delete task %s", request.user.id, task_id)
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    task_title = task.title

    try:
        task.delete()
        logger.info("Tasks %s with ID %s deleted by user %s", task_title, task_id, request.user.id)
        return redirect("task_list")
    except Exception as e:
        logger.error(
            "Failed to delete task %s with ID %s for user %s with the following error: %s",
            task_title, task_id, request.user.id, str(e), exc_info=True,
        )
        # Smell #3 fix: use the singleton helper.
        return _cfg.db_error_response("deleting the task")


@login_required
def complete_task(request: HttpRequest, task_id: int) -> HttpResponse:
    logger.debug("User %s attempting to mark task %s as completed", request.user.id, task_id)
    task = get_object_or_404(Task, pk=task_id, user=request.user)

    if task.status == Task.Status.COMPLETED:
        logger.warning("User %s attempted to mark task %s as completed, but it is already completed.", request.user.id, task_id)
        return redirect("task_list")

    try:
        task.status = Task.Status.COMPLETED
        task.save(update_fields=["status"])
        logger.info("Task %s with ID %s marked as completed by user %s", task.id, task.title, request.user.id)
        return redirect("task_list")
    except Exception as e:
        logger.error("Failed to mark task %s with ID %s as completed for user %s: %s", task.title, task_id, request.user.id, str(e), exc_info=True)
        # Smell #3 fix: use the singleton helper.
        return _cfg.db_error_response("updating the task status")


@login_required
def task_stats(request: HttpRequest) -> JsonResponse:
    logger.debug("User %s accessing task stats endpoint", request.user.id)

    try:
        tasks = list(Task.objects.filter(user=request.user).order_by("-id"))  # pylint: disable=no-member
        total = len(tasks)
        pending = sum(1 for t in tasks if t.status == Task.Status.PENDING)
        completed = sum(1 for t in tasks if t.status == Task.Status.COMPLETED)
        logger.info("Task stats retrieved successfully for user %s: total=%d, pending=%d, completed=%d", request.user.id, total, pending, completed)
        return JsonResponse({"total": total, "pending": pending, "completed": completed})
    except Exception as e:
        logger.error("Failed to retrieve task stats for user %s: %s", request.user.id, str(e), exc_info=True)
        return _cfg.db_json_error_response("retrieving task stats")


@login_required
def note_create(request: HttpRequest, task_id: int) -> HttpResponse:
    logger.debug("User %s accessing note creation for task %s", request.user.id, task_id)
    task = get_object_or_404(Task, pk=task_id, user=request.user)

    if request.method == "POST":
        logger.debug("POST data received for note creation for task %s: %s", task_id, request.POST.dict())
        notes = request.POST.get("notes", "").strip()

        if notes:
            try:
                task.notes = notes
                task.save(update_fields=["notes"])
                logger.info("Note for task %s with ID %s updated successfully by user %s", task.title, task_id, request.user.id)
                return redirect("task_list")
            except Exception as e:
                logger.error("Database failure while saving note for task %s with ID %s for user %s: %s", task.title, task_id, request.user.id, str(e), exc_info=True)
                # Smell #3 fix: use the singleton helper.
                return _cfg.db_error_response("creating the note")
        logger.debug("Empty note content submitted for task %s with ID %s by user %s.", task.title, task_id, request.user.id)

    return render(request, "todos/note_list.html", {"task": task})
