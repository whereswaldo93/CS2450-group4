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
            due_date="2026-04-01",
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

if __name__ == '__main__':
    unittest.main()