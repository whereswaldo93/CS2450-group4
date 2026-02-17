# MVP Validation

## Implemented MVP Features
- Add task
- List tasks
- Mark task as complete
- JSON save/load

The CLI is built with `typer`.

## Setup
1. Install Typer:

```bash
pip install typer
```

2. Move into the source directory:

```bash
cd task_manager_app/src
```

3. Show available commands:

```bash
typer cli.py run
```

Expected commands:
- `add`
- `list`
- `complete`

## Command Notes
- `add` requires a title argument.
- Run `typer cli.py run add --help` to see required and optional parameters.
- Due date format is `YYYY-MM-DD`.
- Priority defaults to `Medium` and accepts `Low`, `Medium`, or `High`.

## Manual Validation Scenarios
The examples below assume a fresh `data/tasks.json` file.

### 1) Add a basic task
```bash
typer cli.py run add "Buy groceries"
```

Expected output:
```text
Added task #1: Buy groceries
```

### 2) List tasks
```bash
typer cli.py run list
```

Expected output:
```text
ID | Title         | Status  | Due | Priority
---+---------------+---------+-----+---------
1  | Buy groceries | Pending |     | Medium
```

### 3) Add a task with optional fields
```bash
typer cli.py run add "Review open pull requests" --description "Check code quality and leave comments" --due-date 2026-02-13 --priority Medium
```

Expected output:
```text
Added task #2: Review open pull requests
```

List again:
```bash
typer cli.py run list
```

Expected output:
```text
ID | Title                     | Status  | Due        | Priority
---+---------------------------+---------+------------+---------
1  | Buy groceries             | Pending |            | Medium
2  | Review open pull requests | Pending | 2026-02-13 | Medium
```

### 4) Validate JSON persistence
Open `data/tasks.json` and confirm entries were saved. Example:

```json
[
  {
    "id": 1,
    "title": "Buy groceries",
    "description": "",
    "status": "Pending",
    "priority": "Medium",
    "due_date": null,
    "created_at": "2026-02-10T16:50:38",
    "updated_at": "2026-02-10T16:50:38"
  },
  {
    "id": 2,
    "title": "Review open pull requests",
    "description": "Check code quality and leave comments",
    "status": "Pending",
    "priority": "Medium",
    "due_date": "2026-02-13",
    "created_at": "2026-02-10T16:53:13",
    "updated_at": "2026-02-10T16:53:13"
  }
]
```

### 5) Add more tasks
```bash
typer cli.py run add "Write unit tests for task commands" --description "Cover add, list, and complete flows" --due-date 2026-02-14 --priority High
typer cli.py run add "Update README usage section" --description "Add setup and CLI examples" --due-date 2026-02-15 --priority Medium
typer cli.py run add "Submit milestone progress report" --description "Summarize completed work and blockers" --due-date 2026-02-16 --priority High
typer cli.py run add "Plan next team meeting" --description "Draft agenda and assign owners" --due-date 2026-02-17 --priority Low
typer cli.py run add "Clean backlog items" --description "Move done tasks and re-prioritize remaining" --due-date 2026-02-18 --priority Medium
typer cli.py run add "Archive old notes" --description "Store outdated docs in archive folder" --due-date 2026-02-19 --priority Low
```

Expected output:
```text
Added task #3: Write unit tests for task commands
Added task #4: Update README usage section
Added task #5: Submit milestone progress report
Added task #6: Plan next team meeting
Added task #7: Clean backlog items
Added task #8: Archive old notes
```

### 6) Mark a task complete
```bash
typer cli.py run complete 1
```

Expected output:
```text
Marked task #1 as complete.
```

List again:
```bash
typer cli.py run list
```

Expected output:
```text
ID | Title                              | Status   | Due        | Priority
---+------------------------------------+----------+------------+---------
1  | Buy groceries                      | Complete |            | Medium
2  | Review open pull requests          | Pending  | 2026-02-13 | Medium
3  | Write unit tests for task commands | Pending  | 2026-02-14 | High
4  | Update README usage section        | Pending  | 2026-02-15 | Medium
5  | Submit milestone progress report   | Pending  | 2026-02-16 | High
6  | Plan next team meeting             | Pending  | 2026-02-17 | Low
7  | Clean backlog items                | Pending  | 2026-02-18 | Medium
8  | Archive old notes                  | Pending  | 2026-02-19 | Low
```

