# Style API Contract

**Module**: `src.cli.style`
**Version**: 1.0.0
**Purpose**: Provide consistent terminal styling API for CLI visual enhancements

## API Overview

The `style` module provides a clean, functional API for applying ANSI terminal colors and formatting to text output. It automatically detects terminal capabilities and gracefully degrades to text-only mode when colors are not supported.

## Module Initialization

The module initializes color support detection on import. No explicit initialization call is required.

```python
import src.cli.style as style
# Color support is automatically detected
```

## Public API

### Text Formatting Functions

All formatting functions are pure functions with no side effects.

#### `success(text: str) -> str`

**Purpose**: Format text as a success message
**Parameters**:
- `text` (str): Message text to format (required)

**Returns**: `str` - Formatted text with success styling

**Behavior**:
- With colors: Returns text in bright green with ANSI codes
- Without colors: Returns text prefixed with "✓ "

**Example**:
```python
from src.cli.style import success
print(success("Task added successfully"))
# Output (with colors): [bright green]Task added successfully[reset]
# Output (no colors): ✓ Task added successfully
```

**Edge Cases**:
- Empty string: Returns styled empty string (or just symbol in fallback mode)
- Multiline text: Preserves newlines, applies styling to entire text

---

#### `error(text: str) -> str`

**Purpose**: Format text as an error message
**Parameters**:
- `text` (str): Error message text to format (required)

**Returns**: `str` - Formatted text with error styling

**Behavior**:
- With colors: Returns text in bright red with ANSI codes
- Without colors: Returns text prefixed with "✗ "

**Example**:
```python
from src.cli.style import error
print(error("Task not found"))
# Output (with colors): [bright red]Task not found[reset]
# Output (no colors): ✗ Task not found
```

**Edge Cases**:
- Empty string: Returns styled empty string (or just symbol in fallback mode)
- Text already starting with "Error:": No duplication, styles entire text

---

#### `info(text: str) -> str`

**Purpose**: Format text as an informational message
**Parameters**:
- `text` (str): Info message text to format (required)

**Returns**: `str` - Formatted text with info styling

**Behavior**:
- With colors: Returns text in bright cyan with ANSI codes
- Without colors: Returns text prefixed with "ℹ "

**Example**:
```python
from src.cli.style import info
print(info("No tasks found"))
# Output (with colors): [bright cyan]No tasks found[reset]
# Output (no colors): ℹ No tasks found
```

**Edge Cases**:
- Empty string: Returns styled empty string (or just symbol in fallback mode)

---

#### `heading(text: str) -> str`

**Purpose**: Format text as a heading or title
**Parameters**:
- `text` (str): Heading text to format (required)

**Returns**: `str` - Formatted text with heading styling

**Behavior**:
- With colors: Returns text in bright yellow and bold with ANSI codes
- Without colors: Returns text as-is (terminal may apply bold if supported)

**Example**:
```python
from src.cli.style import heading
print(heading("Main Menu"))
# Output (with colors): [bold][bright yellow]Main Menu[reset]
# Output (no colors): Main Menu
```

**Edge Cases**:
- Empty string: Returns styled empty string

---

#### `prompt(text: str) -> str`

**Purpose**: Format text as a user input prompt
**Parameters**:
- `text` (str): Prompt text to format (required)

**Returns**: `str` - Formatted text with prompt styling

**Behavior**:
- With colors: Returns text in bright blue with ANSI codes
- Without colors: Returns text as-is (no modification)

**Example**:
```python
from src.cli.style import prompt
user_input = input(prompt("Enter your choice: "))
# Output (with colors): [bright blue]Enter your choice: [reset]
# Output (no colors): Enter your choice:
```

**Edge Cases**:
- Empty string: Returns empty string (styled if colors enabled)
- Text with trailing space: Preserves whitespace

---

#### `format_task_status(task_title: str, is_completed: bool) -> str`

**Purpose**: Format task text based on completion status
**Parameters**:
- `task_title` (str): The task title text (required)
- `is_completed` (bool): True if task is completed, False if incomplete (required)

**Returns**: `str` - Formatted task title with status-appropriate styling

**Behavior**:
- With colors, completed: Returns text in gray (dimmed)
- With colors, incomplete: Returns text in bright white (emphasized)
- Without colors, completed: Returns "[✓] {task_title}"
- Without colors, incomplete: Returns "[ ] {task_title}"

**Example**:
```python
from src.cli.style import format_task_status
title1 = format_task_status("Buy groceries", True)
title2 = format_task_status("Write report", False)
print(title1)  # Completed task
print(title2)  # Incomplete task
# With colors: [gray]Buy groceries[reset]
#              [bright white]Write report[reset]
# No colors:   [✓] Buy groceries
#              [ ] Write report
```

**Edge Cases**:
- Empty task title: Returns styled empty string or just brackets/symbol
- Very long task title: No truncation, full text is styled

---

#### `separator(width: int = 40, char: str = "─") -> str`

**Purpose**: Generate a visual separator line
**Parameters**:
- `width` (int): Number of characters wide (default: 40, optional)
- `char` (str): Character to repeat for separator (default: "─", optional)

**Returns**: `str` - Separator line string

**Behavior**:
- With colors: Returns gray colored separator
- Without colors: Returns plain separator

**Example**:
```python
from src.cli.style import separator
print(separator(40))
# Output (with colors): [gray]────────────────────────────────────────[reset]
# Output (no colors):   ────────────────────────────────────────

print(separator(20, "="))
# Output: ==================== (styled if colors enabled)
```

**Edge Cases**:
- `width = 0`: Returns empty string
- `width < 0`: Raises ValueError
- `char` with length > 1: Uses first character only
- `char` is empty string: Raises ValueError

---

### Utility Functions

#### `supports_color() -> bool`

**Purpose**: Check if terminal supports ANSI colors
**Parameters**: None

**Returns**: `bool` - True if colors are enabled and supported, False otherwise

**Example**:
```python
from src.cli.style import supports_color
if supports_color():
    print("Terminal supports colors!")
else:
    print("Running in fallback mode")
```

**Note**: This function is provided for informational purposes. The formatting functions already handle color detection internally, so explicit checks are typically not needed.

---

#### `strip_ansi(text: str) -> str`

**Purpose**: Remove ANSI escape codes from text
**Parameters**:
- `text` (str): Text potentially containing ANSI escape codes (required)

**Returns**: `str` - Text with all ANSI codes removed

**Example**:
```python
from src.cli.style import strip_ansi, success
styled = success("Hello")
plain = strip_ansi(styled)
print(len(plain))  # Returns 5, not counting ANSI codes
```

**Use Cases**:
- Testing output assertions
- Calculating display width
- Logging to files without formatting

**Edge Cases**:
- Text without ANSI codes: Returns text unchanged
- Empty string: Returns empty string
- Malformed ANSI codes: Best-effort removal

---

## Module Constants

### `AnsiColors` Class

**Purpose**: Container for ANSI escape code constants
**Visibility**: Internal (not part of public API, but can be imported for advanced use)

**Attributes**:
```python
class AnsiColors:
    RESET: str       # "\033[0m"
    BOLD: str        # "\033[1m"
    SUCCESS: str     # "\033[92m" (Bright Green)
    ERROR: str       # "\033[91m" (Bright Red)
    INFO: str        # "\033[96m" (Bright Cyan)
    HEADING: str     # "\033[93m" (Bright Yellow)
    PROMPT: str      # "\033[94m" (Bright Blue)
    COMPLETED: str   # "\033[90m" (Gray)
    INCOMPLETE: str  # "\033[97m" (Bright White)
    SEPARATOR: str   # "\033[90m" (Gray)
```

### `Symbols` Class

**Purpose**: Container for Unicode symbol constants
**Visibility**: Internal (not part of public API)

**Attributes**:
```python
class Symbols:
    CHECK: str      # "✓" (U+2713)
    CIRCLE: str     # "○" (U+25CB)
    SUCCESS: str    # "✓"
    ERROR: str      # "✗" (U+2717)
    INFO: str       # "ℹ" (U+2139)
    SEPARATOR: str  # "─" (U+2500)
```

---

## Color Detection Logic

The module uses the following logic to detect color support:

1. **Check `NO_COLOR` environment variable**
   - If set (any value), disable colors
   - Respects [NO_COLOR standard](https://no-color.org/)

2. **Check if stdout is a TTY**
   - Use `sys.stdout.isatty()`
   - If False (redirected to file/pipe), disable colors

3. **Check `TERM` environment variable**
   - If value is "dumb", disable colors
   - Prevents ANSI codes in basic terminals

4. **Enable colors if all checks pass**

---

## Thread Safety

All functions in this module are **thread-safe** because they are pure functions with no side effects and no mutable shared state (the `_COLORS_ENABLED` module variable is set once at import time and never modified).

---

## Performance Characteristics

- **Initialization**: O(1) - Single terminal capability check at import time
- **Formatting Functions**: O(n) - Linear in text length (simple string concatenation)
- **Memory**: O(1) - No caching or state storage
- **Overhead**: < 1ms for typical CLI text formatting

---

## Error Handling

All functions handle edge cases gracefully:
- **Empty strings**: Return appropriately styled/formatted empty string
- **None values**: Raise `TypeError` (Python default for string operations)
- **Invalid types**: Raise `TypeError` (Python default)
- **Invalid `width` parameter**: Raise `ValueError` if < 0
- **Invalid `char` parameter**: Raise `ValueError` if empty

No exceptions are raised for valid inputs under any terminal configuration.

---

## Example Usage Patterns

### Basic Message Formatting

```python
from src.cli.style import success, error, info

# Success message
print(success("Operation completed successfully"))

# Error message
print(error("Operation failed: File not found"))

# Info message
print(info("Processing 10 items..."))
```

### Menu Display

```python
from src.cli.style import heading, separator, prompt

print(f"\n{heading('Main Menu')}")
print(separator(40))
print("1. View all tasks")
print("2. Add a new task")
print("3. Exit")
print(separator(40))
choice = input(prompt("Enter your choice: "))
```

### Task List Display

```python
from src.cli.style import heading, format_task_status, info

print(f"\n{heading('Task List')}")

if not tasks:
    print(info("No tasks found. Add a task to get started!"))
else:
    for task in tasks:
        is_completed = task.status == "Complete"
        formatted_title = format_task_status(task.title, is_completed)
        print(f"ID: {task.id} | {formatted_title} | Status: {task.status}")
```

### Conditional Styling

```python
from src.cli.style import success, error

success_flag, message = service.add_task(title, description)
print(success(message) if success_flag else error(message))
```

---

## Testing Contract

### Unit Test Coverage Requirements

1. **Color detection tests** (`test_style_init.py`)
   - Test with NO_COLOR set
   - Test with stdout not a TTY
   - Test with TERM=dumb
   - Test with full color support

2. **Formatting function tests** (`test_style_formatting.py`)
   - Test each function with colors enabled
   - Test each function with colors disabled
   - Test with empty strings
   - Test with special characters

3. **Task status formatting tests** (`test_style_tasks.py`)
   - Test completed task formatting
   - Test incomplete task formatting
   - Test with both color modes

4. **Utility function tests** (`test_style_utils.py`)
   - Test `separator()` with various widths
   - Test `strip_ansi()` with various inputs
   - Test edge cases

### Integration Test Requirements

Tests should verify that styled output appears correctly in actual CLI operations without breaking application logic.

---

## Deprecation Policy

This is version 1.0.0 of the Style API. Breaking changes will only be introduced in major version bumps (2.0.0, etc.) and will be communicated clearly. Minor and patch versions will maintain backward compatibility.

---

## Compliance

✅ **No External Dependencies**: Uses Python 3.11+ standard library only
✅ **Purely Presentational**: No business logic changes
✅ **Graceful Degradation**: Works in any terminal environment
✅ **Consistent API**: All formatting functions follow same pattern
✅ **Well-Documented**: Complete parameter and behavior specification
✅ **Testable**: Pure functions enable comprehensive unit testing
