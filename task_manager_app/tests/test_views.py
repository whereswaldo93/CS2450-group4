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
            due_date="2026-04-01",
            priority=TaskPriority.MEDIUM,
            status=TaskStatus.PENDING,
            notes=""
        )
        self.task2 = Task(
            task_id=2,
            title="Test Task two",
            description="This is another test task.",
            due_date="2026-04-02",
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
if __name__ == '__main__':
    unittest.main()

# class TaskViewsTestCase(TestCase):
#     def setUp(self):
#         # Create a sample task status and a task for testing
#         self.task1 = Task.objects.create(
#             title='Test Task one',
#             description='This is a test task.',
#             status=TaskStatus.PENDING
#         )
#         self.task2 = Task.objects.create(
#             title='Test Task two',
#             description='This is another test task.',
#             status=TaskStatus.COMPLETED
#         )

#    

#     def test_add_task(self):
#         response = self.client.post(reverse('add_task'), {
#             'title': 'New Task',
#             'description': 'This is a new task.',
#             'priority': 'High',
#             'due_date': '2026-12-31',
#         })
#         self.assertEqual(response.status_code, 302)  # Redirect after successful creation
#         self.assertTrue(Task.objects.filter(title='New Task').exists())

#     def test_add_task_without_title(self):
#         response = self.client.post(reverse('add_task'), {
#             'description': 'This task has no title.',
#             'priority': 'Low',
#             'due_date': '2026-09-16',
#         })
#         self.assertEqual(response.status_code, 200)  # Render the form again with errors
#         self.assertFormError(response, 'form', 'title', 'This field is required.')

#     def test_add_task_with_past_due_date(self):
#         response = self.client.post(reverse('add_task'), {
#             'title': 'Task with Past Due Date',
#             'description': 'This task has a past due date.',
#             'priority': 'Medium',
#             'due_date': '2020-01-01',  # Past date
#         })
#         self.assertEqual(response.status_code, 200)  # Render the form again with errors
#         self.assertFormError(response, 'form', 'due_date', 'Due date cannot be in the past.')

#     def test_edit_task(self):
#         response = self.client.post(reverse('edit_task', args=[self.task1.id]), {
#             'title': 'Updated Task Title',
#             'description': 'Updated description.',
#             'priority': 'Low',
#             'due_date': '2026-10-10',
#         })
#         self.assertEqual(response.status_code, 302)  # Redirect after successful update
#         self.task1.refresh_from_db()
#         self.assertEqual(self.task1.title, 'Updated Task Title')
#         self.assertEqual(self.task1.description, 'Updated description.')

#     def test_delete_task(self):
#         response = self.client.post(reverse('delete_task', args=[self.task1.id]))
#         self.assertEqual(response.status_code, 302)  # Redirect after successful deletion
#         self.assertFalse(Task.objects.filter(id=self.task1.id).exists()) # Task should be deleted

    # test_add_task_with_empty_description:

        # Ensure that a task can be created with an empty description. Validate that the task still saves successfully.

    # test_add_task_with_invalid_priority:

        # Test attempting to create a task with an invalid priority value. Ensure it raises a validation error.

    # test_edit_task_with_invalid_priority:

        # Test editing an existing task to assign an invalid priority. Ensure the application raises an appropriate error.

    # test_delete_non_existing_task:

        # Attempt to delete a task that doesn't exist and ensure the application handles this gracefully (e.g., returns a 404 error).

    # test_task_list_view_with_no_tasks:

        # Verify that the task list view behaves correctly when there are no tasks present (e.g., displays a message indicating no tasks).

    # test_add_task_with_notes:

        # Create a task with notes and ensure that the notes are saved and displayed correctly in the task.

    # test_edit_task_with_empty_notes:

        # Test editing a task to set its notes to empty. Verify that it updates correctly.

    # test_task_status_transition:

        # Create a task and change its status from "Pending" to "Completed". Ensure the status updates correctly.

    # test_task_retrieval_by_id:
        # Retrieve a task by its ID and verify that the correct task is returned.