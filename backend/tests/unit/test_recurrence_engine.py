from datetime import datetime, timedelta, timezone
import uuid
from unittest.mock import MagicMock, patch

import pytest
from sqlmodel import Session, SQLModel, Field

from src.models.todo import Todo, RecurrenceType
from src.services.recurrence_engine import RecurrenceEngine
from src.events.todo_events import TaskCompletedEvent
from src.utils.datetime_utils import get_utc_now


class MockTodo(SQLModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(default_factory=uuid.uuid4)
    title: str = "Test Todo"
    description: Optional[str] = None
    completed: bool = False
    priority: str = "medium"
    tags: str = ""
    due_date: Optional[datetime] = None
    recurrence_type: RecurrenceType = RecurrenceType.NONE
    recurrence_interval: Optional[int] = None
    next_occurrence: Optional[datetime] = None
    reminder_at: Optional[datetime] = None
    ai_generated: bool = False
    ai_context: Optional[str] = None
    created_at: datetime = Field(default_factory=get_utc_now)
    updated_at: datetime = Field(default_factory=get_utc_now)


@pytest.fixture
def mock_session():
    """Fixture for a mock SQLAlchemy session."""
    session = MagicMock(spec=Session)
    yield session
    session.rollback()


@pytest.fixture
def recurrence_engine(mock_session):
    """Fixture for RecurrenceEngine with a mock session factory."""
    return RecurrenceEngine(session_factory=lambda: mock_session)


@patch("backend.src.utils.datetime_utils.get_utc_now", return_value=datetime(2026, 2, 8, 12, 0, 0, tzinfo=timezone.utc))
def test_process_task_completed_event_non_recurring(mock_get_utc_now, recurrence_engine, mock_session):
    """
    Test that no new task is created for a non-recurring task.
    """
    task_id = uuid.uuid4()
    user_id = uuid.uuid4()
    event = TaskCompletedEvent(task_id=task_id, user_id=user_id, completed_at=get_utc_now(), recurrence_type="none")

    # Mock the session to return a non-recurring task
    mock_session.exec().first.return_value = MockTodo(
        id=task_id,
        user_id=user_id,
        recurrence_type=RecurrenceType.NONE,
        due_date=get_utc_now() + timedelta(days=1)
    )

    new_todo = recurrence_engine.process_task_completed_event(event)

    assert new_todo is None
    mock_session.add.assert_not_called()
    mock_session.commit.assert_not_called()


@patch("backend.src.utils.datetime_utils.get_utc_now", return_value=datetime(2026, 2, 8, 12, 0, 0, tzinfo=timezone.utc))
def test_process_task_completed_event_daily_recurring(mock_get_utc_now, recurrence_engine, mock_session):
    """
    Test that a new daily recurring task is created.
    """
    task_id = uuid.uuid4()
    user_id = uuid.uuid4()
    original_due_date = get_utc_now().replace(hour=10, minute=0, second=0, microsecond=0) # Feb 8, 10:00 UTC
    event = TaskCompletedEvent(task_id=task_id, user_id=user_id, completed_at=get_utc_now(), recurrence_type="daily")

    mock_original_todo = MockTodo(
        id=task_id,
        user_id=user_id,
        title="Daily Task",
        recurrence_type=RecurrenceType.DAILY,
        recurrence_interval=1,
        due_date=original_due_date
    )
    mock_session.exec().first.side_effect = [mock_original_todo, None] # First call for original, second for existing next occurrence

    new_todo = recurrence_engine.process_task_completed_event(event)

    assert new_todo is not None
    assert new_todo.title == "Daily Task"
    assert new_todo.completed is False
    assert new_todo.due_date == original_due_date + timedelta(days=1)
    assert new_todo.recurrence_type == RecurrenceType.DAILY
    assert new_todo.recurrence_interval == 1
    assert new_todo.next_occurrence == new_todo.due_date # For the new task, its next_occurrence is its own due_date
    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()
    mock_session.refresh.assert_called_once_with(new_todo)


@patch("backend.src.utils.datetime_utils.get_utc_now", return_value=datetime(2026, 2, 8, 12, 0, 0, tzinfo=timezone.utc))
def test_process_task_completed_event_weekly_recurring(mock_get_utc_now, recurrence_engine, mock_session):
    """
    Test that a new weekly recurring task is created.
    """
    task_id = uuid.uuid4()
    user_id = uuid.uuid4()
    original_due_date = get_utc_now().replace(hour=10, minute=0, second=0, microsecond=0) # Feb 8, 10:00 UTC
    event = TaskCompletedEvent(task_id=task_id, user_id=user_id, completed_at=get_utc_now(), recurrence_type="weekly")

    mock_original_todo = MockTodo(
        id=task_id,
        user_id=user_id,
        title="Weekly Task",
        recurrence_type=RecurrenceType.WEEKLY,
        recurrence_interval=2,
        due_date=original_due_date
    )
    mock_session.exec().first.side_effect = [mock_original_todo, None]

    new_todo = recurrence_engine.process_task_completed_event(event)

    assert new_todo is not None
    assert new_todo.title == "Weekly Task"
    assert new_todo.completed is False
    assert new_todo.due_date == original_due_date + timedelta(weeks=2)
    assert new_todo.recurrence_type == RecurrenceType.WEEKLY
    assert new_todo.recurrence_interval == 2
    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()
    mock_session.refresh.assert_called_once_with(new_todo)


@patch("backend.src.utils.datetime_utils.get_utc_now", return_value=datetime(2026, 2, 8, 12, 0, 0, tzinfo=timezone.utc))
def test_process_task_completed_event_monthly_recurring(mock_get_utc_now, recurrence_engine, mock_session):
    """
    Test that a new monthly recurring task is created (simplified calculation).
    """
    task_id = uuid.uuid4()
    user_id = uuid.uuid4()
    original_due_date = get_utc_now().replace(day=8, hour=10, minute=0, second=0, microsecond=0) # Feb 8, 10:00 UTC
    event = TaskCompletedEvent(task_id=task_id, user_id=user_id, completed_at=get_utc_now(), recurrence_type="monthly")

    mock_original_todo = MockTodo(
        id=task_id,
        user_id=user_id,
        title="Monthly Task",
        recurrence_type=RecurrenceType.MONTHLY,
        recurrence_interval=1,
        due_date=original_due_date
    )
    mock_session.exec().first.side_effect = [mock_original_todo, None]

    new_todo = recurrence_engine.process_task_completed_event(event)

    assert new_todo is not None
    assert new_todo.title == "Monthly Task"
    assert new_todo.completed is False
    assert new_todo.due_date == original_due_date + timedelta(days=30) # Simplified monthly
    assert new_todo.recurrence_type == RecurrenceType.MONTHLY
    assert new_todo.recurrence_interval == 1
    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()
    mock_session.refresh.assert_called_once_with(new_todo)


@patch("backend.src.utils.datetime_utils.get_utc_now", return_value=datetime(2026, 2, 8, 12, 0, 0, tzinfo=timezone.utc))
def test_process_task_completed_event_original_task_not_found(mock_get_utc_now, recurrence_engine, mock_session):
    """
    Test that no new task is created if the original task is not found.
    """
    task_id = uuid.uuid4()
    user_id = uuid.uuid4()
    event = TaskCompletedEvent(task_id=task_id, user_id=user_id, completed_at=get_utc_now(), recurrence_type="daily")

    mock_session.exec().first.return_value = None # Original task not found

    new_todo = recurrence_engine.process_task_completed_event(event)

    assert new_todo is None
    mock_session.add.assert_not_called()
    mock_session.commit.assert_not_called()


@patch("backend.src.utils.datetime_utils.get_utc_now", return_value=datetime(2026, 2, 8, 12, 0, 0, tzinfo=timezone.utc))
def test_process_task_completed_event_duplicate_prevention(mock_get_utc_now, recurrence_engine, mock_session):
    """
    Test that a new task is not created if a next occurrence already exists.
    """
    task_id = uuid.uuid4()
    user_id = uuid.uuid4()
    original_due_date = get_utc_now().replace(hour=10, minute=0, second=0, microsecond=0)
    event = TaskCompletedEvent(task_id=task_id, user_id=user_id, completed_at=get_utc_now(), recurrence_type="daily")

    mock_original_todo = MockTodo(
        id=task_id,
        user_id=user_id,
        title="Daily Task",
        recurrence_type=RecurrenceType.DAILY,
        recurrence_interval=1,
        due_date=original_due_date
    )
    # Simulate that a next occurrence already exists
    mock_session.exec().first.side_effect = [mock_original_todo, MockTodo()] 

    new_todo = recurrence_engine.process_task_completed_event(event)

    assert new_todo is None
    mock_session.add.assert_not_called()
    mock_session.commit.assert_not_called()

@patch("backend.src.utils.datetime_utils.get_utc_now", return_value=datetime(2026, 2, 8, 12, 0, 0, tzinfo=timezone.utc))
def test_process_task_completed_event_missing_recurrence_interval(mock_get_utc_now, recurrence_engine, mock_session):
    """
    Test that recurrence generation is skipped if recurrence_interval is missing for a recurring task.
    """
    task_id = uuid.uuid4()
    user_id = uuid.uuid4()
    original_due_date = get_utc_now().replace(hour=10, minute=0, second=0, microsecond=0)
    event = TaskCompletedEvent(task_id=task_id, user_id=user_id, completed_at=get_utc_now(), recurrence_type="daily")

    mock_original_todo = MockTodo(
        id=task_id,
        user_id=user_id,
        title="Daily Task",
        recurrence_type=RecurrenceType.DAILY,
        recurrence_interval=None, # Missing interval
        due_date=original_due_date
    )
    mock_session.exec().first.return_value = mock_original_todo

    new_todo = recurrence_engine.process_task_completed_event(event)

    assert new_todo is None
    mock_session.add.assert_not_called()
    mock_session.commit.assert_not_called()
