---
id: 4
title: "Advanced-Todo-Features-Breakdown-Tasks"
stage: "tasks"
date_iso: "2026-02-07"
surface: "agent"
model: "Claude Sonnet 4.5"
feature: "001-advanced-todo-features"
branch: "001-advanced-todo-features"
user: "user"
command: "/sp.tasks"
labels: ["tasks", "todo", "recurring", "due-dates", "reminders", "implementation"]
links:
  spec: "specs/001-advanced-todo-features/spec.md"
  plan: "specs/001-advanced-todo-features/plan.md"
  ticket: null
  adr: null
  pr: null
files_yaml:
  - "specs/001-advanced-todo-features/tasks.md"
tests_yaml: []
---

"Break Advanced Todo Features into execution tasks"

OBJECTIVE:
Implement ONLY advanced features → Recurring Tasks + Due Dates + Reminders.
(Intermediate features already exist — DO NOT modify them.)

TASK GROUPS:

1️⃣ Database
- Extend Todo model with:
  recurrence_type
  recurrence_interval
  next_occurrence
  reminder_at
- Generate safe migration.

2️⃣ Recurring Engine
- Create service that:
  - listens for task completion
  - auto-creates next occurrence
  - prevents duplicates.

3️⃣ Reminder System
- Build async scheduler/background worker.
- Trigger reminders at reminder_at.
- Keep logic decoupled from API.

4️⃣ API Updates
- Add endpoints:
  - set recurrence
  - set due date
  - set reminder
  - get upcoming tasks
- No refactoring.

5️⃣ Chatbot Upgrade
- Map intents → tools:
  - repeat task
  - set due date
  - remind me
  - upcoming tasks

6️⃣ Safety + Validation
- Future-only dates
- Idempotency checks
- Timezone-safe handling

7️⃣ Testing
- Unit → recurring