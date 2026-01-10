---
description: "Task list for Todo UX Feedback, Form Reset & Dark Gradient UI implementation"
---

# Tasks: Todo UX Feedback, Form Reset & Dark Gradient UI

**Input**: Design documents from `/specs/004-arguments-feature-todo/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: No explicit tests requested in feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `backend/src/`, `frontend/src/`
- Paths shown below assume web app structure from plan.md

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Create Notification component in frontend/src/components/Notification.tsx
- [x] T002 [P] Update Tailwind configuration for gradient support in frontend/tailwind.config.js
- [x] T003 [P] Verify project structure exists per plan.md

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T004 Apply dark gradient background to main layout in frontend/src/app/layout.tsx
- [x] T005 [P] Define dark gradient CSS in frontend/src/styles/globals.css
- [x] T006 [P] Ensure gradient covers full viewport height
- [x] T007 Verify cards maintain light/white background for contrast
- [x] T008 Test gradient accessibility compliance (WCAG AA)

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Apply Dark Gradient Background (Priority: P1) 🎯 MVP

**Goal**: Apply a modern dark gradient background with deep black edges and subtle blend of dark purple, blue, and teal while maintaining card contrast and readability

**Independent Test**: User accesses the Todo app and sees the dark gradient background applied across the dashboard area while cards remain light/white with sufficient contrast

### Implementation for User Story 1

- [x] T009 [P] [US1] Implement radial gradient with deep black edges in globals.css
- [x] T010 [US1] Add purple/blue/teal color blend to gradient definition
- [x] T011 [US1] Ensure gradient applies to entire dashboard area
- [x] T012 [US1] Verify text readability maintains WCAG AA compliance
- [x] T013 [US1] Test gradient on different screen sizes and devices
- [x] T014 [US1] Validate no CSS breaking on localhost

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Reset Form After Adding Todo (Priority: P1)

**Goal**: Reset all form fields after successfully adding a todo and display success message "Todo added successfully"

**Independent Test**: User fills out the todo form, submits successfully, and sees all form fields cleared automatically with a temporary success message

### Implementation for User Story 2

- [x] T015 [P] [US2] Update TodoForm component state management in frontend/src/components/TodoForm.tsx
- [x] T016 [US2] Implement form reset functionality after successful API call
- [x] T017 [US2] Add success message display "Todo added successfully" after form submission
- [x] T018 [US2] Ensure success message auto-dismisses after 3 seconds
- [x] T019 [US2] Test form reset works correctly when API call succeeds
- [x] T020 [US2] Verify form does not reset when API call fails

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Show Success Message After Delete (Priority: P2)

**Goal**: Display success message "Todo deleted successfully" after deleting a todo with auto-dismiss after short duration

**Independent Test**: User deletes a todo and sees success message "Todo deleted successfully" displayed temporarily before auto-dismissing

### Implementation for User Story 3

- [x] T021 [P] [US3] Update TodoItem component to handle delete success in frontend/src/components/TodoItem.tsx
- [x] T022 [US3] Implement success message display "Todo deleted successfully" after delete operation
- [x] T023 [US3] Ensure delete success message auto-dismisses after 3 seconds
- [x] T024 [US3] Integrate with Notification component for consistent messaging
- [x] T025 [US3] Test delete success message appears only on successful deletion
- [x] T026 [US3] Validate success message timing and display behavior

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T027 [P] Update README with new UI features
- [x] T028 Test CSS breaking on Vercel deployment
- [x] T029 Verify all success messages follow consistent styling
- [x] T030 [P] Run quickstart.md validation
- [x] T031 Final accessibility compliance check

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

- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1

```bash
# Launch all tasks for User Story 1 together:
Task: "Implement radial gradient with deep black edges in globals.css"
Task: "Add purple/blue/teal color blend to gradient definition"
Task: "Ensure gradient applies to entire dashboard area"
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
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence