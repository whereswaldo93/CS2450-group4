import tkinter as tk
from tkinter import ttk, messagebox
from controllers.gui_controller import GUIController

class GUIView:
    def __init__(self, gui_controller: GUIController) -> None:
        self.gui_controller = gui_controller
        self.root = tk.Tk()
        self.root.title("Task Manager")
        self.root.geometry("800x600")
        self.root.resizable(True, True)

        self._create_widgets()
        self.refresh_tasks()

    def _create_widgets(self) -> None:
        #------Input Frame------#
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill="both", expand=True)

        input_frame = ttk.LabelFrame(main_frame, text="Add Task", padding="10")
        input_frame.pack(fill="x", padx=10, pady=10)

        ttk.Label(input_frame, text="Title:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.title_entry = ttk.Entry(input_frame, width=25)
        self.title_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(input_frame, text="Description:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.description_entry = ttk.Entry(input_frame, width=25)
        self.description_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(input_frame, text="Due Date").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.due_date_entry = ttk.Entry(input_frame, width=25)
        self.due_date_entry.grid(row=2, column=1, padx=5, pady=5)
        self.due_date_entry.insert(0, "YYYY-MM-DD")

        ttk.Label(input_frame, text="Priority").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.priority_combo = ttk.Combobox(
            input_frame, 
            values=["Low", "Medium", "High"], 
            state="readonly",
            width=22
            )
        self.priority_combo.grid(row=3, column=1, padx=5, pady=5)
        self.priority_combo.set("Medium")

        add_button = ttk.Button(input_frame, text="Add Task", command=self.add_task)
        add_button.grid(row=4, column=0, columnspan=2, pady=10)

        input_frame.columnconfigure(1, weight=1)
        input_frame.rowconfigure(3, weight=1)

        table_frame = ttk.Frame(main_frame, padding="10")
        table_frame.pack(fill="both", expand=True)

        columns = ("ID", "Title", "Description", "Status", "Due Date", "Priority")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")

        self.tree.heading("ID", text="ID")
        self.tree.heading("Title", text="Title")
        self.tree.heading("Description", text="Description")
        self.tree.heading("Status", text="Status")
        self.tree.heading("Due Date", text="Due Date")
        self.tree.heading("Priority", text="Priority")

        self.tree.column("ID", width=50, anchor="center")
        self.tree.column("Title", width=150, anchor="w")
        self.tree.column("Description", width=200, anchor="w")
        self.tree.column("Status", width=100, anchor="center")
        self.tree.column("Due Date", width=120, anchor="center")
        self.tree.column("Priority", width=100, anchor="center")

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        action_frame = ttk.Frame(main_frame)
        action_frame.pack(fill="x", padx=10, pady=10)

        ttk.Button(action_frame, text="Refresh", command=self.refresh_tasks).pack(side="left", padx=5)
        ttk.Button(action_frame, text="Complete Task", command=self.complete_task).pack(side="left", padx=5)
        ttk.Button(action_frame, text="Delete Task", command=self.delete_task).pack(side="left", padx=5)

        self.status_label = ttk.Label(main_frame, text="Ready")
        self.status_label.pack(anchor="w")

    def refresh_tasks(self) -> None:
        for item in self.tree.get_children():
            self.tree.delete(item)

        tasks = self.gui_controller.list_tasks()
        
        for task in tasks:
            self.tree.insert(
                "", 
                "end", 
                values=(
                    task.task_id, 
                    task.title, 
                    task.description, 
                    task.status.value, 
                    task.due_date or "", 
                    task.priority.value,
                ),
            )
        self.status_label.config(text=f"Loaded {len(tasks)} tasks.")

    def add_task(self) -> None:
        title = self.title_entry.get().strip()
        description = self.description_entry.get().strip()
        due_date = self.due_date_entry.get().strip()
        priority = self.priority_combo.get()

        if due_date == "YYYY-MM-DD" or  due_date == "":
            due_date = None

        try:
            task = self.gui_controller.add_task(title, description, due_date, priority)
            self.status_label.config(text=f"Task #{task.task_id}: {task.title} added successfully.")
            self.clear_inputs()
            self.refresh_tasks()
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def complete_task(self) -> None:
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a task to complete.")
            return

        item = self.tree.item(selected[0])
        task_id = int(item["values"][0])

        result = self.gui_controller.complete_task(task_id)

        if result == "completed":
            messagebox.showinfo("Success", f"Task #{task_id} marked as complete.")
        elif result == "already_complete":
            messagebox.showinfo("Info", f"Task #{task_id} is already complete.")
        else:
            messagebox.showerror("Error", f"Task #{task_id} was not found.")

        self.refresh_tasks()

    def delete_task(self) -> None:
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a task to delete.")
            return

        item = self.tree.item(selected[0])
        task_id = int(item["values"][0])

        confirmed = messagebox.askyesno(
            "Confirm Delete", 
            f"Are you sure you want to delete Task #{task_id}?"
            )
        if not confirmed:
            return
        
        deleted = self.gui_controller.delete_task(task_id)

        if deleted:
            self.status_label.config(text=f"Task #{task_id} deleted successfully.")
            self.refresh_tasks()
        else:
            messagebox.showerror("Error", f"Task #{task_id} was not found.")

    def clear_inputs(self) -> None:
        self.title_entry.delete(0, tk.END)
        self.description_entry.delete(0, tk.END)
        self.due_date_entry.delete(0, tk.END)
        self.due_date_entry.insert(0, "YYYY-MM-DD")
        self.priority_combo.set("Medium")

    def run(self) -> None:
        self.root.mainloop()