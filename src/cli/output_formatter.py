"""Output formatting for CLI.

This module handles formatting task data for display to the user.
"""

from datetime import datetime
from src.models.task import Task
from src.cli.style import heading, separator, success, error, info


def format_task_status(task: Task) -> str:
    """Format task completion status for display."""
    is_completed = task.status == "Complete"
    return success(task.status) if is_completed else info(task.status)


def format_task_list(tasks: list[Task]) -> None:
    """
    Display all tasks in a formatted list or show empty message.
    Extended for Phase I Intermediate to show priority and tags.
    Extended for Phase I Advanced to show due dates and recurrence.

    Args:
        tasks: List of Task objects to display
    """
    print(f"\n{heading('All Tasks')}")
    print(separator(60))

    if not tasks:
        print(info("No tasks found. Add a task to get started!"))
        return

    for task in tasks:
        is_completed = task.status == "Complete"
        status_str = format_task_status(task)

        # Format priority (Phase I Intermediate)
        priority_str = f"[{task.priority.value}]" if task.priority else ""

        # Format tags (Phase I Intermediate)
        if task.tags:
            tags_str = f"Tags: {', '.join(task.tags)}"
        else:
            tags_str = ""

        # Format due date (Phase I Advanced)
        due_date_str = ""
        if task.due_date:
            due_date_str = f"Due: {task.due_date.strftime('%Y-%m-%d %H:%M')}"
            if task.is_overdue:
                due_date_str += " 🚨 OVERDUE"
            elif task.is_due_today:
                due_date_str += " 📅 TODAY"
            elif task.is_upcoming:
                due_date_str += " ⏰ UPCOMING"

        # Format recurrence (Phase I Advanced)
        recurrence_str = ""
        if task.is_recurring:
            recurrence_type = task.recurrence_rule.type.value
            if task.recurrence_rule.type.value == 'custom':
                recurrence_str = f"Recurs: every {task.recurrence_rule.interval_days} days"
            else:
                recurrence_str = f"Recurs: {recurrence_type}"

        print(f"ID: {task.id} | Title: {task.title} {priority_str}")
        if task.description:
            print(f"      {task.description}")

        if tags_str:
            print(f"      {tags_str}")

        if due_date_str:
            print(f"      {due_date_str}")

        if recurrence_str:
            print(f"      {recurrence_str}")

        print(f"      Status: {status_str}")
        print(separator(50))


def format_single_task(task: Task) -> None:
    """Display a single task with full details."""
    print(f"\n{heading('Task Details')}")
    print(separator(40))

    if not task:
        print(error("Task not found"))
        return

    print(f"ID: {task.id}")
    print(f"Title: {task.title}")
    print(f"Description: {task.description if task.description else 'None'}")

    # Display priority (Phase I Intermediate)
    print(f"Priority: {task.priority.value if task.priority else 'Not set'}")

    # Display tags (Phase I Intermediate)
    if task.tags:
        print(f"Tags: {', '.join(task.tags)}")
    else:
        print(f"Tags: None")

    # Display due date (Phase I Advanced)
    if task.due_date:
        due_date_str = f"Due: {task.due_date.strftime('%Y-%m-%d %H:%M')}"
        if task.is_overdue:
            due_date_str += " 🚨 OVERDUE"
        elif task.is_due_today:
            due_date_str += " 📅 TODAY"
        elif task.is_upcoming:
            due_date_str += " ⏰ UPCOMING"
        print(f"{due_date_str}")
    else:
        print("Due Date: None")

    # Display recurrence (Phase I Advanced)
    if task.is_recurring:
        recurrence_type = task.recurrence_rule.type.value
        if task.recurrence_rule.type.value == 'custom':
            recurrence_str = f"Recurs: every {task.recurrence_rule.interval_days} days"
        else:
            recurrence_str = f"Recurs: {recurrence_type}"
        print(f"{recurrence_str}")
    else:
        print("Recurs: No")

    print(f"Status: {task.status}")
    print(f"Created: {task.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
    if task.completed_at:
        print(f"Completed: {task.completed_at.strftime('%Y-%m-%d %H:%M:%S')}")
    print(separator(40))


def format_statistics(stats: dict) -> None:
    """Display task statistics."""
    print(f"\n{heading('Task Statistics')}")
    print(separator(50))

    if stats["total_tasks"] == 0:
        print(info("No tasks available for statistics."))
        return

    completion_rate = stats["completion_percentage"]
    print(f"Total Tasks: {stats['total_tasks']}")
    print(f"Completed: {stats['completed_tasks']}")
    print(f"Incomplete: {stats['incomplete_tasks']}")
    print(f"Completion Rate: {completion_rate}% ({stats['completed_tasks']}/{stats['total_tasks']})")
    print()

    print("By Priority:")
    print(f"  High: {stats['by_priority']['high']}")
    print(f"  Medium: {stats['by_priority']['medium']}")
    print(f"  Low: {stats['by_priority']['low']}")
    print()

    print("By Status:")
    print(f"  Complete: {stats['by_status']['complete']}")
    print(f"  Incomplete: {stats['by_status']['incomplete']}")
    print()

    print("Due Date Analytics:")
    print(f"  Overdue: {stats['overdue_count']}")
    print(f"  Due Today: {stats['due_today_count']}")
    print(f"  Upcoming (7 days): {stats['upcoming_count']}")


def format_reminders(reminders_output: str) -> None:
    """Display reminder information."""
    print(f"\n{heading('REMINDERS')}")
    print(separator(40))
    print(reminders_output)


def format_templates(templates: list) -> None:
    """Display templates for selection."""
    print(f"\n{heading('Task Templates')}")
    print(separator(40))

    if not templates:
        print(info("No templates available."))
        return

    for i, template in enumerate(templates):
        due_date_info = f" | Due: {template.due_date_offset}" if template.due_date_offset else ""
        priority_info = f" | Priority: {template.priority.value}" if template.priority else ""
        tags_info = f" | Tags: [{', '.join(template.tags)}]" if template.tags else ""

        print(f"{i + 1}. [{template.id}] {template.name} | "
              f"Title: {template.title}{due_date_info}{priority_info}{tags_info}")


def format_history(history: list) -> None:
    """Display history entries."""
    print(f"\n{heading('Recent History')}")
    print(separator(40))

    if not history:
        print(info("No history available."))
        return

    # Show last 10 entries
    recent_entries = history[-10:] if len(history) > 10 else history
    for i, entry in enumerate(recent_entries):
        timestamp_str = entry.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        print(f"{i + 1}. {entry.action.value} task {entry.task_id} at {timestamp_str}")
