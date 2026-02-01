---
id: 001
title: Create-specification-for-Phase-III-Todo-AI-Chatbot
stage: spec
date_iso: 2026-01-19
surface: agent
model: sonnet-4-5-20250929
feature: ai-todo-chatbot
branch: 001-ai-todo-chatbot
user: Claude
command: /sp.specify
labels: ["spec", "ai", "todo", "mcp", "stateless", "openrouter"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml: |
  - specs/001-ai-todo-chatbot/spec.md
  - backend/src/api/v1/chat_router.py
tests_yaml: |
  - specs/001-ai-todo-chatbot/checklists/requirements.md
---

# PHR: Create specification for Phase III: Todo AI Chatbot

## PROMPT_TEXT

Create a technical specification for Phase III: Todo AI Chatbot.
1. Use the Official Python MCP SDK to build an internal MCP server.
2. Expose 5 tools: add_task, list_tasks, complete_task, delete_task, update_task.
3. Use OpenRouter API for the AI model logic.
4. The system must be 100% stateless: fetch history from Neon DB (SQLModel) on every request.
5. Requirements: FastAPI backend, SQLModel ORM, and OpenAI Agents SDK pattern using OpenRouter.
6. Fix all existing syntax/indentation errors in src/api/v1/chat_router.py during this process.

## RESPONSE_TEXT

Updated the AI Todo Chatbot specification to reflect Phase III requirements including MCP SDK integration, 5 standardized tools (add_task, list_tasks, complete_task, delete_task, update_task), OpenRouter API integration, and stateless architecture. Also refactored the chat_router.py to eliminate in-memory session storage and make it 100% stateless by fetching all necessary data from the database on each request.