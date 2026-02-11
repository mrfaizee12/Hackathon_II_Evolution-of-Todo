<!--
Sync Impact Report
==================
Version: 3.0.0 → 4.0.0
Change Type: MAJOR - Phase V Event-Driven Microservices introduction with Kafka, Dapr, and Hugging Face deployment requirements

Changes Made:
- Complete overhaul of constitution to support Phase V Event-Driven Architecture
- Introduction of Agentic Development Stack: specify → plan → tasks → implement
- Removal of manual coding allowance - all work must be agentic
- Introduction of Hugging Face deployment constraint as strategic requirement
- Addition of event-driven architecture doctrine with Kafka and Dapr responsibilities
- New failure prevention rules and decision hierarchy for Phase V
- Updated success criteria for event-driven, decoupled system

Templates Status:
- ⚠️ .specify/templates/plan-template.md - Needs alignment with updated architecture options
- ⚠️ .specify/templates/spec-template.md - Needs alignment with event-driven architecture requirements
- ⚠️ .specify/templates/tasks-template.md - Needs alignment with event-driven and microservices requirements
- ⚠️ .specify/templates/phr-template.prompt.md - Needs alignment with updated constitution

Follow-up Actions:
- Templates need to be updated to reflect Phase V event-driven architecture
- All dependent artifacts need review to ensure consistency with new requirements

Notes:
- This amendment fundamentally changes the development approach to be strictly agentic with event-driven architecture focus. The Hugging Face deployment constraint is introduced as a non-negotiable strategic constraint. All Phase V work must follow the new event-driven microservices pattern with Kafka and Dapr responsibilities as specified.
-->

# Agentic Todo Chatbot — Execution Constitution

## Core Principles

### I. Agentic Development Stack (Mandatory)

**No development work may occur without following the strict agentic workflow.** All development work MUST follow the strict workflow:

1. specify → plan → tasks → implement
2. Manual coding is FORBIDDEN - all work MUST be executed via Claude Code using agents and skills
3. Every feature begins with a complete specification in `specs/<feature>/spec.md`
4. Every feature requires an approved implementation plan in `specs/<feature>/plan.md`
5. Every feature requires a task list in `specs/<feature>/tasks.md` before implementation
6. Implementation begins ONLY via `/sp.implement` using agent skills

**Rationale**: The Agentic Development Stack ensures all work follows autonomous agent execution, prevents manual coding deviations, maintains traceability, and creates consistent development methodology. This is particularly critical for Phase V Event-Driven Architecture with Kafka and Dapr complexities.

**Violations**: Manual coding or deviation from the agentic workflow is considered non-compliant and MUST be reverted.

### II. Spec-First Law (Mandatory)

**No implementation may begin without reading and understanding the specification.** The specification ALWAYS overrides assumptions and serves as the single source of truth:

- Spec-first development: No code, no plans, no tasks without complete spec
- Spec overrides all assumptions: When conflict exists between spec and assumption, spec wins
- Specification completeness check: All acceptance criteria, edge cases, and error paths must be defined
- Phase compliance: Each phase's spec defines the scope and boundaries for that phase

**Rationale**: Spec-First Law prevents implementation drift, ensures stakeholder alignment, and maintains clear requirements traceability. Specifications serve as the authoritative reference for all implementation decisions.

**Violations**: Starting implementation without complete, approved specification is non-compliant behavior.

### III. Skill Priority Enforcement

**Agents MUST prefer existing project skills before inventing new workflows.** The following hierarchy applies:

- Phase IV skills are considered ACTIVE infrastructure intelligence and MUST be leveraged
- Existing project skills take precedence over new tool recommendations
- Claude Code skills are preferred over shell commands or manual approaches
- Custom workflows should only be created when no suitable existing skill exists

**Rationale**: Skill priority prevents tool sprawl, maximizes existing investment, ensures consistency, and maintains architectural coherence. Phase IV infrastructure intelligence provides battle-tested patterns that should be reused.

**Enforcement**: Agents must check existing skills before proposing new approaches or manual execution.

### IV. Zero Manual Command Policy

**No shell commands should be requested from users unless absolutely unavoidable.** Autonomous execution is the default expectation:

- Claude must attempt autonomous execution of all required operations
- Shell commands should only be requested when agent capabilities are insufficient
- All deployment, build, and orchestration should use agent skills when possible
- Manual intervention should be exceptional, not routine

**Rationale**: Zero Manual Command Policy ensures autonomous operation, maintains traceability, reduces user friction, and demonstrates agent capability maturity. It forces the development of proper agent skills and workflows.

**Exception**: Only when agent capabilities are genuinely insufficient for required operations.

### V. Production Thinking Doctrine

**All design decisions must favor production-grade attributes over prototype considerations.** The following priorities apply:

- Scalability: Systems must handle growth and increased load gracefully
- Loose Coupling: Services must operate independently with minimal dependencies
- Event-Driven Architecture: Prefer asynchronous, event-based communication
- Observability: Systems must provide comprehensive logging, metrics, and tracing
- Resilience: Systems must handle failures gracefully with recovery mechanisms

**Rationale**: Production Thinking ensures the resulting system can operate reliably in real-world conditions, handles failure scenarios appropriately, and scales with user adoption. This prevents the common "hackathon-style shortcuts" that cause maintenance problems later.

**Anti-patterns**: Quick fixes, tight coupling, synchronous blocking operations, poor error handling, inadequate monitoring.

## Phase Governance

### Phase State Management

**Completed phases are stable infrastructure and must be built upon, not redesigned.** Current phase state:

**Completed Phases (Considered Stable Infrastructure)**:
- Phase I — Advanced Todo Features: COMPLETE, stable foundation
- Phase II — Chat + MCP: COMPLETE, stable foundation
- Phase III — Production Backend: COMPLETE, stable foundation
- Phase IV — Kubernetes + DevOps: COMPLETE, stable foundation

**Phase IV outputs are considered STABLE INFRASTRUCTURE.** Claude MUST build on them — NOT redesign them.

**Phase V — Event-Driven Microservices (Current)**:
- Transform the Todo Chatbot into an advanced event-driven microservices system
- Target capabilities: Recurring tasks, Due dates & reminders, Priorities/tags/filters/sorting
- Technical requirements: Kafka-based event streaming, Dapr distributed runtime, CI/CD, Monitoring
- Deployment target: Hugging Face Spaces/Docker-based hosting (NOT traditional cloud)

**Allowed functionality additions in Phase V**:
- Recurring tasks engine driven by Kafka events
- Due date reminder system with event-driven notifications
- Priority and tagging systems with filtering/sorting capabilities
- Kafka-based event streaming for audit trails and processing
- Dapr distributed runtime for service orchestration
- Event-driven architecture with loose coupling between services
- Container-ready services optimized for Hugging Face deployment

**Global Restrictions (Maintained)**:
- No breaking changes to completed phases (I, II, III, IV)
- No redesign of stable Phase IV infrastructure
- No credit card-dependent cloud services (Azure, GCP, Oracle)
- All new functionality must integrate with existing architecture

**Enforcement**:
- Phase V work must extend existing Phase IV behavior without breaking changes
- All event-driven services must maintain existing functionality while adding new capabilities
- Architecture evolution must follow loose coupling and event-driven patterns
- This constitution amendment is authoritative and must be enforced across all artifacts

### Critical Deployment Constraint

**Phase V deployment will be done on Hugging Face, NOT on credit card-requiring clouds.** This is a strategic constraint, not a limitation:

**Constraint Requirements**:
- NEVER push Azure/GCP setup recommendations
- NEVER recommend paid infrastructure requiring credit cards
- NEVER assume cloud access with billing
- NEVER block progress due to cloud access limitations
- Optimize architecture for Hugging Face deployment compatibility

**Preferred Patterns**:
- Container-ready services that run in constrained environments
- Lightweight event systems suitable for platform constraints
- Managed abstractions when possible to reduce operational overhead
- Stateless compute wherever feasible to reduce resource requirements

**Rationale**: The Hugging Face constraint ensures the system can be deployed without financial barriers, maintains accessibility for the user, and drives architectural decisions toward lightweight, efficient patterns that benefit the system regardless of ultimate deployment target.

## Event-Driven Architecture Doctrine

### Event-Driven vs Synchronous

**Prefer event-driven architectures over synchronous request-response patterns.** Decision hierarchy:

- EVENT-DRIVEN > SYNCHRONOUS - Use event-driven for all new services
- LOOSE COUPLING > DIRECT DEPENDENCIES - Services communicate via events
- SIDECARS > EMBEDDED INFRA - Use Dapr for infrastructure concerns
- CONFIG > HARD CODING - Configuration over hardcoded behavior

**Rationale**: Event-driven architecture provides better scalability, resilience, loose coupling, and ability to handle asynchronous operations like recurring tasks and reminders that are core to Phase V objectives.

### Kafka Responsibilities

**Kafka handles specific categories of event processing in the system.** Defined responsibilities:

- **task-events**: Audit trail and recurring task engine triggers
- **reminders**: Notification service activation for due date alerts
- **task-updates**: Real-time synchronization between services and UI

**Flexibility Requirement**: Kafka must be designed for portability so it can be swapped if hosting constraints demand it.

### Dapr Responsibilities

**Dapr provides distributed runtime capabilities for service coordination.** Core responsibilities:

- **Pub/Sub abstraction**: Message broker abstraction layer
- **State management**: Distributed state storage and retrieval
- **Service invocation**: Reliable inter-service communication
- **Secrets management**: Secure configuration and credential handling
- **Job scheduling**: Cron job and scheduled task management

**Rationale**: Dapr provides standardized patterns for distributed systems concerns, reducing custom code and improving reliability while maintaining platform portability.

## Local-First Strategy

### Pre-Production Validation

**Validate all architecture components locally before production deployment.** Validation sequence:

1. **Local Architecture Validation**: Ensure event-driven patterns work correctly
2. **Service Communication**: Verify services communicate properly via events
3. **Event Flow Confirmation**: Confirm all event flows function as designed
4. **Reminder & Recurring Logic**: Verify asynchronous processing works correctly

**Rationale**: Local-first validation catches integration issues early, reduces production deployment risk, and ensures the event-driven architecture functions correctly before deployment preparation.

**Gate Criteria**: Only after local validation succeeds should Hugging Face deployment artifacts be prepared.

## Failure Prevention Rules

### What NOT to Do

**Strict prohibitions to prevent architectural and implementation problems.** Mandatory avoidance:

- **Redesign completed phases**: Never redesign Phase I-IV stable infrastructure
- **Introduce unnecessary tools**: Only use tools that serve specific architectural needs
- **Over-engineer**: Implement the minimal viable solution that meets requirements
- **Create tight coupling**: Maintain loose coupling between services
- **Require enterprise cloud**: Never mandate credit card-dependent cloud services

### What TO Do

**Positive actions that ensure success.** Mandatory behaviors:

- **Reuse Helm outputs**: Leverage existing Phase IV deployment artifacts when applicable
- **Leverage Docker artifacts**: Build upon existing containerization patterns
- **Prefer minimal operational burden**: Choose solutions that reduce ongoing maintenance
- **Keep infrastructure portable**: Maintain flexibility for different deployment targets
- **Maintain backward compatibility**: Never break existing functionality

## Decision Hierarchy

### Priority Order for Uncertain Situations

**When uncertain about implementation approach, follow this priority order:**

1. **Spec correctness**: Ensure implementation matches specification requirements
2. **Deployment feasibility on Hugging Face**: Architecture must work on target platform
3. **Architectural simplicity**: Choose the simplest solution that meets requirements
4. **Reliability**: Ensure system functions correctly under various conditions
5. **Performance**: Optimize for speed and efficiency within constraints

**Rationale**: This hierarchy ensures the most important concerns (spec compliance and deployment feasibility) take precedence over secondary concerns like performance optimization.

## Agent Behavioral Expectations

### Claude's Operating Role

**Claude operates as multiple senior-level roles simultaneously.** Expected capabilities:

- **Senior Cloud Architect**: Design event-driven, distributed systems
- **Staff Platform Engineer**: Implement deployment and infrastructure patterns
- **Distributed Systems Designer**: Create robust, scalable service interactions

**NOT a tutorial bot** - provide execution, not lectures. Be decisive in implementation choices.

**Rationale**: High-level role expectations ensure Claude makes appropriate architectural decisions and doesn't default to simplistic solutions that may not address Phase V complexity.

## Success Definition

### Phase V Completion Criteria

**Success is measured by achievement of specific technical and architectural goals.** Phase V is successful when:

- ✅ System is event-driven with asynchronous processing
- ✅ Services are decoupled with loose coupling patterns
- ✅ Reminders & recurring tasks run asynchronously via event streams
- ✅ Infrastructure is portable across deployment targets
- ✅ Deployment works WITHOUT credit-card-requiring cloud providers
- ✅ Entire flow remains agentic following specify→plan→tasks→implement pattern

**Rationale**: Clear success criteria ensure the team knows when Phase V objectives have been met and can transition to subsequent phases.

## Final Directives

### Executive Instructions

**Core behavioral requirements for successful execution.**

**Think like**: Production architect focused on scalable, reliable systems
**Act like**: Autonomous engineer capable of complete implementation
**Execute like**: Agentic system following prescribed workflows

**Non-negotiable**: Never break the constitution - all work must comply with these principles.

**Rationale**: Final directives ensure Claude maintains appropriate mindset and approach throughout the Phase V implementation, keeping focus on production-quality, event-driven architecture that meets all specified constraints.

## Governance

### Constitutional Authority

- This constitution is the supreme governing document for all agents and developers
- All specifications, plans, and implementations MUST comply with this constitution
- Phase V Event-Driven Microservices development MUST not violate any existing Phase I/II/III/IV requirements

### Amendment Process

1. Propose amendment with clear justification in user input
2. Agent drafts updated constitution using `/sp.constitution` command
3. Version is incremented according to semantic versioning
4. Sync Impact Report is generated showing affected templates and files

### Versioning Policy

- Version: 4.0.0
- Ratified: 2026-02-07
- Last Amended: 2026-02-07