# Implementation Plan: Phase I Intermediate - Task Organization Features

**Branch**: `001-phase-i-intermediate` | **Date**: 2026-01-01 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-phase-i-intermediate/spec.md`

**Note**: This template is filled in by `/sp.plan` command. See `.specify/templates/commands/plan.md` for execution workflow.

## Summary

This plan extends the existing Phase I Basic todo application with task priority, tags, search, filter, and sort functionality. The approach maintains backward compatibility by extending the existing in-memory Task model and TaskService with new optional fields (priority, tags) while preserving all existing CRUD operations. All new features are additive extensions that coexist with Basic Level functionality.

**Technical Approach**:
- Extend Task dataclass with `priority` (enum: High/Medium/Low, defaults to Medium) and `tags` (list[str], defaults to empty list)
- Extend TaskService with search, filter, and sort methods that operate on views (not modify underlying storage)
- Add new CLI menu options (7-11) for priority, tags, search, filter, and sort
- Maintain in-memory storage with no persistence (Phase I scope constraint)

## Technical Context

**Language/Version**: Python 3.11+ (matches existing Phase I Basic implementation)
**Primary Dependencies**: dataclasses (built-in), typing (built-in), enum (built-in) - no new external dependencies
**Storage**: In-memory dictionary (existing TaskService._tasks: dict[int, Task]) - no databases or files
**Testing**: pytest (existing test framework), maintain same test structure
**Target Platform**: Console/terminal (existing CLI application)
**Project Type**: Single (Python console application)
**Performance Goals**: Search/filter/sort operations under 500ms for up to 100 tasks (SC-015)
**Constraints**: In-memory only, no persistence, no web/API, no Phase II+ features
**Scale/Scope**: Up to 100 tasks per session, 10 tags per task max, 50 chars per tag max

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Phase Governance
- ✅ **Phase Isolation**: This plan stays within Phase I scope (console app, in-memory, no persistence, no multi-user)
- ✅ **No Future Phase Leaks**: No references to Phase II+ features (web, API, databases, authentication, cloud)
- ✅ **Technology Constraints**: Uses Python 3.11+ (existing), no new technology beyond existing stack

### Spec-Driven Development
- ✅ **Specification Approved**: spec.md exists and is complete
- ✅ **No Code Before Spec**: This plan is created from approved specification
- ✅ **Follow Constitution**: All design decisions align with constitution principles

### Agent Behavior Rules
- ✅ **No Feature Invention**: Plan implements exactly what's specified (priority, tags, search, filter, sort)
- ✅ **No Deviation from Spec**: Plan follows spec requirements FR-001 to FR-039
- ✅ **Clarification Required**: No [NEEDS CLARIFICATION] markers - spec is complete

### Quality Principles
- ✅ **Clean Architecture**: Maintains separation of concerns (models, services, CLI layers)
- ✅ **Stateless Service**: TaskService remains stateless except for in-memory storage (Phase I constraint)
- ✅ **Testing Discipline**: Will extend existing test structure, maintain pytest framework
- ✅ **Security**: No secrets, no external dependencies, input validation in Task.__post_init__

### Technology Constraints
- ✅ **Python 3.11+**: Using existing version, no changes
- ✅ **No New Dependencies**: Extends existing dataclass-based model
- ✅ **In-Memory Only**: No databases, files, or persistence
- ✅ **CLI Interface Only**: Maintains menu-driven console interface
- ✅ **No Web/API**: No REST, no networking, no HTTP

**CONCLUSION**: All gates PASSED. Proceeding to Phase 0 research and Phase 1 design.

## Project Structure

### Documentation (this feature)

```text
specs/001-phase-i-intermediate/
├── plan.md              # This file (/sp.plan command output)
├── spec.md              # Feature specification (already exists)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command - for CLI command contracts)
│   └── cli-operations.yaml  # CLI operation definitions (search, filter, sort)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
src/
├── models/
│   ├── task.py              # Extended with priority and tags
│   ├── enums.py            # NEW: Priority enum (HIGH, MEDIUM, LOW)
│   └── filters.py          # NEW: Filter, Sort, Search models
├── services/
│   └── task_service.py       # Extended with search, filter, sort methods
├── cli/
│   ├── menu.py              # Extended with new menu options 7-11
│   ├── input_handler.py      # Extended with priority, tags, search, filter, sort input functions
│   └── output_formatter.py  # Extended to display priority, tags, filtered/sorted views
├── utils/                  # NEW: Utility functions
│   └── validators.py       # NEW: Priority and tag validators
└── main.py                 # No changes needed (menu loop works with new options)

tests/
├── contract/
│   └── test_cli_operations.py   # NEW: Test CLI operation contracts
├── integration/
│   └── test_todo_app_flows.py    # Extended with new feature flows
└── unit/
    ├── test_task_model.py         # Extended with priority and tags
    ├── test_task_service.py       # Extended with search, filter, sort
    └── test_cli_components.py    # Extended with new input/output
```

**Structure Decision**: Selected single project structure (Option 1) extending existing Phase I Basic layout. No new external dependencies. Maintains existing separation of models, services, and CLI layers. New utility module (src/utils) for validators. New contracts directory in specs for CLI operation definitions.

## Complexity Tracking

> No Constitution Check violations. This section intentionally empty.

---

## Phase 0: Research & Decisions

### Research Tasks

Since all technical decisions are specified in the spec and follow existing Phase I patterns, no research tasks are needed. All aspects use existing Python standard library features (dataclasses, enums, typing) that match the current implementation approach.

**Research Output**: See [research.md](./research.md)

## Phase 1: Design & Contracts

### Data Model Extension

See [data-model.md](./data-model.md) for extended Task entity, Priority enum, Filter/Sort/Search models with validation rules.

### CLI Operation Contracts

See [contracts/cli-operations.yaml](./contracts/cli-operations.yaml) for search, filter, and sort operation definitions.

### Quickstart Guide

See [quickstart.md](./quickstart.md) for development setup and new feature usage examples.

### Agent Context Update

Run `.specify/scripts/powershell/update-agent-context.ps1 -AgentType claude` to add new Priority enum and Filter/Sort/Search models to agent context.

## Implementation Approach

### 1. Data Model Extension (src/models/)

**Task Model Extension** (task.py):
```python
from dataclasses import dataclass, field
from .enums import Priority

@dataclass
class Task:
    id: int
    title: str
    description: str = ""
    status: str = "Incomplete"
    priority: Priority = Priority.MEDIUM  # NEW, defaults to Medium
    tags: list[str] = field(default_factory=list)  # NEW, defaults to empty list
```

**Priority Enum** (enums.py - NEW):
```python
from enum import Enum

class Priority(Enum):
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"

    def __str__(self) -> str:
        return self.value
```

**Filter/Sort Models** (filters.py - NEW):
```python
from enum import Enum
from .enums import Priority

class SortBy(Enum):
    TITLE_ASC = "Title (A-Z)"
    TITLE_DESC = "Title (Z-A)"
    PRIORITY_HIGH_LOW = "Priority (High to Low)"
    PRIORITY_LOW_HIGH = "Priority (Low to High)"

class FilterStatus(Enum):
    ALL = "All"
    COMPLETE = "Complete"
    INCOMPLETE = "Incomplete"
```

### 2. Service Layer Extension (src/services/task_service.py)

**New Methods** (add to existing TaskService):

```python
def search_tasks(self, keyword: str) -> list[Task]:
    """Case-insensitive search in title and description."""
    if not keyword or not keyword.strip():
        return self.list_tasks()

    keyword_lower = keyword.lower().strip()
    return [
        task for task in self.list_tasks()
        if keyword_lower in task.title.lower() or
           keyword_lower in task.description.lower()
    ]

def filter_tasks(self,
              status_filter: FilterStatus = FilterStatus.ALL,
              priority_filter: Priority = None,
              tag_filter: str = None) -> list[Task]:
    """Apply status, priority, and/or tag filters (AND logic)."""
    tasks = self.list_tasks()

    if status_filter != FilterStatus.ALL:
        if status_filter == FilterStatus.COMPLETE:
            tasks = [t for t in tasks if t.status == "Complete"]
        else:
            tasks = [t for t in tasks if t.status == "Incomplete"]

    if priority_filter:
        tasks = [t for t in tasks if t.priority == priority_filter]

    if tag_filter:
        tasks = [t for t in tasks if tag_filter in t.tags]

    return tasks

def sort_tasks(self, tasks: list[Task], sort_by: SortBy) -> list[Task]:
    """Sort task list by title or priority (stable sort)."""
    sorted_tasks = tasks.copy()  # Don't modify input

    if sort_by == SortBy.TITLE_ASC:
        sorted_tasks.sort(key=lambda t: t.title.lower(), reverse=False)
    elif sort_by == SortBy.TITLE_DESC:
        sorted_tasks.sort(key=lambda t: t.title.lower(), reverse=True)
    elif sort_by == SortBy.PRIORITY_HIGH_LOW:
        priority_order = {Priority.HIGH: 0, Priority.MEDIUM: 1, Priority.LOW: 2}
        sorted_tasks.sort(key=lambda t: priority_order[t.priority])
    elif sort_by == SortBy.PRIORITY_LOW_HIGH:
        priority_order = {Priority.HIGH: 2, Priority.MEDIUM: 1, Priority.LOW: 0}
        sorted_tasks.sort(key=lambda t: priority_order[t.priority])

    return sorted_tasks

def update_task_priority(self, task_id: int, priority: Priority) -> tuple[bool, str]:
    """Update task priority."""
    # Similar to existing update_task pattern

def update_task_tags(self, task_id: int, tags: list[str]) -> tuple[bool, str]:
    """Update task tags (replace existing)."""
    # Similar to existing update_task pattern
```

### 3. CLI Layer Extension (src/cli/)

**Menu Options** (menu.py - extend display_menu):
```python
def display_menu() -> None:
    print(f"\n{heading('Main Menu')}")
    print(separator(40))
    print("1. View all tasks")
    print("2. Add a new task")
    print("3. Update a task")
    print("4. Delete a task")
    print("5. Mark task complete/incomplete")
    # NEW OPTIONS 7-11
    print("7. Update task priority")
    print("8. Manage task tags")
    print("9. Search tasks")
    print("10. Filter tasks")
    print("11. Sort tasks")
    print("6. Exit")  # Existing option
    print(separator(40))
```

**New Menu Handlers** (menu.py - add):
```python
def update_task_priority(service: TaskService) -> None:
    """Handler for updating task priority (Menu option 7)."""
    # Get task_id, show current priority, get new priority, update

def manage_task_tags(service: TaskService) -> None:
    """Handler for managing task tags (Menu option 8)."""
    # Get task_id, show current tags, add/remove tags

def search_tasks(service: TaskService) -> None:
    """Handler for searching tasks (Menu option 9)."""
    # Get keyword, call service.search_tasks(), display results

def filter_tasks(service: TaskService) -> None:
    """Handler for filtering tasks (Menu option 10)."""
    # Get filter criteria, call service.filter_tasks(), display results

def sort_tasks(service: TaskService) -> None:
    """Handler for sorting tasks (Menu option 11)."""
    # Get sort criteria, call service.sort_tasks(), display results
```

**Input Handlers** (input_handler.py - add):
```python
def get_priority_choice() -> Priority:
    """Get priority choice from user (High/Medium/Low)."""
    # Prompt user, validate, return Priority enum

def get_tags_input() -> list[str]:
    """Get comma-separated tags from user, return list."""
    # Get input, split by comma, validate max length/count, return list

def get_search_keyword() -> str:
    """Get search keyword from user."""
    # Get input, return string (empty allowed)

def get_filter_status() -> FilterStatus:
    """Get status filter choice from user."""
    # Prompt user, return FilterStatus enum

def get_filter_priority() -> Priority:
    """Get priority filter choice from user."""
    # Prompt user, return Priority enum (None for all)

def get_filter_tag(service: TaskService) -> str:
    """Get tag filter from user, show available tags."""
    # Get all unique tags from tasks, show as menu, return selected tag

def get_sort_choice() -> SortBy:
    """Get sort choice from user."""
    # Show SortBy options as menu, return enum
```

**Output Formatter** (output_formatter.py - extend):
```python
def format_task_list(tasks: list[Task]) -> None:
    """Extended to display priority and tags."""
    if not tasks:
        print(info("No tasks found."))
        return

    print(f"\n{heading('Tasks')}")
    for task in tasks:
        priority_str = f"[{task.priority.value}]" if task.priority else ""
        tags_str = f"Tags: {', '.join(task.tags)}" if task.tags else ""
        print(f"  {task.id}. {task.title} {priority_str}")
        if task.description:
            print(f"      {task.description}")
        if tags_str:
            print(f"      {tags_str}")
        print(f"      Status: {task.status}")
        print(separator(30))
```

### 4. Backward Compatibility Strategy

**Existing Task Handling** (TaskService.__init__):
```python
def __init__(self):
    self._tasks: dict[int, Task] = {}
    self._next_id: int = 1

def migrate_legacy_tasks(self) -> None:
    """Migrate tasks created before priority/tags feature."""
    for task_id, task in self._tasks.items():
        if not hasattr(task, 'priority'):
            task.priority = Priority.MEDIUM
        if not hasattr(task, 'tags'):
            task.tags = []
```

**Update add_task Method**:
```python
def add_task(self, title: str, description: str = "",
            priority: Priority = Priority.MEDIUM,
            tags: list[str] = None) -> tuple[bool, str, int]:
    # Extend to accept priority and tags, default to Medium and empty list
    tags = tags or []
    task = Task(id=task_id, title=title, description=description,
                priority=priority, tags=tags)
```

### 5. Error Handling

**Validation Functions** (src/utils/validators.py - NEW):
```python
def validate_tag(tag: str) -> tuple[bool, str]:
    """Validate tag length and characters."""
    max_length = 50
    if len(tag) > max_length:
        return (False, f"Tag too long (max {max_length} characters)")
    return (True, "")

def validate_tags(tags: list[str]) -> tuple[bool, str]:
    """Validate all tags and max count."""
    max_tags = 10
    if len(tags) > max_tags:
        return (False, f"Too many tags (max {max_tags})")
    for tag in tags:
        valid, msg = validate_tag(tag)
        if not valid:
            return (False, msg)
    return (True, "")

def validate_priority(value: str) -> Priority:
    """Convert string to Priority enum."""
    for priority in Priority:
        if priority.value.lower() == value.lower():
            return priority
    raise ValueError(f"Invalid priority: {value}")
```

**Error Messages** (CLI handlers):
- Invalid priority: "Invalid priority. Please choose High, Medium, or Low."
- Tag too long: "Tag 'exampletagnameistoolong...' exceeds 50 character limit."
- Too many tags: "Cannot add more than 10 tags to a task."
- No search results: "No tasks found matching '{keyword}'."
- No filter results: "No tasks match current filters."

## Testing Strategy

### Unit Tests

**test_task_model.py** (extend):
- Test Task creation with default priority (Medium) and tags (empty list)
- Test Task creation with explicit priority and tags
- Test Task validation for title (existing)
- Test priority enum conversion to string

**test_task_service.py** (extend):
- Test search_tasks() with keyword in title
- Test search_tasks() with keyword in description
- Test search_tasks() case-insensitive
- Test filter_tasks() by status
- Test filter_tasks() by priority
- Test filter_tasks() by tag
- Test filter_tasks() combined (AND logic)
- Test sort_tasks() by title ascending/descending
- Test sort_tasks() by priority high-to-low/low-to-high
- Test sort_tasks() stable sort for identical values
- Test update_task_priority()
- Test update_task_tags()

**test_cli_components.py** (extend):
- Test get_priority_choice() input handling
- Test get_tags_input() parsing comma-separated tags
- Test get_search_keyword() input
- Test validators (validate_tag, validate_tags, validate_priority)

### Integration Tests

**test_todo_app_flows.py** (extend):
- Test complete flow: create task with priority and tags, search, filter, sort
- Test backward compatibility: create task (old format), view (defaults to Medium, empty tags)
- Test combined search+filter+sort workflow
- Test edge cases: empty search, invalid filter, duplicate tags

### Contract Tests

**test_cli_operations.py** (NEW):
- Test search operation contract (FR-013 to FR-019)
- Test filter operation contract (FR-020 to FR-028)
- Test sort operation contract (FR-029 to FR-036)

## Performance Considerations

**Search Operations** (FR-013 to FR-019):
- Linear scan of task list (acceptable for ≤100 tasks)
- Case-insensitive comparison using str.lower() once per task
- O(n) complexity where n = number of tasks

**Filter Operations** (FR-020 to FR-028):
- List comprehension filtering (3 passes max for combined filters)
- O(n) complexity per filter
- Combined filters still O(n) due to Python list comprehension efficiency

**Sort Operations** (FR-029 to FR-036):
- Python Timsort (O(n log n) average case)
- Stable sort preserves insertion order for equal keys
- Priority sort uses dictionary lookup for O(1) priority comparison

**Memory Usage**:
- Task model extension: ~8 bytes per priority, ~56 bytes per empty tags list
- For 100 tasks: ~6.4KB additional memory (negligible)
- Total with existing model: ~10KB for 100 tasks

## Risk Analysis

**Risk 1: Breaking Existing Tests**
- **Impact**: High - may break 10+ existing unit tests
- **Mitigation**: Extend tests incrementally, maintain backward compatibility in Task.__post_init__
- **Fallback**: If test failures >50%, revert and add migration layer

**Risk 2: Priority/Tags Input Complexity**
- **Impact**: Medium - users may find tag entry confusing
- **Mitigation**: Provide clear prompts, show examples, validate input
- **Fallback**: Simplify to single tag per task if usability issues found

**Risk 3: Sort/Filter Performance Degradation**
- **Impact**: Low - only affects >50 tasks scenario
- **Mitigation**: Use list comprehensions, avoid nested loops, measure performance
- **Fallback**: Limit max tasks to 100 if performance >500ms

## Definition of Done

**Plan Phase Complete When**:
- [x] plan.md written with Technical Context, Constitution Check, Project Structure
- [x] research.md generated with all decisions documented
- [x] data-model.md with extended Task entity, Priority enum, Filter/Sort models
- [x] contracts/cli-operations.yaml with CLI operation definitions
- [x] quickstart.md with setup and usage examples
- [x] Agent context updated with Priority enum and Filter/Sort/Search models
- [x] Constitution Check re-evaluated post-design (PASS)
- [x] No [NEEDS CLARIFICATION] markers in any artifact
- [x] All new files created in specs/001-phase-i-intermediate/

**READY FOR**: `/sp.tasks` command to generate task breakdown for implementation
