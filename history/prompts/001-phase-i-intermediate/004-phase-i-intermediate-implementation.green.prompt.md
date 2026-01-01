---
id: 004
title: Phase I Intermediate Implementation
stage: green
date: 2026-01-01
surface: agent
model: claude-sonnet-4-5-20250929
feature: phase-i-intermediate
branch: 002-phase-ii-todo
user: (continuation from previous session)
command: /sp.implement continue
labels: ["implementation","phase-i-intermediate","cli"]
links:
  spec: history/prompts/001-phase-i-intermediate/001-phase-i-intermediate.spec.prompt.md
  ticket: null
  adr: null
  pr: null
files:
  - src/utils/__init__.py
  - src/utils/validators.py
  - src/models/enums.py
  - src/models/task.py
  - src/services/task_service.py
  - src/cli/input_handler.py
  - src/cli/output_formatter.py
  - src/cli/menu.py
  - src/main.py
tests:
  - Python syntax compilation validation for all modified files
  - Functional test of core service methods (add_task, update_task_priority, update_task_tags, search_tasks, filter_tasks, sort_tasks)
---

## Prompt

Implement the Phase I Intermediate Level features by EXTENDING existing Phase I Basic source code WITHOUT breaking existing functionality. The in-memory console application runs from src/main.py and should gain the following capabilities:

User Story 1 - Priority
- Menu Option 7: Update task priority
- Data model: Priority enum (High/Medium/Low) field added to Task
- Validation: validate_priority() function converts string to Priority enum
- Display: Priority shown in brackets like [High] when viewing tasks
- Defaults: New tasks default to Medium priority

User Story 2 - Tags
- Menu Option 8: Manage task tags (add/remove/replace sub-menu)
- Data model: tags list[str] field added to Task
- Validation: validate_tag() checks length (max 50 chars), validate_tags() checks count (max 10 tags)
- Display: Tags shown as "Tags: work, important" when viewing tasks
- Defaults: New tasks default to empty tags list

User Story 3 - Search
- Menu Option 9: Search tasks by keyword
- Behavior: Case-insensitive search in title OR description (empty keyword returns all tasks)
- UI: Prompt for keyword, show all matching tasks with existing format_task_list
- Service Method: search_tasks(keyword: str) -> list[Task]

User Story 4 - Filter
- Menu Option 10: Filter tasks by status, priority, and/or tag (AND logic)
- Service Method: filter_tasks(status_filter: FilterStatus, priority_filter: Priority, tag_filter: str) -> list[Task]
- UI: Interactive sub-menus for each filter criterion
- Filters:
  - Status: All, Complete, Incomplete
  - Priority: All, High, Medium, Low
  - Tag: Optional, press Enter to skip (show available tags)

User Story 5 - Sort
- Menu Option 11: Sort tasks by title or priority
- Service Method: sort_tasks(tasks: list[Task], sort_by: SortBy) -> list[Task]
- Sort options:
  - Title A-Z (case-insensitive)
  - Title Z-A (case-insensitive)
  - Priority High→Low
  - Priority Low→High
- Behavior: Stable sort, does not modify input list (copy first)

Phase 8 - Polish
- Update display_menu() to show options 7-11 with [NEW] markers
- Update get_menu_choice() validation to accept 1-11 instead of 1-6
- Wire new handlers in main.py menu dispatch table
- Verify all Python files compile without syntax errors
- Ensure backward compatibility with existing options 1-6

Technical Constraints
- Python 3.11+ required for dataclass field(default_factory=list)
- In-memory storage only (no persistence layer)
- Enum-based types for type safety (Priority, SortBy, FilterStatus)
- Validation functions return tuple[bool, str] for (is_valid, error_message)
- All error messages must be user-friendly and actionable
- All new features maintain backward compatibility with Phase I Basic

Implementation Approach
- Extend existing data model (Task dataclass) with new fields using default values
- Create new enums module with Priority, SortBy, FilterStatus
- Create utils module with validators for tag/priority validation
- Extend TaskService with 5 new methods (search, filter, sort, update priority/tags)
- Extend CLI with 5 new menu handlers (options 7-11)
- Update existing output formatter to show priority and tags
- Extend input handlers with get_priority_choice() and get_tags()

Order of Execution (Tasks)
1. Create utils/__init__.py to export validators
2. Implement validate_priority(), validate_tag(), validate_tags() in validators.py
3. Create enums.py with Priority, SortBy, FilterStatus enums
4. Extend Task model with priority: Priority = Priority.MEDIUM and tags: list[str] = field(default_factory=list)
5. Extend TaskService with 5 new methods for priority, tags, search, filter, sort
6. Extend CLI input_handler.py with get_priority_choice() and get_tags()
7. Extend CLI output_formatter.py to display priority and tags in task lists
8. Add 5 new menu handlers in menu.py with [NEW] marker logic
9. Update display_menu() to show options 7-11
10. Update main.py handler dictionary and get_menu_choice validation
11. Verify all code compiles with python -m py_compile
12. Test basic functionality

continue

## Response snapshot

Successfully implemented all Phase I Intermediate features by extending the existing Phase I Basic codebase:

**Created Files:**
- src/utils/__init__.py - Utility module exports
- src/utils/validators.py - Validation functions (validate_priority, validate_tag, validate_tags)
- src/models/enums.py - Enum types (Priority, SortBy, FilterStatus)

**Modified Files:**
- src/models/task.py - Extended with priority and tags fields
- src/services/task_service.py - Added search_tasks, filter_tasks, sort_tasks, update_task_priority, update_task_tags
- src/cli/input_handler.py - Added get_priority_choice(), get_tags_input(), get_tags()
- src/cli/output_formatter.py - Extended format_task_list() to display priority and tags
- src/cli/menu.py - Rewritten with new handlers for options 7-11
- src/main.py - Updated imports and handler dispatch table

**Key Implementation Details:**
- Task dataclass extended with default values maintaining backward compatibility
- Enum-based type safety for Priority (HIGH, MEDIUM, LOW), SortBy, and FilterStatus
- Validation uses tuple[bool, str] pattern for success/error messaging
- In-memory service layer methods use list comprehensions for O(n) search/filter
- Stable sort implementation that copies input list before sorting
- AND logic for combined filters in filter_tasks()
- Menu handlers include proper error handling and user feedback

**Testing:**
- All Python files compiled successfully without syntax errors
- Functional test passed: add_task, update_task_priority, update_task_tags, search_tasks, filter_tasks, sort_tasks

## Outcome

- ✅ Impact: Phase I Intermediate features fully implemented with backward compatibility preserved
- 🧪 Tests: Python syntax compilation validated; functional tests of all service methods passed
- 📁 Files: 9 files created/modified (2 new files, 7 extensions)
- 🔁 Next prompts: None - implementation complete
- 🧠 Reflection: File corruption issue in menu.py encountered due to nested f-string quotes; resolved by extracting error message to separate variable. Import paths corrected from relative (.enums) to absolute (src.models.enums) in task_service.py.

## Evaluation notes (flywheel)

- Failure modes observed: menu.py file corruption due to nested f-string quotes (f\" inside f-string); KeyError in sort_tasks due to dictionary keys being strings but t.priority being enum objects
- Graders run and results (PASS/FAIL): PASS - All files compile; functional tests pass
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A - Implementation complete
