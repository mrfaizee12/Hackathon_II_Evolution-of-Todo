# Tasks: Advanced Todo Features

**Feature**: Advanced Todo Features (Recurring Tasks, Due Dates, Reminders)
**Branch**: `001-advanced-todo-features`
**Generated**: 2026-02-07
**Dependencies**: Python 3.11, FastAPI, SQLModel, Neon PostgreSQL

## Implementation Strategy

Build advanced todo features incrementally with user stories as priority milestones:
1. MVP: Core recurring tasks functionality (User Story 1)
2. Enhanced: Due date management (User Story 2)
3. Complete: Reminder system (User Story 3)
4. Integration: Chatbot capabilities and safety features

Each user story delivers independently testable functionality while building toward the complete feature set.

## Dependencies

User stories can be developed in parallel after foundational components are complete:
- User Story 1 (Recurring Tasks) has no dependencies on other stories
- User Story 2 (Due Dates) has no dependencies on other stories
- User Story 3 (Reminders) depends on User Story 2 (due dates exist)

## Parallel Execution Examples

**Story 1 Tasks** (can execute in parallel):
- T003-T006: Model extensions, service logic, API endpoints, tests for recurring tasks

**Story 2 Tasks** (can execute in parallel):
- T012-T015: Model extensions, service logic, API endpoints, tests for due dates

**Story 3 Tasks** (can execute in parallel):
- T018-T021: Model extensions, service logic, API endpoints, tests for reminders

## Phase 1: Setup Tasks

**Goal**: Initialize feature-specific components and environment

- [x] T001 Create backend/src/models/__init__.py if not exists
- [x] T002 Create backend/src/services/__init__.py if not exists
- [x] T003 Create backend/src/api/__init__.py if not exists
- [x] T004 Create backend/tests/unit/__init__.py if not exists
- [x] T005 Create backend/tests/integration/__init__.py if not exists

## Phase 2: Foundational Tasks

**Goal**: Establish core infrastructure and common components

- [ ] T006 [P] Extend todo_model.py with recurrence, due_date, and reminder fields
- [ ] T007 [P] Create safe database migration for todo table extensions
- [ ] T008 [P] Create todo_events.py for event-driven architecture
- [ ] T009 [P] Create publisher.py for event publishing interface
- [ ] T010 [P] Create helper functions for date/time calculations
- [ ] T011 [P] Implement future date validation utility

## Phase 3: User Story 1 - Recurring Tasks (Priority: P1)

**Goal**: Enable users to create recurring tasks that automatically generate new instances based on frequency (daily, weekly, monthly)

**Independent Test Criteria**: Users can create recurring tasks with daily, weekly, or monthly frequencies and see next instances auto-generated after completion

- [ ] T012 [P] [US1] Implement recurrence logic in todo_service.py
- [ ] T013 [P] [US1] Create recurrence_engine.py for auto-generation
- [ ] T014 [US1] Add recurrence API endpoints to todo_router.py
- [ ] T015 [US1] Create unit tests for recurrence logic in test_recurrence_engine.py
- [ ] T016 [US1] Create integration tests for recurrence API in test_todo_api.py
- [ ] T017 [US1] Validate recurrence integrity and prevent duplicate generations

## Phase 4: User Story 2 - Due Date Management (Priority: P1)

**Goal**: Allow users to assign future-only due dates to tasks and enable sorting/filtering by due dates

**Independent Test Criteria**: Users can add due dates to tasks, validate that only future dates are accepted, and verify that sorting and filtering by due date work correctly

- [ ] T018 [P] [US2] Implement due date validation in todo_model.py
- [ ] T019 [P] [US2] Add due date handling to todo_service.py
- [ ] T020 [US2] Add due date API endpoints to todo_router.py
- [ ] T021 [US2] Create unit tests for due date validation in test_todo_model.py
- [ ] T022 [US2] Create integration tests for due date API in test_todo_api.py
- [ ] T023 [US2] Implement upcoming tasks query with due date filtering

## Phase 5: User Story 3 - Smart Reminders (Priority: P2)

**Goal**: Deliver configurable reminder notifications before task due dates without spam

**Independent Test Criteria**: Users can configure reminder preferences for tasks, set due dates, and verify that timely, non-spammy notifications are delivered

**Depends on**: User Story 2 (due dates exist)

- [ ] T024 [P] [US3] Create reminder_scheduler.py for background processing
- [ ] T025 [P] [US3] Implement reminder logic in todo_service.py
- [ ] T026 [US3] Add reminder API endpoints to todo_router.py
- [ ] T027 [US3] Create unit tests for reminder logic in test_reminder_scheduler.py
- [ ] T028 [US3] Create integration tests for reminder API in test_todo_api.py
- [ ] T029 [US3] Implement spam prevention and deduplication logic

## Phase 6: Chatbot Upgrade

**Goal**: Enable chatbot to handle advanced commands for recurring tasks, due dates, and reminders

- [ ] T030 [P] Create new tools for recurrence functionality
- [ ] T031 [P] Create new tools for due date functionality
- [ ] T032 [P] Create new tools for reminder functionality
- [ ] T033 [P] Update NLP patterns for advanced user intents
- [ ] T034 Update chatbot service to use new tools
- [ ] T035 Test chatbot integration with advanced features

## Phase 7: Safety & Validation

**Goal**: Implement validation and safety measures to prevent issues

- [ ] T036 [P] Implement timezone-safe handling for dates and reminders
- [ ] T037 [P] Add idempotency checks for recurring tasks
- [ ] T038 [P] Add proper error handling for scheduler
- [ ] T039 [P] Implement graceful failure for scheduler
- [ ] T040 Create safety tests for edge cases

## Phase 8: Polish & Cross-Cutting Concerns

**Goal**: Complete the feature with proper documentation, testing, and polish

- [ ] T041 [P] Update documentation with new API endpoints
- [ ] T042 [P] Add performance optimization for due date queries
- [ ] T043 [P] Create contract tests for new API endpoints
- [ ] T044 [P] Add proper logging for new functionality
- [ ] T045 [P] Update indexes as specified in data model
- [ ] T046 [P] Create comprehensive test suite for all features
- [ ] T047 Verify backward compatibility with existing functionality
- [ ] T048 Update quickstart documentation with new features
- [ ] T049 Run full test suite to ensure no regressions