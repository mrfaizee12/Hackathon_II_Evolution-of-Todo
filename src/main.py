"""Main entry point for the Todo Application - Phase I Advanced.

This module contains the main application loop and menu dispatch logic.
"""

import sys
from src.services.task_service import TaskService
from src.services.reminder_service import ReminderService
from src.services.template_service import TemplateService
from src.cli.menu import (
    display_menu,
    view_tasks,
    add_task,
    update_task,
    delete_task,
    toggle_status,
    update_task_priority,
    manage_task_tags,
    search_tasks,
    filter_tasks,
    sort_tasks,
    exit_application,
    set_task_due_date,
    clear_task_due_date,
    set_task_recurrence,
    clear_task_recurrence,
    view_statistics,
    view_reminders,
    manage_templates,
    undo_last_action
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

    # Initialize services
    service = TaskService()
    reminder_service = ReminderService()
    template_service = TemplateService()

    # Display welcome message
    print(heading("Welcome to Todo Application - Phase I Advanced"))

    # Check for reminders at startup
    tasks = service.list_tasks()
    reminder_summary = reminder_service.evaluate_reminders(tasks)
    if reminder_summary.total_count > 0:
        print("\n🔔 REMINDERS AT STARTUP:")
        reminder_output = reminder_service.display_reminders(reminder_summary)
        print(reminder_output)

    # Menu dispatch table
    handlers = {
        1: lambda: view_tasks(service),
        2: lambda: add_task(service),
        3: lambda: update_task(service),
        4: lambda: delete_task(service),
        5: lambda: toggle_status(service),
        6: lambda: exit_application(),
        7: lambda: update_task_priority(service),
        8: lambda: manage_task_tags(service),
        9: lambda: search_tasks(service),
        10: lambda: filter_tasks(service),
        11: lambda: sort_tasks(service),
        12: lambda: set_task_due_date(service),
        13: lambda: clear_task_due_date(service),
        14: lambda: set_task_recurrence(service),
        15: lambda: clear_task_recurrence(service),
        16: lambda: view_statistics(service),
        17: lambda: view_reminders(service),
        18: lambda: manage_templates(service),
        19: lambda: undo_last_action(service)
    }

    # Main menu loop
    while True:
        display_menu()
        choice = get_menu_choice(19)  # Updated max choice for Phase I Advanced

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
            print(error("Invalid choice. Please enter a number between 1 and 19."))


if __name__ == "__main__":
    main()
