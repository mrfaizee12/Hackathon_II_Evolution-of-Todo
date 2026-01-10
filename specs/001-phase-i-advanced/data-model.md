# Data Model Design: Phase I Advanced - Task Deadline and Organization Features

**Feature**: 001-phase-i-advanced
**Date**: 2026-01-01
**Purpose**: Define data entities, relationships, validation rules, and state transitions for Advanced features

## Overview

Phase I Advanced extends the existing data model with three new entities and one extended entity:

1. **Task** (Extended): Add `due_date` field for deadline tracking
2. **TaskTemplate** (NEW): Predefined task configuration for rapid creation
3. **HistoryEntry** (NEW): Audit trail entry for undo functionality
4. **ActionHistory** (NEW): Manages undo history stack (service, not persisted entity)

All entities are Python dataclasses with type hints, validation in `__post_init__`, and optional fields with defaults for backward compatibility.

## Entity: Task (Extended from Phase I Intermediate)

### Purpose
Represents a single todo item with deadline tracking capability.

### Definition

```python
from dataclasses import dataclass, field
from datetime import date
from typing import Optional, List
from src.models.enums import Priority

@dataclass
class Task:
    """
    Represents a single todo item with extended due date support.

    Attributes:
        id: Unique numeric identifier (auto-assigned, starts at 1)
        title: Short description of the task (required, non-empty)
        description: Optional detailed description
        status: Completion status ("Complete" or "Incomplete")
        priority: Task importance level (High, Medium, or Low; defaults to Medium)
        tags: Collection of text labels for categorization (zero or more tags)
        due_date: Optional deadline for task completion (date-only, no time)
    """
    id: int
    title: str
    description: str = ""
    status: str = "Incomplete"
    priority: Priority = Priority.MEDIUM
    tags: List[str] = field(default_factory=list)
    due_date: Optional[date] = None  # NEW for Phase I Advanced

    def __post_init__(self):
        """
        Validate task data after initialization.

        Raises:
            ValueError: If title is empty, status is invalid, or due_date is past
        """
        # Validate title (existing)
        if not self.title or not self.title.strip():
            raise ValueError("Task title cannot be empty")

        # Validate status (existing)
        if self.status not in ("Complete", "Incomplete"):
            raise ValueError(f"Invalid status: {self.status}. Must be 'Complete' or 'Incomplete'")

        # Validate due_date (NEW - FR-002)
        if self.due_date:
            today = date.today()
            if self.due_date < today:
                raise ValueError(f"Due date cannot be in the past: {self.due_date}")
```

### Fields

| Field | Type | Required | Default | Description | Validation |
|--------|------|----------|-------------|-------------|
| id | int | Yes | N/A | Unique numeric identifier (auto-assigned) | Must be positive integer |
| title | str | Yes | N/A | Brief name of the task | Non-empty string |
| description | str | No | "" | Detailed information about the task | Any string or empty |
| status | str | No | "Incomplete" | Completion status | Must be "Complete" or "Incomplete" |
| priority | Priority | No | MEDIUM | Task importance level | Must be HIGH, MEDIUM, or LOW |
| tags | List[str] | No | [] | Text labels for categorization | Zero or more strings, each non-empty |
| due_date | Optional[date] | No | None | Deadline for task completion | Date only (no time), must be today or future |

### State Transitions

| Current State | Action | Next State | Valid? |
|--------------|--------|-------------|---------|
| Any | Set due_date (future) | due_date set | ✅ Yes |
| Any | Set due_date (today) | due_date set | ✅ Yes |
| Any | Set due_date (past) | Error | ❌ No - FR-002 |
| Any | Clear due_date | due_date = None | ✅ Yes |
| Incomplete | Mark complete | Complete | ✅ Yes |
| Complete | Mark incomplete | Incomplete | ✅ Yes |

### Validation Rules

**FR-009** (existing): Title cannot be empty
- Check: `if not self.title or not self.title.strip(): raise ValueError(...)`

**FR-042** (existing): Status must be "Complete" or "Incomplete"
- Check: `if self.status not in ("Complete", "Incomplete"): raise ValueError(...)`

**FR-002** (NEW): Due date must be today or future
- Check: `if self.due_date and self.due_date < date.today(): raise ValueError(...)`

**FR-008** (NEW): Today's date is valid due date
- Check: `if self.due_date == date.today():` (no error, allowed)

### Relationships

**Task** has many-to-many relationship with **Tags** (stored as list on Task entity)
**Task** is referenced by **HistoryEntry** (for undo functionality)

### Backward Compatibility

**FR-043**: Tasks created before due date feature function correctly
- Existing Task instances have `due_date=None` (default value)
- All existing Phase I Basic and Intermediate functionality works unchanged
- No breaking changes to Task API or constructor

## Entity: TaskTemplate (NEW)

### Purpose
Stores predefined task configuration for rapid task creation. Templates reduce data entry for recurring task patterns (e.g., weekly meetings, monthly reports).

### Definition

```python
from dataclasses import dataclass, field
from datetime import date
from typing import Optional, List
from src.models.enums import Priority

@dataclass
class TaskTemplate:
    """
    Represents a reusable task template with predefined values.

    Attributes:
        id: Unique numeric identifier (auto-assigned, separate from Task IDs)
        name: Human-readable name for the template (required, non-empty)
        title: Predefined title for tasks created from this template (required, non-empty)
        description: Optional predefined description
        priority: Optional predefined priority level
        tags: Optional predefined tags
        due_date: Optional absolute due date (date-only, no time)
    """
    id: int
    name: str
    title: str
    description: str = ""
    priority: Optional[Priority] = None
    tags: List[str] = field(default_factory=list)
    due_date: Optional[date] = None

    def __post_init__(self):
        """
        Validate template data after initialization.

        Raises:
            ValueError: If name or title is empty (FR-033)
        """
        # Validate name (FR-033)
        if not self.name or not self.name.strip():
            raise ValueError("Template name cannot be empty")

        # Validate title (FR-027)
        if not self.title or not self.title.strip():
            raise ValueError("Template title cannot be empty")
```

### Fields

| Field | Type | Required | Default | Description | Validation |
|--------|------|----------|-------------|-------------|
| id | int | Yes | N/A | Unique numeric identifier (separate from Task IDs) | Must be positive integer |
| name | str | Yes | N/A | Human-readable name for the template | Non-empty string |
| title | str | Yes | N/A | Predefined title for tasks created from this template | Non-empty string |
| description | str | No | "" | Optional predefined description | Any string or empty |
| priority | Optional[Priority] | No | None | Optional predefined priority level | Must be None, HIGH, MEDIUM, or LOW |
| tags | List[str] | No | [] | Optional predefined tags | Zero or more strings |
| due_date | Optional[date] | No | None | Optional absolute due date | Date only, no validation on future/past |

### Validation Rules

**FR-033**: Template name cannot be empty
- Check: `if not self.name or not self.name.strip(): raise ValueError(...)`

**FR-027**: Template title cannot be empty
- Check: `if not self.title or not self.title.strip(): raise ValueError(...)`

**FR-028**: Description, priority, tags, due_date are optional
- These fields can be None, empty list, or absent
- No validation applied (user can choose any values or None)

### Relationships

**TaskTemplate** is used to create **Task** instances (one-to-many relationship)

### Constraints

**FR-033**: Maximum 10 templates
- Enforced by TemplateService (not by model validation)
- TemplateService rejects creation when `len(templates) >= 10`

### Template Usage Flow

```
1. User selects "Manage Task Templates" -> "Create new template"
2. User enters template name (e.g., "Weekly Report")
3. User enters title (e.g., "Complete weekly report")
4. User optionally enters description, priority, tags, due_date
5. TaskTemplate instance created and stored
6. Later, user selects "Create task from template"
7. System displays available templates by name
8. User selects template
9. Task instance created with all template values applied
10. User can override any field during creation (FR-030)
```

## Entity: HistoryEntry (NEW)

### Purpose
Stores a single action in the undo history for error recovery. Each entry captures the action type, affected task IDs, and previous state snapshot.

### Definition

```python
from dataclasses import dataclass
from datetime import datetime
from typing import List, Dict, Any
from enum import Enum

class ActionType(Enum):
    """Types of actions tracked in history."""
    CREATE_TASK = "create_task"
    UPDATE_TASK = "update_task"
    DELETE_TASK = "delete_task"
    TOGGLE_STATUS = "toggle_status"
    BULK_UPDATE = "bulk_update"
    BULK_DELETE = "bulk_delete"

@dataclass
class HistoryEntry:
    """
    Represents a single action in undo history.

    Attributes:
        action_type: Type of action performed
        task_ids: List of task IDs affected by the action
        previous_state: Snapshot of task states before action (for undo)
        timestamp: When the action was performed
    """
    action_type: ActionType
    task_ids: List[int]
    previous_state: List[Dict[str, Any]]  # Snapshot of tasks before action
    timestamp: datetime
```

### Fields

| Field | Type | Required | Default | Description |
|--------|------|----------|-------------|
| action_type | ActionType | Yes | N/A | Type of action performed |
| task_ids | List[int] | Yes | N/A | List of task IDs affected by action |
| previous_state | List[Dict[str, Any]] | Yes | N/A | Snapshot of task states before action (for undo) |
| timestamp | datetime | Yes | N/A | When the action was performed |

### Previous State Structure

`previous_state` stores a list of task snapshots, where each snapshot is a dictionary containing all Task fields:

```python
{
    "id": 1,
    "title": "Example task",
    "description": "Example description",
    "status": "Incomplete",
    "priority": Priority.MEDIUM,
    "tags": ["work"],
    "due_date": None
}
```

**Note**: Priority is stored as enum value, tags as list, due_date as date object or None.

### Action Type Definitions

| Action Type | Description | Previous State Example |
|--------------|-------------|----------------------|
| CREATE_TASK | New task was created | Empty list (no previous state) |
| UPDATE_TASK | Task was modified | Snapshot of task before update |
| DELETE_TASK | Task was deleted | Snapshot of deleted task |
| TOGGLE_STATUS | Task status was toggled | Snapshot of task before toggle |
| BULK_UPDATE | Multiple tasks updated (status, priority) | Snapshots of all affected tasks before update |
| BULK_DELETE | Multiple tasks deleted | Snapshots of all deleted tasks |

### Undo Behavior

| Action Type | Undo Operation |
|--------------|---------------|
| CREATE_TASK | Delete the created task (FR-039) |
| UPDATE_TASK | Restore previous values from previous_state (FR-038) |
| DELETE_TASK | Restore deleted task from previous_state (FR-037) |
| TOGGLE_STATUS | Restore previous status from previous_state (FR-038) |
| BULK_UPDATE | Restore previous values for all affected tasks (FR-038) |
| BULK_DELETE | Restore all deleted tasks from previous_state (FR-037) |

### Constraints

**FR-034**: Maintain history of recent user actions
- Enforced by HistoryService (service, not model)
- Maximum 50 entries stored (FIFO when limit exceeded)

**FR-041**: Clear redo history on new action after undoing
- Undoing removes entry from history (pop from stack)
- New actions are appended to history (not inserted)
- Redo is not implemented (out of scope per spec)

### History Flow Example

```
1. Create task #1
   → HistoryEntry(action_type=CREATE_TASK, task_ids=[1], previous_state=[], timestamp=...)

2. Delete task #1
   → HistoryEntry(action_type=DELETE_TASK, task_ids=[1], previous_state=[{task1_snapshot}], timestamp=...)

3. Undo (reverses delete)
   → Pop last entry (DELETE_TASK)
   → Restore task #1 from previous_state
   → History now contains only CREATE_TASK entry

4. Update task #1
   → HistoryEntry(action_type=UPDATE_TASK, task_ids=[1], previous_state=[{task1_before_update}], timestamp=...)
   → History now contains CREATE_TASK, UPDATE_TASK entries

5. Undo (reverses update)
   → Pop last entry (UPDATE_TASK)
   → Restore task #1 to previous_state values
   → History now contains only CREATE_TASK entry
```

## Entity: TaskStatistics (NEW - Data Transfer Object)

### Purpose
Data transfer object (DTO) for task statistics returned by TaskService. Not stored, computed on-demand.

### Definition

```python
from dataclasses import dataclass
from typing import Dict, Counter

@dataclass
class TaskStatistics:
    """
    Represents summary statistics about task list.

    Attributes:
        total_tasks: Total count of all tasks
        completed_tasks: Count of completed tasks
        incomplete_tasks: Count of incomplete tasks
        completion_percentage: Percentage of tasks completed (0-100)
        priority_distribution: Count of tasks per priority level (High/Medium/Low)
        tag_distribution: Count of tasks per tag
        overdue_count: Count of tasks with due dates in the past
        due_today_count: Count of tasks with due date equal to today
        due_this_week_count: Count of tasks due within the next 7 days
    """
    total_tasks: int
    completed_tasks: int
    incomplete_tasks: int
    completion_percentage: float
    priority_distribution: Dict[str, int]  # {"High": 5, "Medium": 10, "Low": 3}
    tag_distribution: Dict[str, int]      # {"work": 7, "personal": 4}
    overdue_count: int
    due_today_count: int
    due_this_week_count: int
```

### Fields

| Field | Type | Description | Calculation |
|--------|------|-------------|--------------|
| total_tasks | int | Total count of all tasks | `len(tasks)` |
| completed_tasks | int | Count of completed tasks | `sum(1 for t in tasks if t.status == "Complete")` |
| incomplete_tasks | int | Count of incomplete tasks | `total_tasks - completed_tasks` |
| completion_percentage | float | Percentage of tasks completed (0-100) | `(completed_tasks / total_tasks * 100) if total_tasks > 0 else 0` |
| priority_distribution | Dict[str, int] | Count of tasks per priority level | `Counter(t.priority.value for t in tasks)` |
| tag_distribution | Dict[str, int] | Count of tasks per tag | `Counter(tag for t in tasks for tag in t.tags)` |
| overdue_count | int | Count of tasks with due dates in the past | `sum(1 for t in tasks if t.due_date and t.due_date < today)` |
| due_today_count | int | Count of tasks with due date equal to today | `sum(1 for t in tasks if t.due_date == today)` |
| due_this_week_count | int | Count of tasks due within the next 7 days | `sum(1 for t in tasks if t.due_date and today < t.due_date <= today + timedelta(days=7))` |

### Validation Rules

**FR-016**: Handle division by zero for percentages
- Check: `if total_tasks == 0: completion_percentage = 0` (or display "N/A")

**FR-015**: Handle empty task list gracefully
- All counts are zero when `total_tasks == 0`
- Display appropriate message in CLI (not in model)

### Calculation Complexity

- Time complexity: O(n) where n = number of tasks
- Space complexity: O(p + t) where p = number of unique priorities (3), t = number of unique tags
- Performance: <500ms for n=100 (per SC-018)

## Entity Relationships Summary

```
Task
├── has many tags (stored as list)
├── optional due_date (date object)
├── created from TaskTemplate (optional)
└── referenced by HistoryEntry (for undo)

TaskTemplate
├── has optional tags
├── optional due_date (date object)
├── optional priority
└── creates Task instances (one-to-many)

HistoryEntry
├── has ActionType (enum)
├── references one or more Task IDs
└── stores previous state snapshots

TaskStatistics
├── computed from list of Task instances
├── not stored (data transfer object only)
└── returned by TaskService.get_statistics()
```

## Service Layer Contracts

### TaskService Extensions

**Method**: `set_due_date(task_id: int, due_date: Optional[date]) -> tuple[bool, str]`
- **Purpose**: Set or update due date for a task (FR-001, FR-005)
- **Returns**: Success flag and message
- **Validation**: Due date must be today or future (FR-002)
- **Error**: If task not found or due_date is past

**Method**: `get_statistics() -> TaskStatistics`
- **Purpose**: Calculate and return task statistics (FR-009 through FR-014)
- **Returns**: TaskStatistics object
- **Calculation**: On-demand, no caching
- **Performance**: <500ms for up to 100 tasks (SC-018)

**Method**: `bulk_update_status(task_ids: List[int], status: str) -> tuple[bool, str]`
- **Purpose**: Mark multiple tasks complete or incomplete (FR-018, FR-019)
- **Returns**: Success flag and message with affected count
- **Confirmation**: Required by service caller (FR-022)
- **Validation**: All task IDs must exist

**Method**: `bulk_delete(task_ids: List[int]) -> tuple[bool, str]`
- **Purpose**: Delete multiple tasks at once (FR-020)
- **Returns**: Success flag and message with affected count
- **Confirmation**: Required by service caller (FR-022)
- **Validation**: All task IDs must exist

**Method**: `bulk_update_priority(task_ids: List[int], priority: Priority) -> tuple[bool, str]`
- **Purpose**: Update priority for multiple tasks (FR-021)
- **Returns**: Success flag and message with affected count
- **Confirmation**: Required by service caller (FR-022)
- **Validation**: All task IDs must exist

### TemplateService (NEW)

**Method**: `create_template(name: str, title: str, description: str = "", priority: Optional[Priority] = None, tags: List[str] = [], due_date: Optional[date] = None) -> tuple[bool, str, int]`
- **Purpose**: Create new task template (FR-026)
- **Returns**: Success flag, message, and template ID
- **Validation**: Name and title non-empty (FR-027, FR-033)
- **Constraint**: Maximum 10 templates (enforced by service)

**Method**: `list_templates() -> List[TaskTemplate]`
- **Purpose**: Get all templates for display (FR-031)
- **Returns**: List of all TaskTemplate instances

**Method**: `delete_template(template_id: int) -> tuple[bool, str]`
- **Purpose**: Delete a template (FR-032)
- **Returns**: Success flag and message
- **Validation**: Template ID must exist

**Method**: `use_template(template_id: int, overrides: Dict[str, Any] = None) -> Task`
- **Purpose**: Create task from template (FR-029)
- **Returns**: New Task instance with template values applied
- **Overrides**: User can override any field during creation (FR-030)
- **Validation**: Template ID must exist

### HistoryService (NEW)

**Method**: `record_action(action_type: ActionType, task_ids: List[int], previous_state: List[Dict[str, Any]]) -> None`
- **Purpose**: Add entry to undo history (FR-034)
- **Side effect**: Enforces 50 entry limit with FIFO behavior

**Method**: `undo() -> tuple[bool, str]`
- **Purpose**: Undo most recent action (FR-035)
- **Returns**: Success flag and message
- **Behavior**: Pop last entry, reverse action, update tasks
- **Error**: If no history available (FR-040)

**Method**: `has_undo() -> bool`
- **Purpose**: Check if undo is available
- **Returns**: True if history not empty

## Validation and Error Handling

### Date Validation (FR-002, FR-006, FR-007)

**Input**: User-provided string (e.g., "2026-01-15")
**Validation Steps**:
1. Check format matches YYYY-MM-DD pattern: `^\d{4}-\d{2}-\d{2}$`
2. Parse with `datetime.date.fromisoformat()` (handles leap years, month lengths)
3. Check date is not in the past: `parsed_date >= date.today()`
4. Return error messages:
   - "Invalid date format. Use YYYY-MM-DD (e.g., 2026-01-15)"
   - "Due date cannot be in the past: {parsed_date}"

### Template Validation (FR-027, FR-033)

**Input**: Template name and title from user
**Validation Steps**:
1. Check name is non-empty: `if not name or not name.strip():`
2. Check title is non-empty: `if not title or not title.strip():`
3. Check template limit not exceeded: `if len(templates) >= 10:`
4. Return error messages:
   - "Template name cannot be empty"
   - "Template title cannot be empty"
   - "Maximum 10 templates reached. Delete a template to create a new one."

### Bulk Operation Validation (FR-024)

**Input**: Start ID and end ID for range selection
**Validation Steps**:
1. Check both are positive integers
2. Check start ≤ end
3. Check all IDs in range exist in task storage
4. Return error messages:
   - "Invalid range: start ID must be ≤ end ID"
   - "One or more tasks in range do not exist"

### Undo Validation (FR-040)

**Input**: None (user requests undo)
**Validation Steps**:
1. Check history not empty: `if not history:`
2. Return error message: "No actions available to undo"

## Summary

This data model extends the existing Phase I Intermediate Task entity with `due_date` field and introduces three new entities (TaskTemplate, HistoryEntry, TaskStatistics). All entities are Python dataclasses with type hints and validation. The model maintains strict backward compatibility (FR-043) and aligns with all 44 functional requirements in the specification. No external dependencies required - uses Python standard library only (datetime, dataclasses, typing, enum).
