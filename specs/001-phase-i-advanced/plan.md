# Implementation Plan: Phase I Advanced - Task Deadline and Organization Features

**Branch**: `001-phase-i-advanced` | **Date**: 2026-01-01 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-phase-i-advanced/spec.md`

## Summary

Phase I Advanced extends the existing in-memory Python CLI todo application with five major feature areas: (1) Task Due Date Management for deadline tracking with validation, (2) Task Statistics and Progress Tracking for productivity insights, (3) Bulk Task Operations for efficient multi-task management, (4) Task Templates for rapid consistent task creation, and (5) Command History and Undo for error recovery. Implementation strictly maintains Phase I scope: in-memory storage only, no databases/files/web/notifications, no Phase II+ references. All features are additive extensions that preserve 100% backward compatibility with Phase I Basic and Intermediate functionality.

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: Python standard library (datetime, dataclasses, collections, typing), no external packages required
**Storage**: In-memory data structures (dict, list), no persistence layer
**Testing**: Standard library unittest framework
**Target Platform**: Windows/Linux/macOS console environment
**Project Type**: Single project (CLI application)
**Performance Goals**:
  - Due date validation: <100ms per date
  - Statistics calculations: <500ms for up to 100 tasks
  - Bulk operations: <1 second for up to 50 selected tasks
  - Undo operations: <200ms regardless of action type
**Constraints**:
  - No database, file system, or persistence mechanisms (Phase I scope)
  - No web, API, network, or external services
  - No notifications, reminders, or background services
  - Maximum 50 undo history entries
  - Maximum 10 task templates
  - Strict backward compatibility (no changes to Basic/Intermediate behavior)
**Scale/Scope**:
  - Single-user CLI application
  - Typically <100 tasks in memory at one time
  - 5 menu extensions (due date, statistics, bulk operations, templates, undo)
  - 44 functional requirements across 5 user stories

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Constitution Compliance Verification

**Phase I Scope Compliance**:
- ✅ In-memory Python console application only (no Phase II+ web/database)
- ✅ No databases, files, or persistence mechanisms
- ✅ No web, browser, or notification APIs
- ✅ No AI or chatbot features
- ✅ No future Phase II+ references

**Spec-Driven Development**:
- ✅ Plan derives from approved specification (spec.md)
- ✅ No feature invention beyond specification scope
- ✅ Backward compatibility mandated (FR-042, FR-043, FR-044)
- ✅ Implementation will follow approved tasks (to be created by /sp.tasks)

**Technology Stack**:
- ✅ Python 3.11+ (as required by constitution for Phase I)
- ✅ No external dependencies required (standard library only)
- ✅ Clean architecture maintained (models, services, CLI layers)
- ✅ Domain logic independent of frameworks (pure Python dataclasses)

**Quality Principles**:
- ✅ Clean Architecture: Clear separation between models (Task, Template, History), services (TaskService, TemplateService, HistoryManager), and CLI (menus, input/output)
- ✅ Testing: All features require integration tests covering primary user journeys
- ✅ Security: Input validation for dates, template titles, bulk operations
- ✅ Performance: Performance goals defined in Technical Context align with SC-017 through SC-024

**Phase Isolation**:
- ✅ No Phase II+ features (no persistence, no multi-user, no REST API, no web UI)
- ✅ No recurrence or reminders (explicitly out of scope per spec)
- ✅ All features are extensions to existing Phase I CLI

**GATE RESULT**: ✅ PASS - All constitution gates satisfied

## Project Structure

### Documentation (this feature)

```text
specs/001-phase-i-advanced/
├── spec.md              # Feature specification (already created)
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (below)
├── data-model.md        # Phase 1 output (below)
├── quickstart.md        # Phase 1 output (below)
├── contracts/           # Not applicable (no external APIs)
└── tasks.md             # Phase 2 output (created by /sp.tasks)
```

### Source Code (repository root)

```text
src/
├── models/
│   ├── __init__.py
│   ├── task.py           # Extended: add due_date field
│   ├── template.py        # NEW: TaskTemplate dataclass
│   ├── enums.py          # Extended: add bulk operation types
│   └── history.py        # NEW: ActionHistory and HistoryEntry
├── services/
│   ├── __init__.py
│   ├── task_service.py    # Extended: due date logic, statistics, bulk ops
│   ├── template_service.py # NEW: Template CRUD operations
│   └── history_service.py # NEW: Undo/redo management
├── cli/
│   ├── __init__.py
│   ├── menu.py           # Extended: new menu options (12-16)
│   ├── input_handler.py   # Extended: date input, bulk selection, template input
│   └── output_formatter.py # Extended: due date display, statistics display
├── utils/
│   ├── __init__.py
│   └── validators.py     # Extended: date validation, template validation
└── main.py              # Extended: initialize new services

tests/
├── __init__.py
├── test_task_model.py              # Tests for extended Task model
├── test_template_model.py           # Tests for Template model
├── test_history_model.py           # Tests for History model
├── test_task_service.py             # Tests for TaskService extensions
├── test_template_service.py          # Tests for TemplateService
├── test_history_service.py          # Tests for HistoryService
├── test_date_validation.py          # Tests for date validation utilities
├── test_statistics.py              # Tests for statistics calculations
├── test_bulk_operations.py         # Tests for bulk operations
├── integration_test_due_dates.py    # Integration tests for due date workflow
├── integration_test_statistics.py    # Integration tests for statistics
├── integration_test_bulk_ops.py      # Integration tests for bulk operations
├── integration_test_templates.py     # Integration tests for templates
├── integration_test_undo.py          # Integration tests for undo functionality
└── integration_test_backward_compat.py # Tests for backward compatibility
```

**Structure Decision**: Single project structure (existing repository) with modular extensions. New models (template, history), services (template, history), and CLI extensions added to existing directories. No new top-level directories - maintains clean architecture and follows existing patterns established in Phase I Basic and Intermediate.

## Phase 0: Outline & Research

### Research Summary

Based on the specification and existing codebase analysis, the following decisions and patterns are established:

#### Decision 1: Date Format and Validation

**Decision**: Use ISO 8601 date format (YYYY-MM-DD) for all user-facing due dates and internal storage.

**Rationale**:
- FR-003 explicitly specifies YYYY-MM-DD format
- Python datetime module has built-in support for ISO format parsing and validation
- Unambiguous, internationally recognized format
- Lexicographically sortable as strings (e.g., "2026-01-15" < "2026-01-20")
- No timezone complexity (date-only validation per spec constraints)

**Alternatives considered**:
- MM/DD/YYYY (US locale-specific, confusing internationally)
- DD/MM/YYYY (varies by region, ambiguous)
- Natural language parsing ("tomorrow", "next week") - rejected due to complexity and out of scope (no recurrence)

#### Decision 2: Undo History Implementation Pattern

**Decision**: Use stack-based undo history with maximum 50 entries (FIFO when limit exceeded).

**Rationale**:
- Simple, predictable behavior: undo reverses most recent action first
- Memory-bounded with FIFO prevents uncontrolled growth
- FR-041 requires clearing redo history on new actions (standard pattern)
- No redo needed beyond basic undo (per spec out of scope)
- Each history entry stores action type, task IDs, and previous state snapshot

**Alternatives considered**:
- Full command pattern with redo capability - rejected (redo out of scope)
- Memento pattern with deep copy - rejected (overkill for in-memory structures)
- Persistent undo history - rejected (violates Phase I in-memory constraint)

#### Decision 3: Bulk Task Selection Approach

**Decision**: Range-based selection (start ID, end ID) for bulk operations in CLI environment.

**Rationale**:
- CLI lacks mouse selection capabilities
- Range selection provides clear, unambiguous user interface (e.g., "Select tasks 1-5")
- Efficient for contiguous selections (most common use case)
- Can be extended with individual ID selection if needed
- FR-022 requires confirmation (prevents accidental bulk changes)

**Alternatives considered**:
- Checkbox-style multi-select - not feasible in CLI
- Tag-based selection - already covered by filtering (FR-022, FR-027)
- Individual task ID selection with loop - rejected (inefficient for bulk operations)

#### Decision 4: Template Due Date Handling

**Decision**: Templates store absolute due dates, not relative offsets.

**Rationale**:
- Spec ambiguity resolved (edge case Q: "What happens when user creates template from task with due date, then uses template tomorrow?")
- Absolute dates are simpler: template with "2026-01-15" always creates task with that due date
- User can override due date during task creation (FR-030)
- Relative offsets would require time-awareness and are out of scope (no recurrence per spec)

**Alternatives considered**:
- Relative offset (+7 days) - rejected (adds complexity, time-awareness, potential confusion)
- Prompt user for due date during template-based creation - hybrid approach rejected (choose one pattern)

#### Decision 5: Statistics Calculation Strategy

**Decision**: Calculate statistics on-demand when user views them, not maintain cached statistics.

**Rationale**:
- In-memory data structures make on-demand calculation fast (<500ms per SC-018)
- No stale statistics (always reflects current state)
- Simpler implementation (no cache invalidation logic)
- Task count is low (<100 typical), so overhead is negligible

**Alternatives considered**:
- Event-driven statistics (update on every task change) - rejected (adds complexity, unnecessary for scale)
- Lazy calculation with simple caching - rejected (caching overhead > calculation overhead)

**Research Document**: See `research.md` for complete details.

## Phase 1: Design & Contracts

### Data Model Design

See `data-model.md` for complete entity definitions, relationships, validation rules, and state transitions.

### API/Service Contracts

**Note**: No external API contracts (no web/network). Service layer contracts documented in `data-model.md`.

### Quickstart Guide

See `quickstart.md` for development setup, testing procedures, and usage examples.

### Agent Context Update

**Decision**: Skip agent context update script invocation. This is a Phase I CLI feature with no new technology or frameworks. Existing codebase already uses Python 3.11+, dataclasses, and standard library. No new external dependencies or framework-specific context needs updating.

**Rationale**:
- Constitution requires agent context updates only for "new technology from current plan"
- This plan uses only existing technology: Python 3.11+, dataclasses, datetime, typing
- No new frameworks, libraries, or external dependencies
- Existing codebase patterns already support all planned features

**Confirmation**: Agent context remains unchanged. All implementation can proceed with existing Python knowledge and established codebase patterns.

## Complexity Tracking

> **No constitution violations or unclarified needs - this section remains empty**

All features are within Phase I scope and follow existing architectural patterns established in Phase I Basic and Intermediate. No violations requiring justification.

## Implementation Notes

### Key Implementation Patterns

1. **Backward Compatibility**: All new Task fields (due_date) are optional with default values. Existing tasks (created before Advanced feature) will have due_date=None.

2. **In-Memory Storage**: All data structures (tasks, templates, history) live in service instance memory. Data is lost on application exit (Phase I constraint).

3. **CLI Menu Extensions**: Menu options 12-16 will be added for Advanced features:
   - 12. Set/Update Task Due Date
   - 13. View Task Statistics
   - 14. Bulk Task Operations
   - 15. Manage Task Templates
   - 16. Undo Last Action

4. **Date Validation**: Centralized in validators.py using datetime.date.fromisoformat() with explicit error messages for invalid formats and past dates.

5. **Bulk Operations Confirmation**: All bulk operations require explicit user confirmation (y/n) before execution to prevent accidental changes (FR-022).

6. **History FIFO**: When undo history exceeds 50 entries, oldest entry is removed to maintain limit (FIFO behavior per edge case Q in spec).

### Integration Points

1. **TaskService Extension**: Add methods for due_date, statistics, and bulk operations to existing TaskService without modifying existing methods.

2. **New Services**:
   - TemplateService: Manage template CRUD (create, list, delete, use)
   - HistoryService: Manage undo history and perform undo operations

3. **CLI Integration**:
   - Update display_menu() to show options 12-16
   - Add handler functions for each new menu option
   - Extend input_handler.py for date input, bulk selection, template selection
   - Extend output_formatter.py for due date display and statistics formatting

### Testing Strategy

1. **Unit Tests**: Test each model and service method independently
2. **Integration Tests**: Test complete user flows (create task with due date, view statistics, bulk operations, use template, undo action)
3. **Backward Compatibility Tests**: Ensure all Phase I Basic and Intermediate workflows function identically

### Success Metrics

Per specification success criteria (SC-001 through SC-024):
- All operations meet performance goals (SC-017 through SC-020)
- 100% backward compatibility maintained (SC-006)
- No memory leaks (SC-021, SC-022)
- Graceful error handling (SC-024)

## Post-Implementation Phase (after /sp.tasks and /sp.implement)

1. Run all tests and verify 100% pass rate
2. Manually test each user story with acceptance scenarios from spec.md
3. Verify performance goals met (use time.perf_counter() for validation)
4. Run backward compatibility integration tests
5. Create PHR for implementation work
6. Consider ADR creation if any significant architectural decisions emerge during implementation

---

**READY FOR**: `/sp.tasks` - Create task breakdown from this plan
