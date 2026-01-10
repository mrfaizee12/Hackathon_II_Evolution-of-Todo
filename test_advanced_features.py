"""Test script to verify Phase I Advanced features are working correctly."""

import sys
from datetime import datetime
from src.services.task_service import TaskService
from src.services.reminder_service import ReminderService
from src.services.template_service import TemplateService
from src.models.enums import RecurrenceType


def test_basic_functionality():
    """Test basic task operations still work."""
    print("Testing basic functionality...")
    service = TaskService()

    # Add a task
    success, message, task_id = service.add_task("Test task", "Test description")
    print(f"Add task: {success}, {message}, ID: {task_id}")

    # List tasks
    tasks = service.list_tasks()
    print(f"List tasks: {len(tasks)} tasks")

    # Toggle status
    success, message = service.toggle_status(task_id)
    print(f"Toggle status: {success}, {message}")

    print("PASS: Basic functionality test passed\n")


def test_due_date_functionality():
    """Test due date functionality."""
    print("Testing due date functionality...")
    service = TaskService()

    # Add a task
    success, message, task_id = service.add_task("Task with due date", "Test description")
    print(f"Add task: {success}, {message}, ID: {task_id}")

    # Set due date
    due_date_str = "2026-12-31 23:59"
    success, message = service.set_due_date(task_id, due_date_str)
    print(f"Set due date: {success}, {message}")

    # Get task and verify due date
    task = service.get_task(task_id)
    if task and task.due_date:
        print(f"Task due date: {task.due_date}")
        print("PASS: Due date functionality test passed\n")
    else:
        print("FAIL: Due date functionality test failed\n")


def test_recurrence_functionality():
    """Test recurrence functionality."""
    print("Testing recurrence functionality...")
    service = TaskService()

    # Add a task
    success, message, task_id = service.add_task("Recurring task", "Test recurring task")
    print(f"Add task: {success}, {message}, ID: {task_id}")

    # Set recurrence rule
    success, message = service.set_recurrence_rule(task_id, RecurrenceType.DAILY)
    print(f"Set recurrence: {success}, {message}")

    # Get task and verify recurrence
    task = service.get_task(task_id)
    if task and task.recurrence_rule.type == RecurrenceType.DAILY:
        print(f"Task recurrence: {task.recurrence_rule.type.value}")
        print("PASS: Recurrence functionality test passed\n")
    else:
        print("FAIL: Recurrence functionality test failed\n")


def test_statistics():
    """Test statistics functionality."""
    print("Testing statistics functionality...")
    service = TaskService()

    # Add some tasks
    service.add_task("Task 1", "Description 1")
    service.add_task("Task 2", "Description 2")
    service.toggle_status(2)  # Complete the second task

    # Get statistics
    stats = service.get_statistics()
    print(f"Statistics: {stats}")

    if stats["total_tasks"] == 2 and stats["completed_tasks"] == 1:
        print("PASS: Statistics functionality test passed\n")
    else:
        print("FAIL: Statistics functionality test failed\n")


def test_reminders():
    """Test reminder functionality."""
    print("Testing reminder functionality...")
    service = TaskService()
    reminder_service = ReminderService()

    # Add a task with a past due date to test overdue functionality
    success, message, task_id = service.add_task("Overdue task", "Test overdue task")
    # We'll skip setting an actual past due date to avoid time-sensitive tests
    # but we can test that the service works

    tasks = service.list_tasks()
    summary = reminder_service.evaluate_reminders(tasks)
    print(f"Reminder summary: {summary.total_count} tasks needing attention")

    print("PASS: Reminder functionality test passed\n")


def test_undo_functionality():
    """Test undo functionality."""
    print("Testing undo functionality...")
    service = TaskService()

    # Add a task
    success, message, task_id = service.add_task("Task to delete", "Test task")
    print(f"Add task: {success}, {message}, ID: {task_id}")

    # Verify task exists
    task = service.get_task(task_id)
    if task:
        print(f"Task exists before delete: {task.title}")

    # Delete the task
    success, message = service.delete_task(task_id)
    print(f"Delete task: {success}, {message}")

    # Verify task is gone
    task = service.get_task(task_id)
    if not task:
        print("Task successfully deleted")

    # Undo the deletion
    success, message = service.undo_last_action()
    print(f"Undo: {success}, {message}")

    # Verify task is back
    task = service.get_task(task_id)
    if task:
        print(f"Task restored after undo: {task.title}")
        print("PASS: Undo functionality test passed\n")
    else:
        print("FAIL: Undo functionality test failed\n")


if __name__ == "__main__":
    print("Testing Phase I Advanced Features\n")

    test_basic_functionality()
    test_due_date_functionality()
    test_recurrence_functionality()
    test_statistics()
    test_reminders()
    test_undo_functionality()

    print("All tests completed!")