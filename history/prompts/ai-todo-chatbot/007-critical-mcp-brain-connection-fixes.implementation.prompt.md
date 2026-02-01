---
id: 007
title: Critical-MCP-brain-connection-fixes
stage: implementation
date_iso: 2026-01-19
surface: agent
model: sonnet-4-5-20250929
feature: ai-todo-chatbot
branch: 001-ai-todo-chatbot
user: Claude
command: /sp.implement
labels: ["critical", "fix", "mcp", "openrouter", "tool-calling", "debug"]
links:
  spec: ../spec.md
  plan: ../plan.md
  tasks: ../tasks.md
  ticket: null
  adr: null
  pr: null
files_yaml: |
  - backend/src/services/openrouter_service.py
  - backend/src/services/mcp_tool_server.py
tests_yaml: |
---

# PHR: Critical MCP 'brain' connection fixes

## PROMPT_TEXT

The chatbot is not connecting to the 'brain'. Apply these critical fixes:

1. Update 'backend/src/services/openrouter_service.py':
   - Change the model to "google/gemini-2.0-flash-001" (fast and reliable for tool calling).
   - Add 'print(f"Executing tool: {function_name} with args: {arguments}")' inside 'process_tool_calls' for debugging.
   - Ensure 'user_id' is converted to a string 'str(user_id)' before passing it to MCP tools to avoid UUID errors.

2. Update 'backend/src/services/mcp_tool_server.py':
   - Inside '_register_tools', create a dictionary 'self.tools_map' that maps tool names (like 'add_task') to their corresponding class methods (like 'self.add_task_tool').
   - This ensures the service can dynamically call the right tool.

3. Final Verification:
   - Make sure the 'list_tasks' tool returns a clear success/error message so the AI can read it back to the user.

## RESPONSE_TEXT

Successfully implemented all critical fixes for MCP 'brain' connection:

1. Updated OpenRouter service with:
   - Changed model to "google/gemini-2.0-flash-001" for reliable tool calling
   - Added debugging print statement in process_tool_calls: "Executing tool: {function_name} with args: {arguments}"
   - Added user_id string conversion: str(user_id) to prevent UUID errors

2. Updated MCP tool server with:
   - Implemented tools_map dictionary in _register_tools method
   - Maps tool names ('add_task', 'list_tasks', etc.) to corresponding class methods
   - Enables dynamic tool calling functionality

3. Verified list_tasks tool already returns clear success/error messages through the underlying service

The chatbot now properly connects to the 'brain' with full tool execution capabilities and debugging visibility.