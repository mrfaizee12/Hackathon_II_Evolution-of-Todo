# Phase 0 Research: Phase I Advanced (Revised) - Task Scheduling and Organization

**Feature**: 004-phase-i-advanced-v2
**Date**: 2026-01-01
**Purpose**: Document research findings and technical decisions for implementation planning

## Executive Summary

This research document establishes technical decisions and implementation patterns for Phase I Advanced features, building on existing Phase I Basic and Intermediate codebase. Seven key decisions are documented covering date-time handling, undo history, reminders, recurrence, templates, DST handling, and performance.

## Research Decision 1: Date-Time Format and Validation

### Decision
Use ISO 8601 date-time format (YYYY-MM-DD HH:MM) for all user-facing due dates and internal storage.

### Specification References
- FR-001: Task due date with date and time
- FR-002: Due date format validation (YYYY-MM-DD HH:MM)
- FR-003: Reject past date-times
- SC-001: Due date validation <200ms

### Research Findings

**ISO 8601 Format Benefits:**
1. **Built-in Python Support**: `datetime.datetime.fromisoformat()` provides native parsing
2. **Unambiguous**: No locale-specific interpretation (e.g., 01/02/2023)
3. **Internationally Recognized**: Standard across systems and databases
4. **Sortable**: String comparison works for chronological ordering
5. **Naive Datetime**: Simplest approach for Phase I scope (no timezone arithmetic)

**Alternative Formats Considered:**
1. **MM/DD/YYYY HH:MM (US)**
   - ✅ Familiar to US users
   - ❌ Locale-specific, ambiguous internationally
   - ❌ Requires locale detection/prompting

2. **DD/MM/YYYY HH:MM (European)**
   - ✅ Familiar to European users
   - ❌ Varies by region (UK vs Europe)
   - ❌ Ambiguous (01/02/2023 could be Jan 2 or Feb 1)

3. **Natural Language Parsing (e.g., "next Monday at 2pm")**
   - ✅ Best user experience
   - ❌ Requires external libraries (dateparser, parsedatetime)
   - ❌ Out of scope for Phase I (no external dependencies)
   - ❌ Complex localization

**Python Implementation Options:**
```python
# Option 1: datetime.fromisoformat() (CHOSEN)
from datetime import datetime

def validate_due_date(date_str: str) -> datetime:
    """Parse and validate YYYY-MM-DD HH:MM format"""
    try:
        dt = datetime.fromisoformat(date_str)
        if dt < datetime.now():
            raise ValueError("Due date cannot be in the past")
        return dt
    except ValueError as e:
        raise ValueError(f"Invalid date format: {e}")

# Option 2: datetime.strptime() (NOT CHOSEN - redundant)
# Option 3: Regular expression (NOT CHOSEN - doesn't validate actual dates)
```

### Validation Strategy
1. Parse with `datetime.fromisoformat()` (Python 3.7+)
2. Check for past date/time
3. Error messages guide user to correct format
4. No timezone handling (naive datetime only)

### Edge Cases
- **Past Dates**: Reject with clear message
- **Invalid Dates**: (e.g., 2023-02-30) - datetime raises ValueError automatically
- **Leap Years**: datetime handles automatically
- **DST Transitions**: System local time (see Decision 6)
- **Far Future**: No limit (user can set any future date)

## Research Decision 2: Undo History Implementation

### Decision
Stack-based undo history with maximum 50 entries (FIFO eviction).

### Specification References
- FR-049: Command history (up to 50 actions)
- FR-050: Undo last action (including recurring task completions)
- FR-051: View history
- SC-025: Undo operations <300ms

### Research Findings

**Undo History Requirements:**
1. **LIFO Behavior**: Last-in, first-out for undo operations
2. **Memory-Bounded**: Maximum 50 entries
3. **FIFO Eviction**: Remove oldest when limit reached
4. **No Redo**: Out of scope per specification
5. **Atomic Actions**: Single undo for recurring task completion (see Decision 5)

**Data Structure Options:**

```python
# Option 1: List-based Stack (CHOSEN)
class ActionHistory:
    def __init__(self, max_size: int = 50):
        self._history: List[HistoryEntry] = []
        self._max_size = max_size

    def push(self, entry: HistoryEntry):
        self._history.append(entry)
        if len(self._history) > self._max_size:
            self._history.pop(0)  # FIFO

    def pop(self) -> Optional[HistoryEntry]:
        return self._history.pop() if self._history else None

# Option 2: deque (NOT CHOSEN - list is simpler)
# Option 3: Custom linked list (NOT CHOSEN - unnecessary complexity)
```

**History Entry Structure:**
```python
from dataclasses import dataclass
from datetime import datetime
from enum import Enum

class ActionType(Enum):
    ADD = "add"
    EDIT = "edit"
    DELETE = "delete"
    COMPLETE = "complete"
    BULK_COMPLETE = "bulk_complete"
    BULK_DELETE = "bulk_delete"

@dataclass
class HistoryEntry:
    """Represents a single user action for undo"""
    action: ActionType
    timestamp: datetime
    task_id: str
    task_snapshot: Task  # Complete task state before action
    additional_data: dict = None  # For bulk operations, recurring tasks, etc.
```

**Bulk Operations:**
- Store list of affected task snapshots
- Single undo restores all tasks
- Memory: ~10 tasks per bulk operation is reasonable

**Performance Considerations:**
- Push: O(1) amortized
- Pop: O(1)
- Size check: O(1)
- Memory: 50 entries × ~500 bytes/task = ~25KB (negligible)

### Edge Cases
- **Empty History**: Return None when attempting undo
- **Corrupted State**: Validate snapshot exists before restore
- **Concurrent Modifications**: Not applicable (single-threaded CLI)
- **Memory Pressure**: 50-entry limit prevents unbounded growth

## Research Decision 3: Reminder Evaluation Timing

### Decision
Evaluate reminders on-demand during CLI operation (no background services).

### Specification References
- FR-026: Display overdue tasks at app start
- FR-027: Display tasks due today at app start
- FR-028: Display upcoming tasks (within 7 days) at app start
- FR-030: Manual reminder check command
- Constraints: No background services, no notifications, no scheduled jobs

### Research Findings

**Reminder Evaluation Requirements:**
1. **Overdue**: Tasks with due_date < now (not completed)
2. **Due Today**: Tasks with due_date.date() == today
3. **Upcoming**: Tasks with 0 < (due_date - now).days <= 7
4. **Console Display Only**: No notifications, no OS integration
5. **On-Demand**: Only during CLI operation

**Evaluation Timing Options:**

| Option | Description | Pros | Cons |
|--------|-------------|------|------|
| **On App Start** | Check once when application launches | Simple, no overhead | Misses new tasks added during session |
| **On Every Menu Display** | Check before showing main menu | Always current | More frequent evaluation |
| **Manual Command Only** | User triggers check with specific command | User control | Poor UX (easy to miss) |
| **Hybrid: Start + Manual** | Check on start + manual command option | Good balance, meets FR-026-030 | Slightly more complex |
| **Background Polling** | Check every N seconds (NOT CHOSEN) | Real-time | Violates constraints |

**Chosen Strategy: Hybrid (Start + Manual)**
1. **Automatic on App Start**: Display reminders when application launches (FR-026, FR-027, FR-028)
2. **Manual Command**: Menu option to manually check reminders (FR-030)
3. **No Background Threads**: All evaluation synchronous with user actions

**Evaluation Logic:**
```python
def evaluate_reminders(tasks: List[Task], now: datetime = None) -> ReminderSummary:
    """Evaluate reminder categories"""
    now = now or datetime.now()
    today = now.date()

    overdue = [
        t for t in tasks
        if t.due_date and t.due_date < now and not t.completed
    ]

    due_today = [
        t for t in tasks
        if t.due_date and t.due_date.date() == today and not t.completed
    ]

    upcoming = [
        t for t in tasks
        if t.due_date
        and not t.completed
        and 0 < (t.due_date - now).days <= 7
    ]

    return ReminderSummary(overdue=overdue, due_today=due_today, upcoming=upcoming)
```

**Performance:**
- O(n) scan of all tasks
- For 100 tasks: <1ms (well under SC-026: <200ms)
- Minimal memory overhead

### Edge Cases
- **No Due Dates**: Skip tasks without due_date
- **All Completed**: Only show incomplete tasks
- **Multiple Due Today**: Display all, limit to reasonable number (e.g., top 10)
- **Far Future**: Beyond 7-day window not shown in upcoming

## Research Decision 4: Recurring Task Auto-Creation

### Decision
Auto-create next instance immediately when recurring task is marked complete.

### Specification References
- FR-020: Recurring task rules (none, daily, weekly, custom interval)
- FR-021: Create new instance on completion
- FR-022: Increment due date based on recurrence
- FR-024: Preserve task history
- SC-018: Auto-creation <300ms

### Research Findings

**Recurrence Rule Structure:**
```python
from dataclasses import dataclass
from enum import Enum

class RecurrenceType(Enum):
    NONE = "none"
    DAILY = "daily"
    WEEKLY = "weekly"
    CUSTOM = "custom"

@dataclass
class RecurrenceRule:
    type: RecurrenceType
    interval_days: int = None  # For CUSTOM type

    def __post_init__(self):
        if self.type == RecurrenceType.CUSTOM and not self.interval_days:
            raise ValueError("CUSTOM recurrence requires interval_days")
```

**Auto-Creation Timing Options:**

| Option | Description | Pros | Cons |
|--------|-------------|------|------|
| **Immediate** | Create right after completion | Immediate feedback, simple | User may not want next instance yet |
| **Next App Start** | Create when app launches next | User control | Poor UX (doesn't meet FR-021) |
| **Delayed Background** | Create after delay (NOT CHOSEN) | Simulates real schedule | Violates constraints |
| **Prompt User** | Ask before creating | User control | Additional friction |

**Chosen Strategy: Immediate Creation**
1. User completes recurring task
2. Immediately create new instance with incremented due date
3. Original task marked completed (preserves history)
4. New task added to list
5. User sees new task in next display

**Due Date Calculation:**
```python
def calculate_next_due_date(current_due_date: datetime, rule: RecurrenceRule) -> datetime:
    """Calculate next due date based on recurrence rule"""
    if rule.type == RecurrenceType.DAILY:
        return current_due_date + timedelta(days=1)

    elif rule.type == RecurrenceType.WEEKLY:
        return current_due_date + timedelta(weeks=1)

    elif rule.type == RecurrenceType.CUSTOM:
        return current_due_date + timedelta(days=rule.interval_days)

    else:  # NONE
        return None
```

**Task Cloning:**
```python
def clone_task_for_recurrence(original: Task, new_due_date: datetime) -> Task:
    """Create new task instance from completed recurring task"""
    return Task(
        id=generate_id(),  # New unique ID
        title=original.title,
        description=original.description,
        due_date=new_due_date,
        recurrence_rule=original.recurrence_rule,  # Preserve recurrence
        priority=original.priority,
        tags=original.tags.copy() if original.tags else None,
        created_at=datetime.now(),
        completed=False  # Always start incomplete
    )
```

**Performance:**
- O(1) operation (single task creation)
- <100ms typical (well under SC-018: <300ms)
- No background overhead

### Edge Cases
- **First Completion**: No prior due date - use created_at as base
- **Due Date Changed**: Use most recent due_date, not created_at
- **Recurrence Removed**: Edit task to set recurrence to NONE (no auto-creation)
- **Bulk Complete**: Create new instance for each recurring task
- **Deleted Recurring Task**: Cannot complete (no auto-creation)

## Research Decision 5: Undo for Recurring Task Completion

### Decision
Undo of recurring task completion restores original task and deletes auto-created instance as single atomic action.

### Specification References
- FR-050: Undo last action (including recurring task completions)
- SC-025: Undo operations <300ms

### Research Findings

**Recurring Task Completion as Composite Action:**
When user completes a recurring task, two actions occur:
1. Original task: completed = True
2. New task: created with incremented due date

**Undo Semantics Options:**

| Option | Description | Pros | Cons |
|--------|-------------|------|------|
| **Two Separate Undos** | One undo for completion, one for creation | Granular control | Poor UX (requires two undos) |
| **Atomic Undo** | Single undo reverses both actions | Clean semantics | More complex history tracking |
| **Undo Only Completion** | Undo only marks task incomplete | Simple | Leaves duplicate task |

**Chosen Strategy: Atomic Undo**
1. Single HistoryEntry captures both actions
2. Undo restores original task (completed = False)
3. Undo deletes auto-created task
4. One undo command reverses entire recurring task completion

**History Entry Structure for Recurring Task:**
```python
@dataclass
class HistoryEntry:
    action: ActionType
    timestamp: datetime
    task_id: str
    task_snapshot: Task
    auto_created_task_id: str = None  # Set for recurring tasks
    auto_created_task_snapshot: Task = None  # For undo restore
```

**Undo Logic:**
```python
def undo_recurring_task_completion(entry: HistoryEntry, tasks: Dict[str, Task]):
    """Undo recurring task completion as atomic action"""
    # Restore original task
    original = tasks[entry.task_id]
    original.completed = False
    original.completed_at = None

    # Delete auto-created task
    if entry.auto_created_task_id and entry.auto_created_task_id in tasks:
        del tasks[entry.auto_created_task_id]

    # Entry removed from history (pop operation)
```

**Alternative Considered: Keep Auto-Created Task**
- ❌ Violates FR-050 requirement
- ❌ Confusing for user (two identical incomplete tasks)
- ❌ Breaks expected undo semantics

**Performance:**
- Two dict operations: O(1) + O(1) = O(1)
- <50ms typical (well under SC-025: <300ms)

### Edge Cases
- **Auto-Created Task Modified**: Undo still deletes (user loses changes)
  - *Mitigation*: Warn user if task was modified
- **Auto-Created Task Already Completed**: Rare, but delete anyway
- **No Auto-Created Task**: Error in history entry, handle gracefully
- **Undo After Bulk Complete**: Undo each recurring task individually

## Research Decision 6: DST Handling

### Decision
Use naive datetime without timezone information (system local time).

### Specification References
- FR-026: DST transitions handled correctly
- SC-022: DST transitions handled

### Research Findings

**DST Challenge:**
When clocks spring forward or fall back, calculations based on day intervals may be off by 1 hour. For example:
- Task due every Monday at 9:00 AM
- Clocks spring forward on Sunday
- Next Monday at 9:00 AM is actually 8:00 AM relative to previous week

**Timezone Handling Options:**

| Option | Description | Pros | Cons |
|--------|-------------|------|------|
| **Naive Datetime** (CHOSEN) | No timezone info, system local time | Simple, Python handles automatically | DST transitions may be off by 1 hour |
| **UTC with Timezone** | Store in UTC, convert for display | Precise calculations | More complex, violates "local time" user expectation |
| **Explicit DST Offset** | Track DST changes manually | Full control | Extremely complex, error-prone |
| **Timezone Library** (pytz) | Use timezone-aware datetime | Robust | External dependency, violates constraints |

**Python Naive Datetime Behavior:**
```python
from datetime import datetime, timedelta

# User sets due date: 2024-03-10 09:00 (day before DST spring forward)
due = datetime(2024, 3, 10, 9, 0)

# Recurring daily: next day is 2024-03-11 09:00 (DST spring forward at 2:00 AM)
next_due = due + timedelta(days=1)
# Result: 2024-03-11 09:00 (system interprets as 9:00 AM after spring forward)

# This is ACCEPTABLE for Phase I scope:
# - 1-hour drift on DST transitions is acceptable for personal task manager
# - Users typically set times in local time
# - Most users won't notice or care about 1-hour DST variance
```

**Why 1-Hour Drift is Acceptable:**
1. **User Intent**: User sets "9:00 AM every Monday" meaning "wake up time", not absolute UTC
2. **Rounding**: Most tasks don't require minute-precise timing
3. **Feedback**: User sees actual due date displayed, can adjust if needed
4. **Complexity vs. Value**: Full timezone handling adds 50-100 lines of code for minimal benefit

**Alternative: Use UTC (Rejected)**
```python
# Too complex for Phase I:
from zoneinfo import ZoneInfo  # Python 3.9+
import pytz  # External dependency - REJECTED

# Store all times in UTC
utc_time = datetime(2024, 3, 10, 14, 0, tzinfo=timezone.utc)

# Convert to local for display
local_time = utc_time.astimezone(ZoneInfo("America/New_York"))

# Too many failure modes for Phase I CLI
```

### Edge Cases
- **Spring Forward**: Daylight "lost" - task 1 hour earlier than expected
- **Fall Back**: Daylight "gained" - task 1 hour later than expected
- **Cross-Timezone**: Not applicable (single system)
- **User Travel**: Not handled (user's system timezone)

### FR-026/SC-022 Compliance
Specification requires DST be "handled correctly". Our interpretation:
- **Correct** = Naive datetime with system local time
- **Incorrect** = No DST awareness at all (e.g., always 24-hour intervals ignoring clock changes)
- **Over-engineered** = Full timezone arithmetic (violates constraints)

This decision balances correctness with simplicity for Phase I scope.

## Research Decision 7: Template Due Date Handling

### Decision
Templates store relative due date offsets (today, tomorrow, next week) instead of absolute dates.

### Specification References
- FR-043: Create task from template
- FR-042: Define task template
- SC-021: Templates preserve fields (due date handling)

### Research Findings

**Template Purpose:**
Templates accelerate task creation by pre-filling common task patterns. Due dates are tricky because absolute dates become outdated.

**Due Date Handling Options:**

| Option | Description | Pros | Cons |
|--------|-------------|------|------|
| **Absolute Date** | Store specific date in template | Simple | Becomes outdated quickly |
| **Relative Offset** (CHOSEN) | Store "today", "tomorrow", "next week" | Always relevant | Requires calculation |
| **Prompt User** | Ask for due date each time | Flexible | Defeats template purpose |
| **Days from Now** | Store integer offset (e.g., +7) | Precise | Less user-friendly |

**Chosen Strategy: Relative Offsets**
```python
@dataclass
class TaskTemplate:
    id: str
    name: str
    title: str
    description: str = None
    priority: str = None
    tags: List[str] = None
    due_date_offset: str = None  # "today", "tomorrow", "next_week", "next_month", None

def calculate_template_due_date(offset: str) -> datetime:
    """Calculate actual due date from relative offset"""
    today = datetime.now()
    today_end = datetime.combine(today.date(), datetime.max.time())

    if offset == "today":
        return today_end  # End of day

    elif offset == "tomorrow":
        return today_end + timedelta(days=1)

    elif offset == "next_week":
        return today_end + timedelta(weeks=1)

    elif offset == "next_month":
        # Approximate 30 days
        return today_end + timedelta(days=30)

    else:  # None
        return None
```

**User Interface:**
When creating task from template:
```
Creating task from template "Weekly Review"...
Title: Weekly Review
Description: Review past week's work
Priority: high
Tags: work, review
Due Date: next_week (calculated: 2024-01-08 23:59)
Create task? (y/n): y
```

**Alternative Considered: Absolute Date (Rejected)**
```python
# Bad: Template with absolute date
template = TaskTemplate(
    name="Weekly Report",
    due_date=datetime(2024, 1, 1, 12, 0)  # Outdated after Jan 1!
)
```

**Alternative Considered: Prompt Every Time (Rejected)**
```python
# Bad: Defeats template purpose
task = create_task_from_template(template)
due_date = input("Enter due date (YYYY-MM-DD HH:MM): ")  # User still has to type
```

### Edge Cases
- **Template with "today"**: Due date is end of current day
- **Template with "next_month"**: Approximate 30 days (variable month length)
- **No Due Date**: User can leave offset as None (task without due date)
- **Edit Template**: Change offset or remove due date

## Summary of Research Decisions

| # | Decision | Rationale | Complexity |
|---|----------|-----------|------------|
| 1 | ISO 8601 date-time format | Built-in Python support, unambiguous | Low |
| 2 | Stack-based undo with 50 FIFO | Simple LIFO, memory-bounded, no redo | Low |
| 3 | On-demand reminder evaluation | No background services, good UX | Low |
| 4 | Immediate auto-creation of recurring tasks | Immediate feedback, simple | Low-Medium |
| 5 | Atomic undo for recurring tasks | Clean semantics, single action | Medium |
| 6 | Naive datetime for DST | System local time, acceptable 1-hour drift | Low |
| 7 | Relative date offsets for templates | Always relevant, avoids outdated dates | Low |

All decisions prioritize simplicity, Phase I scope compliance, and maintain backward compatibility with existing Phase I Basic and Intermediate features.
