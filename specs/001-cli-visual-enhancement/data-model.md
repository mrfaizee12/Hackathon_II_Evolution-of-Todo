# Data Model: CLI Visual Enhancement

**Feature**: Phase I CLI Visual Enhancement
**Date**: 2025-12-29
**Note**: This feature does not introduce or modify data entities. This document describes the styling API contract.

## Overview

The CLI Visual Enhancement feature is purely presentational and does not introduce new data models or modify existing entities. The `Task` model remains unchanged. This document describes the styling API contract that will be used throughout the application.

## Existing Data Model (No Changes)

### Task Entity (Unchanged)

The existing `Task` model from `src/models/task.py` remains unmodified:

```python
from dataclasses import dataclass

@dataclass
class Task:
    """Represents a todo task."""
    id: int
    title: str
    description: str
    status: str  # "Complete" or "Incomplete"
```

**No changes to**:
- Field names or types
- Data structure
- Validation rules
- State transitions

## Styling API Contract

### Module: `src/cli/style.py`

This new module provides a clean API for applying visual styling to text output throughout the application.

### Constants

#### Color Codes (When Colors Supported)

```python
class AnsiColors:
    """ANSI escape codes for terminal colors (when supported)."""
    RESET: str = "\033[0m"
    BOLD: str = "\033[1m"

    # Semantic colors (bright variants for better contrast)
    SUCCESS: str = "\033[92m"      # Bright Green
    ERROR: str = "\033[91m"        # Bright Red
    INFO: str = "\033[96m"         # Bright Cyan
    HEADING: str = "\033[93m"      # Bright Yellow
    PROMPT: str = "\033[94m"       # Bright Blue

    # Task status colors
    COMPLETED: str = "\033[90m"    # Bright Black (Gray) - dimmed
    INCOMPLETE: str = "\033[97m"   # Bright White - emphasized

    # Utility
    SEPARATOR: str = "\033[90m"    # Gray for visual dividers
```

#### Symbols (Fallback for Non-Color Terminals)

```python
class Symbols:
    """Unicode symbols for visual indicators (fallback mode)."""
    CHECK: str = "✓"           # U+2713 - Completed task
    CIRCLE: str = "○"          # U+25CB - Incomplete task
    SUCCESS: str = "✓"         # Success indicator
    ERROR: str = "✗"           # U+2717 - Error indicator
    INFO: str = "ℹ"            # U+2139 - Info indicator
    SEPARATOR: str = "─"       # U+2500 - Horizontal line
```

### Module-Level State

```python
# Module-level variable set during initialization
_COLORS_ENABLED: bool = False
```

**Initialization**: The module determines color support once at import time via `_init_colors()` function.

### Core Functions

#### Initialization

```python
def _init_colors() -> bool:
    """
    Initialize color support detection.

    Returns:
        True if terminal supports ANSI colors, False otherwise

    Detection Logic:
        1. Check NO_COLOR environment variable (if set, disable colors)
        2. Check if stdout is a TTY (sys.stdout.isatty())
        3. Check TERM environment variable (disable if 'dumb')
        4. Return True only if all checks pass

    Side Effects:
        Sets module-level _COLORS_ENABLED variable
    """
```

#### Text Formatting Functions

All formatting functions follow the same contract:

**Input**: Plain text string
**Output**: Formatted string (with ANSI codes if colors enabled, or with symbols if not)
**Side Effects**: None
**Thread Safety**: Safe (pure functions)

```python
def success(text: str) -> str:
    """
    Format text as a success message.

    Args:
        text: Message text to format

    Returns:
        If colors enabled: Green colored text
        If colors disabled: "✓ {text}" with check symbol

    Example:
        success("Task added successfully")
        # With colors: "\033[92mTask added successfully\033[0m"
        # Without colors: "✓ Task added successfully"
    """

def error(text: str) -> str:
    """
    Format text as an error message.

    Args:
        text: Error message text to format

    Returns:
        If colors enabled: Red colored text
        If colors disabled: "✗ {text}" with error symbol

    Example:
        error("Task not found")
        # With colors: "\033[91mTask not found\033[0m"
        # Without colors: "✗ Task not found"
    """

def info(text: str) -> str:
    """
    Format text as an informational message.

    Args:
        text: Info message text to format

    Returns:
        If colors enabled: Cyan colored text
        If colors disabled: "ℹ {text}" with info symbol

    Example:
        info("No tasks found")
        # With colors: "\033[96mNo tasks found\033[0m"
        # Without colors: "ℹ No tasks found"
    """

def heading(text: str) -> str:
    """
    Format text as a heading/title.

    Args:
        text: Heading text to format

    Returns:
        If colors enabled: Yellow bold text
        If colors disabled: "{text}" (bold if terminal supports)

    Example:
        heading("Main Menu")
        # With colors: "\033[1m\033[93mMain Menu\033[0m"
        # Without colors: "Main Menu" (may be bold)
    """

def prompt(text: str) -> str:
    """
    Format text as a user prompt.

    Args:
        text: Prompt text to format

    Returns:
        If colors enabled: Blue colored text
        If colors disabled: "{text}" (no modification)

    Example:
        prompt("Enter your choice: ")
        # With colors: "\033[94mEnter your choice: \033[0m"
        # Without colors: "Enter your choice: "
    """
```

#### Task-Specific Formatting

```python
def format_task_status(task_title: str, is_completed: bool) -> str:
    """
    Format task text based on completion status.

    Args:
        task_title: The task title text
        is_completed: True if task is completed, False otherwise

    Returns:
        If colors enabled:
            - Completed: Gray colored text
            - Incomplete: White colored text
        If colors disabled:
            - Completed: "[✓] {task_title}"
            - Incomplete: "[ ] {task_title}"

    Example:
        format_task_status("Buy groceries", True)
        # With colors: "\033[90mBuy groceries\033[0m"
        # Without colors: "[✓] Buy groceries"

        format_task_status("Write report", False)
        # With colors: "\033[97mWrite report\033[0m"
        # Without colors: "[ ] Write report"
    """
```

#### Visual Separator

```python
def separator(width: int = 40, char: str = "─") -> str:
    """
    Generate a visual separator line.

    Args:
        width: Number of characters wide (default: 40)
        char: Character to use for separator (default: "─")

    Returns:
        If colors enabled: Gray colored separator
        If colors disabled: Plain separator

    Example:
        separator(40)
        # With colors: "\033[90m────────────────────────────────────────\033[0m"
        # Without colors: "────────────────────────────────────────"
    """
```

#### Utility Functions

```python
def supports_color() -> bool:
    """
    Check if the current terminal supports ANSI colors.

    Returns:
        True if colors are enabled and supported, False otherwise

    Note:
        This reflects the module initialization result and can be used
        for conditional logic (though typically not needed as formatting
        functions handle this internally).
    """

def strip_ansi(text: str) -> str:
    """
    Remove ANSI escape codes from text.

    Args:
        text: Text potentially containing ANSI codes

    Returns:
        Text with all ANSI escape codes removed

    Use Case:
        Useful for testing or calculating text length without formatting

    Example:
        strip_ansi("\033[92mSuccess\033[0m")
        # Returns: "Success"
    """
```

## Integration Points

### Files to be Modified (Presentation Only)

1. **`src/main.py`**
   - Import `style` module
   - Wrap welcome message with `heading()`
   - Wrap error messages with `error()`

2. **`src/cli/menu.py`**
   - Import `style` module
   - Wrap menu title with `heading()`
   - Wrap success/error messages with `success()` / `error()`
   - Add visual separators with `separator()`

3. **`src/cli/output_formatter.py`**
   - Import `style` module
   - Wrap task list header with `heading()`
   - Use `format_task_status()` for task display
   - Wrap empty state message with `info()`

### No Modifications Required

- `src/models/task.py` - Data model unchanged
- `src/services/task_service.py` - Business logic unchanged
- `src/cli/input_handler.py` - Input validation unchanged (may add `prompt()` wrapper to prompts)

## API Contract Examples

### Usage in Menu Display

```python
# Before
print("\nMain Menu:")
print("1. View all tasks")

# After
from src.cli.style import heading, separator
print(f"\n{heading('Main Menu')}")
print(separator(40))
print("1. View all tasks")
```

### Usage in Success/Error Messages

```python
# Before
print(f"\n{message}")  # Generic message
print(f"\nError: {message}")

# After
from src.cli.style import success, error
print(f"\n{success(message)}")  # For success messages
print(f"\n{error(f'Error: {message}')}")  # For error messages
```

### Usage in Task List Display

```python
# Before
for task in tasks:
    print(f"ID: {task.id} | Title: {task.title} | Status: {task.status}")

# After
from src.cli.style import format_task_status
for task in tasks:
    is_completed = task.status == "Complete"
    formatted_title = format_task_status(task.title, is_completed)
    print(f"ID: {task.id} | Title: {formatted_title} | Status: {task.status}")
```

## Validation & Testing

### Unit Tests Required

Test file: `tests/unit/test_style.py`

1. **Color Detection Tests**
   - Test `_init_colors()` with various environment configurations
   - Test `supports_color()` returns correct state

2. **Formatting Function Tests** (with colors enabled)
   - Test `success()` returns text with green ANSI codes
   - Test `error()` returns text with red ANSI codes
   - Test `info()` returns text with cyan ANSI codes
   - Test `heading()` returns text with yellow bold ANSI codes
   - Test `prompt()` returns text with blue ANSI codes

3. **Formatting Function Tests** (with colors disabled)
   - Test `success()` returns text with check symbol prefix
   - Test `error()` returns text with error symbol prefix
   - Test `info()` returns text with info symbol prefix
   - Test `format_task_status()` returns text with bracket notation

4. **Edge Cases**
   - Test empty strings
   - Test strings with special characters
   - Test very long strings
   - Test strings already containing ANSI codes

5. **Utility Function Tests**
   - Test `separator()` generates correct length
   - Test `strip_ansi()` removes ANSI codes correctly

### Integration Tests Required

Test file: `tests/integration/test_styled_output.py`

1. **Menu Display Tests**
   - Verify menu displays with styled heading
   - Verify separators appear correctly

2. **Task List Display Tests**
   - Verify completed tasks display with appropriate styling
   - Verify incomplete tasks display with appropriate styling
   - Verify empty task list displays info message

3. **Message Display Tests**
   - Verify success messages display correctly after operations
   - Verify error messages display correctly for invalid operations

4. **Consistency Tests**
   - Verify same message type always uses same styling
   - Verify styling doesn't break application flow

## No Schema Changes

This feature introduces no schema, database, or data persistence changes. All styling is applied at the presentation layer during runtime and does not affect data storage or retrieval.

## Backward Compatibility

Since this is Phase I with in-memory storage and no persistence, there are no backward compatibility concerns. The application behavior remains identical—only the visual presentation changes.

## Performance Considerations

- **String Operations**: All formatting functions perform simple string concatenation (O(n))
- **No Caching**: Direct formatting is faster than cache lookup for CLI text
- **No I/O**: All operations are in-memory string manipulation
- **Terminal Rendering**: ANSI code interpretation is handled by the terminal, not Python
- **Expected Overhead**: < 1ms for typical task list formatting (< 100 tasks)

## Compliance

✅ **No Data Model Changes**: Existing `Task` entity unchanged
✅ **Presentation Layer Only**: All styling at output level
✅ **No Business Logic Changes**: Service and model layers untouched
✅ **No External Dependencies**: Standard library only
✅ **Backward Compatible**: No breaking changes to application behavior
✅ **Phase I Constraints**: No persistence, cloud, or multi-user features
