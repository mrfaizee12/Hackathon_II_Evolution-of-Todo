# Quickstart Guide: Phase I Advanced (Revised) - Task Scheduling and Organization

**Feature**: 004-phase-i-advanced-v2
**Date**: 2026-01-01
**Purpose**: Development setup, testing procedures, usage examples, and troubleshooting

## Development Setup

### Prerequisites
- Python 3.11+ (required by constitution)
- Git (for version control)
- Terminal/Console environment (Windows PowerShell, Linux bash, macOS Terminal)

### Repository Structure
```text
todo_app/
├── src/
│   ├── models/           # Data models (Task, Template, History, etc.)
│   ├── services/         # Business logic (TaskService, TemplateService, etc.)
│   ├── cli/              # Command-line interface (menu, input, output)
│   ├── utils/            # Utilities (validators, helpers)
│   └── main.py           # Application entry point
├── tests/                # Unit and integration tests
├── specs/                # Feature specifications and plans
│   └── 004-phase-i-advanced-v2/
├── history/              # Prompt history and ADRs
└── CLAUDE.md             # Project instructions
```

### Installation Steps

1. **Clone repository** (if not already cloned):
   ```bash
   git clone <repository-url>
   cd todo_app
   ```

2. **Create virtual environment** (recommended):
   ```bash
   # Windows (PowerShell)
   python -m venv venv
   .\venv\Scripts\activate

   # Linux/macOS
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   # No external dependencies required (standard library only)
   # Just verify Python installation:
   python --version  # Should be 3.11+
   ```

4. **Run application**:
   ```bash
   python src/main.py
   ```

### Branch Management
Current development branch: `004-phase-i-advanced-v2`

```bash
# Switch to feature branch
git checkout 004-phase-i-advanced-v2

# Verify branch
git branch
```

## Testing Procedures

### Running Tests

```bash
# Run all tests
python -m unittest discover -s tests -p "test_*.py"

# Run specific test file
python -m unittest tests.test_task_model

# Run with verbose output
python -m unittest discover -s tests -p "test_*.py" -v

# Run integration tests only
python -m unittest tests.integration_test_due_dates -v
```

### Test Coverage

**Unit Tests:**
- `test_task_model.py` - Extended Task model with due_date and recurrence_rule
- `test_template_model.py` - TaskTemplate model
- `test_history_model.py` - ActionHistory and HistoryEntry models
- `test_recurrence_model.py` - RecurrenceRule model
- `test_task_service.py` - TaskService extensions
- `test_template_service.py` - TemplateService
- `test_history_service.py` - HistoryService
- `test_reminder_service.py` - ReminderService
- `test_date_validation.py` - Date-time validation
- `test_recurrence_logic.py` - Recurrence calculation logic
- `test_statistics.py` - Statistics calculations
- `test_bulk_operations.py` - Bulk operations

**Integration Tests:**
- `integration_test_due_dates.py` - Due date workflow
- `integration_test_statistics.py` - Statistics
- `integration_test_recurrence.py` - Recurring tasks
- `integration_test_reminders.py` - Console reminders
- `integration_test_templates.py` - Templates
- `integration_test_undo.py` - Undo functionality
- `integration_test_backward_compat.py` - Backward compatibility

### Test Success Criteria
- All tests must pass (100% pass rate)
- No skipped tests
- No test failures or errors
- Performance goals met (see specification SC-001 through SC-027)

## Usage Examples

### Example 1: Creating Tasks with Due Dates

```python
# Create task with due date
from datetime import datetime
from src.models.task import Task
from src.services.task_service import TaskService

service = TaskService()

# Set due date: January 15, 2026 at 5:00 PM
task = Task(
    id="1",
    title="Submit project report",
    due_date=datetime(2026, 1, 15, 17, 0),
    priority="high"
)

service.add_task(task)

# Display tasks (shows due date)
service.list_tasks()
# Output:
# [1] Submit project report [HIGH] Due: 2026-01-15 17:00
```

### Example 2: Recurring Tasks

```python
from src.models.task import Task, RecurrenceRule
from src.models.enums import RecurrenceType

# Create daily recurring task
task = Task(
    id="2",
    title="Check emails",
    recurrence_rule=RecurrenceRule(type=RecurrenceType.DAILY),
    due_date=datetime(2026, 1, 2, 9, 0)  # First instance at 9:00 AM
)

service.add_task(task)

# Complete task - auto-creates next instance
service.complete_task("2")
# New task created with due_date: 2026-01-03 09:00
```

### Example 3: Weekly Recurring Task

```python
# Create weekly recurring task
task = Task(
    id="3",
    title="Weekly team meeting",
    recurrence_rule=RecurrenceRule(type=RecurrenceType.WEEKLY),
    due_date=datetime(2026, 1, 6, 14, 0)  # Every Monday at 2:00 PM
)

service.add_task(task)

# Complete task - next instance in 1 week
service.complete_task("3")
# New task created with due_date: 2026-01-13 14:00
```

### Example 4: Custom Interval Recurrence

```python
# Create custom recurring task (every 3 days)
task = Task(
    id="4",
    title="Water plants",
    recurrence_rule=RecurrenceRule(
        type=RecurrenceType.CUSTOM,
        interval_days=3
    ),
    due_date=datetime(2026, 1, 2, 10, 0)
)

service.add_task(task)

# Complete task - next instance in 3 days
service.complete_task("4")
# New task created with due_date: 2026-01-05 10:00
```

### Example 5: Task Templates

```python
from src.models.template import TaskTemplate
from src.services.template_service import TemplateService

template_service = TemplateService()

# Create template
template = TaskTemplate(
    id="t1",
    name="Weekly Review",
    title="Weekly Review",
    description="Review past week's work",
    priority="medium",
    tags=["work", "review"],
    due_date_offset="next_week"
)

template_service.create_template(template)

# Create task from template
task = template_service.create_task_from_template("t1")
service.add_task(task)
# Task created with due date: 7 days from now
```

### Example 6: Customizing Template Fields

```python
# Create task from template with custom overrides
custom_fields = {
    "title": "Q4 Weekly Review",  # Override title
    "priority": "high",           # Override priority
    "due_date": datetime(2026, 1, 15, 17, 0)  # Override due date
}

task = template_service.create_task_from_template("t1", custom_fields)
service.add_task(task)
```

### Example 7: Console Reminders

```python
from src.services.reminder_service import ReminderService

reminder_service = ReminderService()

# Evaluate reminders (automatically called on app start)
summary = reminder_service.evaluate_reminders(service.list_tasks())

# Display reminders
reminder_service.display_reminders(summary)

# Example output:
# ⚠️  OVERDUE TASKS (2):
#   [1] Submit project report [HIGH] Due: 2026-01-10 17:00 (2 days overdue)
#   [3] Weekly team meeting [MEDIUM] Due: 2026-01-12 14:00 (1 day overdue)
#
# 📅 DUE TODAY (3):
#   [5] Buy groceries [MEDIUM] Due: 2026-01-12 23:59
#   [7] Call client [HIGH] Due: 2026-01-12 17:00
#   [9] Review documentation [LOW] Due: 2026-01-12 16:00
#
# 📆 UPCOMING (within 7 days, 4 tasks):
#   [2] Check emails [MEDIUM] Due: 2026-01-15 09:00 (3 days)
#   [4] Water plants [LOW] Due: 2026-01-16 10:00 (4 days)
#   [6] Team standup [HIGH] Due: 2026-01-18 09:00 (6 days)
#   [8] Monthly report [HIGH] Due: 2026-01-19 17:00 (7 days)
```

### Example 8: Task Statistics

```python
# Get task statistics
stats = service.get_statistics()

print(f"Total tasks: {stats.total_tasks}")
print(f"Completed: {stats.completed_tasks} ({stats.completion_percentage}%)")
print(f"Incomplete: {stats.incomplete_tasks}")
print(f"Overdue: {stats.overdue_count}")
print(f"Due today: {stats.due_today_count}")
print(f"Upcoming (7 days): {stats.upcoming_count}")

if stats.average_completion_time_days:
    print(f"Avg completion time: {stats.average_completion_time_days:.1f} days")

print(f"By priority: {stats.by_priority}")
print(f"By status: {stats.by_status}")

# Example output:
# Total tasks: 25
# Completed: 15 (60%)
# Incomplete: 10
# Overdue: 3
# Due today: 2
# Upcoming (7 days): 5
# Avg completion time: 2.3 days
# By priority: {'low': 5, 'medium': 12, 'high': 8}
# By status: {'todo': 7, 'in_progress': 3, 'done': 15}
```

### Example 9: Bulk Operations

```python
# Bulk complete multiple tasks
task_ids = ["1", "3", "5"]
completed_tasks = service.bulk_complete_tasks(task_ids)

# Example interaction:
# Confirm: Complete 3 tasks? (y/n): y
# ✅ Completed 3 tasks

# Bulk delete multiple tasks
task_ids = ["2", "4"]
deleted_tasks = service.bulk_delete_tasks(task_ids)

# Example interaction:
# Confirm: Delete 2 tasks? (y/n): y
# 🗑️  Deleted 2 tasks
```

### Example 10: Undo Operations

```python
# Undo last action
restored = service.undo_last_action()
if restored:
    print(f"✅ Undid: {restored.action.value} - Task {restored.task_id}")
else:
    print("❌ No actions to undo")

# View recent history
history = service.get_history(limit=5)
for entry in history:
    print(f"{entry.timestamp} - {entry.action.value}: Task {entry.task_id}")

# Example output:
# 2026-01-01 15:30:45 - complete: Task 1
# 2026-01-01 15:30:30 - add: Task 1
# 2026-01-01 15:30:15 - edit: Task 2
```

### Example 11: Undo Recurring Task Completion

```python
# Complete recurring task (creates next instance)
service.complete_task("2")
# Task 2 marked complete, Task 3 created (next instance)

# Undo - restores original task AND deletes auto-created instance
restored = service.undo_last_action()
# Task 2 restored (incomplete), Task 3 deleted
```

## CLI Usage

### Main Menu Structure

```
Main Menu:
  1. List all tasks
  2. Add new task
  3. Edit task
  4. Delete task
  5. Mark task complete
  6. Search tasks
  7. Filter tasks
  8. Sort tasks
  9. View statistics

Advanced Features:
  10. Set task due date
  11. Set task recurrence
  12. View reminders
  13. Manage templates
  14. Bulk operations
  15. Undo last action
  16. View history

  0. Exit
```

### Setting Due Date (Menu Option 10)
```
Enter task ID: 1
Enter due date (YYYY-MM-DD HH:MM): 2026-01-15 17:00
✅ Due date set: 2026-01-15 17:00
```

### Setting Recurrence (Menu Option 11)
```
Enter task ID: 2
Select recurrence type:
  1. None
  2. Daily
  3. Weekly
  4. Custom interval
Enter choice: 2
✅ Recurrence set: Daily
```

### Viewing Reminders (Menu Option 12)
```
⚠️  OVERDUE TASKS (2):
  [1] Submit project report [HIGH] Due: 2026-01-10 17:00
  [3] Weekly team meeting [MEDIUM] Due: 2026-01-12 14:00

📅 DUE TODAY (3):
  [5] Buy groceries [MEDIUM] Due: 2026-01-12 23:59
  [7] Call client [HIGH] Due: 2026-01-12 17:00

📆 UPCOMING (within 7 days, 4 tasks):
  [2] Check emails [MEDIUM] Due: 2026-01-15 09:00 (3 days)
  [4] Water plants [LOW] Due: 2026-01-16 10:00 (4 days)
```

### Managing Templates (Menu Option 13)
```
Template Management:
  1. Create template
  2. List templates
  3. Apply template
  4. Edit template
  5. Delete template
  0. Back

Enter choice: 1

Template name: Weekly Review
Task title: Weekly Review
Description (optional): Review past week's work
Priority (optional, low/medium/high): medium
Tags (optional, comma-separated): work, review
Due date offset (today/tomorrow/next_week/next_month/none): next_week
✅ Template created: Weekly Review
```

### Bulk Operations (Menu Option 14)
```
Bulk Operations:
  1. Bulk complete tasks
  2. Bulk delete tasks
  0. Back

Enter choice: 1

Enter task IDs (comma-separated): 1,3,5
Confirm: Complete 3 tasks? (y/n): y
✅ Completed 3 tasks
```

### Undo (Menu Option 15)
```
Enter: undo
✅ Undid: complete - Task 1
```

### View History (Menu Option 16)
```
Recent actions (5):
  2026-01-01 15:30:45 - complete: Task 1
  2026-01-01 15:30:30 - add: Task 1
  2026-01-01 15:30:15 - edit: Task 2
  2026-01-01 15:30:00 - delete: Task 3
  2026-01-01 15:29:45 - add: Task 3
```

## Troubleshooting

### Issue: Invalid date format

**Problem**: User enters date in wrong format
```
Enter due date (YYYY-MM-DD HH:MM): 01/15/2026 5:00 PM
❌ Invalid date format: Invalid isoformat string: '01/15/2026 5:00 PM'
```

**Solution**: Use ISO 8601 format (YYYY-MM-DD HH:MM)
```
Enter due date (YYYY-MM-DD HH:MM): 2026-01-15 17:00
✅ Due date set: 2026-01-15 17:00
```

### Issue: Due date in the past

**Problem**: User tries to set due date that has already passed
```
Enter due date (YYYY-MM-DD HH:MM): 2025-12-31 17:00
❌ Due date cannot be in the past
```

**Solution**: Use current or future date/time

### Issue: Undo after bulk operation

**Problem**: User expects bulk operation to be single undo
```
Service.bulk_complete_tasks(["1", "3", "5"])
# Creates 3 separate history entries
```

**Solution**: Current design creates separate history entry per task. User must undo 3 times.
**Note**: This is intentional - allows granular undo control.

### Issue: Recurring task auto-creation when not wanted

**Problem**: User completes recurring task but doesn't want next instance
```
Service.complete_task("2")
# Automatically creates Task 3 with incremented due date
```

**Solution**: Remove recurrence rule before completing
```python
service.clear_recurrence_rule("2")
service.complete_task("2")  # No auto-creation
```

### Issue: Template with outdated due date

**Problem**: Absolute date in template becomes outdated
```python
# Bad: Absolute date
template = TaskTemplate(
    name="Weekly Report",
    title="Weekly Report",
    due_date=datetime(2024, 1, 1, 12, 0)  # Outdated!
)
```

**Solution**: Use relative offsets
```python
# Good: Relative offset
template = TaskTemplate(
    name="Weekly Report",
    title="Weekly Report",
    due_date_offset="next_week"  # Always relevant
)
```

### Issue: DST transition affects recurring task timing

**Problem**: Task appears 1 hour earlier/later after DST change
```
# Task due every Monday at 9:00 AM
# DST spring forward: Task appears at 8:00 AM (1 hour drift)
```

**Solution**: This is expected behavior. Use naive datetime (system local time).
1-hour drift on DST transitions is acceptable for Phase I scope.

### Issue: Performance degradation with many tasks

**Problem**: Slow statistics or reminder evaluation with >100 tasks

**Solution**:
- Statistics: O(n) scan, should complete in <500ms for 100 tasks
- Reminders: O(n) scan, should complete in <200ms for 100 tasks
- If slower, check for performance bottlenecks (e.g., inefficient date calculations)

### Issue: Undo history full

**Problem**: Oldest history entry automatically removed
```
# 51st action - oldest entry automatically removed
```

**Solution**: This is expected FIFO behavior. Max 50 entries per specification.

### Issue: Cannot undo after application restart

**Problem**: Undo history lost after closing application

**Solution**: This is expected behavior. In-memory storage only (Phase I constraint).
Undo history is not persisted.

## Performance Benchmarks

### Expected Performance (from specification)

| Operation | Target | Notes |
|-----------|--------|-------|
| Due date validation | <200ms | Per date input |
| Statistics calculation | <500ms | Up to 100 tasks |
| Recurring task auto-creation | <300ms | Per completion |
| Undo operations | <300ms | Includes recurring tasks |
| Reminder evaluation | <200ms | On-demand display |

### Measuring Performance

```python
import time

# Measure statistics calculation
start = time.time()
stats = service.get_statistics()
end = time.time()
print(f"Statistics: {(end - start) * 1000:.2f}ms")

# Measure reminder evaluation
start = time.time()
summary = reminder_service.evaluate_reminders(service.list_tasks())
end = time.time()
print(f"Reminders: {(end - start) * 1000:.2f}ms")
```

## Integration with Existing Features

### Phase I Basic Features (Compatible)
- ✅ Task CRUD (create, read, update, delete)
- ✅ Task completion
- ✅ Priority levels (LOW, MEDIUM, HIGH)
- ✅ Task filtering by priority
- ✅ Task sorting by priority

### Phase I Intermediate Features (Compatible)
- ✅ Tags and tag management
- ✅ Task search
- ✅ Advanced filtering (by status, priority, tags)
- ✅ Advanced sorting (by priority, created date)
- ✅ CLI visual enhancements (colors, progress bars)

### Phase I Advanced Extensions (New)
- ✅ Due dates with date-time
- ✅ Recurring tasks (daily, weekly, custom)
- ✅ Console reminders (overdue, due today, upcoming)
- ✅ Task statistics
- ✅ Task templates
- ✅ Bulk operations
- ✅ Command history and undo

### Cross-Feature Compatibility

**Due dates with all features:**
- ✅ Priority: Can set priority on tasks with due dates
- ✅ Tags: Can tag tasks with due dates
- ✅ Search: Search tasks by title/description (due date in search results)
- ✅ Filter: Filter by priority, status, tags (due date visible in results)
- ✅ Sort: Sort by priority, created date (due date visible in results)

**Recurrence with all features:**
- ✅ Priority: Recurring tasks can have priorities
- ✅ Tags: Recurring tasks can have tags
- ✅ Search: Search recurring tasks
- ✅ Filter: Filter recurring tasks by priority, status, tags
- ✅ Sort: Sort recurring tasks by priority, due date

**Templates with all features:**
- ✅ Templates preserve priority, tags, due date offset
- ✅ Tasks created from templates support all features
- ✅ Can override template fields when creating task

## Best Practices

### Task Creation
1. Use meaningful titles (clear, concise, specific)
2. Add descriptions for complex tasks
3. Set appropriate priorities (HIGH for urgent, MEDIUM default, LOW for nice-to-have)
4. Use tags for categorization (work, personal, urgent, etc.)
5. Set due dates only when time-sensitive
6. Use recurrence for repetitive tasks (daily, weekly, custom)

### Template Management
1. Create templates for common task patterns
2. Use relative due date offsets (today, tomorrow, next_week)
3. Set default priorities in templates
4. Include common tags in templates
5. Limit to 10 templates maximum (specification constraint)

### Recurring Task Usage
1. Use daily for routine tasks (check emails, meditation)
2. Use weekly for weekly meetings/reports
3. Use custom interval for tasks with non-standard frequency (every 3 days)
4. Remove recurrence when task series is complete
5. Be aware: Completing recurring task immediately creates next instance

### Undo Usage
1. Review history before undoing (`View history` menu option)
2. Undo is LIFO (last-in, first-out)
3. Maximum 50 history entries
4. Undo is not persisted (lost on application exit)
5. For recurring task completions: Undo restores original AND deletes auto-created instance

### Statistics Review
1. Check statistics regularly (weekly recommended)
2. Monitor completion rate (aim for >60%)
3. Address overdue tasks promptly
4. Review average completion time to identify time-consuming tasks
5. Use priority distribution to balance workload

## Support and Resources

### Documentation
- Specification: `specs/004-phase-i-advanced-v2/spec.md`
- Implementation Plan: `specs/004-phase-i-advanced-v2/plan.md`
- Research: `specs/004-phase-i-advanced-v2/research.md`
- Data Model: `specs/004-phase-i-advanced-v2/data-model.md`

### Source Code
- Models: `src/models/`
- Services: `src/services/`
- CLI: `src/cli/`
- Entry Point: `src/main.py`

### Tests
- Unit Tests: `tests/test_*.py`
- Integration Tests: `tests/integration_test_*.py`

### Constitution
- Project Principles: `.specify/memory/constitution.md`
- Project Instructions: `CLAUDE.md`

---

**Ready for**: Implementation task breakdown (`/sp.tasks`) and code implementation (`/sp.implement`)
