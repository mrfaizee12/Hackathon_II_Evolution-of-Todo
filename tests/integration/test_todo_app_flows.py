"""Integration tests for complete user story flows."""

import pytest
from src.services.task_service import TaskService


def test_us1_view_empty_and_populated_list():
    """Test US1: View empty list, add tasks, view populated list."""
    service = TaskService()

    # View empty list
    tasks = service.list_tasks()
    assert len(tasks) == 0

    # Add tasks
    service.add_task("Task 1", "Description 1")
    service.add_task("Task 2", "Description 2")
    service.add_task("Task 3", "Description 3")

    # View populated list
    tasks = service.list_tasks()
    assert len(tasks) == 3
    assert all(task.status == "Incomplete" for task in tasks)
    assert tasks[0].title == "Task 1"
    assert tasks[1].title == "Task 2"
    assert tasks[2].title == "Task 3"


def test_us2_add_task_with_title_and_description():
    """Test US2: Add task with title and description."""
    service = TaskService()

    success, message, task_id = service.add_task("Buy groceries", "Milk, eggs, bread")
    assert success is True
    assert task_id == 1

    task = service.get_task(task_id)
    assert task.title == "Buy groceries"
    assert task.description == "Milk, eggs, bread"
    assert task.status == "Incomplete"


def test_us2_add_task_with_title_only():
    """Test US2: Add task with title only (no description)."""
    service = TaskService()

    success, message, task_id = service.add_task("Call dentist")
    assert success is True

    task = service.get_task(task_id)
    assert task.title == "Call dentist"
    assert task.description == ""
    assert task.status == "Incomplete"


def test_us2_reject_empty_title():
    """Test US2: Reject task with empty title."""
    service = TaskService()

    success, message, task_id = service.add_task("")
    assert success is False
    assert task_id == -1
    assert "cannot be empty" in message


def test_us3_mark_complete_and_incomplete():
    """Test US3: Mark task complete, then mark incomplete."""
    service = TaskService()

    # Add task
    success, message, task_id = service.add_task("Test Task")
    task = service.get_task(task_id)
    assert task.status == "Incomplete"

    # Mark complete
    success, message = service.toggle_status(task_id)
    assert success is True
    assert "Complete" in message
    task = service.get_task(task_id)
    assert task.status == "Complete"

    # Mark incomplete
    success, message = service.toggle_status(task_id)
    assert success is True
    assert "Incomplete" in message
    task = service.get_task(task_id)
    assert task.status == "Incomplete"


def test_us3_invalid_id_error():
    """Test US3: Error when marking non-existent task."""
    service = TaskService()

    success, message = service.toggle_status(999)
    assert success is False
    assert "not found" in message


def test_us4_update_title():
    """Test US4: Update task title."""
    service = TaskService()

    success, message, task_id = service.add_task("Old Title", "Description")
    success, message = service.update_task(task_id, title="New Title")
    assert success is True

    task = service.get_task(task_id)
    assert task.title == "New Title"
    assert task.description == "Description"  # Unchanged


def test_us4_update_description():
    """Test US4: Update task description."""
    service = TaskService()

    success, message, task_id = service.add_task("Title", "Old Description")
    success, message = service.update_task(task_id, description="New Description")
    assert success is True

    task = service.get_task(task_id)
    assert task.title == "Title"  # Unchanged
    assert task.description == "New Description"


def test_us4_update_invalid_id_error():
    """Test US4: Error when updating non-existent task."""
    service = TaskService()

    success, message = service.update_task(999, title="New Title")
    assert success is False
    assert "not found" in message


def test_us4_empty_title_error():
    """Test US4: Error when updating to empty title."""
    service = TaskService()

    success, message, task_id = service.add_task("Title")
    success, message = service.update_task(task_id, title="")
    assert success is False
    assert "cannot be empty" in message


def test_us5_delete_task():
    """Test US5: Delete task and verify removal."""
    service = TaskService()

    # Add task
    success, message, task_id = service.add_task("Test Task")
    assert service.get_task(task_id) is not None

    # Delete task
    success, message = service.delete_task(task_id)
    assert success is True
    assert "deleted successfully" in message

    # Verify deletion
    assert service.get_task(task_id) is None
    tasks = service.list_tasks()
    assert len(tasks) == 0


def test_us5_delete_invalid_id_error():
    """Test US5: Error when deleting non-existent task."""
    service = TaskService()

    success, message = service.delete_task(999)
    assert success is False
    assert "not found" in message


def test_complete_workflow():
    """Test complete workflow: add, view, update, toggle, delete."""
    service = TaskService()

    # Start with empty list
    assert len(service.list_tasks()) == 0

    # Add three tasks
    _, _, id1 = service.add_task("Task 1", "Desc 1")
    _, _, id2 = service.add_task("Task 2", "Desc 2")
    _, _, id3 = service.add_task("Task 3", "Desc 3")

    # Verify all added
    tasks = service.list_tasks()
    assert len(tasks) == 3

    # Update task 2
    service.update_task(id2, title="Updated Task 2")
    task2 = service.get_task(id2)
    assert task2.title == "Updated Task 2"

    # Mark task 1 complete
    service.toggle_status(id1)
    task1 = service.get_task(id1)
    assert task1.status == "Complete"

    # Delete task 3
    service.delete_task(id3)
    assert len(service.list_tasks()) == 2

    # Verify remaining tasks
    tasks = service.list_tasks()
    assert tasks[0].id == id1
    assert tasks[0].status == "Complete"
    assert tasks[1].id == id2
    assert tasks[1].title == "Updated Task 2"
