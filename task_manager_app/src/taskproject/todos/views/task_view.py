from datetime import datetime, date
from typing import Any
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_http_methods
from ..models import Task
import logging

logger = logging.getLogger("taskproject.todos")

def _count_overdue(tasks: list) -> int:
    """Count overdue tasks for the todo app.

    Args:
        tasks (list): The list of tasks.

    Returns:
        int: The number of overdue tasks.
    """
    today = date.today()
    n = 0
    for t in tasks:
        if t.status != Task.Status.PENDING or not t.due_date:
            continue
        if t.due_date < today:
            n += 1
    return n


def _summary_stats(tasks: list) -> dict:
    """Summary stats for the todo app.

    Args:
        tasks (list): The list of tasks.

    Returns:
        dict: The summary stats object.
    """
    return {
        "total": len(tasks),
        "pending": sum(1 for t in tasks if t.status == Task.Status.PENDING),
        "completed": sum(1 for t in tasks if t.status == Task.Status.COMPLETED),
        "overdue": _count_overdue(tasks),
    }


def task_list_page_context(
    request: HttpRequest,
) -> dict[str, Any | list[Task] | int | str | None]:
    """Task list page context for the todo app.

    Args:
        request (HttpRequest): The request object.

    Returns:
        dict[str, Any | list[Task] | int | str | None]: The context object.
    """
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

    sort_by = request.GET.get("sort", "id")
    priority_order = {
        Task.Priority.HIGH: 0,
        Task.Priority.MEDIUM: 1,
        Task.Priority.LOW: 2,
    }

    if sort_by == "priority":
        tasks = sorted(tasks, key=lambda t: priority_order.get(t.priority, 99))
    elif sort_by == "due_date":
        tasks = sorted(
            tasks, key=lambda t: (t.due_date is None, t.due_date or date.min)
        )
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
    """Hello HTML view for the todo app.

    Args:
        request (AuthHttpRequest): The request object.

    Returns:
        HttpResponse: The response object.
    """
    return render(request, "todos/hello.html", task_list_page_context(request))


@login_required
def task_list(request: HttpRequest) -> HttpResponse:
    """Task list view for the todo app.

    Args:
        request (AuthHttpRequest): The request object.

    Returns:
        HttpResponse: The response object.
    """
    return render(request, "todos/tasks_list.html", task_list_page_context(request))


@login_required
def add_task(request: HttpRequest) -> HttpResponse:
    """Add task view for the todo app.

    Args:
        request (AuthHttpRequest): The request object.

    Returns:
        HttpResponse: The response object.
    """
    # DEBUG: Log the start of the add task process
    logger.debug("User %s accessing add task page", request.user.id)

    if request.method == "POST":

        #DEBUG: Log the form submission
        logger.debug("POST data received for new task: %s", request.POST.dict())

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
                # WARNING: Log validation failures such as User error/Unexpected conditons
                logger.warning(
                    "Invalid date format submitted: %s",
                    due_date_raw,
                )
                errors["due_date"] = "Invalid date format. Use YYYY-MM-DD."

            if due_date is not None and due_date < date.today():
                # WARNING: Log validation failures such as User error/Unexpected conditons
                logger.warning(
                    "Attempted to submit due date in the past: %s",
                    due_date,
                )
                errors["due_date"] = "Due date cannot be in the past."

        if errors:
            #WARNING: Log validation failures such as User error/Unexpected conditons
            logger.warning(
                "Task creation validation failed for user %s: %s", 
                request.user.id, 
                errors
            )
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
        #STATE CHANGE: Logging a new database record creation
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
            #INFO: Log successful task creation and DB record change
            logger.info(
                "Task '%s' with ID %d, created successfully for user %s",
                task.title,
                task.id,
                request.user.id
            )
            return redirect("task_list")
        
        except Exception as e:
            #ERROR: Unexpected system failure during task creation to DB
            logger.error(
                "System failure during task creation for user %s: %s",
                request.user.id,
                str(e),
                exc_info=True
            )
            return HttpResponse("A database error occurred while creating the task. Please try again later.", status=500)

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
def toggle_task(request: HttpRequest, task_id: int) -> HttpResponse:
    """Toggle task view for the todo app.

    Args:
        request (AuthHttpRequest): The request object.
        task_id (int): The task ID.

    Returns:
        HttpResponse: The response object.
    """

    # Log the start of the toggle process
    logger.debug("Toggle request received for task id %s by user %s", 
        task_id, 
        request.user.id,
    )

    task = get_object_or_404(Task, pk=task_id, user=request.user)
    old_status = task.status

    if task.status == Task.Status.PENDING:
        task.status = Task.Status.COMPLETED
    else:
        task.status = Task.Status.PENDING

    try:    
        task.save(update_fields=["status"])

        # Log status change success
        logger.info(
            "Task %s status changed from %s to %s by user %s",
            task.id,
            old_status,
            task.status,
            request.user.id
        )
        return redirect("task_list")
    
    except Exception as e:
        # Unexpected system failure during task status update to DB
        logger.error(
            "Failed to toggle status for task %s:: %s",
            task_id,
            str(e),
            exc_info=True
        )
        return HttpResponse("A database error occurred while updating the task status. Please try again later.", status=500)

@login_required
def edit_task(request: HttpRequest, task_id: int) -> HttpResponse:
    """Edit task view for the todo app.

    Args:
        request (AuthHttpRequest): The request object.
        task_id (int): The task ID.

    Returns:
        HttpResponse: The response object.
    """
    # DEBUG: Log the start of the edit process
    logger.debug("User %s attempting to edit task %s",
                request.user.id,
                 task_id
    )

    task = get_object_or_404(Task, pk=task_id, user=request.user)

    if request.method == "POST":
        #DEBUG: Log the form submission
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
            #WARNING: Log validation failures such as User error/Unexpected conditons
            logger.warning(
                "Task update validation failed for task %s by user %s: %s",
                task_id,
                request.user.id,
                errors
            )

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
                # WARNING: Log validation failures such as User error/Unexpected conditons
                logger.warning(
                    "Invalid due date format for task %s: %s",
                    task_id,
                    due_date_str,
                )
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

        #STATE CHANGE: Logging a database record update
        try:
            task.title = title
            task.description = description
            task.priority = priority
            task.due_date = due_date
            task.notes = notes
            task.save()

            #INFO: Log successful task update and DB record change
            logger.info(
                "Task %s ('%s') successfully updated by user %s",
                task.id,
                task.title,
                request.user.id
            )
            return redirect("task_list")

        except Exception as e:
            #ERROR: Unexpected system failure during task update to DB
            logger.error(
                "Failed to update task %s in database: %s",
                task_id,
                str(e)
            )
            return HttpResponse("A database error occurred while updating the task. Please try again later.", status=500)

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
def delete_task(request: HttpRequest, task_id: int) -> HttpResponse:
    """Delete task view for the todo app.

    Args:
        request (AuthHttpRequest): The request object.
        task_id (int): The task ID.

    Returns:
        HttpResponse: The response object.
    """
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    task_title = task.title
    task.delete()

    #INFO: Log task deletion
    logger.info(
        "Task '%s' deleted",
        task_title,
    )
    return redirect("task_list")


@login_required
def complete_task(request: HttpRequest, task_id: int) -> HttpResponse:
    """Complete task view for the todo app.

    Args:
        request (AuthHttpRequest): The request object.
        task_id (int): The task ID.

    Returns:
        HttpResponse: The response object.
    """
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    task.status = Task.Status.COMPLETED
    task.save(update_fields=["status"])

    #INFO: Log status change
    logger.info(
        "Task marked as completed",
        task.title,
    )
    return redirect("task_list")


@login_required
def task_stats(request: HttpRequest) -> JsonResponse:
    """Task stats view for the todo app.

    Args:
        request (AuthHttpRequest): The request object.

    Returns:
        JsonResponse: The JSON response object.
    """
    tasks = list(
        Task.objects.filter(user=request.user).order_by(
            "-id"
        )  # pylint: disable=no-member
    )
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
def note_create(request: HttpRequest, task_id: int) -> HttpResponse:
    """Note create view for the todo app.

    Args:
        request (AuthHttpRequest): The request object.
        task_id (int): The task ID.

    Returns:
        HttpResponse: The response object.
    """
    task = get_object_or_404(Task, pk=task_id, user=request.user)

    if request.method == "POST":
        notes = request.POST.get("notes", "").strip()
        if notes:
            task.notes = notes
            task.save(update_fields=["notes"])
            return redirect("task_list")
    return render(request, "todos/note_list.html", {"task": task})
