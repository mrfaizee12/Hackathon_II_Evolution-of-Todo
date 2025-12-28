"""Unit tests for the Task model."""

import pytest
from src.models.task import Task


def test_task_creation_with_all_fields():
    """Test creating a task with all fields specified."""
    task = Task(id=1, title="Test Task", description="Test Description", status="Incomplete")
    assert task.id == 1
    assert task.title == "Test Task"
    assert task.description == "Test Description"
    assert task.status == "Incomplete"


def test_task_creation_with_defaults():
    """Test creating a task with default values."""
    task = Task(id=1, title="Test Task")
    assert task.id == 1
    assert task.title == "Test Task"
    assert task.description == ""
    assert task.status == "Incomplete"


def test_task_empty_title_raises_valueerror():
    """Test that empty title raises ValueError."""
    with pytest.raises(ValueError, match="Task title cannot be empty"):
        Task(id=1, title="")


def test_task_whitespace_title_raises_valueerror():
    """Test that whitespace-only title raises ValueError."""
    with pytest.raises(ValueError, match="Task title cannot be empty"):
        Task(id=1, title="   ")


def test_task_invalid_status_raises_valueerror():
    """Test that invalid status raises ValueError."""
    with pytest.raises(ValueError, match="Invalid status"):
        Task(id=1, title="Test", status="Invalid")


def test_task_complete_status():
    """Test creating a task with Complete status."""
    task = Task(id=1, title="Test", status="Complete")
    assert task.status == "Complete"


def test_task_str_representation():
    """Test __str__ method."""
    task = Task(id=1, title="Test Task", status="Incomplete")
    expected = "ID: 1 | Title: Test Task | Status: Incomplete"
    assert str(task) == expected


def test_task_repr_representation():
    """Test __repr__ method."""
    task = Task(id=1, title="Test Task", description="Desc", status="Complete")
    expected = "Task(id=1, title='Test Task', description='Desc', status=Complete)"
    assert repr(task) == expected
