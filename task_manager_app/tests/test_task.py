from datetime import datetime, date
import sys
import os
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from taskproject.todos.models import Task, TaskPriority, TaskStatus

class MockRepo:
    def __init__(self):
        self.tasks = []

    def load_tasks(self) -> list[Task]:
        return self.tasks

    def save_tasks(self, tasks: list[Task]) -> None:
        self.tasks = tasks

class TestTask(unittest.TestCase):
    def setUp(self):
        self.repo = MockRepo()
        self.task1 = Task(
            task_id=1,
            title="Learn Pytest",
            description="Write some tests",
            due_date="2027-04-01",
            priority=TaskPriority.HIGH,
            status=TaskStatus.PENDING,
            notes=""
        )
        self.repo.save_tasks([self.task1])

    def test_create_task(self):
        task = Task(
            task_id=2,
            title="New Task",
            description="Another task description.",
            due_date="2026-04-05",
            priority=TaskPriority.MEDIUM,
            status=TaskStatus.PENDING,
            notes=""
        )
        self.repo.save_tasks(self.repo.load_tasks() + [task])
        
        self.assertEqual(len(self.repo.load_tasks()), 2)
        self.assertEqual(task.title, "New Task")
        self.assertEqual(task.priority, TaskPriority.MEDIUM)

    def test_complete_task(self):
        self.task1.status = TaskStatus.COMPLETED
        self.assertEqual(self.task1.status, TaskStatus.COMPLETED)

    def test_delete_task(self):
        self.repo.save_tasks([self.task1])  # Ensure task is in the repo
        self.repo.save_tasks([task for task in self.repo.load_tasks() if task.task_id != 1])
        
        self.assertEqual(len(self.repo.load_tasks()), 0)  # Task should be deleted
        self.assertNotIn(self.task1, self.repo.load_tasks())  # Task should not be in the repo anymore

    def test_invalid_due_date(self):
        with self.assertRaises(ValueError):
            Task(
                task_id=3,
                title="Bad Date Task",
                description="This task has an invalid due date.",
                due_date="04-01-2026",  # Invalid format
                priority=TaskPriority.LOW,
                status=TaskStatus.PENDING,
                notes=""
            )
    def test_invalid_priority(self):
        with self.assertRaises(ValueError):
            Task(
                task_id=4,
                title="Bad Priority Task",
                description="This task has an invalid priority.",
                due_date="2027-04-01",
                priority="URGENT",  # Invalid priority
                status=TaskStatus.PENDING,
                notes=""
            )
    def test_task_with_no_due_date(self):
        task = Task(
            task_id=5,
            title="No Due Date Task",
            description="This task has no due date.",
            due_date=None,  # No due date
            priority=TaskPriority.MEDIUM,
            status=TaskStatus.PENDING,
            notes=""
        )
        self.assertIsNone(task.due_date)
    
    def test_add_task_without_title(self):
        with self.assertRaises(ValueError):
            Task(
                task_id=6,
                title="",  # Empty title
                description="This task has no title.",
                due_date="2027-04-01",
                priority=TaskPriority.MEDIUM,
                status=TaskStatus.PENDING,
                notes=""
            )

    def test_add_task_with_past_due_date(self):
        past_date = "2022-01-01"
        with self.assertRaises(ValueError) as context:
            Task(
                task_id=7,
                title="Past Due Date Task",
                description="This task has a past due date.",
                due_date=past_date,  # Past due date
                priority=TaskPriority.MEDIUM,
                status=TaskStatus.PENDING,
                notes=""
            )
        self.assertEqual(str(context.exception), "Due date cannot be in the past.")

    def test_add_task_with_notes(self):
        task_with_notes = Task(
            task_id=8,
            title="Task with Notes",
            description="This task has notes.",
            due_date="2026-06-01",
            priority=TaskPriority.LOW,
            status=TaskStatus.PENDING,
            notes="These are some notes for the task."
        )
        self.repo.save_tasks(self.repo.load_tasks() + [task_with_notes])
        saved_task = self.repo.load_tasks()[-1]
        self.assertEqual(saved_task.notes, "These are some notes for the task.")

    def test_delete_non_existent_task(self):
        self.repo.save_tasks([task for task in self.repo.load_tasks() if task.task_id != 999])  # Attempt to delete a non-existent task
        self.assertEqual(len(self.repo.load_tasks()), 1)  # Task list should remain unchanged

    def test_delete_task_notes(self):
        task_with_notes = Task(
            task_id=9,
            title="Task with Notes to Delete",
            description="This task has notes that will be deleted.",
            due_date="2026-07-01",
            priority=TaskPriority.MEDIUM,
            status=TaskStatus.PENDING,
            notes="These notes will be deleted."
        )
        self.repo.save_tasks(self.repo.load_tasks() + [task_with_notes])
        saved_task = self.repo.load_tasks()[-1]
        saved_task.notes = None  # Delete the notes
        self.assertIsNone(saved_task.notes)  # Ensure the notes are deleted

    def test_edit_task_notes(self):
        task_with_notes = Task(
            task_id=11,
            title="Task with Notes to Edit",
            description="This task has notes that will be edited.",
            due_date="2026-09-01",
            priority=TaskPriority.HIGH,
            status=TaskStatus.PENDING,
            notes="These notes will be edited."
        )
        self.repo.save_tasks(self.repo.load_tasks() + [task_with_notes])
        saved_task = self.repo.load_tasks()[-1]
        saved_task.notes = "These notes have been edited."  # Edit the notes
        self.assertEqual(saved_task.notes, "These notes have been edited.")  # Ensure the notes are updated correctly

    def test_adding_notes_to_existing_task(self):
        task_without_notes = Task(
            task_id=10,
            title="Task without Notes",
            description="This task initially has no notes.",
            due_date="2026-08-01",
            priority=TaskPriority.HIGH,
            status=TaskStatus.PENDING,
            notes=None
        )
        self.repo.save_tasks(self.repo.load_tasks() + [task_without_notes])
        saved_task = self.repo.load_tasks()[-1]
        saved_task.notes = "These are some added notes."  # Add notes to the existing task
        self.assertEqual(saved_task.notes, "These are some added notes.")  # Ensure the notes are added correctly

if __name__ == '__main__':
    unittest.main()