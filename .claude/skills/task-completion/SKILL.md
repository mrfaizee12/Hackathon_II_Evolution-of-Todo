---
name: "task-completion"
description: "Mark an existing task as completed using natural language cues."
version: "1.0.0"
---

# Task Completion Skill

## When to Use
- User says: done, completed, finished

## Process
1. Identify task by id or description
2. Ask clarification if ambiguous
3. Call MCP complete_task tool
4. Confirm completion

## Quality Criteria
- Task exists
- Operation is idempotent