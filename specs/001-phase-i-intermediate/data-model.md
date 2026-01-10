# Data Model: Phase I Intermediate

**Feature**: 001-phase-i-intermediate
**Date**: 2026-01-01
**Purpose**: Extended Task entity, Priority enum, Filter/Sort/Search models for Intermediate features

## Entities

### Task

**Description**: Extended todo item with priority and tags for Phase I Intermediate.

**Fields**:

| Field | Type | Required | Default | Validation | Description |
|--------|------|----------|------------|-------------|
| id | int | Yes | - | Unique identifier (auto-assigned, starts at 1) |
| title | str | Yes | Non-empty | Brief description of the task |
| description | str | No | "" | Optional detailed description |
| status | str | Yes | "Incomplete" | Completion status: "Complete" or "Incomplete" |
| priority | Priority | No | Priority.MEDIUM | Task importance level (FR-002) |
| tags | list[str] | No | [] | Collection of text labels for categorization |

**Validation Rules**:

1. **Title Validation** (existing from Phase I Basic):
   - Must be non-empty string after stripping whitespace
   - Raises `ValueError` if empty

2. **Status Validation** (existing from Phase I Basic):
   - Must be "Complete" or "Incomplete"
   - Raises `ValueError` if invalid

3. **Priority Validation** (NEW):
   - Must be Priority enum value (HIGH, MEDIUM, LOW)
   - Defaults to MEDIUM for new tasks (FR-002)
   - Migrated to MEDIUM for existing tasks created before this feature (FR-038)

4. **Tags Validation** (NEW):
   - Zero or more tags allowed (FR-006, FR-011)
   - Each tag max 50 characters (constraint from spec)
   - Maximum 10 tags per task (constraint from spec)
   - Duplicate tags allowed (removed on user action, not stored)
   - Special characters preserved (FR-012)
   - Case-sensitive storage (user's original case)

**Relationships**: None (standalone entity in Phase I scope)

**State Transitions**:

| Current State | Action | Next State |
|---------------|--------|-------------|
| Incomplete | User marks as complete | Complete |
| Complete | User marks as incomplete | Incomplete |
| Any priority | User updates priority | New priority value (HIGH/MEDIUM/LOW) |
| Any tags | User adds tags | Tags list extended (up to 10) |
| Any tags | User removes tag | Tag removed from list |

**Python Dataclass Definition**:

```python
from dataclasses import dataclass, field
from enum import Enum

class Priority(Enum):
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"

@dataclass
class Task:
    id: int
    title: str
    description: str = ""
    status: str = "Incomplete"
    priority: Priority = Priority.MEDIUM
    tags: list[str] = field(default_factory=list)
```

---

### Priority

**Description**: Enumeration of task importance levels.

**Values**:

| Value | String Representation | Use Case |
|--------|---------------------|------------|
| Priority.HIGH | "High" | Urgent or critical task requiring immediate attention |
| Priority.MEDIUM | "Medium" | Normal priority task (default) |
| Priority.LOW | "Low" | Less urgent task that can be deferred |

**Validation Rules**:
- Only three valid values (HIGH, MEDIUM, LOW)
- Case-insensitive user input conversion (e.g., "high" → Priority.HIGH)
- Invalid input raises `ValueError`

**Python Enum Definition**:

```python
from enum import Enum

class Priority(Enum):
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"

    def __str__(self) -> str:
        return self.value
```

---

### SortBy

**Description**: Enumeration of sort criteria for task list.

**Values**:

| Value | String Representation | Behavior |
|--------|---------------------|----------|
| SortBy.TITLE_ASC | "Title (A-Z)" | Sort by title ascending, case-insensitive |
| SortBy.TITLE_DESC | "Title (Z-A)" | Sort by title descending, case-insensitive |
| SortBy.PRIORITY_HIGH_LOW | "Priority (High to Low)" | Sort HIGH → MEDIUM → LOW |
| SortBy.PRIORITY_LOW_HIGH | "Priority (Low to High)" | Sort LOW → MEDIUM → HIGH |

**Validation Rules**:
- Four valid sort options
- Case-insensitive user input conversion
- Invalid input raises `ValueError`

**Python Enum Definition**:

```python
from enum import Enum

class SortBy(Enum):
    TITLE_ASC = "Title (A-Z)"
    TITLE_DESC = "Title (Z-A)"
    PRIORITY_HIGH_LOW = "Priority (High to Low)"
    PRIORITY_LOW_HIGH = "Priority (Low to High)"
```

---

### FilterStatus

**Description**: Enumeration of completion status filter options.

**Values**:

| Value | String Representation | Behavior |
|--------|---------------------|----------|
| FilterStatus.ALL | "All" | Show all tasks (no status filter) |
| FilterStatus.COMPLETE | "Complete" | Show only completed tasks |
| FilterStatus.INCOMPLETE | "Incomplete" | Show only incomplete tasks |

**Validation Rules**:
- Three valid filter options
- Case-insensitive user input conversion
- Invalid input raises `ValueError`

**Python Enum Definition**:

```python
from enum import Enum

class FilterStatus(Enum):
    ALL = "All"
    COMPLETE = "Complete"
    INCOMPLETE = "Incomplete"
```

---

## Collections

### Task Collection (In-Memory Storage)

**Description**: Dictionary mapping task IDs to Task objects, maintained by TaskService.

**Structure**:
- Type: `dict[int, Task]`
- Key: Task ID (int)
- Value: Task object
- Location: TaskService._tasks (private attribute)

**Constraints**:
- In-memory only (no persistence to files or databases)
- Single instance (Phase I single-user scope)
- Auto-increment IDs starting from 1

**Python Implementation**:

```python
class TaskService:
    def __init__(self):
        self._tasks: dict[int, Task] = {}
        self._next_id: int = 1
```

---

## Search/Filter Models

### Search Query

**Description**: User-provided keyword for task search.

**Fields**:

| Field | Type | Required | Default | Validation |
|--------|------|----------|------------|
| keyword | str | No | "" (empty shows all tasks) |

**Behavior**:
- Case-insensitive search
- Matches in title OR description (logical OR)
- Empty keyword returns all tasks (FR-019)

---

### Filter Query

**Description**: Combined filter criteria for status, priority, and tag.

**Fields**:

| Field | Type | Required | Default | Validation |
|--------|------|----------|------------|
| status_filter | FilterStatus | No | FilterStatus.ALL |
| priority_filter | Priority | No | None (no priority filter) |
| tag_filter | str | No | None (no tag filter) |

**Behavior**:
- All filters applied using AND logic (all conditions must be met)
- Any filter can be None/ALL for no filtering
- Combined filters supported (e.g., status=Complete + priority=HIGH + tag="work")

---

### Sort Query

**Description**: Sort criteria applied to task list.

**Fields**:

| Field | Type | Required | Validation |
|--------|------|----------|------------|
| sort_by | SortBy | Yes | Must be valid SortBy enum value |

**Behavior**:
- Stable sort (preserves relative order for equal keys)
- Applies to filtered result set if filters active
- Case-insensitive title sorting

---

## Validation Models

### Tag Validation

**Rules**:
1. **Length**: Maximum 50 characters per tag
   - Valid: `"work"`, `"personal-project"`
   - Invalid: `"a" * 51` (51 characters)

2. **Count**: Maximum 10 tags per task
   - Valid: `["work", "home", "personal"]` (3 tags)
   - Invalid: `["tag1", ..., "tag11"]` (11 tags)

3. **Characters**: All characters allowed (including special characters)
   - Valid: `"work"`, `"@work"`, `"work-2024"`, `"#urgent"`

**Error Messages**:
- Tag too long: `"Tag 'exampletag...' exceeds 50 character limit."`
- Too many tags: `"Cannot add more than 10 tags to a task."`

---

### Priority Validation

**Rules**:
1. **Valid Values**: Only HIGH, MEDIUM, LOW allowed
2. **Case-Insensitive**: User input "high", "HIGH", "High" all valid
3. **Conversion**: String input converted to Priority enum

**Error Messages**:
- Invalid priority: `"Invalid priority. Please choose High, Medium, or Low."`

---

## Data Flow Examples

### Create Task with Priority and Tags

```python
# User input
title = "Review documentation"
description = "Check API docs for new endpoints"
priority_input = "high"  # User types "high"
tags_input = "work, urgent"  # User types comma-separated

# Validation
priority = validate_priority(priority_input)  # Returns Priority.HIGH
tags = [t.strip() for t in tags_input.split(",")]  # ["work", "urgent"]

# Create task
task = Task(
    id=1,
    title="Review documentation",
    description="Check API docs for new endpoints",
    priority=Priority.HIGH,
    tags=["work", "urgent"]
)

# Result
task.id == 1  # ✅
task.title == "Review documentation"  # ✅
task.description == "Check API docs for new endpoints"  # ✅
task.status == "Incomplete"  # ✅ (default)
task.priority == Priority.HIGH  # ✅
task.tags == ["work", "urgent"]  # ✅
```

### Search Tasks

```python
# User searches for "API"
keyword = "API"

# Search logic (case-insensitive, title OR description)
tasks = [
    task for task in service.list_tasks()
    if "api" in task.title.lower() or "api" in task.description.lower()
]

# Matches tasks with:
# - Title: "Review API documentation"
# - Description: "Learn about REST API design"
# - Does NOT match: "Review documentation" (no "api" in title or description)
```

### Filter Tasks

```python
# User filters: Complete tasks, High priority, "work" tag
status_filter = FilterStatus.COMPLETE
priority_filter = Priority.HIGH
tag_filter = "work"

# Filter logic (AND condition)
tasks = service.list_tasks()

# 1. Filter by status
tasks = [t for t in tasks if t.status == "Complete"]

# 2. Filter by priority
tasks = [t for t in tasks if t.priority == Priority.HIGH]

# 3. Filter by tag
tasks = [t for t in tasks if "work" in t.tags]

# Result: Tasks that are Complete AND High priority AND have "work" tag
```

### Sort Tasks

```python
# User sorts by priority (High to Low)
sort_by = SortBy.PRIORITY_HIGH_LOW

# Sort logic
priority_order = {Priority.HIGH: 0, Priority.MEDIUM: 1, Priority.LOW: 2}
sorted_tasks = sorted(tasks, key=lambda t: priority_order[t.priority])

# Result: [High1, High2, Medium1, Medium2, Low1, Low2]
# Stable sort: High1 before High2 (original order preserved)
```

---

## Backward Compatibility

### Existing Task Handling

Tasks created before Phase I Intermediate (without priority and tags fields):

1. **Missing priority field**: Defaults to Priority.MEDIUM (FR-038)
2. **Missing tags field**: Defaults to empty list [] (FR-039)

**No migration required** - Task dataclass default values handle this automatically.

### Existing Tests

All existing unit tests for Task model continue to pass:
- Task creation with title and description (existing behavior unchanged)
- Task validation for title and status (existing behavior unchanged)
- Task string representation (extended to show priority and tags)

---

## Index Strategy

**Decision**: No indexes required for Phase I Intermediate.

**Rationale**:
- Linear scan O(n) is acceptable for ≤100 tasks (Phase I scope constraint)
- Index maintenance overhead exceeds benefits for in-memory storage
- No persistence (indexes lost on exit, no need to rebuild)

**Future Consideration**: If Phase II extends to persistent storage or >1000 tasks, consider:
- Dictionary indexes: `{"high": [task_ids], "work": [task_ids]}`
- Reverse indexes: `{"title": set(task_ids), "description": set(task_ids)}`

---

## Summary

**Entities Defined**:
1. ✅ Task (extended with priority and tags)
2. ✅ Priority (enum: HIGH, MEDIUM, LOW)
3. ✅ SortBy (enum: 4 sort options)
4. ✅ FilterStatus (enum: 3 status filter options)

**Collections Defined**:
1. ✅ Task collection (dict[int, Task] in TaskService)

**Validation Models Defined**:
1. ✅ Tag validation (50 chars max, 10 per task)
2. ✅ Priority validation (3 valid values, case-insensitive)

**Data Flow Examples Provided**:
1. ✅ Create task with priority and tags
2. ✅ Search tasks (case-insensitive, OR logic)
3. ✅ Filter tasks (AND logic, combined filters)
4. ✅ Sort tasks (stable sort, custom order)

**Backward Compatibility Documented**:
1. ✅ Existing tasks auto-default to Medium priority and empty tags
2. ✅ Existing tests continue to pass

**Ready for**: Implementation and unit test generation
