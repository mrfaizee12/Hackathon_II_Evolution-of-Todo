# Research Document: Phase I Advanced - Task Deadline and Organization Features

**Feature**: 001-phase-i-advanced
**Date**: 2026-01-01
**Purpose**: Document research findings and design decisions for Phase I Advanced implementation

## Decision 1: Date Format and Validation

**Decision**: Use ISO 8601 date format (YYYY-MM-DD) for all user-facing due dates and internal storage.

**Rationale**:
- FR-003 explicitly specifies YYYY-MM-DD format in specification
- Python `datetime.date.fromisoformat()` provides built-in parsing and validation
- Internationally recognized, unambiguous format (no confusion between DD/MM/YYYY and MM/DD/YYYY)
- Lexicographically sortable as strings (e.g., "2026-01-15" < "2026-01-20")
- Date-only validation avoids timezone complexity (per spec constraints: no time-aware features)

**Alternatives considered**:
1. **MM/DD/YYYY** (US format)
   - Rejected: Locale-specific, confusing for international users
   - Example: "01/02/2026" could be January 2nd or February 1st

2. **DD/MM/YYYY** (European format)
   - Rejected: Varies by region, ambiguous
   - Same ambiguity problem as MM/DD/YYYY

3. **Natural language parsing** ("tomorrow", "next week", "in 3 days")
   - Rejected: Out of scope per specification (no recurrence, no reminders)
   - Would add significant complexity for limited value in Phase I CLI

**Implementation approach**:
- User input: Accept YYYY-MM-DD string, validate with `datetime.date.fromisoformat()`
- Storage: Store as `datetime.date` object or ISO string
- Display: Format with `.strftime("%Y-%m-%d")` or direct string representation
- Validation: Reject past dates, validate calendar correctness (leap years, month lengths)
- Error messages: Clear, actionable feedback explaining expected format

**Examples**:
- Valid: "2026-01-15", "2026-12-31", "2024-02-29" (leap year)
- Invalid: "01/15/2026", "15-01-2026", "2026-02-29" (2026 not leap year)
- Past: "2025-12-31" (rejected with "Due date must be today or future")

## Decision 2: Undo History Implementation Pattern

**Decision**: Use stack-based undo history with maximum 50 entries (FIFO when limit exceeded).

**Rationale**:
- Simple, predictable behavior: undo reverses most recent action first (LIFO stack)
- Memory-bounded with FIFO prevents uncontrolled growth (50 entry limit per spec constraints)
- FR-041 requires clearing redo history on new actions (standard undo pattern)
- No redo needed beyond basic undo (explicitly out of scope per spec)
- Each history entry stores: action type, task IDs affected, previous state snapshot

**Alternatives considered**:
1. **Full Command Pattern with Redo Capability**
   - Rejected: Redo is explicitly out of scope (spec section "Out of Scope")
   - Would add significant complexity for limited value in Phase I CLI

2. **Memento Pattern with Deep Copy**
   - Rejected: Overkill for in-memory data structures
   - Deep copying adds performance overhead for simple CLI application
   - Shallow copy sufficient for immutable dataclasses

3. **Persistent Undo History**
   - Rejected: Violates Phase I in-memory constraint (no databases or files)
   - History lost on application exit is acceptable (per spec assumptions)

**Implementation approach**:
- Data structure: Python list as stack (append to push, pop to undo)
- History entry: `HistoryEntry` dataclass with action_type, task_ids, previous_state, timestamp
- Limit enforcement: When `len(history) > 50`, pop oldest entry (index 0)
- Undo logic: Pop most recent entry, restore state, add to history as "undo" action (optional, or just pop)
- Bulk operations: Single history entry covering all affected tasks (atomic undo)

**Example flow**:
```
1. Create task #1
   → History: [(create, [1], {...state...})]

2. Delete task #1
   → History: [(create, [1], {...}), (delete, [1], {...state...})]

3. Undo (reverses delete)
   → Pop last entry (delete, [1], {...})
   → Restore task #1
   → History: [(create, [1], {...})]

4. Create task #2
   → History: [(create, [1], {...}), (create, [2], {...})]
   → Clear any "redo" history (if implemented)
```

**Memory estimation**:
- Assume average history entry: ~1KB (action type + task IDs + task snapshot)
- 50 entries: ~50KB total
- Negligible for Phase I CLI (<100 tasks typical)

## Decision 3: Bulk Task Selection Approach

**Decision**: Range-based selection (start ID, end ID) for bulk operations in CLI environment.

**Rationale**:
- CLI lacks mouse selection or checkbox-style multi-select capabilities
- Range selection provides clear, unambiguous user interface (e.g., "Select tasks 1-5")
- Efficient for contiguous selections (most common use case: "mark all old tasks complete")
- Can be extended with individual ID selection if needed in future phases
- FR-022 requires confirmation before execution (prevents accidental bulk changes)

**Alternatives considered**:
1. **Checkbox-style Multi-select**
   - Rejected: Not feasible in CLI environment
   - Would require complex UI state management for limited benefit

2. **Tag-based Selection**
   - Rejected: Already covered by existing filtering (FR-022, FR-027 in Phase I Intermediate)
   - Users can filter by tag, then apply bulk operation to all filtered results
   - Separate bulk selection mechanism needed for non-tag-based operations

3. **Individual Task ID Selection with Loop**
   - Rejected: Inefficient for bulk operations (tedious user experience)
   - Example: "Enter task ID to add: 1 [Enter] Enter task ID to add: 2 [Enter]..." - poor UX

**Implementation approach**:
- User input: Prompt for start ID and end ID (e.g., "Select tasks from ID: 1 to ID: 5")
- Validation: Validate both IDs exist and start ≤ end
- Range expansion: Generate list of all task IDs in range [start, end]
- Confirmation: Display count and affected task IDs, require "y/n" confirmation (FR-022)
- Error handling: Clear error messages for invalid ranges, non-existent IDs

**Example flow**:
```
User: Selects option 14 (Bulk Operations)
System: "Bulk task operations: 1. Mark complete, 2. Mark incomplete, 3. Delete, 4. Update priority"
User: Chooses 1 (Mark complete)
System: "Enter start task ID: 1"
User: "1"
System: "Enter end task ID: 5"
User: "5"
System: "Selected 5 tasks: [1, 2, 3, 4, 5]. Mark complete? (y/n)"
User: "y"
System: Execute bulk operation, show summary message
```

**Edge cases handled**:
- Single task range (start == end): Treated as single task operation
- Non-contiguous selection: Not supported in Phase I (future enhancement)
- Invalid range (start > end): Error message, prompt re-entry
- Missing IDs in range: Only affect existing IDs (no error, but show affected count)

## Decision 4: Template Due Date Handling

**Decision**: Templates store absolute due dates, not relative offsets.

**Rationale**:
- Resolves spec ambiguity (edge case Q: "What happens when user creates template from task with due date, then uses template tomorrow?")
- Absolute dates are simpler and more predictable: template with "2026-01-15" always creates task with that due date
- User can override due date during task creation (FR-030 allows field overrides)
- Relative offsets would require time-awareness and are out of scope (no recurrence per spec)
- Aligns with other template fields (title, description, priority, tags) which are absolute values

**Alternatives considered**:
1. **Relative Offset (+7 days, +1 month)**
   - Rejected: Adds complexity (requires tracking when template was used)
   - Potential confusion: Does +7 days mean "7 days from now" or "7 days from template creation"?
   - Out of scope: No recurrence features (relative offsets more useful with recurrence)
   - Time-awareness required (calculating "next week" depends on current date)

2. **Hybrid Approach (Prompt user for due date during template-based creation)**
   - Rejected: Inconsistent user experience
   - Templates should reduce data entry, not require additional input
   - Confusing: Template has due date, but user must enter it again?

**Implementation approach**:
- Template storage: `due_date` as optional `datetime.date` or ISO string (same as Task)
- Task creation from template: Copy `due_date` value from template to new task
- Override: Allow user to change due date during creation (same as other fields)
- No offset: Absolute date used as-is, no calculation

**Example flow**:
```
Template created:
- Name: "Weekly Report"
- Title: "Complete weekly report"
- Due date: "2026-01-15"

User creates task from template:
System: "Using template: Weekly Report"
        Title: Complete weekly report
        Due date: 2026-01-15
        Override due date? (Enter new date or press Enter to keep): [User presses Enter]
Result: Task created with due date 2026-01-15

User creates task from template next day:
System: "Using template: Weekly Report"
        Title: Complete weekly report
        Due date: 2026-01-15
        Override due date? (Enter new date or press Enter to keep): [User enters "2026-01-22"]
Result: Task created with due date 2026-01-22 (override)
```

## Decision 5: Statistics Calculation Strategy

**Decision**: Calculate statistics on-demand when user views them, not maintain cached statistics.

**Rationale**:
- In-memory data structures make on-demand calculation fast (<500ms per SC-018)
- No stale statistics: Always reflects current state (no cache invalidation complexity)
- Simpler implementation: No cache layer, no invalidation logic, no state synchronization
- Task count is low (<100 typical), so calculation overhead is negligible
- Aligns with existing Phase I Intermediate approach (search/filter calculated on-demand)

**Alternatives considered**:
1. **Event-driven Statistics (Update on every task change)**
   - Rejected: Adds complexity (every service method must update statistics)
   - Overkill for Phase I scale (<100 tasks, <500ms calculation time)
   - Risk of inconsistent state (if statistics update fails, task update may still succeed)

2. **Lazy Calculation with Simple Caching**
   - Rejected: Caching overhead > calculation overhead for small datasets
   - Cache invalidation complexity (when do we invalidate? On every task change?)
   - Not worth complexity for Phase I CLI scale

**Implementation approach**:
- Trigger: User selects "View task statistics" menu option
- Calculation: Iterate through all tasks, aggregate counts
- Storage: No persistence, calculate fresh each time
- Performance: Use list comprehensions and Counter for efficient aggregation
- Categories: Total, completed, incomplete, priority distribution, tag distribution, due date categories

**Example calculation pseudocode**:
```python
def calculate_statistics(tasks: list[Task]) -> TaskStatistics:
    total = len(tasks)
    completed = sum(1 for t in tasks if t.status == "Complete")
    incomplete = total - completed
    completion_pct = (completed / total * 100) if total > 0 else 0

    priority_counts = Counter(t.priority for t in tasks)
    tag_counts = Counter(tag for t in tasks for tag in t.tags)

    today = date.today()
    overdue = sum(1 for t in tasks if t.due_date and t.due_date < today)
    due_today = sum(1 for t in tasks if t.due_date == today)
    due_this_week = sum(1 for t in tasks if t.due_date and today < t.due_date <= today + timedelta(days=7))

    return TaskStatistics(
        total_tasks=total,
        completed_tasks=completed,
        incomplete_tasks=incomplete,
        completion_percentage=completion_pct,
        priority_distribution=priority_counts,
        tag_distribution=tag_counts,
        overdue_count=overdue,
        due_today_count=due_today,
        due_this_week_count=due_this_week
    )
```

**Performance analysis**:
- Iteration: O(n) where n = task count (typically <100)
- List comprehensions: Efficient Python construct, optimized C implementation
- Counter: O(k) where k = number of unique priorities/tags (small constant)
- Expected time: <500ms for n=100 (well within SC-018 goal)

## Additional Considerations

### Backward Compatibility Strategy

All new features are additive extensions to existing Phase I Basic and Intermediate:

1. **Task Model Extension**:
   - New field: `due_date: Optional[date] = None` (default None for existing tasks)
   - No breaking changes to existing Task API
   - Existing Task instances work without modification

2. **Service Extensions**:
   - New methods added to TaskService (e.g., `set_due_date`, `get_statistics`)
   - Existing methods unchanged (e.g., `add_task`, `delete_task`)
   - No modification to method signatures

3. **CLI Extensions**:
   - New menu options (12-16) added without removing options 1-11
   - Existing menu handlers unchanged
   - Menu flow preserved: User can ignore new features

4. **Testing Strategy**:
   - Dedicated backward compatibility integration tests
   - Tests verify Phase I Basic and Intermediate workflows function identically

### In-Memory Constraints Compliance

Strict adherence to Phase I scope (no persistence, no databases, no files):

1. **No Database Layer**:
   - TaskService uses `dict[int, Task]` for storage (existing pattern)
   - TemplateService uses `dict[int, TaskTemplate]` for storage
   - HistoryService uses `list[HistoryEntry]` for storage

2. **No File I/O**:
   - No `open()`, `read()`, `write()` calls for persistence
   - All data lives in service instance memory
   - Data lost on application exit (explicitly acceptable per spec assumptions)

3. **No Background Services**:
   - No threads, asyncio, or background tasks
   - Reminder evaluation runs synchronously in main menu loop
   - No scheduled jobs or periodic timers

### Error Handling Strategy

1. **Date Validation Errors**:
   - Invalid format: Clear message with expected format ("Use YYYY-MM-DD format")
   - Past date: Clear message ("Due date must be today or future")
   - Leap year: Automatic rejection by datetime.date (built-in validation)

2. **Template Validation Errors**:
   - Empty title: Error ("Template title cannot be empty")
   - Max templates exceeded: Error ("Maximum 10 templates reached")

3. **Bulk Operation Errors**:
   - No selection: Error ("At least one task must be selected")
   - Invalid range: Error ("Invalid range: start ID must be ≤ end ID")
   - Cancelled: No error, just "Operation cancelled" message

4. **Undo Operation Errors**:
   - No history: Message ("No actions available to undo")
   - History limit: Silent (FIFO, no error to user)

## Summary

All research decisions align with:
- Phase I scope (in-memory CLI only)
- Specification requirements (44 functional requirements)
- Constitution principles (clean architecture, spec-driven development)
- Backward compatibility (100% preservation of Basic/Intermediate behavior)

No unclarified needs or constitution violations. Ready for Phase 1 design artifacts.
