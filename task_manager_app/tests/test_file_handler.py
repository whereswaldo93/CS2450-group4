# from unittest.mock import patch, mock_open
# from pathlib import Path
# import json
# from src.taskproject.todos.models import Task, TaskStatus, TaskPriority
# from src.taskproject.todos.file_handler import TaskFileRepo

# from datetime import date
# import sys
# import os
# import unittest

# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

# class TestTaskFileRepo(unittest.TestCase):
#     def setUp(self):
#         self.test_file_path = Path("test_tasks.json")
#         self.repo = TaskFileRepo(self.test_file_path)

#     def tearDown(self):
#         # Clean up the test file after each test
#         if self.test_file_path.exists():
#             self.test_file_path.unlink()

#     @patch("builtins.open", new_callable=mock_open, read_data='[{"task_id": 1, "title": "Test Task", "description": "A test task", "due_date": "2027-12-31", "priority": "MEDIUM", "status": "PENDING", "notes": ""}]')
#     def test_load_tasks_valid_json(self, mock_file):
#         tasks = self.repo.load_tasks()
#         self.assertEqual(len(tasks), 1)
#         self.assertEqual(tasks[0].task_id, 1)
#         self.assertEqual(tasks[0].title, "Test Task")
#         self.assertEqual(tasks[0].description, "A test task")
#         self.assertEqual(tasks[0].due_date, "2027-12-31")
#         self.assertEqual(tasks[0].priority, TaskPriority.MEDIUM)
#         self.assertEqual(tasks[0].status, TaskStatus.PENDING)
#         self.assertEqual(tasks[0].notes, "")

#     @patch("pathlib.Path.exists", return_value=True)
#     @patch("pathlib.Path.stat")
#     @patch("builtins.open", new_callable=mock_open, read_data='invalid json')
#     def test_load_tasks_invalid_json(self, mock_file, mock_stat, mock_exists):
#         mock_stat.return_value.st_size = 10  # Simulate non-empty file
#         with self.assertRaises(ValueError) as context:
#             self.repo.load_tasks()
#         self.assertIn("Expected a list of tasks", str(context.exception))

#     @patch("builtins.open", new_callable=mock_open)
#     def test_save_tasks(self, mock_file):
#         task = Task(
#             task_id=1,
#             title="Test Task",
#             description="A test task",
#             due_date="2027-12-31",
#             priority=TaskPriority.MEDIUM,
#             status=TaskStatus.PENDING,
#             notes=""
#         )
#         self.repo.save_tasks([task])
#         mock_file().write.assert_called_once_with(
#             json.dumps([task.to_dict()], indent=2)
#             )
        
#         @patch("pathlib.Path.mkdir")
#         @patch("builtins.open", new_callable=mock_open)
#         def test_save_tasks_creates_directory(self, mock_file, mock_mkdir):
#             task = Task(
#                 task_id=1,
#                 title="Test Task",
#                 description="A test task",
#                 due_date="2027-12-31",
#                 priority=TaskPriority.MEDIUM,
#                 status=TaskStatus.PENDING,
#                 notes=""
#             )
#             self.repo.save_tasks([task])
#             mock_mkdir.assert_called_once_with(parents=True, exist_ok=True)

# if __name__ == "__main__":
#     unittest.main()