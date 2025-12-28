# Implementation Plan: Phase I - Basic Todo Console Application

**Branch**: `001-phase-i-basic-todo` | **Date**: 2025-12-28 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-phase-i-basic-todo/spec.md`

**Note**: This plan describes HOW the approved Phase I requirements will be implemented.

## Summary

Phase I delivers a minimal viable todo application as an in-memory Python console program. Users interact via a text-based menu to perform CRUD operations on tasks (add, view, update, delete, mark complete/incomplete). All data is stored in memory during runtime only - no persistence beyond application exit. This establishes the foundational task management capabilities before adding persistence, multi-user, or web features in later phases.

**Technical Approach**: Single Python script with clean separation between data management (task storage, ID generation, CRUD operations) and user interface (menu display, input handling, output formatting). Tasks stored in a Python dictionary keyed by ID for O(1) lookups. Simple counter-based ID generation ensures uniqueness.

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: None (Python standard library only)
**Storage**: In-memory Python dictionary (no persistence)
**Testing**: pytest (for unit and integration tests)
**Target Platform**: Cross-platform (Windows, Linux, macOS) - runs in any terminal with Python 3.11+
**Project Type**: Single console application
**Performance Goals**: Instant response time (<10ms for all operations), handles 100+ tasks without noticeable delay
**Constraints**: No external dependencies, no file I/O, no network calls, single-threaded execution
**Scale/Scope**: Single user, single session, expected max ~100 tasks per session

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Constitutional Compliance

**✅ Spec-Driven Development (Principle I)**
- Plan derived strictly from approved spec.md
- No features added beyond specification
- All requirements traced to functional requirements (FR-001 through FR-014)

**✅ Agent Behavior Rules (Principle II)**
- No feature invention - implementing only specified CRUD operations
- No deviation - following exact requirements for menu structure, validation, error handling
- No unauthorized improvements - simple, direct implementation

**✅ Phase Governance (Principle III)**
- Zero references to future phases
- No database concepts (Phase II+)
- No web/API infrastructure (Phase II+)
- No authentication (Phase II+)
- No persistence mechanisms that would complicate future database migration

**✅ Technology Stack (Principle IV)**
- Python 3.11+ as mandated by constitution
- Standard library only (no frameworks for Phase I simplicity)
- Prepares for FastAPI/SQLModel in Phase II (clean data model, separation of concerns)

**✅ Quality Principles (Principle V)**
- Clean Architecture: Separation between domain (Task), application (operations), and interface (CLI)
- Stateless operations: Each menu action is independent
- Testing: pytest for unit and integration tests
- Security: Input validation for empty titles, invalid IDs, malformed input
- Performance: In-memory operations, O(1) lookups, instant response

### Phase I Specific Gates

- [x] No database imports or ORM usage
- [x] No file system operations (open, write, read, json.dump, pickle)
- [x] No web framework imports (flask, fastapi, django)
- [x] No authentication logic
- [x] No network operations (requests, http.client, socket)
- [x] Single-user only (no user management, no sessions)
- [x] All data structures are in-memory Python objects

**Status**: ✅ ALL GATES PASSED - Constitution compliant

## Project Structure

### Documentation (this feature)

```text
specs/001-phase-i-basic-todo/
├── plan.md              # This file (/sp.plan command output)
├── spec.md              # Phase I specification (complete)
├── research.md          # Phase 0 output (architectural decisions)
├── data-model.md        # Phase 1 output (Task entity definition)
├── quickstart.md        # Phase 1 output (how to run the application)
├── contracts/           # Phase 1 output (CLI interface contract)
│   └── cli-interface.md # Menu options, inputs, outputs, error messages
├── checklists/          # Validation checklists
│   └── requirements.md  # Spec quality checklist (complete, 100% pass)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created yet)
```

### Source Code (repository root)

```text
src/
├── __init__.py          # Empty module marker
├── main.py              # Application entry point, CLI menu loop
├── models/
│   ├── __init__.py      # Empty module marker
│   └── task.py          # Task data class (dataclass with id, title, description, status)
├── services/
│   ├── __init__.py      # Empty module marker
│   └── task_service.py  # Task CRUD operations (add, get, update, delete, list, toggle_status)
└── cli/
    ├── __init__.py      # Empty module marker
    ├── menu.py          # Menu display and choice handling
    ├── input_handler.py # User input collection and validation
    └── output_formatter.py # Task list display formatting

tests/
├── __init__.py          # Empty module marker
├── integration/
│   ├── __init__.py      # Empty module marker
│   └── test_todo_app_flows.py # End-to-end user story tests
└── unit/
    ├── __init__.py      # Empty module marker
    ├── test_task_model.py      # Task data class tests
    ├── test_task_service.py    # CRUD operation tests
    └── test_cli_components.py  # Input/output handler tests

pyproject.toml           # Project metadata, dependencies, pytest config
README.md                # Project overview, installation, usage
.gitignore               # Python artifacts (__pycache__, .pytest_cache, etc.)
```

**Structure Decision**: Single project layout selected because Phase I is a standalone console application with no frontend/backend split. The `src/` directory organizes code into clear layers (models, services, cli) following clean architecture principles. This structure will accommodate future phases:
- Phase II: Add persistence layer to services (database repositories)
- Phase II: Add web API alongside existing CLI
- Phase III+: Modularize further as complexity grows

The separation of concerns now prevents tight coupling and makes Phase II migration straightforward.

## Complexity Tracking

> No violations - all constitutional gates passed. No complexity justifications needed.

---

## Phase 0: Research & Architectural Decisions

### Research Questions

Since Phase I uses only Python standard library with no external frameworks or persistence, research focuses on architectural patterns and best practices for clean, maintainable console applications.

1. **Data Structure Selection**: What in-memory structure best supports O(1) task lookups by ID while maintaining insertion order for display?
   - **Decision**: Python dictionary with integer keys
   - **Rationale**: O(1) get/set/delete by ID, maintains insertion order (Python 3.7+), simple to implement
   - **Alternatives**: List (O(n) lookup), OrderedDict (unnecessary in 3.7+), custom class (over-engineered)

2. **ID Generation Strategy**: How to generate unique, sequential task IDs that don't conflict after deletions?
   - **Decision**: Counter-based auto-increment, never reuse deleted IDs
   - **Rationale**: Simple, predictable, matches user expectation from spec (ASM-004)
   - **Alternatives**: UUID (overkill), timestamp (not sequential), reuse IDs (confusing for users)

3. **Input Validation Approach**: Where and how to validate user input (menu choices, task IDs, titles)?
   - **Decision**: Validate at input handler layer before passing to service layer
   - **Rationale**: Fail fast, clear error messages, service layer assumes valid input
   - **Alternatives**: Validate in service (duplicates validation), validate in model (too late)

4. **Error Handling Strategy**: How to communicate errors to users (invalid ID, empty title, etc.)?
   - **Decision**: Return success/failure status from services, format error messages in CLI layer
   - **Rationale**: Separation of concerns, testable, consistent error messages
   - **Alternatives**: Exceptions (heavy for expected errors), print directly (not testable)

5. **Menu Loop Architecture**: How to structure the main menu loop for clarity and testability?
   - **Decision**: Infinite loop with explicit exit condition, dispatch table for menu choices
   - **Rationale**: Clear control flow, easy to test individual handlers, follows CLI conventions
   - **Alternatives**: Recursive (stack overflow risk), goto-style (unreadable), state machine (over-engineered)

6. **Testing Strategy**: What level of test coverage for Phase I given no persistence layer?
   - **Decision**: Unit tests for service layer CRUD operations, integration tests for complete user flows
   - **Rationale**: Focus on business logic (services) and user scenarios (spec acceptance criteria)
   - **Alternatives**: Only integration (brittle), only unit (misses workflows), no tests (violates constitution)

### Architectural Decisions Summary

**Architecture Style**: Layered architecture with three distinct layers
- **Model Layer** (`models/`): Data structures (Task dataclass)
- **Service Layer** (`services/`): Business logic (CRUD operations, validation)
- **CLI Layer** (`cli/`): User interface (menu, input, output formatting)

**Data Flow**:
```
User Input → CLI (input_handler) → Service (task_service) → Model (Task) → In-Memory Dict
                                                                                ↓
User Output ← CLI (output_formatter) ←─────────────────────────────────────────┘
```

**Key Patterns**:
- **Dependency Injection**: Service receives task storage dict, enabling test mocking
- **Single Responsibility**: Each module has one clear purpose
- **Separation of Concerns**: UI logic never touches data structures directly

**Future-Proofing for Phase II**:
- Service layer interface remains stable when adding database persistence
- Task model can be converted to SQLModel with minimal changes (add `table=True`)
- CLI layer can coexist with FastAPI web layer

---

## Phase 1: Design & Data Model

### Data Model

**Entity: Task**

```python
from dataclasses import dataclass, field
from typing import Optional

@dataclass
class Task:
    """
    Represents a single todo item.

    Attributes:
        id: Unique numeric identifier (auto-assigned)
        title: Short description of the task (required, non-empty)
        description: Optional detailed description
        status: Completion status ("Complete" or "Incomplete")
    """
    id: int
    title: str
    description: Optional[str] = ""
    status: str = "Incomplete"

    def __post_init__(self):
        """Validate task data after initialization."""
        if not self.title or not self.title.strip():
            raise ValueError("Task title cannot be empty")
        if self.status not in ("Complete", "Incomplete"):
            raise ValueError(f"Invalid status: {self.status}")
```

**Validation Rules** (from FR-009, FR-014):
- Title: Required, non-empty after stripping whitespace
- Description: Optional, can be empty string
- Status: Must be exactly "Complete" or "Incomplete"
- ID: Positive integer, unique within session

**State Transitions**:
- New Task: Always created with status "Incomplete"
- Mark Complete: "Incomplete" → "Complete"
- Mark Incomplete: "Complete" → "Incomplete"
- No other status transitions allowed

**Relationships**: None (Phase I is single-entity)

### Service Layer Interface

**TaskService Class**

```python
class TaskService:
    """
    Manages task CRUD operations with in-memory storage.
    """

    def __init__(self):
        self._tasks: dict[int, Task] = {}  # Storage: task_id -> Task
        self._next_id: int = 1              # Auto-increment counter

    def add_task(self, title: str, description: str = "") -> tuple[bool, str, Optional[int]]:
        """
        Create a new task.
        Returns: (success, message, task_id)
        """
        pass

    def get_task(self, task_id: int) -> Optional[Task]:
        """
        Retrieve a task by ID.
        Returns: Task if found, None otherwise
        """
        pass

    def list_tasks(self) -> list[Task]:
        """
        Get all tasks in insertion order.
        Returns: List of all tasks
        """
        pass

    def update_task(self, task_id: int, title: Optional[str] = None,
                    description: Optional[str] = None) -> tuple[bool, str]:
        """
        Update task title and/or description.
        Returns: (success, message)
        """
        pass

    def delete_task(self, task_id: int) -> tuple[bool, str]:
        """
        Remove a task from storage.
        Returns: (success, message)
        """
        pass

    def toggle_status(self, task_id: int) -> tuple[bool, str]:
        """
        Toggle task between Complete and Incomplete.
        Returns: (success, message)
        """
        pass
```

**Return Convention**: All mutating operations return `(success: bool, message: str, ...)` tuple for consistent error handling in CLI layer.

### CLI Layer Interface

**Menu Options** (from FR-001):
```
1. View all tasks
2. Add a new task
3. Update a task
4. Delete a task
5. Mark task complete/incomplete
6. Exit
```

**Input Contracts**:
- Menu choice: Integer 1-6
- Task ID: Positive integer
- Task title: Non-empty string (validated before service call)
- Task description: Any string (optional, can be empty)
- Complete/Incomplete choice: 'c' or 'i' character

**Output Formats**:
- **Task List**: `ID: <id> | Title: <title> | Status: <status>\nDescription: <description>`
- **Empty List**: "No tasks found. Add a task to get started!"
- **Success Messages**: "<Operation> successful! (ID: <id>)" or "Task marked as <status>!"
- **Error Messages**: "Error: Task not found (ID: <id>)" or "Error: Task title cannot be empty"

**Error Scenarios** (from FR-010, Edge Cases):
- Invalid menu choice → "Invalid choice. Please enter a number between 1 and 6."
- Non-numeric menu input → "Invalid input. Please enter a number."
- Task not found → "Error: Task not found (ID: <id>)"
- Empty title → "Error: Task title cannot be empty"
- Invalid status choice → "Invalid choice. Please enter 'c' for complete or 'i' for incomplete."

See [contracts/cli-interface.md](./contracts/cli-interface.md) for complete interface specification.

### Control Flow

**Main Application Loop** (main.py):
```
1. Display welcome message (FR-013)
2. Loop until exit:
   a. Display menu (FR-001)
   b. Get user choice (1-6)
   c. Validate choice
   d. Dispatch to handler:
      - 1: view_tasks()
      - 2: add_task()
      - 3: update_task()
      - 4: delete_task()
      - 5: toggle_status()
      - 6: exit_application()
   e. Display result
   f. Return to menu (FR-012)
3. Display goodbye message on exit
```

**Handler Pattern**: Each menu option has a dedicated handler function that:
1. Prompts for required input
2. Validates input
3. Calls appropriate service method
4. Formats and displays result

### Error Handling Strategy

**Input Validation** (CLI Layer):
- Menu choice: Try/except for int() conversion, range check 1-6
- Task ID: Try/except for int() conversion, positive check
- Task title: Strip whitespace, check non-empty
- Description: Accept as-is (optional)

**Service Errors** (Service Layer):
- Task not found: Return (False, "Task not found")
- Empty title: Return (False, "Title cannot be empty")
- Invalid status: Raise ValueError in Task.__post_init__

**Display** (CLI Layer):
- Success: Green/bold formatting (if terminal supports), clear message
- Error: Red/bold formatting (if terminal supports), prefix with "Error:"
- Fallback: Plain text if no color support

### Testing Strategy

**Unit Tests** (tests/unit/):
- `test_task_model.py`: Task creation, validation, status values
- `test_task_service.py`: All CRUD operations, edge cases (empty list, invalid ID)
- `test_cli_components.py`: Input validation, output formatting

**Integration Tests** (tests/integration/):
- `test_todo_app_flows.py`: Complete user stories from spec.md
  - US1: View empty list, view populated list
  - US2: Add task with title only, add task with title+description, reject empty title
  - US3: Mark complete, mark incomplete, invalid ID
  - US4: Update title, update description, invalid ID, empty title
  - US5: Delete task, invalid ID

**Test Coverage Target**: 80% line coverage (constitutional requirement)

**Test Data**: Fixtures for common scenarios (empty service, service with 3 tasks, etc.)

---

## Phase 2: Implementation Planning

**Note**: Phase 2 (task breakdown) is handled by the `/sp.tasks` command, not `/sp.plan`. This plan stops here.

The next step is to run `/sp.tasks` to generate the task list from this plan. Tasks will be organized by user story (US1-US5) with clear dependencies and parallel execution opportunities.

---

## Quickstart

See [quickstart.md](./quickstart.md) for detailed setup and run instructions.

**Quick Run**:
```bash
# Ensure Python 3.11+ installed
python --version

# Run the application
python src/main.py

# Run tests
pytest
```

**Development Workflow**:
1. Write tests first (TDD, if requested)
2. Implement feature
3. Run tests: `pytest -v`
4. Check coverage: `pytest --cov=src --cov-report=term-missing`
5. Commit with task reference

---

## Architectural Decision Records

No ADRs created yet. During `/sp.plan` execution, the following architectural decisions were made but do not meet the three-part significance test (Impact + Alternatives + Scope):

**Decisions Made** (documented in research.md, not ADR-worthy):
1. **In-memory dict for storage**: Simple, obvious choice for Phase I, no alternatives seriously considered
2. **Layered architecture**: Standard pattern for console apps, not cross-cutting or system-level
3. **Counter-based ID generation**: Straightforward implementation, no tradeoffs to document

**When to create ADR**: Phase II will require ADRs for:
- Database selection and schema design (Impact: long-term, Alternatives: SQLite vs Neon DB, Scope: all future phases)
- Authentication strategy (Impact: security model, Alternatives: sessions vs JWT, Scope: all user features)
- API design (Impact: contract, Alternatives: REST vs GraphQL, Scope: frontend integration)

---

## Next Steps

1. **Review this plan** for accuracy and constitutional compliance
2. **Run `/sp.tasks`** to generate task breakdown from this plan
3. **Approve tasks** before implementation begins
4. **Run `/sp.implement`** to execute tasks in dependency order

**Dependencies**: None - Phase I is self-contained

**Estimated Effort**: Small (1-2 days for single developer including tests and documentation)

**Risk**: Low - No external dependencies, no persistence complexity, straightforward CRUD operations
