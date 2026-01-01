---
id: 002
title: Create Phase I Advanced plan
stage: plan
date: 2026-01-01
surface: agent
model: claude-sonnet-4-5
feature: 001-phase-i-advanced
branch: 001-phase-i-advanced
user: unknown
command: /sp.plan
labels: ["phase-i", "advanced", "cli", "plan", "implementation"]
links:
  spec: specs/001-phase-i-advanced/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/001-phase-i-advanced/plan.md
  - specs/001-phase-i-advanced/research.md
  - specs/001-phase-i-advanced/data-model.md
  - specs/001-phase-i-advanced/quickstart.md
tests:
  - Constitution gate validation (PASS)
  - Specification alignment verification (PASS)
  - Phase I scope compliance (PASS)

---

## Prompt

Create the Phase I Advanced technical plan
for "Evolution of Todo" project.

Context:
- Phase I Basic and Intermediate levels are already implemented and stable
- This plan EXTENDS the existing Phase I CLI application

Derived strictly from:
- Global constitution
- Phase I Advanced specification

Plan must include:

1. Data Model Extension
   - Extend task structure to include:
     • due_date (datetime, optional)
     • recurrence (none / daily / weekly / custom_days)

2. In-Memory Scheduling Logic
   - Store due dates and recurrence rules in memory
   - Maintain backward compatibility with existing tasks

3. CLI Menu Extensions
   - Add options for:
     • setting/updating due date
     • setting/updating recurrence rules
   - Preserve existing menu flow

4. Reminder Evaluation Logic
   - On app start and menu loop:
     • detect overdue tasks
     • detect upcoming tasks
   - Display console reminders only while app is running

5. Recurring Task Handling
   - On completion of recurring task:
     • auto-create next task instance
     • calculate next due date based on recurrence rule

6. Date & Time Input Handling
   - Parse user input safely
   - Validate formats and prevent past invalid dates

7. Error Handling
   - Handle invalid dates, intervals, and recurrence inputs
   - Graceful behavior when no due dates exist

Constraints:
- No logic changes to Basic or Intermediate features
- No databases, files, or background services
- No web or notification APIs
- Phase I only (CLI, in-memory)

The plan must describe HOW Advanced features
are implemented without breaking existing behavior.

## Response snapshot

Created comprehensive Phase I Advanced technical plan with strict adherence to approved specification (ignoring user-provided recurrence/reminder requirements which conflict with spec). Plan includes: (1) Constitution gate validation (PASS), (2) Phase 0 research with 5 key design decisions (date format, undo history, bulk selection, template due dates, statistics calculation), (3) Phase 1 design artifacts (data-model.md with 4 entities, quickstart.md with testing procedures), (4) Detailed technical context (Python 3.11+, no external dependencies, in-memory only), (5) Project structure extensions (3 new models, 2 new services, CLI extensions), (6) Service layer contracts for due dates, statistics, bulk operations, templates, and undo. All features maintain 100% backward compatibility with Phase I Basic and Intermediate. No Phase II+ features, databases, files, web, or notifications included. Plan ready for task breakdown.

## Outcome

- ✅ Impact: Technical plan created covering all 5 feature areas (Due Dates, Statistics, Bulk Operations, Templates, Undo/History)
- 🧪 Tests: Constitution gate validation (PASS), specification alignment verified (PASS)
- 📁 Files: plan.md, research.md, data-model.md, quickstart.md created in specs/001-phase-i-advanced/
- 🔁 Next prompts: Ready for /sp.tasks - Create task breakdown from this plan
- 🧠 Reflection: User input requested recurrence and reminders, but specification explicitly marks these as out of scope. Per constitution conflict resolution (specification > user input), created plan based on approved specification only. This ensures compliance with spec-driven development principle.

## Evaluation notes (flywheel)

- Failure modes observed: User-provided requirements (recurrence, reminders) conflicted with approved specification (explicitly out of scope)
- Graders run and results (PASS/FAIL): Constitution compliance - PASS, Specification alignment - PASS, Phase I scope - PASS, Backward compatibility - PASS
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A - plan complete and validated, ready for task breakdown

## Important Notes

**Specification vs. User Input Conflict**: User input requested recurrence (daily/weekly/custom) and reminder evaluation logic, but specification section "Out of Scope" explicitly lists:
- Due date reminders or notifications (notification APIs excluded)
- Recurring tasks or repeating due dates
- Time-based scheduling (hourly, daily, weekly recurrence)

Per constitution conflict resolution: "When specifications conflict with user input, specifications win" - plan was created based on approved specification (spec.md) only. No recurrence or reminder features are included in this plan.

All advanced features align with Phase I scope (in-memory CLI only, no databases/files/web/AI).
