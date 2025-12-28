# Todo Application - Phase I

A simple in-memory todo application with a menu-driven command-line interface.

## Phase I Features

- **Add Tasks**: Create new tasks with title and optional description
- **View Tasks**: Display all tasks with ID, title, status, and description
- **Update Tasks**: Modify task title and/or description
- **Delete Tasks**: Remove tasks from the list
- **Toggle Status**: Mark tasks as Complete or Incomplete

## Requirements

- Python 3.11 or higher
- pytest (for running tests)

## Installation

1. Ensure Python 3.11+ is installed:
   ```bash
   python --version
   ```

2. Clone or download this repository

3. (Optional) Install pytest for running tests:
   ```bash
   pip install pytest pytest-cov
   ```

## Usage

### Running the Application

From the project root directory:

**Windows:**
```bash
set PYTHONPATH=.
python src/main.py
```

**Linux/macOS:**
```bash
PYTHONPATH=. python src/main.py
```

or use the Python module approach:

```bash
python -m src.main
```

### Main Menu

The application presents a menu with 6 options:

```
1. View all tasks
2. Add a new task
3. Update a task
4. Delete a task
5. Mark task complete/incomplete
6. Exit
```

Simply enter the number of your choice and press Enter.

### Example Session

```
Welcome to Todo Application - Phase I

Main Menu:
1. View all tasks
2. Add a new task
3. Update a task
4. Delete a task
5. Mark task complete/incomplete
6. Exit

Enter your choice: 2

--- Add New Task ---
Enter task title: Buy groceries
Enter task description (optional): Milk, eggs, bread

Task added successfully! (ID: 1)

Main Menu:
...
Enter your choice: 1

--- All Tasks ---
ID: 1 | Title: Buy groceries | Status: Incomplete
Description: Milk, eggs, bread

...
Enter your choice: 6

Exiting application. All data will be lost.
Goodbye!
```

## Important Notes

- **No Persistence**: All task data exists only in memory during the application session. When you exit (option 6), all data is lost.
- **Single User**: Designed for single-user, single-session use
- **In-Memory Only**: No databases or file storage (Phase I constraint)

## Running Tests

Run all tests:
```bash
pytest
```

Run with verbose output:
```bash
pytest -v
```

Run with coverage report:
```bash
pytest --cov=src --cov-report=term-missing
```

## Project Structure

```
todo_app/
├── src/
│   ├── models/          # Task data model
│   ├── services/        # Business logic (CRUD operations)
│   ├── cli/             # User interface (menu, input, output)
│   └── main.py          # Application entry point
├── tests/
│   ├── unit/            # Unit tests
│   └── integration/     # Integration tests
├── specs/               # Specification documents
├── pyproject.toml       # Project configuration
└── README.md            # This file
```

## Development

This project follows Spec-Driven Development principles with clear separation of concerns:

- **Models**: Task dataclass with validation
- **Services**: TaskService handles all CRUD operations
- **CLI**: User interface components (menu, input handling, output formatting)

See `specs/001-phase-i-basic-todo/` for detailed specification, plan, and design documents.

## Constitutional Compliance

Phase I strictly adheres to the Evolution of Todo constitution:
- ✅ No databases or persistence
- ✅ No file system operations
- ✅ No web frameworks or APIs
- ✅ No authentication
- ✅ Single-user, in-memory only
- ✅ Python 3.11+ standard library only

## License

This is an educational project for demonstrating Spec-Driven Development.

## Future Phases

Phase I is the foundation. Future phases will add:
- Phase II: Multi-user support, authentication, cloud persistence (Neon DB)
- Phase III: Real-time collaboration, notifications, advanced search
- Phase IV: Agent orchestration, MCP integration, workflow automation
- Phase V: Distributed architecture with event sourcing and CQRS

Each phase builds on the previous while maintaining the clean architecture established in Phase I.
