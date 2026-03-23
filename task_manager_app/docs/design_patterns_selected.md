Design Patterns Selection

1. Editing Tasks

Pattern used: Command Pattern

What Problem Does it Solve? Right now editing a task is overwriting it's attributes. We intend to implement an "Undo action(s)" button. As it stands, previous states are lost immediately. The Command Pattern will solve this by encapsulating an operation into an object with information capable of reversing the action. 

Is it necessary, or would a basic implementation work? Again as it stands, our basic implementation is fully functioning and operational until it becomes necessary to undo any actions. An undo function makes this implementation necessary.

Implementation Pseudocode:

from typing import Protocol
from models.task import Task

class Command(Protocol):
    def execute(self) -> None: ...
    def undo(self) -> None: ...

class EditTaskCommand:
    def __init__(self, task: Task, new_data: dict):
        self.task = task
        self.new_data = new_data
        self.previous_data = task.to_dict() # Store old state for undo

    def execute(self) -> None:
        if "title" in self.new_data:
            self.task.title = self.new_data["title"]

    def undo(self) -> None:
        self.task.title = self.previous_data["title"]

2. Mark "Done" on Tasks

Pattern used: Observer Patterm

What problem does it solve? Our current complete_task() function updates TaskStatus. Looking at the backlog, our task completion will also need to trigger other effects like archiving tasks, updating a progress bar or other analytics, and notifying group members.

Is it necessary, or would a basic implementation work? If marking a task "done" only needed to change a string/Enum then our current method works. Adding any additional logic into TaskManager.complete_task() would violate the Single Responsibility Principle. So a basic implementation will not be the best option.

Implementation Pseudocode: 

class TaskObserver(Protocol):
    def update(self, task: Task, event_type: str) -> None: ...

class TaskManager:
    def __init__(self, repo):
        self.repo = repo
        self._observers: list[TaskObserver] = []

    def add_observer(self, observer: TaskObserver):
        self._observers.append(observer)

    def complete_task(self, task_id: int) -> str:
        task = self.get_task(task_id)
        if task and task.status != TaskStatus.COMPLETED:
            task.status = TaskStatus.COMPLETED
            self.repo.save_tasks(self.list_tasks())
            
            for obs in self._observers:
                obs.update(task, "COMPLETED")
            return "completed"
        return "already_complete"

class AnalyticsTracker:
    def update(self, task: Task, event_type: str):
        if event_type == "COMPLETED":
            print(f"Analytics: Incrementing completed count for user.")

3. Filtering Task

Pattern used: Specification Pattern

What Problem Does it Solve? Users will need to filter tasks by various metrics. This will require specific implementation to not rely on multiple if/elif statements or other long, difficult to test code.

Is it necessary or would a basic implementation work?
A basic implementation will work for a single filter, such as the priority of a task or specific due date. If a user instead tries to combine filters or sort by a metric, a simple implementation will become rapidly more complex when using Booleans. the Specification Pattern lets us create filter classes that can be chained together with logical operators.

Implementation pseudocode:

from typing import Protocol

class TaskSpecification(Protocol):
    def is_satisfied_by(self, task: Task) -> bool: ...

class PrioritySpecification:
    def __init__(self, target_priority: str):
        self.target_priority = target_priority

    def is_satisfied_by(self, task: Task) -> bool:
        return task.priority.value == self.target_priority

class StatusSpecification:
    def __init__(self, target_status: str):
        self.target_status = target_status

    def is_satisfied_by(self, task: Task) -> bool:
        return task.status.value == self.target_status

class AndSpecification:
    def __init__(self, spec1: TaskSpecification, spec2: TaskSpecification):
        self.spec1 = spec1
        self.spec2 = spec2

    def is_satisfied_by(self, task: Task) -> bool:
        return self.spec1.is_satisfied_by(task) and self.spec2.is_satisfied_by(task)

# In the Model (TaskManager):
class TaskManager:
    # ...
    def filter_tasks(self, spec: TaskSpecification) -> list[Task]:
        return [task for task in self.repo.load_tasks() if spec.is_satisfied_by(task)]

