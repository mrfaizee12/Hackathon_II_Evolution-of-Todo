# Quickstart: CLI Visual Enhancement Implementation

**Feature**: Phase I CLI Visual Enhancement
**Target Audience**: Developers implementing the visual enhancements
**Est. Implementation Time**: 2-3 hours

## Overview

This guide walks through implementing visual enhancements for the Todo CLI application. All changes are purely presentational—no business logic or data models are modified.

## Prerequisites

- Python 3.11+ installed
- Existing Phase I Todo application codebase
- Familiarity with ANSI escape codes (helpful but not required)

## What You'll Build

A centralized styling module (`src/cli/style.py`) that provides:
- Color-coded messages (success, error, info)
- Status-based task formatting (completed vs incomplete)
- Styled headings and separators
- Graceful fallback for terminals without color support

## Implementation Steps

### Step 1: Create the Style Module (30-45 minutes)

**File**: `src/cli/style.py`

**Substeps**:

1. **Define ANSI color constants**
   ```python
   class AnsiColors:
       RESET = "\033[0m"
       BOLD = "\033[1m"
       SUCCESS = "\033[92m"   # Bright Green
       ERROR = "\033[91m"     # Bright Red
       INFO = "\033[96m"      # Bright Cyan
       HEADING = "\033[93m"   # Bright Yellow
       PROMPT = "\033[94m"    # Bright Blue
       COMPLETED = "\033[90m" # Gray
       INCOMPLETE = "\033[97m" # Bright White
       SEPARATOR = "\033[90m" # Gray
   ```

2. **Define Unicode symbol fallbacks**
   ```python
   class Symbols:
       CHECK = "✓"
       CIRCLE = "○"
       SUCCESS = "✓"
       ERROR = "✗"
       INFO = "ℹ"
       SEPARATOR = "─"
   ```

3. **Implement color detection**
   ```python
   import sys
   import os

   def _init_colors() -> bool:
       """Detect if terminal supports colors."""
       if os.getenv('NO_COLOR'):
           return False
       if not sys.stdout.isatty():
           return False
       if os.getenv('TERM', '') == 'dumb':
           return False
       return True

   _COLORS_ENABLED = _init_colors()
   ```

4. **Implement formatting functions**
   - `success(text: str) -> str`
   - `error(text: str) -> str`
   - `info(text: str) -> str`
   - `heading(text: str) -> str`
   - `prompt(text: str) -> str`
   - `format_task_status(task_title: str, is_completed: bool) -> str`
   - `separator(width: int = 40, char: str = "─") -> str`

   **Pattern** (apply to all functions):
   ```python
   def success(text: str) -> str:
       """Format text as success message."""
       if _COLORS_ENABLED:
           return f"{AnsiColors.SUCCESS}{text}{AnsiColors.RESET}"
       else:
           return f"{Symbols.SUCCESS} {text}"
   ```

5. **Implement utility functions**
   - `supports_color() -> bool`
   - `strip_ansi(text: str) -> str`

**Verification**: Import the module and test basic functions:
```bash
python -c "from src.cli.style import success; print(success('Test'))"
```

### Step 2: Update Main Entry Point (15 minutes)

**File**: `src/main.py`

**Changes**:

1. **Import styling functions**
   ```python
   from src.cli.style import heading, error
   ```

2. **Style the welcome message** (line ~47)
   ```python
   # Before:
   print("Welcome to Todo Application - Phase I")

   # After:
   print(heading("Welcome to Todo Application - Phase I"))
   ```

3. **Style error messages** (line ~75)
   ```python
   # Before:
   print("Invalid choice. Please enter a number between 1 and 6.")

   # After:
   print(error("Invalid choice. Please enter a number between 1 and 6."))
   ```

4. **Style version error** (line ~27-30)
   ```python
   # Before:
   print("Error: Python 3.11 or higher is required.")

   # After:
   from src.cli.style import error
   print(error("Python 3.11 or higher is required."))
   ```

**Verification**: Run the application and verify the welcome message is styled.

### Step 3: Update Menu Display (20 minutes)

**File**: `src/cli/menu.py`

**Changes**:

1. **Import styling functions**
   ```python
   from src.cli.style import heading, separator, success, error, prompt
   ```

2. **Style `display_menu()` function** (line ~28-36)
   ```python
   def display_menu() -> None:
       """Display the main menu options."""
       print(f"\n{heading('Main Menu')}")
       print(separator(40))
       print("1. View all tasks")
       print("2. Add a new task")
       print("3. Update a task")
       print("4. Delete a task")
       print("5. Mark task complete/incomplete")
       print("6. Exit")
       print(separator(40))
   ```

3. **Style section headers in handler functions**
   ```python
   # In add_task() (line ~46):
   print(f"\n{heading('--- Add New Task ---')}")

   # In update_task() (line ~70):
   print(f"\n{heading('--- Update Task ---')}")

   # In delete_task() (line ~97):
   print(f"\n{heading('--- Delete Task ---')}")

   # In toggle_status() (line ~117):
   print(f"\n{heading('--- Mark Task Complete/Incomplete ---')}")
   ```

4. **Style success/error messages throughout**
   ```python
   # Pattern for success messages:
   if success:
       print(f"\n{success(message)}")
   else:
       print(f"\n{error(f'Error: {message}')}")
   ```

   Apply to:
   - `add_task()` (line ~57-60)
   - `update_task()` (line ~83-86)
   - `delete_task()` (line ~103-106)
   - `toggle_status()` (line ~141-143)

5. **Style exit message** (line ~153-154)
   ```python
   def exit_application() -> bool:
       print(f"\n{info('Exiting application. All data will be lost.')}")
       print(success("Goodbye!"))
       return True
   ```

**Verification**: Navigate through the menu and verify all sections display with proper styling.

### Step 4: Update Output Formatter (25 minutes)

**File**: `src/cli/output_formatter.py`

**Changes**:

1. **Import styling functions**
   ```python
   from src.cli.style import heading, info, format_task_status, separator
   ```

2. **Style `format_task_list()` function** (line ~9-31)
   ```python
   def format_task_list(tasks: list[Task]) -> None:
       """
       Display all tasks in a formatted list or show empty message.

       Args:
           tasks: List of Task objects to display
       """
       print(f"\n{heading('All Tasks')}")
       print(separator(60))

       if not tasks:
           print(info("No tasks found. Add a task to get started!"))
       else:
           for task in tasks:
               is_completed = task.status == "Complete"
               formatted_title = format_task_status(task.title, is_completed)

               print(f"ID: {task.id} | Title: {formatted_title} | Status: {task.status}")
               print(f"Description: {task.description}")
               print()  # Blank line between tasks

       print(separator(60))
   ```

**Verification**: View the task list and verify completed/incomplete tasks are visually distinct.

### Step 5: Optional - Update Input Handler (10 minutes)

**File**: `src/cli/input_handler.py`

**Changes** (optional, for consistent prompt styling):

1. **Import prompt function**
   ```python
   from src.cli.style import prompt
   ```

2. **Wrap input prompts** (apply throughout file)
   ```python
   # Example in get_task_title() (line ~13):
   return input(prompt("Enter task title: ")).strip()

   # Example in get_task_description() (line ~24):
   return input(prompt("Enter task description: ")).strip()

   # Example in get_menu_choice() (line ~35):
   choice_str = input(prompt("Enter your choice (1-6): ")).strip()
   ```

**Verification**: Verify prompts display with consistent styling.

## Testing

### Manual Testing Checklist

After implementation, manually verify:

- [ ] Welcome message displays with heading style
- [ ] Main menu displays with heading and separators
- [ ] Menu options are clearly readable
- [ ] Success messages display in green (or with ✓ symbol)
- [ ] Error messages display in red (or with ✗ symbol)
- [ ] Completed tasks display dimmed/gray (or with [✓])
- [ ] Incomplete tasks display bright/white (or with [ ])
- [ ] Empty task list shows info message
- [ ] All styling is consistent across screens
- [ ] Application still functions correctly (no broken logic)

### Test in Different Environments

1. **Standard terminal** (with color support)
   ```bash
   python -m src.main
   ```

2. **Without colors** (NO_COLOR environment variable)
   ```bash
   NO_COLOR=1 python -m src.main
   ```
   Verify symbols (✓, ✗, [ ], [✓]) appear instead of colors

3. **Redirected output** (should disable colors)
   ```bash
   python -m src.main > output.txt
   ```
   Check `output.txt` has no ANSI codes

### Automated Testing

Create unit tests in `tests/unit/test_style.py`:

```python
from src.cli.style import success, error, info, format_task_status, strip_ansi

def test_success_with_colors():
    result = success("Test message")
    assert "Test message" in result
    # Should contain ANSI codes when colors enabled

def test_format_task_completed():
    result = format_task_status("Buy milk", True)
    assert "Buy milk" in result
    # Check for completion indicator

def test_format_task_incomplete():
    result = format_task_status("Buy milk", False)
    assert "Buy milk" in result
    # Check for incomplete indicator

def test_strip_ansi():
    styled = "\033[92mSuccess\033[0m"
    plain = strip_ansi(styled)
    assert plain == "Success"
```

Run tests:
```bash
pytest tests/unit/test_style.py
```

## Common Issues & Solutions

### Issue: Colors not displaying

**Symptoms**: Text appears plain without colors

**Solutions**:
1. Verify terminal supports ANSI colors (most modern terminals do)
2. Check `NO_COLOR` environment variable is not set
3. Verify stdout is a TTY (run directly, not redirected)
4. Check TERM environment variable (should not be "dumb")

**Debug**:
```python
from src.cli.style import supports_color
print(f"Color support: {supports_color()}")
```

### Issue: Incorrect colors on light terminal themes

**Symptoms**: Text is hard to read on light backgrounds

**Solution**: The bright color variants (90-97) are chosen for good contrast on both light and dark themes. If issues persist, consider adjusting colors in `AnsiColors` class.

### Issue: Unicode symbols not displaying

**Symptoms**: Boxes or question marks instead of symbols (✓, ✗, ℹ)

**Solution**: Ensure terminal uses UTF-8 encoding. On Windows, use Windows Terminal or PowerShell Core instead of cmd.exe.

### Issue: Tests failing after styling changes

**Symptoms**: Existing tests expect plain text output

**Solution**: Update test assertions to use `strip_ansi()` function:
```python
from src.cli.style import strip_ansi

# In tests:
actual_output = strip_ansi(captured_output)
assert actual_output == expected_plain_text
```

## Performance Considerations

- **Expected overhead**: < 1ms for typical usage
- **No caching needed**: String concatenation is fast enough
- **No I/O operations**: All formatting is in-memory

If you have 100+ tasks and notice slowdown, profile with:
```bash
python -m cProfile -s cumtime -m src.main
```

## Rollback Plan

If issues arise, rollback is simple:

1. Remove or comment out style imports:
   ```python
   # from src.cli.style import heading, success, error
   ```

2. Remove style function wrappings, reverting to plain `print()` statements

3. Optionally delete `src/cli/style.py` file

The application will function identically without styling.

## Next Steps

After completing implementation:

1. **Run full test suite**: `pytest tests/`
2. **Manual QA**: Test all menu options with and without colors
3. **Create pull request**: Reference specification and this quickstart
4. **Document**: Update main README.md with screenshot showing styled output

## Reference

- **Specification**: `specs/001-cli-visual-enhancement/spec.md`
- **Research**: `specs/001-cli-visual-enhancement/research.md`
- **API Contract**: `specs/001-cli-visual-enhancement/contracts/style-api.md`
- **Plan**: `specs/001-cli-visual-enhancement/plan.md`

## Support

If you encounter issues during implementation:
1. Review the specification for requirements clarity
2. Check research.md for technical decisions and rationale
3. Review API contract for function signatures and behavior
4. Test in isolation to identify the problematic area

## Estimated Timeline

- Step 1 (Create style module): 30-45 minutes
- Step 2 (Update main.py): 15 minutes
- Step 3 (Update menu.py): 20 minutes
- Step 4 (Update output_formatter.py): 25 minutes
- Step 5 (Optional input_handler.py): 10 minutes
- Testing & verification: 30 minutes

**Total**: ~2-3 hours for complete implementation and testing
