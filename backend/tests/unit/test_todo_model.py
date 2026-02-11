from datetime import datetime, timedelta, timezone
import uuid
import pytest

from pydantic import ValidationError
from sqlmodel import Session, Field

from src.models.todo import Todo, TodoCreate, RecurrenceType
from src.utils.datetime_utils import get_utc_now

class MockUser:
    """A mock user for Todo creation."""
    def __init__(self, user_id: uuid.UUID):
        self.id = user_id

@pytest.fixture
def sample_user_id():
    return uuid.uuid4()

@pytest.fixture
def create_todo_instance(sample_user_id):
    def _create_todo(**kwargs):
        todo_data = {
            "title": "Test Todo",
            "user_id": sample_user_id,
            "created_at": get_utc_now(),
            "updated_at": get_utc_now(),
        }
        todo_data.update(kwargs)
        return Todo(**todo_data)
    return _create_todo


def test_todo_model_due_date_future_validation_success(create_todo_instance):
    """
    Test that due_date set to a future time is valid.
    """
    future_date = get_utc_now() + timedelta(days=1)
    todo = create_todo_instance(due_date=future_date)
    assert todo.due_date == future_date


def test_todo_model_due_date_past_validation_failure(create_todo_instance):
    """
    Test that due_date set to a past time raises ValidationError.
    """
    past_date = get_utc_now() - timedelta(days=1)
    with pytest.raises(ValidationError, match="Date/time must be in the future"):
        create_todo_instance(due_date=past_date)


def test_todo_model_reminder_at_future_validation_success(create_todo_instance):
    """
    Test that reminder_at set to a future time is valid.
    """
    future_date = get_utc_now() + timedelta(days=1)
    reminder_time = future_date - timedelta(hours=1)
    todo = create_todo_instance(due_date=future_date, reminder_at=reminder_time)
    assert todo.reminder_at == reminder_time


def test_todo_model_reminder_at_past_validation_failure(create_todo_instance):
    """
    Test that reminder_at set to a past time raises ValidationError.
    """
    future_date = get_utc_now() + timedelta(days=1)
    past_reminder_time = get_utc_now() - timedelta(hours=1)
    with pytest.raises(ValidationError, match="Date/time must be in the future"):
        create_todo_instance(due_date=future_date, reminder_at=past_reminder_time)


def test_todo_model_reminder_at_after_due_date_validation_failure(create_todo_instance):
    """
    Test that reminder_at set after due_date raises ValidationError.
    """
    due_date = get_utc_now() + timedelta(days=1)
    reminder_time = due_date + timedelta(hours=1)
    with pytest.raises(ValidationError, match="Reminder time must be before or equal to due date"):
        create_todo_instance(due_date=due_date, reminder_at=reminder_time)


def test_todo_model_recurrence_interval_required_for_recurring_task_failure(create_todo_instance):
    """
    Test that recurrence_interval is required for recurring tasks.
    """
    with pytest.raises(ValidationError, match="Recurrence interval is required for recurring tasks"):
        create_todo_instance(recurrence_type=RecurrenceType.DAILY, recurrence_interval=None)


def test_todo_model_recurrence_interval_not_set_for_non_recurring_task_failure(create_todo_instance):
    """
    Test that recurrence_interval should not be set for non-recurring tasks.
    """
    with pytest.raises(ValidationError, match="Recurrence interval should not be set for non-recurring tasks"):
        create_todo_instance(recurrence_type=RecurrenceType.NONE, recurrence_interval=1)


def test_todo_model_recurrence_interval_valid_for_recurring_task_success(create_todo_instance):
    """
    Test valid recurrence_interval for recurring tasks.
    """
    todo = create_todo_instance(recurrence_type=RecurrenceType.WEEKLY, recurrence_interval=2)
    assert todo.recurrence_interval == 2


def test_todo_model_default_recurrence_type(create_todo_instance):
    """
    Test that recurrence_type defaults to NONE.
    """
    todo = create_todo_instance()
    assert todo.recurrence_type == RecurrenceType.NONE


def test_todo_model_no_due_date_no_reminder_success(create_todo_instance):
    """
    Test creation of a todo with no due date or reminder.
    """
    todo = create_todo_instance(due_date=None, reminder_at=None)
    assert todo.due_date is None
    assert todo.reminder_at is None


def test_todo_create_schema_recurrence_type_validation_success():
    """
    Test that TodoCreate validates recurrence_type correctly.
    """
    data = {
        "title": "Daily Standup",
        "recurrence_type": "daily",
        "recurrence_interval": 1,
        "due_date": (get_utc_now() + timedelta(days=1)).isoformat()
    }
    todo_create = TodoCreate(**data)
    assert todo_create.recurrence_type == RecurrenceType.DAILY
    assert todo_create.recurrence_interval == 1


def test_todo_create_schema_recurrence_type_invalid_failure():
    """
    Test that TodoCreate raises ValidationError for invalid recurrence_type.
    """
    data = {
        "title": "Invalid Recurrence",
        "recurrence_type": "yearly",
        "recurrence_interval": 1,
        "due_date": (get_utc_now() + timedelta(days=1)).isoformat()
    }
    with pytest.raises(ValidationError):
        TodoCreate(**data)

