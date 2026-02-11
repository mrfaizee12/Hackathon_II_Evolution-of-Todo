---

description: "Task list for frontend integration of advanced todo features"
---

# Tasks: Frontend Integration for Advanced Todo Features (Recurring, Due Dates, Reminders)

**Input**: Design documents from `/specs/002-advanced-todo-features/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- **Web app**: `backend/src/`, `frontend/src/`
- **Mobile**: `api/src/`, `ios/src/` or `android/src/`
- Paths shown below assume web app structure - adjust based on plan.md structure

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Create frontend/src/types/advancedTodoTypes.ts for extended task interfaces
- [ ] T002 [P] Install date/time picker library if not already available in project
- [ ] T003 [P] Verify API service structure exists in frontend/src/services/api/

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

Examples of foundational tasks (adjust based on your project):

- [x] T004 Extend Todo interface in frontend/src/services/api.ts with recurrence, dueDate, reminderDateTime, nextOccurrence, reminderAt
- [x] T005 [P] Create RecurrencePattern interface in frontend/src/types/advancedTodoTypes.ts
- [x] T006 [P] Update API service to handle new fields in createTask function
- [x] T007 Update API service to handle new fields in updateTask function
- [x] T008 Create utility functions for determining task metadata (isRecurring, isDueSoon, hasReminder) in frontend/src/utils/taskUtils.ts
- [x] T009 [P] Create validation functions for advanced fields in frontend/src/utils/validation.ts

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Create Recurring/Dated/Reminded Tasks (Priority: P1) 🎯 MVP

**Goal**: Enable users to create tasks with recurrence, due dates, and reminders so that they can manage recurring responsibilities and ensure timely completion of important activities.

**Independent Test**: Can be fully tested by creating a new task with recurrence, due date, and reminder settings and verifying that the data is saved correctly and displayed in the task list.

### Tests for User Story 1 (OPTIONAL - only if tests requested) ⚠️

- [ ] T010 [P] [US1] Create unit test for advanced task creation in frontend/tests/components/TaskForm.test.tsx
- [ ] T011 [P] [US1] Create integration test for API payload in frontend/tests/services/api/taskService.test.ts

### Implementation for User Story 1

- [x] T012 [P] [US1] Add recurrence dropdown to TaskForm component in frontend/src/components/TaskForm/index.tsx
- [x] T013 [P] [US1] Add due date picker to TaskForm component in frontend/src/components/TaskForm/index.tsx
- [x] T014 [P] [US1] Add reminder datetime picker to TaskForm component in frontend/src/components/TaskForm/index.tsx
- [x] T015 [US1] Update TaskForm state to include recurrence, dueDate, and reminderDateTime fields
- [x] T016 [US1] Update TaskForm submission handler to include new fields in API payload
- [x] T017 [US1] Add validation to TaskForm for new fields (reminder before due date, etc.)

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - View Advanced Task Metadata (Priority: P2)

**Goal**: Enable users to see visual indicators for tasks with recurrence, due dates, and reminders so that they can quickly identify which tasks have these advanced properties.

**Independent Test**: Can be tested by viewing a task list with various tasks that have different combinations of recurrence, due dates, and reminders, and verifying that appropriate badges are displayed.

### Tests for User Story 2 (OPTIONAL - only if tests requested) ⚠️

- [ ] T018 [P] [US2] Create unit test for task card badges in frontend/tests/components/TaskCard.test.tsx

### Implementation for User Story 2

- [x] T019 [P] [US2] Add badge rendering logic to TaskCard component in frontend/src/components/TaskCard/index.tsx
- [x] T020 [US2] Implement "Recurring" badge display when task has recurrence pattern
- [x] T021 [US2] Implement "Due Soon" badge display when task due date is within 24 hours
- [x] T022 [US2] Implement "Reminder Set" badge display when task has reminder configured
- [x] T023 [US2] Add CSS classes for badge styling in frontend/src/components/TaskCard/styles.css

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Edit Advanced Task Properties (Priority: P3)

**Goal**: Enable users to modify the recurrence, due date, and reminder settings of existing tasks so that they can adjust their schedule and notifications as needed.

**Independent Test**: Can be tested by selecting an existing task, modifying its advanced properties, saving the changes, and verifying that the updates are reflected in the task list.

### Tests for User Story 3 (OPTIONAL - only if tests requested) ⚠️

- [ ] T024 [P] [US3] Create unit test for advanced task editing in frontend/tests/components/TaskForm.test.tsx

### Implementation for User Story 3

- [x] T025 [P] [US3] Update TaskForm to accept existing task data for editing
- [x] T026 [US3] Populate recurrence dropdown with existing task recurrence value
- [x] T027 [US3] Populate due date picker with existing task due date value
- [x] T028 [US3] Populate reminder datetime picker with existing task reminder value
- [x] T029 [US3] Ensure updateTask API call includes new fields when editing existing tasks

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T030 [P] Update documentation in README or docs/ for advanced features
- [ ] T031 Code cleanup and refactoring of new components
- [ ] T032 Performance optimization for task card rendering with badges
- [ ] T033 [P] Additional unit tests for edge cases in frontend/tests/
- [ ] T034 Security validation for new input fields
- [ ] T035 Run quickstart.md validation checklist

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1 but should be independently testable
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - May integrate with US1/US2 but should be independently testable

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
Task: "Create unit test for advanced task creation in frontend/tests/components/TaskForm.test.tsx"
Task: "Create integration test for API payload in frontend/tests/services/api/taskService.test.ts"

# Launch all UI elements for User Story 1 together:
Task: "Add recurrence dropdown to TaskForm component in frontend/src/components/TaskForm/index.tsx"
Task: "Add due date picker to TaskForm component in frontend/src/components/TaskForm/index.tsx"
Task: "Add reminder datetime picker to TaskForm component in frontend/src/components/TaskForm/index.tsx"
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
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence