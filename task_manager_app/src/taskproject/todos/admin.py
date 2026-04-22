from django.contrib import admin

from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    # Configure the admin interface for the Task model, specifying which fields to display, filter, and search by.
    list_display = ("title", "user", "priority", "status", "due_date")
    list_filter = ("status", "priority")
    search_fields = ("title", "description", "user__username")
