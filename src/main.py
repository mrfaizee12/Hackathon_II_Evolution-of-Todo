"""Main entry point for the Todo Application - Phase I.

This module contains the main application loop and menu dispatch logic.
"""

import sys
from src.services.task_service import TaskService
from src.cli.menu import (
    display_menu,
    view_tasks,
    add_task,
    update_task,
    delete_task,
    toggle_status,
    exit_application
)
from src.cli.input_handler import get_menu_choice
from src.cli.style import heading, error


def check_python_version():
    """
    Check if Python version is 3.11 or higher.

    Exits the application if version requirement is not met.
    """
    if sys.version_info < (3, 11):
        print(error("Python 3.11 or higher is required."))
        print(f"Current version: {sys.version}")
        print("Please upgrade Python and try again.")
        sys.exit(1)


def main():
    """
    Main application entry point.

    Initializes the task service, displays welcome message,
    and runs the main menu loop until user exits.
    """
    # Check Python version first
    check_python_version()

    # Initialize service
    service = TaskService()

    # Display welcome message
    print(heading("Welcome to Todo Application - Phase I"))

    # Menu dispatch table
    handlers = {
        1: lambda: view_tasks(service),
        2: lambda: add_task(service),
        3: lambda: update_task(service),
        4: lambda: delete_task(service),
        5: lambda: toggle_status(service),
        6: lambda: exit_application()
    }

    # Main menu loop
    while True:
        display_menu()
        choice = get_menu_choice()

        if choice is None:
            # Invalid input, continue loop
            continue

        if choice in handlers:
            result = handlers[choice]()
            # If exit_application returns True, break the loop
            if result is True:
                break
        else:
            # This should not happen due to validation in get_menu_choice
            print(error("Invalid choice. Please enter a number between 1 and 6."))


if __name__ == "__main__":
    main()
