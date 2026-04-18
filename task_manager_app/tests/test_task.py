from datetime import datetime, date
import sys
import os
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from taskproject.todos.file_task import Task, TaskPriority, TaskStatus

class MockRepo:
    # Mock repository class for testing purposes, simulating the behavior of a task repository by storing tasks in memory and providing methods to load and save tasks.
    def __init__(self):
        self.tasks = []

    def load_tasks(self) -> list[Task]:
        return self.tasks

    def save_tasks(self, tasks: list[Task]) -> None:
        self.tasks = tasks

class TestTask(unittest.TestCase):
    def setUp(self):
        # Set up the test environment by creating a MockRepo instance and adding a sample task to it, allowing subsequent tests to interact with a predefined task list.
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
        # Test case for creating a new task and saving it to the repository, ensuring that the task is correctly added to the list of tasks and that its attributes are set as expected.
        task = Task(
            task_id=2,
            title="New Task",
            description="Another task description.",
            due_date="2027-04-05",
            priority=TaskPriority.MEDIUM,
            status=TaskStatus.PENDING,
            notes=""
        )
        self.repo.save_tasks(self.repo.load_tasks() + [task])
        
        self.assertEqual(len(self.repo.load_tasks()), 2)
        self.assertEqual(task.title, "New Task")
        self.assertEqual(task.priority, TaskPriority.MEDIUM)

    def test_complete_task(self):
        # Test case for marking a task as completed, ensuring that the status of the task is updated correctly and that the change is reflected in the repository.
        self.task1.status = TaskStatus.COMPLETED
        self.assertEqual(self.task1.status, TaskStatus.COMPLETED)

    def test_delete_task(self):
        # Test case for deleting a task from the repository, ensuring that the task is removed from the list of tasks and that it is no longer present in the repository after deletion.
        self.repo.save_tasks([self.task1])  # Ensure task is in the repo
        self.repo.save_tasks([task for task in self.repo.load_tasks() if task.task_id != 1])
        
        self.assertEqual(len(self.repo.load_tasks()), 0)  # Task should be deleted
        self.assertNotIn(self.task1, self.repo.load_tasks())  # Task should not be in the repo anymore

    def test_invalid_due_date(self):
        # Test case for creating a task with an invalid due date format, ensuring that a ValueError is raised when the due date does not conform to the expected "YYYY-MM-DD" format.
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
        # Test case for creating a task with an invalid priority value, ensuring that a ValueError is raised when the priority does not match one of the defined choices in TaskPriority.
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
        # Test case for creating a task without a due date, ensuring that the task can be created successfully and that the due_date attribute is set to None when no due date is provided.
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
        # Test case for creating a task without a title, ensuring that a ValueError is raised when the title is empty, as the title is a required field for a task.
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
        # Test case for creating a task with a past due date, ensuring that a ValueError is raised when the due date is set to a date in the past, as tasks should not have due dates that have already passed.
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
        # Test case for creating a task with notes, ensuring that the task can be created successfully and that the notes attribute is correctly set and saved in the repository.
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
        # Test case for attempting to delete a non-existent task, ensuring that the repository remains unchanged and that no errors occur when trying to delete a task that is not present in the repository.
        self.repo.save_tasks([task for task in self.repo.load_tasks() if task.task_id != 999])  # Attempt to delete a non-existent task
        self.assertEqual(len(self.repo.load_tasks()), 1)  # Task list should remain unchanged

    def test_delete_task_notes(self):
        # Test case for deleting the notes of a task, ensuring that the notes can be removed from a task and that the notes attribute is set to None or an empty string after deletion.
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
        # Test case for editing the notes of a task, ensuring that the notes can be updated and that the changes are correctly reflected in the repository when the notes of a task are modified.
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
        # Test case for adding notes to an existing task that initially has no notes, ensuring that notes can be added to a task after it has been created and that the notes attribute is updated correctly in the repository.
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