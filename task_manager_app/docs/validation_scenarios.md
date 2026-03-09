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

## Scenario 5: SOLID Benefits - Single Responsibility Principle
**Objective:** Verify that the application layers are strictly separated. Modifying the underlying data source directly should seamlessly reflect in the View upon request, proving the View and Controller are completely decoupled from data persistence mechanics.
* **Steps:**
    1. Launch the GUI application and observe the current list of tasks.
    2. Outside of the application, open the `tasks.json` data file in a text editor.
    3. Manually edit the `"title"` or `"description"` of an existing task and save the file.
    4. Return to the GUI application and click the "Refresh" button.
* **Expected Result:** The GUI immediately updates the Treeview to reflect the manual changes made to the JSON file without needing a restart.
* **Actual Result:** Passed.
* **Observations:** This demonstrates SRP. The `GUIView` is strictly responsible for rendering, `TaskFileRepo` strictly handles file I/O, and `GUIController` bridges them. Because of this separation, external changes to the data state are handled gracefully.

<img width="720" height="120" alt="image" src="https://github.com/user-attachments/assets/04fe30bb-7aa1-408c-8a2c-8354aa4abbad" />
<img width="619" height="399" alt="image" src="https://github.com/user-attachments/assets/5ecdc150-6ca6-45a3-a549-e0dea0d4c1c2" />
<img width="775" height="365" alt="image" src="https://github.com/user-attachments/assets/c9db03a1-3976-42a0-b651-c8ed2a90ce9d" />
<img width="770" height="332" alt="image" src="https://github.com/user-attachments/assets/58ffc95c-9577-48c1-9d8f-1e7433f94b4c" />
<img width="406" height="263" alt="image" src="https://github.com/user-attachments/assets/25507eaa-76db-49dc-92f3-5bdbdc61cccf" />
<img width="783" height="323" alt="image" src="https://github.com/user-attachments/assets/e66c2228-3505-4e35-a2d5-2ea67f58fe3d" />

