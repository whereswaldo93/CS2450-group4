# CS2450: Task Manager
A comprehensive task management solution tailored for modern college student. This application bridges the gap between academic deadlines, personal wellness, and professional growth in one unified dashboard.

### Key Features
- **Academic Tracking**: Organize tasks by priority, due date and status.
- **Restful API**:  Powered by Django REST Framework for seamless integration.
- **Structured Logging**: Meaningful traceability for debugging and maintenance.

### Logging & Observability
To ensure the application is maintainable and easy to debug, we using the following structured logging system.

**Log Levels & Usage**

| **Level** | **Usage Criteria** |
| --------- | ------------------ |
| **DEBUG** | Granular details for developers (e.g. raw API payloads and internal state)|
| **INFO**  | Key lifecycle events (e.g. App startup, successful DB writes, and user actions) |
| **WARNING** | Handled errors or unexpected behavior (e.g. failed logins and slow responses) |
| **ERROR** | Significant functional failures (e.g. database connection issues and 500 errors) |
| **CRITICAL** | System-wide failures (e.g. server unable to start) |

### Best Practices
When adding logs to the project, import the standard logger and use the `extra` parameter to provide searchable context:
```python
import logging
logger = logging.getLogger('task_manager')

# Example: Logging a state change
logger.info("Task status updated", extra={'task_id': 42, 'new_status': 'Completed'})
```
---
### Running the Project
**Prerequisites**

- **Python**: 3.8 or higher.
- **pip**: Package management tool.

### Installation & Setup

1. **Clone the repository**: 
```bash
   git clone https://github.com/whereswaldo93/CS2450-group4
   cd CS2450-group4
```

2. **Create and activate a virtual environment (optional)**:
```bash
   # Create a virtual environment
   python -m venv venv
   
   # Activate the virtual environment
   # On Windows
   .\venv\Scripts\activate

   # On macOS/Linux
   source venv/bin/activate
```

3. **Install dependencies**:
```bash
   pip install -r requirements.txt
```
---
### Testing & Coverage   

**Running Unit Tests**

  To run all unit tests, use the following command: 
```bash
  python -m unittest discover -f
```

**Running Coverage Tests**

To run tests with coverage measurement, follow these steps:

1. **Install the `coverage` package if not already installed**:
```bash
   pip install coverage
```
   
2. **Run tests with coverage**:
```bash
   coverage run -m unittest discover -s task_manager_app/tests -p "*.py"
```

3. **Generate a coverage report**:
`coverage report`

4. **Generate an HTML report for detailed coverage**:
`coverage html`
You can find the detailed report in the htmlcov directory. Open index.html in your web browser to view it.
---

### Dependencies
- **Django**: `Django>=5.0,<6.1`
- **Django REST framework**: `djangorestframework>=3.14,<4.0`
- **Production server**: `gunicorn>=21.0`
- **Environment Management**: `python-dotenv>=1.0,<2.0`
- **JSON Logging**: `python-json-logger`

### Group 4 Contributors
  - Javi Gutierrez, Kyle Bluemel, Jake Michie and Osvaldo Saldana
---