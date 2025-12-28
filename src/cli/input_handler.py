"""Input handling for the CLI.

This module handles user input collection and validation.
"""

from typing import Optional
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


def get_menu_choice() -> Optional[int]:
    """
    Prompt user for menu choice and validate it's an integer between 1-6.

    Returns:
        Menu choice (1-6) if valid, None if invalid
    """
    try:
        choice = int(input(prompt("\nEnter your choice (1-6): ")))
        if 1 <= choice <= 6:
            return choice
        else:
            print("Invalid choice. Please enter a number between 1 and 6.")
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
