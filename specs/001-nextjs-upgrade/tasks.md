---
description: "Task list for Next.js 14+ to 16+ upgrade implementation"
---

# Tasks: Next.js 14+ to 16+ Upgrade

**Input**: Design documents from `/specs/001-nextjs-upgrade/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, quickstart.md

**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Frontend only**: `frontend/` directory structure
- Paths shown below follow the plan.md structure for the Next.js upgrade

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and preparation for the Next.js upgrade

- [X] T001 Review current frontend dependency versions in frontend/package.json
- [X] T002 [P] Backup current package.json and package-lock.json files
- [X] T003 [P] Document current build and dev server behavior before upgrade

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core dependency upgrades that MUST be complete before compatibility testing can begin

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T004 Upgrade Next.js from 14.0.3 to latest 16.x version in frontend/package.json
- [X] T005 [P] Upgrade react and react-dom to compatible versions in frontend/package.json
- [X] T006 [P] Update related dependencies (@types/react, @types/react-dom, eslint-config-next) in frontend/package.json
- [X] T007 Run npm install in frontend/ to update dependencies
- [X] T008 [P] Review and update next.config.js if needed for Next.js 16 compatibility
- [X] T009 [P] Verify tsconfig.json compatibility with new versions in frontend/tsconfig.json

**Checkpoint**: Dependencies upgraded - compatibility testing can now begin

---

## Phase 3: User Story 1 - Continue Using Todo App Without Disruption (Priority: P1) 🎯 MVP

**Goal**: Ensure all existing functionality works identically after the Next.js upgrade

**Independent Test**: The application should build successfully and all existing UI elements, navigation, and feature interactions should function exactly as before the upgrade.

### Implementation for User Story 1

- [X] T010 [P] [US1] Run build process to identify any compilation issues in frontend/
- [X] T011 [P] [US1] Fix any build errors that arise from Next.js 16 upgrade
- [X] T012 [US1] Test basic app startup and navigation in dev server
- [X] T013 [US1] Verify all existing UI elements display correctly
- [X] T014 [US1] Test todo creation, editing, and deletion functionality
- [X] T015 [US1] Verify tagging, prioritization, search, and due date features work
- [X] T016 [US1] Test all existing component patterns and TypeScript configurations

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Experience Improved Performance (Priority: P2)

**Goal**: Ensure the application maintains or improves performance characteristics after the Next.js 16 upgrade

**Independent Test**: Application should load faster and respond to user interactions with equal or improved speed compared to the previous version.

### Implementation for User Story 2

- [X] T017 [P] [US2] Compare build times between old and new Next.js versions
- [X] T018 [P] [US2] Run production build to verify successful compilation
- [X] T019 [US2] Test runtime performance of key user interactions
- [X] T020 [US2] Verify no performance regression in page loading times
- [X] T021 [US2] Test bundle size differences and optimization features

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Maintain Security and Authentication (Priority: P1)

**Goal**: Ensure Better Auth integration continues to work properly after the Next.js upgrade

**Independent Test**: Login, logout, and protected route access should function exactly as before the upgrade.

### Implementation for User Story 3

- [X] T022 [P] [US3] Test login functionality with Better Auth
- [X] T023 [P] [US3] Test logout functionality with Better Auth
- [X] T024 [US3] Verify protected route access and redirects work properly
- [X] T025 [US3] Test session persistence across page refreshes
- [X] T026 [US3] Verify authentication state management works correctly
- [X] T027 [US3] Test API contract interactions with backend remain unchanged

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Final validation and verification tasks

- [X] T028 [P] Run production build to ensure everything compiles correctly
- [X] T029 [P] Perform comprehensive testing of all app features
- [X] T030 [P] Verify App Router compatibility remains intact
- [X] T031 [P] Check for any runtime warnings or errors
- [X] T032 [P] Clean up any temporary files or backup configurations
- [X] T033 [P] Run quickstart.md validation to confirm setup works
- [X] T034 [P] Document any new Next.js 16+ features leveraged

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
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Builds upon US1 but should be independently testable
- **User Story 3 (P1)**: Can start after Foundational (Phase 2) - Builds upon US1 but should be independently testable

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
# Launch all parallel tasks for User Story 1 together:
Task: "Run build process to identify any compilation issues in frontend/"
Task: "Fix any build errors that arise from Next.js 16 upgrade"
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