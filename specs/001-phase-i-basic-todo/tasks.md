# Tasks: Phase I - Basic Todo Console Application

**Input**: Design documents from `/specs/001-phase-i-basic-todo/`
**Prerequisites**: plan.md (complete), spec.md (complete), research.md (complete), data-model.md (complete), contracts/cli-interface.md (complete)

**Tests**: Tests are NOT explicitly requested in the Phase I specification. Test tasks are included for completeness and constitutional compliance (80% coverage requirement) but can be executed after implementation if TDD is not required.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root (Phase I uses this structure)
- All paths are relative to repository root: `G:\hackathon_ii\todo_app\`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic Python structure

- [X] T001 Create project directory structure with src/, tests/, and spec directories
- [X] T002 [P] Create Python package markers (__init__.py) in src/, src/models/, src/services/, src/cli/
- [X] T003 [P] Create Python package markers (__init__.py) in tests/, tests/unit/, tests/integration/
- [X] T004 [P] Create pyproject.toml with project metadata and pytest configuration
- [X] T005 [P] Create .gitignore for Python artifacts (__pycache__, .pytest_cache, *.pyc, .coverage)
- [X] T006 [P] Create README.md with project overview, setup instructions, and usage

**Checkpoint**: Project structure ready - can begin foundational implementation

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core Task model and service foundation that ALL user stories depend on

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T007 Create Task dataclass in src/models/task.py with id, title, description, status attributes per data-model.md
- [X] T008 Add __post_init__ validation to Task model (empty title check, status validation) per FR-009
- [X] T009 Add __str__ and __repr__ methods to Task model for display and debugging
- [X] T010 Create TaskService class skeleton in src/services/task_service.py with __init__ method
- [X] T011 Add _tasks dict[int, Task] and _next_id counter to TaskService.__init__ for in-memory storage

**Checkpoint**: Foundation ready - Task model and TaskService skeleton complete, user story implementation can now begin

---

## Phase 3: User Story 1 - View Task List (Priority: P1) 🎯 MVP

**Goal**: Users can view all their tasks in a clear list format, including empty list handling

**Independent Test**: Launch application, select option 1 (View Tasks), verify empty message or task list displays correctly

**Spec Reference**: spec.md lines 10-23 (User Story 1)
**Plan Reference**: plan.md lines 340-361 (CLI Layer Interface, Control Flow)
**Contract Reference**: contracts/cli-interface.md lines 66-108 (View All Tasks)

### Implementation for User Story 1

- [X] T012 [P] [US1] Implement TaskService.list_tasks() method returning list[Task] in src/services/task_service.py
- [X] T013 [P] [US1] Create output_formatter.py in src/cli/ with format_task_list(tasks) function per contracts/cli-interface.md
- [X] T014 [P] [US1] Implement format_task_list to display "No tasks found" message when list is empty per contract
- [X] T015 [US1] Implement format_task_list to display tasks with format "ID: X | Title: Y | Status: Z\nDescription: W" per contract
- [X] T016 [US1] Create view_tasks() handler function in src/cli/menu.py that calls list_tasks() and format_task_list()

**Checkpoint**: User Story 1 complete - users can view empty or populated task lists

---

## Phase 4: User Story 2 - Add New Task (Priority: P1) 🎯 MVP

**Goal**: Users can add new tasks with title and optional description

**Independent Test**: Launch application, select option 2 (Add Task), enter title and description, verify task created and appears in view

**Spec Reference**: spec.md lines 26-40 (User Story 2)
**Plan Reference**: plan.md lines 262-304 (TaskService.add_task interface)
**Contract Reference**: contracts/cli-interface.md lines 110-171 (Add New Task)

### Implementation for User Story 2

- [X] T017 [P] [US2] Implement TaskService.add_task(title, description="") returning (bool, str, int) in src/services/task_service.py
- [X] T018 [US2] Add ID auto-increment logic to add_task: assign _next_id, create Task, increment counter per research.md
- [X] T019 [US2] Add title validation to add_task: check empty/whitespace, return error tuple if invalid per FR-009
- [X] T020 [P] [US2] Create input_handler.py in src/cli/ with get_task_title() function that prompts and validates
- [X] T021 [P] [US2] Create get_task_description() function in src/cli/input_handler.py that prompts (optional input)
- [X] T022 [US2] Create add_task() handler function in src/cli/menu.py that collects input and calls TaskService.add_task()
- [X] T023 [US2] Add success/error message display to add_task() handler per contracts/cli-interface.md format

**Checkpoint**: User Story 2 complete - users can add tasks with title and optional description, see confirmation

---

## Phase 5: User Story 3 - Mark Task Complete/Incomplete (Priority: P2)

**Goal**: Users can toggle task status between Complete and Incomplete

**Independent Test**: Add a task, mark it complete, verify status changes; mark incomplete, verify status changes back

**Spec Reference**: spec.md lines 43-57 (User Story 3)
**Plan Reference**: plan.md lines 298-304 (TaskService.toggle_status interface)
**Contract Reference**: contracts/cli-interface.md lines 260-332 (Mark Task Complete/Incomplete)

### Implementation for User Story 3

- [X] T024 [P] [US3] Implement TaskService.get_task(task_id) returning Optional[Task] in src/services/task_service.py
- [X] T025 [P] [US3] Implement TaskService.toggle_status(task_id) returning (bool, str) in src/services/task_service.py
- [X] T026 [US3] Add task existence check to toggle_status: return (False, "Task not found") if ID invalid per FR-014
- [X] T027 [US3] Add status flip logic to toggle_status: "Complete" ↔ "Incomplete" per data-model.md state transitions
- [X] T028 [P] [US3] Create get_task_id() function in src/cli/input_handler.py with int validation and positive check
- [X] T029 [P] [US3] Create get_status_choice() function in src/cli/input_handler.py that prompts for 'c' or 'i'
- [X] T030 [US3] Create toggle_status() handler in src/cli/menu.py that gets ID, shows current status, gets choice, calls service
- [X] T031 [US3] Add success/error message display to toggle_status() handler per contracts/cli-interface.md format

**Checkpoint**: User Story 3 complete - users can mark tasks complete/incomplete with visual confirmation

---

## Phase 6: User Story 4 - Update Task Details (Priority: P3)

**Goal**: Users can update task title and/or description

**Independent Test**: Add a task, update its title, verify change; update description, verify change

**Spec Reference**: spec.md lines 60-75 (User Story 4)
**Plan Reference**: plan.md lines 283-289 (TaskService.update_task interface)
**Contract Reference**: contracts/cli-interface.md lines 173-258 (Update Task)

### Implementation for User Story 4

- [X] T032 [P] [US4] Implement TaskService.update_task(task_id, title=None, description=None) returning (bool, str) in src/services/task_service.py
- [X] T033 [US4] Add task existence check to update_task: return (False, "Task not found") if ID invalid per FR-014
- [X] T034 [US4] Add title validation to update_task: if title provided and empty, return (False, "Title cannot be empty") per FR-009
- [X] T035 [US4] Add update logic: modify task.title if title provided, modify task.description if description provided
- [X] T036 [P] [US4] Create get_optional_input(prompt) function in src/cli/input_handler.py that returns None on empty input
- [X] T037 [US4] Create update_task() handler in src/cli/menu.py that gets ID, prompts for new title/description, calls service
- [X] T038 [US4] Add "No changes made" handling if both inputs are None/skipped per contracts/cli-interface.md
- [X] T039 [US4] Add success/error message display to update_task() handler per contracts/cli-interface.md format

**Checkpoint**: User Story 4 complete - users can update task details selectively

---

## Phase 7: User Story 5 - Delete Task (Priority: P3)

**Goal**: Users can delete tasks they no longer need

**Independent Test**: Add a task, delete it, verify it no longer appears in task list

**Spec Reference**: spec.md lines 78-92 (User Story 5)
**Plan Reference**: plan.md lines 290-296 (TaskService.delete_task interface)
**Contract Reference**: contracts/cli-interface.md lines 334-380 (Delete Task)

### Implementation for User Story 5

- [X] T040 [P] [US5] Implement TaskService.delete_task(task_id) returning (bool, str) in src/services/task_service.py
- [X] T041 [US5] Add task existence check to delete_task: return (False, "Task not found") if ID invalid per FR-014
- [X] T042 [US5] Add deletion logic: remove task from _tasks dict using del _tasks[task_id]
- [X] T043 [US5] Create delete_task() handler in src/cli/menu.py that gets ID, calls service, displays result
- [X] T044 [US5] Add success/error message display to delete_task() handler per contracts/cli-interface.md format

**Checkpoint**: User Story 5 complete - users can delete tasks with confirmation

---

## Phase 8: Application Shell & Menu System

**Purpose**: Main menu loop, startup, exit, and menu dispatch - integrates all user stories

**Spec Reference**: spec.md lines 184-244 (CLI Interaction Flow)
**Plan Reference**: plan.md lines 343-361 (Main Application Loop, Control Flow)
**Contract Reference**: contracts/cli-interface.md lines 1-65 (Main Menu), lines 382-406 (Exit)

### Menu System Implementation

- [X] T045 Create display_menu() function in src/cli/menu.py that prints 6-option menu per contracts/cli-interface.md
- [X] T046 Create get_menu_choice() function in src/cli/input_handler.py with int validation and range check (1-6)
- [X] T047 Add error handling to get_menu_choice() for non-numeric input and out-of-range per contracts/cli-interface.md
- [X] T048 Create exit_application() handler in src/cli/menu.py that displays goodbye message and returns True
- [X] T049 Create main() function in src/main.py with welcome message, TaskService initialization, and menu loop
- [X] T050 Add menu dispatch logic to main() using dict mapping choices to handler functions per plan.md
- [X] T051 Add loop continuation logic: display menu, get choice, dispatch handler, repeat until exit
- [X] T052 Add Python version check to main() ensuring Python 3.11+ per quickstart.md troubleshooting

**Checkpoint**: Complete application - all 6 menu options functional, startup and exit flow working

---

## Phase 9: Testing & Quality Assurance

**Purpose**: Unit and integration tests for 80% coverage per constitutional requirement

**Spec Reference**: spec.md lines 163-172 (Definition of Done - all tests passing)
**Plan Reference**: plan.md lines 387-404 (Testing Strategy)

### Unit Tests

- [X] T053 [P] Create test_task_model.py in tests/unit/ testing Task creation, validation, status values
- [X] T054 [P] Add test cases for empty title ValueError in test_task_model.py per FR-009
- [X] T055 [P] Add test cases for invalid status ValueError in test_task_model.py
- [X] T056 [P] Create test_task_service.py in tests/unit/ testing TaskService CRUD operations
- [X] T057 [P] Add test cases for add_task (success, empty title error) in test_task_service.py
- [X] T058 [P] Add test cases for list_tasks (empty list, populated list) in test_task_service.py
- [X] T059 [P] Add test cases for get_task (found, not found) in test_task_service.py
- [X] T060 [P] Add test cases for update_task (success, not found, empty title) in test_task_service.py
- [X] T061 [P] Add test cases for delete_task (success, not found) in test_task_service.py
- [X] T062 [P] Add test cases for toggle_status (complete, incomplete, not found) in test_task_service.py
- [X] T063 [P] Create test_cli_components.py in tests/unit/ testing input validation and output formatting
- [X] T064 [P] Add test cases for get_task_id validation (valid, invalid, non-numeric) in test_cli_components.py
- [X] T065 [P] Add test cases for format_task_list (empty, populated) in test_cli_components.py

### Integration Tests

- [X] T066 Create test_todo_app_flows.py in tests/integration/ for end-to-end user story tests
- [X] T067 [P] Add US1 integration test: view empty list, add tasks, view populated list
- [X] T068 [P] Add US2 integration test: add task with title+description, add with title only, reject empty title
- [X] T069 [P] Add US3 integration test: mark task complete, mark incomplete, invalid ID error
- [X] T070 [P] Add US4 integration test: update title, update description, invalid ID error, empty title error
- [X] T071 [P] Add US5 integration test: delete task, invalid ID error

### Test Execution

- [X] T072 Run pytest with coverage: pytest --cov=src --cov-report=term-missing, verify 80%+ coverage
- [X] T073 Fix any failing tests and coverage gaps identified in T072
- [X] T074 Run manual testing scenarios from quickstart.md (CRUD operations, error handling)

**Checkpoint**: All tests passing, 80%+ coverage achieved, manual validation complete

---

## Phase 10: Documentation & Polish

**Purpose**: Final documentation, code cleanup, and repository polish

**Spec Reference**: spec.md lines 163-172 (Definition of Done)
**Plan Reference**: quickstart.md (complete setup and usage instructions)

### Documentation

- [X] T075 [P] Verify README.md has correct Python version requirement (3.11+) and setup instructions
- [X] T076 [P] Verify pyproject.toml has correct project metadata and pytest dependency
- [X] T077 [P] Add inline docstrings to all public functions and classes following Google style
- [X] T078 [P] Add type hints to all function signatures for better IDE support

### Code Quality

- [X] T079 Run manual code review: check for hardcoded values, magic numbers, unclear variable names
- [X] T080 Verify all error messages match contracts/cli-interface.md exactly
- [X] T081 Verify all menu options and prompts match contracts/cli-interface.md exactly
- [X] T082 Test cross-platform compatibility: run on Windows, Linux, or macOS if available

### Final Validation

- [X] T083 Run complete manual test of all 5 user stories following spec.md acceptance scenarios
- [X] T084 Verify constitutional compliance: no databases, no files, no web frameworks, no future-phase references
- [X] T085 Run pytest one final time, ensure 100% pass rate and 80%+ coverage
- [X] T086 Tag completion: all spec.md acceptance criteria met, all FR requirements implemented

**Checkpoint**: Phase I complete and ready for demo/review

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup (Phase 1) - BLOCKS all user stories
- **User Stories (Phase 3-7)**: All depend on Foundational (Phase 2) completion
  - User Story 1 (P1): Can start after Foundational
  - User Story 2 (P1): Can start after Foundational (independent of US1, but US1+US2 = MVP)
  - User Story 3 (P2): Can start after Foundational (independent of US1/US2)
  - User Story 4 (P3): Can start after Foundational (independent of US1/US2/US3)
  - User Story 5 (P3): Can start after Foundational (independent of US1/US2/US3/US4)
- **Application Shell (Phase 8)**: Depends on at least US1 and US2 for minimal functionality
- **Testing (Phase 9)**: Depends on all implementation phases being complete
- **Documentation (Phase 10)**: Can be done in parallel with testing, depends on implementation

### User Story Dependencies

- **US1 (View)**: Only depends on Foundational - no dependencies on other stories
- **US2 (Add)**: Only depends on Foundational - no dependencies on other stories
- **US3 (Toggle Status)**: Depends on Foundational, logically after Add (need tasks to toggle)
- **US4 (Update)**: Depends on Foundational, logically after Add (need tasks to update)
- **US5 (Delete)**: Depends on Foundational, logically after Add (need tasks to delete)

### Within Each User Story

- Service methods before CLI handlers
- Input validation before service calls
- Error handling integrated with operations
- Output formatting alongside handlers

### Parallel Opportunities

**Phase 1 (Setup)**: All tasks T002-T006 can run in parallel (marked [P])

**Phase 2 (Foundational)**:
- T007-T009 (Task model) can run in parallel with T010-T011 (TaskService skeleton)

**User Story Phases (3-7)**:
- Service implementation [P] tasks can run parallel with CLI helper [P] tasks
- Example US2: T017-T019 (service) parallel with T020-T021 (input helpers)
- Different user stories can be implemented in parallel by different developers

**Phase 9 (Testing)**:
- All unit test files (T053-T065) can be created in parallel (marked [P])
- All integration test files (T067-T071) can be created in parallel (marked [P])

**Phase 10 (Documentation)**:
- All documentation tasks (T075-T078) can run in parallel (marked [P])

---

## Parallel Execution Examples

### Example 1: Foundational Phase (Fast Track)

Launch in parallel:
- Task T007-T009: Create and validate Task model
- Task T010-T011: Create TaskService skeleton

Both groups work on different files (models/task.py vs services/task_service.py), no conflicts.

### Example 2: User Story 2 (Add Task)

Launch in parallel:
- Task T017-T019: Implement TaskService.add_task (services/task_service.py)
- Task T020-T021: Create input helpers (cli/input_handler.py)

Then sequentially:
- Task T022-T023: Create menu handler (needs both service and input helpers)

### Example 3: Multiple User Stories (Team Approach)

After Foundational phase completes:
- Developer A: Implement User Story 1 (T012-T016)
- Developer B: Implement User Story 2 (T017-T023)
- Developer C: Implement User Story 3 (T024-T031)

All work independently on different functionality, can integrate later.

### Example 4: Testing Phase (Maximum Parallelism)

Launch all test file creation tasks simultaneously:
- T053-T065: All unit test files (13 tasks)
- T067-T071: All integration test files (5 tasks)

18 tasks running in parallel, then T072-T074 run sequentially to fix issues.

---

## Implementation Strategy

### MVP First (Minimum Viable Product)

**Goal**: Fastest path to working demo

1. Complete Phase 1: Setup (T001-T006)
2. Complete Phase 2: Foundational (T007-T011)
3. Complete Phase 3: User Story 1 - View Tasks (T012-T016)
4. Complete Phase 4: User Story 2 - Add Tasks (T017-T023)
5. Complete Phase 8: Application Shell (T045-T052) - minimal menu
6. **STOP and VALIDATE**: Test US1+US2 independently
7. Demo: Users can add tasks and view them - basic functionality working

**Estimated Time**: 60-70 tasks for MVP (T001-T023 + T045-T052)

### Incremental Delivery

1. MVP (US1 + US2) → Test → Demo
2. Add US3 (Toggle Status) → Test independently → Deploy/Demo
3. Add US4 (Update) → Test independently → Deploy/Demo
4. Add US5 (Delete) → Test independently → Deploy/Demo
5. Complete testing (Phase 9) → Full test suite passing
6. Polish (Phase 10) → Production-ready

Each increment adds value without breaking previous features.

### Full Implementation (Complete Phase I)

1. Sequential execution: T001 → T002 → ... → T086
2. Total: 86 tasks
3. Estimated effort: 1-2 days for single developer (per plan.md estimate)
4. Includes all user stories, full testing, documentation

---

## Task Summary

| Phase | Purpose | Task Count | Parallel Tasks | Dependencies |
|-------|---------|------------|----------------|--------------|
| Phase 1 | Setup | 6 | 5 (T002-T006) | None |
| Phase 2 | Foundational | 5 | 3 (T007-T009, T010-T011 groups) | Phase 1 |
| Phase 3 | US1 - View Tasks | 5 | 3 (T012-T014) | Phase 2 |
| Phase 4 | US2 - Add Tasks | 7 | 4 (T017/T020-T021 groups) | Phase 2 |
| Phase 5 | US3 - Toggle Status | 8 | 4 (T024-T025, T028-T029 groups) | Phase 2 |
| Phase 6 | US4 - Update Tasks | 8 | 2 (T032, T036) | Phase 2 |
| Phase 7 | US5 - Delete Tasks | 5 | 1 (T040) | Phase 2 |
| Phase 8 | Application Shell | 8 | 0 | US1, US2 (minimum) |
| Phase 9 | Testing | 22 | 18 (T053-T071) | All implementation |
| Phase 10 | Documentation | 12 | 4 (T075-T078) | Phase 9 |

**Total Tasks**: 86
**Total Parallel Opportunities**: 44 tasks can run in parallel with others
**Critical Path**: Phase 1 → Phase 2 → Any User Story → Phase 8 → Phase 9 → Phase 10

**Estimated Effort**:
- MVP (US1+US2+Shell): ~25 tasks, 4-6 hours
- Full Phase I: 86 tasks, 1-2 days for single developer
- With parallelization: Can reduce to ~50% time with 2-3 developers

---

## Notes

- All tasks include explicit file paths for clarity
- Tasks marked [P] can run in parallel (different files, no dependencies)
- Tasks marked [US#] belong to specific user stories for traceability
- Each user story is independently testable after its phase completes
- Foundational phase (Phase 2) MUST complete before any user story work begins
- Application Shell (Phase 8) requires at least US1+US2 for minimal functionality
- Testing phase can begin once implementation is stable (doesn't block other work)
- Follow checklist format strictly: `- [ ] T### [P?] [US#?] Description with file path`
