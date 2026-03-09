# Validation & Testing Scenarios

**Application:** Task Manager (GUI & CLI)
**Testing Goal:** Confirm refactored MVC architecture functions correctly and demonstrates SOLID principles.

---

## Scenario 1: GUI Interaction - Add a Task
**Objective:** Verify that a user can successfully add a task through the Tkinter GUI and see it rendered in the Treeview.
* **Steps:**
    1. Launch the application via `python main.py`.
    2. Enter "Write Unit Tests" in the Title field.
    3. Enter "Cover TaskManager logic" in the Description field.
    4. Enter "2026-03-15" in the Due Date field.
    5. Select "High" from the Priority dropdown.
    6. Click "Add Task".
* **Expected Result:** The status label updates to "Task #1: Write Unit Tests added successfully." The inputs clear, and the new task appears as a row in the Treeview table.
* **Actual Result:** Passed. Task appeared in Treeview and saved to JSON.
* **Observations:** The `refresh_tasks` method correctly pulled the new data from the `GUIController`.

## Scenario 2: GUI Interaction - Add a Task with Invalid Date
**Objective:** Validate that business logic errors in the Model are correctly caught and displayed by the View.
* **Steps:**
    1. Enter "Invalid Date Task" in the Title field.
    2. Enter "15-03-2026" (DD-MM-YYYY instead of YYYY-MM-DD) in the Due Date field.
    3. Click "Add Task".
* **Expected Result:** A Tkinter `messagebox.showerror` pops up displaying: "Invalid due date format. Use YYYY-MM-DD." The task is not added to the Treeview.
* **Actual Result:** Passed. The error correctly bubbled up from `TaskManager.validate_due_date` to `gui_view.add_task`.

## Scenario 3: MVC Flow - Mark Task as Complete
**Objective:** Confirm that selecting a task in the UI correctly updates the underlying model state and refreshes the display.
* **Steps:**
    1. Select the previously created "Write Unit Tests" task in the Treeview.
    2. Click the "Complete Task" button.
* **Expected Result:** A success messagebox appears. The Treeview refreshes, and the "Status" column for that task changes from "Pending" to "Completed". 
* **Actual Result:** Passed.
* **Observations:** The controller correctly mapped the UI `task_id` to the model's `complete_task` method. 

## Scenario 4: MVC Flow - Delete a Task
**Objective:** Verify the delete operation removes the task from both the UI and the persistent JSON storage.
* **Steps:**
    1. Select a task in the Treeview.
    2. Click "Delete Task".
    3. Click "Yes" on the confirmation prompt.
    4. Open the `tasks.json` file in a text editor.
* **Expected Result:** The task instantly disappears from the Treeview. The `tasks.json` file no longer contains the JSON object for that task.
* **Actual Result:** Passed.

## Scenario 5: SOLID Benefit (CLI vs. GUI)
**Objective:** Demonstrate that the `TaskManager` and `Task` models can be used by entirely different interfaces without any modification to the models themselves (Single Responsibility & Open/Closed Principles).
* **Steps:**
    1. Open the terminal and use the Typer CLI to add a task: `python cli_controller.py add "CLI Task" -d "Added from terminal" -p High`.
    2. Keep the GUI window open (or open it if closed) and click the "Refresh" button.
* **Expected Result:** The task added via the command line immediately appears in the Tkinter GUI.
* **Actual Result:** Passed. 
* **Observations:** Because `cli_controller` and `gui_controller` both route to `TaskController` and read from the same `TaskFileRepo`, the business logic remains strictly isolated from the presentation layer.
