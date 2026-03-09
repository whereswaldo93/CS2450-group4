import unittest
from models.task import Task, TaskPriority, TaskStatus
from models.task_manager import TaskManager

class MockRepo:
    """An in-memory repository to test TaskManager without touching the disk."""
    def __init__(self):
        self.tasks = []

    def load_tasks(self) -> list[Task]:
        return self.tasks

    def save_tasks(self, tasks: list[Task]) -> None:
        self.tasks = tasks

class TestTaskManager(unittest.TestCase):
    def setUp(self):
        self.repo = MockRepo()
        self.manager = TaskManager(self.repo)

    def test_add_task_success(self):
        task = self.manager.add_task(
            title="Learn Pytest",
            description="Write some tests",
            due_date="2026-04-01",
            priority="High"
        )
        
        self.assertEqual(task.task_id, 1)
        self.assertEqual(task.title, "Learn Pytest")
        self.assertEqual(task.priority, TaskPriority.HIGH)
        self.assertEqual(len(self.repo.tasks), 1)

    def test_add_task_invalid_due_date(self):
        with self.assertRaises(ValueError) as context:
            self.manager.add_task(
                title="Bad Date",
                description="Testing errors",
                due_date="04-01-2026",
                priority="Low"
            )
        self.assertTrue("Invalid due date format" in str(context.exception))

    def test_complete_task(self):
        self.manager.add_task("Test Task", "", None, "Medium")
        
        result = self.manager.complete_task(task_id=1)
        self.assertEqual(result, "completed")
        self.assertEqual(self.manager.get_task(1).status, TaskStatus.COMPLETED)

        result_again = self.manager.complete_task(task_id=1)
        self.assertEqual(result_again, "already_complete")

    def test_delete_task(self):
        self.manager.add_task("To be deleted", "", None, "Low")
        self.assertEqual(len(self.manager.list_tasks()), 1)
        
        success = self.manager.delete_task(task_id=1)
        self.assertTrue(success)
        self.assertEqual(len(self.manager.list_tasks()), 0)

if __name__ == '__main__':
    unittest.main()
