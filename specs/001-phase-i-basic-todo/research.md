# Research: Phase I - Basic Todo Console Application

**Feature**: Phase I - Basic Todo Console Application
**Date**: 2025-12-28
**Status**: Complete

## Purpose

This document consolidates research findings and architectural decisions made during Phase 0 planning for the Phase I todo application. Since Phase I uses only Python standard library with no external frameworks or persistence, research focuses on design patterns, data structures, and architectural approaches for clean, maintainable console applications.

## Research Questions & Findings

### 1. Data Structure Selection

**Question**: What in-memory structure best supports O(1) task lookups by ID while maintaining insertion order for display?

**Research Context**:
- Need fast lookups by ID for update/delete/status operations
- Need to preserve insertion order for predictable task list display
- Python 3.7+ guarantees dict insertion order (PEP 468)

**Decision**: Python dictionary with integer keys (`dict[int, Task]`)

**Rationale**:
- O(1) average-case lookup, insert, and delete by ID
- Maintains insertion order automatically in Python 3.7+
- Simple, built-in, no external dependencies
- Natural mapping from task ID to Task object
- Well-understood performance characteristics

**Alternatives Considered**:
1. **List[Task]**
   - ❌ O(n) lookup by ID requires linear search
   - ✅ Simple, maintains order
   - **Rejected**: Performance degrades with task count

2. **OrderedDict**
   - ✅ Guaranteed order, O(1) operations
   - ❌ Unnecessary since dict is ordered in Python 3.7+
   - **Rejected**: No benefit over dict

3. **Custom class with index**
   - ✅ Could optimize specific operations
   - ❌ Over-engineered for simple requirements
   - ❌ Adds complexity without clear benefit
   - **Rejected**: YAGNI principle

**Impact**: Foundation for all task storage and retrieval operations throughout Phase I.

---

### 2. ID Generation Strategy

**Question**: How to generate unique, sequential task IDs that don't conflict after deletions?

**Research Context**:
- Spec assumption ASM-004: "Task IDs are sequential integers (1, 2, 3...) and are not reused after deletion"
- Need predictable, user-friendly IDs
- Must handle deletions without ID collisions

**Decision**: Counter-based auto-increment, never reuse deleted IDs

**Rationale**:
- Simple integer counter starting at 1
- Increment counter on each add, never decrement
- Predictable: IDs increase monotonically
- User-friendly: Small integers easy to type
- Matches user expectations from spec

**Implementation**:
```python
self._next_id: int = 1  # Auto-increment counter

def add_task(self, title: str, description: str = ""):
    task_id = self._next_id
    self._next_id += 1  # Never reuse IDs
    # ... create task with task_id
```

**Alternatives Considered**:
1. **UUID**
   - ✅ Globally unique, no collision risk
   - ❌ Not user-friendly (long hex strings like "550e8400-e29b-41d4-a716-446655440000")
   - ❌ Overkill for single-session, single-user app
   - **Rejected**: Violates simplicity principle

2. **Timestamp-based IDs**
   - ✅ Unique if precision is sufficient
   - ❌ Not sequential (clock skew, duplicates in fast operations)
   - ❌ Meaningless to users
   - **Rejected**: Doesn't meet sequential requirement

3. **Reuse deleted IDs**
   - ✅ Keeps IDs small
   - ❌ Confusing if user remembers old task with same ID
   - ❌ Contradicts spec assumption ASM-004
   - **Rejected**: Violates spec

**Impact**: Affects add_task service method and user perception of task identity.

---

### 3. Input Validation Approach

**Question**: Where and how to validate user input (menu choices, task IDs, titles)?

**Research Context**:
- Multiple input types: menu choices (1-6), task IDs (integers), titles (strings)
- Need clear error messages for users
- Want separation of concerns between layers

**Decision**: Validate at CLI input handler layer before passing to service layer

**Rationale**:
- **Fail Fast**: Catch errors immediately at user input point
- **Clear Error Messages**: CLI layer can format user-friendly messages
- **Separation of Concerns**: Service layer can assume valid input, simplifying logic
- **Testability**: Input validation logic is isolated and unit-testable

**Implementation Pattern**:
```python
# CLI Layer (input_handler.py)
def get_task_id() -> Optional[int]:
    try:
        task_id = int(input("Enter task ID: "))
        if task_id < 1:
            print("Error: Task ID must be positive")
            return None
        return task_id
    except ValueError:
        print("Error: Please enter a valid number")
        return None

# Service Layer (task_service.py)
def delete_task(self, task_id: int):  # Assumes task_id is valid positive int
    if task_id not in self._tasks:
        return (False, "Task not found")
    # ... delete logic
```

**Alternatives Considered**:
1. **Validate in service layer**
   - ✅ Centralized validation logic
   - ❌ Duplicates validation if multiple CLI entry points
   - ❌ Service layer couples to CLI error message formatting
   - **Rejected**: Violates separation of concerns

2. **Validate in model (__post_init__)**
   - ✅ Data integrity guaranteed
   - ❌ Too late - task already partially created
   - ❌ Exceptions harder to handle than return codes for CLI
   - **Rejected**: Use for final integrity checks only (title non-empty, valid status)

3. **No validation (fail at service/model)**
   - ❌ Poor user experience (cryptic errors)
   - ❌ Violates FR-010 (clear error messages)
   - **Rejected**: Unacceptable UX

**Impact**: Defines layer responsibilities and error handling pattern throughout application.

---

### 4. Error Handling Strategy

**Question**: How to communicate errors to users (invalid ID, empty title, etc.)?

**Research Context**:
- Expected errors: task not found, empty title, invalid input
- Need consistent error handling across all operations
- Want testable error paths

**Decision**: Return `(success: bool, message: str, ...)` tuples from service methods, format messages in CLI layer

**Rationale**:
- **Explicit Success/Failure**: Caller always checks success flag
- **Testable**: No side effects (print), return values are easy to assert
- **Consistent Interface**: All service methods follow same pattern
- **Separation of Concerns**: Service returns status, CLI formats and displays

**Implementation**:
```python
# Service Layer
def update_task(self, task_id: int, title: Optional[str], description: Optional[str]):
    if task_id not in self._tasks:
        return (False, "Task not found")
    if title is not None and not title.strip():
        return (False, "Title cannot be empty")
    # ... update logic
    return (True, "Task updated successfully")

# CLI Layer
success, message = service.update_task(task_id, title, description)
if success:
    print(f"✓ {message}")
else:
    print(f"✗ Error: {message}")
```

**Alternatives Considered**:
1. **Exceptions for errors**
   - ✅ Pythonic, clear control flow
   - ❌ Heavy for expected errors (task not found is normal)
   - ❌ Requires try/except boilerplate in CLI
   - ❌ Harder to differentiate error types
   - **Rejected**: Reserve exceptions for unexpected errors

2. **Print directly from service**
   - ✅ Simple, immediate feedback
   - ❌ Not testable (output to stdout)
   - ❌ Couples service to CLI concerns
   - ❌ Can't reuse service in future web API (Phase II)
   - **Rejected**: Violates separation of concerns

3. **Custom result types (Result[T, E])**
   - ✅ Type-safe, explicit errors
   - ❌ Not idiomatic Python (common in Rust/Haskell)
   - ❌ Requires custom classes or library
   - **Rejected**: Over-engineered for simple app

**Impact**: Defines service layer interface and error communication pattern.

---

### 5. Menu Loop Architecture

**Question**: How to structure the main menu loop for clarity and testability?

**Research Context**:
- Need infinite loop until user chooses exit
- Six menu options, each with different handler
- Want clear, maintainable control flow

**Decision**: Infinite `while True` loop with explicit exit condition, dispatch table for menu choices

**Rationale**:
- **Clarity**: Obvious loop structure, clear exit condition
- **Testability**: Handlers are separate functions, easy to unit test
- **Extensibility**: Adding menu options is straightforward (add to dispatch table)
- **Standard Pattern**: Common CLI application pattern

**Implementation**:
```python
def main():
    service = TaskService()
    handlers = {
        1: lambda: view_tasks(service),
        2: lambda: add_task(service),
        3: lambda: update_task(service),
        4: lambda: delete_task(service),
        5: lambda: toggle_status(service),
        6: lambda: exit_application()
    }

    print("Welcome to Todo Application - Phase I")
    while True:
        display_menu()
        choice = get_menu_choice()
        if choice in handlers:
            should_exit = handlers[choice]()
            if should_exit:  # Only exit handler returns True
                break
        else:
            print("Invalid choice. Please enter 1-6.")
```

**Alternatives Considered**:
1. **Recursive menu calls**
   - ✅ Functional style
   - ❌ Stack overflow risk with many iterations
   - ❌ Uncommon in Python CLI apps
   - **Rejected**: Safety concern

2. **Goto-style with labels**
   - ❌ Not supported in Python
   - ❌ Unreadable spaghetti code
   - **Rejected**: Not possible and bad practice

3. **State machine with explicit states**
   - ✅ Formal, clear transitions
   - ❌ Overkill for simple menu (6 options, linear flow)
   - ❌ Adds complexity without benefit
   - **Rejected**: Over-engineered

**Impact**: Defines main application structure and control flow.

---

### 6. Testing Strategy

**Question**: What level of test coverage for Phase I given no persistence layer?

**Research Context**:
- Constitutional requirement: 80% line coverage minimum
- No database, network, or filesystem to mock
- User stories in spec provide acceptance criteria

**Decision**: Unit tests for service layer CRUD operations, integration tests for complete user flows

**Rationale**:
- **Unit Tests**: Isolate business logic (task service) for fast, focused tests
- **Integration Tests**: Validate user stories end-to-end as specified in spec.md
- **Coverage**: Focus on service layer (core logic) and integration paths (user value)
- **Maintainability**: Unit tests document expected behavior, integration tests catch regressions

**Test Structure**:
```
tests/
├── unit/
│   ├── test_task_model.py       # Task creation, validation, status transitions
│   ├── test_task_service.py     # All CRUD operations, edge cases
│   └── test_cli_components.py   # Input validation, output formatting
└── integration/
    └── test_todo_app_flows.py   # User stories US1-US5 from spec.md
```

**Test Coverage Targets**:
- Service layer: 90%+ (core business logic)
- Model layer: 100% (simple dataclass, easy to cover)
- CLI layer: 70%+ (focus on validation logic, formatting tested via integration)
- Overall: 80%+ (constitutional requirement)

**Alternatives Considered**:
1. **Only integration tests**
   - ✅ Tests user value directly
   - ❌ Slow, brittle (full stack)
   - ❌ Hard to isolate failures
   - ❌ Miss edge cases not in user stories
   - **Rejected**: Insufficient coverage

2. **Only unit tests**
   - ✅ Fast, isolated
   - ❌ Miss integration issues
   - ❌ Don't validate user stories from spec
   - **Rejected**: Doesn't verify user value

3. **No tests (manual testing)**
   - ❌ Violates constitutional Quality Principles
   - ❌ Regressions on changes
   - ❌ No documentation of expected behavior
   - **Rejected**: Constitution requires tests

**Impact**: Defines test organization, coverage goals, and development workflow.

---

## Architectural Summary

### Selected Architecture: Layered Architecture (3 Layers)

**Layers**:
1. **Model Layer** (`src/models/`): Data structures (Task dataclass)
2. **Service Layer** (`src/services/`): Business logic (CRUD operations)
3. **CLI Layer** (`src/cli/`): User interface (menu, input, output)

**Data Flow**:
```
User → CLI Input → Service → Model → Storage (dict)
User ← CLI Output ← Service ← Model ← Storage (dict)
```

**Key Principles**:
- **Dependency Injection**: Service receives storage dict, enabling testing
- **Single Responsibility**: Each module has one clear purpose
- **Separation of Concerns**: Layers don't bypass each other (CLI never touches storage directly)

**Benefits for Phase I**:
- Simple, understandable structure
- Testable (layers can be tested independently)
- Maintainable (clear boundaries, easy to locate code)

**Future-Proofing for Phase II**:
- Service layer interface stable when adding database (replace dict with DB repository)
- Task model converts to SQLModel with minimal changes (add `table=True`, database fields)
- CLI layer coexists with FastAPI web layer (both use same service layer)

---

## Technology Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Language | Python 3.11+ | Constitutional requirement, modern features (type hints, dataclasses) |
| Dependencies | Standard library only | Simplicity, no external dependencies to manage |
| Data Storage | dict[int, Task] | O(1) operations, insertion order, built-in |
| Task Model | dataclass | Simple, type-safe, minimal boilerplate |
| ID Generation | Auto-increment counter | Predictable, user-friendly, matches spec assumptions |
| Error Handling | Return tuples (bool, str) | Testable, explicit, consistent interface |
| Testing | pytest | Standard Python testing, good tooling, constitutional compliance |
| Project Structure | src/ + tests/ layout | Standard Python project structure, clear separation |

---

## Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| User enters very long input | Medium | Low | No explicit limit in spec, Python handles large strings fine |
| User creates 1000+ tasks | Low | Low | Dict handles large sizes, spec targets ~100 tasks |
| Invalid UTF-8 in input | Low | Low | Python 3 handles Unicode natively |
| Terminal doesn't support color | Medium | Very Low | Fallback to plain text (already planned) |
| Python < 3.11 installed | Medium | High | Document requirement in README, check version in main.py |

**Overall Risk**: Low - Simple application, no external dependencies, well-understood technology.

---

## Open Questions (Resolved)

All research questions have been resolved. No clarifications needed from user.

---

## References

- [PEP 468 - Preserving Keyword Argument Order](https://peps.python.org/pep-0468/)
- [Python dataclasses documentation](https://docs.python.org/3/library/dataclasses.html)
- [pytest documentation](https://docs.pytest.org/)
- Phase I Specification: [spec.md](./spec.md)
- Evolution of Todo Constitution: [constitution.md](../../.specify/memory/constitution.md)

---

**Status**: Research complete, ready for Phase 1 (data model and contracts definition).
