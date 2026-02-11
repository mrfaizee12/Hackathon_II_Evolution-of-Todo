from sqlmodel import Session, select
from datetime import datetime, timedelta
from typing import Optional
import uuid

from ..models.todo import Todo, TodoCreate, RecurrenceType
from src.utils.datetime_utils import calculate_next_occurrence, get_utc_now
from ..events.todo_events import TaskCompletedEvent

class RecurrenceEngine:
    def __init__(self, session_factory: callable):
        self.session_factory = session_factory

    def process_task_completed_event(self, event: TaskCompletedEvent) -> Optional[Todo]:
        """
        Processes a TaskCompletedEvent to create the next occurrence of a recurring task.
        """
        with self.session_factory() as session:
            # Retrieve the original recurring task using task_id
            original_task = session.exec(select(Todo).where(Todo.id == event.task_id)).first()

            if not original_task:
                print(f"Original task with ID {event.task_id} not found. Cannot create next recurrence.")
                return None

            if original_task.recurrence_type == RecurrenceType.NONE:
                print(f"Task {original_task.id} is not a recurring task. Skipping recurrence generation.")
                return None
            
            if not original_task.recurrence_interval:
                print(f"Task {original_task.id} is a recurring task but recurrence_interval is missing. Skipping recurrence generation.")
                return None

            # Calculate the next occurrence
            try:
                next_due_date = calculate_next_occurrence(
                    current_occurrence=original_task.due_date if original_task.due_date else get_utc_now(),
                    recurrence_type=original_task.recurrence_type.value,
                    recurrence_interval=original_task.recurrence_interval
                )
            except ValueError as e:
                print(f"Error calculating next occurrence for task {original_task.id}: {e}")
                return None
            
            # Check if a next occurrence already exists to prevent duplicates
            existing_next_occurrence = session.exec(
                select(Todo).where(
                    Todo.user_id == original_task.user_id,
                    Todo.title == original_task.title, # Assuming title + user_id uniquely identifies a recurring series for now
                    Todo.recurrence_type == original_task.recurrence_type,
                    Todo.recurrence_interval == original_task.recurrence_interval,
                    Todo.next_occurrence == next_due_date # Check against the newly calculated next_occurrence
                )
            ).first()

            if existing_next_occurrence:
                print(f"Next occurrence for task {original_task.id} with due date {next_due_date} already exists. Skipping duplicate creation.")
                return None

            # Create a new todo item for the next occurrence
            new_todo = Todo(
                user_id=original_task.user_id,
                title=original_task.title,
                description=original_task.description,
                completed=False, # New occurrence is not completed
                priority=original_task.priority,
                tags=original_task.tags,
                due_date=next_due_date,
                recurrence_type=original_task.recurrence_type,
                recurrence_interval=original_task.recurrence_interval,
                next_occurrence=next_due_date, # For the new task, its next_occurrence is its own due_date
                reminder_at=None, # Reminders should be set individually for each occurrence
                ai_generated=original_task.ai_generated,
                ai_context=original_task.ai_context
            )
            session.add(new_todo)
            session.commit()
            session.refresh(new_todo)
            print(f"Created next occurrence for task {original_task.id}: {new_todo.id} with due date {new_todo.due_date}")
            return new_todo
