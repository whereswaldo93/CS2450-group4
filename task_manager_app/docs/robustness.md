#### Date modified: 04/21/2026
<ol>
  <li>Smell 1: priority_order in task_list_page_context() was built inline on every request. Added PRIORITY_ORDER as a property of TaskConfig in task_config.py. Built once when it is first created and reused. Adheres to Singleton design pattern.</li>
  <li>Smell 2: in task_view.py add_task() and edit_task() had duplicated logic. Extracted into data_parser.py and both views now call this. Adheres to Singleton design pattern.</li>
  <li>Smell 3: task_view.py included 6 seperate except blocks with repeated error responses and slightly different wording. Added db_error_response(action) as a statci method on TaskConfig singleton. Adheres to Singleton design pattern. </li>
  <li>Smell 4: TaskFileRepo allows multiple instances to point to the same file. Enforced path-based Singleton pattern with TaskFileRepoSingelton using a registry to only allow one instance per file path.</li>
  <li>Smell 5: Modules were using different base names for loggers by using todos and taskproject.todos. Introduced AppLogger singleton to enforce unified and consistent logging heirarchy across app.</li>
  <li>3 Additional fixes made to ensure all files adhere to Singleton Design Pattern: apps.py was using logging.getLogger("todos") (raw) replaced with AppLogger.get_logger(__name__) (goes through smae singleton as other views). settings.py needed "todos" namespace registered. task_view.py was using raw inline JsonResponse for error path. Added TaskConfig.db_json_error_response() static method and updated task_stats to call it.</li>
</ol>
