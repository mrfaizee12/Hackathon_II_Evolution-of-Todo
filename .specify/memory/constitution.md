<!--
     Sync Impact Report
     ==================
     Version: 2.0.0 → 3.0.0
     Change Type: MAJOR - Phase IV Cloud-Native Deployment introduction with containerization and Kubernetes orchestration requirements

     Changes Made:
     - Added Phase IV Cloud-Native Deployment Extension with authorized features:
       - Expert DevOps AI Orchestrator for Kubernetes migration
       - Strict Spec-Driven approach for deployment artifacts
       - Containerization using Multi-stage builds for FastAPI and Next.js
       - Orchestration on Minikube using Helm Charts
       - AIOps integration using Gordon, kubectl-ai, and Kagent
     - Updated Technology Requirements to include containerization and orchestration tools for Phase IV
     - Added new Phase IV workflow protocol for deployment activities
     - Introduced tool preferences for Gordon, kubectl-ai, and Kagent for containerization and orchestration

     Templates Status:
     - ✅ .specify/templates/plan-template.md - Aligned with updated architecture options including cloud-native deployment
     - ✅ .specify/templates/spec-template.md - Aligned with cloud-native deployment requirements
     - ✅ .specify/templates/tasks-template.md - Aligned with containerization and orchestration requirements for Phase IV
     - ✅ .specify/templates/phr-template.prompt.md - Aligned with updated constitution

     Follow-up Actions:
     - None - all placeholders filled, all templates aligned

     Notes:
     - This amendment enables Phase IV Cloud-Native Deployment while maintaining strict phase isolation and non-breaking extension policy. Containerization and orchestration tools are now authorized specifically for Phase IV, introducing Gordon, kubectl-ai, and Kagent as preferred tools for deployment activities. All deployment artifacts must follow Spec-Driven approach with no manual coding allowed.
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
     - Phase II Intermediate (Todo priorities, tags, search, filters, UI enhancements) is completed and must not be broken.
     - Phase III AI Todo Chatbot (AI features as native dashboard components) is completed and must not be broken.
     - All new development is restricted to Phase IV Cloud-Native Deployment as incremental, non-breaking extensions for deployment activities only.

     **Phase III — AI Todo Chatbot (Completed)**:
     Phase III evolved the todo application to include AI-powered features while maintaining all existing functionality. AI features were implemented as native dashboard components without breaking existing functionality or requiring separate applications/pages.

     **Phase IV — Cloud-Native Deployment (Authorized)**:
     Phase IV is permitted to migrate the Phase III Todo Chatbot to a Local Kubernetes Environment (Minikube) using a strictly Spec-Driven approach. All deployment artifacts (Dockerfiles, Helm Charts, K8s Manifests) must be generated via Agent Skills or AI Tools (Gordon/kubectl-ai) with no manual coding allowed. The system must maintain all existing functionality while enabling cloud-native deployment capabilities.


     **Allowed functionality additions in Phase IV Cloud-Native Deployment**:
     - Expert DevOps AI Orchestrator for Kubernetes migration
     - Containerization using Multi-stage builds for Frontend (Next.js) and Backend (FastAPI)
     - Orchestration on Minikube using Helm Charts
     - AIOps integration using `docker ai`, `kubectl-ai`, and `kagent` tools
     - Deployment workflow: Spec Writing → Plan Generation → Task Execution → Validation
     - Image optimization using Gordon (Docker AI)
     - Automated scaling using kubectl-ai
     - Cluster health monitoring using Kagent
     - Deployment naming convention: Image Tags: `faizananjum/<app-name>:v1`, Namespace: `todo-chatbot`

     **Mandatory Technology Requirements (Phase IV)**:
     - Containerization: Multi-stage builds for Frontend (Next.js) and Backend (FastAPI)
     - Orchestration: Deploy on Minikube using Helm Charts
     - Tool Preference: Use 'Gordon' (Docker AI) for all containerization tasks
     - Tool Preference: Use 'kubectl-ai' or 'Kagent' for all Kubernetes operations
     - AIOps Integration: Use `docker ai` for image optimization suggestions
     - AIOps Integration: Use `kubectl-ai` for generating K8s resources (e.g., "deploy frontend with 2 replicas")
     - AIOps Integration: Use `kagent` for debugging cluster health and resource optimization
     - Verification First: Before any deployment, verify that Minikube is running and Docker Desktop (Beta) is active
     - No Manual Coding: All Dockerfiles, Helm Charts, and K8s Manifests must be generated via Agent Skills or AI Tools
     - Workflow Protocol: Spec Writing → Plan Generation → Task Execution → Validation
     - Error Handling: Use AIOps-Observability-Skill to diagnose using Kagent logic for pod failures
     - Deployment Naming Convention: Image Tags: `faizananjum/<app-name>:v1`, Namespace: `todo-chatbot`

     **Updated Global Restrictions** (for future phases beyond Phase IV):
     - No background jobs or workers
     - No real-time features
     - No future-phase infrastructure or technologies
     - AI and agent frameworks are NOW AUTHORIZED for Phase III and Phase IV (previously restricted)

     **Enforcement**:
     - Phase IV work must extend existing Phase III behavior without refactoring or breaking changes to functionality.
     - Deployment artifacts MUST be generated via AI tools (Gordon, kubectl-ai, Kagent) with no manual coding allowed.
     - Backend and frontend services MUST remain stateless with all state stored in Neon PostgreSQL.
     - This constitution amendment is authoritative and must be enforced across all specifications, plans, tasks, and implementations.

     **Phase Isolation Rules**:
     1. Each phase has its own specification in `specs/phase-<N>-<name>/`
     2. Implementation MUST NOT reference or depend on future-phase features
     3. Architecture MAY evolve only through updated specifications and plans
     4. Phase boundaries are enforcement points; no feature may span phases without explicit specification
     5. Containerization and orchestration tools are now authorized specifically for Phase IV
     6. **No breaking changes** are permitted to completed phases (I, II Basic, II Intermediate, III AI Chatbot).
     7. Phase IV deployment activities MUST maintain all existing functionality while enabling cloud-native capabilities.

     **Rationale**: Strict phase isolation prevents premature optimization, maintains focus on current deliverables, enables incremental validation, and ensures each phase delivers standalone value while maintaining backward compatibility. The authorization of containerization and orchestration tools for Phase IV represents a strategic evolution toward cloud-native deployment while preserving all existing functionality. The Spec-Driven approach ensures all deployment artifacts are properly specified and validated before implementation.

     ### IV. Technology Stack

     **The following technology constraints are mandatory across all phases:**

     **Backend** (Phase II+ and Phase III and Phase IV):
     - Language: Python 3.11+
     - Framework: FastAPI (async web framework) for REST API
     - ORM: SQLModel (Pydantic + SQLAlchemy)
     - Database: Neon Serverless PostgreSQL
     - Dependency Management: UV
     - AI Integration: OpenRouter API compatible with OpenAI Agents SDK
     - Model: openrouter/deepseek/deepseek-r1-0528-qwen3-8b:free
     - Base URL: https://openrouter.ai/api/v1

     **Frontend** (Phase II+ and Phase III and Phase IV):
     - Framework: Next.js 14+ (App Router, React, TypeScript)
     - Language: TypeScript
     - UI: Tailwind CSS (with gradient themes)
     - AI Chat Interface: Integrated into existing dashboard UI, opened from sidebar

     **Authentication** (Phase II+ and Phase III and Phase IV):
     - Solution: Better Auth (signup/signin only)

     **Architecture** (Phase II+ and Phase III and Phase IV):
     - Full-stack web application with stateless services
     - AI logic in backend, UI in frontend
     - All state persisted in Neon PostgreSQL database
     - Native dashboard integration for AI features

     **Infrastructure** (Authorized Phases):
     - Containerization: Docker (Multi-stage builds with Gordon optimization)
     - Orchestration: Kubernetes (Minikube for local development, Helm Charts for packaging)
     - AIOps: Gordon (Docker AI), kubectl-ai, Kagent for automation and monitoring

     **Rationale**: Standardizing the technology stack ensures consistency across phases, reduces cognitive load, enables code reuse, and simplifies integration. These technologies are chosen for their cloud-native capabilities, strong typing, async support, and proven reliability. The addition of containerization and orchestration tools in Phase IV extends the stack to include cloud-native deployment capabilities while maintaining the existing architecture patterns. The AIOps tools (Gordon, kubectl-ai, Kagent) provide intelligent automation for containerization and orchestration tasks.

     **Exceptions**: Technology changes MUST be proposed through constitution amendments with clear justification.

     ### V. Quality Principles

     **Clean Architecture**:
     - MUST maintain clear separation of concerns (domain, application, infrastructure layers)
     - MUST define explicit boundaries between layers with well-defined interfaces
     - MUST ensure domain logic is independent of frameworks and infrastructure
     - Business rules MUST NOT depend on UI, database, or external services

     **Stateless Services** (Phase III AI Logic):
     - AI services MUST be stateless to enable horizontal scaling
     - All state MUST be externalized to databases, caches, or message queues
     - Session state MUST be handled by centralized Auth (Better Auth) and DB
     - AI conversation state MUST be stored in Neon PostgreSQL

     **Cloud-Native Readiness** (Phase IV):
     - Applications MUST support 12-factor app principles
     - Configuration MUST be environment-based (via .env or secret management)
     - Services MUST expose health checks and readiness probes
     - Logs MUST be structured (JSON) and written to stdout
     - Metrics MUST be exposed in Prometheus format
     - Container images MUST be optimized using multi-stage builds
     - Deployment configurations MUST be parameterized using Helm values
     - Resource limits and requests MUST be properly configured for Kubernetes

     **Testing Discipline**:
     - All features MUST have integration tests covering primary user journeys
     - All APIs MUST have contract tests
     - Critical business logic MUST have unit tests
     - AI features MUST include conversation flow tests
     - Deployment configurations MUST be validated using Helm dry-run
     - Test coverage targets: 80% line coverage minimum

     **Security**:
     - MUST follow OWASP Top 10 guidelines
     - MUST NOT hardcode secrets, credentials, or tokens
     - MUST use environment variables for all secrets
     - MUST implement proper authentication and authorization (Phase II+)
     - MUST sanitize all user inputs including AI chat inputs
     - MUST implement rate limiting on public APIs and AI endpoints (Phase II+)
     - MUST protect against prompt injection attacks in AI features
     - Kubernetes deployments MUST follow security best practices (non-root users, resource limits, RBAC)

     **Performance**:
     - API responses MUST complete within 200ms p95 latency under normal load
     - AI responses MUST complete within 5000ms p95 latency under normal load
     - Database queries MUST be optimized and indexed appropriately
     - MUST implement caching strategies for frequently accessed data
     - Container images MUST be optimized for fast startup times
     - Kubernetes deployments MUST be configured for appropriate resource allocation

     **Rationale**: Quality principles ensure the system remains maintainable, scalable, and reliable as it evolves across phases. These principles prevent technical debt accumulation and enable sustainable long-term development. The addition of AI-specific and cloud-native requirements ensures safe and performant AI integration while maintaining security, scalability and deployment standards. The Spec-Driven approach for Phase IV ensures all deployment artifacts are properly validated before implementation in Kubernetes environments.

     ## Technology Constraints

     **Language & Runtime Requirements**:
     - Python 3.11 or higher for all backend services including AI logic
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
     - AI conversation history MUST be stored in Neon PostgreSQL

     **AI Framework Requirements** (Phase III):
     - AI Provider: OpenRouter API
     - Compatible with: OpenAI Agents SDK
     - Model: openrouter/deepseek/deepseek-r1-0528-qwen3-8b:free
     - Base URL: https://openrouter.ai/api/v1
     - MUST NOT use OpenAI API key directly
     - MUST NOT use Cohere or Gemini
     - AI integration MUST be stateless with state stored in database

     **Containerization Requirements** (Phase IV):
     - Container Engine: Docker (with Docker Desktop Beta features)
     - Build Strategy: Multi-stage builds for both Frontend (Next.js) and Backend (FastAPI)
     - Optimization Tool: Gordon (Docker AI) for image optimization and layer caching
     - Orchestration Format: Docker Compose for local testing before Kubernetes deployment
     - Image Registry: Container images tagged as `faizananjum/<app-name>:v1`

     **Kubernetes Requirements** (Phase IV):
     - Orchestration Platform: Minikube for local development
     - Packaging Format: Helm Charts for deployment configuration
     - Tool Preference: kubectl-ai for intelligent Kubernetes resource management
     - Monitoring Tool: Kagent for cluster health analysis and debugging
     - Namespace: `todo-chatbot` for all deployment resources
     - Resource Types: Deployments, Services, Ingress, HPA, ConfigMaps, Secrets

     **API Standards**:
     - REST APIs MUST follow OpenAPI 3.0+ specification
     - AI APIs MUST follow OpenAI-compatible interface standards
     - Kubernetes APIs MUST follow standard resource definitions
     - MUST use semantic HTTP status codes
     - MUST implement proper error response formats (RFC 7807 Problem Details)
     - MUST version APIs (e.g., `/api/v1/...`)

     **Development Environment**:
     - MUST support local development
     - MUST support Minikube local cluster setup
     - MUST provide setup documentation in quickstart.md
     - MUST use consistent code formatting (Black for Python, Prettier for TypeScript)
     - MUST enforce linting (ruff for Python, ESLint for TypeScript)

     **UI/UX Requirements** (Phase II+ and Phase III and Phase IV):
     - MUST implement modern, professional, hackathon-quality UI
     - MUST use gradient-based colorful theme across the application
     - MUST include subtle animations (hover effects, transitions, loading states)
     - MUST implement smooth page transitions
     - MUST use clean card-based layouts and spacing
     - MUST include a Landing Page with hero section and footer
     - UI enhancements MUST be visual only and MUST NOT change functionality
     - Allowed UI enhancements: Public landing page, Hero section, Footer, Improved authenticated dashboard UI
     - Phase III AI Chatbot: Integrated into dashboard sidebar, opens as native component
     - NO auto-execution of AI features on page load

     ## Development Workflow

     **Spec-Driven Development Workflow** (mandatory for all features including deployments):

     1. **Constitution Review**: Verify feature aligns with constitutional principles
     2. **Specification** (`/sp.specify`):
        - Create feature specification in `specs/<feature>/spec.md`
        - Include user stories, requirements (FRs), success criteria (SCs)
        - For Phase IV: Include deployment architecture, containerization strategy, orchestration approach
     3. **Planning** (`/sp.plan`):
        - Research existing codebase patterns
        - Design architecture and implementation approach
        - For Phase IV: Plan containerization, Helm packaging, and Kubernetes deployment strategy
        - Document in `specs/<feature>/plan.md`
     4. **Task Breakdown** (`/sp.tasks`):
        - Break down plan into specific, testable tasks
        - For Phase IV: Separate tasks for containerization, Helm chart creation, and deployment validation
        - Document in `specs/<feature>/tasks.md`
     5. **Implementation** (`/sp.implement`):
        - Execute tasks in dependency order
        - For Phase IV: Use Gordon for containerization, kubectl-ai for Kubernetes resources, Kagent for validation
        - Commit after each task or logical group
     6. **Deployment & Validation** (Phase IV):
        - Verify Minikube is running and Docker Desktop (Beta) is active
        - Execute deployment workflow: Spec Writing → Plan Generation → Task Execution → Validation
        - Run `kubectl get pods` and `kagent "analyze cluster"` to ensure 100% health
        - For pod failures: Use AIOps-Observability-Skill to diagnose using Kagent logic
     7. **Review & Integration**:
        - Run all tests and verify acceptance criteria
        - Verify NO breaking changes to existing functionality

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
     - Phase IV commits MUST NOT break existing Phase I/II/III functionality

     ## Governance

     **Constitutional Authority**:
     - This constitution is the supreme governing document for all agents and developers
     - All specifications, plans, and implementations MUST comply with this constitution
     - Phase IV Cloud-Native Deployment development MUST NOT violate any existing Phase I/II/III requirements

     **Amendment Process**:
     1. Propose amendment with clear justification in user input
     2. Agent drafts updated constitution using `/sp.constitution` command
     3. Version is incremented according to semantic versioning
     4. Sync Impact Report is generated showing affected templates and files

     **Versioning Policy**:
     - Version: 3.0.0
     - Ratified: 2025-12-28
     - Last Amended: 2026-01-29