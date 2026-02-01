---
name: "chatkit-integrator"
description: "Integrate OpenAI ChatKit with a backend chat API."
version: "1.0.0"
---

## When to Use
- Adding chatbot UI

## Process
1. Validate domain allowlist
2. Configure domain key
3. Map ChatKit messages to API payload
4. Handle conversation_id lifecycle
5. Handle loading and error states

## Quality Criteria
- Messages persist across refresh
- No hardcoded secrets