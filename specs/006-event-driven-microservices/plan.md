# Implementation Plan: Event-Driven Microservices Architecture

**Branch**: `006-event-driven-microservices` | **Date**: 2026-02-08 | **Spec**: [link](spec.md)
**Input**: Feature specification from `/specs/006-event-driven-microservices/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Transform the existing Todo Chatbot platform into an event-driven microservices architecture using Kafka-compatible pub/sub messaging and Dapr for service orchestration. The system will support recurring tasks and reminders through asynchronous processing, with deployment targets for both local Minikube and Hugging Face Spaces. The architecture emphasizes loose coupling, portability, and scalability while preserving all existing functionality from previous phases.

## Technical Context

**Language/Version**: Python 3.11 (maintaining compatibility with existing backend)
**Primary Dependencies**: 
- Dapr (distributed runtime for pub/sub, state management, service invocation)
- Kafka/Redpanda/NATS (event streaming platform with abstraction layer)
- FastAPI (web framework for service APIs)
- Docker (containerization)
- Helm (Kubernetes package management)
**Storage**: PostgreSQL (existing backend database) with Dapr state stores for distributed state
**Testing**: pytest (unit/integration tests), contract tests for API validation
**Target Platform**: 
- Local: Minikube (Kubernetes cluster)
- Deployment: Hugging Face Spaces (Docker-based)
**Project Type**: Web application (backend services with existing frontend)
**Performance Goals**: 
- Handle 1000 concurrent users
- Process events with <500ms latency
- Support 10k tasks per day
**Constraints**: 
- <200ms p95 API response time
- <500MB memory footprint per service
- Stateless services for horizontal scaling
- Portable across deployment targets
**Scale/Scope**: 
- Support 10k active users
- Process 1M+ events per month
- Handle 50k tasks per day

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Compliance Verification:
- ✅ Agentic Development Stack: Following specify → plan → tasks → implement workflow
- ✅ Spec-First Law: Building from complete specification
- ✅ Skill Priority: Leveraging existing project skills and infrastructure
- ✅ Zero Manual Command Policy: Using automated deployment tools
- ✅ Production Thinking: Designing for scalability, loose coupling, observability
- ✅ Phase State Management: Building on stable Phase I-IV infrastructure
- ✅ Critical Deployment Constraint: Optimizing for Hugging Face deployment
- ✅ Event-Driven Architecture: Prioritizing event-driven over synchronous patterns
- ✅ Local-First Strategy: Validating locally before deployment
- ✅ Failure Prevention: Avoiding redesign of completed phases, tight coupling, enterprise cloud

## Project Structure

### Documentation (this feature)

```text
specs/006-event-driven-microservices/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
│   └── openapi.yaml
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
# Web application with microservices architecture
backend/
├── todo-service/           # Handle task CRUD operations
│   ├── src/
│   │   ├── models/
│   │   ├── services/
│   │   └── api/
│   └── tests/
├── recurring-engine/       # Process recurring task logic
│   ├── src/
│   │   ├── models/
│   │   ├── services/
│   │   └── api/
│   └── tests/
├── reminder-service/       # Handle reminder triggers and notifications
│   ├── src/
│   │   ├── models/
│   │   ├── services/
│   │   └── api/
│   └── tests/
├── chatbot-service/        # Handle chatbot interactions
│   ├── src/
│   │   ├── models/
│   │   ├── services/
│   │   └── api/
│   └── tests/
├── shared/                 # Shared utilities and models
│   └── event-bus/
└── tests/                  # Cross-service integration tests

# Infrastructure
Dockerfiles/
├── todo-service.Dockerfile
├── recurring-engine.Dockerfile
├── reminder-service.Dockerfile
├── chatbot-service.Dockerfile
└── kafka-dapr.Dockerfile

helm-charts/
└── todo-platform/
    ├── Chart.yaml
    ├── values.yaml
    └── templates/
        ├── todo-service.yaml
        ├── recurring-engine.yaml
        ├── reminder-service.yaml
        ├── chatbot-service.yaml
        ├── kafka.yaml
        ├── dapr-components.yaml
        └── ingress.yaml

# Existing artifacts reused
├── docker-compose.yml      # Adapted for local development
└── custom-values.yaml      # Extended for new services
```

**Structure Decision**: Web application architecture with separate microservices following the event-driven model specified in the requirements. Each service has its own codebase with shared utilities and models. Infrastructure is managed through Dockerfiles and Helm charts, building upon existing Phase IV artifacts.

## 1️⃣ Target System Architecture

### Service Boundaries
- **Todo Service**: Handles all task CRUD operations, validates inputs, and publishes events
- **Recurring Engine**: Processes recurrence patterns and generates new tasks based on schedules
- **Reminder/Notification Service**: Manages reminder scheduling and notification delivery
- **Chatbot Service**: Processes natural language queries and commands, orchestrates actions

### Event Flow Design
- **Task Creation Flow**: Client → API Gateway → Todo Service → "task-created" event → Reminder Service & Recurring Engine
- **Task Update Flow**: Client → API Gateway → Todo Service → "task-updated" event → Relevant Services
- **Recurring Task Flow**: Scheduled Trigger → Recurring Engine → "recurring-task-triggered" event → New Task Creation
- **Reminder Flow**: Scheduled Trigger → Reminder Service → "reminder-triggered" event → Notification Delivery

### Communication Patterns
- **Event-Driven**: Services communicate primarily through pub/sub events
- **Dapr Service Invocation**: For synchronous communication when necessary
- **API Gateway**: Single entry point for client requests (optional, may use direct service access)

### Dapr Control-Plane Role
- **Pub/Sub Component**: Abstracts the underlying event bus (Kafka/Redpanda/NATS)
- **State Store**: Manages distributed state for services
- **Service Invocation**: Enables reliable inter-service communication
- **Secrets Management**: Securely manages configuration and credentials
- **Bindings**: Connects services to external systems

### Broker Abstraction Strategy
- **Interface Layer**: Define abstract interfaces for event publishing/subscribing
- **Implementation Adapters**: Create adapters for different brokers (Kafka, Redpanda, NATS)
- **Configuration-Based Switching**: Allow broker selection via configuration
- **Migration Path**: Design with easy switching in mind from the beginning

## 2️⃣ Microservice Extraction Strategy

### SAFE Sequence: Monolith → Modular → Extracted Services → Event Integration

#### Phase A: Service Identification
- Analyze existing backend code to identify service boundaries
- Map existing functionality to new service responsibilities
- Identify shared components that become common libraries

#### Phase B: Safe Extraction
- Create new service repositories while maintaining existing functionality
- Implement API compatibility layers to avoid breaking changes
- Gradually migrate functionality with feature flags

#### Phase C: Event Integration
- Replace direct service calls with event-based communication
- Implement event publishers and subscribers
- Establish event schemas and contracts

### Service-Specific Details

#### Todo Service
- **Responsibility**: Handle task CRUD operations, validation, and persistence
- **Events Published**: task-created, task-updated, task-deleted
- **Events Consumed**: None (primary event source)
- **Deployment Model**: Kubernetes deployment with Dapr sidecar

#### Recurring Engine
- **Responsibility**: Process recurrence patterns and generate new tasks
- **Events Published**: recurring-task-triggered
- **Events Consumed**: task-created (to identify recurring tasks), recurring-task-triggered (for chained recurrences)
- **Deployment Model**: Kubernetes deployment with Dapr sidecar and scheduled job capability

#### Reminder/Notification Service
- **Responsibility**: Manage reminder scheduling and notification delivery
- **Events Published**: reminder-triggered
- **Events Consumed**: task-created (to schedule reminders), task-updated (to reschedule if needed)
- **Deployment Model**: Kubernetes deployment with Dapr sidecar and scheduled job capability

#### Chatbot Service
- **Responsibility**: Process natural language queries and commands
- **Events Published**: chatbot-event
- **Events Consumed**: task-created, task-updated (to maintain context), reminder-triggered (to notify users)
- **Deployment Model**: Kubernetes deployment with Dapr sidecar

## 3️⃣ Event Bus Design

### Topic Structure
- `todo.task.created` - New tasks created
- `todo.task.updated` - Task updates
- `todo.task.deleted` - Task deletions
- `todo.recurring.triggered` - Recurring task triggers
- `todo.reminder.triggered` - Reminder triggers
- `todo.chatbot.event` - Chatbot interaction events

### Schema Approach
- **JSON Schema Validation**: Define schemas for each event type
- **Versioning**: Include version in event metadata for backward compatibility
- **Standard Headers**: Include correlation IDs, timestamps, source service
- **Payload Consistency**: Maintain consistent structure across similar events

### Retry Strategy
- **Exponential Backoff**: Implement exponential backoff for failed event processing
- **Dead Letter Queue**: Route permanently failed events to DLQ for inspection
- **Circuit Breaker**: Prevent cascading failures when downstream services are unavailable
- **Duplicate Detection**: Track processed events to prevent duplicate processing

### Idempotency
- **Event Deduplication**: Use event IDs to detect and skip duplicate events
- **State-Based Processing**: Design event handlers to be safe when applied multiple times
- **Idempotent Operations**: Ensure that processing the same event twice has the same effect as once

### Failure Handling
- **Graceful Degradation**: Services continue operating when event bus is unavailable
- **Event Persistence**: Store events durably to prevent loss during failures
- **Monitoring**: Track event processing rates, failure rates, and lag
- **Alerting**: Notify operators when failure thresholds are exceeded

## 4️⃣ Async Execution Model

### Recurring Tasks Trigger
- **Scheduled Jobs**: Use Dapr's built-in job scheduling or cron bindings
- **Event-Based Triggers**: Respond to "recurring-task-triggered" events
- **Time-Based Processing**: Calculate next occurrence based on recurrence pattern
- **Zero Blocking**: All processing happens asynchronously without blocking API calls

### Reminders Execution
- **Timer-Based**: Use Dapr timers for precise reminder scheduling
- **Event-Driven**: Respond to "task-created" and "task-updated" events to schedule reminders
- **Notification Delivery**: Send notifications via email, push, or other channels
- **Zero Blocking**: All reminder processing happens asynchronously

### Chatbot Reactions to Events
- **Event Subscription**: Subscribe to relevant events to maintain context
- **Context Updates**: Update conversation context based on task changes
- **Proactive Notifications**: Inform users of task changes or upcoming reminders
- **Zero Blocking**: Event reactions happen asynchronously without affecting user interactions

## 5️⃣ Infrastructure Blueprint

### Local: Minikube
- **Container Strategy**: Docker containers for all services
- **Orchestration**: Kubernetes manifests via Helm charts
- **Service Mesh**: Dapr for service-to-service communication
- **Event Bus**: Kafka/Redpanda in local cluster
- **Config Management**: Kubernetes ConfigMaps and Secrets, Dapr components
- **Networking**: Kubernetes Services and Ingress for service exposure

### Deployment: Hugging Face Docker
- **Container Strategy**: Optimized Docker images for constrained environments
- **State Management**: Externalized state to prevent data loss during container restarts
- **Config Management**: Environment variables for configuration
- **Scaling**: Stateless services designed for horizontal scaling
- **Resource Limits**: Carefully tuned CPU and memory limits for platform constraints

### Common Infrastructure Components
- **Event Bus**: Kafka-compatible with abstraction layer for portability
- **Service Discovery**: Kubernetes DNS with Dapr service invocation
- **Health Checks**: Standard HTTP health endpoints for each service
- **Logging**: Structured logging aggregated to central system
- **Monitoring**: Prometheus-compatible metrics collection

## 6️⃣ Observability Layer

### Logging
- **Structured Logging**: JSON-formatted logs with consistent fields
- **Correlation IDs**: Track requests across service boundaries
- **Centralized Aggregation**: Collect logs from all services in one place
- **Log Levels**: Support different log levels for different environments

### Metrics
- **Application Metrics**: Request rates, error rates, processing times
- **Infrastructure Metrics**: Resource utilization, queue depths
- **Business Metrics**: Task creation rates, reminder success rates
- **Prometheus Compatible**: Export metrics in Prometheus format

### Tracing
- **Distributed Tracing**: Trace requests across service boundaries
- **Event Correlation**: Track events from creation to processing
- **Performance Analysis**: Identify bottlenecks in event processing
- **OpenTelemetry**: Use standard tracing protocols

### Health Probes
- **Liveness Probes**: Verify services are running
- **Readiness Probes**: Verify services are ready to accept traffic
- **Custom Health Checks**: Application-specific health indicators
- **Event Bus Connectivity**: Verify event bus connectivity

## 7️⃣ Execution Roadmap (CRITICAL)

### Phase A — Foundations
**Goal**: Set up the infrastructure and foundational components
**Key Actions**:
- Deploy Dapr to the cluster
- Set up event bus (Kafka/Redpanda) in the cluster
- Create service accounts and security configurations
- Set up monitoring and logging infrastructure
**Validation Check**: Dapr is running, event bus is accessible, services can connect to event bus

### Phase B — Broker + Dapr
**Goal**: Configure Dapr components and event bus connectivity
**Key Actions**:
- Define Dapr pub/sub component for event bus
- Set up Dapr state store components
- Configure Dapr service invocation
- Implement event publishing/subscribing patterns
**Validation Check**: Services can publish and subscribe to events, Dapr components are properly configured

### Phase C — Service Extraction
**Goal**: Extract services from existing monolith
**Key Actions**:
- Create new service repositories
- Migrate task management logic to Todo Service
- Migrate recurring logic to Recurring Engine
- Migrate reminder logic to Reminder Service
- Migrate chatbot logic to Chatbot Service
**Validation Check**: All services are running and handling their respective responsibilities

### Phase D — Async Engines
**Goal**: Implement asynchronous processing for recurring tasks and reminders
**Key Actions**:
- Implement recurring task scheduler in Recurring Engine
- Implement reminder scheduler in Reminder Service
- Set up event processing for both engines
- Test event-driven task creation and reminder delivery
**Validation Check**: Recurring tasks are generated automatically, reminders are delivered on time

### Phase E — Minikube Validation
**Goal**: Validate the complete system on local Minikube
**Key Actions**:
- Deploy complete system to Minikube
- Test end-to-end workflows
- Verify event flows work correctly
- Validate service communication
- Ensure no CrashLoopBackOff errors
**Validation Check**: All services communicate, events flow correctly, system operates as expected

### Phase F — Hugging Face Deployment
**Goal**: Package and deploy to Hugging Face Spaces
**Key Actions**:
- Optimize Docker images for Hugging Face constraints
- Create deployment configuration for Hugging Face
- Test deployment process
- Validate functionality in Hugging Face environment
**Validation Check**: System runs successfully on Hugging Face with equivalent functionality to local deployment

## 8️⃣ Risk Controls

### Top Architectural Risks

#### Risk 1: Broker Weight
**Issue**: Kafka may be too heavy for Hugging Face deployment
**Mitigation Strategy**:
- Design abstraction layer to allow easy migration
- Test with lighter alternatives like Redpanda during development
- Implement graceful degradation when event bus is unavailable
- Provide fallback mechanisms for critical operations

#### Risk 2: Service Fragmentation
**Issue**: Too many services causing complexity and communication overhead
**Mitigation Strategy**:
- Maintain clear service boundaries based on business domains
- Use event-driven communication to reduce coupling
- Implement proper monitoring to detect performance issues
- Consolidate services if fragmentation becomes problematic

#### Risk 3: Event Processing Failures
**Issue**: Events not processed correctly leading to inconsistent state
**Mitigation Strategy**:
- Implement idempotent event processors
- Use dead letter queues for failed events
- Monitor event processing rates and lag
- Implement circuit breakers to prevent cascading failures

#### Risk 4: Local Cluster Limits
**Issue**: Minikube resources insufficient for testing full architecture
**Mitigation Strategy**:
- Optimize resource usage in development configurations
- Use minikube profiles with increased resources
- Implement scaled-down versions for local testing
- Provide clear documentation on recommended hardware requirements

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| Multiple services | Event-driven architecture requires separation of concerns | Single service would create tight coupling and block async processing | 
| Dapr dependency | Required for pub/sub abstraction and service mesh capabilities | Custom implementation would increase complexity and maintenance |
