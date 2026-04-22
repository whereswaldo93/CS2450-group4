from .task_view import (
    add_task,
    complete_task,
    delete_task,
    edit_task,
    hello_html_view,
    note_create,
    task_list,
    task_stats,
    toggle_task,
)
from .auth_views import login_view, signup_view

__all__ = [
    "add_task",
    "complete_task",
    "delete_task",
    "edit_task",
    "hello_html_view",
    "login_view",
    "note_create",
    "signup_view",
    "task_list",
    "task_stats",
    "toggle_task",
]
