# Data Model: Phase I - Basic Todo Console Application

**Feature**: Phase I - Basic Todo Console Application
**Date**: 2025-12-28
**Status**: Complete

## Overview

Phase I has a single entity: **Task**. Tasks are stored in memory only and are lost when the application exits. This document defines the Task entity structure, validation rules, state transitions, and storage approach.

---

## Entity: Task

### Purpose

Represents a single todo item with a title, optional description, completion status, and unique identifier.

### Attributes

| Attribute | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `id` | `int` | Yes | Auto-assigned | Unique numeric identifier, starts at 1, increments sequentially |
| `title` | `str` | Yes | N/A | Short description of the task (non-empty after stripping whitespace) |
| `description` | `str` | No | `""` | Optional detailed description (can be empty string) |
| `status` | `str` | Yes | `"Incomplete"` | Completion status, must be exactly `"Complete"` or `"Incomplete"` |

### Python Implementation

```python
from dataclasses import dataclass
from typing import Optional

@dataclass
class Task:
    """
    Represents a single todo item.

    Attributes:
        id: Unique numeric identifier (auto-assigned, starts at 1)
        title: Short description of the task (required, non-empty)
        description: Optional detailed description (can be empty)
        status: Completion status ("Complete" or "Incomplete")
    """
    id: int
    title: str
    description: str = ""
    status: str = "Incomplete"

    def __post_init__(self):
        """
        Validate task data after initialization.

        Raises:
            ValueError: If title is empty or status is invalid
        """
        # Validate title (FR-009)
        if not self.title or not self.title.strip():
            raise ValueError("Task title cannot be empty")

        # Validate status
        if self.status not in ("Complete", "Incomplete"):
            raise ValueError(f"Invalid status: {self.status}. Must be 'Complete' or 'Incomplete'")

    def __str__(self) -> str:
        """Return user-friendly string representation."""
        return f"ID: {self.id} | Title: {self.title} | Status: {self.status}"

    def __repr__(self) -> str:
        """Return detailed string representation for debugging."""
        return (f"Task(id={self.id}, title={self.title!r}, "
                f"description={self.description!r}, status={self.status})")
```

### Validation Rules

Based on functional requirements FR-009 (title validation) and FR-014 (ID validation):

1. **ID Validation**
   - Must be positive integer (>= 1)
   - Must be unique within the current session
   - Auto-assigned by TaskService, users don't provide IDs

2. **Title Validation**
   - Required (cannot be None)
   - Non-empty after stripping leading/trailing whitespace
   - Enforced in Task.__post_init__ and CLI input handler
   - Error message: "Task title cannot be empty"

3. **Description Validation**
   - Optional (can be empty string)
   - No length restrictions
   - Defaults to empty string if not provided

4. **Status Validation**
   - Must be exactly "Complete" or "Incomplete" (case-sensitive)
   - Defaults to "Incomplete" for new tasks
   - Enforced in Task.__post_init__
   - Error message: "Invalid status: {status}. Must be 'Complete' or 'Incomplete'"

### State Transitions

Tasks have two valid states with specific transitions:

```
         ┌─────────────┐
    ┌───>│ Incomplete  │<────┐
    │    └─────────────┘     │
    │           │             │
    │           │ (Initial)   │
    │           v             │
    │    ┌─────────────┐     │
    └────│  Complete   │─────┘
         └─────────────┘
```

**Transitions**:
1. **Creation**: New tasks always start as "Incomplete"
2. **Mark Complete**: "Incomplete" → "Complete" (via toggle_status)
3. **Mark Incomplete**: "Complete" → "Incomplete" (via toggle_status)

**Invalid Transitions**: None - only two states, both are reachable from each other

**Transition Trigger**: User selects menu option 5 ("Mark task complete/incomplete") and provides task ID

### Relationships

**Phase I**: No relationships - single entity, no foreign keys

**Future Phases** (for reference, not implemented in Phase I):
- Phase II: Task → User (many-to-one, task belongs to user)
- Phase III: Task → Tags (many-to-many, task can have multiple tags)
- Phase IV: Task → WorkflowStep (many-to-one, task part of workflow)

---

## Storage Model

### In-Memory Storage

**Data Structure**: Python dictionary with integer keys

```python
# In TaskService class
self._tasks: dict[int, Task] = {}  # task_id -> Task object
self._next_id: int = 1              # Auto-increment counter for IDs
```

**Characteristics**:
- **Performance**: O(1) average-case for get, set, delete by ID
- **Ordering**: Insertion order preserved (Python 3.7+ guarantee)
- **Capacity**: Limited by available RAM, expected max ~100 tasks per session
- **Persistence**: None - data lost on application exit (per specification)

### ID Generation

**Strategy**: Auto-incrementing counter, never reuse deleted IDs

```python
def add_task(self, title: str, description: str = "") -> tuple[bool, str, int]:
    """
    Create a new task with auto-generated ID.

    Args:
        title: Task title (required, non-empty)
        description: Task description (optional)

    Returns:
        Tuple of (success: bool, message: str, task_id: int)
    """
    task_id = self._next_id
    self._next_id += 1  # Increment for next task, never decrement

    try:
        task = Task(id=task_id, title=title, description=description)
        self._tasks[task_id] = task
        return (True, f"Task added successfully! (ID: {task_id})", task_id)
    except ValueError as e:
        # Title validation failed
        return (False, str(e), -1)
```

**Why This Approach**:
- Simple implementation (single counter variable)
- Predictable IDs (users see 1, 2, 3, 4, ...)
- Matches spec assumption ASM-004: "Task IDs are sequential integers"
- User-friendly (small integers, easy to type)
- No collision risk within session

**Alternative Approaches** (rejected in research.md):
- UUID: Too complex, not user-friendly
- Timestamp: Not sequential, collision risk
- Reuse deleted IDs: Confusing for users, contradicts spec

---

## Data Access Patterns

### Common Operations

All operations are performed via the `TaskService` class, which encapsulates storage:

1. **Create Task** (add_task)
   - Generate new ID
   - Validate title
   - Create Task object
   - Store in dict
   - Return success + ID

2. **Read Task** (get_task)
   - Lookup by ID in dict
   - Return Task or None

3. **Read All Tasks** (list_tasks)
   - Return list of all tasks in insertion order
   - Empty list if no tasks

4. **Update Task** (update_task)
   - Lookup by ID
   - Validate new title (if provided)
   - Update title and/or description
   - Return success status

5. **Delete Task** (delete_task)
   - Lookup by ID
   - Remove from dict
   - Return success status

6. **Toggle Status** (toggle_status)
   - Lookup by ID
   - Flip status: "Complete" ↔ "Incomplete"
   - Return success status

### Query Patterns

**All Queries are In-Memory Dictionary Operations**:

```python
# Get single task by ID
task = self._tasks.get(task_id)  # O(1)

# Get all tasks
all_tasks = list(self._tasks.values())  # O(n)

# Check if task exists
exists = task_id in self._tasks  # O(1)

# Count tasks
count = len(self._tasks)  # O(1)

# Filter tasks by status (example, not required in Phase I)
complete_tasks = [t for t in self._tasks.values() if t.status == "Complete"]  # O(n)
```

**Performance Characteristics**:
- Single task operations: O(1) average case
- List all tasks: O(n) where n is task count
- Filter/search: O(n) (not required in Phase I, but possible)

**Expected Scale**: ~10-100 tasks per session, all operations effectively instant

---

## Migration Path to Phase II

### Phase II Changes (Database Persistence)

When Phase II adds database persistence, the Task model will convert to SQLModel:

```python
from sqlmodel import SQLModel, Field

class Task(SQLModel, table=True):
    """
    Task entity with database persistence.
    """
    id: int | None = Field(default=None, primary_key=True)  # Auto-increment by DB
    title: str = Field(min_length=1)  # Non-empty validation
    description: str = Field(default="")
    status: str = Field(default="Incomplete")
    user_id: int = Field(foreign_key="user.id")  # Phase II: multi-user support

    # Validation moved to Pydantic validators
    @validator('status')
    def validate_status(cls, v):
        if v not in ("Complete", "Incomplete"):
            raise ValueError("Status must be 'Complete' or 'Incomplete'")
        return v
```

**Changes Required**:
1. Add SQLModel inheritance and `table=True`
2. Change ID field to optional (auto-generated by database)
3. Add Field descriptors for constraints (min_length, default, foreign_key)
4. Move validation to Pydantic validators
5. Add user_id foreign key for multi-user support

**Service Layer Changes**:
- Replace `dict[int, Task]` with database session
- Replace dict operations with SQLModel queries
- Add transaction handling (commit, rollback)
- Interface remains the same (add, get, update, delete, list, toggle)

**CLI Layer Changes**: None - CLI layer uses service interface, agnostic to storage

**Benefits of Current Design**:
- Clean separation makes migration straightforward
- Service interface doesn't leak storage details
- Task model structure matches future database schema

---

## Data Integrity

### Phase I Constraints

Since Phase I uses in-memory storage with no persistence:

1. **No Concurrent Access Issues**: Single-threaded, single-user application
2. **No Transaction Requirements**: All operations are atomic (dict operations)
3. **No Referential Integrity**: Only one entity, no foreign keys
4. **No Data Loss Recovery**: Expected behavior per specification (NFR-004)

### Validation Enforcement

**Two-Layer Validation**:

1. **CLI Layer** (input_handler.py):
   - Validate title non-empty before creating Task
   - Validate task ID is positive integer before calling service
   - Validate menu choices are in range 1-6
   - **Purpose**: Fast fail with user-friendly error messages

2. **Model Layer** (Task.__post_init__):
   - Enforce title non-empty (final check)
   - Enforce status is "Complete" or "Incomplete"
   - **Purpose**: Guarantee data integrity, prevent invalid Task objects

**Service Layer**: Assumes input is validated, focuses on business logic

### Error Handling

**Validation Errors**:
- Empty title → ValueError with message "Task title cannot be empty"
- Invalid status → ValueError with message "Invalid status: {status}..."
- Caught by CLI layer, displayed to user, operation aborted

**Not Found Errors**:
- Invalid task ID → Service returns (False, "Task not found")
- Handled gracefully by CLI layer with error message

**No Data Corruption**: Python's strong typing and dataclass validation prevent invalid Task objects from existing

---

## Example Data Lifecycle

### Scenario: User adds, updates, and completes a task

**Step 1: Add Task**
```python
# User input: title="Buy groceries", description="Milk, eggs, bread"
service = TaskService()
success, message, task_id = service.add_task("Buy groceries", "Milk, eggs, bread")

# State after:
# _tasks = {1: Task(id=1, title="Buy groceries", description="Milk, eggs, bread", status="Incomplete")}
# _next_id = 2
```

**Step 2: Update Task**
```python
# User input: task_id=1, new_title="Buy groceries and toiletries"
success, message = service.update_task(1, title="Buy groceries and toiletries", description=None)

# State after:
# _tasks = {1: Task(id=1, title="Buy groceries and toiletries", description="Milk, eggs, bread", status="Incomplete")}
# (description unchanged because None passed)
```

**Step 3: Mark Complete**
```python
# User input: task_id=1
success, message = service.toggle_status(1)

# State after:
# _tasks = {1: Task(id=1, title="Buy groceries and toiletries", description="Milk, eggs, bread", status="Complete")}
```

**Step 4: View Tasks**
```python
tasks = service.list_tasks()
# Returns: [Task(id=1, title="Buy groceries and toiletries", ...)]
```

**Step 5: Exit Application**
```python
# All data lost (expected behavior per NFR-004)
# _tasks dict is garbage collected
```

---

## Summary

**Entity Count**: 1 (Task)
**Storage**: In-memory Python dict
**Persistence**: None (data lost on exit)
**ID Generation**: Auto-incrementing counter
**Validation**: Two layers (CLI + Model)
**Relationships**: None (single entity)
**Future-Proof**: Clean structure enables Phase II database migration

**Status**: Data model complete and ready for implementation.
