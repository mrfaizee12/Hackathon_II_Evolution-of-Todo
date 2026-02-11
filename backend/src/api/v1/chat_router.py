from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import Dict, Any, Optional
from datetime import datetime
import uuid
import json
import re
from pydantic import BaseModel

from ...database.database import get_session
from ...database.config import settings
from ...middleware.auth import get_current_user
from ...models.user import User
from ...services.ai_conversation_service import AIConversationService
from ...tools.todo_tools import (
    add_task, list_tasks, update_task, complete_task, delete_task, get_all_tasks,
    set_task_recurrence, remove_task_recurrence, set_task_due_date, set_task_reminder, list_upcoming_tasks,
    AddTaskInput, ListTasksInput, UpdateTaskInput, CompleteTaskInput, DeleteTaskInput,
    SetRecurrenceInput, RemoveRecurrenceInput, SetDueDateInput, SetReminderInput, ListUpcomingTasksInput
)
from ...tools.user_tools import get_user_identity, GetUserIdentityInput
from ...services.openrouter_service import OpenRouterService
from ...services.mcp_tool_server import mcp_server


def convert_position_to_uuid(arguments: Dict, last_displayed_tasks: list) -> Dict:
    """
    Convert position numbers (1, 2, 3...) to actual UUIDs based on the last displayed tasks.
    If task_id contains a number, try to map it to the corresponding UUID in the last displayed tasks.
    """
    if 'task_id' in arguments and isinstance(arguments['task_id'], str):
        task_id_str = arguments['task_id'].strip()

        # Check if the task_id is a number (position)
        if task_id_str.isdigit():
            position = int(task_id_str)

            # Adjust for 1-based indexing (users say "task 1" for first task)
            if 1 <= position <= len(last_displayed_tasks):
                actual_task = last_displayed_tasks[position - 1]
                arguments['task_id'] = actual_task['id']
                print(f"Converted position {position} to UUID {actual_task['id']}")
            else:
                # If position is out of range, return error message
                print(f"Position {position} is out of range. Available tasks: 1-{len(last_displayed_tasks) if last_displayed_tasks else 0}")

    return arguments


def format_task_list_for_display(tasks: list) -> str:
    """
    Format the task list for display to the user with proper numbering and status indicators.
    """
    if not tasks:
        return "No tasks found."

    formatted_tasks = []
    for idx, task in enumerate(tasks, 1):
        status = "Completed" if task.get('completed', False) else "Pending"
        formatted_tasks.append(f"{idx}) {task.get('title', 'Untitled')} — {status}")

    return "\n".join(formatted_tasks)


# State is maintained in the database - no in-memory session storage for stateless operation

class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None


router = APIRouter()


@router.post("/send")
async def chat_with_ai(
    request: ChatRequest,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Send a message to the AI assistant and get a response.
    Creates or continues a conversation with the AI assistant.
    """
    # Debug: print current user
    print(f"Current user: {current_user}")
    print(f"Current user ID: {current_user.id if current_user else None}")

    # Use the authenticated user's ID directly
    user_id = str(current_user.id)
    message = request.message
    conversation_id = request.conversation_id

    # State is maintained in the database - fetch current state from DB for this user
    # Fetch the user's last displayed tasks by getting their most recent conversation data
    last_displayed_tasks = []  # Will be populated based on conversation context if needed

    # Get or create conversation
    ai_service = AIConversationService(session)
    conv_uuid = None

    if conversation_id:
        try:
            conv_uuid = uuid.UUID(conversation_id)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid conversation ID format"
            )

        conversation = ai_service.get_conversation_by_id(conv_uuid)
        if not conversation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversation not found"
            )
    else:
        # Create a new conversation
        conversation = ai_service.create_conversation(
            user_id=current_user.id,
            title=f"AI Chat - {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        )
        conv_uuid = conversation.id

    # State is maintained in database - no conversation-specific state in memory
    # We'll determine active intent based on conversation context from database when needed
    # For now, initialize as none for stateless operation
    active_intent = "none"
    pending_task_id = ""

    # Add user message to conversation (don't commit yet - wait for full transaction)
    user_message = ai_service.add_message_to_conversation(
        conversation_id=conv_uuid,
        sender_type="USER",
        content=message,
        message_type="TEXT",
        commit=False
    )

    # Prepare tools for the AI agent
    tools = [
        {
            "type": "function",
            "function": {
                "name": "add_task",
                "description": "Add a new task to the user's todo list",
                "parameters": {
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
            }
        },
        {
            "type": "function",
            "function": {
                "name": "get_all_tasks",
                "description": "Get all tasks from the user's todo list",
                "parameters": {
                    "type": "object",
                    "properties": {}
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "list_tasks",
                "description": "List tasks from the user's todo list with optional filtering",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "status": {"type": "string", "enum": ["all", "pending", "completed"], "description": "Filter by completion status"},
                        "limit": {"type": "integer", "description": "Maximum number of tasks to return"},
                        "offset": {"type": "integer", "description": "Number of tasks to skip"}
                    }
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "update_task",
                "description": "Update an existing task in the user's todo list",
                "parameters": {
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
                    }
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "delete_task",
                "description": "Delete a task from the user's todo list",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "task_id": {"type": "string", "description": "The ID of the task to delete"}
                    },
                    "required": ["task_id"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "complete_task",
                "description": "Mark a task as completed/done",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "task_id": {"type": "string", "description": "The ID of the task to mark as completed"}
                    },
                    "required": ["task_id"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "set_task_recurrence",
                "description": "Set or update recurrence settings for a task",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "task_id": {"type": "string", "description": "The ID of the task to update"},
                        "recurrence_type": {"type": "string", "enum": ["none", "daily", "weekly", "monthly"], "description": "Frequency of recurrence"},
                        "recurrence_interval": {"type": "integer", "description": "Interval multiplier for recurrence"}
                    },
                    "required": ["task_id", "recurrence_type"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "remove_task_recurrence",
                "description": "Remove recurrence settings from a task",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "task_id": {"type": "string", "description": "The ID of the task to update"}
                    },
                    "required": ["task_id"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "set_task_due_date",
                "description": "Set or update the due date for a task",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "task_id": {"type": "string", "description": "The ID of the task to update"},
                        "due_date": {"type": "string", "description": "ISO format date string for the new due date"}
                    },
                    "required": ["task_id", "due_date"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "set_task_reminder",
                "description": "Set or update the reminder time for a task",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "task_id": {"type": "string", "description": "The ID of the task to update"},
                        "reminder_at": {"type": "string", "description": "ISO format date string for when to send the reminder"}
                    },
                    "required": ["task_id", "reminder_at"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "list_upcoming_tasks",
                "description": "List tasks with upcoming due dates for the user",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "days_ahead": {"type": "integer", "description": "Number of days to look ahead for due tasks (default 7)"},
                        "include_overdue": {"type": "boolean", "description": "Whether to include overdue tasks (default false)"}
                    }
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "get_user_identity",
                "description": "Get user identity information",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string", "description": "The ID of the user to get information for"}
                    },
                    "required": ["user_id"]
                }
            }
        }
    ]

    # For stateless operation, we don't maintain active intent in memory
    # Instead, we rely on the AI model to determine intent from the message alone
    # and fetch necessary context from the database when needed

    # Fetch last displayed tasks if needed for position-to-UUID conversion
    if re.search(r'\b(task\s+\d+|\d+\s+task)', message.lower()):
        # If the message refers to a task by position, we need to fetch the current task list
        refresh_result = get_all_tasks(str(current_user.id), session)
        if refresh_result.get("success") and "tasks" in refresh_result:
            last_displayed_tasks = refresh_result["tasks"]


    messages = [
        {"role": "system", "content": """You are an action-oriented database operator specialized in executing user commands immediately. Follow these deterministic rules:

INTENT + TASK NUMBER HANDLING:
- When user says 'Delete task 3' or 'Update task 3', AUTO-FETCH task list if not in memory
- RESOLVE position → UUID immediately in the SAME turn
- EXECUTE action in the SAME turn
- NEVER ask for task ID if task number is already provided

TASK LIST MEMORY:
- Always persist last_task_list in session memory
- Never overwrite it unless refreshed
- Auto-refresh when needed for position-to-UUID mapping

STATUS CHANGES:
- Use complete_task ONLY for marking tasks done
- Never call update_task just to mark completed

UPDATE TASK BEHAVIOR:
- NEVER call add_task when user intent is update
- If update_task fails, ask user for missing fields (e.g. title)
- DO NOT fallback to add_task under any condition
- For partial updates (description, priority), fetch existing task data and send full payload (title + updated field)

DELETE TASK BEHAVIOR:
- After delete_task or complete_task: immediately refresh task list and update session memory before responding

MEMORY RULES:
- last_task_list must always reflect latest backend state
- Never respond using stale task data

SINGLE TASK QUERIES:
- If user asks for 'task X description': resolve task X from last_task_list and read description from memory
- Do NOT refuse if data already exists

ADD_TASK FLOW:
- Store draft task details in memory when user provides incomplete info
- Accept 'yes', 'do that', 'confirm' as confirmation for pending tasks
- Normalize date formats automatically to YYYY-MM-DD

EXECUTION RULES:
- When user says 'update task 5 to change title to New Title', call update_task with task_id: UUID of task 5, title: 'New Title'
- When user says 'add task Buy groceries', call add_task with title: 'Buy groceries'
- When user says 'complete task 3', call complete_task with task_id: UUID of task 3"""},
        {"role": "user", "content": message}
    ]


    # Initialize OpenRouter service
    openrouter_service = OpenRouterService()

    try:
        # Use the enhanced chat completion method that handles tools internally
        response_result = openrouter_service.chat_completion_v2(
            messages=messages,
            tools=tools,
            tool_choice="auto",
            user_id=str(current_user.id)
        )

        if not response_result["success"]:
            # Log the actual error for debugging
            error_msg = response_result.get("response", "AI service is experiencing issues. Please try again.")
            print(f"OpenRouter error: {error_msg}")

            return {
                "response": "⚠️ AI service is experiencing issues. Please try again.",
                "conversation_id": str(conv_uuid),
                "action_performed": False,
                "error": error_msg
            }

        # Extract the final response text
        ai_response = response_result["response"]
        # Reset tool_calls_results since they're handled internally now
        tool_calls_results = []

    except Exception as api_error:
        # Handle any unexpected errors
        print(f"Unexpected error in OpenRouter API call: {str(api_error)}")
        return {
            "response": "⚠️ AI service is experiencing issues. Please try again.",
            "conversation_id": str(conv_uuid),
            "action_performed": False,
            "error": str(api_error)
        }

    # Process the response - all tool execution is handled internally now
    # Clean up any internal reasoning/thought tags from the response
    # Simple removal of internal AI reasoning tags using string operations
    if ai_response:
        # Remove common thinking tags using split method (safest approach)
        if "<thought>" in ai_response and "</thought>" in ai_response:
            parts = ai_response.split("</thought>")
            ai_response = parts[-1].strip() if parts else ai_response

        if "<reasoning>" in ai_response and "</reasoning>" in ai_response:
            parts = ai_response.split("</reasoning>")
            ai_response = parts[-1].strip() if parts else ai_response

        if "<analysis>" in ai_response and "</analysis>" in ai_response:
            parts = ai_response.split("</analysis>")
            ai_response = parts[-1].strip() if parts else ai_response

        if "<internal_thought>" in ai_response and "</internal_thought>" in ai_response:
            parts = ai_response.split("</internal_thought>")
            ai_response = parts[-1].strip() if parts else ai_response

        if "<reflection>" in ai_response and "</reflection>" in ai_response:
            parts = ai_response.split("</reflection>")
            ai_response = parts[-1].strip() if parts else ai_response

        if "<plan>" in ai_response and "</plan>" in ai_response:
            parts = ai_response.split("</plan>")
            ai_response = parts[-1].strip() if parts else ai_response

        if "<scratchpad>" in ai_response and "</scratchpad>" in ai_response:
            parts = ai_response.split("</scratchpad>")
            ai_response = parts[-1].strip() if parts else ai_response

        # Remove common bracketed content
        if "[thinking]" in ai_response and "[/thinking]" in ai_response:
            parts = ai_response.split("[/thinking]")
            ai_response = parts[-1].strip() if parts else ai_response

        if "[reasoning]" in ai_response and "[/reasoning]" in ai_response:
            parts = ai_response.split("[/reasoning]")
            ai_response = parts[-1].strip() if parts else ai_response

        if "[analysis]" in ai_response and "[/analysis]" in ai_response:
            parts = ai_response.split("[/analysis]")
            ai_response = parts[-1].strip() if parts else ai_response

        # Remove any remaining unwanted content
        if '{"name":' in ai_response and '"arguments":' in ai_response:
            parts = ai_response.split('"arguments":')
            if len(parts) > 1:
                # Get everything after the arguments part
                ai_response = parts[-1].strip()

        # Final cleanup: strip and normalize whitespace
        ai_response = ai_response.strip()
        ai_response = ai_response.replace('\n\n', '\n').replace('\n\n', '\n')  # Handle multiple newlines
        ai_response = ai_response.replace('  ', ' ').replace('  ', ' ')  # Handle multiple spaces
        ai_response = ai_response.strip()

    # Add AI response to conversation
    try:
        ai_message = ai_service.add_message_to_conversation(
            conversation_id=conv_uuid,
            sender_type="ASSISTANT",
            content=ai_response,
            message_type="TEXT",
            commit=False  # Don't commit here, will commit at the end
        )

        # Commit the conversation message as part of the main transaction
        session.commit()
    except Exception as e:
        # Rollback on error to clear failed transaction
        session.rollback()
        print(f"Error saving AI response to conversation: {str(e)}")

    # Check if any tool calls that mutate tasks were processed by OpenRouter
    # The OpenRouter service handles tool execution internally and already fetches updated tasks after mutations
    # We'll assume that if there was a response with task-related language, we should fetch updated tasks
    task_mutation_detected = False

    # Look for signs of task mutations in the AI response
    mutation_keywords = [
        "task added", "task created", "added successfully", "created successfully",
        "task updated", "updated successfully", "changed successfully",
        "task deleted", "removed successfully", "deleted successfully",
        "task completed", "marked as completed", "marked as done", "completed successfully",
        "task marked", "deleted task", "updated task", "added task", "created task"
    ]

    ai_response_lower = ai_response.lower() if ai_response else ""
    for keyword in mutation_keywords:
        if keyword in ai_response_lower:
            task_mutation_detected = True
            break

    # Prepare the response data
    response_data = {
        "response": ai_response,
        "conversation_id": str(conv_uuid),
        "action_performed": task_mutation_detected,
        "tool_calls": [] # This is now empty list, as previously there was tool_calls_results
    }

    # If a task mutation was detected, fetch and include the updated task list
    if task_mutation_detected:
        tasks_result = get_all_tasks(str(current_user.id), session)
        if tasks_result.get("success"):
            response_data["tasks"] = tasks_result.get("tasks", [])
        else:
            print(f"Warning: Failed to fetch updated tasks after mutation: {tasks_result.get('message', 'Unknown error')}")

    return response_data


@router.get("/conversations/{user_id}")
async def get_user_conversations(
    user_id: str,
    limit: int = 10,
    offset: int = 0,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Get all conversations for a user.
    """
    if str(current_user.id) != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this conversation"
        )

    ai_service = AIConversationService(session)
    conversations = ai_service.get_conversations_by_user(
        user_id=current_user.id,
        limit=limit,
        offset=offset
    )

    return {
        "conversations": [
            {
                "id": str(conv.id),
                "title": conv.title,
                "created_at": conv.created_at.isoformat(),
                "updated_at": conv.updated_at.isoformat(),
                "is_active": conv.is_active
            } for conv in conversations
        ],
        "total": len(conversations)
    }


@router.get("/conversations/{conversation_id}/messages")
async def get_conversation_messages(
    conversation_id: str,
    limit: int = 50,
    offset: int = 0,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Get messages from a specific conversation.
    """
    try:
        conv_uuid = uuid.UUID(conversation_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid conversation ID format"
        )

    ai_service = AIConversationService(session)
    conversation = ai_service.get_conversation_by_id(conv_uuid)

    if not conversation or str(conversation.user_id) != str(current_user.id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found or not authorized"
        )

    messages = ai_service.get_messages_by_conversation(
        conversation_id=conv_uuid,
        limit=limit,
        offset=offset
    )

    return {
        "messages": [
            {
                "id": str(msg.id),
                "sender_type": msg.sender_type,
                "content": msg.content,
                "message_type": msg.message_type,
                "created_at": msg.created_at.isoformat(),
                "metadata": msg.extra_metadata
            } for msg in messages
        ],
        "total": len(messages)
    }