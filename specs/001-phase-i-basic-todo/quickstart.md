# Quickstart: Phase I - Basic Todo Console Application

**Feature**: Phase I - Basic Todo Console Application
**Date**: 2025-12-28
**Status**: Ready for Implementation

## Overview

This quickstart guide helps you set up, run, and develop the Phase I todo console application. Phase I is a simple in-memory Python program with no external dependencies.

---

## Prerequisites

### Required

- **Python 3.11 or higher**
  - Check version: `python --version` or `python3 --version`
  - Download: [python.org](https://www.python.org/downloads/)

### Optional (for development)

- **pytest** (for running tests)
  - Install: `pip install pytest pytest-cov`
- **Git** (for version control)
  - Check version: `git --version`
  - Download: [git-scm.com](https://git-scm.com/)

---

## Quick Start (Run the Application)

### Step 1: Navigate to Project Root

```bash
cd /path/to/todo_app
```

### Step 2: Run the Application

```bash
python src/main.py
```

or on some systems:

```bash
python3 src/main.py
```

### Step 3: Use the Application

You'll see the welcome message and main menu:

```
Welcome to Todo Application - Phase I

Main Menu:
1. View all tasks
2. Add a new task
3. Update a task
4. Delete a task
5. Mark task complete/incomplete
6. Exit

Enter your choice:
```

Follow the prompts to manage your tasks. Type `6` and press Enter to exit.

---

## Development Setup

### Step 1: Clone the Repository (if needed)

```bash
git clone <repository-url>
cd todo_app
```

### Step 2: Verify Python Version

```bash
python --version
# Should output: Python 3.11.x or higher
```

If Python 3.11+ is not your default, use `python3.11` or `python3` explicitly:

```bash
python3.11 --version
```

### Step 3: Install Development Dependencies

```bash
pip install pytest pytest-cov
```

or using pip3:

```bash
pip3 install pytest pytest-cov
```

### Step 4: Verify Installation

```bash
pytest --version
# Should output: pytest x.x.x
```

---

## Project Structure

```
todo_app/
├── src/                     # Application source code
│   ├── __init__.py          # Python package marker
│   ├── main.py              # Application entry point
│   ├── models/              # Data models
│   │   ├── __init__.py
│   │   └── task.py          # Task dataclass
│   ├── services/            # Business logic
│   │   ├── __init__.py
│   │   └── task_service.py  # CRUD operations
│   └── cli/                 # User interface
│       ├── __init__.py
│       ├── menu.py          # Menu display
│       ├── input_handler.py # Input validation
│       └── output_formatter.py # Output formatting
├── tests/                   # Test suite
│   ├── __init__.py
│   ├── integration/         # End-to-end tests
│   │   ├── __init__.py
│   │   └── test_todo_app_flows.py
│   └── unit/                # Unit tests
│       ├── __init__.py
│       ├── test_task_model.py
│       ├── test_task_service.py
│       └── test_cli_components.py
├── specs/                   # Specification documents
│   └── 001-phase-i-basic-todo/
│       ├── spec.md          # Requirements
│       ├── plan.md          # Implementation plan
│       ├── data-model.md    # Entity definitions
│       ├── contracts/       # Interface contracts
│       └── quickstart.md    # This file
├── pyproject.toml           # Project metadata (created during implementation)
├── README.md                # Project overview (created during implementation)
└── .gitignore               # Git ignore patterns (created during implementation)
```

---

## Running the Application

### Basic Run

From project root:

```bash
python src/main.py
```

### Run with Specific Python Version

If you have multiple Python versions installed:

```bash
python3.11 src/main.py
# or
python3 src/main.py
```

### Expected Behavior

- Welcome message displays
- Main menu appears
- You can perform all 6 operations:
  1. View tasks
  2. Add tasks
  3. Update tasks
  4. Delete tasks
  5. Mark tasks complete/incomplete
  6. Exit (loses all data)

---

## Running Tests

### Run All Tests

```bash
pytest
```

### Run with Verbose Output

```bash
pytest -v
```

### Run Specific Test File

```bash
# Unit tests
pytest tests/unit/test_task_model.py
pytest tests/unit/test_task_service.py
pytest tests/unit/test_cli_components.py

# Integration tests
pytest tests/integration/test_todo_app_flows.py
```

### Run with Coverage Report

```bash
pytest --cov=src --cov-report=term-missing
```

**Expected Output**:
```
---------- coverage: platform linux, python 3.11.x -----------
Name                              Stmts   Miss  Cover   Missing
---------------------------------------------------------------
src/__init__.py                       0      0   100%
src/main.py                          45      2    96%   89-90
src/models/__init__.py                0      0   100%
src/models/task.py                   15      0   100%
src/services/__init__.py              0      0   100%
src/services/task_service.py         58      3    95%   112-114
src/cli/__init__.py                   0      0   100%
src/cli/menu.py                      22      1    95%   67
src/cli/input_handler.py             35      2    94%   78-79
src/cli/output_formatter.py          18      0   100%
---------------------------------------------------------------
TOTAL                               193      8    96%
```

**Target Coverage**: 80% minimum (constitutional requirement)

### Run Tests by Category

```bash
# Only unit tests
pytest tests/unit/

# Only integration tests
pytest tests/integration/
```

---

## Development Workflow

### 1. Create a Feature Branch (if using Git)

```bash
git checkout -b feature/add-new-functionality
```

### 2. Write Tests First (if following TDD)

```bash
# Edit test file
nano tests/unit/test_my_feature.py

# Run tests (should fail initially)
pytest tests/unit/test_my_feature.py -v
```

### 3. Implement Feature

```bash
# Edit source file
nano src/services/task_service.py

# Run tests again (should pass now)
pytest tests/unit/test_my_feature.py -v
```

### 4. Check Coverage

```bash
pytest --cov=src --cov-report=term-missing
```

Ensure coverage is at least 80%.

### 5. Run All Tests

```bash
pytest -v
```

Ensure all tests pass before committing.

### 6. Commit Changes

```bash
git add src/ tests/
git commit -m "feat: add new functionality

- Implements feature X
- Adds tests for edge cases Y and Z
- Maintains 85% coverage

Refs: task T042"
```

---

## Troubleshooting

### Issue: "python: command not found"

**Solution**: Install Python 3.11+ or use `python3` instead:

```bash
python3 src/main.py
```

### Issue: "No module named 'src'"

**Solution**: Run from project root directory:

```bash
cd /path/to/todo_app
python src/main.py
```

### Issue: "pytest: command not found"

**Solution**: Install pytest:

```bash
pip install pytest pytest-cov
# or
pip3 install pytest pytest-cov
```

### Issue: "SyntaxError: invalid syntax" (Python < 3.11)

**Solution**: Upgrade to Python 3.11 or higher. Check version:

```bash
python --version
```

Phase I requires Python 3.11+ for modern type hints like `dict[int, Task]`.

### Issue: Tests fail with import errors

**Solution**: Ensure `__init__.py` files exist in all directories:

```bash
# Check for __init__.py files
ls src/__init__.py
ls src/models/__init__.py
ls src/services/__init__.py
ls src/cli/__init__.py
ls tests/__init__.py
```

If missing, create them:

```bash
touch src/__init__.py
# ... etc
```

### Issue: Application doesn't save data between runs

**Expected Behavior**: Phase I has no persistence (NFR-003, NFR-004). All data is lost on exit. This is correct and intentional for Phase I.

---

## Testing the Application Manually

### Test Scenario 1: Basic CRUD Operations

1. Run application: `python src/main.py`
2. Add a task (option 2):
   - Title: "Test Task 1"
   - Description: "This is a test"
3. View tasks (option 1):
   - Should see task with ID 1, status Incomplete
4. Mark complete (option 5):
   - ID: 1
   - Choice: c
5. View tasks (option 1):
   - Should see task with status Complete
6. Update task (option 3):
   - ID: 1
   - New title: "Updated Test Task"
   - Keep description (press Enter)
7. View tasks (option 1):
   - Should see updated title
8. Delete task (option 4):
   - ID: 1
9. View tasks (option 1):
   - Should see empty list message
10. Exit (option 6)

### Test Scenario 2: Error Handling

1. Run application
2. Try to view task (option 1) when empty:
   - Should see "No tasks found" message
3. Try to update non-existent task (option 3):
   - ID: 999
   - Should see "Error: Task not found"
4. Try to add task with empty title (option 2):
   - Title: (press Enter)
   - Should see "Error: Task title cannot be empty"
5. Try invalid menu choice:
   - Enter: abc
   - Should see "Invalid input. Please enter a number."
6. Exit (option 6)

---

## Performance Expectations

Based on success criteria (SC-001 through SC-008):

| Operation | Expected Time |
|-----------|---------------|
| Add task | <30 seconds (including user input) |
| View tasks | Instant (<10ms for 100 tasks) |
| Mark complete | <15 seconds (including user input) |
| Update task | Instant operation (<10ms) |
| Delete task | Instant operation (<10ms) |
| Handle 100 tasks | No noticeable delay |

**All operations should feel instant** from the user's perspective.

---

## Next Steps

### After Phase I Implementation

1. **Run full test suite**: `pytest -v`
2. **Check coverage**: `pytest --cov=src --cov-report=html`
3. **Manual testing**: Follow test scenarios above
4. **Review plan.md**: Ensure all requirements met
5. **Review spec.md**: Validate against acceptance criteria

### Moving to Phase II

Phase II will add:
- Database persistence (Neon DB)
- Multi-user support
- Authentication
- Web API (FastAPI)

The current Phase I structure is designed to migrate smoothly:
- Task model → SQLModel (add `table=True`)
- TaskService → Add database session
- CLI layer → Unchanged (or add alongside web API)

---

## Quick Reference

### Common Commands

```bash
# Run application
python src/main.py

# Run all tests
pytest -v

# Run with coverage
pytest --cov=src --cov-report=term-missing

# Run specific test
pytest tests/unit/test_task_service.py -v

# Check Python version
python --version

# Install dev dependencies
pip install pytest pytest-cov
```

### File Locations

- **Application**: `src/main.py`
- **Task Model**: `src/models/task.py`
- **Service Logic**: `src/services/task_service.py`
- **Tests**: `tests/unit/` and `tests/integration/`
- **Specifications**: `specs/001-phase-i-basic-todo/`

---

## Support & Documentation

- **Specification**: [spec.md](./spec.md)
- **Implementation Plan**: [plan.md](./plan.md)
- **Data Model**: [data-model.md](./data-model.md)
- **CLI Contract**: [contracts/cli-interface.md](./contracts/cli-interface.md)
- **Constitution**: `../../.specify/memory/constitution.md`

---

**Status**: Ready for implementation - all planning documents complete.
