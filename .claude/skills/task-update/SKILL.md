---
name: "task-update"
description: "Update task title, priority, due date, or tags."
version: "1.0.0"
---

# Task Update Skill

## When to Use
- User says: change, update, modify

## Process
1. Identify task
2. Identify fields to update
3. Validate new values
4. Call MCP update_task tool
5. Confirm changes

## Quality Criteria
- Only requested fields modified
- Invalid updates rejected