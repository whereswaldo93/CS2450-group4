import os
import django
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import date, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'taskproject.core.settings')
django.setup()

from taskproject.todos.models import Task

class TaskManagerDjangoTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

    def test_signup_creates_user(self):
        """1. Integration Test: Verify the signup view successfully creates a new user and logs them in."""
        self.client.logout()
        
        response = self.client.post(reverse('signup'), {
            'username': 'newuser',
            'password1': 'strongpassword123',
            'password2': 'strongpassword123'
        })        
        self.assertRedirects(response, reverse('task_list'))
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_unauthenticated_access_redirects(self):
        """2. Security Test: Verify that accessing protected views without logging in redirects to the login page."""
        self.client.logout()
        response = self.client.get(reverse('task_list'))
      
        expected_url = f"{reverse('login')}?next={reverse('task_list')}"
        self.assertRedirects(response, expected_url)

    def test_add_task_view(self):
        """3. Integration Test: Verify adding a task through the POST view creates a database entry."""
        task_data = {
            'title': 'Test Django Task',
            'description': 'Integration test for adding a task',
            'priority': 'High',
            'due_date': (date.today() + timedelta(days=5)).strftime('%Y-%m-%d'),
            'notes': 'Some notes'
        }
        response = self.client.post(reverse('add_task'), task_data)
        
        self.assertRedirects(response, reverse('task_list'))
        
        task = Task.objects.get(title='Test Django Task')
        self.assertEqual(task.description, 'Integration test for adding a task')
        self.assertEqual(task.priority, 'High')
        self.assertEqual(task.status, 'Pending')
        self.assertEqual(task.user, self.user)

    def test_toggle_task_status(self):
        """4. Integration Test: Verify that the toggle_task view correctly flips a task's status."""
        task = Task.objects.create(
            title="Task to Toggle",
            user=self.user,
            priority="Medium",
            status="Pending"
        )
        
        response = self.client.post(reverse('toggle_task', args=[task.id]))
        self.assertRedirects(response, reverse('task_list'))
        
        task.refresh_from_db()
        self.assertEqual(task.status, 'Completed')

    def test_task_list_stats_context(self):
        """5. Unit/Integration Test: Verify the dashboard calculations for total, pending, completed, and overdue tasks."""
        Task.objects.create(title="Completed Task", user=self.user, status="Completed")
        Task.objects.create(title="Pending Task", user=self.user, status="Pending", due_date=date.today() + timedelta(days=2))
        Task.objects.create(title="Overdue Task", user=self.user, status="Pending", due_date=date.today() - timedelta(days=2))
        
        response = self.client.get(reverse('task_list'))
        self.assertEqual(response.status_code, 200)
        
        self.assertEqual(response.context['total'], 3)
        self.assertEqual(response.context['completed'], 1)
        self.assertEqual(response.context['pending'], 2)
        self.assertEqual(response.context['overdue'], 1)
