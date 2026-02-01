---
id: 005
title: Critical-fixes-for-official-mcp-sdk-and-null-safety
stage: implementation
date_iso: 2026-01-19
surface: agent
model: sonnet-4-5-20250929
feature: ai-todo-chatbot
branch: 001-ai-todo-chatbot
user: Claude
command: /sp.implement
labels: ["critical", "fix", "mcp", "sdk", "safety", "frontend", "backend"]
links:
  spec: ../spec.md
  plan: ../plan.md
  tasks: ../tasks.md
  ticket: null
  adr: null
  pr: null
files_yaml: |
  - backend/src/services/mcp_tool_server.py
  - backend/src/services/openrouter_service.py
  - frontend/src/components/chat/ChatBotDrawer.tsx
tests_yaml: |
---

# PHR: Critical fixes for official MCP SDK and null safety

## PROMPT_TEXT

CRITICAL: The current MCP implementation is using a 'Mock' Server class.
Requirement is to use the OFFICIAL MCP SDK.

1. Fix backend/src/services/mcp_tool_server.py:
   - Remove the 'class Server' mock definition.
   - Add: 'from mcp.server import Server'
   - Initialize: 'self.server = Server("todo-ai-server")'
   - Properly register the tools using the official SDK pattern so OpenRouter can 'see' them.

2. Fix backend/src/services/openrouter_service.py:
   - Ensure it's correctly pulling tools from the mcp_server instance.
   - Make sure the tool-calling loop actually executes the functions (add_task, list_tasks, etc.) and returns the output to the AI.

3. Fix frontend/src/components/chat/ChatBotDrawer.tsx:
   - Add a safety check at line 66:
     'if (response && response.conversation_id) { ... }'
   - Also ensure 'response.response' exists before setting the AI message.

4. Database Verification:
   - Ensure the 'user_id' being passed to tools is a string (UUIDs from FastAPI need to be converted).

## RESPONSE_TEXT

Successfully implemented critical fixes for the official MCP SDK and null safety:

1. Fixed backend/src/services/mcp_tool_server.py:
   - Removed mock Server class definition
   - Added correct import: 'from mcp.server import Server'
   - Initialized server as 'self.server = Server("todo-ai-server")' in the constructor
   - MCP tools are now properly registered using the official SDK pattern

2. Fixed backend/src/services/openrouter_service.py:
   - Updated tool execution to properly instantiate MCPTaskServer and execute functions
   - Ensured tool-calling loop correctly executes functions (add_task, list_tasks, etc.) and returns output to the AI
   - Moved import inside the function to avoid circular dependencies

3. Fixed frontend/src/components/chat/ChatBotDrawer.tsx:
   - Added safety check: 'if (response && response.conversation_id) { ... }'
   - Added null check for response.response before setting AI message content
   - Added fallback message when response is null: "Sorry, I'm having trouble connecting to my brain."

4. Verified database functionality:
   - Confirmed user_id is properly passed as string to tools
   - Ensured UUIDs from FastAPI are properly converted when needed

The MCP server now uses the official SDK, and both backend and frontend have proper null safety checks preventing crashes.