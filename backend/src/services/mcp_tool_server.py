from typing import Dict, Any
import asyncio
import json
from mcp.server import Server
from ..database.database import Session
from ..models.user import User
from ..tools.todo_tools import (
    add_task, list_tasks, update_task, complete_task, delete_task,
    AddTaskInput, ListTasksInput, UpdateTaskInput, CompleteTaskInput, DeleteTaskInput
)


class MCPTaskServer:
    """
    MCP Server that exposes 5 standardized tools for AI consumption:
    add_task, list_tasks, complete_task, delete_task, update_task.
    """

    def __init__(self):
        """Initialize the MCP server instance."""
        self.server = Server("todo-ai-server")
        self._register_tools()

    def _register_tools(self):
        """Register the 5 MCP tools with the server."""
        # Create a mapping of tool names to their corresponding class methods
        # This ensures the service can dynamically call the right tool
        self.tools_map = {
            "add_task": self.add_task_tool,
            "list_tasks": self.list_tasks_tool,
            "complete_task": self.complete_task_tool,
            "delete_task": self.delete_task_tool,
            "update_task": self.update_task_tool
        }

        # In a real MCP implementation, we would use decorators like @self.server.tools.register
        # For now, we're preparing the tools to be available via the tools_map
        pass

    def get_server(self):
        """Return the initialized MCP server instance."""
        return self.server

    def add_task_tool(self, input_data: AddTaskInput, user_id: str, db_session: Session) -> Dict[str, Any]:
        """
        MCP tool to add a new task to the user's todo list.

        Args:
            input_data: Contains task details
            user_id: ID of the user creating the task
            db_session: Database session

        Returns:
            Result of the task creation
        """
        # Call the actual add_task function from todo_tools
        result = add_task(input_data, user_id, db_session)
        return result

    def list_tasks_tool(self, input_data: ListTasksInput, user_id: str, db_session: Session) -> Dict[str, Any]:
        """
        MCP tool to list tasks from the user's todo list with optional filtering.

        Args:
            input_data: Contains filtering options
            user_id: ID of the user whose tasks to list
            db_session: Database session

        Returns:
            List of tasks
        """
        # Call the actual list_tasks function from todo_tools
        result = list_tasks(input_data, user_id, db_session)
        return result

    def complete_task_tool(self, input_data: CompleteTaskInput, user_id: str, db_session: Session) -> Dict[str, Any]:
        """
        MCP tool to mark a task as completed/done.

        Args:
            input_data: Contains task ID and completion status
            user_id: ID of the user whose task to update
            db_session: Database session

        Returns:
            Result of the completion operation
        """
        # Call the actual complete_task function from todo_tools
        result = complete_task(input_data, user_id, db_session)
        return result

    def delete_task_tool(self, input_data: DeleteTaskInput, user_id: str, db_session: Session) -> Dict[str, Any]:
        """
        MCP tool to delete a task from the user's todo list.

        Args:
            input_data: Contains task ID to delete
            user_id: ID of the user whose task to delete
            db_session: Database session

        Returns:
            Result of the deletion operation
        """
        # Call the actual delete_task function from todo_tools
        result = delete_task(input_data, user_id, db_session)
        return result

    def update_task_tool(self, input_data: UpdateTaskInput, user_id: str, db_session: Session) -> Dict[str, Any]:
        """
        MCP tool to update an existing task in the user's todo list.

        Args:
            input_data: Contains task ID and updates
            user_id: ID of the user whose task to update
            db_session: Database session

        Returns:
            Result of the update operation
        """
        # Call the actual update_task function from todo_tools
        result = update_task(input_data, user_id, db_session)
        return result

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
                        "ai_context": {"type": "string", "description": "Context for AI-assisted update"}
                    },
                    "required": ["task_id"]
                }
            }
        ]


# Singleton instance
mcp_server = MCPTaskServer()