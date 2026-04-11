from __future__ import annotations

import datetime
from typing import ClassVar

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.manager import Manager
from django.utils import timezone


class Task(models.Model):
    # Typed default manager so static analysis recognizes `.objects` / `.create()`.
    objects: ClassVar[Manager[Task]] = models.Manager()

    class Priority(models.TextChoices):
        LOW = "Low", "Low"
        MEDIUM = "Medium", "Medium"
        HIGH = "High", "High"

    class Status(models.TextChoices):
        PENDING = "Pending", "Pending"
        COMPLETED = "Completed", "Completed"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="tasks",
    )
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    priority = models.CharField(
        max_length=20,
        choices=Priority.choices,
        default=Priority.MEDIUM,
    )
    due_date = models.DateField(null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
    )
    notes = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ["-id"]

    def __str__(self) -> str:
        return self.title
    
    def clean(self):
        # Validate that the due date is not in the past
        if self.due_date and self.due_date < timezone.now().date():
            raise ValidationError("Due date cannot be in the past.")
        
        # Validate that the title is not empty
        if not self.title:
            raise ValidationError("Title cannot be empty.")
        
        # Validate the due date format
        if isinstance(self.due_date, str):
            try:
                datetime.datetime.strptime(self.due_date, "%Y-%m-%d")
            except ValueError:
                raise ValidationError("Due date must be in YYYY-MM-DD format.")
            
        # Validate that the priority is one of the defined choices
        if self.priority not in self.Priority.values:
            raise ValidationError(f"Priority must be one of: {', '.join(self.Priority.values)}.")
        
        # Validate that the status is one of the defined choices
        if self.status not in self.Status.values:
            raise ValidationError(f"Status must be one of: {', '.join(self.Status.values)}.")  
        
    def save(self, *args, **kwargs):
        self.full_clean()  # This will call the clean() method to validate the model before saving
        super().save(*args, **kwargs)