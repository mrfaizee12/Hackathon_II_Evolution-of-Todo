import json
from typing import Dict, Any, Optional, List
from openai import OpenAI
from ..database.config import settings
from ..database.database import Session
from ..tools.todo_tools import (
    AddTaskInput, ListTasksInput, UpdateTaskInput,
    CompleteTaskInput, DeleteTaskInput, get_all_tasks
)
from ..tools.user_tools import get_user_identity
from ..services.mcp_tool_server import mcp_server


class OpenRouterService:
    """
    Service class that handles the OpenRouter API integration,
    with enhanced debugging and robust error handling.
    """

    def __init__(self):
        """Initialize the OpenRouter client with the API key."""
        if not settings.openrouter_api_key:
            raise ValueError("OPENROUTER_API_KEY environment variable is required")

        # Verify API Key
        print(f"Using Key: {settings.openrouter_api_key[:5]}...")

        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=settings.openrouter_api_key
        )

        # Session memory to store last fetched task lists per user
        # Format: {user_id: {'cached_tasks': [...], 'timestamp': time, 'context': {'task_number': {'resolved_task_id': 'uuid', 'task_title': 'title'}}}}
        self.session_memory = {}

    def _get_contextual_task_id(self, user_uuid: str, position: int) -> Optional[str]:
        """
        Check session memory for stored context of task number to UUID mapping.
        """
        user_session_key = str(user_uuid)
        if (user_session_key in self.session_memory and
            'context' in self.session_memory[user_session_key] and
            str(position) in self.session_memory[user_session_key]['context']):

            context_entry = self.session_memory[user_session_key]['context'][str(position)]
            # Check if the context is still valid (recent enough)
            import time
            current_time = time.time()
            # Context is valid for 5 minutes (300 seconds)
            if current_time - context_entry.get('timestamp', 0) < 300:
                return context_entry.get('resolved_task_id')

        return None

    def chat_completion(self, messages: List[Dict], tools: Optional[List[Dict]] = None,
                       tool_choice: str = "auto", user_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Use OpenRouter API with enhanced error handling and debugging.

        Args:
            messages: List of messages in the conversation
            tools: Optional list of tools that the AI can use
            tool_choice: How the model should use the provided tools
            user_id: ID of the user for context

        Returns:
            Response containing the final natural language response from the AI
        """
        try:
            # Add debugging
            user_input = messages[-1]['content'] if messages else "No input"
            print(f"User Input: {user_input}")

            headers = {
                "HTTP-Referer": "http://localhost:3000",  # Optional but recommended by OpenRouter
                "X-Title": "Todo Chatbot",               # Optional but recommended by OpenRouter
            }

            # Use the model that bypasses Qwen rate limits
            model = "google/gemini-2.0-flash-001"

            # Make the API call
            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
                tools=tools if tools else None,
                tool_choice=tool_choice if tools else "none",  # Don't specify tool choice if no tools
                extra_headers=headers,
                user=user_id if user_id else "user_default"
            )

            # Extract the actual text response for the frontend
            response_text = response.choices[0].message.content if response.choices and response.choices[0].message.content else "I couldn't process that request."

            result = {
                "success": True,
                "response": response_text
            }
            print(f"Agent Result: {result}")
            return result

        except Exception as e:
            # Enhanced error handling with actual exception details
            print(f"OpenRouter API error: {str(e)}")
            import traceback
            print(f"Full traceback: {traceback.format_exc()}")

            # Return the actual error for debugging
            return {
                "success": False,
                "response": f"Brain Error: {str(e)}"
            }

    def chat_completion_v2(self, messages: List[Dict], tools: Optional[List[Dict]] = None,
                          tool_choice: str = "auto", user_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Robust alternative method with enhanced error handling, tool execution, and proper response parsing.

        Args:
            messages: List of messages in the conversation
            tools: Optional list of tools that the AI can use
            tool_choice: How the model should use the provided tools
            user_id: ID of the user for context

        Returns:
            Response containing the final natural language response from the AI
        """
        try:
            # Add debugging
            user_input = messages[-1]['content'] if messages else "No input"
            print(f"User Input: {user_input}")

            headers = {
                "HTTP-Referer": "http://localhost:3000",  # Optional but recommended by OpenRouter
                "X-Title": "Todo Chatbot",               # Optional but recommended by OpenRouter
            }

            # Ensure instructions are not empty - Enhanced system message
            if not messages or not any(msg.get('content') for msg in messages if msg.get('role') == 'system'):
                # Insert system message if missing
                system_message = {
                    "role": "system",
                    "content": "You are a Todo Manager with session memory. If a user gives a task number (e.g., Task 3), you must FIRST check your session memory for the task list. If not available, call 'get_all_tasks' to see the UUID of Task 3, then use that UUID to perform the requested delete/update action. DO NOT just show the list and stop. You are an Action-Oriented Agent. DO NOT write code blocks or explain how you would use a tool. You MUST directly call the tool using the provided function schema. If you need a UUID, first check session memory, then call 'get_all_tasks' if needed, then immediately call the next tool with the resolved UUID. You are a helpful and professional Todo Manager. Never say 'Processed your request successfully.' Instead, always give a conversational response. Example: 'I've added the task \"buy a car\" to your list!' or 'You have 3 tasks pending: ...'. Always confirm the specific action you took. Before deleting or updating, if the user provides a number (1, 2, 3...), you MUST first check your session memory for the task list, and if not available or outdated, call 'get_all_tasks' to find the corresponding UUID for that specific index. When a user asks to delete or update a task by a simple number (e.g., 'task 1'), check session memory first, then call 'get_all_tasks' if needed, find the UUID for that number in the list, and then use that UUID for the next tool call. Never tell the user you don't have access; you have the tools to get it. Always describe what you did. For example: 'I've updated task 6 for you!' or 'Task 5 has been removed from your list.' The user will speak in Roman Urdu (e.g., 'list dikhao', 'task 2 khatam kar do'). You must understand these commands and respond in a friendly, professional mix of English and Roman Urdu (Hinglish/Urdish). Be helpful, concise, and professional."
                }
                messages = [system_message] + messages

            # Use the model that bypasses Qwen rate limits
            model = "google/gemini-2.0-flash-001"

            # Make the API call
            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
                tools=tools if tools else None,
                tool_choice=tool_choice if tools else "auto",  # Allow auto tool choice for proper execution
                extra_headers=headers,
                user=user_id if user_id else "user_default"
            )

            # Check if there are tool calls that need to be processed
            if response.choices[0].message.tool_calls:
                # Process tool calls and get results - need to get a proper db session
                from ..database.database import get_session
                from uuid import UUID

                # Cast user_id to UUID object for database compatibility
                user_uuid = UUID(user_id) if user_id and isinstance(user_id, str) and len(user_id) > 10 else user_id

                # Use the generator directly since it doesn't support context manager protocol
                db_gen = get_session()
                db_session = next(db_gen)
                try:
                    # Process each tool call
                    tool_results = []

                    # First pass: collect all initial tool calls
                    initial_tool_calls = list(response.choices[0].message.tool_calls)

                    # Process initial tool calls
                    for tool_call in initial_tool_calls:
                        function_name = tool_call.function.name
                        try:
                            arguments = json.loads(tool_call.function.arguments)

                            # Execute the appropriate tool function based on the function name
                            print(f"Executing tool: {function_name} with args: {arguments}")

                            # Handle position-to-UUID conversion for tasks
                            if function_name in ["update_task", "delete_task", "complete_task"] and 'task_id' in arguments:
                                # If task_id is a number (position), get all tasks and map to UUID
                                task_id_str = str(arguments['task_id']).strip()
                                if task_id_str.isdigit():
                                    position = int(task_id_str)

                                    # First, check if we have the task number to UUID mapping in context memory
                                    contextual_task_id = self._get_contextual_task_id(user_uuid, position)
                                    if contextual_task_id:
                                        # Use the stored UUID mapping from context
                                        arguments['task_id'] = contextual_task_id
                                        print(f"Used contextual mapping: position {position} to UUID {contextual_task_id}")
                                    else:
                                        # First, check if we have the task list in session memory
                                        user_session_key = str(user_uuid)
                                        cached_tasks = self.session_memory.get(user_session_key, {}).get('cached_tasks', [])

                                        # Always fetch the latest task list to ensure consistency
                                        import time
                                        current_time = time.time()

                                        # Get all tasks for the user to map position to UUID (always fetch fresh to avoid stale data)
                                        get_all_result = get_all_tasks(str(user_uuid), db_session)
                                        if get_all_result.get("success") and "tasks" in get_all_result:
                                            all_tasks = get_all_result["tasks"]
                                            # Store in session memory
                                            self.session_memory[user_session_key] = {
                                                'cached_tasks': all_tasks,
                                                'timestamp': current_time
                                            }
                                        else:
                                            # Retry mechanism: if we can't get tasks, try again
                                            print("Failed to fetch tasks, attempting retry...")
                                            retry_result = get_all_tasks(str(user_uuid), db_session)
                                            if retry_result.get("success") and "tasks" in retry_result:
                                                all_tasks = retry_result["tasks"]
                                                # Store in session memory
                                                self.session_memory[user_session_key] = {
                                                    'cached_tasks': all_tasks,
                                                    'timestamp': current_time
                                                }
                                            else:
                                                result = {
                                                    "success": False,
                                                    "message": f"Sorry, I couldn't access your task list to map task number {task_id_str}. Please try again."
                                                }
                                                tool_results.append({
                                                    "tool_call_id": tool_call.id,
                                                    "function_name": function_name,
                                                    "result": result
                                                })
                                                continue  # Skip to next tool call

                                        # Adjust for 1-based indexing
                                        if 1 <= position <= len(all_tasks):
                                            actual_task = all_tasks[position - 1]
                                            arguments['task_id'] = actual_task['id']
                                            print(f"Converted position {position} to UUID {actual_task['id']}")

                                            # Store the context for reuse in follow-up messages
                                            user_session_key = str(user_uuid)
                                            if user_session_key not in self.session_memory:
                                                self.session_memory[user_session_key] = {}

                                            if 'context' not in self.session_memory[user_session_key]:
                                                self.session_memory[user_session_key]['context'] = {}

                                            # Store the mapping of task number to UUID and title
                                            self.session_memory[user_session_key]['context'][str(position)] = {
                                                'resolved_task_id': actual_task['id'],
                                                'task_title': actual_task.get('title', 'Untitled'),
                                                'timestamp': time.time()
                                            }
                                        else:
                                            # Retry mechanism: if the position is out of range, try to find the task in a different way
                                            # or provide more helpful error message
                                            result = {
                                                "success": False,
                                                "message": f"Sorry, I couldn't find task number {position}. You currently have {len(all_tasks)} tasks. Please check the task number and try again."
                                            }
                                            tool_results.append({
                                                "tool_call_id": tool_call.id,
                                                "function_name": function_name,
                                                "result": result
                                            })
                                            continue  # Skip to next tool call

                            if function_name == "add_task":
                                input_data = AddTaskInput(**arguments)
                                result = mcp_server.add_task_tool(input_data, str(user_uuid), db_session)
                                # After mutation, always fetch fresh task list to update session memory
                                if result.get("success"):
                                    updated_tasks_result = get_all_tasks(str(user_uuid), db_session)
                                    if updated_tasks_result.get("success") and "tasks" in updated_tasks_result:
                                        user_session_key = str(user_uuid)
                                        import time
                                        self.session_memory[user_session_key] = {
                                            'cached_tasks': updated_tasks_result["tasks"],
                                            'timestamp': time.time()
                                        }
                                        # Add the updated task list to tool results so AI gets the fresh data
                                        updated_list_result = {
                                            "success": True,
                                            "message": "Task added successfully. Here is your updated list:",
                                            "tasks": updated_tasks_result["tasks"]
                                        }
                                        # Add this as a separate tool call result so the AI sees the updated list
                                        tool_results.append({
                                            "tool_call_id": f"refresh_{tool_call.id}",
                                            "function_name": "get_all_tasks",
                                            "result": updated_list_result
                                        })
                            elif function_name == "list_tasks":
                                input_data = ListTasksInput(**arguments)
                                result = mcp_server.list_tasks_tool(input_data, str(user_uuid), db_session)
                            elif function_name == "complete_task":
                                input_data = CompleteTaskInput(**arguments)
                                result = mcp_server.complete_task_tool(input_data, str(user_uuid), db_session)
                                # After mutation, always fetch fresh task list to update session memory
                                if result.get("success"):
                                    updated_tasks_result = get_all_tasks(str(user_uuid), db_session)
                                    if updated_tasks_result.get("success") and "tasks" in updated_tasks_result:
                                        user_session_key = str(user_uuid)
                                        import time
                                        self.session_memory[user_session_key] = {
                                            'cached_tasks': updated_tasks_result["tasks"],
                                            'timestamp': time.time()
                                        }
                                        # Add the updated task list to tool results so AI gets the fresh data
                                        updated_list_result = {
                                            "success": True,
                                            "message": "Task marked as completed! Here is your updated list:",
                                            "tasks": updated_tasks_result["tasks"]
                                        }
                                        # Add this as a separate tool call result so the AI sees the updated list
                                        tool_results.append({
                                            "tool_call_id": f"refresh_{tool_call.id}",
                                            "function_name": "get_all_tasks",
                                            "result": updated_list_result
                                        })
                            elif function_name == "delete_task":
                                input_data = DeleteTaskInput(**arguments)
                                result = mcp_server.delete_task_tool(input_data, str(user_uuid), db_session)
                                # After mutation, always fetch fresh task list to update session memory
                                if result.get("success"):
                                    updated_tasks_result = get_all_tasks(str(user_uuid), db_session)
                                    if updated_tasks_result.get("success") and "tasks" in updated_tasks_result:
                                        user_session_key = str(user_uuid)
                                        import time
                                        self.session_memory[user_session_key] = {
                                            'cached_tasks': updated_tasks_result["tasks"],
                                            'timestamp': time.time()
                                        }
                                        # Add the updated task list to tool results so AI gets the fresh data
                                        updated_list_result = {
                                            "success": True,
                                            "message": "Task deleted successfully. Here is your updated list:",
                                            "tasks": updated_tasks_result["tasks"]
                                        }
                                        # Add this as a separate tool call result so the AI sees the updated list
                                        tool_results.append({
                                            "tool_call_id": f"refresh_{tool_call.id}",
                                            "function_name": "get_all_tasks",
                                            "result": updated_list_result
                                        })
                            elif function_name == "update_task":
                                # Check if the update_task is being used just to change completion status
                                # If so, redirect to complete_task instead
                                # Allow more flexible completion-only updates (not just limited to 2 keys)
                                completion_keys = ['completed']
                                update_keys = set(arguments.keys())
                                remaining_keys = update_keys - {'task_id', 'completed'}

                                # If only task_id and completion-related fields are being updated, redirect to complete_task
                                if 'completed' in arguments and not remaining_keys:
                                    # Redirect to complete_task for status changes
                                    input_data = CompleteTaskInput(task_id=arguments['task_id'], completed=arguments['completed'])
                                    result = mcp_server.complete_task_tool(input_data, str(user_uuid), db_session)
                                else:
                                    # For partial updates (description, priority, etc.), fetch existing task data first
                                    # to ensure we send a complete payload with all required fields
                                    from sqlmodel import select
                                    from ..models.todo import Todo

                                    # Get the existing task to fill in missing required fields
                                    existing_task_stmt = select(Todo).where(Todo.id == arguments['task_id'], Todo.user_id == str(user_uuid))
                                    existing_task = db_session.exec(existing_task_stmt).first()

                                    if existing_task:
                                        # Prepare the full update data with existing values as defaults
                                        full_update_data = {
                                            'task_id': arguments['task_id'],
                                            'title': arguments.get('title', existing_task.title),
                                            'description': arguments.get('description', existing_task.description),
                                            'completed': arguments.get('completed', existing_task.completed),
                                            'priority': arguments.get('priority', existing_task.priority),
                                            'tags': arguments.get('tags', existing_task.tags),
                                            'due_date': arguments.get('due_date', existing_task.due_date.isoformat() if existing_task.due_date else None),
                                            'ai_context': arguments.get('ai_context', existing_task.ai_context)
                                        }

                                        # Remove None values to avoid overwriting with nulls
                                        full_update_data = {k: v for k, v in full_update_data.items() if v is not None}

                                        input_data = UpdateTaskInput(**full_update_data)
                                    else:
                                        # If task doesn't exist, use the original arguments
                                        input_data = UpdateTaskInput(**arguments)

                                    result = mcp_server.update_task_tool(input_data, str(user_uuid), db_session)
                                # After mutation, always fetch fresh task list to update session memory
                                if result.get("success"):
                                    updated_tasks_result = get_all_tasks(str(user_uuid), db_session)
                                    if updated_tasks_result.get("success") and "tasks" in updated_tasks_result:
                                        user_session_key = str(user_uuid)
                                        import time
                                        self.session_memory[user_session_key] = {
                                            'cached_tasks': updated_tasks_result["tasks"],
                                            'timestamp': time.time()
                                        }
                                        # Add the updated task list to tool results so AI gets the fresh data
                                        updated_list_result = {
                                            "success": True,
                                            "message": "Task updated successfully. Here is your updated list:",
                                            "tasks": updated_tasks_result["tasks"]
                                        }
                                        # Add this as a separate tool call result so the AI sees the updated list
                                        tool_results.append({
                                            "tool_call_id": f"refresh_{tool_call.id}",
                                            "function_name": "get_all_tasks",
                                            "result": updated_list_result
                                        })
                            elif function_name == "get_user_identity":
                                result = get_user_identity(str(user_uuid), db_session)
                            elif function_name == "get_all_tasks":
                                result = get_all_tasks(str(user_uuid), db_session)
                                # Store the retrieved tasks in session memory
                                user_session_key = str(user_uuid)
                                import time
                                self.session_memory[user_session_key] = {
                                    'cached_tasks': result.get('tasks', []),
                                    'timestamp': time.time()
                                }
                            else:
                                result = {
                                    "success": False,
                                    "message": f"Unknown function: {function_name}"
                                }

                            # Ensure tool results are not None
                            if result is None:
                                result = {"success": True, "message": "Operation completed successfully", "data": []}

                            tool_results.append({
                                "tool_call_id": tool_call.id,
                                "function_name": function_name,
                                "result": result
                            })

                        except Exception as tool_error:
                            print(f"Tool execution error: {str(tool_error)}")
                            # Return descriptive message instead of failing
                            error_result = {
                                "success": False,
                                "message": f"I couldn't process that request: {str(tool_error)}",
                                "data": []
                            }
                            tool_results.append({
                                "tool_call_id": tool_call.id,
                                "function_name": function_name,
                                "result": error_result
                            })

                    # Check if the first tool call was get_all_tasks and we need to continue with another action
                    # This handles the case where the agent needs to first get the task list and then perform an action
                    if len(initial_tool_calls) == 1 and initial_tool_calls[0].function.name == "get_all_tasks":
                        # After getting the tasks, we need to continue the conversation to determine the next action
                        # Add the tool response to the message history
                        new_messages = messages.copy()

                        # Add the assistant's original message that triggered the tool calls
                        new_messages.append({
                            "role": "assistant",
                            "content": response.choices[0].message.content,
                            "tool_calls": response.choices[0].message.tool_calls
                        })

                        # Add the tool responses so the AI can see the results
                        for tool_result in tool_results:
                            result_content = tool_result["result"]
                            # Ensure we're sending proper JSON-serializable content
                            content_str = json.dumps(result_content) if result_content else json.dumps({"message": "No data returned"})

                            new_messages.append({
                                "role": "tool",
                                "content": content_str,
                                "tool_call_id": tool_result["tool_call_id"]
                            })

                        # Call the AI again to continue the conversation and potentially trigger the next tool call
                        follow_up_response = self.client.chat.completions.create(
                            model=model,
                            messages=new_messages,
                            tools=tools if tools else None,
                            tool_choice=tool_choice if tools else "auto",  # Allow auto tool choice for proper execution
                            extra_headers=headers,
                            user=user_id if user_id else "user_default"
                        )

                        # Check if the follow-up response has additional tool calls
                        if follow_up_response.choices[0].message.tool_calls:
                            # Process the follow-up tool calls
                            follow_up_tool_results = []

                            for tool_call in follow_up_response.choices[0].message.tool_calls:
                                function_name = tool_call.function.name
                                try:
                                    arguments = json.loads(tool_call.function.arguments)

                                    # Execute the appropriate tool function based on the function name
                                    print(f"Executing follow-up tool: {function_name} with args: {arguments}")

                                    # Handle position-to-UUID conversion for tasks
                                    if function_name in ["update_task", "delete_task", "complete_task"] and 'task_id' in arguments:
                                        # If task_id is a number (position), get all tasks and map to UUID
                                        task_id_str = str(arguments['task_id']).strip()
                                        if task_id_str.isdigit():
                                            position = int(task_id_str)

                                            # First, check if we have the task number to UUID mapping in context memory
                                            contextual_task_id = self._get_contextual_task_id(user_uuid, position)
                                            if contextual_task_id:
                                                # Use the stored UUID mapping from context
                                                arguments['task_id'] = contextual_task_id
                                                print(f"Used contextual mapping: position {position} to UUID {contextual_task_id}")
                                            else:
                                                # First, check if we have the task list in session memory
                                                user_session_key = str(user_uuid)
                                                cached_tasks = self.session_memory.get(user_session_key, {}).get('cached_tasks', [])

                                                # Always fetch the latest task list to ensure consistency
                                                import time
                                                current_time = time.time()

                                                # Get all tasks for the user to map position to UUID (always fetch fresh to avoid stale data)
                                                get_all_result = get_all_tasks(str(user_uuid), db_session)
                                                if get_all_result.get("success") and "tasks" in get_all_result:
                                                    all_tasks = get_all_result["tasks"]
                                                    # Store in session memory
                                                    self.session_memory[user_session_key] = {
                                                        'cached_tasks': all_tasks,
                                                        'timestamp': current_time
                                                    }
                                                else:
                                                    # Retry mechanism: if we can't get tasks, try again
                                                    print("Failed to fetch tasks for follow-up, attempting retry...")
                                                    retry_result = get_all_tasks(str(user_uuid), db_session)
                                                    if retry_result.get("success") and "tasks" in retry_result:
                                                        all_tasks = retry_result["tasks"]
                                                        # Store in session memory
                                                        self.session_memory[user_session_key] = {
                                                            'cached_tasks': all_tasks,
                                                            'timestamp': current_time
                                                        }
                                                    else:
                                                        result = {
                                                            "success": False,
                                                            "message": f"Sorry, I couldn't access your task list to map task number {task_id_str}. Please try again."
                                                        }
                                                        follow_up_tool_results.append({
                                                            "tool_call_id": tool_call.id,
                                                            "function_name": function_name,
                                                            "result": result
                                                        })
                                                        continue  # Skip to next tool call

                                                # Adjust for 1-based indexing
                                                if 1 <= position <= len(all_tasks):
                                                    actual_task = all_tasks[position - 1]
                                                    arguments['task_id'] = actual_task['id']
                                                    print(f"Converted position {position} to UUID {actual_task['id']} for follow-up")

                                                    # Store the context for reuse in follow-up messages
                                                    user_session_key = str(user_uuid)
                                                    if user_session_key not in self.session_memory:
                                                        self.session_memory[user_session_key] = {}

                                                    if 'context' not in self.session_memory[user_session_key]:
                                                        self.session_memory[user_session_key]['context'] = {}

                                                    # Store the mapping of task number to UUID and title
                                                    self.session_memory[user_session_key]['context'][str(position)] = {
                                                        'resolved_task_id': actual_task['id'],
                                                        'task_title': actual_task.get('title', 'Untitled'),
                                                        'timestamp': time.time()
                                                    }
                                                else:
                                                    # Retry mechanism: if the position is out of range, try to find the task in a different way
                                                    # or provide more helpful error message
                                                    result = {
                                                        "success": False,
                                                        "message": f"Sorry, I couldn't find task number {position}. You currently have {len(all_tasks)} tasks. Please check the task number and try again."
                                                    }
                                                    follow_up_tool_results.append({
                                                        "tool_call_id": tool_call.id,
                                                        "function_name": function_name,
                                                        "result": result
                                                    })
                                                    continue  # Skip to next tool call

                                    if function_name == "add_task":
                                        input_data = AddTaskInput(**arguments)
                                        result = mcp_server.add_task_tool(input_data, str(user_uuid), db_session)
                                        # After mutation, always fetch fresh task list to update session memory
                                        if result.get("success"):
                                            updated_tasks_result = get_all_tasks(str(user_uuid), db_session)
                                            if updated_tasks_result.get("success") and "tasks" in updated_tasks_result:
                                                user_session_key = str(user_uuid)
                                                import time
                                                self.session_memory[user_session_key] = {
                                                    'cached_tasks': updated_tasks_result["tasks"],
                                                    'timestamp': time.time()
                                                }
                                                # Add the updated task list to tool results so AI gets the fresh data
                                                updated_list_result = {
                                                    "success": True,
                                                    "message": "Task added successfully. Here is your updated list:",
                                                    "tasks": updated_tasks_result["tasks"]
                                                }
                                                # Add this as a separate tool call result so the AI sees the updated list
                                                follow_up_tool_results.append({
                                                    "tool_call_id": f"refresh_{tool_call.id}",
                                                    "function_name": "get_all_tasks",
                                                    "result": updated_list_result
                                                })
                                    elif function_name == "list_tasks":
                                        input_data = ListTasksInput(**arguments)
                                        result = mcp_server.list_tasks_tool(input_data, str(user_uuid), db_session)
                                    elif function_name == "complete_task":
                                        input_data = CompleteTaskInput(**arguments)
                                        result = mcp_server.complete_task_tool(input_data, str(user_uuid), db_session)
                                        # After mutation, always fetch fresh task list to update session memory
                                        if result.get("success"):
                                            updated_tasks_result = get_all_tasks(str(user_uuid), db_session)
                                            if updated_tasks_result.get("success") and "tasks" in updated_tasks_result:
                                                user_session_key = str(user_uuid)
                                                import time
                                                self.session_memory[user_session_key] = {
                                                    'cached_tasks': updated_tasks_result["tasks"],
                                                    'timestamp': time.time()
                                                }
                                                # Add the updated task list to tool results so AI gets the fresh data
                                                updated_list_result = {
                                                    "success": True,
                                                    "message": "Task marked as completed! Here is your updated list:",
                                                    "tasks": updated_tasks_result["tasks"]
                                                }
                                                # Add this as a separate tool call result so the AI sees the updated list
                                                follow_up_tool_results.append({
                                                    "tool_call_id": f"refresh_{tool_call.id}",
                                                    "function_name": "get_all_tasks",
                                                    "result": updated_list_result
                                                })
                                    elif function_name == "delete_task":
                                        input_data = DeleteTaskInput(**arguments)
                                        result = mcp_server.delete_task_tool(input_data, str(user_uuid), db_session)
                                        # After mutation, always fetch fresh task list to update session memory
                                        if result.get("success"):
                                            updated_tasks_result = get_all_tasks(str(user_uuid), db_session)
                                            if updated_tasks_result.get("success") and "tasks" in updated_tasks_result:
                                                user_session_key = str(user_uuid)
                                                import time
                                                self.session_memory[user_session_key] = {
                                                    'cached_tasks': updated_tasks_result["tasks"],
                                                    'timestamp': time.time()
                                                }
                                                # Add the updated task list to tool results so AI gets the fresh data
                                                updated_list_result = {
                                                    "success": True,
                                                    "message": "Task deleted successfully. Here is your updated list:",
                                                    "tasks": updated_tasks_result["tasks"]
                                                }
                                                # Add this as a separate tool call result so the AI sees the updated list
                                                follow_up_tool_results.append({
                                                    "tool_call_id": f"refresh_{tool_call.id}",
                                                    "function_name": "get_all_tasks",
                                                    "result": updated_list_result
                                                })
                                    elif function_name == "update_task":
                                        # Check if the update_task is being used just to change completion status
                                        # If so, redirect to complete_task instead
                                        # Allow more flexible completion-only updates (not just limited to 2 keys)
                                        completion_keys = ['completed']
                                        update_keys = set(arguments.keys())
                                        remaining_keys = update_keys - {'task_id', 'completed'}

                                        # If only task_id and completion-related fields are being updated, redirect to complete_task
                                        if 'completed' in arguments and not remaining_keys:
                                            # Redirect to complete_task for status changes
                                            input_data = CompleteTaskInput(task_id=arguments['task_id'], completed=arguments['completed'])
                                            result = mcp_server.complete_task_tool(input_data, str(user_uuid), db_session)
                                        else:
                                            # For partial updates (description, priority, etc.), fetch existing task data first
                                            # to ensure we send a complete payload with all required fields
                                            from sqlmodel import select
                                            from ..models.todo import Todo

                                            # Get the existing task to fill in missing required fields
                                            existing_task_stmt = select(Todo).where(Todo.id == arguments['task_id'], Todo.user_id == str(user_uuid))
                                            existing_task = db_session.exec(existing_task_stmt).first()

                                            if existing_task:
                                                # Prepare the full update data with existing values as defaults
                                                full_update_data = {
                                                    'task_id': arguments['task_id'],
                                                    'title': arguments.get('title', existing_task.title),
                                                    'description': arguments.get('description', existing_task.description),
                                                    'completed': arguments.get('completed', existing_task.completed),
                                                    'priority': arguments.get('priority', existing_task.priority),
                                                    'tags': arguments.get('tags', existing_task.tags),
                                                    'due_date': arguments.get('due_date', existing_task.due_date.isoformat() if existing_task.due_date else None),
                                                    'ai_context': arguments.get('ai_context', existing_task.ai_context)
                                                }

                                                # Remove None values to avoid overwriting with nulls
                                                full_update_data = {k: v for k, v in full_update_data.items() if v is not None}

                                                input_data = UpdateTaskInput(**full_update_data)
                                            else:
                                                # If task doesn't exist, use the original arguments
                                                input_data = UpdateTaskInput(**arguments)

                                            result = mcp_server.update_task_tool(input_data, str(user_uuid), db_session)
                                            # After mutation, always fetch fresh task list to update session memory
                                            if result.get("success"):
                                                updated_tasks_result = get_all_tasks(str(user_uuid), db_session)
                                                if updated_tasks_result.get("success") and "tasks" in updated_tasks_result:
                                                    user_session_key = str(user_uuid)
                                                    import time
                                                    self.session_memory[user_session_key] = {
                                                        'cached_tasks': updated_tasks_result["tasks"],
                                                        'timestamp': time.time()
                                                    }
                                                    # Add the updated task list to tool results so AI gets the fresh data
                                                    updated_list_result = {
                                                        "success": True,
                                                        "message": "Task updated successfully. Here is your updated list:",
                                                        "tasks": updated_tasks_result["tasks"]
                                                    }
                                                    # Add this as a separate tool call result so the AI sees the updated list
                                                    follow_up_tool_results.append({
                                                        "tool_call_id": f"refresh_{tool_call.id}",
                                                        "function_name": "get_all_tasks",
                                                        "result": updated_list_result
                                                    })
                                    elif function_name == "get_user_identity":
                                        result = get_user_identity(str(user_uuid), db_session)
                                    elif function_name == "get_all_tasks":
                                        result = get_all_tasks(str(user_uuid), db_session)
                                        # Store the retrieved tasks in session memory
                                        user_session_key = str(user_uuid)
                                        import time
                                        self.session_memory[user_session_key] = {
                                            'cached_tasks': result.get('tasks', []),
                                            'timestamp': time.time()
                                        }
                                    else:
                                        result = {
                                            "success": False,
                                            "message": f"Unknown function: {function_name}"
                                        }

                                    # Ensure tool results are not None
                                    if result is None:
                                        result = {"success": True, "message": "Operation completed successfully", "data": []}

                                    follow_up_tool_results.append({
                                        "tool_call_id": tool_call.id,
                                        "function_name": function_name,
                                        "result": result
                                    })

                                except Exception as tool_error:
                                    print(f"Follow-up tool execution error: {str(tool_error)}")
                                    # Return descriptive message instead of failing
                                    error_result = {
                                        "success": False,
                                        "message": f"I couldn't process that request: {str(tool_error)}",
                                        "data": []
                                    }
                                    follow_up_tool_results.append({
                                        "tool_call_id": tool_call.id,
                                        "function_name": function_name,
                                        "result": error_result
                                    })

                            # Combine results for final response
                            all_tool_results = tool_results + follow_up_tool_results

                            # Create new messages list with follow-up tool responses for the AI to see
                            final_messages = new_messages.copy()

                            # Add the follow-up assistant's message that triggered the follow-up tool calls
                            final_messages.append({
                                "role": "assistant",
                                "content": follow_up_response.choices[0].message.content,
                                "tool_calls": follow_up_response.choices[0].message.tool_calls
                            })

                            # Add the follow-up tool responses so the AI can see the results
                            for tool_result in follow_up_tool_results:
                                result_content = tool_result["result"]
                                # Ensure we're sending proper JSON-serializable content
                                content_str = json.dumps(result_content) if result_content else json.dumps({"message": "No data returned"})

                                final_messages.append({
                                    "role": "tool",
                                    "content": content_str,
                                    "tool_call_id": tool_result["tool_call_id"]
                                })

                            # Call the AI again to get the final formatted response based on tool results
                            final_response = self.client.chat.completions.create(
                                model=model,
                                messages=final_messages,
                                tools=tools if tools else None,
                                tool_choice="none",  # Don't call tools again in the follow-up
                                extra_headers=headers,
                                user=user_id if user_id else "user_default"
                            )

                            # Extract the final output text - ensure it's conversational and not robotic
                            final_output = final_response.choices[0].message.content if final_response.choices and final_response.choices[0].message.content else "I've completed your request."

                            # Clean up any hallucinated code blocks or Python syntax that might be generated
                            if final_output:
                                # Remove any Python code block markers
                                import re
                                final_output = re.sub(r'```python\s*\n.*?\n```', '', final_output, flags=re.DOTALL)
                                final_output = re.sub(r'```\s*python.*?\n```', '', final_output, flags=re.DOTALL)
                                final_output = re.sub(r'```.*?\n```', '', final_output, flags=re.DOTALL)

                                # Remove any standalone triple backticks
                                final_output = final_output.replace('```', '')

                                # Remove any Python-specific syntax that might be hallucinated
                                final_output = re.sub(r'#.*$', '', final_output, flags=re.MULTILINE)  # Remove Python comments
                                final_output = re.sub(r'^\s*[a-zA-Z_][a-zA-Z0-9_]*\s*=', '', final_output, flags=re.MULTILINE)  # Remove variable assignments

                                # Strip extra whitespace
                                final_output = final_output.strip()

                            # Ensure final_output is never empty and not robotic
                            if not final_output or final_output.strip() == "" or final_output.strip() == "Processed your request successfully." or final_output.strip() == "I've completed your request." or final_output.strip() == "I processed your request.":
                                # Build a more specific response based on the tool results
                                success_operations = [tr for tr in all_tool_results if tr["result"].get("success")]

                                if success_operations:
                                    # Create a specific response based on the operation performed
                                    specific_response_found = False
                                    for op in success_operations:
                                        func_name = op["function_name"]
                                        result_data = op["result"]

                                        if func_name == "add_task" and result_data.get("success"):
                                            final_output = f"✅ I've added the task \"{result_data.get('task_title', 'your task')}\" to your list!"
                                            # Always fetch the updated task list after adding a task
                                            updated_tasks_result = get_all_tasks(str(user_uuid), db_session)
                                            if updated_tasks_result.get("success") and "tasks" in updated_tasks_result:
                                                task_list = updated_tasks_result["tasks"]
                                                if task_list:
                                                    task_list_text = "\n".join([f"{i+1}) {task.get('title', 'Untitled')} — {'Completed' if task.get('completed') else 'Pending'}" for i, task in enumerate(task_list)])
                                                    final_output += f"\n\nHere's your updated task list:\n{task_list_text}"

                                                    # Update session memory with the new task list
                                                    user_session_key = str(user_uuid)
                                                    import time
                                                    self.session_memory[user_session_key] = {
                                                        'cached_tasks': task_list,
                                                        'timestamp': time.time()
                                                    }
                                            specific_response_found = True
                                            break
                                        elif func_name == "update_task" and result_data.get("success"):
                                            # Get the updated task list to show to the user
                                            updated_tasks_result = get_all_tasks(str(user_uuid), db_session)
                                            if updated_tasks_result.get("success") and "tasks" in updated_tasks_result:
                                                task_list = updated_tasks_result["tasks"]
                                                if task_list:
                                                    # Find which task was updated by looking at the task_id
                                                    updated_task_id = result_data.get("task_id")
                                                    task_number = "?"
                                                    for idx, task in enumerate(task_list):
                                                        if task.get("id") == updated_task_id:
                                                            task_number = idx + 1
                                                            break

                                                    final_output = f"✏️ I've updated task #{task_number} for you!"

                                                    # Include the updated task list
                                                    task_list_text = "\n".join([f"{i+1}) {task.get('title', 'Untitled')} — {'Completed' if task.get('completed') else 'Pending'}" for i, task in enumerate(task_list)])
                                                    final_output += f"\n\nHere's your updated task list:\n{task_list_text}"

                                                    # Update session memory with the new task list
                                                    user_session_key = str(user_uuid)
                                                    import time
                                                    self.session_memory[user_session_key] = {
                                                        'cached_tasks': task_list,
                                                        'timestamp': time.time()
                                                    }
                                                else:
                                                    final_output = "✏️ I've updated the task for you! Your task list is now empty."
                                            else:
                                                final_output = "✏️ I've updated the task for you!"
                                            specific_response_found = True
                                            break
                                        elif func_name == "delete_task" and result_data.get("success"):
                                            # Get the updated task list to show to the user
                                            updated_tasks_result = get_all_tasks(str(user_uuid), db_session)
                                            if updated_tasks_result.get("success") and "tasks" in updated_tasks_result:
                                                task_list = updated_tasks_result["tasks"]
                                                if task_list:
                                                    task_list_text = "\n".join([f"{i+1}) {task.get('title', 'Untitled')} — {'Completed' if task.get('completed') else 'Pending'}" for i, task in enumerate(task_list)])
                                                    final_output = f"🗑️ Task has been removed from your list!\n\nHere's your updated task list:\n{task_list_text}"

                                                    # Update session memory with the new task list
                                                    user_session_key = str(user_uuid)
                                                    import time
                                                    self.session_memory[user_session_key] = {
                                                        'cached_tasks': task_list,
                                                        'timestamp': time.time()
                                                    }
                                                else:
                                                    final_output = "🗑️ Task has been removed from your list!\n\nYour task list is now empty."
                                            else:
                                                final_output = "🗑️ Task has been removed from your list!"
                                            specific_response_found = True
                                            break
                                        elif func_name == "complete_task" and result_data.get("success"):
                                            status_text = "completed" if result_data.get("completed", True) else "marked as incomplete"

                                            # Get the updated task list to show to the user
                                            updated_tasks_result = get_all_tasks(str(user_uuid), db_session)
                                            if updated_tasks_result.get("success") and "tasks" in updated_tasks_result:
                                                task_list = updated_tasks_result["tasks"]
                                                if task_list:
                                                    task_list_text = "\n".join([f"{i+1}) {task.get('title', 'Untitled')} — {'Completed' if task.get('completed') else 'Pending'}" for i, task in enumerate(task_list)])
                                                    final_output = f"✅ Task has been {status_text}!\n\nHere's your updated task list:\n{task_list_text}"

                                                    # Update session memory with the new task list
                                                    user_session_key = str(user_uuid)
                                                    import time
                                                    self.session_memory[user_session_key] = {
                                                        'cached_tasks': task_list,
                                                        'timestamp': time.time()
                                                    }
                                                else:
                                                    final_output = f"✅ Task has been {status_text}!\n\nYour task list is now empty."
                                            else:
                                                final_output = f"✅ Task has been {status_text}!"
                                            specific_response_found = True
                                            break
                                        elif func_name == "list_tasks" and result_data.get("success"):
                                            task_list = result_data.get("tasks", [])
                                            if task_list:
                                                task_list_text = "\n".join([f"{i+1}) {task.get('title', 'Untitled')} — {'Completed' if task.get('completed') else 'Pending'}" for i, task in enumerate(task_list)])
                                                final_output = f"You have {len(task_list)} tasks:\n{task_list_text}"

                                                # Update session memory with the new task list
                                                user_session_key = str(user_uuid)
                                                import time
                                                self.session_memory[user_session_key] = {
                                                    'cached_tasks': task_list,
                                                    'timestamp': time.time()
                                                }
                                            else:
                                                final_output = "You don't have any tasks right now."
                                            specific_response_found = True
                                            break
                                        elif func_name == "get_all_tasks" and result_data.get("success"):
                                            task_list = result_data.get("tasks", [])
                                            if task_list:
                                                task_list_text = "\n".join([f"{i+1}) {task.get('title', 'Untitled')} — {'Completed' if task.get('completed') else 'Pending'}" for i, task in enumerate(task_list)])
                                                final_output = f"Here are your {len(task_list)} tasks:\n{task_list_text}"

                                                # Update session memory with the new task list
                                                user_session_key = str(user_uuid)
                                                import time
                                                self.session_memory[user_session_key] = {
                                                    'cached_tasks': task_list,
                                                    'timestamp': time.time()
                                                }
                                            else:
                                                final_output = "You don't have any tasks right now."
                                            specific_response_found = True
                                            break

                                    if not specific_response_found:
                                        # If no specific operation message was generated, use a default
                                        final_output = "I've handled your request. Let me know if you need anything else!"
                                else:
                                    # If no successful operations, use error response from the first failed operation
                                    failed_ops = [tr for tr in all_tool_results if not tr["result"].get("success")]
                                    if failed_ops:
                                        error_msg = failed_ops[0]["result"].get("message", "I'm having trouble processing your request right now.")
                                        failed_func_name = failed_ops[0]["function_name"]

                                        # Check if update_task failed due to missing required fields
                                        if failed_func_name == "update_task" and ("missing" in error_msg.lower() or "required" in error_msg.lower() or "title" in error_msg.lower()):
                                            # Extract task ID from the failed operation
                                            failed_task_id = failed_ops[0].get("result", {}).get("task_id", "unknown")

                                            # Ask user for missing fields instead of falling back to add_task
                                            final_output = f"I need more information to update the task. Could you please provide the missing details like title, description, or other fields you'd like to update for task {failed_task_id}?"
                                        # Retry mechanism: if parsing failed, suggest user rephrase or try again
                                        elif "couldn't find task number" in error_msg or "access your task list" in error_msg:
                                            # Fetch the current task list to help the user
                                            current_tasks_result = get_all_tasks(str(user_uuid), db_session)
                                            if current_tasks_result.get("success") and "tasks" in current_tasks_result and current_tasks_result["tasks"]:
                                                task_list = current_tasks_result["tasks"]
                                                task_list_text = "\n".join([f"{i+1}) {task.get('title', 'Untitled')} — {'Completed' if task.get('completed') else 'Pending'}" for i, task in enumerate(task_list)])
                                                final_output = f"{error_msg}\n\nHere's your current task list to help you reference the correct task numbers:\n{task_list_text}"

                                                # Update session memory with the new task list
                                                user_session_key = str(user_uuid)
                                                import time
                                                self.session_memory[user_session_key] = {
                                                    'cached_tasks': task_list,
                                                    'timestamp': time.time()
                                                }
                                            else:
                                                final_output = f"{error_msg}\n\nPlease check your command and try again, making sure to use the correct task number from your list."
                                        else:
                                            final_output = f"I'm having trouble with that request: {error_msg}\n\nPlease try rephrasing your request or check your task numbers."
                                    else:
                                        final_output = "I've handled your request. Let me know if you need anything else!"
                        else:
                            # No follow-up tool calls, process normally
                            # Call the AI again to get the final formatted response based on tool results
                            final_response = self.client.chat.completions.create(
                                model=model,
                                messages=new_messages,
                                tools=tools if tools else None,
                                tool_choice="none",  # Don't call tools again in the follow-up
                                extra_headers=headers,
                                user=user_id if user_id else "user_default"
                            )

                            # Extract the final output text - ensure it's conversational and not robotic
                            final_output = final_response.choices[0].message.content if final_response.choices and final_response.choices[0].message.content else "I've completed your request."

                            # Clean up any hallucinated code blocks or Python syntax that might be generated
                            if final_output:
                                # Remove any Python code block markers
                                import re
                                final_output = re.sub(r'```python\s*\n.*?\n```', '', final_output, flags=re.DOTALL)
                                final_output = re.sub(r'```\s*python.*?\n```', '', final_output, flags=re.DOTALL)
                                final_output = re.sub(r'```.*?\n```', '', final_output, flags=re.DOTALL)

                                # Remove any standalone triple backticks
                                final_output = final_output.replace('```', '')

                                # Remove any Python-specific syntax that might be hallucinated
                                final_output = re.sub(r'#.*$', '', final_output, flags=re.MULTILINE)  # Remove Python comments
                                final_output = re.sub(r'^\s*[a-zA-Z_][a-zA-Z0-9_]*\s*=', '', final_output, flags=re.MULTILINE)  # Remove variable assignments

                                # Strip extra whitespace
                                final_output = final_output.strip()

                            # Ensure final_output is never empty and not robotic
                            if not final_output or final_output.strip() == "" or final_output.strip() == "Processed your request successfully." or final_output.strip() == "I've completed your request." or final_output.strip() == "I processed your request.":
                                # Build a more specific response based on the tool results
                                success_operations = [tr for tr in tool_results if tr["result"].get("success")]

                                if success_operations:
                                    # Create a specific response based on the operation performed
                                    specific_response_found = False
                                    for op in success_operations:
                                        func_name = op["function_name"]
                                        result_data = op["result"]

                                        if func_name == "add_task" and result_data.get("success"):
                                            final_output = f"✅ I've added the task \"{result_data.get('task_title', 'your task')}\" to your list!"
                                            # Always fetch the updated task list after adding a task
                                            updated_tasks_result = get_all_tasks(str(user_uuid), db_session)
                                            if updated_tasks_result.get("success") and "tasks" in updated_tasks_result:
                                                task_list = updated_tasks_result["tasks"]
                                                if task_list:
                                                    task_list_text = "\n".join([f"{i+1}) {task.get('title', 'Untitled')} — {'Completed' if task.get('completed') else 'Pending'}" for i, task in enumerate(task_list)])
                                                    final_output += f"\n\nHere's your updated task list:\n{task_list_text}"

                                                    # Update session memory with the new task list
                                                    user_session_key = str(user_uuid)
                                                    import time
                                                    self.session_memory[user_session_key] = {
                                                        'cached_tasks': task_list,
                                                        'timestamp': time.time()
                                                    }
                                            specific_response_found = True
                                            break
                                        elif func_name == "update_task" and result_data.get("success"):
                                            # Get the updated task list to show to the user
                                            updated_tasks_result = get_all_tasks(str(user_uuid), db_session)
                                            if updated_tasks_result.get("success") and "tasks" in updated_tasks_result:
                                                task_list = updated_tasks_result["tasks"]
                                                if task_list:
                                                    # Find which task was updated by looking at the task_id
                                                    updated_task_id = result_data.get("task_id")
                                                    task_number = "?"
                                                    for idx, task in enumerate(task_list):
                                                        if task.get("id") == updated_task_id:
                                                            task_number = idx + 1
                                                            break

                                                    final_output = f"✏️ I've updated task #{task_number} for you!"

                                                    # Include the updated task list
                                                    task_list_text = "\n".join([f"{i+1}) {task.get('title', 'Untitled')} — {'Completed' if task.get('completed') else 'Pending'}" for i, task in enumerate(task_list)])
                                                    final_output += f"\n\nHere's your updated task list:\n{task_list_text}"

                                                    # Update session memory with the new task list
                                                    user_session_key = str(user_uuid)
                                                    import time
                                                    self.session_memory[user_session_key] = {
                                                        'cached_tasks': task_list,
                                                        'timestamp': time.time()
                                                    }
                                                else:
                                                    final_output = "✏️ I've updated the task for you! Your task list is now empty."
                                            else:
                                                final_output = "✏️ I've updated the task for you!"
                                            specific_response_found = True
                                            break
                                        elif func_name == "delete_task" and result_data.get("success"):
                                            # Get the updated task list to show to the user
                                            updated_tasks_result = get_all_tasks(str(user_uuid), db_session)
                                            if updated_tasks_result.get("success") and "tasks" in updated_tasks_result:
                                                task_list = updated_tasks_result["tasks"]
                                                if task_list:
                                                    task_list_text = "\n".join([f"{i+1}) {task.get('title', 'Untitled')} — {'Completed' if task.get('completed') else 'Pending'}" for i, task in enumerate(task_list)])
                                                    final_output = f"🗑️ Task has been removed from your list!\n\nHere's your updated task list:\n{task_list_text}"

                                                    # Update session memory with the new task list
                                                    user_session_key = str(user_uuid)
                                                    import time
                                                    self.session_memory[user_session_key] = {
                                                        'cached_tasks': task_list,
                                                        'timestamp': time.time()
                                                    }
                                                else:
                                                    final_output = "🗑️ Task has been removed from your list!\n\nYour task list is now empty."
                                            else:
                                                final_output = "🗑️ Task has been removed from your list!"
                                            specific_response_found = True
                                            break
                                        elif func_name == "complete_task" and result_data.get("success"):
                                            status_text = "completed" if result_data.get("completed", True) else "marked as incomplete"

                                            # Get the updated task list to show to the user
                                            updated_tasks_result = get_all_tasks(str(user_uuid), db_session)
                                            if updated_tasks_result.get("success") and "tasks" in updated_tasks_result:
                                                task_list = updated_tasks_result["tasks"]
                                                if task_list:
                                                    task_list_text = "\n".join([f"{i+1}) {task.get('title', 'Untitled')} — {'Completed' if task.get('completed') else 'Pending'}" for i, task in enumerate(task_list)])
                                                    final_output = f"✅ Task has been {status_text}!\n\nHere's your updated task list:\n{task_list_text}"

                                                    # Update session memory with the new task list
                                                    user_session_key = str(user_uuid)
                                                    import time
                                                    self.session_memory[user_session_key] = {
                                                        'cached_tasks': task_list,
                                                        'timestamp': time.time()
                                                    }
                                                else:
                                                    final_output = f"✅ Task has been {status_text}!\n\nYour task list is now empty."
                                            else:
                                                final_output = f"✅ Task has been {status_text}!"
                                            specific_response_found = True
                                            break
                                        elif func_name == "list_tasks" and result_data.get("success"):
                                            task_list = result_data.get("tasks", [])
                                            if task_list:
                                                task_list_text = "\n".join([f"{i+1}) {task.get('title', 'Untitled')} — {'Completed' if task.get('completed') else 'Pending'}" for i, task in enumerate(task_list)])
                                                final_output = f"You have {len(task_list)} tasks:\n{task_list_text}"

                                                # Update session memory with the new task list
                                                user_session_key = str(user_uuid)
                                                import time
                                                self.session_memory[user_session_key] = {
                                                    'cached_tasks': task_list,
                                                    'timestamp': time.time()
                                                }
                                            else:
                                                final_output = "You don't have any tasks right now."
                                            specific_response_found = True
                                            break
                                        elif func_name == "get_all_tasks" and result_data.get("success"):
                                            task_list = result_data.get("tasks", [])
                                            if task_list:
                                                task_list_text = "\n".join([f"{i+1}) {task.get('title', 'Untitled')} — {'Completed' if task.get('completed') else 'Pending'}" for i, task in enumerate(task_list)])
                                                final_output = f"Here are your {len(task_list)} tasks:\n{task_list_text}"

                                                # Update session memory with the new task list
                                                user_session_key = str(user_uuid)
                                                import time
                                                self.session_memory[user_session_key] = {
                                                    'cached_tasks': task_list,
                                                    'timestamp': time.time()
                                                }
                                            else:
                                                final_output = "You don't have any tasks right now."
                                            specific_response_found = True
                                            break

                                    if not specific_response_found:
                                        # If no specific operation message was generated, use a default
                                        final_output = "I've handled your request. Let me know if you need anything else!"
                                else:
                                    # If no successful operations, use error response from the first failed operation
                                    failed_ops = [tr for tr in tool_results if not tr["result"].get("success")]
                                    if failed_ops:
                                        error_msg = failed_ops[0]["result"].get("message", "I'm having trouble processing your request right now.")

                                        # Retry mechanism: if parsing failed, suggest user rephrase or try again
                                        if "couldn't find task number" in error_msg or "access your task list" in error_msg:
                                            # Fetch the current task list to help the user
                                            current_tasks_result = get_all_tasks(str(user_uuid), db_session)
                                            if current_tasks_result.get("success") and "tasks" in current_tasks_result and current_tasks_result["tasks"]:
                                                task_list = current_tasks_result["tasks"]
                                                task_list_text = "\n".join([f"{i+1}) {task.get('title', 'Untitled')} — {'Completed' if task.get('completed') else 'Pending'}" for i, task in enumerate(task_list)])
                                                final_output = f"{error_msg}\n\nHere's your current task list to help you reference the correct task numbers:\n{task_list_text}"

                                                # Update session memory with the new task list
                                                user_session_key = str(user_uuid)
                                                import time
                                                self.session_memory[user_session_key] = {
                                                    'cached_tasks': task_list,
                                                    'timestamp': time.time()
                                                }
                                            else:
                                                final_output = f"{error_msg}\n\nPlease check your command and try again, making sure to use the correct task number from your list."
                                        else:
                                            final_output = f"I'm having trouble with that request: {error_msg}\n\nPlease try rephrasing your request or check your task numbers."
                                    else:
                                        final_output = "I've handled your request. Let me know if you need anything else!"
                    else:
                        # Normal flow with initial tool calls only
                        # Create new messages list with tool responses for the AI to see
                        new_messages = messages.copy()

                        # Add the assistant's original message that triggered the tool calls
                        new_messages.append({
                            "role": "assistant",
                            "content": response.choices[0].message.content,
                            "tool_calls": response.choices[0].message.tool_calls
                        })

                        # Add the tool responses so the AI can see the results
                        for tool_result in tool_results:
                            result_content = tool_result["result"]
                            # Ensure we're sending proper JSON-serializable content
                            content_str = json.dumps(result_content) if result_content else json.dumps({"message": "No data returned"})

                            new_messages.append({
                                "role": "tool",
                                "content": content_str,
                                "tool_call_id": tool_result["tool_call_id"]
                            })

                        # Call the AI again to get the final formatted response based on tool results
                        final_response = self.client.chat.completions.create(
                            model=model,
                            messages=new_messages,
                            tools=tools if tools else None,
                            tool_choice="none",  # Don't call tools again in the follow-up
                            extra_headers=headers,
                            user=user_id if user_id else "user_default"
                        )

                        # Extract the final output text - ensure it's conversational and not robotic
                        final_output = final_response.choices[0].message.content if final_response.choices and final_response.choices[0].message.content else "I've completed your request."

                        # Clean up any hallucinated code blocks or Python syntax that might be generated
                        if final_output:
                            # Remove any Python code block markers
                            import re
                            final_output = re.sub(r'```python\s*\n.*?\n```', '', final_output, flags=re.DOTALL)
                            final_output = re.sub(r'```\s*python.*?\n```', '', final_output, flags=re.DOTALL)
                            final_output = re.sub(r'```.*?\n```', '', final_output, flags=re.DOTALL)

                            # Remove any standalone triple backticks
                            final_output = final_output.replace('```', '')

                            # Remove any Python-specific syntax that might be hallucinated
                            final_output = re.sub(r'#.*$', '', final_output, flags=re.MULTILINE)  # Remove Python comments
                            final_output = re.sub(r'^\s*[a-zA-Z_][a-zA-Z0-9_]*\s*=', '', final_output, flags=re.MULTILINE)  # Remove variable assignments

                            # Strip extra whitespace
                            final_output = final_output.strip()

                        # Ensure final_output is never empty and not robotic
                        if not final_output or final_output.strip() == "" or final_output.strip() == "Processed your request successfully." or final_output.strip() == "I've completed your request." or final_output.strip() == "I processed your request.":
                            # Build a more specific response based on the tool results
                            success_operations = [tr for tr in tool_results if tr["result"].get("success")]

                            if success_operations:
                                # Create a specific response based on the operation performed
                                specific_response_found = False
                                for op in success_operations:
                                    func_name = op["function_name"]
                                    result_data = op["result"]

                                    if func_name == "add_task" and result_data.get("success"):
                                        final_output = f"✅ I've added the task \"{result_data.get('task_title', 'your task')}\" to your list!"
                                        # Always fetch the updated task list after adding a task
                                        updated_tasks_result = get_all_tasks(str(user_uuid), db_session)
                                        if updated_tasks_result.get("success") and "tasks" in updated_tasks_result:
                                            task_list = updated_tasks_result["tasks"]
                                            if task_list:
                                                task_list_text = "\n".join([f"{i+1}) {task.get('title', 'Untitled')} — {'Completed' if task.get('completed') else 'Pending'}" for i, task in enumerate(task_list)])
                                                final_output += f"\n\nHere's your updated task list:\n{task_list_text}"

                                                # Update session memory with the new task list
                                                user_session_key = str(user_uuid)
                                                import time
                                                self.session_memory[user_session_key] = {
                                                    'cached_tasks': task_list,
                                                    'timestamp': time.time()
                                                }
                                        specific_response_found = True
                                        break
                                    elif func_name == "update_task" and result_data.get("success"):
                                        # Get the updated task list to show to the user
                                        updated_tasks_result = get_all_tasks(str(user_uuid), db_session)
                                        if updated_tasks_result.get("success") and "tasks" in updated_tasks_result:
                                            task_list = updated_tasks_result["tasks"]
                                            if task_list:
                                                # Find which task was updated by looking at the task_id
                                                updated_task_id = result_data.get("task_id")
                                                task_number = "?"
                                                for idx, task in enumerate(task_list):
                                                    if task.get("id") == updated_task_id:
                                                        task_number = idx + 1
                                                        break

                                                final_output = f"✏️ I've updated task #{task_number} for you!"

                                                # Include the updated task list
                                                task_list_text = "\n".join([f"{i+1}) {task.get('title', 'Untitled')} — {'Completed' if task.get('completed') else 'Pending'}" for i, task in enumerate(task_list)])
                                                final_output += f"\n\nHere's your updated task list:\n{task_list_text}"
                                            else:
                                                final_output = "✏️ I've updated the task for you! Your task list is now empty."
                                        else:
                                            final_output = "✏️ I've updated the task for you!"
                                        specific_response_found = True
                                        break
                                    elif func_name == "delete_task" and result_data.get("success"):
                                        # Get the updated task list to show to the user
                                        updated_tasks_result = get_all_tasks(str(user_uuid), db_session)
                                        if updated_tasks_result.get("success") and "tasks" in updated_tasks_result:
                                            task_list = updated_tasks_result["tasks"]
                                            if task_list:
                                                task_list_text = "\n".join([f"{i+1}) {task.get('title', 'Untitled')} — {'Completed' if task.get('completed') else 'Pending'}" for i, task in enumerate(task_list)])
                                                final_output = f"🗑️ Task has been removed from your list!\n\nHere's your updated task list:\n{task_list_text}"
                                            else:
                                                final_output = "🗑️ Task has been removed from your list!\n\nYour task list is now empty."
                                        else:
                                            final_output = "🗑️ Task has been removed from your list!"
                                        specific_response_found = True
                                        break
                                    elif func_name == "complete_task" and result_data.get("success"):
                                        status_text = "completed" if result_data.get("completed", True) else "marked as incomplete"

                                        # Get the updated task list to show to the user
                                        updated_tasks_result = get_all_tasks(str(user_uuid), db_session)
                                        if updated_tasks_result.get("success") and "tasks" in updated_tasks_result:
                                            task_list = updated_tasks_result["tasks"]
                                            if task_list:
                                                task_list_text = "\n".join([f"{i+1}) {task.get('title', 'Untitled')} — {'Completed' if task.get('completed') else 'Pending'}" for i, task in enumerate(task_list)])
                                                final_output = f"✅ Task has been {status_text}!\n\nHere's your updated task list:\n{task_list_text}"
                                            else:
                                                final_output = f"✅ Task has been {status_text}!\n\nYour task list is now empty."
                                        else:
                                            final_output = f"✅ Task has been {status_text}!"
                                        specific_response_found = True
                                        break
                                    elif func_name == "list_tasks" and result_data.get("success"):
                                        task_list = result_data.get("tasks", [])
                                        if task_list:
                                            task_list_text = "\n".join([f"{i+1}) {task.get('title', 'Untitled')} — {'Completed' if task.get('completed') else 'Pending'}" for i, task in enumerate(task_list)])
                                            final_output = f"You have {len(task_list)} tasks:\n{task_list_text}"
                                        else:
                                            final_output = "You don't have any tasks right now."
                                        specific_response_found = True
                                        break
                                    elif func_name == "get_all_tasks" and result_data.get("success"):
                                        task_list = result_data.get("tasks", [])
                                        if task_list:
                                            task_list_text = "\n".join([f"{i+1}) {task.get('title', 'Untitled')} — {'Completed' if task.get('completed') else 'Pending'}" for i, task in enumerate(task_list)])
                                            final_output = f"Here are your {len(task_list)} tasks:\n{task_list_text}"
                                        else:
                                            final_output = "You don't have any tasks right now."
                                        specific_response_found = True
                                        break

                                if not specific_response_found:
                                    # If no specific operation message was generated, use a default
                                    final_output = "I've handled your request. Let me know if you need anything else!"
                            else:
                                # If no successful operations, use error response from the first failed operation
                                failed_ops = [tr for tr in tool_results if not tr["result"].get("success")]
                                if failed_ops:
                                    error_msg = failed_ops[0]["result"].get("message", "I'm having trouble processing your request right now.")

                                    # Retry mechanism: if parsing failed, suggest user rephrase or try again
                                    if "couldn't find task number" in error_msg or "access your task list" in error_msg:
                                        # Fetch the current task list to help the user
                                        current_tasks_result = get_all_tasks(str(user_uuid), db_session)
                                        if current_tasks_result.get("success") and "tasks" in current_tasks_result and current_tasks_result["tasks"]:
                                            task_list = current_tasks_result["tasks"]
                                            task_list_text = "\n".join([f"{i+1}) {task.get('title', 'Untitled')} — {'Completed' if task.get('completed') else 'Pending'}" for i, task in enumerate(task_list)])
                                            final_output = f"{error_msg}\n\nHere's your current task list to help you reference the correct task numbers:\n{task_list_text}"
                                        else:
                                            final_output = f"{error_msg}\n\nPlease check your command and try again, making sure to use the correct task number from your list."
                                    else:
                                        final_output = f"I'm having trouble with that request: {error_msg}\n\nPlease try rephrasing your request or check your task numbers."
                                else:
                                    final_output = "I've handled your request. Let me know if you need anything else!"

                    # Update result with final output
                    result = {"success": True, "response": final_output}
                    print(f"Agent Result: {result}")
                    return result
                finally:
                    # Ensure proper cleanup of the generator
                    try:
                        next(db_gen)
                    except StopIteration:
                        pass

            # If no tool calls, extract the response text directly
            response_text = response.choices[0].message.content if response.choices and response.choices[0].message.content and response.choices[0].message.content.strip() else "I couldn't process that request."

            # Ensure response_text is never empty and not robotic
            if not response_text or response_text.strip() == "" or response_text.strip() == "I processed your request.":
                response_text = "I've handled your request. Let me know if you need anything else!"

            result = {"success": True, "response": response_text}
            print(f"Agent Result: {result}")
            return result

        except Exception as e:
            # Robust error handling to show the actual error in the chat UI
            print(f"OpenRouter API error in v2: {str(e)}")
            import traceback
            print(f"Full traceback in v2: {traceback.format_exc()}")

            # Return the actual error for debugging
            return {
                "success": False,
                "response": f"Brain Error: {str(e)}"
            }