---
id: 001
title: ai-todo-chatbot-spec
stage: spec
date: 2026-01-15
surface: agent
model: sonnet-4-5-20250929
feature: ai-todo-chatbot
branch: 001-ai-todo-chatbot
user: Claude
command: /sp.specify
labels: [ai, chatbot, todo, specification]
links:
  spec: specs/001-ai-todo-chatbot/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/001-ai-todo-chatbot/spec.md
  - specs/001-ai-todo-chatbot/checklists/requirements.md
tests:
  - none
---

## Prompt

```
# PHASE III — AI TODO CHATBOT (SPEC)
## OBJECTIVE
Integrate an AI-powered Todo Chatbot into the EXISTING Phase II Todo App.
The chatbot must fully manage todos using natural language and feel like a native assistant.
## CHATBOT CAPABILITIES
The AI assistant MUST:
- Add tasks
- Update tasks
- Delete tasks
- Complete tasks
- List tasks (all / pending / completed)
- Answer questions about the logged-in user (email, identity)
- Confirm every action politely
## UI REQUIREMENTS
### Landing Page (Pre-Auth)
- Upgrade existing landing page ONLY
- Header with:
  - Logo
  - Sign In
  - Sign Up
- Dark flagship UI
- Gradient hero section
- Animated feature cards
- Footer retained (visual upgrade only)
### Dashboard (Post-Auth)
- Existing dashboard preserved
- Add LEFT sidebar
- Sidebar items:
  - Todos
  - AI Assistant 🤖
- Clicking AI Assistant opens chatbot as:
  - Right drawer OR modal (ChatGPT style)
- No navigation to new routes
### Chatbot UI
- Dark glassmorphism panel
- Smooth open/close animation
- ChatKit UI
- Typing + loading states
- Mobile responsive
## BACKEND REQUIREMENTS
- FastAPI
- OpenAI Agents SDK
- MCP Server with tools:
  add_task, list_tasks, update_task, complete_task, delete_task
- Stateless `/api/{user_id}/chat` endpoint
- Conversation + messages stored in Neon DB
## AI MODEL CONFIG (MANDATORY)
Use OpenRouter via Agents SDK compatible client:
- Model:
  openrouter/deepseek/deepseek-r1-0528-qwen3-8b:free
- Base URL:
  https://openrouter.ai/api/v1
- API Key:
  OPENROUTER_API_KEY from .env
DAT
```

## Response snapshot

Created comprehensive specification for AI Todo Chatbot feature in specs/001-ai-todo-chatbot/spec.md. The specification includes:

- Three prioritized user stories covering core AI functionality, user identity access, and interface experience
- Functional requirements covering all AI capabilities (add, update, delete, complete, list tasks)
- Key entities (AIConversation, AIMessage, TodoAction)
- Success criteria with measurable outcomes
- Edge cases handling

Quality checklist completed with all items validated.

## Outcome

- ✅ Impact: Successfully created detailed spec for AI Todo Chatbot feature
- 🧪 Tests: No tests needed for specification creation
- 📁 Files: specs/001-ai-todo-chatbot/spec.md and checklists/requirements.md created
- 🔁 Next prompts: Ready for /sp.plan to create implementation plan
- 🧠 Reflection: Spec captures all requirements from user input while maintaining focus on user value

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Begin implementation planning with /sp.plan