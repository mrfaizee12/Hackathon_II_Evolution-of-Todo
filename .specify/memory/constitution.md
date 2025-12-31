<!--
Sync Impact Report
==================
Version: 1.0.0 → 1.1.0
Change Type: MINOR - Amendment to reflect Phase II requirements and UI/UX policy

Changes Made:
- Updated Technology Stack section to specify Phase II technologies (Python REST API, Neon Serverless PostgreSQL, SQLModel, Next.js, Better Auth)
- Enhanced Phase Governance to detail Phase I and Phase II scope and requirements
- Added UI/UX Requirements section to Technology Constraints for Phase II+ features
- Updated Database Requirements to specify Neon Serverless PostgreSQL and SQLModel or equivalent

Templates Status:
- ✅ .specify/templates/plan-template.md - Reviewed, aligns with constitution
- ✅ .specify/templates/spec-template.md - Reviewed, aligns with constitution
- ✅ .specify/templates/tasks-template.md - Reviewed, aligns with constitution

Follow-up Actions:
- None - all placeholders filled, all templates aligned

Notes:
- Amendment reflects Phase II requirements as specified
- Preserves phase isolation and acts as authoritative technology policy
- Maintains all existing Phase I requirements while adding Phase II specifics
-->

# Evolution of Todo Project Constitution

## Core Principles

### I. Spec-Driven Development (Mandatory)

**No agent may write code without approved specs and tasks.** All development work MUST follow the strict workflow:

1. Constitution → Specifications → Plan → Tasks → Implement
2. Every feature begins with a complete specification in `specs/<feature>/spec.md`
3. Every feature requires an approved implementation plan in `specs/<feature>/plan.md`
4. Every feature requires a task list in `specs/<feature>/tasks.md` before implementation
5. Implementation begins ONLY after user approval of specifications and tasks

**Rationale**: Spec-Driven Development ensures all stakeholders understand requirements before code is written, prevents scope creep, enables accurate effort estimation, and creates traceable documentation. This is particularly critical for the Evolution of Todo project, which spans five distinct phases with increasing complexity.

**Violations**: Code written without approved specs is considered non-compliant and MUST be reverted.

### II. Agent Behavior Rules

**Agents are implementation executors, not designers.** The following rules are non-negotiable:

- **No Manual Coding by Humans**: All code MUST be written by agents following approved specifications
- **No Feature Invention**: Agents MUST NOT add features, capabilities, or "improvements" beyond specifications
- **No Deviation from Specifications**: Agents MUST implement exactly what is specified, no more, no less
- **Refinement at Spec Level**: When issues or improvements are identified, agents MUST suggest specification updates rather than directly modifying code
- **Clarification Required**: When specifications are ambiguous, agents MUST ask for clarification before proceeding

**Rationale**: Clear separation between design (human) and implementation (agent) prevents uncontrolled complexity, maintains architectural consistency, and ensures all stakeholders approve changes before implementation.

**Human as Tool**: Agents MUST invoke users for clarification when encountering:
- Ambiguous requirements (ask 2-3 targeted questions)
- Unforeseen dependencies (surface and ask for prioritization)
- Architectural uncertainty (present options with tradeoffs)
- Completion checkpoints (summarize and confirm next steps)

### III. Phase Governance

**Each phase is strictly scoped; future-phase features MUST NOT leak into earlier phases.**

The Evolution of Todo project consists of five phases:

- **Phase I**: Basic Todo CRUD with local persistence
  - Backend: In-memory console application only
  - UI/UX: Console-based interface only
- **Phase II**: Multi-user support with authentication and cloud persistence
  - Backend: Python REST API
  - Database: Neon Serverless PostgreSQL
  - ORM/Data layer: SQLModel or equivalent
  - Frontend: Next.js (React, TypeScript)
  - Authentication: Better Auth (signup/signin)
  - Architecture: Full-stack web application
  - UI/UX: Modern, professional, hackathon-quality UI with gradient-based colorful theme, subtle animations (hover effects, transitions, loading states), smooth page transitions, clean card-based layouts and spacing. UI enhancements must be visual only and must not change functionality.
- **Phase III**: Real-time collaboration, notifications, and advanced search
- **Phase IV**: Agent orchestration, MCP integration, and workflow automation
- **Phase V**: Distributed architecture with event sourcing and CQRS

**Phase Isolation Rules**:
1. Each phase has its own specification in `specs/phase-<N>-<name>/`
2. Implementation MUST NOT reference or depend on future-phase features
3. Architecture MAY evolve only through updated specifications and plans
4. Phase boundaries are enforcement points; no feature may span phases without explicit specification

**Rationale**: Strict phase isolation prevents premature optimization, maintains focus on current deliverables, enables incremental validation, and ensures each phase delivers standalone value.

### IV. Technology Stack

**The following technology constraints are mandatory across all phases:**

**Backend** (Phase II+):
- Language: Python 3.11+
- Framework: FastAPI (async web framework) for REST API
- ORM: SQLModel (Pydantic + SQLAlchemy) or equivalent
- Database: Neon Serverless PostgreSQL
- Agent Framework: OpenAI Agents SDK (Phase IV+)
- MCP: Model Context Protocol servers (Phase IV+)

**Frontend** (Phase II+):
- Framework: Next.js (React with SSR/SSG)
- Language: TypeScript
- State Management: To be specified per phase requirements

**Authentication** (Phase II+):
- Solution: Better Auth (signup/signin)

**Architecture** (Phase II+):
- Full-stack web application

**Infrastructure** (Phase III+):
- Containerization: Docker
- Orchestration: Kubernetes
- Event Streaming: Apache Kafka (Phase V)
- Service Mesh: Dapr (Phase V)

**Rationale**: Standardizing the technology stack ensures consistency across phases, reduces cognitive load, enables code reuse, and simplifies integration. These technologies are chosen for their cloud-native capabilities, strong typing, async support, and agent integration features.

**Exceptions**: Technology changes MUST be proposed through constitution amendments with clear justification.

### V. Quality Principles

**Clean Architecture**:
- MUST maintain clear separation of concerns (domain, application, infrastructure layers)
- MUST define explicit boundaries between layers with well-defined interfaces
- MUST ensure domain logic is independent of frameworks and infrastructure
- Business rules MUST NOT depend on UI, database, or external services

**Stateless Services** (where applicable):
- Services MUST be stateless to enable horizontal scaling (Phase III+)
- All state MUST be externalized to databases, caches, or message queues
- Session state MUST be stored in distributed caches or databases (Phase II+)

**Cloud-Native Readiness**:
- Applications MUST support 12-factor app principles
- Configuration MUST be environment-based (via environment variables or config services)
- Services MUST expose health checks and readiness probes
- Logs MUST be structured (JSON) and written to stdout (Phase III+)
- Metrics MUST be exposed in Prometheus format (Phase III+)

**Testing Discipline**:
- Test-Driven Development (TDD) is RECOMMENDED but not mandatory
- All features MUST have integration tests covering primary user journeys
- All APIs MUST have contract tests
- Critical business logic MUST have unit tests
- Test coverage targets: 80% line coverage minimum

**Security**:
- MUST follow OWASP Top 10 guidelines
- MUST NOT hardcode secrets, credentials, or tokens
- MUST use environment variables or secret management services
- MUST implement proper authentication and authorization (Phase II+)
- MUST sanitize all user inputs
- MUST implement rate limiting on public APIs (Phase II+)

**Performance**:
- API responses MUST complete within 200ms p95 latency (Phase III+ under normal load)
- Database queries MUST be optimized and indexed appropriately
- MUST implement caching strategies for frequently accessed data (Phase III+)
- MUST monitor and alert on performance degradation

**Rationale**: Quality principles ensure the system remains maintainable, scalable, and reliable as it evolves across phases. These principles prevent technical debt accumulation and enable sustainable long-term development.

## Technology Constraints

**Language & Runtime Requirements**:
- Python 3.11 or higher for all backend services
- Node.js 18+ for frontend tooling and Next.js runtime
- TypeScript 5+ for all frontend code
- Strict type checking enabled (mypy for Python, strict mode for TypeScript)

**Dependency Management**:
- Backend: Poetry or pip-tools for Python dependency management
- Frontend: npm or pnpm for JavaScript dependency management
- MUST pin exact versions in production
- MUST document all direct dependencies with purpose

**Database Requirements**:
- Primary database: Neon Serverless PostgreSQL
- MUST use SQLModel or equivalent for ORM operations
- MUST version control all schema migrations
- MUST support rollback for all migrations

**API Standards**:
- REST APIs MUST follow OpenAPI 3.0+ specification
- MUST use semantic HTTP status codes
- MUST implement proper error response formats (RFC 7807 Problem Details)
- MUST version APIs (e.g., `/api/v1/...`)

**Development Environment**:
- MUST support local development with Docker Compose
- MUST provide setup documentation in quickstart.md
- MUST use consistent code formatting (Black for Python, Prettier for TypeScript)
- MUST enforce linting (ruff for Python, ESLint for TypeScript)

**UI/UX Requirements** (Phase II+):
- MUST implement modern, professional, hackathon-quality UI
- MUST use gradient-based colorful theme across the application
- MAY include subtle animations (hover effects, transitions, loading states)
- MAY implement smooth page transitions
- MUST use clean card-based layouts and spacing
- UI enhancements MUST be visual only and MUST NOT change functionality

## Development Workflow

**Spec-Driven Development Workflow** (mandatory for all features):

1. **Constitution Review**: Verify feature aligns with constitutional principles
2. **Specification** (`/sp.specify`):
   - Create feature specification with user stories, requirements, and success criteria
   - Document in `specs/<feature>/spec.md`
   - Obtain user approval
3. **Planning** (`/sp.plan`):
   - Research existing codebase patterns
   - Design architecture and implementation approach
   - Document in `specs/<feature>/plan.md`
   - Identify Architectural Decision Records (ADRs) if needed
   - Obtain user approval
4. **Task Breakdown** (`/sp.tasks`):
   - Break down plan into specific, testable tasks
   - Document in `specs/<feature>/tasks.md`
   - Organize by user story for independent testing
   - Obtain user approval
5. **Implementation** (`/sp.implement`):
   - Execute tasks in dependency order
   - Create tests before implementation (if TDD requested)
   - Commit after each task or logical group
   - Reference tasks in commit messages
6. **Review & Integration**:
   - Run all tests
   - Verify acceptance criteria from specification
   - Create pull request with specification reference
   - Document with `/sp.adr` if architectural decisions made

**Prompt History Records (PHR)**:
- MUST create PHR after every user interaction involving implementation, planning, or specification
- PHR routing: constitution → `history/prompts/constitution/`, feature → `history/prompts/<feature>/`, general → `history/prompts/general/`
- MUST capture full user prompt verbatim (no truncation)
- MUST record stage, title, date, files changed, and representative response

**Architectural Decision Records (ADR)**:
- MUST suggest ADR when architecturally significant decisions are made during planning or task generation
- ADR suggestion format: "📋 Architectural decision detected: [brief description] — Document reasoning and tradeoffs? Run `/sp.adr <decision-title>`"
- MUST NOT auto-create ADRs; require user consent
- ADR significance test (ALL must be true):
  - Impact: Long-term consequences (framework, data model, API, security, platform)
  - Alternatives: Multiple viable options considered
  - Scope: Cross-cutting and influences system design

**Git Workflow**:
- Feature branches: `<issue-number>-<feature-name>` (e.g., `001-phase-i-todo-crud`)
- Commit messages: Follow Conventional Commits (e.g., `feat:`, `fix:`, `docs:`, `refactor:`)
- Pull requests: MUST reference specification and include summary of changes
- MUST pass all tests and linting before merge

**Code Review Requirements**:
- All code changes MUST go through pull request review
- MUST verify compliance with constitution principles
- MUST verify implementation matches approved specification
- MUST verify tests are included and passing
- MUST verify no future-phase features leaked into current phase

## Governance

**Constitutional Authority**:
- This constitution is the supreme governing document for all agents and developers
- All specifications, plans, and implementations MUST comply with this constitution
- When conflicts arise between constitution and other documents, constitution takes precedence

**Amendment Process**:
1. Propose amendment with clear justification in user input
2. Agent drafts updated constitution using `/sp.constitution` command
3. Version is incremented according to semantic versioning:
   - MAJOR: Backward incompatible governance/principle removals or redefinitions
   - MINOR: New principle/section added or materially expanded guidance
   - PATCH: Clarifications, wording, typo fixes, non-semantic refinements
4. Sync Impact Report is generated showing affected templates and files
5. User approves amendment
6. Constitution is updated and all dependent templates are synchronized
7. Amendment is committed with clear commit message

**Compliance Review**:
- All pull requests MUST include constitution compliance verification
- Agents MUST flag any potential constitutional violations before implementation
- Non-compliant code MUST be reverted and re-implemented following proper workflow

**Versioning Policy**:
- Constitution version follows semantic versioning (MAJOR.MINOR.PATCH)
- Version is tracked in this document footer
- Changes MUST be documented in Sync Impact Report comments

**Conflict Resolution**:
- When specifications conflict with constitution, constitution wins
- When plans conflict with specifications, specifications win (plan must be updated)
- When implementation conflicts with plans, plans win (implementation must be corrected)
- Ambiguities MUST be resolved at the highest applicable level (constitution > spec > plan > tasks)

**Scope of Authority**:
- Constitution applies to ALL phases (Phase I through Phase V)
- Constitution applies to ALL agents working on the Evolution of Todo project
- Constitution applies to ALL features, regardless of size or complexity

**Definition of Done** (for all features):
- [ ] Specification approved by user
- [ ] Plan approved by user
- [ ] Tasks approved by user
- [ ] All tasks completed
- [ ] All tests passing
- [ ] Constitution compliance verified
- [ ] Code review completed
- [ ] Documentation updated (if applicable)
- [ ] ADRs created for significant decisions (if applicable)
- [ ] PHR created for the work

**Version**: 1.1.0 | **Ratified**: 2025-12-28 | **Last Amended**: 2025-12-29
