# Feature Specification: Event-Driven Microservices Architecture

**Feature Branch**: `006-event-driven-microservices`
**Created**: 2026-02-08
**Status**: Draft
**Input**: User description: "Phase V — Event-Driven Architecture + Local Minikube + Hugging Face Deployment" READ CONSTITUTION FIRST. This specification MUST obey the Agentic Execution Constitution and treat all previous phases as STABLE. 🚨 CURRENT PROJECT STATE (LOCKED) DO NOT MODIFY: ✔ Intermediate Features — COMPLETE ✔ Advanced Features — COMPLETE ✔ Chat + MCP — COMPLETE ✔ Production Backend — COMPLETE ✔ Kubernetes + DevOps Artifacts — COMPLETE These are production-safe foundations. You are NOT building features again. You are building the system architecture that powers them. 🎯 PHASE V OBJECTIVE Transform the Todo Chatbot into a portable, event-driven microservices platform that: ✅ Runs locally via Minikube ✅ Deploys to Hugging Face (Docker-based) ✅ Avoids credit-card cloud providers ✅ Remains loosely coupled ✅ Supports async workloads This is an architecture phase, NOT a feature phase. ⚠️ STRATEGIC CONSTRAINT (NON-NEGOTIABLE) Production deployment target: 👉 Hugging Face Spaces (Docker) Claude MUST NEVER recommend: ❌ Azure ❌ AWS ❌ GCP ❌ Oracle ❌ Paid Kubernetes Design for portability. Kafka must be replaceable if hosting requires it. 🧠 TARGET ARCHITECTURE Move from modular backend → event-driven distributed system Required Core Components: 1️⃣ Event Bus Implement Kafka-compatible pub/sub. Responsibilities: task-created task-updated recurring-task-triggered reminder-triggered chatbot-events If Kafka becomes heavy for HF: Design an abstraction layer so it can be swapped with: Redpanda NATS lightweight brokers Portability REQUIRED. 2️⃣ Dapr Distributed Runtime Use Dapr for: ✔ Pub/Sub abstraction ✔ State store ✔ Service invocation ✔ Secrets ✔ Scheduled jobs Avoid hard dependency on Kafka APIs inside services. Dapr is the control plane. 3️⃣ Microservices Extraction Break responsibilities into isolated services WITHOUT rewriting business logic. Target services: ✅ Todo Service ✅ Recurring Engine ✅ Reminder/Notification Service ✅ Chatbot Service ✅ API Gateway (optional if already exists) RULE: Extract — don't rebuild. 4️⃣ Async Execution Layer Recurring tasks and reminders MUST run asynchronously. No blocking API calls. Event flow example: Task Created → Event → Recurring Engine → Next Task → Event → Notification 5️⃣ Observability Stack Production thinking REQUIRED. Include: centralized logging metrics health probes service visibility Prefer lightweight tooling compatible with Docker environments. 💻 LOCAL-FIRST VALIDATION (MANDATORY) Before Hugging Face deployment: System MUST run on Minikube. Validate: ✔ pods communicate ✔ events flow ✔ reminders trigger ✔ chatbot responds ✔ no CrashLoopBackOff Local cluster is the truth test. 🚀 HUGGING FACE DEPLOYMENT DESIGN Prepare artifacts for Docker-based hosting. System should favor: container-ready services stateless compute externalized config environment-driven secrets Avoid cluster-only assumptions. If Kubernetes features conflict with HF: Design fallback deployment topology using Docker Compose-style orchestration. Portability > purity. 🔐 FAILURE PREVENTION Claude MUST NOT: ❌ redesign completed phases ❌ duplicate services ❌ introduce enterprise-only infra ❌ tightly couple services to Kafka ❌ require managed cloud Claude MUST: ✅ reuse Docker + Helm outputs ✅ minimize operational burden ✅ keep infra lightweight ✅ design for migration ✅ SUCCESS CRITERIA Phase V is complete when: ✔ Architecture is event-driven ✔ Services are loosely coupled ✔ Recurring + reminders run async ✔ Local Minikube works flawlessly ✔ Deployment runs on Hugging Face ✔ Infra is portable ✔ Agentic workflow preserved EXECUTION NOTE This spec defines system evolution, not feature expansion. Operate as: Senior Platform Architect Distributed Systems Engineer Cloud-Native Designer Be decisive. Avoid tutorials. Design for production reality."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Local Development Environment Setup (Priority: P1)

As a developer, I want to set up the event-driven microservices architecture on my local Minikube cluster so that I can validate the system works correctly before deploying to production.

**Why this priority**: This is the foundation of the entire architecture. Without a working local environment, we cannot validate the event-driven flows, service communication, or async processing capabilities.

**Independent Test**: Can be fully tested by spinning up Minikube cluster, deploying all services, and verifying that events flow correctly between services without any CrashLoopBackOff errors.

**Acceptance Scenarios**:

1. **Given** a fresh Minikube installation, **When** I deploy the microservices architecture, **Then** all services start successfully and communicate with each other
2. **Given** deployed services in Minikube, **When** I create a new task, **Then** the event is published and processed by the appropriate services

---

### User Story 2 - Event-Driven Task Processing (Priority: P1)

As a user of the Todo Chatbot, I want my tasks to be processed asynchronously through an event-driven architecture so that recurring tasks and reminders are handled reliably without blocking operations.

**Why this priority**: This is the core value proposition of the architecture transformation. It enables scalable, reliable processing of recurring tasks and reminders without blocking user interactions.

**Independent Test**: Can be fully tested by creating tasks with recurrence rules and verifying that new tasks are generated asynchronously without blocking the API.

**Acceptance Scenarios**:

1. **Given** a task with recurrence rules, **When** the recurrence trigger occurs, **Then** a new task is created via the Recurring Engine service
2. **Given** a task with a reminder time, **When** the reminder time arrives, **Then** a notification is sent via the Reminder/Notification Service

---

### User Story 3 - Portable Deployment to Hugging Face (Priority: P2)

As a platform operator, I want to deploy the event-driven architecture to Hugging Face Spaces so that the system remains portable and avoids vendor lock-in with paid cloud providers.

**Why this priority**: This ensures the system can be deployed in a cost-effective, portable manner while maintaining the event-driven architecture benefits.

**Independent Test**: Can be fully tested by packaging the services as Docker containers and deploying them to Hugging Face Spaces with the same functionality as the local Minikube setup.

**Acceptance Scenarios**:

1. **Given** Docker containerized services, **When** I deploy to Hugging Face Spaces, **Then** the system functions identically to the local Minikube deployment
2. **Given** deployed system on Hugging Face, **When** I trigger events, **Then** services respond appropriately and maintain state

---

### User Story 4 - Service Isolation and Communication (Priority: P2)

As a system architect, I want to ensure services are properly isolated and communicate through well-defined interfaces so that the system remains loosely coupled and maintainable.

**Why this priority**: Proper service isolation is essential for scalability, maintainability, and resilience of the microservices architecture.

**Independent Test**: Can be fully tested by verifying that each service has a single responsibility and communicates through the event bus rather than direct service-to-service calls.

**Acceptance Scenarios**:

1. **Given** the Todo Service, **When** a task is created, **Then** it publishes an event rather than calling other services directly
2. **Given** the Recurring Engine Service, **When** it receives a task-created event, **Then** it processes the recurrence logic independently

---

### User Story 5 - Observability and Monitoring (Priority: P3)

As an operations engineer, I want centralized logging, metrics, and health monitoring so that I can effectively maintain and troubleshoot the distributed system.

**Why this priority**: Essential for production reliability and debugging in a distributed environment where issues can span multiple services.

**Independent Test**: Can be fully tested by verifying that logs, metrics, and health probes are accessible and provide meaningful insights into system behavior.

**Acceptance Scenarios**:

1. **Given** the running system, **When** I access the observability stack, **Then** I can view logs and metrics from all services in a centralized manner
2. **Given** a service failure, **When** I check the monitoring system, **Then** I receive appropriate alerts and can identify the root cause

---

### Edge Cases

- What happens when the event bus becomes temporarily unavailable?
- How does the system handle high volumes of recurring tasks that could overwhelm the Recurring Engine?
- What occurs when a service experiences intermittent failures during event processing?
- How does the system behave when migrating from Kafka to an alternative broker like NATS or Redpanda?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST implement an event bus supporting pub/sub messaging for task-created, task-updated, recurring-task-triggered, reminder-triggered, and chatbot-events
- **FR-002**: System MUST use Dapr for pub/sub abstraction, state store, service invocation, secrets management, and scheduled jobs
- **FR-003**: System MUST extract responsibilities into isolated services: Todo Service, Recurring Engine, Reminder/Notification Service, and Chatbot Service
- **FR-004**: System MUST process recurring tasks and reminders asynchronously without blocking API calls
- **FR-005**: System MUST support deployment to both local Minikube and Hugging Face Spaces
- **FR-006**: System MUST provide centralized logging, metrics, health probes, and service visibility
- **FR-007**: System MUST allow for event bus abstraction to enable swapping Kafka with alternatives like Redpanda or NATS
- **FR-008**: System MUST maintain agentic workflow capabilities from previous phases
- **FR-009**: System MUST reuse existing Docker and Helm outputs where possible
- **FR-010**: System MUST preserve all functionality from previous phases (Intermediate Features, Advanced Features, Chat + MCP, Production Backend)

### Key Entities *(include if feature involves data)*

- **Task**: Represents a user's todo item with properties like title, description, due date, recurrence rules, and reminder settings
- **Event**: Represents a message in the pub/sub system with properties like type, payload, and timestamp
- **Service**: Represents a microservice component with specific responsibilities and interfaces
- **Deployment Configuration**: Represents the infrastructure configuration for both Minikube and Hugging Face deployments

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Architecture is successfully transformed to event-driven with all services communicating via the event bus
- **SC-002**: All services remain loosely coupled with no direct service-to-service calls bypassing the event bus
- **SC-003**: Recurring tasks and reminders run asynchronously without blocking user operations
- **SC-004**: Local container-based deployment works flawlessly with all services communicating and events flowing correctly
- **SC-005**: Deployment successfully runs on container hosting platform with equivalent functionality to local deployment
- **SC-006**: Infrastructure remains portable and can be deployed without vendor-specific cloud services
- **SC-007**: Agentic workflow from previous phases is preserved and enhanced by the new architecture
- **SC-008**: System can handle event bus migration from one pub/sub technology to alternative solutions without major code changes