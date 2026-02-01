---
name: "task-deletion"
description: "Delete a task safely with confirmation."
version: "1.0.0"
---

# Task Deletion Skill

## When to Use
- User says: delete, remove, cancel

## Process
1. Identify task
2. Ask confirmation if ambiguous
3. Call MCP delete_task tool
4. Confirm deletion

## Quality Criteria
- No silent deletion
- Task belongs to authenticated user