The following MVP does the following things:
	•	Add task ✅
	•	List tasks ✅
	•	Mark complete ✅
	•	JSON save/load ✅

It is built using typer. 

To run the program, first install typer by typing the following command on the terminal: 
	pip install typer


Make sure you are within the src folder.

cd task_manager_app/src/

Once it is installed, we can execute the program, which is cli.py



Type typer cli.py run on the terminal to see all the commands allowed. 

Should be able to see: 
	* add
	* list
	* complete
  
The add command has a required argument 'Title.' So make sure to include the title, otherwise you will see an error pop up. 

Run typer cli.py run add --help to be able to see the required and optional arguments.


typer cli.py run add "Buy groceries" outputs on the terminal: Added task #1: Buy groceries

There are two ways to check that our task is saved. One is going opening the data/tasks.json file, and the other is to run typer cli.py run list, which would display all the tasks added. If it is the first time running it, there should be no tasks.

The command, typer cli.py run list, should output: 

ID | Title                              | Status  | Due        | Priority
---+------------------------------------+---------+------------+---------
1  | Buy groceries                      | Pending |            | Medium  

We are seeing an empty Due date since we did not add one in the command that we run previously. To check that the due date can be added, we can add another task including the due-date option like this: 
	typer cli.py run add "Review open pull requests" --description "Check code quality and leave comments" --due-date 2026-02-13 --priority Medium

This should have created a new task. And run list should output: 
	ID | Title                     | Status  | Due        | Priority
	---+---------------------------+---------+------------+---------
	1  | Buy groceries             | Pending |            | Medium  
	2  | Review open pull requests | Pending | 2026-02-13 | Medium  

The priority is Medium by default. However, it could be changed to either Low or High. The due format is YYYY-MM-DD


After running the previosly stated commands, we should be able to see some changes made in the tasks.json file: 

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

Add more tasks: 
	typer cli.py run add "Write unit tests for task commands" --description "Cover add, list, and complete flows" --due-date 2026-02-14 --priority High
	typer cli.py run add "Update README usage section" --description "Add setup and CLI examples" --due-date 2026-02-15 --priority Medium
	typer cli.py run add "Submit milestone progress report" --description "Summarize completed work and blockers" --due-date 2026-02-16 --priority High
	typer cli.py run add "Plan next team meeting" --description "Draft agenda and assign owners" --due-date 2026-02-17 --priority Low
	typer cli.py run add "Clean backlog items" --description "Move done tasks and re-prioritize remaining" --due-date 2026-02-18 --priority Medium
	typer cli.py run add "Archive old notes" --description "Store outdated docs in archive folder" --due-date 2026-02-19 --priority Low

Output on the terminal: 
	Added task #3: Write unit tests for task commands
	Added task #4: Update README usage section
	Added task #5: Submit milestone progress report
	Added task #6: Plan next team meeting
	Added task #7: Clean backlog items
	Added task #8: Archive old notes

typer cli.py run list: 
	ID | Title                              | Status  | Due        | Priority
	---+------------------------------------+---------+------------+---------
	1  | Buy groceries                      | Pending |            | Medium  
	2  | Review open pull requests          | Pending | 2026-02-13 | Medium  
	3  | Write unit tests for task commands | Pending | 2026-02-14 | High    
	4  | Update README usage section        | Pending | 2026-02-15 | Medium  
	5  | Submit milestone progress report   | Pending | 2026-02-16 | High    
	6  | Plan next team meeting             | Pending | 2026-02-17 | Low     
	7  | Clean backlog items                | Pending | 2026-02-18 | Medium  
	8  | Archive old notes                  | Pending | 2026-02-19 | Low     


We can mark tasks as completed by running

typer cli.py run complete [TASK_ID]

where the argument "TASK_ID" is the id assigned to that task.

For example, if we run : 
	typer cli.py run complete 1 

Output on the terminal: 
	Marked task #1 as complete.


Now when we run typer cli.py run list, we see: 

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

Id 1 has a complete status now.