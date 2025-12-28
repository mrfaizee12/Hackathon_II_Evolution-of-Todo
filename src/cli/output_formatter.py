"""Output formatting for the CLI.

This module handles formatting task data for display to the user.
"""

from src.models.task import Task
from src.cli.style import heading, info, format_task_status, separator


def format_task_list(tasks: list[Task]) -> None:
    """
    Display all tasks in a formatted list or show empty message.

    Args:
        tasks: List of Task objects to display

    Contract:
        - If list is empty: Display "No tasks found. Add a task to get started!"
        - If list has tasks: Display each task with format:
          "ID: X | Title: Y | Status: Z"
          "Description: W"
          (blank line between tasks)
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
