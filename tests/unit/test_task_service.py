"""Unit tests for the TaskService."""

import pytest
from src.services.task_service import TaskService


def test_add_task_success():
    """Test successful task addition."""
    service = TaskService()
    success, message, task_id = service.add_task("Test Task", "Test Description")
    assert success is True
    assert task_id == 1
    assert "Task added successfully" in message


def test_add_task_empty_title():
    """Test adding task with empty title fails."""
    service = TaskService()
    success, message, task_id = service.add_task("", "Description")
    assert success is False
    assert task_id == -1
    assert "cannot be empty" in message


def test_add_task_whitespace_title():
    """Test adding task with whitespace title fails."""
    service = TaskService()
    success, message, task_id = service.add_task("   ", "Description")
    assert success is False
    assert task_id == -1


def test_add_task_without_description():
    """Test adding task without description."""
    service = TaskService()
    success, message, task_id = service.add_task("Test Task")
    assert success is True
    assert task_id == 1


def test_list_tasks_empty():
    """Test listing tasks when none exist."""
    service = TaskService()
    tasks = service.list_tasks()
    assert tasks == []


def test_list_tasks_with_items():
    """Test listing tasks after adding some."""
    service = TaskService()
    service.add_task("Task 1", "Desc 1")
    service.add_task("Task 2", "Desc 2")
    service.add_task("Task 3", "Desc 3")
    tasks = service.list_tasks()
    assert len(tasks) == 3
    assert tasks[0].title == "Task 1"
    assert tasks[1].title == "Task 2"
    assert tasks[2].title == "Task 3"


def test_get_task_exists():
    """Test getting an existing task."""
    service = TaskService()
    success, message, task_id = service.add_task("Test Task")
    task = service.get_task(task_id)
    assert task is not None
    assert task.id == task_id
    assert task.title == "Test Task"


def test_get_task_not_found():
    """Test getting a non-existent task."""
    service = TaskService()
    task = service.get_task(999)
    assert task is None


def test_update_task_title():
    """Test updating task title."""
    service = TaskService()
    success, message, task_id = service.add_task("Old Title", "Description")
    success, message = service.update_task(task_id, title="New Title")
    assert success is True
    assert "updated successfully" in message
    task = service.get_task(task_id)
    assert task.title == "New Title"
    assert task.description == "Description"  # Unchanged


def test_update_task_description():
    """Test updating task description."""
    service = TaskService()
    success, message, task_id = service.add_task("Title", "Old Desc")
    success, message = service.update_task(task_id, description="New Desc")
    assert success is True
    task = service.get_task(task_id)
    assert task.title == "Title"  # Unchanged
    assert task.description == "New Desc"


def test_update_task_both_fields():
    """Test updating both title and description."""
    service = TaskService()
    success, message, task_id = service.add_task("Old Title", "Old Desc")
    success, message = service.update_task(task_id, "New Title", "New Desc")
    assert success is True
    task = service.get_task(task_id)
    assert task.title == "New Title"
    assert task.description == "New Desc"


def test_update_task_not_found():
    """Test updating non-existent task."""
    service = TaskService()
    success, message = service.update_task(999, title="New Title")
    assert success is False
    assert "not found" in message


def test_update_task_empty_title():
    """Test updating with empty title fails."""
    service = TaskService()
    success, message, task_id = service.add_task("Title")
    success, message = service.update_task(task_id, title="")
    assert success is False
    assert "cannot be empty" in message


def test_update_task_no_changes():
    """Test updating with no changes."""
    service = TaskService()
    success, message, task_id = service.add_task("Title")
    success, message = service.update_task(task_id)
    assert success is True
    assert "No changes made" in message


def test_delete_task_success():
    """Test successful task deletion."""
    service = TaskService()
    success, message, task_id = service.add_task("Test Task")
    success, message = service.delete_task(task_id)
    assert success is True
    assert "deleted successfully" in message
    assert service.get_task(task_id) is None


def test_delete_task_not_found():
    """Test deleting non-existent task."""
    service = TaskService()
    success, message = service.delete_task(999)
    assert success is False
    assert "not found" in message


def test_toggle_status_incomplete_to_complete():
    """Test toggling status from Incomplete to Complete."""
    service = TaskService()
    success, message, task_id = service.add_task("Test Task")
    task = service.get_task(task_id)
    assert task.status == "Incomplete"
    success, message = service.toggle_status(task_id)
    assert success is True
    assert "Complete" in message
    task = service.get_task(task_id)
    assert task.status == "Complete"


def test_toggle_status_complete_to_incomplete():
    """Test toggling status from Complete to Incomplete."""
    service = TaskService()
    success, message, task_id = service.add_task("Test Task")
    service.toggle_status(task_id)  # Make it Complete
    success, message = service.toggle_status(task_id)  # Toggle back
    assert success is True
    assert "Incomplete" in message
    task = service.get_task(task_id)
    assert task.status == "Incomplete"


def test_toggle_status_not_found():
    """Test toggling status of non-existent task."""
    service = TaskService()
    success, message = service.toggle_status(999)
    assert success is False
    assert "not found" in message


def test_id_auto_increment():
    """Test that task IDs auto-increment."""
    service = TaskService()
    _, _, id1 = service.add_task("Task 1")
    _, _, id2 = service.add_task("Task 2")
    _, _, id3 = service.add_task("Task 3")
    assert id1 == 1
    assert id2 == 2
    assert id3 == 3


def test_id_not_reused_after_deletion():
    """Test that IDs are not reused after deletion."""
    service = TaskService()
    _, _, id1 = service.add_task("Task 1")
    _, _, id2 = service.add_task("Task 2")
    service.delete_task(id1)
    _, _, id3 = service.add_task("Task 3")
    assert id3 == 3  # Not 1, IDs never reused
