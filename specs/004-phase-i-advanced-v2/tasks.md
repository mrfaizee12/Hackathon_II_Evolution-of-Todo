# Implementation Tasks: Phase I Advanced (Revised) - Task Scheduling and Organization

**Feature**: 004-phase-i-advanced-v2
**Date**: 2026-01-01
**Plan**: [plan.md](./plan.md) | **Spec**: [spec.md](./spec.md)

## Summary

This document breaks down the implementation of Phase I Advanced (Revised) features into atomic, executable tasks. The feature adds six major capabilities to the existing CLI todo application: (1) Task Due Date & Time Management, (2) Task Statistics & Progress Tracking, (3) Recurring Task Management, (4) Console Reminders, (5) Task Templates, and (6) Command History and Undo. All implementation maintains Phase I scope: in-memory storage, CLI-only, no persistence.

## Task Organization

Tasks are organized by user story priority (P1, P2, P3) with foundational setup tasks first. Each user story gets its own phase with independent test criteria. Tasks follow the checklist format with sequential IDs, file paths, and story labels where applicable.

## Phase 1: Setup Tasks

### Goal
Initialize project structure and foundational components for Phase I Advanced features.

**Independent Test**: All existing Phase I Basic and Intermediate functionality continues to work identically after setup completion.

- [ ] T001 Create new enums for Phase I Advanced in src/models/enums.py
- [ ] T002 Update Task model to support due dates and recurrence in src/models/task.py
- [ ] T003 Create RecurrenceRule model in src/models/task.py
- [ ] T004 Create TaskTemplate model in src/models/template.py
- [ ] T005 Create HistoryEntry and ActionHistory models in src/models/history.py

## Phase 2: Foundational Tasks

### Goal
Implement core infrastructure needed by multiple user stories: due date validation, basic recurrence handling, and undo history.

**Independent Test**: Core data models and validation work correctly with basic operations.

- [ ] T006 Implement due date validation utilities in src/utils/validators.py
- [ ] T007 Extend TaskService with due date methods in src/services/task_service.py
- [ ] T008 Extend TaskService with recurrence methods in src/services/task_service.py
- [ ] T009 Implement HistoryService in src/services/history_service.py
- [ ] T010 Update TaskService to integrate with HistoryService in src/services/task_service.py
- [ ] T011 Implement statistics calculation in src/services/task_service.py

## Phase 3: [US1] Task Due Date Management (Priority: P1)

### Goal
Enable users to set, view, and manage due dates and times on tasks with proper validation.

**Independent Test**: Can create tasks with various due dates and times and verify they display correctly in task list with appropriate formatting.

- [ ] T012 [US1] Implement due date input validation in src/utils/validators.py
- [ ] T013 [US1] Add set_due_date method to TaskService in src/services/task_service.py
- [ ] T014 [US1] Add clear_due_date method to TaskService in src/services/task_service.py
- [ ] T015 [US1] Update Task model to support due date property methods in src/models/task.py
- [ ] T016 [US1] Add due date display to output formatter in src/cli/output_formatter.py
- [ ] T017 [US1] Add due date input handling to CLI in src/cli/input_handler.py
- [ ] T018 [US1] Add due date menu options to CLI in src/cli/menu.py
- [ ] T019 [US1] Add due date functionality to main CLI loop in src/main.py
- [ ] T020 [US1] Test due date validation scenarios in tests/test_date_validation.py

## Phase 4: [US2] Task Progress Tracking and Statistics (Priority: P2)

### Goal
Provide summary statistics about task list including completion rates, priority distribution, and due date analytics.

**Independent Test**: Can create tasks with various states and due dates and verify statistics accurately reflect current task list.

- [ ] T021 [US2] Create TaskStatistics dataclass in src/models/statistics.py
- [ ] T022 [US2] Implement get_statistics method in TaskService in src/services/task_service.py
- [ ] T023 [US2] Add statistics display to output formatter in src/cli/output_formatter.py
- [ ] T024 [US2] Add statistics menu option to CLI in src/cli/menu.py
- [ ] T025 [US2] Test statistics calculations in tests/test_statistics.py

## Phase 5: [US3] Recurring Task Management (Priority: P2)

### Goal
Enable users to set up recurring tasks (daily, weekly, custom) with automatic next instance creation on completion.

**Independent Test**: Can create a recurring task, complete it, and verify the next instance is created with the correct due date based on the recurrence rule.

- [ ] T026 [US3] Implement RecurrenceRule validation in src/utils/validators.py
- [ ] T027 [US3] Add recurrence rule methods to TaskService in src/services/task_service.py
- [ ] T028 [US3] Update toggle_status to handle recurring tasks in src/services/task_service.py
- [ ] T029 [US3] Implement recurring task auto-creation logic in src/services/task_service.py
- [ ] T030 [US3] Add recurrence input handling to CLI in src/cli/input_handler.py
- [ ] T031 [US3] Add recurrence display to output formatter in src/cli/output_formatter.py
- [ ] T032 [US3] Add recurrence menu options to CLI in src/cli/menu.py
- [ ] T033 [US3] Test recurrence logic in tests/test_recurrence_logic.py
- [ ] T034 [US3] Test recurring task integration in tests/integration_test_recurrence.py

## Phase 6: [US4] Console Reminders (Priority: P3)

### Goal
Display console-based reminders about overdue and upcoming tasks during normal CLI operation.

**Independent Test**: Can create tasks with various due dates, run the application, and verify reminders are displayed at appropriate times.

- [ ] T035 [US4] Create ReminderSummary dataclass in src/models/reminder.py
- [ ] T036 [US4] Implement ReminderService in src/services/reminder_service.py
- [ ] T037 [US4] Add reminder evaluation to TaskService in src/services/task_service.py
- [ ] T038 [US4] Add reminder display to output formatter in src/cli/output_formatter.py
- [ ] T039 [US4] Integrate reminders into CLI menu in src/cli/menu.py
- [ ] T040 [US4] Test reminder functionality in tests/test_reminder_service.py
- [ ] T041 [US4] Test reminder integration in tests/integration_test_reminders.py

## Phase 7: [US5] Task Templates (Priority: P3)

### Goal
Enable users to define and use task templates for rapid consistent task creation.

**Independent Test**: Can create a template with predefined values, then use it to create tasks and verify all predefined values are applied correctly.

- [ ] T042 [US5] Implement TemplateService in src/services/template_service.py
- [ ] T043 [US5] Add template input handling to CLI in src/cli/input_handler.py
- [ ] T044 [US5] Add template display to output formatter in src/cli/output_formatter.py
- [ ] T045 [US5] Add template menu options to CLI in src/cli/menu.py
- [ ] T046 [US5] Add template functionality to main CLI loop in src/main.py
- [ ] T047 [US5] Test template functionality in tests/test_template_service.py
- [ ] T048 [US5] Test template integration in tests/integration_test_templates.py

## Phase 8: [US6] Command History and Undo (Priority: P3)

### Goal
Provide undo functionality for recent actions to recover from mistakes.

**Independent Test**: Can perform various actions (create, update, delete, toggle status, complete recurring tasks) and then use undo to verify operations are reversed correctly.

- [ ] T049 [US6] Complete HistoryService implementation with undo logic in src/services/history_service.py
- [ ] T050 [US6] Add undo methods to TaskService in src/services/task_service.py
- [ ] T051 [US6] Add undo menu option to CLI in src/cli/menu.py
- [ ] T052 [US6] Test undo functionality in tests/test_history_service.py
- [ ] T053 [US6] Test undo integration in tests/integration_test_undo.py

## Phase 9: Polish & Cross-Cutting Concerns

### Goal
Complete integration, ensure backward compatibility, add bulk operations, and finalize user experience.

**Independent Test**: All Phase I Advanced features work together and all existing Phase I Basic/Intermediate functionality remains unchanged.

- [ ] T054 Add bulk operations to TaskService in src/services/task_service.py
- [ ] T055 Add bulk operation menu options to CLI in src/cli/menu.py
- [ ] T056 Update main.py to initialize all new services in src/main.py
- [ ] T057 Test backward compatibility in tests/integration_test_backward_compat.py
- [ ] T058 Add comprehensive integration tests in tests/integration_test_due_dates.py
- [ ] T059 Add comprehensive integration tests in tests/integration_test_statistics.py
- [ ] T060 Update CLI output formatting for enhanced display in src/cli/output_formatter.py
- [ ] T061 Add error handling and validation tests in tests/test_task_service.py

## Dependencies

### User Story Completion Order
1. **US1 (P1)**: Due Date Management - Foundation for US4 (Reminders)
2. **US2 (P2)**: Statistics - Depends on US1 (due date analytics)
3. **US3 (P2)**: Recurring Tasks - Independent but uses due dates from US1
4. **US4 (P3)**: Reminders - Depends on US1 (due date detection)
5. **US5 (P3)**: Templates - Independent
6. **US6 (P3)**: Undo - Depends on all other features for comprehensive undo

### Parallel Execution Examples
- **T006-T009**: Validators, TaskService extensions, and HistoryService can be developed in parallel
- **T012-T018**: Due date functionality can be developed in parallel with statistics (T021-T024)
- **T026-T032**: Recurrence logic can be developed in parallel with templates (T042-T046)

## Implementation Strategy

### MVP Scope
The MVP includes User Story 1 (Due Date Management) with basic validation and display. This provides immediate value with minimal implementation effort.

### Delivery Approach
1. **Foundation**: Complete Phase 1-2 (setup and foundational tasks)
2. **P1 Feature**: Complete US1 (due dates) as MVP
3. **P2 Features**: Complete US2 (statistics) and US3 (recurrence) in parallel
4. **P3 Features**: Complete US4 (reminders), US5 (templates), and US6 (undo) in parallel
5. **Integration**: Complete cross-cutting concerns and backward compatibility

### Test Strategy
- Unit tests for each model and service method
- Integration tests for complete user workflows
- Backward compatibility tests to ensure existing functionality unchanged
- Performance tests to verify timing requirements met