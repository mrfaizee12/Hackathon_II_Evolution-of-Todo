import pytest
import asyncio
from datetime import datetime, timedelta, timezone
import uuid
from unittest.mock import MagicMock, patch

from sqlmodel import Session, SQLModel, Field

from src.models.todo import Todo, RecurrenceType
from src.services.reminder_scheduler import ReminderScheduler
from src.events.publisher import EventPublisher
from src.events.todo_events import ReminderTriggeredEvent
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


@pytest.fixture
def mock_event_publisher():
    """Fixture for a mock EventPublisher."""
    publisher = MagicMock(spec=EventPublisher)
    publisher.publish.return_value = None
    return publisher


@pytest.fixture
def reminder_scheduler(mock_session, mock_event_publisher):
    """Fixture for ReminderScheduler with mock session factory and event publisher."""
    return ReminderScheduler(session_factory=lambda: mock_session, event_publisher=mock_event_publisher, check_interval_seconds=1)


@patch("backend.src.utils.datetime_utils.get_utc_now", return_value=datetime(2026, 2, 8, 12, 0, 0, tzinfo=timezone.utc))
async def test_check_and_trigger_reminders_no_todos(mock_get_utc_now, reminder_scheduler, mock_session, mock_event_publisher):
    """
    Test that no reminders are triggered if there are no todos due for reminder.
    """
    mock_session.exec().all.return_value = [] # No todos found

    await reminder_scheduler.check_and_trigger_reminders()

    mock_event_publisher.publish.assert_not_called()
    mock_session.add.assert_not_called()
    mock_session.commit.assert_not_called()


@patch("backend.src.utils.datetime_utils.get_utc_now", return_value=datetime(2026, 2, 8, 12, 0, 0, tzinfo=timezone.utc))
async def test_check_and_trigger_reminders_single_todo(mock_get_utc_now, reminder_scheduler, mock_session, mock_event_publisher):
    """
    Test that a single todo with an upcoming reminder is triggered.
    """
    now_utc = mock_get_utc_now.return_value
    todo_id = uuid.uuid4()
    user_id = uuid.uuid4()
    reminder_time = now_utc - timedelta(seconds=1) # Slightly in the past

    mock_todo = MockTodo(
        id=todo_id,
        user_id=user_id,
        title="Reminder Todo",
        reminder_at=reminder_time,
        completed=False
    )
    mock_session.exec().all.return_value = [mock_todo]

    await reminder_scheduler.check_and_trigger_reminders()

    mock_event_publisher.publish.assert_called_once()
    assert mock_todo.reminder_at is None # Reminder should be cleared
    mock_session.add.assert_called_once_with(mock_todo)
    mock_session.commit.assert_called_once()


@patch("backend.src.utils.datetime_utils.get_utc_now", return_value=datetime(2026, 2, 8, 12, 0, 0, tzinfo=timezone.utc))
async def test_check_and_trigger_reminders_multiple_todos(mock_get_utc_now, reminder_scheduler, mock_session, mock_event_publisher):
    """
    Test that multiple todos with upcoming reminders are triggered.
    """
    now_utc = mock_get_utc_now.return_value
    todo1_id = uuid.uuid4()
    todo2_id = uuid.uuid4()
    user_id = uuid.uuid4()

    mock_todo1 = MockTodo(
        id=todo1_id,
        user_id=user_id,
        title="Reminder Todo 1",
        reminder_at=now_utc - timedelta(seconds=5),
        completed=False
    )
    mock_todo2 = MockTodo(
        id=todo2_id,
        user_id=user_id,
        title="Reminder Todo 2",
        reminder_at=now_utc - timedelta(seconds=1),
        completed=False
    )
    mock_session.exec().all.return_value = [mock_todo1, mock_todo2]

    await reminder_scheduler.check_and_trigger_reminders()

    assert mock_event_publisher.publish.call_count == 2
    assert mock_todo1.reminder_at is None
    assert mock_todo2.reminder_at is None
    assert mock_session.add.call_count == 2
    assert mock_session.commit.assert_called_once()


@patch("backend.src.utils.datetime_utils.get_utc_now", return_value=datetime(2026, 2, 8, 12, 0, 0, tzinfo=timezone.utc))
async def test_check_and_trigger_reminders_completed_todo_ignored(mock_get_utc_now, reminder_scheduler, mock_session, mock_event_publisher):
    """
    Test that completed todos are ignored by the reminder scheduler.
    """
    now_utc = mock_get_utc_now.return_value
    todo_id = uuid.uuid4()
    user_id = uuid.uuid4()
    reminder_time = now_utc - timedelta(seconds=1)

    mock_todo = MockTodo(
        id=todo_id,
        user_id=user_id,
        title="Completed Todo",
        reminder_at=reminder_time,
        completed=True # Already completed
    )
    mock_session.exec().all.return_value = [mock_todo]

    await reminder_scheduler.check_and_trigger_reminders()

    mock_event_publisher.publish.assert_not_called()
    mock_session.add.assert_not_called()
    mock_session.commit.assert_not_called()


@patch("backend.src.utils.datetime_utils.get_utc_now", return_value=datetime(2026, 2, 8, 12, 0, 0, tzinfo=timezone.utc))
async def test_check_and_trigger_reminders_future_reminder_ignored(mock_get_utc_now, reminder_scheduler, mock_session, mock_event_publisher):
    """
    Test that todos with future reminders are ignored.
    """
    now_utc = mock_get_utc_now.return_value
    todo_id = uuid.uuid4()
    user_id = uuid.uuid4()
    reminder_time = now_utc + timedelta(minutes=5) # In the future

    mock_todo = MockTodo(
        id=todo_id,
        user_id=user_id,
        title="Future Reminder Todo",
        reminder_at=reminder_time,
        completed=False
    )
    mock_session.exec().all.return_value = [mock_todo]

    await reminder_scheduler.check_and_trigger_reminders()

    mock_event_publisher.publish.assert_not_called()
    mock_session.add.assert_not_called()
    mock_session.commit.assert_not_called()
