# Tasks: Phase I CLI Visual Enhancement

**Input**: Design documents from `/specs/001-cli-visual-enhancement/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: This feature does not include automated tests per specification requirements. Manual QA testing is specified instead.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3, US4)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- All paths are relative to repository root: `G:\hackathon_ii\todo_app`

---

## Phase 1: Setup (Styling Module Foundation)

**Purpose**: Create the core styling module that all user stories depend on

**Note**: This phase creates the centralized `src/cli/style.py` module with all styling functions. This must be complete before any CLI modifications in user story phases.

- [x] T001 Create `src/cli/style.py` module skeleton with imports (sys, os) and module docstring
- [x] T002 Implement `AnsiColors` class with all color constants in src/cli/style.py (SUCCESS, ERROR, INFO, HEADING, PROMPT, COMPLETED, INCOMPLETE, SEPARATOR)
- [x] T003 [P] Implement `Symbols` class with fallback Unicode symbols in src/cli/style.py (CHECK, CIRCLE, SUCCESS, ERROR, INFO, SEPARATOR)
- [x] T004 Implement `_init_colors()` function with terminal capability detection in src/cli/style.py (NO_COLOR check, isatty check, TERM check)
- [x] T005 Initialize module-level `_COLORS_ENABLED` variable in src/cli/style.py using _init_colors()

**Checkpoint**: Core infrastructure ready - color detection works, constants defined

---

## Phase 2: Foundational (Styling Functions)

**Purpose**: Implement all styling functions that user stories will use

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T006 [P] Implement `success(text: str) -> str` function in src/cli/style.py (green color or ✓ symbol)
- [x] T007 [P] Implement `error(text: str) -> str` function in src/cli/style.py (red color or ✗ symbol)
- [x] T008 [P] Implement `info(text: str) -> str` function in src/cli/style.py (cyan color or ℹ symbol)
- [x] T009 [P] Implement `heading(text: str) -> str` function in src/cli/style.py (bold yellow color)
- [x] T010 [P] Implement `prompt(text: str) -> str` function in src/cli/style.py (blue color)
- [x] T011 Implement `format_task_status(task_title: str, is_completed: bool) -> str` function in src/cli/style.py (gray/white colors or [✓]/[ ] brackets)
- [x] T012 [P] Implement `separator(width: int = 40, char: str = "─") -> str` function in src/cli/style.py with validation (ValueError for width < 0 or empty char)
- [x] T013 [P] Implement `supports_color() -> bool` utility function in src/cli/style.py (returns _COLORS_ENABLED)
- [x] T014 [P] Implement `strip_ansi(text: str) -> str` utility function in src/cli/style.py using regex to remove ANSI codes

**Checkpoint**: Foundation ready - all 9 styling functions implemented and can be imported

---

## Phase 3: User Story 1 - View Clear, Readable Main Menu (Priority: P1) 🎯 MVP

**Goal**: Style the main menu with heading, separators, and clear visual hierarchy (FR-001, FR-002, FR-003, FR-011, FR-012, FR-013, FR-014)

**Independent Test**: Launch application, verify main menu displays with styled heading in yellow/bold, menu options clearly separated, and consistent formatting. Success = user identifies all options within 3 seconds.

**Specification Requirements**: FR-001 (visual hierarchy), FR-002 (color differentiation), FR-003 (consistency), FR-011 (menu title), FR-012 (numbered options), FR-013 (separators), FR-014 (styled prompts)

### Implementation for User Story 1

- [x] T015 [US1] Import style functions (heading, separator) in src/cli/menu.py
- [x] T016 [US1] Update `display_menu()` function in src/cli/menu.py to wrap "Main Menu:" with heading() and add separator() lines before and after options (lines ~28-36)
- [x] T017 [US1] Import style functions (heading, error) in src/main.py
- [x] T018 [US1] Update welcome message in src/main.py line ~47 to wrap with heading() function
- [x] T019 [US1] Update invalid choice error message in src/main.py line ~75 to wrap with error() function
- [x] T020 [US1] Update Python version error message in src/main.py line ~27-30 to wrap with error() function

**Checkpoint**: Main menu now displays with styled heading, separators, and error messages. Test by launching app - menu should have clear visual hierarchy.

---

## Phase 4: User Story 2 - Distinguish Task Status at a Glance (Priority: P1)

**Goal**: Style task list to visually distinguish completed vs incomplete tasks, with styled header and empty state (FR-009, FR-010, FR-015, FR-016, FR-017, FR-018, FR-019, FR-020, FR-021, FR-022)

**Independent Test**: View task list with mixed completed/incomplete tasks. Verify completed tasks appear dimmed/gray (or [✓]) and incomplete tasks appear bright/white (or [ ]). Verify empty state shows info message. Success = status identified in < 1 second per task.

**Specification Requirements**: FR-009 (completed styling), FR-010 (incomplete styling), FR-015 (list header), FR-016 (status indicators), FR-017 (task IDs), FR-018 (spacing), FR-019 (empty state), FR-020-FR-022 (status consistency)

### Implementation for User Story 2

- [x] T021 [US2] Import style functions (heading, info, format_task_status, separator) in src/cli/output_formatter.py
- [x] T022 [US2] Update `format_task_list()` function in src/cli/output_formatter.py line ~23 to wrap "--- All Tasks ---" header with heading() and add separator(60) after header
- [x] T023 [US2] Update empty state message in src/cli/output_formatter.py line ~26 to wrap "No tasks found..." with info() function
- [x] T024 [US2] Update task display loop in src/cli/output_formatter.py lines ~28-31 to determine completion status and use format_task_status() for task title formatting
- [x] T025 [US2] Add separator(60) line at end of `format_task_list()` function in src/cli/output_formatter.py after task loop

**Checkpoint**: Task list now displays with styled header, status-based task formatting, info-styled empty state, and separators. Test by viewing tasks - completed and incomplete tasks should be visually distinct.

---

## Phase 5: User Story 3 - Understand Operation Outcomes Instantly (Priority: P1)

**Goal**: Style all operation outcome messages (success, error, info) for add, update, delete, toggle operations (FR-005, FR-006, FR-007, FR-023, FR-024, FR-025, FR-026)

**Independent Test**: Perform add task, update task, delete task, and toggle status operations. Verify each displays appropriately styled message (green success, red error, cyan info). Success = outcome understood within 1 second.

**Specification Requirements**: FR-005 (success color), FR-006 (error color), FR-007 (info color), FR-023 (error distinction), FR-024 (success distinction), FR-025 (descriptive text), FR-026 (consistent patterns)

### Implementation for User Story 3

- [x] T026 [US3] Import style functions (heading, success, error) in src/cli/menu.py (add to existing imports)
- [x] T027 [US3] Update `add_task()` section header in src/cli/menu.py line ~46 to wrap "--- Add New Task ---" with heading()
- [x] T028 [US3] Update `add_task()` success/error messages in src/cli/menu.py lines ~57-60 to wrap success path with success() and error path with error()
- [x] T029 [US3] Update `update_task()` section header in src/cli/menu.py line ~70 to wrap "--- Update Task ---" with heading()
- [x] T030 [US3] Update `update_task()` success/error messages in src/cli/menu.py lines ~83-86 to wrap success path with success() and error path with error()
- [x] T031 [US3] Update `update_task()` "No changes made" message in src/cli/menu.py line ~80 to wrap with info()
- [x] T032 [US3] Update `delete_task()` section header in src/cli/menu.py line ~97 to wrap "--- Delete Task ---" with heading()
- [x] T033 [US3] Update `delete_task()` success/error messages in src/cli/menu.py lines ~103-106 to wrap success path with success() and error path with error()
- [x] T034 [US3] Update `toggle_status()` section header in src/cli/menu.py line ~117 to wrap "--- Mark Task Complete/Incomplete ---" with heading()
- [x] T035 [US3] Update `toggle_status()` error message in src/cli/menu.py line ~126 to wrap "Task not found" with error()
- [x] T036 [US3] Update `toggle_status()` success message in src/cli/menu.py line ~141 to wrap with success()
- [x] T037 [US3] Update `toggle_status()` "already complete/incomplete" message in src/cli/menu.py line ~143 to wrap with info()
- [x] T038 [US3] Import style functions (info, success) in src/cli/menu.py for exit_application()
- [x] T039 [US3] Update `exit_application()` messages in src/cli/menu.py lines ~153-154 to wrap "Exiting..." with info() and "Goodbye!" with success()

**Checkpoint**: All operation outcome messages now display with appropriate styling. Test by performing all CRUD operations - each should show clearly styled success/error/info messages.

---

## Phase 6: User Story 4 - Navigate Consistent Visual Language (Priority: P2)

**Goal**: Apply consistent styling to all remaining prompts and ensure visual consistency across entire application (FR-003, FR-008, FR-026)

**Independent Test**: Navigate through all application screens (menu, add task, update task, delete task, toggle status, view tasks, exit). Verify all headings use same style, all success messages same color, all error messages same color, all prompts same style. Success = 100% consistency.

**Specification Requirements**: FR-003 (consistency across screens), FR-008 (heading accent color), FR-026 (consistent message patterns)

### Implementation for User Story 4

- [x] T040 [P] [US4] Import style function (prompt) in src/cli/input_handler.py
- [x] T041 [P] [US4] Update `get_task_title()` prompt in src/cli/input_handler.py line ~13 to wrap "Enter task title:" with prompt()
- [x] T042 [P] [US4] Update `get_task_description()` prompt in src/cli/input_handler.py line ~24 to wrap "Enter task description:" with prompt()
- [x] T043 [P] [US4] Update `get_task_id()` prompt in src/cli/input_handler.py line ~35 to wrap "Enter task ID:" with prompt()
- [x] T044 [P] [US4] Update `get_menu_choice()` prompt in src/cli/input_handler.py line ~45 to wrap "Enter your choice (1-6):" with prompt()
- [x] T045 [P] [US4] Update `get_status_choice()` prompt in src/cli/input_handler.py line ~56 to wrap "Mark as (c)omplete or (i)ncomplete?" with prompt()
- [x] T046 [P] [US4] Update `get_optional_input()` prompts in src/cli/input_handler.py to wrap parameter text with prompt() if applicable

**Checkpoint**: All user input prompts now consistently styled with blue color. Test by navigating all screens - prompts should have consistent appearance throughout application.

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Manual QA testing, documentation, and validation

### Manual QA Testing (Required per specification)

- [x] T047 Manual QA: Test application in standard terminal with color support - verify all colors display correctly
- [x] T048 Manual QA: Test application with NO_COLOR=1 environment variable - verify ASCII fallbacks ([OK], [ERROR], [INFO], [TODO], [DONE]) appear instead of colors
- [x] T049 Manual QA: Test application with output redirected to file - verify no ANSI codes in file, ASCII prefixes used instead
- [ ] T050 Manual QA: Test with 10 mixed completed/incomplete tasks - verify status distinction clear, < 1 second per task
- [x] T051 Manual QA: Test with empty task list - verify styled info message displays
- [ ] T052 Manual QA: Test all CRUD operations - verify success messages green, error messages red, info messages cyan
- [x] T053 Manual QA: Test menu navigation - verify menu title, separators, and options clearly formatted
- [ ] T054 Manual QA: Navigate all screens - verify heading consistency (all yellow/bold), message color consistency (success/error/info)
- [ ] T055 Manual QA: Test with very long task title (>80 characters) - verify styling maintained, text wraps or truncates gracefully
- [ ] T056 Manual QA: Performance test with 100 tasks - verify no perceptible delay in task list rendering (< 1ms overhead per SC-007)

### Documentation & Validation

- [ ] T057 Update README.md with mention of CLI visual enhancements and optional screenshot showing styled output
- [x] T058 Verify no changes to pyproject.toml dependencies section (constitution compliance: no external dependencies)
- [x] T059 Verify src/models/task.py and src/services/task_service.py are unchanged (constitution compliance: no business logic changes)
- [x] T060 Final constitution compliance check: Phase Isolation (no future-phase features), Clean Architecture (presentation only), No Feature Invention (FR-001 to FR-028 only)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - creates styling module skeleton
- **Foundational (Phase 2)**: Depends on Phase 1 (Setup) completion - implements all styling functions - BLOCKS all user stories
- **User Story 1 (Phase 3)**: Depends on Phase 2 (Foundational) completion - can start after all styling functions ready
- **User Story 2 (Phase 4)**: Depends on Phase 2 (Foundational) completion - can start in parallel with US1 (different files)
- **User Story 3 (Phase 5)**: Depends on Phase 2 (Foundational) completion - can start in parallel with US1/US2 (modifies menu.py but different functions)
- **User Story 4 (Phase 6)**: Depends on Phase 2 (Foundational) completion - can start in parallel with US1/US2/US3 (different file: input_handler.py)
- **Polish (Phase 7)**: Depends on all desired user stories being complete (US1-US4)

### User Story Dependencies

- **User Story 1 (P1) - Main Menu**: Independent - no dependencies on other stories, modifies menu.py display_menu() and main.py
- **User Story 2 (P1) - Task List**: Independent - no dependencies on other stories, modifies output_formatter.py only
- **User Story 3 (P1) - Operation Messages**: Independent - no dependencies on other stories, modifies menu.py handler functions (different functions than US1)
- **User Story 4 (P2) - Input Prompts**: Independent - no dependencies on other stories, modifies input_handler.py only

**All user stories can run in parallel once Phase 2 (Foundational) is complete!**

### Within Each User Story

- User Story 1: Tasks T015-T020 must run sequentially (imports before usage)
- User Story 2: Tasks T021-T025 must run sequentially (imports before usage)
- User Story 3: Tasks T026-T039 must run sequentially (imports before modifications)
- User Story 4: All tasks T040-T046 can run in parallel (different functions in same file)

### Parallel Opportunities

- **Phase 1 (Setup)**: T002 and T003 can run in parallel (different classes in same file)
- **Phase 2 (Foundational)**: T006-T010 can run in parallel (different functions), T012-T014 can run in parallel (different functions)
- **After Phase 2 completes**: ALL four user stories (Phases 3-6) can start in parallel by different developers
  - Developer A: User Story 1 (menu display and main.py)
  - Developer B: User Story 2 (task list output)
  - Developer C: User Story 3 (operation messages)
  - Developer D: User Story 4 (input prompts)
- **User Story 4 tasks**: T040-T046 can all run in parallel (different functions in input_handler.py)

---

## Parallel Example: After Foundational Phase

```bash
# Once Phase 2 (Foundational) is complete, launch all user stories in parallel:

# User Story 1 - Main Menu
Task: "Import style functions (heading, separator) in src/cli/menu.py"
Task: "Update display_menu() function..."
Task: "Update welcome message in src/main.py..."
...

# User Story 2 - Task List (parallel with US1)
Task: "Import style functions (heading, info, format_task_status) in src/cli/output_formatter.py"
Task: "Update format_task_list() function..."
...

# User Story 3 - Operation Messages (parallel with US1 and US2)
Task: "Import style functions in src/cli/menu.py..."
Task: "Update add_task() section header..."
...

# User Story 4 - Input Prompts (parallel with US1, US2, and US3)
Task: "Import style function (prompt) in src/cli/input_handler.py"
Task: "Update get_task_title() prompt..."
Task: "Update get_task_description() prompt..."
Task: "Update get_task_id() prompt..."
# All US4 tasks can run in parallel
```

---

## Implementation Strategy

### MVP First (User Stories 1 + 2 Only)

1. Complete Phase 1: Setup (T001-T005) - ~15 minutes
2. Complete Phase 2: Foundational (T006-T014) - ~30 minutes
3. Complete Phase 3: User Story 1 (T015-T020) - ~15 minutes
4. Complete Phase 4: User Story 2 (T021-T025) - ~20 minutes
5. **STOP and VALIDATE**: Test menu and task list independently - visual enhancements for core functionality complete!
6. Deploy/demo if ready (menu and task list styled)

**MVP Scope**: User Stories 1 + 2 provide the core visual improvements (menu + task list) = ~80% of user value

### Full Feature Delivery (All User Stories)

1. Complete Setup + Foundational (Phases 1-2) - ~45 minutes
2. Complete User Story 1 (Phase 3) - ~15 minutes → Test menu styling
3. Complete User Story 2 (Phase 4) - ~20 minutes → Test task list styling
4. Complete User Story 3 (Phase 5) - ~45 minutes → Test operation messages
5. Complete User Story 4 (Phase 6) - ~10 minutes → Test prompt styling
6. Complete Polish & QA (Phase 7) - ~30 minutes → Full validation
7. **Total**: ~2.5-3 hours (aligns with quickstart.md estimate)

### Parallel Team Strategy

With 4 developers (after Phases 1-2 complete together):

1. Team completes Setup + Foundational together (~45 minutes)
2. Once Foundational is done, split into 4 parallel tracks:
   - Developer A: User Story 1 (menu styling) - 15 minutes
   - Developer B: User Story 2 (task list styling) - 20 minutes
   - Developer C: User Story 3 (operation messages) - 45 minutes
   - Developer D: User Story 4 (input prompts) - 10 minutes
3. All stories complete in ~45 minutes (longest task = US3)
4. Regroup for Phase 7 (Manual QA) together - 30 minutes
5. **Total with 4 devs**: ~2 hours

---

## Task Summary

**Total Tasks**: 60
- Phase 1 (Setup): 5 tasks
- Phase 2 (Foundational): 9 tasks (BLOCKS all user stories)
- Phase 3 (User Story 1): 6 tasks
- Phase 4 (User Story 2): 5 tasks
- Phase 5 (User Story 3): 14 tasks
- Phase 6 (User Story 4): 7 tasks
- Phase 7 (Polish & QA): 14 tasks

**Task Breakdown by User Story**:
- User Story 1 (P1 - Main Menu): 6 tasks
- User Story 2 (P1 - Task List): 5 tasks
- User Story 3 (P1 - Operation Messages): 14 tasks
- User Story 4 (P2 - Input Prompts): 7 tasks

**Parallel Opportunities**:
- Phase 1: 2 tasks can run in parallel (T002, T003)
- Phase 2: 8 tasks can run in parallel (T006-T010, T012-T014)
- After Phase 2: All 4 user stories can start in parallel
- User Story 4: All 7 tasks can run in parallel

**Independent Test Criteria**:
- User Story 1: Launch app, verify styled menu with heading/separators (3-second comprehension test)
- User Story 2: View tasks, verify completed/incomplete visual distinction (1-second per task test)
- User Story 3: Perform operations, verify success/error/info messages (1-second outcome test)
- User Story 4: Navigate screens, verify consistent prompt styling across all inputs

**MVP Scope**: User Stories 1 + 2 (11 tasks after foundational) = Styled menu + task list = Core visual improvements

**Constitution Compliance**:
- ✅ Phase Isolation: No future-phase features
- ✅ Technology Stack: Python 3.11+ standard library only (no external dependencies)
- ✅ Clean Architecture: Presentation layer only (src/cli/), no changes to models/services
- ✅ Spec-Driven Development: All tasks trace to FR-001 through FR-028
- ✅ No Feature Invention: Strictly implements specification requirements

**Estimated Total Effort**: 2.5-3 hours (sequential), ~2 hours (with 4-person parallel team)

---

## Notes

- **[P] tasks**: Can run in parallel (different files or different functions, no dependencies)
- **[Story] labels**: Map tasks to specific user stories for traceability and independent testing
- **Each user story is independently testable**: Can validate menu styling, task list styling, message styling, and prompt styling separately
- **No automated tests**: Per specification, this feature uses manual QA testing only
- **Graceful degradation**: All styling functions include fallback to Unicode symbols for terminals without color support
- **Performance**: All styling operations are string concatenation (< 1ms overhead for 100 tasks per SC-007)
- **Commit strategy**: Commit after each user story phase completion (T020, T025, T039, T046) or after logical task groups
- **Stop at any checkpoint**: Each user story checkpoint represents a fully functional, independently testable increment
- **Rollback plan**: If issues arise, comment out style imports and revert print statements (< 5 minutes)

---

## Validation Checklist

Before considering this feature complete, verify:

- [x] All 60 tasks follow checklist format: `- [ ] [ID] [P?] [Story?] Description with file path`
- [x] All user story tasks have [US1], [US2], [US3], or [US4] labels
- [x] Setup and Foundational tasks have NO story labels
- [x] All tasks include exact file paths
- [x] Each user story has independent test criteria
- [x] Task IDs are sequential (T001-T060)
- [x] Parallel opportunities are marked with [P]
- [x] Dependencies section shows user story completion order
- [x] MVP scope identified (User Stories 1 + 2)
- [x] Estimated effort aligns with plan.md (2.5-3 hours)
