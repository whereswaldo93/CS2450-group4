
#### Date modified: 2/28/2026
<ol>
  <li>Created controllers, models, utils and views folders along with the files config.py and main.py</li>
  <li>Started removing code from the cli.py, then pasting into file_handler.py, task.py and config.py</li>
  <li>All changes saved so far are saved on my, Osvaldo's, desktop while I separate everything and run debugging to ensure the app works like intended.</li>
  <li>I can push my updates in time for the pre-release scheduled this upcoming Monday.</li>
</ol>

#### Date modified: 03/02/2026
<ol>
  <li>Finished refactoring cli.py file into the strucutre outlined in Milestone 3.</li>
  <li>Applying SOLID principles was not focused on during this first week, leaving that task unfinished</li>
  <li>GUI integration has not been started yet either and will be focused on during this second week of the project milestone.</li>
  <li>I pushed all changes today and will notify Jake so he may begin some testing.</li>
</ol>

#### Date modified: 03/05/2026
<ol>
  <li>We refactored the project to better follow SOLID principles and improve separation of concerns without changing functionality.</li>
  <li>File persistence was moved to a TaskFileRepository in file_handler.py, giving it a single responsibility for loading and saving tasks.</li> 
  <li>The TaskManager now handles only task-related business logic and receives the repository as a dependency instead of accessing file operations directly.</li> 
  <li>The task_controller was updated to create and use the TaskManager, coordinating between the CLI and the model.</li>
</ol>

#### Date modified: 03/07/2026
<ol>
  <li>Added a Tkinter GUI, replacing the command-line interface with a graphical interface that allows users to manage tasks through windows, buttons, and input fields instead of typed commands.</li>
  <li>The GUI was integrated without changing the underlying business logic, because it communicates with the existing TaskController and TaskManager layers.</li> 
  <li>A new branch was created and used while implementing the GUI, once changes were finalized I, Osvaldo, merged to the main branch</li> 
  <li>I will alert Jake for testing.</li>
</ol>

#### Date modified: 04/21/2026
<ol>
  <li>Smell 1: priority_order in task_list_page_context() was built inline on every request. Added PRIORITY_ORDER as a property of TaskConfig in task_config.py. Built once when it is first created and reused. Adheres to Singleton design pattern.</li>
  <li>Smell 2: in task_view.py add_task() and edit_task() had duplicated logic. Extracted into data_parser.py and both views now call this. Adheres to Singleton design pattern.</li>
  <li>Smell 3: task_view.py included 6 seperate except blocks with repeated error responses and slightly different wording. Added db_error_response(action) as a statci method on TaskConfig singleton. Adheres to Singleton design pattern. </li>
  <li>Smell 4: TaskFileRepo allows multiple instances to point to the same file. Enforced path-based Singleton pattern with TaskFileRepoSingelton using a registry to only allow one instance per file path.</li>
  <li>Smell 5: Modules were using different base names for loggers by using todos and taskproject.todos. Introduced AppLogger singleton to enforce unified and consistent logging heirarchy across app.</li>
  <li>3 Additional fixes made to ensure all files adhere to Singleton Design Pattern: apps.py was using logging.getLogger("todos") (raw) replaced with AppLogger.get_logger(__name__) (goes through smae singleton as other views). settings.py needed "todos" namespace registered. task_view.py was using raw inline JsonResponse for error path. Added TaskConfig.db_json_error_response() static method and updated task_stats to call it.</li>
</ol>
