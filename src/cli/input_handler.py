"""Input handling for the CLI.

This module handles user input collection and validation.
"""

from datetime import datetime
from typing import Optional, Tuple
from src.cli.style import prompt


def get_task_title() -> str:
    """
    Prompt user for task title and validate it's non-empty.

    Returns:
        Task title (guaranteed non-empty after stripping)
    """
    title = input(prompt("Enter task title: ")).strip()
    return title


def get_task_description() -> str:
    """
    Prompt user for optional task description.

    Returns:
        Task description (can be empty string)
    """
    description = input(prompt("Enter task description (optional): "))
    return description


def get_menu_choice(max_choice: int = 11) -> Optional[int]:
    """
    Prompt user for menu choice and validate it's an integer between 1 and max_choice.

    Args:
        max_choice: Maximum valid choice (default 11 for basic menu, 19 for advanced)

    Returns:
        Menu choice (1-max_choice) if valid, None if invalid
    """
    try:
        choice = int(input(prompt(f"\nEnter your choice (1-{max_choice}): ")))
        if 1 <= choice <= max_choice:
            return choice
        else:
            print(f"Invalid choice. Please enter a number between 1 and {max_choice}.")
            return None
    except ValueError:
        print("Invalid input. Please enter a number.")
        return None


def get_task_id() -> Optional[int]:
    """
    Prompt user for task ID and validate it's a positive integer.

    Returns:
        Task ID if valid, None if invalid
    """
    try:
        task_id = int(input(prompt("Enter task ID: ")))
        if task_id < 1:
            print("Error: Task ID must be positive")
            return None
        return task_id
    except ValueError:
        print("Invalid input. Please enter a valid task ID.")
        return None


def get_status_choice() -> Optional[str]:
    """
    Prompt user for status choice (c for complete, i for incomplete).

    Returns:
        'c' or 'i' if valid, None if invalid
    """
    choice = input(prompt("Mark as (c)omplete or (i)ncomplete? ")).lower().strip()
    if choice in ('c', 'i'):
        return choice
    else:
        print("Invalid choice. Please enter 'c' for complete or 'i' for incomplete.")
        return None


def get_optional_input(prompt_text: str) -> Optional[str]:
    """
    Prompt user for optional input, return None if empty.

    Args:
        prompt_text: Prompt message to display

    Returns:
        Input string if provided, None if empty
    """
    value = input(prompt(prompt_text)).strip()
    return value if value else None


def get_priority_choice() -> 'Priority':
    """
    Prompt user for priority choice (High, Medium, Low).

    Returns:
        Priority enum value (HIGH, MEDIUM, or LOW)
    """
    from src.models.enums import Priority

    print("\nPriority options:")
    print("1. High")
    print("2. Medium")
    print("3. Low")

    choice = get_menu_choice(3)

    if choice is None:
        raise ValueError("Priority selection cancelled")

    try:
        priority_map = {1: Priority.HIGH, 2: Priority.MEDIUM, 3: Priority.LOW}
        return priority_map[choice]
    except KeyError:
        raise ValueError(f"Invalid choice: {choice}. Please enter 1, 2, or 3.")


def get_tags_input(prompt_text: str = None) -> str:
    """
    Get comma-separated tags from user.

    Args:
        prompt_text: Optional prompt text (defaults to "Enter tags (comma-separated, optional): ")

    Returns:
        Comma-separated tags string (may be empty)
    """
    if prompt_text is None:
        prompt_text = "Enter tags (comma-separated, optional): "
    tags = input(prompt(prompt_text))
    return tags


def get_due_date_input() -> Optional[str]:
    """
    Get due date input from user in YYYY-MM-DD HH:MM format.

    Returns:
        Due date string in YYYY-MM-DD HH:MM format, or None if user skips
    """
    due_date_str = input(prompt("Enter due date (YYYY-MM-DD HH:MM) or press Enter to skip: ")).strip()

    if not due_date_str:
        return None

    # Validate the format by attempting to parse it
    try:
        # Try to parse the date string to validate format
        datetime.fromisoformat(due_date_str.replace(" ", "T"))
        return due_date_str
    except ValueError:
        print("Invalid date format. Please use YYYY-MM-DD HH:MM format (e.g., 2023-12-25 14:30)")
        return None


def get_recurrence_choice() -> Tuple['RecurrenceType', Optional[int]]:
    """
    Get recurrence type and interval from user.

    Returns:
        Tuple of (RecurrenceType, interval_days for custom recurrence)
    """
    from src.models.enums import RecurrenceType

    print("\nRecurrence options:")
    print("1. No recurrence")
    print("2. Daily")
    print("3. Weekly")
    print("4. Custom interval (in days)")

    choice = get_menu_choice(4)

    if choice is None:
        raise ValueError("Recurrence selection cancelled")

    if choice == 1:
        return RecurrenceType.NONE, None
    elif choice == 2:
        return RecurrenceType.DAILY, None
    elif choice == 3:
        return RecurrenceType.WEEKLY, None
    elif choice == 4:
        while True:
            try:
                interval = int(input(prompt("Enter interval in days: ")))
                if interval > 0:
                    return RecurrenceType.CUSTOM, interval
                else:
                    print("Interval must be a positive number.")
            except ValueError:
                print("Please enter a valid number for the interval.")
    else:
        raise ValueError(f"Invalid choice: {choice}. Please enter 1, 2, 3, or 4.")


def get_template_name() -> str:
    """
    Prompt user for template name.

    Returns:
        Template name (guaranteed non-empty after stripping)
    """
    name = input(prompt("Enter template name: ")).strip()
    return name


def get_template_title() -> str:
    """
    Prompt user for template title.

    Returns:
        Template title (guaranteed non-empty after stripping)
    """
    title = input(prompt("Enter template title: ")).strip()
    return title


def get_template_due_date_offset() -> Optional[str]:
    """
    Prompt user for template due date offset.

    Returns:
        Due date offset string (today, tomorrow, next_week, next_month) or None
    """
    print("\nTemplate due date offset options:")
    print("1. No due date")
    print("2. Today")
    print("3. Tomorrow")
    print("4. Next week")
    print("5. Next month")

    choice = get_menu_choice(5)

    if choice is None:
        raise ValueError("Template due date offset selection cancelled")

    offset_map = {
        1: None,
        2: "today",
        3: "tomorrow",
        4: "next_week",
        5: "next_month"
    }

    return offset_map[choice]
