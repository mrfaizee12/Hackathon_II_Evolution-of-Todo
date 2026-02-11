import pytest
from datetime import datetime, timedelta, timezone
from typing import Generator
import uuid

from fastapi.testclient import TestClient
from sqlmodel import Session, create_engine, SQLModel

from src.main import app
from src.database.database import get_session
from src.models.todo import Todo, RecurrenceType
from src.models.user import User
from src.middleware.auth import create_access_token


# Setup for test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_db.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


@pytest.fixture(name="session")
def session_fixture() -> Generator[Session, None, None]:
    create_db_and_tables()
    with Session(engine) as session:
        yield session
    SQLModel.metadata.drop_all(engine)


@pytest.fixture(name="client")
def client_fixture(session: Session) -> Generator[TestClient, None, None]:
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    yield TestClient(app)
    app.dependency_overrides.clear()


@pytest.fixture
def test_user(session: Session):
    user = User(
        id=uuid.uuid4(),
        username="testuser",
        email="test@example.com",
        hashed_password="fakehashedpassword",
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@pytest.fixture
def auth_headers(test_user: User):
    access_token = create_access_token(data={"sub": test_user.email})
    return {"Authorization": f"Bearer {access_token}"}


@pytest.fixture
def test_todo(session: Session, test_user: User):
    todo = Todo(
        id=uuid.uuid4(),
        user_id=test_user.id,
        title="Test Todo",
        description="A simple test todo",
        due_date=datetime.now(timezone.utc) + timedelta(days=7),
    )
    session.add(todo)
    session.commit()
    session.refresh(todo)
    return todo


def test_set_todo_recurrence_daily(client: TestClient, auth_headers: dict, test_todo: Todo):
    """
    Test setting daily recurrence for a todo.
    """
    response = client.put(
        f"/todos/{test_todo.id}/recurrence",
        headers=auth_headers,
        json={"recurrence_type": "daily", "recurrence_interval": 1}
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["recurrence_type"] == "daily"
    assert data["recurrence_interval"] == 1


def test_remove_todo_recurrence(client: TestClient, auth_headers: dict, test_todo: Todo):
    """
    Test removing recurrence settings from a todo.
    """
    # First set recurrence
    client.put(
        f"/todos/{test_todo.id}/recurrence",
        headers=auth_headers,
        json={"recurrence_type": "daily", "recurrence_interval": 1}
    )

    response = client.delete(
        f"/todos/{test_todo.id}/recurrence",
        headers=auth_headers
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["recurrence_type"] == "none"
    assert data["recurrence_interval"] is None
    assert data["next_occurrence"] is None


def test_set_todo_due_date(client: TestClient, auth_headers: dict, test_todo: Todo):
    """
    Test setting a due date for a todo.
    """
    new_due_date = (datetime.now(timezone.utc) + timedelta(days=10)).isoformat()
    response = client.put(
        f"/todos/{test_todo.id}/due-date",
        headers=auth_headers,
        json={"due_date": new_due_date}
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["due_date"] == new_due_date


def test_set_todo_reminder(client: TestClient, auth_headers: dict, test_todo: Todo):
    """
    Test setting a reminder for a todo.
    """
    # Set a due date first as reminder_at depends on it
    future_due_date = datetime.now(timezone.utc) + timedelta(days=5)
    client.put(
        f"/todos/{test_todo.id}/due-date",
        headers=auth_headers,
        json={"due_date": future_due_date.isoformat()}
    )

    new_reminder_at = (future_due_date - timedelta(hours=1)).isoformat()
    response = client.put(
        f"/todos/{test_todo.id}/reminder",
        headers=auth_headers,
        json={"reminder_at": new_reminder_at}
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["reminder_at"] == new_reminder_at


def test_get_upcoming_todos(client: TestClient, auth_headers: dict, test_user: User, session: Session):
    """
    Test fetching upcoming todos.
    """
    # Create some todos with different due dates
    past_todo = Todo(
        user_id=test_user.id,
        title="Past Todo",
        due_date=datetime.now(timezone.utc) - timedelta(days=1),
    )
    upcoming_todo_1 = Todo(
        user_id=test_user.id,
        title="Upcoming Todo 1",
        due_date=datetime.now(timezone.utc) + timedelta(days=1),
    )
    upcoming_todo_2 = Todo(
        user_id=test_user.id,
        title="Upcoming Todo 2",
        due_date=datetime.now(timezone.utc) + timedelta(days=5),
    )
    far_future_todo = Todo(
        user_id=test_user.id,
        title="Far Future Todo",
        due_date=datetime.now(timezone.utc) + timedelta(days=10),
    )
    completed_upcoming_todo = Todo(
        user_id=test_user.id,
        title="Completed Upcoming Todo",
        due_date=datetime.now(timezone.utc) + timedelta(days=2),
        completed=True
    )

    session.add_all([past_todo, upcoming_todo_1, upcoming_todo_2, far_future_todo, completed_upcoming_todo])
    session.commit()
    session.refresh(past_todo)
    session.refresh(upcoming_todo_1)
    session.refresh(upcoming_todo_2)
    session.refresh(far_future_todo)
    session.refresh(completed_upcoming_todo)


    # Test with default days_ahead (7)
    response = client.get(
        "/todos/upcoming",
        headers=auth_headers
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 2 # upcoming_todo_1, upcoming_todo_2
    assert any(todo["title"] == "Upcoming Todo 1" for todo in data)
    assert any(todo["title"] == "Upcoming Todo 2" for todo in data)
    assert not any(todo["title"] == "Past Todo" for todo in data)
    assert not any(todo["title"] == "Far Future Todo" for todo in data)
    assert not any(todo["title"] == "Completed Upcoming Todo" for todo in data)

    # Test with include_overdue=True
    response = client.get(
        "/todos/upcoming?include_overdue=true",
        headers=auth_headers
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 3 # past_todo, upcoming_todo_1, upcoming_todo_2
    assert any(todo["title"] == "Past Todo" for todo in data)
    assert any(todo["title"] == "Upcoming Todo 1" for todo in data)
    assert any(todo["title"] == "Upcoming Todo 2" for todo in data)
    
    # Test with custom days_ahead
    response = client.get(
        "/todos/upcoming?days_ahead=15",
        headers=auth_headers
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 3 # upcoming_todo_1, upcoming_todo_2, far_future_todo
    assert any(todo["title"] == "Upcoming Todo 1" for todo in data)
    assert any(todo["title"] == "Upcoming Todo 2" for todo in data)
    assert any(todo["title"] == "Far Future Todo" for todo in data)
