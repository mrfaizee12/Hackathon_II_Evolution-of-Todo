# Quickstart Guide: Phase I Advanced - Task Deadline and Organization Features

**Feature**: 001-phase-i-advanced
**Date**: 2026-01-01
**Purpose**: Development setup, testing procedures, and usage examples for Phase I Advanced

## Development Setup

### Prerequisites

- Python 3.11 or higher
- Existing Phase I Basic and Intermediate codebase
- Git repository initialized with branch `001-phase-i-advanced`

### Installation Steps

1. **Navigate to repository root**:
   ```bash
   cd G:\evolution-todo\todo_app
   ```

2. **Verify Python version**:
   ```bash
   python --version
   # Output should be 3.11 or higher
   ```

3. **Verify current branch**:
   ```bash
   git branch
   # Output should show 001-phase-i-advanced
   ```

4. **Run existing tests** (to verify Phase I Basic/Intermediate stability):
   ```bash
   python -m unittest discover tests
   ```

### New File Structure

After implementing Phase I Advanced, your repository structure will include:

```
src/
├── models/
│   ├── task.py           # EXTENDED: added due_date field
│   ├── template.py        # NEW: TaskTemplate dataclass
│   ├── enums.py          # EXTENDED: added bulk operation types
│   └── history.py        # NEW: ActionHistory and HistoryEntry
├── services/
│   ├── task_service.py    # EXTENDED: due date, statistics, bulk ops
│   ├── template_service.py # NEW: Template CRUD operations
│   └── history_service.py # NEW: Undo/redo management
├── cli/
│   ├── menu.py           # EXTENDED: new menu options 12-16
│   ├── input_handler.py   # EXTENDED: date input, bulk selection, template input
│   └── output_formatter.py # EXTENDED: due date display, statistics display
└── utils/
    └── validators.py     # EXTENDED: date validation, template validation

tests/
├── test_task_model.py              # NEW: Tests for extended Task model
├── test_template_model.py           # NEW: Tests for Template model
├── test_history_model.py           # NEW: Tests for History model
├── test_task_service.py             # EXTENDED: Tests for TaskService extensions
├── test_template_service.py          # NEW: Tests for TemplateService
├── test_history_service.py          # NEW: Tests for HistoryService
├── test_date_validation.py          # NEW: Tests for date validation utilities
├── test_statistics.py              # NEW: Tests for statistics calculations
├── test_bulk_operations.py         # NEW: Tests for bulk operations
├── integration_test_due_dates.py    # NEW: Integration tests for due date workflow
├── integration_test_statistics.py    # NEW: Integration tests for statistics
├── integration_test_bulk_ops.py      # NEW: Integration tests for bulk operations
├── integration_test_templates.py     # NEW: Integration tests for templates
├── integration_test_undo.py          # NEW: Integration tests for undo functionality
└── integration_test_backward_compat.py # NEW: Tests for backward compatibility
```

## Testing Procedures

### Run All Tests

```bash
# Run all tests (unit and integration)
python -m unittest discover tests

# Run tests with verbose output
python -m unittest discover -v tests

# Run specific test file
python -m unittest tests.test_task_model

# Run specific test class
python -m unittest tests.test_task_model.TestTaskModel
```

### Test Coverage Categories

1. **Unit Tests**: Test individual models and service methods
   ```bash
   python -m unittest tests.test_task_model
   python -m unittest tests.test_template_model
   python -m unittest tests.test_history_model
   python -m unittest tests.test_task_service
   python -m unittest tests.test_template_service
   python -m unittest tests.test_history_service
   python -m unittest tests.test_date_validation
   python -m unittest tests.test_statistics
   python -m unittest tests.test_bulk_operations
   ```

2. **Integration Tests**: Test complete user workflows
   ```bash
   python -m unittest tests.integration_test_due_dates
   python -m unittest tests.integration_test_statistics
   python -m unittest tests.integration_test_bulk_ops
   python -m unittest tests.integration_test_templates
   python -m unittest tests.integration_test_undo
   ```

3. **Backward Compatibility Tests**: Verify existing functionality works unchanged
   ```bash
   python -m unittest tests.integration_test_backward_compat
   ```

### Expected Test Results

- All tests must pass (0 failures)
- No warnings or errors during execution
- Test execution time should be under 5 seconds for full test suite

## Usage Examples

### Example 1: Create Task with Due Date

```python
from src.services.task_service import TaskService
from datetime import date

service = TaskService()

# Create task with due date
success, message, task_id = service.add_task(
    title="Complete Phase I Advanced",
    description="Implement due dates, statistics, bulk operations, templates, and undo"
)
if success:
    # Set due date to 7 days from now
    due_date = date.today() + timedelta(days=7)
    success, message = service.set_due_date(task_id, due_date)
    print(message)  # "Task due date updated successfully!"
else:
    print(f"Error: {message}")
```

**CLI User Flow**:
```
Main Menu
========================================
1. View all tasks
2. Add a new task
...
12. Set/Update Task Due Date [NEW]
...
16. Undo Last Action [NEW]
========================================

Enter your choice (1-16): 2
--- Add New Task ---
Enter task title: Complete Phase I Advanced
Enter task description (optional): Implement due dates, statistics, bulk operations, templates, and undo
Priority options:
1. High
2. Medium
3. Low
Enter your choice (1-11): 1
Enter tags (comma-separated, optional): work, phase-i
Task added successfully! (ID: 1)

Enter your choice (1-16): 12
--- Set/Update Task Due Date ---
Enter task ID: 1
Enter due date (YYYY-MM-DD, optional): 2026-01-15
Task due date updated successfully!
```

### Example 2: View Task Statistics

```python
from src.services.task_service import TaskService

service = TaskService()

# Add some tasks
service.add_task("Task 1", "Description 1")
service.add_task("Task 2", "Description 2")
service.add_task("Task 3", "Description 3")

# Mark task 1 as complete
service.toggle_status(1)

# Get statistics
stats = service.get_statistics()
print(f"Total tasks: {stats.total_tasks}")
print(f"Completed: {stats.completed_tasks}")
print(f"Completion %: {stats.completion_percentage}%")
```

**Output**:
```
Task Statistics
========================================
Total tasks: 3
Completed: 1
Incomplete: 2
Completion %: 33.33%

Priority Distribution:
- High: 0
- Medium: 3
- Low: 0

Due Date Statistics:
- Overdue: 0
- Due today: 0
- Due this week: 0

Tag Distribution:
- No tags found
========================================
```

### Example 3: Bulk Task Operations

```python
from src.services.task_service import TaskService
from src.models.enums import Priority

service = TaskService()

# Add 5 tasks
for i in range(1, 6):
    service.add_task(f"Task {i}")

# Mark tasks 1-3 as complete (bulk operation)
success, message = service.bulk_update_status([1, 2, 3], "Complete")
print(message)  # "3 tasks marked as Complete!"

# Delete tasks 4-5 (bulk operation)
success, message = service.bulk_delete([4, 5])
print(message)  # "2 tasks deleted successfully!"
```

**CLI User Flow**:
```
Main Menu
...
14. Bulk Task Operations [NEW]
...

Enter your choice (1-16): 14
--- Bulk Task Operations ---
1. Mark tasks complete
2. Mark tasks incomplete
3. Delete tasks
4. Update task priority

Enter your choice (1-4): 1
Enter start task ID: 1
Enter end task ID: 3
Selected 3 tasks: [1, 2, 3]. Mark complete? (y/n): y
3 tasks marked as Complete!
```

### Example 4: Use Task Template

```python
from src.services.template_service import TemplateService

template_service = TemplateService()

# Create template
success, message, template_id = template_service.create_template(
    name="Weekly Report",
    title="Complete weekly report",
    description="Submit weekly progress report to manager",
    priority=Priority.HIGH,
    tags=["work", "report"]
)
print(message)  # "Template created successfully! (ID: 1)"

# Later, use template to create task
task = template_service.use_template(template_id)
print(f"Task created from template: {task.title}")
```

**CLI User Flow**:
```
Main Menu
...
15. Manage Task Templates [NEW]
...

Enter your choice (1-16): 15
--- Manage Task Templates ---
1. Create new template
2. Use existing template
3. List all templates
4. Delete template

Enter your choice (1-4): 1
--- Create New Template ---
Enter template name: Weekly Report
Enter template title: Complete weekly report
Enter template description (optional): Submit weekly progress report to manager
Priority options:
1. High
2. Medium
3. Low
Enter your choice (1-11): 1
Enter tags (comma-separated, optional): work, report
Enter due date (YYYY-MM-DD, optional): 2026-01-15
Template created successfully! (ID: 1)

Enter your choice (1-16): 15
--- Manage Task Templates ---
1. Create new template
2. Use existing template
3. List all templates
4. Delete template

Enter your choice (1-4): 2
Available Templates:
1. Weekly Report (Priority: High, Tags: work, report)

Enter template ID to use: 1
Using template: Weekly Report
        Title: Complete weekly report
        Description: Submit weekly progress report to manager
        Priority: High
        Tags: work, report
        Due date: 2026-01-15

Override any field? (Press Enter to keep, or enter new value):
Title: [Enter]
Description: [Enter]
Priority: [Enter]
Tags: [Enter]
Due date: [Enter]
Task added successfully! (ID: 2)
```

### Example 5: Undo Actions

```python
from src.services.task_service import TaskService
from src.services.history_service import HistoryService

task_service = TaskService()
history_service = HistoryService(task_service)

# Create task
success, message, task_id = task_service.add_task("Task to undo")
print(message)  # "Task added successfully! (ID: 1)"

# Delete task
success, message = task_service.delete_task(task_id)
print(message)  # "Task deleted successfully! (ID: 1)"

# Undo delete (restores task)
if history_service.has_undo():
    success, message = history_service.undo()
    print(message)  # "Undo: Task restored (ID: 1)"
else:
    print("No actions available to undo")
```

**CLI User Flow**:
```
Main Menu
...
16. Undo Last Action [NEW]
...

Enter your choice (1-16): 16
--- Undo Last Action ---
Undoing: delete task (ID: 1)
Task restored successfully! (ID: 1)
```

## Performance Validation

### Measure Due Date Validation Time

```python
import time
from src.utils.validators import validate_due_date

start = time.perf_counter()
is_valid, error = validate_due_date("2026-01-15")
end = time.perf_counter()
elapsed_ms = (end - start) * 1000

print(f"Validation time: {elapsed_ms:.3f} ms")
# Expected: <100ms (SC-017)
```

### Measure Statistics Calculation Time

```python
import time
from src.services.task_service import TaskService

service = TaskService()

# Create 100 tasks
for i in range(1, 101):
    service.add_task(f"Task {i}")

start = time.perf_counter()
stats = service.get_statistics()
end = time.perf_counter()
elapsed_ms = (end - start) * 1000

print(f"Statistics calculation time: {elapsed_ms:.3f} ms")
print(f"Total tasks: {stats.total_tasks}")
# Expected: <500ms (SC-018)
```

### Measure Bulk Operation Time

```python
import time
from src.services.task_service import TaskService

service = TaskService()

# Create 50 tasks
task_ids = []
for i in range(1, 51):
    success, message, task_id = service.add_task(f"Task {i}")
    task_ids.append(task_id)

start = time.perf_counter()
success, message = service.bulk_update_status(task_ids, "Complete")
end = time.perf_counter()
elapsed_ms = (end - start) * 1000

print(f"Bulk operation time: {elapsed_ms:.3f} ms")
print(message)  # Should report how many tasks were affected
# Expected: <1000ms (SC-019)
```

### Measure Undo Operation Time

```python
import time
from src.services.task_service import TaskService
from src.services.history_service import HistoryService

task_service = TaskService()
history_service = HistoryService(task_service)

# Create and delete a task
success, message, task_id = task_service.add_task("Task")
task_service.delete_task(task_id)

# Measure undo time
start = time.perf_counter()
success, message = history_service.undo()
end = time.perf_counter()
elapsed_ms = (end - start) * 1000

print(f"Undo operation time: {elapsed_ms:.3f} ms")
print(message)
# Expected: <200ms (SC-020)
```

## Troubleshooting

### Issue: "Invalid date format" error when setting due date

**Cause**: Date not in YYYY-MM-DD format

**Solution**:
- Use ISO 8601 format: "2026-01-15" (not "01/15/2026" or "15-01-2026")
- Ensure 4-digit year, 2-digit month, 2-digit day with hyphens
- Example: January 15, 2026 → "2026-01-15"

### Issue: "Due date cannot be in the past" error

**Cause**: Due date is before today's date

**Solution**:
- Use today's date or future date
- Check system date: `date.today()` in Python
- Example: If today is 2026-01-01, then "2025-12-31" is rejected

### Issue: "Maximum 10 templates reached" error

**Cause**: Template storage limit (FR-033) exceeded

**Solution**:
- Delete an existing template before creating new one
- Use menu option 15.4 to delete a template
- Template limit prevents uncontrolled memory usage in Phase I (in-memory only)

### Issue: "No actions available to undo" message

**Cause**: Undo history is empty or limit exceeded (50 entries)

**Solution**:
- Perform an action (create, update, delete) before undoing
- If history exceeded limit (50 actions), older actions are no longer undoable
- Check history with `has_undo()` before attempting undo

### Issue: Backward compatibility test fails

**Cause**: Phase I Basic or Intermediate functionality was modified

**Solution**:
- Verify Task model `__post_init__()` allows existing tasks without due_date (default None)
- Verify TaskService existing methods (add_task, delete_task, etc.) are unchanged
- Verify menu options 1-11 work identically to Phase I Intermediate
- Review changes in git diff and remove modifications to existing functionality

## Next Steps

1. **Review specification**: `specs/001-phase-i-advanced/spec.md`
2. **Review plan**: `specs/001-phase-i-advanced/plan.md`
3. **Review data model**: `specs/001-phase-i-advanced/data-model.md`
4. **Review research**: `specs/001-phase-i-advanced/research.md`
5. **Generate tasks**: Run `/sp.tasks` to create `specs/001-phase-i-advanced/tasks.md`
6. **Implement features**: Run `/sp.implement` to execute tasks
7. **Test thoroughly**: Run all unit and integration tests
8. **Validate backward compatibility**: Ensure Phase I Basic and Intermediate work unchanged
9. **Verify performance goals**: Run performance validation scripts
10. **Create pull request**: Reference specification and include summary of changes

## Support

For questions or issues:
- Review specification for feature requirements
- Review data model for entity definitions
- Review research for design decisions and rationale
- Check constitution for development principles
- Run `/sp.adr <title>` if significant architectural decisions emerge during implementation

---

**Phase I Advanced is an in-memory CLI extension. All data is lost when application exits. No databases, files, or persistence mechanisms are used.**
