# Data Model Design: Phase I Advanced (Revised) - Task Scheduling and Organization

**Feature**: 004-phase-i-advanced-v2
**Date**: 2026-01-01
**Purpose**: Complete entity definitions, relationships, validation rules, and state transitions

## Executive Summary

This document defines the complete data model for Phase I Advanced features, extending existing Phase I Basic/Intermediate models with due dates, recurrence, templates, history, and statistics. All models use Python dataclasses with clear validation rules and maintain 100% backward compatibility.

## Core Entities

### 1. Task (Extended)

**File**: `src/models/task.py`

**Description**: Core task entity, extended with due date and recurrence rule support.

```python
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List
from .enums import Priority, Status, RecurrenceType

@dataclass
class RecurrenceRule:
    """Defines how a task recurs"""
    type: RecurrenceType = RecurrenceType.NONE
    interval_days: Optional[int] = None  # Only for CUSTOM type

    def __post_init__(self):
        if self.type == RecurrenceType.CUSTOM and self.interval_days is None:
            raise ValueError("CUSTOM recurrence requires interval_days")
        if self.interval_days is not None and self.interval_days < 1:
            raise ValueError("interval_days must be positive")

@dataclass
class Task:
    """Represents a todo task with extended Phase I Advanced features"""
    id: str
    title: str
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    recurrence_rule: RecurrenceRule = field(default_factory=RecurrenceRule)
    priority: Priority = Priority.MEDIUM
    status: Status = Status.TODO
    tags: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None

    def __post_init__(self):
        # Validate due date is not in past
        if self.due_date and self.due_date < datetime.now():
            raise ValueError("Due date cannot be in the past")

        # Validate tags are strings
        if self.tags:
            if not all(isinstance(tag, str) for tag in self.tags):
                raise TypeError("All tags must be strings")

        # Validate status consistency
        if self.status == Status.DONE and not self.completed_at:
            self.completed_at = datetime.now()
        elif self.status == Status.TODO and self.completed_at:
            self.completed_at = None

    @property
    def is_overdue(self) -> bool:
        """Check if task is overdue (due date passed and not completed)"""
        return (
            self.due_date is not None
            and self.due_date < datetime.now()
            and self.status != Status.DONE
        )

    @property
    def is_due_today(self) -> bool:
        """Check if task is due today"""
        return (
            self.due_date is not None
            and self.due_date.date() == datetime.now().date()
            and self.status != Status.DONE
        )

    @property
    def is_upcoming(self) -> bool:
        """Check if task is upcoming (within next 7 days)"""
        if not self.due_date or self.status == Status.DONE:
            return False
        days_until_due = (self.due_date - datetime.now()).days
        return 0 < days_until_due <= 7

    @property
    def is_recurring(self) -> bool:
        """Check if task has recurrence rule"""
        return self.recurrence_rule.type != RecurrenceType.NONE
```

**Validation Rules:**
- `id`: Required, unique string identifier
- `title`: Required, non-empty string
- `description`: Optional string
- `due_date`: Optional datetime, cannot be in past
- `recurrence_rule.type`: One of NONE, DAILY, WEEKLY, CUSTOM
- `recurrence_rule.interval_days`: Required for CUSTOM type, must be >= 1
- `priority`: One of LOW, MEDIUM, HIGH
- `status`: One of TODO, IN_PROGRESS, DONE
- `tags`: List of strings, all elements must be strings
- `created_at`: Required datetime, defaults to now
- `completed_at`: Optional datetime, set when status = DONE

**State Transitions:**
```
TODO --> IN_PROGRESS --> DONE
  ^_________________________|
```

- **TODO → IN_PROGRESS**: User marks task as in progress
- **IN_PROGRESS → DONE**: User completes task, sets completed_at
- **DONE → TODO**: User reopens task, clears completed_at
- Any state → **DELETED**: User deletes task (not shown in state diagram)

**Backward Compatibility:**
- All new fields (`due_date`, `recurrence_rule`) are optional with defaults
- Existing Phase I Basic/Intermediate code continues to work unchanged
- Default `recurrence_rule.type = NONE` means no recurrence

### 2. TaskTemplate

**File**: `src/models/template.py`

**Description**: Template for rapid task creation with pre-filled fields.

```python
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List
from .enums import Priority

@dataclass
class TaskTemplate:
    """Template for rapid task creation"""
    id: str
    name: str  # User-defined template name (e.g., "Weekly Review")
    title: str  # Default task title
    description: Optional[str] = None
    priority: Optional[Priority] = None
    tags: Optional[List[str]] = None
    due_date_offset: Optional[str] = None  # "today", "tomorrow", "next_week", "next_month", None
    created_at: datetime = field(default_factory=datetime.now)

    def __post_init__(self):
        # Validate name is not empty
        if not self.name or not self.name.strip():
            raise ValueError("Template name cannot be empty")

        # Validate title is not empty
        if not self.title or not self.title.strip():
            raise ValueError("Template title cannot be empty")

        # Validate due_date_offset is one of allowed values
        valid_offsets = [None, "today", "tomorrow", "next_week", "next_month"]
        if self.due_date_offset not in valid_offsets:
            raise ValueError(f"Invalid due_date_offset: {self.due_date_offset}")

        # Validate tags if provided
        if self.tags and not all(isinstance(tag, str) for tag in self.tags):
            raise TypeError("All tags must be strings")

    def to_task(self, custom_fields: dict = None) -> Task:
        """Create a Task from this template with optional custom field overrides"""
        from .task import Task, RecurrenceRule
        from .enums import RecurrenceType

        due_date = self._calculate_due_date()

        task = Task(
            id=generate_id(),
            title=self.title,
            description=self.description,
            priority=self.priority or Priority.MEDIUM,
            tags=self.tags.copy() if self.tags else [],
            due_date=due_date,
            recurrence_rule=RecurrenceRule(type=RecurrenceType.NONE),
            created_at=datetime.now(),
            completed_at=None
        )

        # Apply custom field overrides
        if custom_fields:
            if "title" in custom_fields:
                task.title = custom_fields["title"]
            if "description" in custom_fields:
                task.description = custom_fields["description"]
            if "priority" in custom_fields:
                task.priority = custom_fields["priority"]
            if "tags" in custom_fields:
                task.tags = custom_fields["tags"]
            if "due_date" in custom_fields:
                task.due_date = custom_fields["due_date"]

        return task

    def _calculate_due_date(self) -> Optional[datetime]:
        """Calculate actual due date from relative offset"""
        if not self.due_date_offset:
            return None

        today = datetime.now()
        today_end = datetime.combine(today.date(), datetime.max.time())

        offset_map = {
            "today": timedelta(0),
            "tomorrow": timedelta(days=1),
            "next_week": timedelta(weeks=1),
            "next_month": timedelta(days=30)
        }

        return today_end + offset_map.get(self.due_date_offset, timedelta(0))
```

**Validation Rules:**
- `id`: Required, unique string identifier
- `name`: Required, non-empty string
- `title`: Required, non-empty string
- `description`: Optional string
- `priority`: Optional, one of LOW, MEDIUM, HIGH
- `tags`: Optional list of strings
- `due_date_offset`: Optional, one of None, "today", "tomorrow", "next_week", "next_month"
- `created_at`: Required datetime, defaults to now

**Methods:**
- `to_task(custom_fields=None)`: Creates Task instance from template, with optional overrides

**Constraints:**
- Maximum 10 templates per specification constraint
- Templates are in-memory only (no persistence)

### 3. HistoryEntry

**File**: `src/models/history.py`

**Description**: Represents a single user action for undo functionality.

```python
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List
from .task import Task
from .enums import ActionType

@dataclass
class HistoryEntry:
    """Represents a single user action for undo"""
    action: ActionType
    timestamp: datetime
    task_id: str
    task_snapshot: Task  # Complete task state before action
    auto_created_task_id: Optional[str] = None  # Set for recurring task completions
    auto_created_task_snapshot: Optional[Task] = None  # For undo restore
    additional_data: Optional[dict] = None  # For bulk operations

    def __post_init__(self):
        # Validate action type
        if not isinstance(self.action, ActionType):
            raise TypeError(f"action must be ActionType, got {type(self.action)}")

        # Validate task snapshot exists
        if not self.task_snapshot:
            raise ValueError("task_snapshot is required")

        # Validate auto_created_task_id matches action type
        if self.action == ActionType.COMPLETE and self.auto_created_task_id:
            if not self.auto_created_task_snapshot:
                raise ValueError("auto_created_task_snapshot required when auto_created_task_id set")
```

**Validation Rules:**
- `action`: Required ActionType enum value
- `timestamp`: Required datetime, defaults to now
- `task_id`: Required string, ID of primary task affected
- `task_snapshot`: Required Task, complete state before action
- `auto_created_task_id`: Optional string, only for recurring task completions
- `auto_created_task_snapshot`: Optional Task, only set when `auto_created_task_id` is set
- `additional_data`: Optional dict, for bulk operations or complex actions

**Action Types:**
```python
# src/models/enums.py (extended)
class ActionType(Enum):
    ADD = "add"
    EDIT = "edit"
    DELETE = "delete"
    COMPLETE = "complete"
    BULK_COMPLETE = "bulk_complete"
    BULK_DELETE = "bulk_delete"
```

### 4. ActionHistory

**File**: `src/models/history.py`

**Description**: Stack-based undo history with FIFO eviction (max 50 entries).

```python
from dataclasses import dataclass, field
from typing import List, Optional
from .history import HistoryEntry

@dataclass
class ActionHistory:
    """Stack-based undo history with FIFO eviction"""
    entries: List[HistoryEntry] = field(default_factory=list)
    max_size: int = 50

    def __post_init__(self):
        if self.max_size < 1:
            raise ValueError("max_size must be positive")

    def push(self, entry: HistoryEntry):
        """Add entry to history, enforce FIFO eviction"""
        self.entries.append(entry)

        # FIFO: Remove oldest if over limit
        if len(self.entries) > self.max_size:
            self.entries.pop(0)

    def pop(self) -> Optional[HistoryEntry]:
        """Remove and return most recent entry"""
        return self.entries.pop() if self.entries else None

    def peek(self) -> Optional[HistoryEntry]:
        """Return most recent entry without removing"""
        return self.entries[-1] if self.entries else None

    def clear(self):
        """Remove all history entries"""
        self.entries.clear()

    def size(self) -> int:
        """Return current number of entries"""
        return len(self.entries)
```

**Validation Rules:**
- `entries`: List of HistoryEntry objects
- `max_size`: Positive integer, default 50
- Enforces FIFO eviction when size exceeds `max_size`

**Constraints:**
- Maximum 50 entries per specification constraint
- In-memory only (no persistence)
- No redo functionality (out of scope)

### 5. ReminderSummary

**File**: `src/models/reminder.py` (or inline in service)

**Description**: Summary of reminder categories (overdue, due today, upcoming).

```python
from dataclasses import dataclass
from typing import List
from .task import Task

@dataclass
class ReminderSummary:
    """Summary of tasks by reminder category"""
    overdue: List[Task]
    due_today: List[Task]
    upcoming: List[Task]

    @property
    def total_count(self) -> int:
        """Total number of tasks needing attention"""
        return len(self.overdue) + len(self.due_today) + len(self.upcoming)

    @property
    def has_overdue(self) -> bool:
        """Check if any overdue tasks exist"""
        return len(self.overdue) > 0

    @property
    def has_due_today(self) -> bool:
        """Check if any tasks due today exist"""
        return len(self.due_today) > 0

    @property
    def has_upcoming(self) -> bool:
        """Check if any upcoming tasks exist"""
        return len(self.upcoming) > 0
```

**Validation Rules:**
- `overdue`: List of incomplete tasks with due_date < now
- `due_today`: List of incomplete tasks with due_date.date() == today
- `upcoming`: List of incomplete tasks with 0 < days_until_due <= 7

### 6. TaskStatistics

**File**: `src/models/statistics.py` (or inline in service)

**Description**: Statistics and metrics for task tracking.

```python
from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime

@dataclass
class TaskStatistics:
    """Statistics for task tracking and productivity insights"""
    total_tasks: int
    completed_tasks: int
    incomplete_tasks: int
    completion_rate: float  # 0.0 to 1.0
    overdue_count: int
    due_today_count: int
    upcoming_count: int
    average_completion_time_days: Optional[float]
    by_priority: dict  # {"low": count, "medium": count, "high": count}
    by_status: dict  # {"todo": count, "in_progress": count, "done": count}

    @property
    def completion_percentage(self) -> int:
        """Completion rate as percentage (0-100)"""
        return int(self.completion_rate * 100)

    def __post_init__(self):
        # Validate completion_rate is between 0 and 1
        if not 0.0 <= self.completion_rate <= 1.0:
            raise ValueError("completion_rate must be between 0.0 and 1.0")

        # Validate counts are non-negative
        for count in [self.total_tasks, self.completed_tasks, self.incomplete_tasks,
                     self.overdue_count, self.due_today_count, self.upcoming_count]:
            if count < 0:
                raise ValueError("All counts must be non-negative")

        # Validate sum matches total
        if self.completed_tasks + self.incomplete_tasks != self.total_tasks:
            raise ValueError("completed_tasks + incomplete_tasks must equal total_tasks")
```

**Validation Rules:**
- `total_tasks`: Total number of tasks
- `completed_tasks`: Number of completed tasks
- `incomplete_tasks`: Number of incomplete tasks
- `completion_rate`: Ratio of completed/total (0.0 to 1.0)
- `overdue_count`: Number of overdue tasks
- `due_today_count`: Number of tasks due today
- `upcoming_count`: Number of upcoming tasks (within 7 days)
- `average_completion_time_days`: Average days from creation to completion (None if none completed)
- `by_priority`: Dictionary of task counts by priority level
- `by_status`: Dictionary of task counts by status

## Entity Relationships

### Task Relationships
```
Task (1) -----> RecurrenceRule (0..1)
Task (1) -----> Tags (0..*)
Task (1) -----> HistoryEntry (0..*) [as task_snapshot]
Task (1) -----> ReminderSummary (0..1) [as member]
Task (1) -----> TaskStatistics (0..1) [as aggregated data]
```

### Template Relationships
```
TaskTemplate (1) -----> Task (*) [creates via to_task()]
TaskTemplate (1) -----> Tags (0..*)
```

### History Relationships
```
ActionHistory (1) -----> HistoryEntry (0..50)
HistoryEntry (1) -----> Task (1..2) [task_snapshot + optional auto_created_task_snapshot]
```

### Reminder Relationships
```
ReminderSummary (1) -----> Task (*) [overdue + due_today + upcoming]
```

### Statistics Relationships
```
TaskStatistics (1) -----> Task (*) [aggregated from all tasks]
```

## Service Layer Contracts

### TaskService (Extended)

**File**: `src/services/task_service.py`

**Key Methods (New/Extended):**

```python
class TaskService:
    def set_due_date(self, task_id: str, due_date: datetime) -> Task:
        """Set or update task due date"""

    def clear_due_date(self, task_id: str) -> Task:
        """Remove task due date"""

    def set_recurrence_rule(self, task_id: str, rule: RecurrenceRule) -> Task:
        """Set or update task recurrence rule"""

    def clear_recurrence_rule(self, task_id: str) -> Task:
        """Remove task recurrence rule"""

    def complete_task(self, task_id: str) -> Task:
        """Complete task, auto-create next instance if recurring"""

    def bulk_complete_tasks(self, task_ids: List[str]) -> List[Task]:
        """Complete multiple tasks with confirmation"""

    def bulk_delete_tasks(self, task_ids: List[str]) -> List[Task]:
        """Delete multiple tasks with confirmation"""

    def get_overdue_tasks(self) -> List[Task]:
        """Get all overdue tasks"""

    def get_due_today_tasks(self) -> List[Task]:
        """Get all tasks due today"""

    def get_upcoming_tasks(self, days: int = 7) -> List[Task]:
        """Get tasks due within next N days"""

    def get_statistics(self) -> TaskStatistics:
        """Calculate and return task statistics"""

    def undo_last_action(self) -> Optional[Task]:
        """Undo last action (including recurring task completions)"""

    def get_history(self, limit: int = 10) -> List[HistoryEntry]:
        """Get recent history entries"""

    def apply_template(self, template_id: str, custom_fields: dict = None) -> Task:
        """Create task from template"""
```

### TemplateService (New)

**File**: `src/services/template_service.py`

```python
class TemplateService:
    def create_template(self, template: TaskTemplate) -> TaskTemplate:
        """Create new task template"""

    def get_template(self, template_id: str) -> Optional[TaskTemplate]:
        """Get template by ID"""

    def list_templates(self) -> List[TaskTemplate]:
        """List all templates"""

    def update_template(self, template_id: str, updates: dict) -> TaskTemplate:
        """Update template fields"""

    def delete_template(self, template_id: str) -> bool:
        """Delete template"""

    def create_task_from_template(self, template_id: str, custom_fields: dict = None) -> Task:
        """Create task from template with optional overrides"""
```

### HistoryService (New)

**File**: `src/services/history_service.py`

```python
class HistoryService:
    def record_action(self, entry: HistoryEntry):
        """Record action in history"""

    def undo(self) -> Optional[HistoryEntry]:
        """Undo and return most recent action"""

    def peek(self) -> Optional[HistoryEntry]:
        """Peek at most recent action without removing"""

    def get_recent(self, limit: int = 10) -> List[HistoryEntry]:
        """Get recent history entries"""

    def clear(self):
        """Clear all history"""
```

### ReminderService (New)

**File**: `src/services/reminder_service.py`

```python
class ReminderService:
    def evaluate_reminders(self, tasks: List[Task]) -> ReminderSummary:
        """Evaluate reminder categories"""

    def display_reminders(self, summary: ReminderSummary):
        """Display reminders to console"""
```

## State Transition Diagrams

### Task Lifecycle (Extended)
```
                   [Create Task]
                        |
                        v
                    TODO ──────► [Set Due Date]
                        |             |
                        |             v
                        |         [Set Recurrence]
                        |             |
                        v             v
                    IN_PROGRESS ──► [Complete Task]
                        |             |
                        |             v
                        |           DONE ◄─────────────┐
                        |             |                 |
                        |             └────► [Undo] ────┘
                        |
                        v
                   [Delete Task]
```

**Note:** For recurring tasks, [Complete Task] also triggers auto-creation of next instance.

### Template Lifecycle
```
         [Create Template]
               |
               v
         TaskTemplate
               |
               +──► [Apply Template] ──► Task
               |
               +──► [Update Template]
               |
               +──► [Delete Template]
```

### History Lifecycle
```
         [User Action]
               |
               v
         Create HistoryEntry
               |
               v
         Push to ActionHistory
               |
               +──► [Undo] ──► Pop & Restore
               |
               +──► [FIFO Eviction] ──► Remove oldest if > 50
```

## Validation Rules Summary

### Task Validation
- Due date cannot be in past
- Recurrence interval_days must be >= 1 for CUSTOM type
- Tags must be strings
- Status consistency (completed_at set only when status = DONE)

### Template Validation
- Name cannot be empty
- Title cannot be empty
- due_date_offset must be one of: None, "today", "tomorrow", "next_week", "next_month"
- Tags must be strings

### History Validation
- action must be ActionType enum
- task_snapshot is required
- auto_created_task_snapshot required when auto_created_task_id is set

### Statistics Validation
- completion_rate must be 0.0 to 1.0
- All counts must be non-negative
- completed_tasks + incomplete_tasks must equal total_tasks

## In-Memory Storage Patterns

### TaskService Storage
```python
class TaskService:
    def __init__(self):
        self.tasks: Dict[str, Task] = {}  # task_id -> Task
        self.history: ActionHistory = ActionHistory(max_size=50)
```

### TemplateService Storage
```python
class TemplateService:
    def __init__(self):
        self.templates: Dict[str, TaskTemplate] = {}  # template_id -> TaskTemplate
```

### ReminderService Storage
```python
class ReminderService:
    def __init__(self):
        # No persistent storage - evaluates on-demand
        pass
```

**Important:** All data is in-memory only. Data is lost on application exit (Phase I constraint).

## Backward Compatibility Guarantees

### New Fields Are Optional
```python
# Phase I Basic/Intermediate code continues to work:
task = Task(id="1", title="Buy groceries")
# due_date = None (default)
# recurrence_rule = RecurrenceRule(type=NONE) (default)
```

### Existing Methods Unchanged
```python
# All Phase I Basic/Intermediate methods work identically:
service.add_task(task)
service.get_task("1")
service.list_tasks()
service.search_tasks(query)
service.filter_tasks(...)
service.sort_tasks(...)
service.toggle_status("1")
# ... all existing methods unchanged
```

### No Breaking Changes
- Existing Task properties: id, title, description, priority, status, tags, created_at, completed_at
- New properties: due_date, recurrence_rule (both optional with defaults)
- All existing functionality (priority, tags, search/filter/sort) works with extended model

## Performance Considerations

### O(1) Operations
- Task CRUD (add, get, update, delete) - dictionary lookups
- History push/pop - list append/pop
- Template CRUD - dictionary lookups

### O(n) Operations
- Statistics calculation - single pass through all tasks
- Reminder evaluation - single pass through all tasks
- Search/filter - single pass through all tasks (existing)

### Performance Goals (from specification)
- Due date validation: <200ms per date
- Statistics calculation: <500ms for up to 100 tasks
- Recurring task auto-creation: <300ms per completion
- Undo operations: <300ms
- Reminder evaluation: <200ms

All operations within target performance for typical usage (<100 tasks).

## Summary

This data model design provides:
- ✅ Complete entity definitions for all Phase I Advanced features
- ✅ Clear validation rules and constraints
- ✅ State transition diagrams
- ✅ Service layer contracts
- ✅ 100% backward compatibility with Phase I Basic/Intermediate
- ✅ In-memory storage patterns (Phase I scope)
- ✅ Performance characteristics aligned with specification

Ready for implementation task breakdown.
