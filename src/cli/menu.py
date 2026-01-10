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
    get_optional_input,
    get_menu_choice
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


def display_menu() -> None:
    """Display the main menu options. Updated for Phase I Advanced."""
    print(f"\n{heading('Main Menu')}")
    print(separator(40))
    print("1. View all tasks")
    print("2. Add a new task")
    print("3. Update a task")
    print("4. Delete a task")
    print("5. Mark task complete/incomplete")
    print("6. Exit")
    print("7. Update task priority [NEW]")
    print("8. Manage task tags [NEW]")
    print("9. Search tasks [NEW]")
    print("10. Filter tasks [NEW]")
    print("11. Sort tasks [NEW]")
    print("12. Set task due date [ADVANCED]")
    print("13. Clear task due date [ADVANCED]")
    print("14. Set task recurrence [ADVANCED]")
    print("15. Clear task recurrence [ADVANCED]")
    print("16. View statistics [ADVANCED]")
    print("17. View reminders [ADVANCED]")
    print("18. Manage templates [ADVANCED]")
    print("19. Undo last action [ADVANCED]")
    print(separator(40))


def update_task_priority(service: TaskService) -> None:
    """
    Handler for updating task priority (Menu option 7) - New for Phase I Intermediate.

    Args:
        service: TaskService instance
    """
    print(f"\n{heading('--- Update Task Priority ---')}")
    task_id = get_task_id()

    if task_id is None:
        return

    task = service.get_task(task_id)
    if task is None:
        print(f"\n{error(f'Task not found (ID: {task_id})')}")
        return

    print(f"Current priority: {task.priority.value}")

    try:
        from src.cli.input_handler import get_priority_choice
        new_priority = get_priority_choice()
        success_flag, message = service.update_task_priority(task_id, new_priority)
        if success_flag:
            print(f"\n{success(message)}")
        else:
            print(f"\n{error(f'Error: {message}')}")
    except ValueError as e:
        print(f"\n{error(f'{e}')}")


def manage_task_tags(service: TaskService) -> None:
    """
    Handler for managing task tags (Menu option 8) - New for Phase I Intermediate.

    Args:
        service: TaskService instance
    """
    print(f"\n{heading('--- Manage Task Tags ---')}")
    task_id = get_task_id()

    if task_id is None:
        return

    task = service.get_task(task_id)
    if task is None:
        print(f"\n{error(f'Task not found (ID: {task_id})')}")
        return

    print(f"\nCurrent tags: {', '.join(task.tags) if task.tags else 'None'}")
    print("\nAction:")
    print("1. Add tags")
    print("2. Remove tag")
    print("3. Replace all tags")
    print("4. Cancel")

    choice = get_menu_choice()
    if choice is None:
        return

    if choice == 1:
        add_tags_to_task(service, task_id)
    elif choice == 2:
        remove_tag_from_task(service, task_id)
    elif choice == 3:
        replace_task_tags(service, task_id)
    else:
        print(f"\n{info('Action cancelled.')}")
    return


def add_tags_to_task(service: TaskService, task_id: int) -> None:
    """Helper function to add tags to a task."""
    from src.cli.input_handler import get_tags_input
    from src.utils.validators import validate_tags

    tags_str = get_tags_input("Enter tags to add (comma-separated): ")
    if tags_str is None:
        print(f"\n{info('Cancelled.')}")
        return

    # Parse tags
    tags = [tag.strip() for tag in tags_str.split(',') if tag.strip()]

    if not tags:
        print(f"\n{info('Cancelled.')}")
        return

    # Validate tags
    is_valid, error_msg = validate_tags(tags)
    if not is_valid:
        print(f"\n{error(error_msg)}")
        return

    # Get existing tags and add new ones
    task = service.get_task(task_id)
    existing_tags = task.tags.copy()

    # Add tags that aren't already present
    for tag in tags:
        if tag not in existing_tags:
            existing_tags.append(tag)

    success_flag, message = service.update_task_tags(task_id, existing_tags)
    if success_flag:
        print(f"\n{success(message)}")
    else:
        print(f"\n{error(f'Error: {message}')}")


def remove_tag_from_task(service: TaskService, task_id: int) -> None:
    """Helper function to remove a tag from a task."""
    from src.cli.input_handler import get_optional_input

    if not service.get_task(task_id):
        print(f"\n{error(f'Task not found (ID: {task_id})')}")
        return

    task = service.get_task(task_id)
    print(f"Current tags: {', '.join(task.tags) if task.tags else 'None'}")

    tag = get_optional_input("Enter tag to remove: ").strip()

    if not tag:
        print(f"\n{info('Cancelled.')}")
        return

    if tag not in task.tags:
        error_msg = f"Tag '{tag}' not found in task."
        print(f"\n{error(error_msg)}")
        return

    updated_tags = [t for t in task.tags if t != tag]

    success_flag, message = service.update_task_tags(task_id, updated_tags)
    if success_flag:
        print(f"\n{success(message)}")
    else:
        print(f"\n{error(f'Error: {message}')}")


def replace_task_tags(service: TaskService, task_id: int) -> None:
    """Helper function to replace all tags on a task."""
    from src.cli.input_handler import get_tags_input
    from src.utils.validators import validate_tags

    tags_str = get_tags_input("Enter new tags (comma-separated, replaces all): ")
    if tags_str is None:
        print(f"\n{info('Cancelled.')}")
        return

    # Parse tags
    tags = [tag.strip() for tag in tags_str.split(',') if tag.strip()]

    if not tags:
        print(f"\n{info('Cancelled.')}")
        return

    is_valid, error_msg = validate_tags(tags)
    if not is_valid:
        print(f"\n{error(error_msg)}")
        return

    success_flag, message = service.update_task_tags(task_id, tags)
    if success_flag:
        print(f"\n{success(message)}")
    else:
        print(f"\n{error(f'Error: {message}')}")


def search_tasks(service: TaskService) -> None:
    """
    Handler for searching tasks (Menu option 9) - New for Phase I Intermediate.

    Args:
        service: TaskService instance
    """
    print(f"\n{heading('--- Search Tasks ---')}")
    keyword = get_optional_input("Enter search keyword (press Enter to show all tasks): ")
    if keyword is None:
        keyword = ""

    matching_tasks = service.search_tasks(keyword)
    format_task_list(matching_tasks)


def filter_tasks(service: TaskService) -> None:
    """
    Handler for filtering tasks (Menu option 10) - New for Phase I Intermediate.

    Args:
        service: TaskService instance
    """
    from src.cli.input_handler import get_menu_choice
    from src.models.enums import FilterStatus, Priority

    print(f"\n{heading('--- Filter Tasks ---')}")

    print("\nFilter by status:")
    print("1. All")
    print("2. Complete")
    print("3. Incomplete")
    status_choice = get_menu_choice()
    status_filter = FilterStatus.ALL
    if status_choice == 2:
        status_filter = FilterStatus.COMPLETE
    elif status_choice == 3:
        status_filter = FilterStatus.INCOMPLETE

    print("\nFilter by priority:")
    print("1. All")
    print("2. High")
    print("3. Medium")
    print("4. Low")
    priority_choice = get_menu_choice()
    priority_filter = None
    if priority_choice == 2:
        priority_filter = Priority.HIGH
    elif priority_choice == 3:
        priority_filter = Priority.MEDIUM
    elif priority_choice == 4:
        priority_filter = Priority.LOW

    print("\nFilter by tag (optional, press Enter to skip):")
    all_tasks = service.list_tasks()
    all_tags = set()
    for task in all_tasks:
        all_tags.update(task.tags)

    if not all_tags:
        print(f"{info('No tags available to filter.')}")
        tag_filter = None
    else:
        print(f"Available tags: {', '.join(sorted(all_tags))}")
        tag_filter = get_optional_input("Select tag: ")

    # Apply filters
    filtered_tasks = service.filter_tasks(
        status_filter=status_filter,
        priority_filter=priority_filter,
        tag_filter=tag_filter
    )

    print(f"\n{heading('[Filtered Results]')}")
    format_task_list(filtered_tasks)


def sort_tasks(service: TaskService) -> None:
    """
    Handler for sorting tasks (Menu option 11) - New for Phase I Intermediate.

    Args:
        service: TaskService instance
    """
    from src.cli.input_handler import get_menu_choice
    from src.models.enums import SortBy

    print(f"\n{heading('--- Sort Tasks ---')}")

    print("\nSort by:")
    print("1. Title (A-Z)")
    print("2. Title (Z-A)")
    print("3. Priority (High to Low)")
    print("4. Priority (Low to High)")
    choice = get_menu_choice()
    sort_by = SortBy.TITLE_ASC
    if choice == 1:
        sort_by = SortBy.TITLE_ASC
    elif choice == 2:
        sort_by = SortBy.TITLE_DESC
    elif choice == 3:
        sort_by = SortBy.PRIORITY_HIGH_LOW
    elif choice == 4:
        sort_by = SortBy.PRIORITY_LOW_HIGH
    else:
        print(f"\n{error('Invalid choice.')}")
        return

    sorted_tasks = service.sort_tasks(service.list_tasks(), sort_by)
    print(f"\n{heading('[Sorted Results]')}")
    format_task_list(sorted_tasks)


def set_task_due_date(service: TaskService) -> None:
    """
    Handler for setting task due date (Menu option 12) - New for Phase I Advanced.

    Args:
        service: TaskService instance
    """
    print(f"\n{heading('--- Set Task Due Date ---')}")
    task_id = get_task_id()

    if task_id is None:
        return

    task = service.get_task(task_id)
    if task is None:
        print(f"\n{error(f'Task not found (ID: {task_id})')}")
        return

    print(f"Current due date: {task.due_date.strftime('%Y-%m-%d %H:%M') if task.due_date else 'None'}")

    from src.cli.input_handler import get_due_date_input
    due_date_str = get_due_date_input()
    if due_date_str:
        success_flag, message = service.set_due_date(task_id, due_date_str)
        if success_flag:
            print(f"\n{success(message)}")
        else:
            print(f"\n{error(f'Error: {message}')}")


def clear_task_due_date(service: TaskService) -> None:
    """
    Handler for clearing task due date (Menu option 13) - New for Phase I Advanced.

    Args:
        service: TaskService instance
    """
    print(f"\n{heading('--- Clear Task Due Date ---')}")
    task_id = get_task_id()

    if task_id is None:
        return

    task = service.get_task(task_id)
    if task is None:
        print(f"\n{error(f'Task not found (ID: {task_id})')}")
        return

    if task.due_date is None:
        print(f"\n{info('Task already has no due date.')}")
        return

    print(f"Current due date: {task.due_date.strftime('%Y-%m-%d %H:%M')}")
    confirm = input(f"\n{info('Are you sure you want to clear the due date? (y/N): ')}").lower().strip()

    if confirm in ['y', 'yes']:
        success_flag, message = service.clear_due_date(task_id)
        if success_flag:
            print(f"\n{success(message)}")
        else:
            print(f"\n{error(f'Error: {message}')}")
    else:
        print(f"\n{info('Action cancelled.')}")

def set_task_recurrence(service: TaskService) -> None:
    """
    Handler for setting task recurrence (Menu option 14) - New for Phase I Advanced.

    Args:
        service: TaskService instance
    """
    print(f"\n{heading('--- Set Task Recurrence ---')}")
    task_id = get_task_id()

    if task_id is None:
        return

    task = service.get_task(task_id)
    if task is None:
        print(f"\n{error(f'Task not found (ID: {task_id})')}")
        return

    print(f"Current recurrence: {task.recurrence_rule.type.value}")
    if task.recurrence_rule.type.value == 'custom':
        print(f"Current interval: {task.recurrence_rule.interval_days} days")

    from src.cli.input_handler import get_recurrence_choice
    try:
        recurrence_type, interval_days = get_recurrence_choice()
        success_flag, message = service.set_recurrence_rule(task_id, recurrence_type, interval_days)
        if success_flag:
            print(f"\n{success(message)}")
        else:
            print(f"\n{error(f'Error: {message}')}")
    except ValueError as e:
        print(f"\n{error(f'{e}')}")


def clear_task_recurrence(service: TaskService) -> None:
    """
    Handler for clearing task recurrence (Menu option 15) - New for Phase I Advanced.

    Args:
        service: TaskService instance
    """
    print(f"\n{heading('--- Clear Task Recurrence ---')}")
    task_id = get_task_id()

    if task_id is None:
        return

    task = service.get_task(task_id)
    if task is None:
        print(f"\n{error(f'Task not found (ID: {task_id})')}")
        return

    if task.recurrence_rule.type.value == 'none':
        print(f"\n{info('Task already has no recurrence.')}")
        return

    print(f"Current recurrence: {task.recurrence_rule.type.value}")
    confirm = input(f"\n{info('Are you sure you want to clear the recurrence? (y/N): ')}").lower().strip()

    if confirm in ['y', 'yes']:
        success_flag, message = service.clear_recurrence_rule(task_id)
        if success_flag:
            print(f"\n{success(message)}")
        else:
            print(f"\n{error(f'Error: {message}')}")
    else:
        print(f"\n{info('Action cancelled.')}")

def view_statistics(service: TaskService) -> None:
    """
    Handler for viewing task statistics (Menu option 16) - New for Phase I Advanced.

    Args:
        service: TaskService instance
    """
    print(f"\n{heading('--- Task Statistics ---')}")
    stats = service.get_statistics()

    print(f"\nTotal Tasks: {stats['total_tasks']}")
    print(f"Completed: {stats['completed_tasks']}")
    print(f"Incomplete: {stats['incomplete_tasks']}")
    print(f"Completion Rate: {stats['completion_percentage']}%")
    print(f"\nBy Priority:")
    print(f"  High: {stats['by_priority']['high']}")
    print(f"  Medium: {stats['by_priority']['medium']}")
    print(f"  Low: {stats['by_priority']['low']}")
    print(f"\nBy Status:")
    print(f"  Complete: {stats['by_status']['complete']}")
    print(f"  Incomplete: {stats['by_status']['incomplete']}")
    print(f"\nDue Date Analytics:")
    print(f"  Overdue: {stats['overdue_count']}")
    print(f"  Due Today: {stats['due_today_count']}")
    print(f"  Upcoming (7 days): {stats['upcoming_count']}")


def view_reminders(service: TaskService) -> None:
    """
    Handler for viewing reminders (Menu option 17) - New for Phase I Advanced.

    Args:
        service: TaskService instance
    """
    print(f"\n{heading('--- Reminders ---')}")
    from src.services.reminder_service import ReminderService
    reminder_service = ReminderService()
    tasks = service.list_tasks()
    summary = reminder_service.evaluate_reminders(tasks)

    if summary.has_overdue:
        print(f"\n{error('🚨 OVERDUE TASKS:')}")
        for task in summary.overdue:
            print(f"  - ID: {task.id} | {task.title} | Due: {task.due_date.strftime('%Y-%m-%d %H:%M')}")

    if summary.has_due_today:
        print(f"\n{info('📅 DUE TODAY:')}")
        for task in summary.due_today:
            print(f"  - ID: {task.id} | {task.title} | Due: {task.due_date.strftime('%Y-%m-%d %H:%M')}")

    if summary.has_upcoming:
        print(f"\n{success('🔔 UPCOMING TASKS:')}")
        for task in summary.upcoming:
            print(f"  - ID: {task.id} | {task.title} | Due: {task.due_date.strftime('%Y-%m-%d %H:%M')}")

    if not summary.total_count:
        print(f"\n{success('✅ No overdue, due today, or upcoming tasks to display.')}")

def manage_templates(service: TaskService) -> None:
    """
    Handler for managing templates (Menu option 18) - New for Phase I Advanced.

    Args:
        service: TaskService instance
    """
    print(f"\n{heading('--- Template Management ---')}")
    print("Template management is not fully implemented in this version.")
    print("This would include options to create, view, edit, and use templates.")


def undo_last_action(service: TaskService) -> None:
    """
    Handler for undoing the last action (Menu option 19) - New for Phase I Advanced.

    Args:
        service: TaskService instance
    """
    print(f"\n{heading('--- Undo Last Action ---')}")
    success_flag, message = service.undo_last_action()
    if success_flag:
        print(f"\n{success(message)}")
    else:
        print(f"\n{error(f'Error: {message}')}")
