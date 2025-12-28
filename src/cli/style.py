"""Terminal styling module for CLI visual enhancements.

This module provides ANSI color formatting and Unicode symbol fallbacks
for terminal output. It automatically detects terminal color support and
gracefully degrades to text-only mode when colors are unavailable.

All styling functions are pure functions with no side effects.
"""

import sys
import os
import re


class AnsiColors:
    """ANSI escape codes for terminal colors (when supported)."""
    RESET = "\033[0m"
    BOLD = "\033[1m"

    # Semantic colors (bright variants for better contrast)
    SUCCESS = "\033[92m"      # Bright Green
    ERROR = "\033[91m"        # Bright Red
    INFO = "\033[96m"         # Bright Cyan
    HEADING = "\033[93m"      # Bright Yellow
    PROMPT = "\033[94m"       # Bright Blue

    # Task status colors
    COMPLETED = "\033[90m"    # Bright Black (Gray) - dimmed
    INCOMPLETE = "\033[97m"   # Bright White - emphasized

    # Utility
    SEPARATOR = "\033[90m"    # Gray for visual dividers


class Symbols:
    """Unicode symbols for visual indicators (fallback mode)."""
    CHECK = "✓"           # U+2713 - Completed task
    CIRCLE = "○"          # U+25CB - Incomplete task
    SUCCESS = "✓"         # Success indicator
    ERROR = "✗"           # U+2717 - Error indicator
    INFO = "ℹ"            # U+2139 - Info indicator
    SEPARATOR = "─"       # U+2500 - Horizontal line


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
    """
    # Check 1: NO_COLOR environment variable (standard)
    if os.getenv('NO_COLOR'):
        return False

    # Check 2: Stdout is a TTY (not redirected)
    if not sys.stdout.isatty():
        return False

    # Check 3: TERM is not 'dumb' (basic terminal)
    if os.getenv('TERM', '') == 'dumb':
        return False

    return True


# Module-level variable set during initialization
_COLORS_ENABLED = _init_colors()


def success(text: str) -> str:
    """
    Format text as a success message.

    Args:
        text: Message text to format

    Returns:
        If colors enabled: Green colored text
        If colors disabled: "[OK] {text}" prefix

    Example:
        success("Task added successfully")
        # With colors: [bright green]Task added successfully[reset]
        # Without colors: [OK] Task added successfully
    """
    if _COLORS_ENABLED:
        return f"{AnsiColors.SUCCESS}{text}{AnsiColors.RESET}"
    else:
        return f"[OK] {text}"


def error(text: str) -> str:
    """
    Format text as an error message.

    Args:
        text: Error message text to format

    Returns:
        If colors enabled: Red colored text
        If colors disabled: "[ERROR] {text}" prefix

    Example:
        error("Task not found")
        # With colors: [bright red]Task not found[reset]
        # Without colors: [ERROR] Task not found
    """
    if _COLORS_ENABLED:
        return f"{AnsiColors.ERROR}{text}{AnsiColors.RESET}"
    else:
        return f"[ERROR] {text}"


def info(text: str) -> str:
    """
    Format text as an informational message.

    Args:
        text: Info message text to format

    Returns:
        If colors enabled: Cyan colored text
        If colors disabled: "[INFO] {text}" prefix

    Example:
        info("No tasks found")
        # With colors: [bright cyan]No tasks found[reset]
        # Without colors: [INFO] No tasks found
    """
    if _COLORS_ENABLED:
        return f"{AnsiColors.INFO}{text}{AnsiColors.RESET}"
    else:
        return f"[INFO] {text}"


def heading(text: str) -> str:
    """
    Format text as a heading or title.

    Args:
        text: Heading text to format

    Returns:
        If colors enabled: Yellow bold text
        If colors disabled: Text as-is (terminal may apply bold if supported)

    Example:
        heading("Main Menu")
        # With colors: [bold][bright yellow]Main Menu[reset]
        # Without colors: Main Menu
    """
    if _COLORS_ENABLED:
        return f"{AnsiColors.BOLD}{AnsiColors.HEADING}{text}{AnsiColors.RESET}"
    else:
        return text


def prompt(text: str) -> str:
    """
    Format text as a user input prompt.

    Args:
        text: Prompt text to format

    Returns:
        If colors enabled: Blue colored text
        If colors disabled: Text as-is (no modification)

    Example:
        prompt("Enter your choice: ")
        # With colors: [bright blue]Enter your choice: [reset]
        # Without colors: Enter your choice:
    """
    if _COLORS_ENABLED:
        return f"{AnsiColors.PROMPT}{text}{AnsiColors.RESET}"
    else:
        return text


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
            - Completed: "[DONE] {task_title}"
            - Incomplete: "[TODO] {task_title}"

    Example:
        format_task_status("Buy groceries", True)
        # With colors: [gray]Buy groceries[reset]
        # Without colors: [DONE] Buy groceries

        format_task_status("Write report", False)
        # With colors: [bright white]Write report[reset]
        # Without colors: [TODO] Write report
    """
    if _COLORS_ENABLED:
        if is_completed:
            return f"{AnsiColors.COMPLETED}{task_title}{AnsiColors.RESET}"
        else:
            return f"{AnsiColors.INCOMPLETE}{task_title}{AnsiColors.RESET}"
    else:
        if is_completed:
            return f"[DONE] {task_title}"
        else:
            return f"[TODO] {task_title}"


def separator(width: int = 40, char: str = "-") -> str:
    """
    Generate a visual separator line.

    Args:
        width: Number of characters wide (default: 40)
        char: Character to use for separator (default: "-")

    Returns:
        If colors enabled: Gray colored separator
        If colors disabled: Plain separator

    Raises:
        ValueError: If width < 0 or char is empty

    Example:
        separator(40)
        # With colors: [gray]----------------------------------------[reset]
        # Without colors: ----------------------------------------

        separator(20, "=")
        # Output: ==================== (styled if colors enabled)
    """
    if width < 0:
        raise ValueError("Width must be non-negative")
    if not char:
        raise ValueError("Character cannot be empty")

    # Use first character if multiple provided
    sep_char = char[0]
    separator_line = sep_char * width

    if _COLORS_ENABLED:
        return f"{AnsiColors.SEPARATOR}{separator_line}{AnsiColors.RESET}"
    else:
        return separator_line


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
    return _COLORS_ENABLED


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
    # Regex pattern to match ANSI escape codes
    ansi_pattern = re.compile(r'\033\[[0-9;]*m')
    return ansi_pattern.sub('', text)
