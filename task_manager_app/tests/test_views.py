from datetime import date
import sys
import os
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from taskproject.todos.file_task import Task, TaskPriority, TaskStatus

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

    def test_add_task_view(self):
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
        tasks = self.repo.load_tasks()
        self.assertEqual(len(tasks), 3)
        self.assertEqual(tasks[2].title, "Third New Task")
        self.assertEqual(tasks[2].priority, TaskPriority.HIGH)

    
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

    def test_edit_task_view(self):
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

    def test_view_task_details(self):
        task = self.repo.load_tasks()[0]
        self.assertEqual(task.task_id, 1)
        self.assertEqual(task.title, "Test Task one")
        self.assertEqual(task.description, "This is a test task.")
        self.assertEqual(task.due_date, date(2027, 4, 1))
        self.assertEqual(task.priority, TaskPriority.MEDIUM)
        self.assertEqual(task.status, TaskStatus.PENDING)
        self.assertEqual(task.notes, "")

    def test_add_notes_to_task_view(self):
        self.task1.notes = "These are some notes for the task."
        self.repo.save_tasks([self.task1, self.task2])  # Save the updated task
        updated_task = self.repo.load_tasks()[0]
        self.assertEqual(updated_task.notes, "These are some notes for the task.")
    
    def test_delete_notes_from_task_view(self):
        self.task1.notes = "These are some notes for the task."
        self.repo.save_tasks([self.task1, self.task2])  # Save the updated task
        self.task1.notes = ""  # Clear the notes
        self.repo.save_tasks([self.task1, self.task2])  # Save the updated task again
        updated_task = self.repo.load_tasks()[0]
        self.assertEqual(updated_task.notes, "")  # Ensure the notes have been deleted

    def test_edit_task_with_notes_view(self):
        self.task1.notes = "Initial notes."
        self.repo.save_tasks([self.task1, self.task2])  # Save the updated task
        self.task1.title = 'Updated Task Title with Notes'
        self.task1.description = 'Updated description with notes.'
        self.task1.due_date = '2026-06-01'
        self.task1.priority = TaskPriority.HIGH
        self.task1.status = TaskStatus.COMPLETED
        self.repo.save_tasks([self.task1, self.task2])  # Save the updated task again
        updated_task = self.repo.load_tasks()[0]
        self.assertEqual(updated_task.title, 'Updated Task Title with Notes')
        self.assertEqual(updated_task.description, 'Updated description with notes.')
        self.assertEqual(updated_task.due_date, '2026-06-01')
        self.assertEqual(updated_task.priority, TaskPriority.HIGH)
        self.assertEqual(updated_task.status, TaskStatus.COMPLETED)
        self.assertEqual(updated_task.notes, "Initial notes.")  # Ensure notes are unchanged

    def test_delete_non_existent_notes_view(self):
        self.task1.notes = "These are some notes for the task."
        self.repo.save_tasks([self.task1, self.task2])  # Save the updated task
        self.task1.notes = None  # Attempt to delete notes by setting to None
        self.repo.save_tasks([self.task1, self.task2])  # Save the updated task again
        updated_task = self.repo.load_tasks()[0]
        self.assertIsNone(updated_task.notes)  # Ensure the notes have been deleted  

    def test_empty_task_list_view(self):
        self.repo.save_tasks([])  # Clear all tasks
        tasks = self.repo.load_tasks()
        self.assertEqual(len(tasks), 0)  # Ensure the task list is empty

    def test_delete_non_existent_task_view(self):
        self.repo.save_tasks([task for task in self.repo.load_tasks() if task.task_id != 999])  # Attempt to delete a non-existent task
        self.assertEqual(len(self.repo.load_tasks()), 2)  # Task list should remain unchanged

if __name__ == '__main__':
    unittest.main()