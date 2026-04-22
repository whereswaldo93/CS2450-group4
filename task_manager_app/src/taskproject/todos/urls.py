from django.conf import settings
from django.contrib.auth.views import LogoutView
from django.urls import path

from .views import task_view, auth_views

urlpatterns = [
    path("login/", auth_views.login_view, name="login"),
    path("signup/", auth_views.signup_view, name="signup"),
    path(
        "logout/",
        LogoutView.as_view(next_page=settings.LOGOUT_REDIRECT_URL),
        name="logout",
    ),
    path("", task_view.hello_html_view, name="hello_html_view"),
    path("tasks", task_view.task_list, name="task_list"),
    path("tasks/add", task_view.add_task, name="add_task"),
    path(
        "tasks/<int:task_id>/toggle",
        task_view.toggle_task,
        name="toggle_task",
    ),
    path(
        "tasks/<int:task_id>/edit",
        task_view.edit_task,
        name="edit_task",
    ),
    path(
        "tasks/<int:task_id>/delete",
        task_view.delete_task,
        name="delete_task",
    ),
    path(
        "tasks/<int:task_id>/complete",
        task_view.complete_task,
        name="complete_task",
    ),
    path(
        "tasks/<int:task_id>/notes/",
        task_view.note_create,
        name="note_create",
    ),
]
