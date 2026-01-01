---
description: "Task list for Phase I Intermediate implementation"
---

# Tasks: 001-phase-i-intermediate

**Input**: Design documents from `/specs/001-phase-i-intermediate/`

**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3, US4, US5)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- **Web app**: `backend/src/`, `frontend/src/`
- **Mobile**: `api/src/`, `ios/src/` or `android/src/`
- Paths shown below assume single project - adjust based on plan.md structure

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 Create utility module directory structure in src/utils/
- [ ] T002 Create validators module in src/utils/validators.py

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T003 [P] Create Priority enum in src/models/enums.py (FR-001)
- [ ] T004 [P] Create SortBy enum in src/models/enums.py (FR-029 to FR-036)
- [ ] T005 [P] Create FilterStatus enum in src/models/enums.py (FR-020)
- [ ] T006 [P] Extend Task model in src/models/task.py with priority field (FR-001, FR-002)
- [ ] T007 [P] Extend Task model in src/models/task.py with tags field (FR-006, FR-011)
- [ ] T008 [P] Extend TaskService add_task method to accept priority and tags parameters (FR-001, FR-006)
- [ ] T009 [P] Add search_tasks method to TaskService in src/services/task_service.py (FR-013 to FR-019)
- [ ] T010 [P] Add filter_tasks method to TaskService in src/services/task_service.py (FR-020 to FR-028)
- [ ] T011 [P] Add sort_tasks method to TaskService in src/services/task_service.py (FR-029 to FR-036)
- [ ] T012 [P] Add update_task_priority method to TaskService in src/services/task_service.py (FR-003)
- [ ] T013 [P] Add update_task_tags method to TaskService in src/services/task_service.py (FR-008, FR-009)

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Task Priority Management (Priority: P1) 🎯 MVP

**Goal**: Enable users to assign and update task priorities (High, Medium, Low)

**Independent Test**: Can create task with priority, update task priority, and verify priority displays in task list

### Tests for User Story 1 (OPTIONAL - only if tests requested) ⚠️

> **NOTE**: Write these tests FIRST, ensure they FAIL before implementation

- [ ] T014 [P] [US1] Contract test for update_task_priority operation in tests/contract/test_cli_operations.py
- [ ] T015 [P] [US1] Integration test for create task with priority flow in tests/integration/test_todo_app_flows.py

### Implementation for User Story 1

- [ ] T016 [P] [US1] Add get_priority_choice input handler in src/cli/input_handler.py
- [ ] T017 [P] [US1] Add validate_priority function in src/utils/validators.py
- [ ] T018 [P] [US1] Add update_task_priority menu handler in src/cli/menu.py (menu option 7)
- [ ] T019 [P] [US1] Extend format_task_list to display priority in src/cli/output_formatter.py
- [ ] T020 [P] [US1] Add logging for update_task_priority operation

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Tag and Category Management (Priority: P2)

**Goal**: Enable users to add and remove tags from tasks for categorization and filtering

**Independent Test**: Can create task with tags, add/remove tags from existing task, and verify tags display in task list

### Tests for User Story 2 (OPTIONAL - only if tests requested) ⚠️

- [ ] T021 [P] [US2] Contract test for manage_task_tags operation in tests/contract/test_cli_operations.py
- [ ] T022 [P] [US2] Integration test for add/remove tags flow in tests/integration/test_todo_app_flows.py

### Implementation for User Story 2

- [ ] T023 [P] [US2] Add get_tags_input input handler in src/cli/input_handler.py
- [ ] T024 [P] [US2] Add validate_tag function in src/utils/validators.py (FR: 50 chars max)
- [ ] T025 [P] [US2] Add validate_tags function in src/utils/validators.py (FR: 10 tags max)
- [ ] T026 [P] [US2] Add manage_task_tags menu handler in src/cli/menu.py (menu option 8)
- [ ] T027 [P] [US2] Extend format_task_list to display tags in src/cli/output_formatter.py
- [ ] T028 [P] [US2] Add logging for manage_task_tags operation

**Checkpoint**: At this point, User Story 2 should be fully functional and testable independently

---

## Phase 5: User Story 3 - Task Search (Priority: P2)

**Goal**: Enable users to search tasks by keyword in title or description

**Independent Test**: Can search for keyword and see matching tasks (title OR description, case-insensitive)

### Tests for User Story 3 (OPTIONAL - only if tests requested) ⚠️

- [ ] T029 [P] [US3] Contract test for search_tasks operation in tests/contract/test_cli_operations.py
- [ ] T030 [P] [US3] Integration test for search flow in tests/integration/test_todo_app_flows.py

### Implementation for User Story 3

- [ ] T031 [P] [US3] Add get_search_keyword input handler in src/cli/input_handler.py
- [ ] T032 [P] [US3] Add search_tasks menu handler in src/cli/menu.py (menu option 9)
- [ ] T033 [P] [US3] Update format_task_list to show "No tasks found" message in src/cli/output_formatter.py
- [ ] T034 [P] [US3] Add logging for search_tasks operation

**Checkpoint**: At this point, User Story 3 should be fully functional and testable independently

---

## Phase 6: User Story 4 - Task Filtering (Priority: P2)

**Goal**: Enable users to filter tasks by status, priority, and tag

**Independent Test**: Can filter by any criteria and see filtered results (AND logic)

### Tests for User Story 4 (OPTIONAL - only if tests requested) ⚠️

- [ ] T035 [P] [US4] Contract test for filter_tasks operation in tests/contract/test_cli_operations.py
- [ ] T036 [P] [US4] Integration test for filter flow in tests/integration/test_todo_app_flows.py

### Implementation for User Story 4

- [ ] T037 [P] [US4] Add get_filter_status input handler in src/cli/input_handler.py
- [ ] T038 [P] [US4] Add get_filter_priority input handler in src/cli/input_handler.py
- [ ] T039 [P] [US4] Add get_filter_tag input handler in src/cli/input_handler.py (shows available tags)
- [ ] T040 [P] [US4] Add filter_tasks menu handler in src/cli/menu.py (menu option 10)
- [ ] T041 [P] [US4] Extend format_task_list to show active filters in src/cli/output_formatter.py
- [ ] T042 [P] [US4] Add logging for filter_tasks operation

**Checkpoint**: At this point, User Story 4 should be fully functional and testable independently

---

## Phase 7: User Story 5 - Task Sorting (Priority: P3)

**Goal**: Enable users to sort tasks by title or priority

**Independent Test**: Can sort tasks by any criteria and see sorted list (stable sort, case-insensitive)

### Tests for User Story 5 (OPTIONAL - only if tests requested) ⚠️

- [ ] T043 [P] [US5] Contract test for sort_tasks operation in tests/contract/test_cli_operations.py
- [ ] T044 [P] [US5] Integration test for sort flow in tests/integration/test_todo_app_flows.py

### Implementation for User Story 5

- [ ] T045 [P] [US5] Add get_sort_choice input handler in src/cli/input_handler.py
- [ ] T046 [P] [US5] Add sort_tasks menu handler in src/cli/menu.py (menu option 11)
- [ ] T047 [P] [US5] Update format_task_list to show sort order in src/cli/output_formatter.py
- [ ] T048 [P] [US5] Add logging for sort_tasks operation

**Checkpoint**: At this point, User Story 5 should be fully functional and testable independently

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Integration and consistency improvements across all user stories

- [ ] T049 [P] Extend display_menu in src/cli/menu.py to show all new menu options (7-11)
- [ ] T050 [P] Update main.py menu loop to handle new menu options (7-11)
- [ ] T051 [P] Extend update_task menu handler to support priority and tags (menu option 3)
- [ ] T052 [P] Extend add_task menu handler to accept priority and tags (menu option 2)
- [ ] T053 [P] Add validation for tag length and count in validators (FR: 50 chars, 10 max)
- [ ] T054 [P] Update output_formatter to display empty results messages consistently
- [ ] T055 [P] Run all existing unit tests to verify backward compatibility (FR-037)
- [ ] T056 [P] Run integration tests for combined search+filter+sort workflow
- [ ] T057 [P] Code cleanup: remove unused imports, fix formatting with Black
- [ ] T058 [P] Performance validation: verify search/filter/sort operations under 500ms for 100 tasks

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-7)**: All depend on Foundational phase completion
- **Polish (Phase 8)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 3 (P2)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 4 (P2)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 5 (P3)**: Can start after Foundational (Phase 2) - No dependencies on other stories

### Within Each User Story

- Tests (if included) MUST be written and FAIL before implementation
- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- All tests for a user story marked [P] can run in parallel
- Models within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together (if tests requested):
Task: "Contract test for update_task_priority operation in tests/contract/test_cli_operations.py"
Task: "Integration test for create task with priority flow in tests/integration/test_todo_app_flows.py"

# Launch all models for User Story 1 together (already done in Foundational phase):
Task: "Create Priority enum in src/models/enums.py"
Task: "Extend Task model in src/models/task.py with priority field"

# Launch implementation tasks (after models):
Task: "Add get_priority_choice input handler in src/cli/input_handler.py"
Task: "Add validate_priority function in src/utils/validators.py"
Task: "Add update_task_priority menu handler in src/cli/menu.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → MVP (Priority Management)
3. Add User Story 2 → Test independently → Additional value (Tags)
4. Add User Story 3 → Test independently → Additional value (Search)
5. Add User Story 4 → Test independently → Additional value (Filter)
6. Add User Story 5 → Test independently → Additional value (Sort)
7. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1 (Priority)
   - Developer B: User Story 2 (Tags)
   - Developer C: User Story 3 (Search)
3. Stories complete and integrate independently
4. Developer A/B/C swap to User Stories 4 and 5 as they complete

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
- **BACKWARD COMPATIBILITY**: All new features are ADDITIVE - do not modify existing Phase I Basic behavior (FR-037)
- **NO NEW DEPENDENCIES**: Use only Python 3.11+ standard library
- **IN-MEMORY ONLY**: No databases, files, or persistence
- **NO FUTURE PHASE LEAKS**: No web, API, authentication, or Phase II+ features
