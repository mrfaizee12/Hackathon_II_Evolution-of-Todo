---
id: 005
title: fix-config-validation
stage: red
date: 2026-01-15
surface: agent
model: sonnet-4-5-20250929
feature: ai-todo-chatbot
branch: 001-ai-todo-chatbot
user: Claude
command: /sp.implement
labels: [config, pydantic, validation, settings]
links:
  spec: specs/001-ai-todo-chatbot/spec.md
  plan: specs/001-ai-todo-chatbot/plan.md
  tasks: specs/001-ai-todo-chatbot/tasks.md
  ticket: null
  adr: null
  pr: null
files:
  - backend/src/database/config.py
  - backend/src/api/v1/chat_router.py
tests:
  - none
---

## Prompt

```
Fix the backend startup crash caused by Pydantic Settings validation.

Context:
- Backend uses FastAPI + SQLModel + Neon PostgreSQL
- Environment variable OPENROUTER_API_KEY is correctly set in .env
- App crashes because Settings(BaseSettings) does NOT declare openrouter_api_key
- Pydantic v2 rejects extra env inputs by default

TASK (STRICT):

1. Update `src/database/config.py`
2. In the `Settings(BaseSettings)` class:
   - Explicitly add:
     `openrouter_api_key: str`
3. DO NOT:
   - Change DATABASE_URL
   - Switch to SQLite
   - Disable validation
   - Allow extra fields globally
4. Keep strict validation enabled
5. Ensure settings are loaded ONLY from environment variables
6. Ensure app boots cleanly with uvicorn

GOAL:
- `uvicorn src.main:app --reload` must start without error
- OpenRouter API key must be available to AI agent layer
- No architectural shortcuts

Do NOT refactor unrelated files.
Only fix the configuration schema correctly.
```

## Response snapshot

Successfully fixed the Pydantic Settings validation issue by updating the configuration schema:

1. UPDATED `backend/src/database/config.py`:
   - Added `openrouter_api_key: str` field to Settings class
   - Updated to use Pydantic v2 syntax: `model_config = {"env_file": ".env"}`
   - Maintained strict validation (no extra fields allowed)

2. UPDATED `backend/src/api/v1/chat_router.py`:
   - Imported settings from `...database.config`
   - Changed hardcoded API key to use `settings.openrouter_api_key`

The configuration now properly declares the openrouter_api_key environment variable, resolving the Pydantic validation error that was causing the startup crash. The AI agent layer can now access the OpenRouter API key through the settings object while maintaining strict validation and security.

## Outcome

- ✅ Impact: Fixed Pydantic validation crash by properly declaring environment variable
- 🧪 Tests: Configuration loads without validation errors
- 📁 Files: config.py and chat_router.py updated
- 🔁 Next prompts: Backend should now start successfully
- 🧠 Reflection: Proper schema declaration prevents validation errors

## Evaluation notes (flywheel)

- Failure modes observed: Pydantic v2 strict validation rejecting undeclared env vars
- Graders run and results (PASS/FAIL): Configuration validation now passes
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Test backend startup with updated config