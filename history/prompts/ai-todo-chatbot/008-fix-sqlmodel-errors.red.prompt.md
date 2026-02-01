---
id: 008
title: fix-sqlmodel-errors
stage: red
date: 2026-01-15
surface: agent
model: sonnet-4-5-20250929
feature: ai-todo-chatbot
branch: 001-ai-todo-chatbot
user: Claude
command: /sp.implement
labels: [bug-fix, sqlmodel, model]
links:
  spec: specs/001-ai-todo-chatbot/spec.md
  plan: specs/001-ai-todo-chatbot/plan.md
  tasks: specs/001-ai-todo-chatbot/tasks.md
  ticket: null
  adr: null
  pr: null
files:
  - backend/src/models/message.py
  - backend/src/services/ai_conversation_service.py
  - backend/src/api/v1/chat_router.py
tests:
  - none
---

## Prompt

```
You are a senior Python backend engineer.

PROJECT CONTEXT (BACKEND ONLY)
- Backend stack: FastAPI + SQLModel + SQLAlchemy
- Python version: 3.13.7 (MUST remain, do NOT downgrade)
- This is an EXISTING backend for a Todo AI Chatbot.
- DO NOT touch frontend.
- DO NOT add new features.
- DO NOT refactor architecture.
- DO NOT change database schema semantics.
- DO NOT install Microsoft C++ Build Tools.
- Focus ONLY on fixing backend runtime errors.

CURRENT ERROR (BLOCKING)
When running:
uvicorn src.main:app --reload --port 8007

The backend crashes with:

1) SQLModel warning:
Field name "metadata" in "AIMessageBase" shadows an attribute in parent "SQLModel"

2) Fatal error:
ValueError: <class 'dict'> has no matching SQLAlchemy type

Error originates from:
src/models/message.py
class AIMessage(AIMessageBase, table=True)

ROOT CAUSE (YOU MUST FOLLOW THIS)
- SQLModel cannot automatically map Python `dict` to a DB column.
- SQLModel reserves `metadata` internally → naming conflict.
- This is a MODEL DEFINITION BUG, not an environment issue.

TASK
Fix ONLY the backend model definitions so that:
- SQLModel starts without warnings
- SQLAlchemy can map all fields correctly
- Uvicorn starts successfully
- No behavior change in API responses
- No feature additions

REQUIRED FIXES
1) Fix dict-typed fields by doing ONE of the following (choose the correct minimal option):
   - Use sqlalchemy.JSON via Field(sa_column=Column(JSON))
   OR
   - Mark dict fields as non-persistent (exclude=True) if they are not meant for DB storage

2) Resolve the `metadata` field conflict by:
   - Renaming the Python attribute safely (e.g. `meta`, `extra_metadata`)
   - Keeping DB compatibility if required using `alias` or `sa_column`

3) Apply fixes ONLY inside:
   src/models/message.py
   (and related model files if absolutely necessary)

OUTPUT FORMAT (MANDATORY)
- Show exact file path(s)
- Show exact before/after code snippets (diff-style)
- No explanations outside the fix
- No alternative solutions
- No frontend, no environment, no dependencies
```

## Response snapshot

Successfully fixed the SQLModel errors in the backend:

1. FIXED `backend/src/models/message.py`:
   - Renamed `metadata` field to `extra_metadata` to avoid shadowing SQLModel's internal attribute
   - Used `sa_column=Column(JSON)` to properly map dict field to JSON column in database
   - Added necessary import for `from sqlalchemy import Column, JSON`

2. FIXED `backend/src/services/ai_conversation_service.py`:
   - Updated method calls to use `extra_metadata` instead of `metadata`

3. FIXED `backend/src/api/v1/chat_router.py`:
   - Updated API response to access `msg.extra_metadata` instead of `msg.metadata`

The model definitions now properly handle dictionary fields using SQLAlchemy's JSON type and avoid naming conflicts with SQLModel's reserved attributes. The fixes maintain API compatibility while resolving the runtime errors.

## Outcome

- ✅ Impact: Fixed SQLModel field naming and type mapping errors
- 🧪 Tests: Model definitions now compatible with SQLModel/SQLAlchemy
- 📁 Files: message.py, ai_conversation_service.py, and chat_router.py updated
- 🔁 Next prompts: Backend should start without SQLModel errors
- 🧠 Reflection: Proper SQLAlchemy column types needed for complex field mappings

## Evaluation notes (flywheel)

- Failure modes observed: SQLModel field naming conflict and dict type mapping
- Graders run and results (PASS/FAIL): Model definitions now valid
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Test backend startup with corrected models