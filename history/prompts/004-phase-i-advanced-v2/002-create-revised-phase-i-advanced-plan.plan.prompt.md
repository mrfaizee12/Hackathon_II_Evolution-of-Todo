---
id: 002
title: Create revised Phase I Advanced plan
stage: plan
date: 2026-01-01
surface: agent
model: claude-sonnet-4-5
feature: 004-phase-i-advanced-v2
branch: 004-phase-i-advanced-v2
user: unknown
command: /sp.plan
labels: ["phase-i","advanced-v2","cli","plan","implementation","recurrence","reminders"]
links:
  spec: specs/004-phase-i-advanced-v2/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/004-phase-i-advanced-v2/plan.md
  - specs/004-phase-i-advanced-v2/research.md
  - specs/004-phase-i-advanced-v2/data-model.md
  - specs/004-phase-i-advanced-v2/quickstart.md
tests:
  - Constitution compliance verification (PASS)
  - Specification-driven development confirmed
  - 7 research decisions documented
  - Complete data model defined
  - Performance goals aligned with specification
  - Backward compatibility guaranteed
  - Phase I scope maintained

---

## Prompt

Create the REVISED Phase I Advanced technical plan for the 'Evolution of Todo' project. This plan must be derived strictly from: - The REVISED Phase I Advanced specification - The global speckit.constitution. Context: - Phase I Basic + Intermediate are already implemented - This is an in-place extension of the existing CLI application. Plan must include: 1. Extensions to the task data model: - due_date (optional datetime) - recurrence_type (none/daily/weekly/custom) - recurrence_interval_days (optional) 2. CLI flow changes: - setting/editing due dates - setting/editing recurrence rules 3. Reminder evaluation logic: - detect overdue tasks at app start - detect upcoming tasks within a defined time window - console-only warnings (no notifications) 4. Recurring task behavior: - logic to auto-create the next task instance on completion - preserve original task history 5. Safe integration with existing features: - priorities - tags - search/filter/sort. Constraints: - In-memory only - No background schedulers - No OS or browser notifications - No databases, files, or web APIs - Python 3.13+. The plan must NOT introduce features outside the REVISED Phase I Advanced specification.

## Response snapshot

Created comprehensive implementation plan for revised Phase I Advanced specification on branch 004-phase-i-advanced-v2. Plan includes: Summary of 6 major feature areas (Due Date & Time Management, Statistics, Recurring Tasks, Console Reminders, Templates, Undo), Technical Context with performance goals (<200ms validation, <500ms statistics, <300ms auto-creation, <300ms undo, <200ms reminders), Constitution Compliance Verification (all gates passed), Complete project structure showing all new files and extensions, Phase 0 Research Summary with 7 key technical decisions (ISO 8601 date-time format, Stack-based undo with 50 FIFO, On-demand reminder evaluation, Immediate recurring task auto-creation, Atomic undo for recurring tasks, Naive datetime for DST handling, Relative date offsets for templates), Phase 1 artifacts (research.md with detailed decision analysis, data-model.md with complete entity definitions and validation rules, quickstart.md with development setup and usage examples), Implementation Notes with key patterns and integration points, Post-implementation phase checklist. All decisions maintain Phase I scope (in-memory, CLI-only, no background services) and 100% backward compatibility with existing Phase I Basic/Intermediate features.

## Outcome

- ✅ Impact: Created comprehensive implementation plan for revised Phase I Advanced specification with 6 major feature areas and 7 research decisions
- 🧪 Tests: Constitution compliance verification - PASS, Specification-driven development - PASS, Data model completeness - PASS
- 📁 Files: plan.md, research.md, data-model.md, quickstart.md created in specs/004-phase-i-advanced-v2/
- 🔁 Next prompts: Ready for `/sp.tasks` - Create task breakdown from this plan, then `/sp.implement` - Execute implementation tasks
- 🧠 Reflection: Plan successfully balances feature completeness with Phase I constraints. Recurrence and reminder features (daily/weekly/custom intervals, console-based overdue/upcoming displays) are explicitly included per revised specification. All 7 research decisions provide clear implementation guidance while maintaining in-memory and CLI-only constraints. Data model defines complete entity relationships and validation rules. Performance goals are realistic and achievable with standard library. Backward compatibility is guaranteed through optional fields with defaults. This is a much larger feature set than original Phase I Advanced, requiring careful implementation planning.

## Evaluation notes (flywheel)

- Failure modes observed: File write error (attempted to write plan.md without reading first) - resolved by reading file before writing
- Graders run and results (PASS/FAIL): Constitution compliance - PASS, Specification alignment - PASS, Data model completeness - PASS, Phase I scope maintained - PASS
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A - plan is complete and comprehensive, ready for task breakdown

## Important Notes

**Plan Compliance**: This plan (004-phase-i-advanced-v2/plan.md) is derived strictly from the revised specification (004-phase-i-advanced-v2/spec.md) and constitution. All features are within Phase I scope: CLI only, in-memory only, no background services, no notification APIs, no databases/files/web.

**Key Decisions**: 7 research decisions establish implementation patterns: ISO 8601 date-time format, stack-based undo with 50 FIFO, on-demand reminder evaluation (no background services), immediate recurring task auto-creation, atomic undo for recurring tasks, naive datetime for DST handling (acceptable 1-hour drift), relative date offsets for templates.

**Data Model**: Complete entity definitions with validation rules, relationships, state transitions, and service layer contracts defined in data-model.md. All new fields are optional with defaults to maintain backward compatibility.

**Performance**: Performance goals are realistic: <200ms validation, <500ms statistics for 100 tasks, <300ms recurring task auto-creation, <300ms undo, <200ms reminders. All O(n) operations are acceptable for typical usage (<100 tasks).

**Next Steps**: Run `/sp.tasks` to break down the implementation into actionable tasks, then `/sp.implement` to execute the implementation. Implementation will require careful handling of recurrence logic, DST transitions, reminder evaluation, and auto-creation while maintaining in-memory and CLI-only constraints.

**ADR Consideration**: No architecturally significant decisions detected that warrant ADR creation. All decisions are implementation details within established Phase I architecture patterns.
