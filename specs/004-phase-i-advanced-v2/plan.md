# Implementation Plan: Phase I Advanced (Revised) - Task Scheduling and Organization

**Branch**: `004-phase-i-advanced-v2` | **Date**: 2026-01-01 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/004-phase-i-advanced-v2/spec.md`

## Summary

Phase I Advanced (Revised) extends the existing in-memory Python CLI todo application with six major feature areas: (1) Task Due Date & Time Management with date-time specific scheduling (YYYY-MM-DD HH:MM), (2) Task Statistics & Progress Tracking with due date analytics, (3) Recurring Task Management with daily, weekly, and custom interval support and automatic next-instance creation, (4) Console Reminders for overdue, due today, and upcoming (within 7 days) tasks displayed during CLI operation, (5) Task Templates for rapid consistent task creation, and (6) Command History and Undo for error recovery including recurring task completions. Implementation strictly maintains Phase I scope: in-memory storage only, no databases/files/web/notifications/background services. All features are additive extensions that preserve 100% backward compatibility with Phase I Basic and Intermediate functionality.

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: Python standard library (datetime, dataclasses, collections, typing, enum), no external packages required
**Storage**: In-memory data structures (dict, list), no persistence layer
**Testing**: Standard library unittest framework
**Target Platform**: Windows/Linux/macOS console environment
**Project Type**: Single project (CLI application)
**Performance Goals**:
  - Due date & time validation: <200ms per date (extended from 100ms for date-only)
  - Statistics calculations: <500ms for up to 100 tasks
  - Recurring task auto-creation: <300ms per completion
  - Undo operations: <300ms (includes recurring task restoration)
  - Reminder evaluation: <200ms (on-demand display)
**Constraints**:
  - No database, file system, or persistence mechanisms (Phase I scope)
  - No web, API, network, or external services
  - No notifications, reminders, or background services (reminder evaluation only during CLI operation)
  - Maximum 50 undo history entries
  - Maximum 10 task templates
  - Strict backward compatibility (no changes to Basic or Intermediate behavior)
  - Recurrence rules limited to: none, daily, weekly, or custom day intervals (no hourly, cron-style, or complex schedules)
  - Reminder display only during CLI operation (no background scheduled jobs)
**Scale/Scope**:
  - Single-user CLI application
  - Typically <100 tasks in memory at one time
  - 6 menu extensions (due date, statistics, recurrence, reminders, templates, undo)
  - 51 functional requirements across 6 user stories

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Constitution Compliance Verification

**Phase I Scope Compliance**:
- ✅ In-memory Python console application only (no Phase II+ web/database)
- ✅ No databases, files, or persistence mechanisms
- ✅ No web, browser, or notification APIs
- ✅ No AI or chatbot features
- ✅ No future Phase II+ references
- ✅ No background services or scheduled jobs (reminder evaluation only during CLI operation)

**Spec-Driven Development**:
- ✅ Plan derives from approved specification (spec.md - 004-phase-i-advanced-v2)
- ✅ No feature invention beyond specification scope
- ✅ Backward compatibility mandated (FR-053, FR-054, FR-055, FR-056)
- ✅ Implementation will follow approved tasks (to be created by /sp.tasks)

**Technology Stack**:
- ✅ Python 3.11+ (as required by constitution for Phase I)
- ✅ No external dependencies required (standard library only)
- ✅ Clean architecture maintained (models, services, CLI layers)
- ✅ Domain logic independent of frameworks (pure Python dataclasses)

**Quality Principles**:
- ✅ Clean Architecture: Clear separation between models (Task, RecurrenceRule, Template, History), services (TaskService, TemplateService, HistoryService, ReminderService), and CLI (menus, input/output)
- ✅ Testing: All features require integration tests covering primary user journeys
- ✅ Security: Input validation for dates, times, recurrence rules, templates
- ✅ Performance: Performance goals defined in Technical Context align with SC-001 through SC-027

**Phase Isolation**:
- ✅ No Phase II+ features (no persistence, no multi-user, no REST API, no web UI)
- ✅ Recurrence limited to: none, daily, weekly, or custom day intervals (no hourly, no complex schedules)
- ✅ Reminders limited to: console display during CLI operation only (no external notifications, no background scheduled jobs)
- ✅ All features are extensions to existing Phase I CLI

**GATE RESULT**: ✅ PASS - All constitution gates satisfied

## Project Structure

### Documentation (this feature)

```text
specs/004-phase-i-advanced-v2/
├── spec.md              # Feature specification (already created)
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (below)
├── data-model.md        # Phase 1 output (below)
├── quickstart.md        # Phase 1 output (below)
├── checklists/           # Quality checklist (requirements.md already created)
├── contracts/           # Not applicable (no external APIs)
└── tasks.md             # Phase 2 output (created by /sp.tasks)
```

### Source Code (repository root)

```text
src/
├── models/
│   ├── __init__.py
│   ├── task.py           # Extended: add due_date, recurrence_rule fields
│   ├── enums.py          # Extended: add RecurrenceType, ActionType enums
│   ├── template.py        # NEW: TaskTemplate dataclass
│   └── history.py        # NEW: ActionHistory and HistoryEntry
├── services/
│   ├── __init__.py
│   ├── task_service.py    # Extended: due date, recurrence, reminders, templates, undo
│   ├── template_service.py # NEW: Template CRUD operations
│   ├── history_service.py # NEW: Undo/redo management
│   └── reminder_service.py # NEW: Reminder evaluation
├── cli/
│   ├── __init__.py
│   ├── menu.py           # Extended: new menu options (12-17)
│   ├── input_handler.py   # Extended: date-time input, recurrence input, template input
│   └── output_formatter.py # Extended: date-time display, statistics, reminders
├── utils/
│   ├── __init__.py
│   └── validators.py     # Extended: date-time validation, recurrence validation, template validation
└── main.py              # Extended: initialize new services, evaluate reminders on startup

tests/
├── __init__.py
├── test_task_model.py              # Tests for extended Task model (due_date, recurrence_rule)
├── test_template_model.py           # Tests for Template model
├── test_history_model.py           # Tests for History model
├── test_recurrence_model.py         # NEW: Tests for RecurrenceRule model
├── test_task_service.py             # Tests for TaskService extensions
├── test_template_service.py          # Tests for TemplateService
├── test_history_service.py          # Tests for HistoryService
├── test_reminder_service.py         # NEW: Tests for ReminderService
├── test_date_validation.py          # NEW: Tests for date-time validation
├── test_recurrence_logic.py          # NEW: Tests for recurrence calculation logic
├── test_statistics.py              # Tests for statistics calculations
├── test_bulk_operations.py         # Tests for bulk operations
├── integration_test_due_dates.py    # Integration tests for due date workflow
├── integration_test_statistics.py    # Integration tests for statistics
├── integration_test_recurrence.py    # NEW: Integration tests for recurring tasks
├── integration_test_reminders.py     # NEW: Integration tests for console reminders
├── integration_test_templates.py     # Integration tests for templates
├── integration_test_undo.py          # Integration tests for undo functionality
└── integration_test_backward_compat.py # Tests for backward compatibility
```

**Structure Decision**: Single project structure (existing repository) with modular extensions. New models (template, history, RecurrenceRule), services (template, history, reminder), and CLI extensions added to existing directories. No new top-level directories - maintains clean architecture and follows existing patterns established in Phase I Basic and Intermediate.

## Phase 0: Outline & Research

### Research Summary

Based on revised specification and existing codebase analysis, following decisions and patterns are established:

#### Decision 1: Date-Time Format and Validation

**Decision**: Use ISO 8601 date-time format (YYYY-MM-DD HH:MM) for all user-facing due dates and internal storage.

**Rationale**:
- FR-003 explicitly specifies YYYY-MM-DD HH:MM format
- Python `datetime.datetime.fromisoformat()` provides built-in parsing and validation
- Unambiguous, internationally recognized format
- No timezone complexity (naive datetime only, local system time per spec constraints)

**Alternatives considered**:
- MM/DD/YYYY HH:MM (US format) - Rejected: Locale-specific
- DD/MM/YYYY HH:MM (European format) - Rejected: Varies by region, ambiguous
- Natural language parsing - Rejected: Out of scope for Phase I CLI

**Implementation**:
- Validation with `datetime.datetime.fromisoformat()`
- Reject past dates/times with clear error messages

#### Decision 2: Undo History Implementation

**Decision**: Stack-based undo history with maximum 50 entries (FIFO).

**Rationale**:
- Simple LIFO stack behavior
- Memory-bounded with FIFO
- No redo needed (out of scope)

**Alternatives considered**:
- Full command pattern - Rejected: Redo out of scope
- Persistent undo history - Rejected: Violates in-memory constraint

#### Decision 3: Reminder Evaluation Timing

**Decision**: Evaluate reminders on-demand during CLI operation.

**Rationale**:
- No background services allowed
- Simple: Check when displaying tasks
- Immediate feedback

**Alternatives considered**:
- Background thread polling - Rejected: No background services
- Scheduled job - Rejected: Violates in-memory constraint

#### Decision 4: Recurring Task Auto-Creation

**Decision**: Auto-create next instance immediately when recurring task is marked complete.

**Rationale**:
- User expects immediate feedback
- Simple flow: Complete → Create new → Continue

**Alternatives considered**:
- Create at next app start - Rejected: User expects immediate feedback
- Background delayed creation - Rejected: No background services

#### Decision 5: Undo for Recurring Task Completion

**Decision**: Undo of recurring task completion restores original task and deletes auto-created instance as single atomic action.

**Rationale**:
- Clean semantics: Single undo reverses everything
- FR-050 requires this behavior

**Alternatives considered**:
- Two separate history entries - Rejected: Requires two undos
- Keep auto-created task - Rejected: Violates FR-050

#### Decision 6: DST Handling

**Decision**: Use naive datetime without timezone information (system local time).

**Rationale**:
- Python's naive datetime handles DST automatically
- Simpler implementation
- FR-026 requires DST handling

**Alternatives considered**:
- UTC with timezone - Rejected: Adds complexity beyond Phase I scope
- Explicit DST offset - Rejected: Unnecessary complexity

#### Decision 7: Template Due Date Handling

**Decision**: Templates store relative due date offsets (today, tomorrow, next week).

**Rationale**:
- More useful (always creates relevant due date)
- Simpler for users
- FR-043 requires relative offset

**Alternatives considered**:
- Absolute dates - Rejected: Becomes outdated
- Prompt each time - Rejected: Defeats purpose

**Research Document**: See `research.md` for complete details.

## Phase 1: Design & Contracts

### Data Model Design

See `data-model.md` for complete entity definitions, relationships, validation rules, and state transitions.

### API/Service Contracts

**Note**: No external API contracts (no web/network). Service layer contracts documented in `data-model.md`.

### Quickstart Guide

See `quickstart.md` for development setup, testing procedures, usage examples, and troubleshooting.

### Agent Context Update

**Decision**: Skip agent context update. This is a Phase I CLI feature with no new technology or frameworks.

## Complexity Tracking

> **No constitution violations or unclarified needs - this section remains empty**

All features are within Phase I scope and follow existing architectural patterns.

## Implementation Notes

### Key Implementation Patterns

1. **Backward Compatibility**: All new Task fields are optional with defaults.
2. **In-Memory Storage**: All data structures live in service instance memory. Data lost on application exit.
3. **CLI Menu Extensions**: Menu options 12-17 added for Advanced features.
4. **Date-Time Validation**: Centralized in validators.py using datetime.fromisoformat()
5. **Recurrence Auto-Creation**: When user completes task with non-NONE recurrence, immediately create new instance.
6. **Reminder Evaluation**: On-demand during CLI operation, no background jobs.
7. **Bulk Operations Confirmation**: Require y/n confirmation before execution.
8. **History FIFO**: When undo history exceeds 50 entries, remove oldest.
9. **Template Limit Enforcement**: Maximum 10 templates.
10. **DST Transitions**: System local time handles automatically.

### Integration Points

1. **TaskService Extension**: Add methods for due_date, recurrence, statistics, reminders, templates, bulk operations, undo.
2. **New Services**: TemplateService, HistoryService, ReminderService.
3. **CLI Integration**: Extend menu, input handler, output formatter, main.py.
4. **Recurrence Integration**: Extend toggle_status() to check recurrence and auto-create next instance.
5. **Priority/Tags/Search/Filter/Sort Integration**: All existing features work with extended Task model.

### Testing Strategy

1. **Unit Tests**: Test each model and service method.
2. **Integration Tests**: Test complete user flows.
3. **Backward Compatibility Tests**: Ensure Phase I Basic/Intermediate work identically.

### Success Metrics

Per specification success criteria (SC-001 through SC-027).

## Post-Implementation Phase (after /sp.tasks and /sp.implement)

1. Run all tests (100% pass rate)
2. Manual test each user story
3. Verify performance goals
4. Run backward compatibility tests
5. Test DST transitions
6. Create PHR
7. Consider ADR creation for significant decisions

---

**READY FOR**: `/sp.tasks` - Create task breakdown from this plan
