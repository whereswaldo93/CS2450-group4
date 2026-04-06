# CS2450 ToDo - Task Manager App

## Running Tests

This project uses the `unittest` framework for testing. You can run the tests and check the coverage using the following steps:

### Prerequisites

- Make sure you have Python installed (version 3.8 or higher).
- Make sure you have `pip` installed for package management.

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/whereswaldo93/CS2450-group4
   cd CS2450-group4
   
2. Install the required packages:
   `pip install -r requirements.txt`
   
4. (Optional) Create and activate a virtual environment:
   ```
    # Create a virtual environment
    python -m venv venv
    
    # Activate the virtual environment
    # On Windows
    .\venv\Scripts\activate
    # On macOS/Linux
    source venv/bin/activate
   ```

### Running Unit Tests
  To run all unit tests, use the following command: 
  ```bash
  python -m unittest discover -f

```

### Running Coverage Tests
To run tests with coverage measurement, follow these steps:

1. Install the `coverage` package (if not already installed):
   ```bash
    pip install coverage
    ```
   
2. Run tests with coverage:
   ```
    coverage run -m unittest discover -s task_manager_app/tests -p "*.py"

3. Generate a coverage report:
`coverage report`

4. (Optional) Generate an HTML report for detailed coverage:
`coverage html`
You can find the detailed report in the htmlcov directory. Open index.html in your web browser to view it.

### Dependencies
This project requires the following dependencies to run:
- **Django**: Django>=5.0,<6.1
- **Django REST framework**: djangorestframework>=3.14,<4.0
- **Production server**: gunicorn>=21.0
