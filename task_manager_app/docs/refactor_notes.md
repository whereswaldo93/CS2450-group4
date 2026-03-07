
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
