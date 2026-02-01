---
name: "task-creation"
description: "Create a new todo from natural language while validating title, priority, due date, and tags."
version: "1.0.0"
---

# Task Creation Skill

## When to Use
- User says: add, create, remember, remind me
- User expresses future intent

## Process
1. Extract task title from user message
2. Detect optional fields (priority, due date, tags)
3. Validate due date (must not be in the past)
4. Apply defaults if fields missing
5. Call MCP add_task tool
6. Confirm creation to user

## Output Format
- Confirmation message
- Summary of created task

## Quality Criteria
- Title is non-empty
- Due date (if provided) is future
- Priority is one of low / medium / high

## Example
Input: "Remind me to submit report tomorrow with high priority"
Output: "Task added: Submit report (Priority: High, Due: Tomorrow)"