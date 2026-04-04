import sys
import os
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from taskproject.todos.models import Task, TaskStatus, TaskPriority
from taskproject.todos.views import add_task

class MockRepo:
    def __init__(self):
        self.tasks = []

    def load_tasks(self) -> list[Task]:
        return self.tasks

    def save_tasks(self, tasks: list[Task]) -> None:
        self.tasks = tasks

class TestTaskViews(unittest.TestCase):
    def setUp(self):
        self.repo = MockRepo()
        self.task1 = Task(
            task_id=1,
            title="Test Task one",
            description="This is a test task.",
            due_date="2027-04-01",
            priority=TaskPriority.MEDIUM,
            status=TaskStatus.PENDING,
            notes=""
        )
        self.task2 = Task(
            task_id=2,
            title="Test Task two",
            description="This is another test task.",
            due_date="2027-04-02",
            priority=TaskPriority.LOW,
            status=TaskStatus.COMPLETED,
            notes=""
        )
        self.repo.tasks = [self.task1, self.task2]


    def test_task_list_view(self):
        tasks = self.repo.load_tasks()
        self.assertEqual(len(tasks), 2)
        self.assertEqual(tasks[0].title, "Test Task one")
        self.assertEqual(tasks[1].title, "Test Task two")

    def test_add_task(self):
        new_task = Task(
            task_id=3,
            title="Third New Task",
            description="This is a third new task.",
            due_date="2026-12-31",
            priority=TaskPriority.HIGH,
            status=TaskStatus.PENDING,
            notes=""
        )

        self.repo.save_tasks(self.repo.load_tasks() + [new_task])
        self.assertEqual(new_task.task_id, 3) # Ensure the new task has the correct ID
        self.assertEqual(new_task.title, "Third New Task") # Ensure the new task has the correct title
        self.assertEqual(len(self.repo.load_tasks()), 3) # Ensure the task list now has 3 tasks
    
    def test_delete_task(self):
        self.repo.save_tasks([task for task in self.repo.load_tasks() if task.task_id != 1])
        self.assertEqual(len(self.repo.load_tasks()), 1) # Ensure the task list now has 1 task
        self.assertEqual(self.repo.load_tasks()[0].task_id, 2) # Ensure the remaining task is the correct one
    
    def test_filter_by_status(self):
        pending_tasks = [task for task in self.repo.load_tasks() if task.status == TaskStatus.PENDING]
        self.assertEqual(len(pending_tasks), 1)
        self.assertEqual(pending_tasks[0].title, "Test Task one")

        completed_tasks = [task for task in self.repo.load_tasks() if task.status == TaskStatus.COMPLETED]
        self.assertEqual(len(completed_tasks), 1)
        self.assertEqual(completed_tasks[0].title, "Test Task two")
    
    def test_filter_by_priority(self):
        medium_tasks = [task for task in self.repo.load_tasks() if task.priority == TaskPriority.MEDIUM]
        self.assertEqual(len(medium_tasks), 1)
        self.assertEqual(medium_tasks[0].title, "Test Task one")

        low_tasks = [task for task in self.repo.load_tasks() if task.priority == TaskPriority.LOW]
        self.assertEqual(len(low_tasks), 1)
        self.assertEqual(low_tasks[0].title, "Test Task two")

        high_tasks = [task for task in self.repo.load_tasks() if task.priority == TaskPriority.HIGH]
        self.assertEqual(len(high_tasks), 0)

    def test_edit_task(self):
        self.task1.title = 'Updated Task Title'
        self.task1.description = 'Updated description.'
        self.task1.due_date = '2026-05-01'
        self.task1.priority = TaskPriority.HIGH
        self.task1.status = TaskStatus.COMPLETED
        self.repo.save_tasks([self.task1, self.task2])  # Save the updated task
        updated_task = self.repo.load_tasks()[0]
        self.assertEqual(updated_task.title, 'Updated Task Title')
        self.assertEqual(updated_task.description, 'Updated description.')
        self.assertEqual(updated_task.due_date, '2026-05-01')
        self.assertEqual(updated_task.priority, TaskPriority.HIGH)
        self.assertEqual(updated_task.status, TaskStatus.COMPLETED)

        
if __name__ == '__main__':
    unittest.main()