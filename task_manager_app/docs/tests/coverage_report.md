# Test Coverage Report

**Generated:** 2026-04-06  
**Framework:** pytest + pytest-cov  
**Total Coverage: 80%**

---

## Coverage Summary

| Module | Statements | Missed | Coverage |
|---|---|---|---|
| `core/__init__.py` | 0 | 0 | 100% |
| `core/asgi.py` | 4 | 4 | 0% |
| `core/settings.py` | 27 | 2 | 93% |
| `core/urls.py` | 3 | 0 | 100% |
| `core/wsgi.py` | 4 | 4 | 0% |
| `todos/__init__.py` | 0 | 0 | 100% |
| `todos/admin.py` | 7 | 0 | 100% |
| `todos/apps.py` | 3 | 0 | 100% |
| `todos/file_task.py` | 43 | 4 | 91% |
| `todos/migrations/0001_initial.py` | 7 | 0 | 100% |
| `todos/models.py` | 21 | 0 | 100% |
| `todos/urls.py` | 5 | 0 | 100% |
| `todos/views.py` | 182 | 46 | 75% |
| **TOTAL** | **306** | **60** | **80%** |

---

## How to regenerate

```bash
cd task_manager_app
python3 -m pytest tests/test_django_views.py tests/test_task.py tests/test_views.py \
  --cov=src/taskproject/todos \
  --cov=src/taskproject/core \
  --cov-report=html:docs/tests/htmlcov \
  --cov-report=term-missing
```

Open `docs/tests/htmlcov/index.html` in a browser to view the interactive HTML report.

---

## Well-tested areas

**`todos/models.py` — 100%**  
Every line of the Task model is exercised. Tests cover `__str__`, default field values (status = Pending, priority = Medium), the optional notes field, and the `-id` ordering.

**`todos/admin.py` — 100%**, **`todos/urls.py` — 100%**, **`todos/migrations/` — 100%**  
These are structural/config files. Full coverage confirms they load without errors.

**`todos/file_task.py` — 91%**  
The CLI-facing `Task` dataclass (separate from the Django ORM model) is well tested. Validation for title, priority, date format, and past-date rejection are all covered. The 4 missed lines are the `to_dict` `else` branch (line 66) and `from_dict` edge cases — minor gaps.

**`core/settings.py` — 93%**  
Only 2 lines missed: the `RENDER_EXTERNAL_HOSTNAME` environment variable branch (line 40) and the `sys.path` guard (line 22), which only run in specific deployment environments and cannot be triggered in a local test run.

---

## Areas needing improvement

**`todos/views.py` — 75% (46 lines missed)**  
This is the most critical gap. The uncovered lines fall into three categories:

1. **Sorting helpers** (lines 45, 47, 50, 52, 54, 64, 66) — the `due_date` and `priority` sort branches in `_task_list_page_context`. Tests cover title sort but not these two.
2. **`note_create` view** (lines 314–322) — the notes-via-view workflow is not yet tested at the HTTP level (Osvaldo is adding note tests; this will close the gap).
3. **`edit_task` error re-render path** (lines 223–246) — the view re-renders with errors on a bad title, but the template has a bug (`{% url 'edit_task' task.id %}` fails when the task object is passed incorrectly in the error context). This is a pre-existing bug in the template that prevents testing the error branch via the test client.
4. **`hello_html_view`** (line 130) — the `/` landing page is not tested directly.
5. **`add_task` invalid date format branch** (lines 155–156) — the `except ValueError` for a malformed date string (e.g. `"not-a-date"`) is not exercised.

**`core/asgi.py` and `core/wsgi.py` — 0%**  
These are server entry-point files. They're not executed during testing and are typically excluded from coverage targets. They have no testable logic.

---

## Key findings

1. **The Django ORM layer is solid.** Every model field, default, and relationship is covered. The `Task` model is the core data structure and it has zero missed lines.

2. **The view helper functions are now tested at the unit level.** `_summary_stats` and `_count_overdue` are pure functions that were previously untested. Tests 6–9 expose an important edge case: a completed task with a past due date must **not** count as overdue — this is the correct behavior and the tests confirm it holds.

3. **Cross-user data isolation is tested.** Test 24 (`test_cannot_delete_another_users_task`) confirms that User A cannot delete User B's tasks — the view correctly returns 404. This is a security-relevant invariant that had no prior test coverage.

4. **A pre-existing template bug was discovered** during test writing. The `edit_task` view passes `task` in the error context but the template calls `{% url 'edit_task' task.id %}` where `task.id` resolves to an empty string when the task object is the unsaved form data. This causes a `NoReverseMatch` crash when posting with an empty title. The bug is in the template, not the view logic — the view correctly prevents saving. This was uncovered by attempting to write test 21.

5. **The `note_create` view (0% coverage) is the biggest remaining gap**, but it is being addressed separately by a teammate. Once those tests land, overall coverage should reach ~85%.
