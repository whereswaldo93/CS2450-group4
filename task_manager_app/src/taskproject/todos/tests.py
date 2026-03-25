from django.test import TestCase
from django.urls import reverse
from .models import Task, TaskStatus

class TaskViewsTestCase(TestCase):
    def setUp(self):
        # Create a sample task status and a task for testing
        self.task1 = Task.objects.create(
            title='Test Task one',
            description='This is a test task.',
            status=TaskStatus.PENDING
        )
        self.task2 = Task.objects.create(
            title='Test Task two',
            description='This is another test task.',
            status=TaskStatus.COMPLETED
        )

    def test_task_list_view(self):
        response = self.client.get(reverse('task_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'todos/tasks_list.html')
        self.assertContains(response, 'Test Task one')
        self.assertContains(response, 'Test Task two')

    def test_add_task(self):
        response = self.client.post(reverse('add_task'), {
            'title': 'New Task',
            'description': 'This is a new task.',
            'priority': 'High',
            'due_date': '2026-12-31',
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful creation
        self.assertTrue(Task.objects.filter(title='New Task').exists())

    def test_add_task_without_title(self):
        response = self.client.post(reverse('add_task'), {
            'description': 'This task has no title.',
            'priority': 'Low',
            'due_date': '2026-09-16',
        })
        self.assertEqual(response.status_code, 200)  # Render the form again with errors
        self.assertFormError(response, 'form', 'title', 'This field is required.')

    def test_add_task_with_past_due_date(self):
        response = self.client.post(reverse('add_task'), {
            'title': 'Task with Past Due Date',
            'description': 'This task has a past due date.',
            'priority': 'Medium',
            'due_date': '2020-01-01',  # Past date
        })
        self.assertEqual(response.status_code, 200)  # Render the form again with errors
        self.assertFormError(response, 'form', 'due_date', 'Due date cannot be in the past.')

    def test_edit_task(self):
        response = self.client.post(reverse('edit_task', args=[self.task1.id]), {
            'title': 'Updated Task Title',
            'description': 'Updated description.',
            'priority': 'Low',
            'due_date': '2026-10-10',
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful update
        self.task1.refresh_from_db()
        self.assertEqual(self.task1.title, 'Updated Task Title')
        self.assertEqual(self.task1.description, 'Updated description.')

    def test_delete_task(self):
        response = self.client.post(reverse('delete_task', args=[self.task1.id]))
        self.assertEqual(response.status_code, 302)  # Redirect after successful deletion
        self.assertFalse(Task.objects.filter(id=self.task1.id).exists()) # Task should be deleted