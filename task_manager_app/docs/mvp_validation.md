# MVP Validation
## Task Manager Application

### Implemented MVP Features
- Add a new task with:
  - title
  - description
  - due date
  - priority
- Display all saved tasks in the GUI
- Mark a selected task as complete
- Delete a selected task
- Save tasks to a JSON file
- Reload saved tasks when the application starts

The GUI is built with `Tkinter`.

---

### Validation Criteria
The MVP is considered valid if the application satisfies the following conditions:

1. Users can create a task successfully.
2. Users can see tasks displayed in the GUI.
3. Users can mark tasks as complete.
4. Users can delete tasks.
5. Task data persists after closing and reopening the application.
6. Invalid input, such as an empty title or incorrect due date format, is handled with an error message.
7. The GUI can be used without relying on the command-line interface.

---

### Test Scenarios and Results
####The examples below assume a fresh `data/tasks.json` file.

| Test Case | Expected Result | Actual Result | Status |
|----------|-----------------|---------------|--------|
| Add a task with valid title, description, due date, and priority | Task is saved and shown in the GUI | Task was added and displayed correctly | Pass |
| Add a task with an empty title | Error message is shown and task is not saved | Error message displayed correctly | Pass |
| Add a task with invalid due date format | Error message is shown | Error message displayed correctly | Pass |
| View all tasks | All saved tasks are listed in the GUI | Tasks loaded successfully | Pass |
| Complete a selected task | Task status changes to Complete | Task updated successfully | Pass |
| Complete an already completed task | User is informed task is already complete | Correct message shown | Pass |
| Delete a selected task | Task is removed from the system | Task deleted successfully | Pass |
| Restart application after adding tasks | Previously saved tasks still appear | Tasks persisted successfully | Pass |

---

### Evidence of MVP Success
The application demonstrates the core value of a task manager by allowing users to manage tasks through a graphical interface. The backend logic, controller layer, and JSON persistence all function correctly together. The system satisfies the basic requirements needed for an initial usable release.

---

### Current Limitations
Although the MVP is functional, it has several limitations:

- No edit task feature is currently available
- No search or filtering options are implemented
- The interface is basic and can be improved visually
- Long text handling in task table columns is limited
- The application currently supports local file storage only

---

### Conclusion
The Task Manager Application MVP is validated as successful because it delivers the essential features required for task management in a working GUI-based desktop application. Users can add, view, complete, and delete tasks, and task data persists between sessions. Future versions can build on this MVP by adding editing, filtering, improved layout, and more advanced storage options.

---

### Running the Application
python main.py

---

### Validate JSON persistence
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
  }
]
