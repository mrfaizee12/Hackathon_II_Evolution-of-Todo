<!--
Sync Impact Report
==================
Version: 1.2.0 → 1.3.0
Change Type: MINOR - Phase II Intermediate extension with authorized features and restrictions

Changes Made:
- Updated Phase Isolation Policy:
  - Phase I (In-Memory Console Application) is finalized and immutable
  - Phase II Basic (Full-Stack Web Application with basic todo features) is completed and must not be broken
  - All new development is restricted to Phase II Intermediate as incremental, non-breaking extensions
- Added Phase II Intermediate Extension with authorized features:
  - Todo priorities (high / medium / low)
  - Todo tags or categories
  - Search todos by keyword
  - Filter todos by status, priority, and due date
  - Sort todos by due date, priority, or alphabetical order
  - UI enhancements: Public landing page, Hero section, Footer, Improved authenticated dashboard UI
- Mandated Technology Requirements for Phase II:
  - Backend: FastAPI (Python REST API)
  - Database: Neon Serverless PostgreSQL
  - ORM / Data Layer: SQLModel
  - Frontend: Next.js (React, TypeScript)
  - Authentication: Better Auth (signup/signin only)
  - Dependency management: UV
- Added Global Restrictions: No AI or agent frameworks, No background jobs or workers, No real-time features, No future-phase infrastructure or technologies
- Emphasized Enforcement: Phase II Intermediate work must extend existing Phase II Basic behavior without refactoring or breaking changes

Templates Status:
- ✅ .specify/templates/plan-template.md - Aligned with updated architecture options
- ✅ .specify/templates/spec-template.md - Aligned with priority/search requirements
- ✅ .specify/templates/tasks-template.md - Aligned with setup/foundation requirements for Phase II
- ✅ .specify/templates/phr-template.prompt.md - Aligned with updated constitution

Follow-up Actions:
- None - all placeholders filled, all templates aligned

Notes:
- This amendment enables Phase II Intermediate development while maintaining strict phase isolation and non-breaking extension policy.
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

**Rationale**: Spec-Driven Development ensures all stakeholders understand requirements before code is written, prevents scope creep, enables accurate effort estimation, and creates traceable documentation. This is particularly critical for the Evolution of Todo project, which spans multiple phases with increasing complexity.

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

The Evolution of Todo project consists of multiple phases with strict isolation:

**Phase Isolation Policy**:
- Phase I (In-Memory Console Application) is finalized and immutable.
- Phase II Basic (Full-Stack Web Application with basic todo features) is completed and must not be broken.
- All new development is restricted to Phase II Intermediate as incremental, non-breaking extensions.

**Phase II — Intermediate Extension (Authorized)**:
Phase II is permitted to evolve beyond basic functionality to include intermediate-level organization and usability features.

**Allowed functionality additions in Phase II Intermediate**:
- Todo priorities (high / medium / low)
- Todo tags or categories
- Search todos by keyword
- Filter todos by status, priority, and due date
- Sort todos by due date, priority, or alphabetical order
- UI enhancements limited strictly to:
  - Public landing page
  - Hero section
  - Footer
  - Improved authenticated dashboard UI

**Mandatory Technology Requirements (Phase II)**:
- Backend: FastAPI (Python REST API)
- Database: Neon Serverless PostgreSQL
- ORM / Data Layer: SQLModel
- Frontend: Next.js (React, TypeScript)
- Authentication: Better Auth (signup/signin only)
- Dependency management: UV

**Global Restrictions**:
- No AI or agent frameworks
- No background jobs or workers
- No real-time features
- No future-phase infrastructure or technologies

**Enforcement**:
- Phase II Intermediate work must extend existing Phase II Basic behavior without refactoring or breaking changes.
- This constitution amendment is authoritative and must be enforced across all specifications, plans, tasks, and implementations.

**Phase Isolation Rules**:
1. Each phase has its own specification in `specs/phase-<N>-<name>/`
2. Implementation MUST NOT reference or depend on future-phase features
3. Architecture MAY evolve only through updated specifications and plans
4. Phase boundaries are enforcement points; no feature may span phases without explicit specification
5. **No AI or agent frameworks** are allowed until authorized phases.
6. **No breaking changes** are permitted to completed phases.

**Rationale**: Strict phase isolation prevents premature optimization, maintains focus on current deliverables, enables incremental validation, and ensures each phase delivers standalone value while maintaining backward compatibility.

### IV. Technology Stack

**The following technology constraints are mandatory across all phases:**

**Backend** (Phase II+):
- Language: Python 3.11+
- Framework: FastAPI (async web framework) for REST API
- ORM: SQLModel (Pydantic + SQLAlchemy)
- Database: Neon Serverless PostgreSQL
- Dependency Management: UV

**Frontend** (Phase II+):
- Framework: Next.js 14+ (App Router, React, TypeScript)
- Language: TypeScript
- UI: Tailwind CSS (with gradient themes)

**Authentication** (Phase II+):
- Solution: Better Auth (signup/signin only)

**Architecture** (Phase II+):
- Full-stack web application (Separated Backend/Frontend folders if applicable)

**Infrastructure** (Authorized Phases):
- Containerization: Docker
- Orchestration: Kubernetes

**Rationale**: Standardizing the technology stack ensures consistency across phases, reduces cognitive load, enables code reuse, and simplifies integration. These technologies are chosen for their cloud-native capabilities, strong typing, async support, and proven reliability.

**Exceptions**: Technology changes MUST be proposed through constitution amendments with clear justification.

### V. Quality Principles

**Clean Architecture**:
- MUST maintain clear separation of concerns (domain, application, infrastructure layers)
- MUST define explicit boundaries between layers with well-defined interfaces
- MUST ensure domain logic is independent of frameworks and infrastructure
- Business rules MUST NOT depend on UI, database, or external services

**Stateless Services** (where applicable):
- Services MUST be stateless to enable horizontal scaling
- All state MUST be externalized to databases, caches, or message queues
- Session state MUST be handled by centralized Auth (Better Auth) and DB.

**Cloud-Native Readiness**:
- Applications MUST support 12-factor app principles
- Configuration MUST be environment-based (via .env or secret management)
- Services MUST expose health checks and readiness probes
- Logs MUST be structured (JSON) and written to stdout
- Metrics MUST be exposed in Prometheus format

**Testing Discipline**:
- All features MUST have integration tests covering primary user journeys
- All APIs MUST have contract tests
- Critical business logic MUST have unit tests
- Test coverage targets: 80% line coverage minimum

**Security**:
- MUST follow OWASP Top 10 guidelines
- MUST NOT hardcode secrets, credentials, or tokens
- MUST use environment variables for all secrets
- MUST implement proper authentication and authorization (Phase II+)
- MUST sanitize all user inputs
- MUST implement rate limiting on public APIs (Phase II+)

**Performance**:
- API responses MUST complete within 200ms p95 latency under normal load
- Database queries MUST be optimized and indexed appropriately
- MUST implement caching strategies for frequently accessed data

**Rationale**: Quality principles ensure the system remains maintainable, scalable, and reliable as it evolves across phases. These principles prevent technical debt accumulation and enable sustainable long-term development.

## Technology Constraints

**Language & Runtime Requirements**:
- Python 3.11 or higher for all backend services
- Node.js 18+ for frontend tooling and Next.js runtime
- TypeScript 5+ for all frontend code
- Strict type checking enabled (mypy for Python, strict mode for TypeScript)

**Dependency Management**:
- Backend: UV (Python package manager)
- Frontend: npm or pnpm
- MUST pin exact versions in production
- MUST document all direct dependencies with purpose

**Database Requirements**:
- Primary database: Neon Serverless PostgreSQL
- MUST use SQLModel for ORM operations
- MUST version control all schema migrations
- MUST support rollback for all migrations

**API Standards**:
- REST APIs MUST follow OpenAPI 3.0+ specification
- MUST use semantic HTTP status codes
- MUST implement proper error response formats (RFC 7807 Problem Details)
- MUST version APIs (e.g., `/api/v1/...`)

**Development Environment**:
- MUST support local development
- MUST provide setup documentation in quickstart.md
- MUST use consistent code formatting (Black for Python, Prettier for TypeScript)
- MUST enforce linting (ruff for Python, ESLint for TypeScript)

**UI/UX Requirements** (Phase II+):
- MUST implement modern, professional, hackathon-quality UI
- MUST use gradient-based colorful theme across the application
- MUST include subtle animations (hover effects, transitions, loading states)
- MUST implement smooth page transitions
- MUST use clean card-based layouts and spacing
- MUST include a Landing Page with hero section and footer
- UI enhancements MUST be visual only and MUST NOT change functionality
- Allowed UI enhancements: Public landing page, Hero section, Footer, Improved authenticated dashboard UI

## Development Workflow

**Spec-Driven Development Workflow** (mandatory for all features):

1. **Constitution Review**: Verify feature aligns with constitutional principles
2. **Specification** (`/sp.specify`):
   - Create feature specification in `specs/<feature>/spec.md`
   - Include user stories, requirements (FRs), success criteria (SCs)
3. **Planning** (`/sp.plan`):
   - Research existing codebase patterns
   - Design architecture and implementation approach
   - Document in `specs/<feature>/plan.md`
4. **Task Breakdown** (`/sp.tasks`):
   - Break down plan into specific, testable tasks
   - Document in `specs/<feature>/tasks.md`
5. **Implementation** (`/sp.implement`):
   - Execute tasks in dependency order
   - Commit after each task or logical group
6. **Review & Integration**:
   - Run all tests and verify acceptance criteria

**Prompt History Records (PHR)**:
- MUST create PHR after every user interaction involving implementation, planning, or specification
- PHR routing: constitution → `history/prompts/constitution/`, feature → `history/prompts/<feature>/`, general → `history/prompts/general/`

**Architectural Decision Records (ADR)**:
- MUST suggest ADR when architecturally significant decisions are made
- ADR significance test (ALL must be true):
  - Impact: Long-term consequences
  - Alternatives: Multiple viable options considered
  - Scope: Cross-cutting and influences system design

**Git Workflow**:
- Commit messages: Follow Conventional Commits
- Pull requests: MUST reference specification and include summary of changes
- MUST pass all tests and linting before merge

## Governance

**Constitutional Authority**:
- This constitution is the supreme governing document for all agents and developers
- All specifications, plans, and implementations MUST comply with this constitution

**Amendment Process**:
1. Propose amendment with clear justification in user input
2. Agent drafts updated constitution using `/sp.constitution` command
3. Version is incremented according to semantic versioning
4. Sync Impact Report is generated showing affected templates and files

**Versioning Policy**:
- Version: 1.3.0
- Ratified: 2025-12-28
- Last Amended: 2026-01-05
