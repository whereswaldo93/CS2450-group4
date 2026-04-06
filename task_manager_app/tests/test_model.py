# from datetime import datetime, date
# import sys
# import os
# import unittest

from django.test import TestCase
from django.utils import timezone
from src.taskproject.todos.models import Task

# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
# from taskproject.todos.file_task import Task, TaskPriority, TaskStatus

# class MockRepo:
#     def __init__(self):
#         self.tasks = []

#     def load_tasks(self) -> list[Task]:
#         return self.tasks

#     def save_tasks(self, tasks: list[Task]) -> None:
#         self.tasks = tasks

class TestTask(TestCase):
    def setUp(self):
        self.task1 = Task.objects.create(
            title="Learn Pytest",
            description="Write some tests",
            due_date="2027-04-01",
            priority=TaskPriority.HIGH,
            status=TaskStatus.PENDING,
            notes=""
        )

    def test_create_task(self):
        task = Task.objects.create(
            title="New Task",
            description="Another task description.",
            due_date="2027-04-05",
            priority=TaskPriority.MEDIUM,
            status=TaskStatus.PENDING,
            notes=""
        )
        self.assertEqual(len(Task.objects.all()), 2)
        self.assertEqual(task.title, "New Task")
        self.assertEqual(task.priority, TaskPriority.MEDIUM)
        self.assertEqual(task.status, TaskStatus.PENDING)
        self.assertEqual(task.notes, "")

    def test_complete_task(self):
        self.task1.status = TaskStatus.COMPLETED
        self.task1.save()
        self.assertEqual(self.task1.status, TaskStatus.COMPLETED)

    def test_delete_task(self):
        self.task1.delete()
        self.assertEqual(len(Task.objects.all()), 0)  # Task should be deleted
        self.assertFalse(Task.objects.filter(id=self.task1.id).exists())  # Task should not be in the database anymore

    def test_invalid_due_date(self):
        with self.assertRaises(ValueError):
            Task.objects.create(
                title="Bad Date Task",
                description="This task has an invalid due date.",
                due_date="04-01-2026",  # Invalid format
                priority=TaskPriority.LOW,
                status=TaskStatus.PENDING,
                notes=""
            )

    def test_invalid_priority(self):
        with self.assertRaises(ValueError):
            Task.objects.create(
                title="Bad Priority Task",
                description="This task has an invalid priority.",
                due_date="2027-04-01",
                priority="URGENT",  # Invalid priority
                status=TaskStatus.PENDING,
                notes=""
            )

    def test_task_with_no_due_date(self):
        task = Task.objects.create(
            title="No Due Date Task",
            description="This task has no due date.",
            due_date=None,
            priority=TaskPriority.MEDIUM,
            status=TaskStatus.PENDING,
            notes=""
        )
        self.assertIsNone(task.due_date)
    
    def test_add_task_without_title(self):
        with self.assertRaises(ValueError):
            Task.objects.create(
                title="",  # Empty title
                description="This task has no title.",
                due_date="2027-04-01",
                priority=TaskPriority.MEDIUM,
                status=TaskStatus.PENDING,
                notes=""
            )

    def test_add_task_with_past_due_date(self):
        past_date = timezone.now().date() - timezone.timedelta(days=1)  # Set past date to yesterday
        with self.assertRaises(ValueError) as context:
            Task.objects.create(
                title="Past Due Date Task",
                description="This task has a past due date.",
                due_date=past_date,  # Past due date
                priority=TaskPriority.MEDIUM,
                status=TaskStatus.PENDING,
                notes=""
            )
        self.assertEqual(str(context.exception), "Due date cannot be in the past.")

    def test_add_task_with_notes(self):
        task_with_notes = Task.objects.create(
            title="Task with Notes",
            description="This task has notes.",
            due_date="2026-06-01",
            priority=TaskPriority.LOW,
            status=TaskStatus.PENDING,
            notes="These are some notes for the task."
        )
        self.assertEqual(task_with_notes.notes, "These are some notes for the task.")

    def test_delete_non_existent_task(self):
        self.assertEqual(Task.objects.count(), 1)  # Only task1 exists
        # Attempt to delete a task that does not exist
        with self.assertRaises(Task.DoesNotExist):
            Task.objects.get(id=999).delete()  # This should raise an exception since the task does not exist

    def test_delete_task_notes(self):
        task_with_notes = Task.objects.create(
            title="Task with Notes to Delete",
            description="This task has notes that will be deleted.",
            due_date="2026-07-01",
            priority=TaskPriority.MEDIUM,
            status=TaskStatus.PENDING,
            notes="These notes will be deleted."
        )
        task_with_notes.notes = None  # Delete the notes
        task_with_notes.save()
        self.assertIsNone(task_with_notes.notes)  # Ensure the notes are deleted

    def test_edit_task_notes(self):
        task_with_notes = Task.objects.create(
            title="Task with Notes to Edit",
            description="This task has notes that will be edited.",
            due_date="2026-09-01",
            priority=TaskPriority.HIGH,
            status=TaskStatus.PENDING,
            notes="These notes will be edited."
        )
        task_with_notes.notes = "These notes have been edited."  # Edit the notes
        task_with_notes.save()
        self.assertEqual(task_with_notes.notes, "These notes have been edited.")  # Ensure the notes are updated correctly

    def test_adding_notes_to_existing_task(self):
        task_without_notes = Task.objects.create(
            title="Task without Notes",
            description="This task initially has no notes.",
            due_date="2026-08-01",
            priority=TaskPriority.HIGH,
            status=TaskStatus.PENDING,
            notes=None
        )
        task_without_notes.notes = "These are some added notes."  # Add notes to the existing task
        task_without_notes.save()
        self.assertEqual(task_without_notes.notes, "These are some added notes.")  # Ensure the notes are added correctly

# if __name__ == '__main__':
#     unittest.main()