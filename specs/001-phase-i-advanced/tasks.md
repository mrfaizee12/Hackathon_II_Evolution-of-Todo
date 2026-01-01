---
description: "Task list template for Phase I Advanced implementation"
---

# Tasks: Phase I Advanced - Task Deadline and Organization Features

**Input**: Design documents from `/specs/001-phase-i-advanced/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md

**Tests**: The examples below include test tasks. Integration tests are included to verify user story independence.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3, US4, US5)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- Paths shown below assume single project structure per plan.md

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure for Advanced features

- [ ] T001 [P] [Setup] Create new model files in src/models/ (template.py, history.py)
- [ ] T002 [P] [Setup] Create new service files in src/services/ (template_service.py, history_service.py)
- [ ] T003 [P] [Setup] Extend src/models/enums.py with ActionType enum

---

## Phase 2: Foundation (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T004 [P] [Foundation] Extend Task model with due_date field in src/models/task.py
- [ ] T005 [P] [Foundation] Create ActionType enum in src/models/enums.py
- [ ] T006 [P] [Foundation] Create TaskTemplate model in src/models/template.py
- [ ] T007 [P] [Foundation] Create HistoryEntry model in src/models/history.py
- [ ] T008 [P] [Foundation] Create TaskStatistics data transfer object in src/models/template.py
- [ ] T009 [P] [Foundation] Extend src/utils/validators.py with date validation functions
- [ ] T010 [P] [Foundation] Extend src/utils/validators.py with template validation functions
- [ ] T011 [P] [Foundation] Update src/cli/__init__.py to export new models and services

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Task Due Date Management (Priority: P1) 🎯 MVP

**Goal**: Enable users to set, update, and clear due dates on tasks with validation (today or future dates only, ISO format YYYY-MM-DD)

**Independent Test**: Create tasks with various due dates, verify they display correctly, validation rejects past dates, and clearing due dates works. Existing tasks without due dates function unchanged.

### Tests for User Story 1 ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T012 [P] [US1] Unit test for Task model due_date field validation in tests/test_task_model.py
- [ ] T013 [P] [US1] Unit test for date validation (valid formats, invalid formats, past dates) in tests/test_date_validation.py
- [ ] T014 [P] [US1] Integration test for due date creation workflow in tests/integration_test_due_dates.py

### Implementation for User Story 1

- [ ] T015 [P] [US1] Add set_due_date method to TaskService in src/services/task_service.py
- [ ] T016 [P] [US1] Add clear_due_date method to TaskService in src/services/task_service.py
- [ ] T017 [P] [US1] Extend Task.__post_init__ with due_date validation (FR-002) in src/models/task.py
- [ ] T018 [P] [US1] Add get_due_date_input function to src/cli/input_handler.py
- [ ] T019 [P] [US1] Add set_due_date menu handler in src/cli/menu.py
- [ ] T020 [P] [US1] Update format_task_list to display due dates in src/cli/output_formatter.py
- [ ] T021 [P] [US1] Update format_single_task to display due date in src/cli/output_formatter.py
- [ ] T022 [P] [US1] Update display_menu to show option 12 (Set/Update Due Date) in src/cli/menu.py
- [ ] T023 [P] [US1] Add menu handler routing for option 12 in src/main.py
- [ ] T024 [P] [US1] Add error handling for invalid date formats in src/cli/menu.py
- [ ] T025 [P] [US1] Add error handling for past due dates in src/cli/menu.py

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Task Progress Tracking and Statistics (Priority: P2)

**Goal**: Provide summary statistics (total, completed, incomplete, completion %, priority distribution, tag distribution, due date categories) calculated on-demand

**Independent Test**: Create tasks with various states, view statistics, verify all counts and calculations are accurate. Empty task list shows all zeros with appropriate message.

### Tests for User Story 2 ⚠️

- [ ] T026 [P] [US2] Unit test for TaskStatistics calculation in tests/test_statistics.py
- [ ] T027 [P] [US2] Unit test for statistics edge cases (empty list, division by zero) in tests/test_statistics.py
- [ ] T028 [P] [US2] Integration test for statistics workflow in tests/integration_test_statistics.py

### Implementation for User Story 2

- [ ] T029 [P] [US2] Add get_statistics method to TaskService in src/services/task_service.py
- [ ] T030 [P] [US2] Implement total_tasks calculation in TaskService.get_statistics
- [ ] T031 [P] [US2] Implement completed_tasks/incomplete_tasks calculation in TaskService.get_statistics
- [ ] T032 [P] [US2] Implement completion_percentage calculation with division by zero handling in TaskService.get_statistics
- [ ] T033 [P] [US2] Implement priority_distribution calculation using Counter in TaskService.get_statistics
- [ ] T034 [P] [US2] Implement tag_distribution calculation using Counter in TaskService.get_statistics
- [ ] T035 [P] [US2] Implement overdue_count calculation in TaskService.get_statistics
- [ ] T036 [P] [US2] Implement due_today_count and due_this_week_count calculation in TaskService.get_statistics
- [ ] T037 [P] [US2] Add format_statistics function to src/cli/output_formatter.py
- [ ] T038 [P] [US2] Add view_statistics menu handler in src/cli/menu.py
- [ ] T039 [P] [US2] Update display_menu to show option 13 (View Statistics) in src/cli/menu.py
- [ ] T040 [P] [US2] Add menu handler routing for option 13 in src/main.py

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Bulk Task Operations (Priority: P2)

**Goal**: Enable bulk operations (mark complete/incomplete, delete, update priority) for multiple tasks via range-based selection with confirmation

**Independent Test**: Create multiple tasks, perform bulk operations on ranges, verify all affected tasks are updated. Confirmation prevents accidental changes.

### Tests for User Story 3 ⚠️

- [ ] T041 [P] [US3] Unit test for bulk_update_status in tests/test_bulk_operations.py
- [ ] T042 [P] [US3] Unit test for bulk_delete in tests/test_bulk_operations.py
- [ ] T043 [P] [US3] Unit test for bulk_update_priority in tests/test_bulk_operations.py
- [ ] T044 [P] [US3] Unit test for range validation (invalid ranges, missing IDs) in tests/test_bulk_operations.py
- [ ] T045 [P] [US3] Integration test for bulk operations workflow in tests/integration_test_bulk_ops.py

### Implementation for User Story 3

- [ ] T046 [P] [US3] Add get_task_range function to src/cli/input_handler.py
- [ ] T047 [P] [US3] Add bulk_update_status method to TaskService in src/services/task_service.py
- [ ] T048 [P] [US3] Add bulk_delete method to TaskService in src/services/task_service.py
- [ ] T049 [P] [US3] Add bulk_update_priority method to TaskService in src/services/task_service.py
- [ ] T050 [P] [US3] Add get_bulk_confirmation function to src/cli/input_handler.py
- [ ] T051 [P] [US3] Add bulk_operations menu handler in src/cli/menu.py
- [ ] T052 [P] [US3] Add mark_bulk_complete handler in src/cli/menu.py
- [ ] T053 [P] [US3] Add mark_bulk_incomplete handler in src/cli/menu.py
- [ ] T054 [P] [US3] Add bulk_delete_handler in src/cli/menu.py
- [ ] T055 [P] [US3] Add bulk_update_priority_handler in src/cli/menu.py
- [ ] T056 [P] [US3] Update display_menu to show option 14 (Bulk Operations) in src/cli/menu.py
- [ ] T057 [P] [US3] Add menu handler routing for option 14 in src/main.py
- [ ] T058 [P] [US3] Add error handling for zero task selection in src/cli/menu.py
- [ ] T059 [P] [US3] Add error handling for invalid ranges in src/cli/menu.py

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: User Story 4 - Task Templates (Priority: P3)

**Goal**: Enable template CRUD (create, list, delete, use) with 10 template limit. Templates store absolute due dates (not relative offsets).

**Independent Test**: Create templates with various configurations, use templates to create tasks, verify all values applied. User can override fields during creation. Template limit enforced (max 10).

### Tests for User Story 4 ⚠️

- [ ] T060 [P] [US4] Unit test for TaskTemplate model validation in tests/test_template_model.py
- [ ] T061 [P] [US4] Unit test for template service CRUD operations in tests/test_template_service.py
- [ ] T062 [P] [US4] Unit test for 10 template limit enforcement in tests/test_template_service.py
- [ ] T063 [P] [US4] Integration test for template workflow in tests/integration_test_templates.py

### Implementation for User Story 4

- [ ] T064 [P] [US4] Implement TaskTemplate dataclass in src/models/template.py
- [ ] T065 [P] [US4] Implement TaskService in src/services/template_service.py
- [ ] T066 [P] [US4] Add create_template method with limit check to TemplateService
- [ ] T067 [P] [US4] Add list_templates method to TemplateService
- [ ] T068 [P] [US4] Add delete_template method to TemplateService
- [ ] T069 [P] [US4] Add use_template method to TemplateService
- [ ] T070 [P] [US4] Add get_template_input function to src/cli/input_handler.py
- [ ] T071 [P] [US4] Add manage_templates menu handler in src/cli/menu.py
- [ ] T072 [P] [US4] Add create_template_handler in src/cli/menu.py
- [ ] T073 [P] [US4] Add list_templates_handler in src/cli/menu.py
- [ ] T074 [P] [US4] Add delete_template_handler in src/cli/menu.py
- [ ] T075 [P] [US4] Add use_template_handler in src/cli/menu.py
- [ ] T076 [P] [US4] Update display_menu to show option 15 (Manage Templates) in src/cli/menu.py
- [ ] T077 [P] [US4] Add menu handler routing for option 15 in src/main.py
- [ ] T078 [P] [US4] Add error handling for empty template title/name in src/cli/menu.py
- [ ] T079 [P] [US4] Add error handling for 10 template limit in src/cli/menu.py

**Checkpoint**: All user stories should now be independently functional

---

## Phase 7: User Story 5 - Command History and Undo (Priority: P3)

**Goal**: Maintain undo history (create, update, delete, toggle_status, bulk operations) with 50 entry FIFO limit. Undo reverses most recent action.

**Independent Test**: Perform various actions, verify history records them correctly, undo reverses actions (delete restores task, update restores previous values, create deletes task).

### Tests for User Story 5 ⚠️

- [ ] T080 [P] [US5] Unit test for HistoryEntry model in tests/test_history_model.py
- [ ] T081 [P] [US5] Unit test for HistoryService record_action in tests/test_history_service.py
- [ ] T082 [P] [US5] Unit test for HistoryService undo (create, update, delete, toggle) in tests/test_history_service.py
- [ ] T083 [P] [US5] Unit test for 50 entry FIFO limit in tests/test_history_service.py
- [ ] T084 [P] [US5] Integration test for undo workflow in tests/integration_test_undo.py

### Implementation for User Story 5

- [ ] T085 [P] [US5] Implement HistoryEntry dataclass in src/models/history.py
- [ ] T086 [P] [US5] Implement HistoryService in src/services/history_service.py
- [ ] T087 [P] [US5] Add record_action method with FIFO enforcement to HistoryService
- [ ] T088 [P] [US5] Add undo method to HistoryService
- [ ] T089 [P] [US5] Add has_undo method to HistoryService
- [ ] T090 [P] [US5] Integrate HistoryService with TaskService for action tracking
- [ ] T091 [P] [US5] Add undo_handler to src/cli/menu.py
- [ ] T092 [P] [US5] Update display_menu to show option 16 (Undo Last Action) in src/cli/menu.py
- [ ] T093 [P] [US5] Add menu handler routing for option 16 in src/main.py
- [ ] T094 [P] [US5] Add error handling for no undo history in src/cli/menu.py

**Checkpoint**: All user stories should now be independently functional

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T095 [P] [Polish] Update quickstart.md with Advanced feature examples
- [ ] T096 [P] [Polish] Add integration test for backward compatibility in tests/integration_test_backward_compat.py
- [ ] T097 [P] [Polish] Verify all existing Phase I Basic/Intermediate menu options work unchanged
- [ ] T098 [P] [Polish] Verify due date validation performance <100ms per SC-017
- [ ] T099 [P] [Polish] Verify statistics calculation performance <500ms per SC-018
- [ ] T100 [P] [Polish] Verify bulk operations performance <1000ms per SC-019
- [ ] T101 [P] [Polish] Verify undo operations performance <200ms per SC-020
- [ ] T102 [P] [Polish] Run all unit tests with python -m unittest discover tests
- [ ] T103 [P] [Polish] Run all integration tests with python -m unittest discover tests/integration
- [ ] T104 [P] [Polish] Fix any failing tests or warnings

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundation (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-7)**: All depend on Foundation phase completion
  - User stories can proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Phase 8)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundation (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundation (Phase 2) - No dependencies on other stories
- **User Story 3 (P2)**: Can start after Foundation (Phase 2) - No dependencies on other stories
- **User Story 4 (P3)**: Can start after Foundation (Phase 2) - No dependencies on other stories
- **User Story 5 (P3)**: Can start after Foundation (Phase 2) - Integrates with TaskService but independently testable

### Within Each User Story

- Tests MUST be written and FAIL before implementation
- Models before services
- Services before menu handlers
- Menu handlers before main.py routing
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundation tasks marked [P] can run in parallel (within Phase 2)
- Once Foundation phase completes, all user stories can start in parallel (if team capacity allows)
- All tests for a user story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundation (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1 (Due Dates)
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundation → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Add User Story 4 → Test independently → Deploy/Demo
6. Add User Story 5 → Test independently → Deploy/Demo
7. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundation together
2. Once Foundation is done:
   - Developer A: User Story 1 (P1)
   - Developer B: User Story 2 (P2)
   - Developer C: User Story 3 (P2)
3. Once P1-P2-P3 complete:
   - Developer A: User Story 4 (P3)
   - Developer B: User Story 5 (P3)
4. Complete Phase 8: Polish together

---

## Important Notes

**Specification Compliance**: This task list is based on approved specification (spec.md). User input requested recurrence and reminders, but specification explicitly marks these as **out of scope**. Per constitution conflict resolution ("When specifications conflict with user input, specifications win"), this task list implements ONLY approved specification features (Due Dates, Statistics, Bulk Operations, Templates, Undo/History).

**No Recurrence**: Tasks T004 through T008 for Task model do NOT include recurrence field. No recurrence rules, no recurring task logic, no "daily/weekly/custom" intervals. These are explicitly out of scope per specification.

**No Reminders**: No tasks for reminder evaluation, no tasks for overdue detection display, no tasks for upcoming task display. These are explicitly out of scope per specification (no notification APIs, no background services).

**Backward Compatibility**: All new Task fields (due_date) are optional with default values. Existing Phase I Basic and Intermediate functionality must work unchanged.

**Phase I Scope**: All features are in-memory only. No databases, no files, no web APIs, no persistence. All data lost on application exit.

**Tests**: Integration tests included for each user story to verify independence. Backward compatibility test ensures no breaking changes to existing features.

**Performance Goals**: All operations meet performance targets from specification (<100ms due date validation, <500ms statistics, <1000ms bulk ops, <200ms undo).
