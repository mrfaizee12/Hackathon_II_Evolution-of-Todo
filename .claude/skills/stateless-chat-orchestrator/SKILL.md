---
name: "stateless-chat-orchestrator"
description: "Design stateless chat endpoints with persistent conversation history."
version: "1.0.0"
---

## Process
1. Load conversation history from DB
2. Append new user message
3. Run agent with full context
4. Store assistant response
5. Return conversation_id

## Quality Criteria
- Server restart safe
- No in-memory state