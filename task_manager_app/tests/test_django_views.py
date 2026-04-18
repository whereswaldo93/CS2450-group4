"""
Django integration tests for todos views.
Uses Django's test client — hits real DB (SQLite in-memory during tests).
Run from the repo root with:
    pytest tests/test_django_views.py
"""

import os
import sys
import django

# Point Django at the project settings before importing anything Django-related.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src/taskproject")))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

from todos.models import Task


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------

def make_user(username="javi", password="TestPass123!"):
    # Helper function to create a user with the given username and password, returning the created User object.
    return User.objects.create_user(username=username, password=password)


def make_task(user, **kwargs):
    # Helper function to create a task for a given user with default values that can be overridden by kwargs, returning the created Task object.
    defaults = dict(
        title="Sample Task",
        description="A description",
        priority=Task.Priority.MEDIUM,
        status=Task.Status.PENDING,
        due_date=None,
        notes=None,
    )
    defaults.update(kwargs)
    return Task.objects.create(user=user, **defaults)


# ---------------------------------------------------------------------------
# Model unit tests
# ---------------------------------------------------------------------------

class TaskModelTest(TestCase):
    """Unit tests for the Task Django model."""

    def setUp(self):
        self.user = make_user()

    # 1. __str__ returns the title
    def test_str_returns_title(self):
        task = make_task(self.user, title="My Task")
        self.assertEqual(str(task), "My Task")

    # 2. Default status is Pending
    def test_default_status_is_pending(self):
        task = Task.objects.create(user=self.user, title="Defaults Test")
        self.assertEqual(task.status, Task.Status.PENDING)

    # 3. Default priority is Medium
    def test_default_priority_is_medium(self):
        task = Task.objects.create(user=self.user, title="Priority Test")
        self.assertEqual(task.priority, Task.Priority.MEDIUM)

    # 4. Notes field is optional (null/blank)
    def test_notes_field_is_optional(self):
        task = make_task(self.user, notes=None)
        self.assertIsNone(task.notes)

    # 5. Task ordering is newest-first (by -id)
    def test_ordering_newest_first(self):
        t1 = make_task(self.user, title="First")
        t2 = make_task(self.user, title="Second")
        tasks = list(Task.objects.filter(user=self.user))
        self.assertEqual(tasks[0].pk, t2.pk)
        self.assertEqual(tasks[1].pk, t1.pk)


# ---------------------------------------------------------------------------
# Helper function unit tests
# ---------------------------------------------------------------------------

class SummaryStatsTest(TestCase):
    """Unit tests for the _summary_stats and _count_overdue helpers."""

    def setUp(self):
        self.user = make_user()

    # 6. _summary_stats counts totals correctly
    def test_summary_stats_totals(self):
        from todos.views import _summary_stats
        from datetime import date

        tasks = [
            make_task(self.user, title="P1", status=Task.Status.PENDING),
            make_task(self.user, title="P2", status=Task.Status.PENDING),
            make_task(self.user, title="C1", status=Task.Status.COMPLETED),
        ]
        stats = _summary_stats(tasks)
        self.assertEqual(stats["total"], 3)
        self.assertEqual(stats["pending"], 2)
        self.assertEqual(stats["completed"], 1)

    # 7. _count_overdue ignores completed tasks even with past due dates
    def test_count_overdue_excludes_completed(self):
        from todos.views import _count_overdue
        from datetime import date, timedelta

        yesterday = date.today() - timedelta(days=1)
        pending_overdue = make_task(self.user, title="Overdue Pending", due_date=yesterday, status=Task.Status.PENDING)
        completed_overdue = make_task(self.user, title="Overdue Completed", due_date=yesterday, status=Task.Status.COMPLETED)

        count = _count_overdue([pending_overdue, completed_overdue])
        self.assertEqual(count, 1)

    # 8. _count_overdue ignores tasks with no due date
    def test_count_overdue_ignores_no_due_date(self):
        from todos.views import _count_overdue

        task = make_task(self.user, title="No Date", due_date=None, status=Task.Status.PENDING)
        self.assertEqual(_count_overdue([task]), 0)

    # 9. _summary_stats with empty list
    def test_summary_stats_empty_list(self):
        from todos.views import _summary_stats
        stats = _summary_stats([])
        self.assertEqual(stats["total"], 0)
        self.assertEqual(stats["pending"], 0)
        self.assertEqual(stats["completed"], 0)
        self.assertEqual(stats["overdue"], 0)


# ---------------------------------------------------------------------------
# Auth view tests
# ---------------------------------------------------------------------------

class AuthViewTest(TestCase):

    def setUp(self):
        self.client = Client()

    # 10. Login page returns 200 for anonymous user
    def test_login_page_loads(self):
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)

    # 11. Authenticated user hitting /login/ is redirected to task_list
    def test_login_redirects_authenticated_user(self):
        user = make_user()
        self.client.force_login(user)
        response = self.client.get(reverse("login"))
        self.assertRedirects(response, reverse("task_list"), fetch_redirect_response=False)

    # 12. Signup page loads for anonymous user
    def test_signup_page_loads(self):
        response = self.client.get(reverse("signup"))
        self.assertEqual(response.status_code, 200)

    # 13. Signup with mismatched passwords shows error, no user created
    def test_signup_mismatched_passwords_no_user_created(self):
        response = self.client.post(reverse("signup"), {
            "username": "newuser",
            "password1": "GoodPass123!",
            "password2": "WrongPass456!",
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn("Passwords do not match.", response.context["errors"])
        self.assertFalse(User.objects.filter(username="newuser").exists())

    # 14. Signup with duplicate username shows error
    def test_signup_duplicate_username_shows_error(self):
        make_user(username="taken")
        response = self.client.post(reverse("signup"), {
            "username": "taken",
            "password1": "GoodPass123!",
            "password2": "GoodPass123!",
        })
        self.assertEqual(response.status_code, 200)
        errors = response.context["errors"]
        self.assertTrue(any("already taken" in e for e in errors))


# ---------------------------------------------------------------------------
# Task view integration tests
# ---------------------------------------------------------------------------

class TaskViewTest(TestCase):

    def setUp(self):
        self.user = make_user()
        self.client = Client()
        self.client.force_login(self.user)

    # 15. Task list view returns 200 with correct template
    def test_task_list_view_loads(self):
        response = self.client.get(reverse("task_list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "todos/tasks_list.html")

    # 16. Task list view with no tasks shows zero total
    def test_task_list_empty_shows_zero_total(self):
        response = self.client.get(reverse("task_list"))
        self.assertEqual(response.context["total"], 0)

    # 17. Add task with a past due date re-renders form with error
    def test_add_task_past_due_date_returns_error(self):
        response = self.client.post(reverse("add_task"), {
            "title": "Past Task",
            "description": "",
            "priority": "Medium",
            "due_date": "2020-01-01",
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn("due_date", response.context["errors"])
        self.assertFalse(Task.objects.filter(title="Past Task").exists())

    # 18. Add task with empty title re-renders form with error
    def test_add_task_empty_title_returns_error(self):
        response = self.client.post(reverse("add_task"), {
            "title": "",
            "description": "No title here",
            "priority": "Low",
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn("title", response.context["errors"])

    # 19. Toggle a pending task → becomes Completed
    def test_toggle_pending_task_becomes_completed(self):
        task = make_task(self.user, title="Toggler", status=Task.Status.PENDING)
        self.client.post(reverse("toggle_task", args=[task.pk]))
        task.refresh_from_db()
        self.assertEqual(task.status, Task.Status.COMPLETED)

    # 20. Toggle a completed task → becomes Pending
    def test_toggle_completed_task_becomes_pending(self):
        task = make_task(self.user, title="Toggler2", status=Task.Status.COMPLETED)
        self.client.post(reverse("toggle_task", args=[task.pk]))
        task.refresh_from_db()
        self.assertEqual(task.status, Task.Status.PENDING)

    # 21. Edit task: valid POST updates title and description in the DB
    def test_edit_task_updates_fields(self):
        task = make_task(self.user, title="Original Title", description="Old desc")
        self.client.post(reverse("edit_task", args=[task.pk]), {
            "title": "Updated Title",
            "description": "New desc",
            "priority": "High",
            "due_date": "",
            "notes": "",
        })
        task.refresh_from_db()
        self.assertEqual(task.title, "Updated Title")
        self.assertEqual(task.description, "New desc")
        self.assertEqual(task.priority, Task.Priority.HIGH)

    # 22. task_stats view function returns correct JSON (call view directly)
    def test_task_stats_json_correct(self):
        from todos.views import task_stats
        from django.test import RequestFactory
        from django.contrib.auth.models import AnonymousUser

        make_task(self.user, title="S1", status=Task.Status.PENDING)
        make_task(self.user, title="S2", status=Task.Status.PENDING)
        make_task(self.user, title="S3", status=Task.Status.COMPLETED)

        factory = RequestFactory()
        request = factory.get("/tasks/stats")
        request.user = self.user
        response = task_stats(request)
        import json
        data = json.loads(response.content)
        self.assertEqual(data["total"], 3)
        self.assertEqual(data["pending"], 2)
        self.assertEqual(data["completed"], 1)

    # 23. Unauthenticated user is redirected away from the task list
    def test_task_list_requires_login(self):
        anon = Client()
        response = anon.get(reverse("task_list"))
        self.assertNotEqual(response.status_code, 200)

    # 24. User A cannot delete User B's task (404)
    def test_cannot_delete_another_users_task(self):
        other_user = make_user(username="other")
        task = make_task(other_user, title="Other's Task")
        response = self.client.post(reverse("delete_task", args=[task.pk]))
        self.assertEqual(response.status_code, 404)
        self.assertTrue(Task.objects.filter(pk=task.pk).exists())

    # 25. Sort by title returns tasks in alphabetical order
    def test_sort_by_title_alphabetical(self):
        make_task(self.user, title="Zebra Task")
        make_task(self.user, title="Apple Task")
        make_task(self.user, title="Mango Task")
        response = self.client.get(reverse("task_list") + "?sort=title")
        tasks = response.context["tasks"]
        titles = [t.title for t in tasks]
        self.assertEqual(titles, sorted(titles, key=str.lower))

    # 26. complete_task view marks task as Completed
    def test_complete_task_view(self):
        task = make_task(self.user, title="To Complete", status=Task.Status.PENDING)
        self.client.post(reverse("complete_task", args=[task.pk]))
        task.refresh_from_db()
        self.assertEqual(task.status, Task.Status.COMPLETED)
