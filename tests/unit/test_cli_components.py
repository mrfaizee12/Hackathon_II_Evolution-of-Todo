"""Unit tests for CLI components (input handlers and output formatters)."""

import pytest
from io import StringIO
import sys
from src.cli.output_formatter import format_task_list
from src.models.task import Task


def test_format_task_list_empty(capsys):
    """Test formatting empty task list."""
    format_task_list([])
    captured = capsys.readouterr()
    assert "--- All Tasks ---" in captured.out
    assert "No tasks found" in captured.out


def test_format_task_list_single_task(capsys):
    """Test formatting single task."""
    tasks = [Task(id=1, title="Test Task", description="Test Desc", status="Incomplete")]
    format_task_list(tasks)
    captured = capsys.readouterr()
    assert "ID: 1" in captured.out
    assert "Test Task" in captured.out
    assert "Incomplete" in captured.out
    assert "Test Desc" in captured.out


def test_format_task_list_multiple_tasks(capsys):
    """Test formatting multiple tasks."""
    tasks = [
        Task(id=1, title="Task 1", description="Desc 1", status="Incomplete"),
        Task(id=2, title="Task 2", description="Desc 2", status="Complete"),
        Task(id=3, title="Task 3", description="", status="Incomplete"),
    ]
    format_task_list(tasks)
    captured = capsys.readouterr()
    output = captured.out
    assert "ID: 1" in output
    assert "Task 1" in output
    assert "ID: 2" in output
    assert "Task 2" in output
    assert "Complete" in output
    assert "ID: 3" in output
    assert "Task 3" in output


def test_format_task_list_empty_description(capsys):
    """Test formatting task with empty description."""
    tasks = [Task(id=1, title="Test Task", description="", status="Incomplete")]
    format_task_list(tasks)
    captured = capsys.readouterr()
    # Should display "Description: " even if empty
    assert "Description:" in captured.out
