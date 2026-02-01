# Implementation Plan: AI Todo Chatbot

**Branch**: `001-ai-todo-chatbot` | **Date**: 2026-01-15 | **Spec**: [link]
**Input**: Feature specification from `/specs/001-ai-todo-chatbot/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implementation of an AI-powered Todo Chatbot that integrates natively into the existing Phase II Todo App. The solution will leverage OpenRouter's AI service through the OpenAI Agents SDK to provide natural language processing for todo management. The system will include MCP tools for task operations, a stateless chat endpoint, and a ChatKit-based UI that appears as a drawer/modal in the dashboard sidebar.

## Technical Context

**Language/Version**: Python 3.11, TypeScript 5+, Next.js 14+
**Primary Dependencies**: FastAPI, SQLModel, Neon PostgreSQL, OpenAI Agents SDK, OpenRouter API, Better Auth, ChatKit
**Storage**: Neon Serverless PostgreSQL
**Testing**: pytest for backend, Jest for frontend
**Target Platform**: Web application (Linux server deployment)
**Project Type**: Web application with separate backend/frontend
**Performance Goals**: AI responses complete within 5 seconds p95 latency
**Constraints**: Must not break existing Phase II functionality, stateless AI services, all state stored in Neon PostgreSQL
**Scale/Scope**: Support existing user base with AI-enhanced todo management

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- ✅ Phase III AI Todo Chatbot is authorized per constitution
- ✅ AI frameworks are authorized for Phase III
- ✅ OpenRouter API with specified model is compliant with constitution
- ✅ State stored in Neon PostgreSQL only (stateless server)
- ✅ No breaking changes to existing functionality
- ✅ AI features implemented as native dashboard components
- ✅ MCP tools and OpenAI Agents SDK usage authorized
- ✅ All existing Phase II architecture preserved

## Project Structure

### Documentation (this feature)

```text
specs/001-ai-todo-chatbot/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── models/
│   │   ├── todo.py
│   │   ├── conversation.py
│   │   └── message.py
│   ├── services/
│   │   ├── todo_service.py
│   │   ├── ai_conversation_service.py
│   │   └── mcp_tool_server.py
│   ├── api/
│   │   ├── v1/
│   │   │   ├── todo_router.py
│   │   │   └── chat_router.py
│   │   └── __init__.py
│   ├── tools/
│   │   ├── todo_tools.py
│   │   └── user_tools.py
│   └── main.py
└── tests/

frontend/
├── src/
│   ├── components/
│   │   ├── chat/
│   │   │   ├── ChatBotDrawer.tsx
│   │   │   ├── ChatMessage.tsx
│   │   │   └── ChatInput.tsx
│   │   ├── layout/
│   │   │   └── Sidebar.tsx
│   │   └── ui/
│   ├── pages/
│   │   ├── dashboard/
│   │   │   └── index.tsx
│   │   └── index.tsx
│   ├── services/
│   │   └── chatService.ts
│   └── styles/
│       └── globals.css
└── tests/
```

**Structure Decision**: Web application with separate backend and frontend directories following the established architecture from Phase II. Backend will house FastAPI application with AI integration and MCP tool server. Frontend will contain Next.js application with ChatKit UI implementation and sidebar integration.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [None] | [No violations found] | [All constitutional requirements satisfied] |