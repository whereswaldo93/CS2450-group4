from django.urls import path
from . import views


urlpatterns = [
    path("", views.hello_html_view, name="hello_html_view"),
    path("tasks", views.task_list, name="task_list"),
    path("tasks/add", views.add_task, name="add_task"),
    path("tasks/<int:task_id>/toggle", views.toggle_task, name="toggle_task"),
    path("tasks/<int:task_id>/edit", views.edit_task, name="edit_task"),
    path("tasks/<int:task_id>/delete", views.delete_task, name="delete_task"),
    path("tasks/<int:task_id>/complete", views.complete_task, name="complete_task"),
]
