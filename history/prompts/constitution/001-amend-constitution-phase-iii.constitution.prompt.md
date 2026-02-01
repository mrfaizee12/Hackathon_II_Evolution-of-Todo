---
id: 001
title: Amend constitution phase iii
stage: constitution
date: 2026-01-15
surface: agent
model: sonnet-4-5-20250929
feature: none
branch: 001-phase-ii-intermediate
user: Claude
command: /sp.constitution
labels: [constitution, phase-iii, ai-chatbot, amendment]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
tests:
  - none
---

## Prompt

```
# PHASE III — AI TODO CHATBOT (STRICT CONSTITUTION)

## CORE PRINCIPLES
- Phase II Full-Stack Todo App is the BASELINE
- NO breaking changes to existing functionality
- NO separate chatbot app/page
- AI Chatbot is a NATIVE feature inside dashboard
- Backend = AI logic
- Frontend = UI only
- Stateless server, state stored in Neon PostgreSQL ONLY

## AI PROVIDER RULE
- ❌ DO NOT use OpenAI API key
- ❌ DO NOT use Cohere
- ❌ DO NOT use Gemini
- ✅ USE OpenRouter API via OpenAI Agents SDK compatibility
- ✅ Model:
  openrouter/deepseek/deepseek-r1-0528-qwen3-8b:free
- ✅ Base URL:
  https://openrouter.ai/api/v1

## DATABASE RULE
- ONLY Neon Serverless PostgreSQL
- NEVER switch to SQLite
- Use DATABASE_URL from .env

## UI RULE
- Upgrade existing UI, DO NOT replace
- Chatbot opens from dashboard sidebar
- No auto-execution on page load
```

## Response snapshot

The constitution has been updated from version 1.3.0 to 2.0.0 to incorporate Phase III AI Todo Chatbot requirements. Key changes include:

- Updated Phase Isolation Policy to include Phase III AI Todo Chatbot
- Removed Global Restriction: "No AI or agent frameworks" - now authorized for Phase III
- Added specific requirements for AI Chatbot as native dashboard feature
- Defined mandatory technology requirements for Phase III including OpenRouter API
- Maintained all existing Phase II requirements while adding AI-specific constraints
- Updated Quality Principles to include AI-specific security and performance requirements

## Outcome

- ✅ Impact: Major version update (1.3.0 → 2.0.0) reflecting authorization of AI frameworks for Phase III
- 🧪 Tests: No tests required for constitution update
- 📁 Files: .specify/memory/constitution.md updated with new Phase III requirements
- 🔁 Next prompts: Ready for Phase III AI Todo Chatbot specification and implementation
- 🧠 Reflection: Constitution now properly authorizes AI development while maintaining strict phase isolation and backward compatibility requirements

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Begin Phase III specification with AI chatbot requirements