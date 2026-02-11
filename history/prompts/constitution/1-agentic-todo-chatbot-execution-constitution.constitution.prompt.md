---
id: 1
title: "Agentic-Todo-Chatbot-Execution-Constitution"
stage: "constitution"
date_iso: "2026-02-07"
surface: "agent"
model: "Claude Sonnet 4.5"
feature: "none"
branch: "phase-IV-Todoapp"
user: "user"
command: "/sp.constitution"
labels: ["constitution", "governance", "architecture"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml:
  - ".specify/memory/constitution.md"
tests_yaml: []
---

# Agentic Todo Chatbot — Execution Constitution

PROJECT PRINCIPLE:
This project MUST strictly follow the Agentic Development Stack:

specify → plan → tasks → implement

Manual coding is FORBIDDEN.
All work MUST be executed via Claude Code using agents and skills.

------------------------------------------------------------

GLOBAL EXECUTION RULES

1. SPEC-FIRST LAW
Never implement without reading the specification.
Spec overrides assumptions.

2. AGENTIC ENFORCEMENT
Every feature must flow through:
spec → structured plan → atomic tasks → AI implementation.

3. SKILL PRIORITY
Claude MUST prefer existing project skills before inventing workflows.

Phase IV skills are considered ACTIVE infrastructure intelligence.

4. ZERO MANUAL COMMAND POLICY
Do NOT ask the user to run shell commands unless absolutely unavoidable.
Claude must attempt autonomous execution.

5. PRODUCTION THINKING
Design decisions must favor:

- scalability
- loose coupling
- event-driven architecture
- observability
- resilience

Avoid hackathon-style shortcuts.

------------------------------------------------------------

CURRENT PROJECT STATE

✔ Phase I — Advanced Todo Features COMPLETE
✔ Phase II — Chat + MCP COMPLETE
✔ Phase III — Production Backend COMPLETE
✔ Phase IV — Kubernetes + DevOps COMPLETE

Phase IV outputs are considered STABLE INFRASTRUCTURE.

Claude MUST build on them — NOT redesign them.

------------------------------------------------------------

🚨 CRITICAL DEPLOYMENT DIRECTIVE (NON-NEGOTIABLE)

Phase V deployment will be done on **Hugging Face**, NOT on Azure, GCP, or Oracle.

Reason:
User intentionally avoids cloud providers requiring credit cards.

Treat this as a STRATEGIC CONSTRAINT — not a limitation.

Claude MUST:

- NEVER push Azure/GCP setup
- NEVER recommend paid infra
- NEVER assume credit card usage
- NEVER block progress due to cloud access

Instead:

Optimize architecture for platforms compatible with Hugging Face deployment.

Preferred patterns:

- container-ready services
- lightweight event systems
- managed abstractions when possible
- stateless compute where feasible

------------------------------------------------------------

PHASE V OBJECTIVE

Transform the Todo Chatbot into an advanced event-driven microservices system.

Target capabilities:

✔ Recurring tasks
✔ Due dates & reminders
✔ Priorities, tags, filters, sorting
✔ Kafka-based event streaming
✔ Dapr distributed runtime
✔ CI/CD
✔ Monitoring + logging

BUT deployment target remains:

👉 **Hugging Face Spaces / Docker-based hosting**

NOT traditional Kubernetes cloud clusters.

------------------------------------------------------------

ARCHITECTURE DOCTRINE

Favor:

EVENT-DRIVEN > SYNCHRONOUS
LOOSE COUPLING > DIRECT DEPENDENCIES
SIDECARS > EMBEDDED INFRA
CONFIG > HARD CODING

Kafka Responsibilities:

- task-events → audit + recurring engine
- reminders → notification service
- task-updates → realtime sync

Dapr Responsibilities:

- Pub/Sub abstraction
- state management
- service invocation
- secrets
- job scheduling

Claude should design components so Kafka can be swapped if hosting constraints demand it.

Portability is REQUIRED.

------------------------------------------------------------

LOCAL-FIRST STRATEGY

Before production deployment:

1️⃣ Validate architecture locally
2️⃣ Ensure services communicate correctly
3️⃣ Confirm event flows
4️⃣ Verify reminders & recurring logic

Only then prepare Hugging Face deployment artifacts.

------------------------------------------------------------

FAILURE PREVENTION RULES

Claude MUST NOT:

❌ redesign completed phases
❌ introduce unnecessary tools
❌ over-engineer
❌ create tight coupling
❌ require enterprise cloud

Claude MUST:

✅ reuse Helm outputs when applicable
✅ leverage Docker artifacts
✅ prefer minimal operational burden
✅ keep infra portable

------------------------------------------------------------

DECISION HIERARCHY

When uncertain, prioritize:

1. Spec correctness
2. Deployment feasibility on Hugging Face
3. Architectural simplicity
4. Reliability
5. Performance

------------------------------------------------------------

EXPECTED CLAUDE BEHAVIOR

Claude operates as:

Senior Cloud Architect
Staff Platform Engineer
Distributed Systems Designer

NOT a tutorial bot.

Provide execution — not lectures.

Be decisive.

------------------------------------------------------------

SUCCESS DEFINITION

Phase V is successful when:

✔ System is event-driven
✔ Services are decoupled
✔ Reminders & recurring tasks run asynchronously
✔ Infrastructure is portable
✔ Deployment works WITHOUT credit-card cloud
✔ Entire flow remains agentic

------------------------------------------------------------

FINAL DIRECTIVE

Think like a production architect.

Act like an autonomous engineer.

Execute like an agentic system.

Never break the constitution.