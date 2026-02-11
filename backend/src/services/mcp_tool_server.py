from typing import Dict, Any
import asyncio
import json
from mcp.server import Server
from src.database.database import Session # Absolute import
from src.models.user import User # Absolute import
from src.tools.todo_tools import (
    add_task, list_tasks, update_task, complete_task, delete_task,
    set_task_recurrence, remove_task_recurrence, set_task_due_date, set_task_reminder, list_upcoming_tasks,
    AddTaskInput, ListTasksInput, UpdateTaskInput, CompleteTaskInput, DeleteTaskInput,
    SetRecurrenceInput, RemoveRecurrenceInput, SetDueDateInput, SetReminderInput, ListUpcomingTasksInput
)


class MCPTaskServer:
    """
    MCP Server that exposes standardized tools for AI consumption.
    """

    def __init__(self):
        """Initialize the MCP server instance."""
        self.server = Server("todo-ai-server")
        self._register_tools()

    def _register_tools(self):
        """Register the MCP tools with the server."""
        self.tools_map = {
            "add_task": add_task,
            "list_tasks": list_tasks,
            "complete_task": complete_task,
            "delete_task": delete_task,
            "update_task": update_task,
            "set_task_recurrence": set_task_recurrence,
            "remove_task_recurrence": remove_task_recurrence,
            "set_task_due_date": set_task_due_date,
            "set_task_reminder": set_task_reminder,
            "list_upcoming_tasks": list_upcoming_tasks
        }

    def get_server(self):
        """Return the initialized MCP server instance."""
        return self.server

    def add_task_tool(self, input_data: AddTaskInput, user_id: str, db_session: Session) -> Dict[str, Any]:
        return add_task(input_data, user_id, db_session)

    def list_tasks_tool(self, input_data: ListTasksInput, user_id: str, db_session: Session) -> Dict[str, Any]:
        return list_tasks(input_data, user_id, db_session)

    def complete_task_tool(self, input_data: CompleteTaskInput, user_id: str, db_session: Session) -> Dict[str, Any]:
        return complete_task(input_data, user_id, db_session)

    def delete_task_tool(self, input_data: DeleteTaskInput, user_id: str, db_session: Session) -> Dict[str, Any]:
        return delete_task(input_data, user_id, db_session)

    def update_task_tool(self, input_data: UpdateTaskInput, user_id: str, db_session: Session) -> Dict[str, Any]:
        return update_task(input_data, user_id, db_session)
    
    def set_task_recurrence_tool(self, input_data: SetRecurrenceInput, user_id: str, db_session: Session) -> Dict[str, Any]:
        return set_task_recurrence(input_data, user_id, db_session)

    def remove_task_recurrence_tool(self, input_data: RemoveRecurrenceInput, user_id: str, db_session: Session) -> Dict[str, Any]:
        return remove_task_recurrence(input_data, user_id, db_session)

    def set_task_due_date_tool(self, input_data: SetDueDateInput, user_id: str, db_session: Session) -> Dict[str, Any]:
        return set_task_due_date(input_data, user_id, db_session)

    def set_task_reminder_tool(self, input_data: SetReminderInput, user_id: str, db_session: Session) -> Dict[str, Any]:
        return set_task_reminder(input_data, user_id, db_session)

    def list_upcoming_tasks_tool(self, input_data: ListUpcomingTasksInput, user_id: str, db_session: Session) -> Dict[str, Any]:
        return list_upcoming_tasks(input_data, user_id, db_session)

    def get_tools(self) -> list:
        """
        Get the list of available tools.

        Returns:
            List of tool definitions
        """
        return [
            {
                "name": "add_task",
                "description": "Add a new task to the user's todo list",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "title": {"type": "string", "description": "The title of the task"},
                        "description": {"type": "string", "description": "Optional description of the task"},
                        "priority": {"type": "string", "enum": ["low", "medium", "high"], "description": "Priority level"},
                        "tags": {"type": "string", "description": "Comma-separated tags for the task"},
                        "due_date": {"type": "string", "description": "ISO format date string for due date"},
                        "recurrence_type": {"type": "string", "enum": ["none", "daily", "weekly", "monthly"], "description": "Frequency of recurrence"},
                        "recurrence_interval": {"type": "integer", "description": "Interval multiplier for recurrence"},
                        "ai_context": {"type": "string", "description": "Context for AI-generated task"}
                    },
                    "required": ["title"]
                }
            },
            {
                "name": "list_tasks",
                "description": "List tasks from the user's todo list with optional filtering",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "status": {"type": "string", "enum": ["all", "pending", "completed"], "description": "Filter by completion status"},
                        "limit": {"type": "integer", "description": "Maximum number of tasks to return"},
                        "offset": {"type": "integer", "description": "Number of tasks to skip"}
                    }
                }
            },
            {
                "name": "complete_task",
                "description": "Mark a task as completed/done",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "task_id": {"type": "string", "description": "The ID of the task to mark as completed"}
                    },
                    "required": ["task_id"]
                }
            },
            {
                "name": "delete_task",
                "description": "Delete a task from the user's todo list",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "task_id": {"type": "string", "description": "The ID of the task to delete"}
                    },
                    "required": ["task_id"]
                }
            },
            {
                "name": "update_task",
                "description": "Update an existing task in the user's todo list",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "task_id": {"type": "string", "description": "The ID of the task to update"},
                        "title": {"type": "string", "description": "New title for the task"},
                        "description": {"type": "string", "description": "New description for the task"},
                        "completed": {"type": "boolean", "description": "Whether the task is completed"},
                        "priority": {"type": "string", "enum": ["low", "medium", "high"], "description": "New priority level"},
                        "tags": {"type": "string", "description": "New comma-separated tags for the task"},
                        "due_date": {"type": "string", "description": "New ISO format date string for due date"},
                        "recurrence_type": {"type": "string", "enum": ["none", "daily", "weekly", "monthly"], "description": "Frequency of recurrence"},
                        "recurrence_interval": {"type": "integer", "description": "Interval multiplier for recurrence"},
                        "ai_context": {"type": "string", "description": "Context for AI-assisted update"}
                    },
                    "required": ["task_id"]
                }
            },
            {
                "name": "set_task_recurrence",
                "description": "Set or update recurrence settings for a task",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "task_id": {"type": "string", "description": "The ID of the task to update"},
                        "recurrence_type": {"type": "string", "enum": ["none", "daily", "weekly", "monthly"], "description": "Frequency of recurrence"},
                        "recurrence_interval": {"type": "integer", "description": "Interval multiplier for recurrence"}
                    },
                    "required": ["task_id", "recurrence_type"]
                }
            },
            {
                "name": "remove_task_recurrence",
                "description": "Remove recurrence settings from a task",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "task_id": {"type": "string", "description": "The ID of the task to update"}
                    },
                    "required": ["task_id"]
                }
            },
            {
                "name": "set_task_due_date",
                "description": "Set or update the due date for a task",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "task_id": {"type": "string", "description": "The ID of the task to update"},
                        "due_date": {"type": "string", "description": "ISO format date string for the new due date"}
                    },
                    "required": ["task_id", "due_date"]
                }
            },
            {
                "name": "set_task_reminder",
                "description": "Set or update the reminder time for a task",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "task_id": {"type": "string", "description": "The ID of the task to update"},
                        "reminder_at": {"type": "string", "description": "ISO format date string for when to send the reminder"}
                    },
                    "required": ["task_id", "reminder_at"]
                }
            },
            {
                "name": "list_upcoming_tasks",
                "description": "List tasks with upcoming due dates for the user",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "days_ahead": {"type": "integer", "description": "Number of days to look ahead for due tasks (default 7)"},
                        "include_overdue": {"type": "boolean", "description": "Whether to include overdue tasks (default false)"}
                    }
                }
            }
        ]


# Singleton instance
mcp_server = MCPTaskServer()