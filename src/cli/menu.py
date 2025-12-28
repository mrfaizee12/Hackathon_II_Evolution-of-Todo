"""Menu handlers for the CLI.

This module contains all menu option handler functions.
"""

from src.services.task_service import TaskService
from src.cli.output_formatter import format_task_list
from src.cli.input_handler import (
    get_task_title,
    get_task_description,
    get_task_id,
    get_status_choice,
    get_optional_input
)
from src.cli.style import heading, separator, success, error, info


def view_tasks(service: TaskService) -> None:
    """
    Handler for viewing all tasks (Menu option 1).

    Args:
        service: TaskService instance
    """
    tasks = service.list_tasks()
    format_task_list(tasks)


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


def add_task(service: TaskService) -> None:
    """
    Handler for adding a new task (Menu option 2).

    Args:
        service: TaskService instance
    """
    print(f"\n{heading('--- Add New Task ---')}")
    title = get_task_title()

    # Validate title is not empty
    if not title:
        print(error("Task title cannot be empty"))
        return

    description = get_task_description()

    success_flag, message, task_id = service.add_task(title, description)
    if success_flag:
        print(f"\n{success(message)}")
    else:
        print(f"\n{error(f'Error: {message}')}")


def update_task(service: TaskService) -> None:
    """
    Handler for updating a task (Menu option 3).

    Args:
        service: TaskService instance
    """
    print(f"\n{heading('--- Update Task ---')}")
    task_id = get_task_id()

    if task_id is None:
        return

    new_title = get_optional_input("Enter new title (or press Enter to keep current): ")
    new_description = get_optional_input("Enter new description (or press Enter to keep current): ")

    if new_title is None and new_description is None:
        print(f"\n{info('No changes made.')}")
        return

    success_flag, message = service.update_task(task_id, new_title, new_description)
    if success_flag:
        print(f"\n{success(message)}")
    else:
        print(f"\n{error(f'Error: {message}')}")


def delete_task(service: TaskService) -> None:
    """
    Handler for deleting a task (Menu option 4).

    Args:
        service: TaskService instance
    """
    print(f"\n{heading('--- Delete Task ---')}")
    task_id = get_task_id()

    if task_id is None:
        return

    success_flag, message = service.delete_task(task_id)
    if success_flag:
        print(f"\n{success(message)}")
    else:
        print(f"\n{error(f'Error: {message}')}")


def toggle_status(service: TaskService) -> None:
    """
    Handler for toggling task status (Menu option 5).

    Args:
        service: TaskService instance
    """
    print(f"\n{heading('--- Mark Task Complete/Incomplete ---')}")
    task_id = get_task_id()

    if task_id is None:
        return

    # Get current task to show status
    task = service.get_task(task_id)
    if task is None:
        print(f"\n{error(f'Task not found (ID: {task_id})')}")
        return

    print(f"Current status: {task.status}")

    choice = get_status_choice()
    if choice is None:
        return

    # Only toggle if the choice differs from current status
    should_toggle = (choice == 'c' and task.status == "Incomplete") or \
                   (choice == 'i' and task.status == "Complete")

    if should_toggle:
        success_flag, message = service.toggle_status(task_id)
        print(f"\n{success(message)}")
    else:
        print(f"\n{info(f'Task is already {task.status}.')}")


def exit_application() -> bool:
    """
    Handler for exiting the application (Menu option 6).

    Returns:
        True to signal exit
    """
    print(f"\n{info('Exiting application. All data will be lost.')}")
    print(success("Goodbye!"))
    return True
