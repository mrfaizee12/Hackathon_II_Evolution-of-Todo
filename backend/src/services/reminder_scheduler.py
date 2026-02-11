from sqlmodel import Session, select
from datetime import datetime, timedelta
from typing import List
import asyncio

from ..models.todo import Todo
from ..events.publisher import EventPublisher, InMemoryEventPublisher
from ..events.todo_events import ReminderTriggeredEvent
from src.utils.datetime_utils import get_utc_now

class ReminderScheduler:
    def __init__(self, session_factory: callable, event_publisher: EventPublisher = None, check_interval_seconds: int = 60):
        self.session_factory = session_factory
        self.event_publisher = event_publisher if event_publisher else InMemoryEventPublisher()
        self.check_interval_seconds = check_interval_seconds
        self._running = False

    async def start(self):
        """Starts the periodic reminder check."""
        print(f"ReminderScheduler starting with check interval: {self.check_interval_seconds} seconds.")
        self._running = True
        while self._running:
            await self.check_and_trigger_reminders()
            await asyncio.sleep(self.check_interval_seconds)

    def stop(self):
        """Stops the periodic reminder check."""
        print("ReminderScheduler stopping.")
        self._running = False

    async def check_and_trigger_reminders(self):
        """
        Queries for todos with upcoming reminders and triggers events.
        """
        now_utc = get_utc_now()
        print(f"Checking for reminders at {now_utc}")

        with self.session_factory() as session:
            # Select todos where reminder_at is in the past or very near future,
            # and the todo is not yet completed, and it hasn't been reminded recently
            # (assuming 'reminded' status or a flag to prevent immediate re-triggering)
            # For simplicity, we'll mark the reminder_at as None after triggering,
            # indicating it has been "handled" for this specific time.
            statement = select(Todo).where(
                Todo.reminder_at <= now_utc,
                Todo.completed == False,
                Todo.reminder_at != None # Ensure reminder_at is set
            )
            
            todos_to_remind = session.exec(statement).all()

            for todo in todos_to_remind:
                print(f"Triggering reminder for todo ID: {todo.id}, title: {todo.title}")
                self.event_publisher.publish(
                    "reminder.triggered",
                    ReminderTriggeredEvent(
                        task_id=todo.id,
                        user_id=todo.user_id,
                        reminder_time=todo.reminder_at,
                        message=f"Reminder: Your todo '{todo.title}' is due soon!"
                    ).model_dump()
                )
                # Mark reminder as handled by clearing reminder_at or setting a 'reminded_at' flag
                # For now, we'll clear reminder_at, assuming it's a one-time reminder per setting.
                # A more complex system might set a 'next_reminder_at' or use a separate reminder entity.
                todo.reminder_at = None 
                session.add(todo)
            session.commit()
            print(f"Finished checking for reminders. Triggered {len(todos_to_remind)} reminders.")
