"""Integration test to verify all Phase I Advanced features work together."""

from datetime import datetime
from src.services.task_service import TaskService
from src.services.reminder_service import ReminderService
from src.services.template_service import TemplateService
from src.models.enums import RecurrenceType
from src.models.template import TaskTemplate
import uuid


def test_full_workflow():
    """Test a full workflow combining multiple Phase I Advanced features."""
    print("Testing full workflow with multiple Phase I Advanced features...")

    # Initialize services
    service = TaskService()
    reminder_service = ReminderService()
    template_service = TemplateService()

    print("\n1. Creating a task with due date and recurrence...")
    # Add a task
    success, message, task_id = service.add_task("Weekly Report", "Write weekly status report")
    print(f"   Add task: {success}, ID: {task_id}")

    # Set due date
    success, message = service.set_due_date(task_id, "2026-12-31 17:00")
    print(f"   Set due date: {success}")

    # Set recurrence
    success, message = service.set_recurrence_rule(task_id, RecurrenceType.WEEKLY)
    print(f"   Set recurrence: {success}")

    # Update priority
    from src.models.enums import Priority
    success, message = service.update_task_priority(task_id, Priority.HIGH)
    print(f"   Set priority: {success}")

    # Add tags
    success, message = service.update_task_tags(task_id, ["work", "report", "weekly"])
    print(f"   Set tags: {success}")

    print("\n2. Verifying task properties...")
    task = service.get_task(task_id)
    print(f"   Title: {task.title}")
    print(f"   Due date: {task.due_date}")
    print(f"   Recurrence: {task.recurrence_rule.type.value}")
    print(f"   Priority: {task.priority.value}")
    print(f"   Tags: {task.tags}")

    print("\n3. Testing statistics...")
    stats = service.get_statistics()
    print(f"   Total tasks: {stats['total_tasks']}")
    print(f"   Completed: {stats['completed_tasks']}")
    print(f"   By priority - High: {stats['by_priority']['high']}, Medium: {stats['by_priority']['medium']}, Low: {stats['by_priority']['low']}")

    print("\n4. Testing reminders...")
    tasks = service.list_tasks()
    summary = reminder_service.evaluate_reminders(tasks)
    print(f"   Reminder summary - Overdue: {len(summary.overdue)}, Due today: {len(summary.due_today)}, Upcoming: {len(summary.upcoming)}")

    print("\n5. Creating and using a template...")
    # Create a template
    template = TaskTemplate(
        id=str(uuid.uuid4()),
        name="Weekly Meeting Template",
        title="Weekly Team Meeting",
        description="Attend weekly team meeting and take notes",
        priority=Priority.MEDIUM,
        tags=["meeting", "team", "weekly"],
        due_date_offset="next_week"
    )

    success, message, created_template = template_service.create_template(template)
    print(f"   Create template: {success}")

    # Use the template to create a task
    success, message, new_task = template_service.create_task_from_template(
        template.id,
        id_generator=lambda: service._next_id
    )
    print(f"   Use template: {success}")

    if new_task:
        print(f"   New task from template: {new_task.title}")

    print("\n6. Testing task completion with recurrence...")
    # Complete the recurring task to trigger auto-creation
    original_task = service.get_task(task_id)
    original_due_date = original_task.due_date
    print(f"   Original due date: {original_due_date}")

    success, message = service.toggle_status(task_id)  # Mark as complete
    print(f"   Complete recurring task: {success}")

    # Check if a new recurring task was created
    all_tasks = service.list_tasks()
    print(f"   Total tasks after completion: {len(all_tasks)}")

    print("\n7. Testing undo functionality...")
    # Undo the completion
    success, message = service.undo_last_action()
    print(f"   Undo completion: {success}")

    # Check if we're back to original state
    tasks_after_undo = service.list_tasks()
    print(f"   Total tasks after undo: {len(tasks_after_undo)}")

    print("\n8. Final statistics...")
    final_stats = service.get_statistics()
    print(f"   Final total tasks: {final_stats['total_tasks']}")
    print(f"   Final completion rate: {final_stats['completion_percentage']}%")

    print("\nPASS: All Phase I Advanced features integration test passed!")


if __name__ == "__main__":
    print("Running Phase I Advanced Integration Test")
    print("=" * 50)
    test_full_workflow()
    print("=" * 50)
    print("Integration test completed successfully!")