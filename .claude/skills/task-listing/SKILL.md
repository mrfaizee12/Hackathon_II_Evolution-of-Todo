---
name: "task-listing"
description: "List user tasks with optional filters such as status, priority, or due date."
version: "1.0.0"
---

# Task Listing Skill

## When to Use
- User says: show, list, what do I have
- User asks about pending or completed tasks

## Process
1. Identify requested filter (pending / completed / all)
2. Detect optional priority or tag filters
3. Call MCP list_tasks tool
4. Format results clearly
5. Handle empty results gracefully

## Output Format
- Numbered or bullet list with id, title, status, due date

## Quality Criteria
- Results scoped to authenticated user
- Empty state explained clearly