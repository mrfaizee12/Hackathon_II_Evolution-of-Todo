"""ReminderService for managing console-based reminders in Phase I Advanced todo application.

This module provides reminder evaluation and display functionality.
"""

from datetime import datetime
from typing import List
from src.models.task import Task
from src.models.reminder import ReminderSummary


class ReminderService:
    """Manages console-based reminder evaluation and display."""

    def __init__(self):
        """Initialize ReminderService."""
        pass

    def evaluate_reminders(self, tasks: List[Task]) -> ReminderSummary:
        """Evaluate reminder categories."""
        overdue = [
            t for t in tasks
            if t.due_date and t.due_date < datetime.now() and t.status != "Complete"
        ]

        due_today = [
            t for t in tasks
            if t.due_date and t.due_date.date() == datetime.now().date() and t.status != "Complete"
        ]

        from datetime import timedelta
        future_date = datetime.now() + timedelta(days=7)
        upcoming = [
            t for t in tasks
            if t.due_date
            and t.status != "Complete"
            and datetime.now() < t.due_date <= future_date
        ]

        return ReminderSummary(overdue=overdue, due_today=due_today, upcoming=upcoming)

    def display_reminders(self, summary: ReminderSummary) -> str:
        """Format reminders for console display."""
        output = []

        if summary.has_overdue:
            output.append("\n🚨 OVERDUE TASKS:")
            for task in summary.overdue:
                output.append(f"  - ID: {task.id} | {task.title} | Due: {task.due_date.strftime('%Y-%m-%d %H:%M')}")

        if summary.has_due_today:
            output.append("\n📅 DUE TODAY:")
            for task in summary.due_today:
                output.append(f"  - ID: {task.id} | {task.title} | Due: {task.due_date.strftime('%Y-%m-%d %H:%M')}")

        if summary.has_upcoming:
            output.append("\n🔔 UPCOMING TASKS:")
            for task in summary.upcoming:
                output.append(f"  - ID: {task.id} | {task.title} | Due: {task.due_date.strftime('%Y-%m-%d %H:%M')}")

        if not output:
            output.append("\n✅ No overdue, due today, or upcoming tasks to display.")

        return "\n".join(output)

    def get_reminder_count(self, tasks: List[Task]) -> int:
        """Get the total number of reminder tasks."""
        summary = self.evaluate_reminders(tasks)
        return summary.total_count

    def has_reminders(self, tasks: List[Task]) -> bool:
        """Check if there are any reminder tasks."""
        return self.get_reminder_count(tasks) > 0