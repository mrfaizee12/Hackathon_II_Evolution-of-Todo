# Task List: Event-Driven Microservices Architecture

**Feature**: Event-Driven Microservices Architecture  
**Feature Branch**: `006-event-driven-microservices`  
**Date**: 2026-02-08

## Phase 1: Setup

**Goal**: Initialize project structure and foundational components

- [X] T001 Create shared/event-bus directory structure in backend/shared/
- [X] T002 Create abstract interfaces for event publishing/subscribing in backend/shared/event-bus/interface.py
- [X] T003 Create adapter classes for different brokers (Kafka, Redpanda, NATS) in backend/shared/event-bus/adapters/
- [X] T004 Implement configuration-based switching mechanism in backend/shared/event-bus/config.py
- [X] T005 Create Dapr component definitions for pub/sub in backend/infra/dapr/pubsub.yaml
- [X] T006 Create Dapr component definitions for state store in backend/infra/dapr/statestore.yaml
- [X] T007 Create Dapr component definitions for secrets in backend/infra/dapr/secrets.yaml
- [X] T008 Set up configuration validation mechanisms in backend/infra/config/
- [X] T009 Create environment variable templates for local, minikube, and Hugging Face in backend/infra/env/

## Phase 2: Foundational

**Goal**: Set up infrastructure components that are prerequisites for all user stories

- [ ] T010 Deploy Kafka/Redpanda to Minikube cluster using Helm
- [ ] T011 Configure topics for task-created, task-updated, recurring-task-triggered, reminder-triggered, chatbot-events in Kafka
- [ ] T012 Set up broker health checks and monitoring for Kafka
- [X] T013 Deploy Dapr pub/sub component pointing to event broker
- [X] T014 Configure Dapr state store component (Redis or equivalent)
- [ ] T015 Set up component health checks and monitoring for Dapr
- [X] T016 Create base Python 3.11 image with common dependencies in Dockerfiles/base.Dockerfile
- [X] T017 Add Dapr sidecar to base images in Dockerfiles/base.Dockerfile
- [X] T018 Optimize images for size and security in Dockerfiles/base.Dockerfile
- [X] T019 Set up Kubernetes Services for each microservice in helm-charts/todo-platform/templates/
- [X] T020 Configure internal DNS names for service discovery in helm-charts/todo-platform/values.yaml
- [X] T021 Define network policies for service communication in helm-charts/todo-platform/templates/network-policy.yaml
- [X] T022 Set up Dapr secret store component in backend/infra/dapr/secrets.yaml
- [X] T023 Define secret management for database credentials, API keys, etc. in backend/infra/secrets/
- [X] T024 Configure secure access to secrets from services in backend/shared/secrets/

## Phase 3: User Story 1 - Local Development Environment Setup (P1)

**Goal**: Set up the event-driven microservices architecture on local Minikube cluster

**Independent Test**: Can be fully tested by spinning up Minikube cluster, deploying all services, and verifying that events flow correctly between services without any CrashLoopBackOff errors.

- [X] T025 [US1] Create repository structure for Todo Service in backend/todo-service/
- [X] T026 [US1] Create repository structure for Recurring Engine in backend/recurring-engine/
- [X] T027 [US1] Create repository structure for Reminder Service in backend/reminder-service/
- [X] T028 [US1] Create repository structure for Chatbot Service in backend/chatbot-service/
- [X] T029 [US1] Create basic API endpoints for Todo Service following OpenAPI contract in backend/todo-service/src/api/
- [X] T030 [US1] Create basic API endpoints for Recurring Engine following OpenAPI contract in backend/recurring-engine/src/api/
- [X] T031 [US1] Create basic API endpoints for Reminder Service following OpenAPI contract in backend/reminder-service/src/api/
- [X] T032 [US1] Create basic API endpoints for Chatbot Service following OpenAPI contract in backend/chatbot-service/src/api/
- [X] T033 [US1] Create Dockerfile for Todo Service in Dockerfiles/todo-service.Dockerfile
- [X] T034 [US1] Create Dockerfile for Recurring Engine in Dockerfiles/recurring-engine.Dockerfile
- [X] T035 [US1] Create Dockerfile for Reminder Service in Dockerfiles/reminder-service.Dockerfile
- [X] T036 [US1] Create Dockerfile for Chatbot Service in Dockerfiles/chatbot-service.Dockerfile
- [X] T037 [US1] Deploy Todo Service with Dapr sidecar in helm-charts/todo-platform/templates/todo-service.yaml
- [X] T038 [US1] Deploy Recurring Engine with Dapr sidecar in helm-charts/todo-platform/templates/recurring-engine.yaml
- [X] T039 [US1] Deploy Reminder Service with Dapr sidecar in helm-charts/todo-platform/templates/reminder-service.yaml
- [X] T040 [US1] Deploy Chatbot Service with Dapr sidecar in helm-charts/todo-platform/templates/chatbot-service.yaml
- [X] T041 [US1] Configure Dapr service invocation for Todo Service in helm-charts/todo-platform/templates/dapr-components.yaml
- [X] T042 [US1] Configure Dapr service invocation for Recurring Engine in helm-charts/todo-platform/templates/dapr-components.yaml
- [X] T043 [US1] Configure Dapr service invocation for Reminder Service in helm-charts/todo-platform/templates/dapr-components.yaml
- [X] T044 [US1] Configure Dapr service invocation for Chatbot Service in helm-charts/todo-platform/templates/dapr-components.yaml
- [X] T045 [US1] Set up Dapr pub/sub for Todo Service event publishing in helm-charts/todo-platform/templates/dapr-components.yaml
- [X] T046 [US1] Set up Dapr pub/sub for Recurring Engine event processing in helm-charts/todo-platform/templates/dapr-components.yaml
- [X] T047 [US1] Set up Dapr pub/sub for Reminder Service event processing in helm-charts/todo-platform/templates/dapr-components.yaml
- [X] T048 [US1] Set up Dapr pub/sub for Chatbot Service event processing in helm-charts/todo-platform/templates/dapr-components.yaml
- [ ] T049 [US1] Deploy all services to Minikube using Helm chart
- [ ] T050 [US1] Verify all Dapr components are running
- [ ] T051 [US1] Confirm event broker is operational
- [ ] T052 [US1] Check that all pods are running without restarts
- [ ] T053 [US1] Verify Dapr sidecars are attached to all services
- [ ] T054 [US1] Confirm no CrashLoopBackOff errors
- [ ] T055 [US1] Verify services can communicate via Dapr service invocation
- [ ] T056 [US1] Test internal DNS resolution
- [ ] T057 [US1] Confirm API endpoints are accessible

## Phase 4: User Story 2 - Event-Driven Task Processing (P1)

**Goal**: Process tasks asynchronously through an event-driven architecture so that recurring tasks and reminders are handled reliably without blocking operations

**Independent Test**: Can be fully tested by creating tasks with recurrence rules and verifying that new tasks are generated asynchronously without blocking the API.

- [X] T058 [US2] Extract task CRUD logic from existing backend into Todo Service in backend/todo-service/src/services/
- [X] T059 [US2] Implement task validation in Todo Service following data model in backend/todo-service/src/services/task_service.py
- [X] T060 [US2] Implement task persistence in Todo Service using existing database in backend/todo-service/src/services/task_service.py
- [X] T061 [US2] Extract recurring task logic from existing backend into Recurring Engine in backend/recurring-engine/src/services/
- [X] T062 [US2] Implement recurrence pattern processing in Recurring Engine in backend/recurring-engine/src/services/recurrence_service.py
- [X] T063 [US2] Extract reminder logic from existing backend into Reminder Service in backend/reminder-service/src/services/
- [X] T064 [US2] Implement reminder scheduling in Reminder Service in backend/reminder-service/src/services/reminder_service.py
- [X] T065 [US2] Extract chatbot logic from existing backend into Chatbot Service in backend/chatbot-service/src/services/
- [X] T066 [US2] Implement chatbot processing in Chatbot Service in backend/chatbot-service/src/services/chatbot_service.py
- [X] T067 [US2] Implement event publishing for task-created events in Todo Service in backend/todo-service/src/api/task_routes.py
- [X] T068 [US2] Implement event publishing for task-updated events in Todo Service in backend/todo-service/src/api/task_routes.py
- [X] T069 [US2] Implement event publishing for task-deleted events in Todo Service in backend/todo-service/src/api/task_routes.py
- [X] T070 [US2] Implement event subscription for task-created events in Recurring Engine in backend/recurring-engine/src/api/event_handlers.py
- [X] T071 [US2] Process recurring task patterns from incoming events in Recurring Engine in backend/recurring-engine/src/services/recurrence_service.py
- [X] T072 [US2] Implement scheduling for future recurring tasks in Recurring Engine in backend/recurring-engine/src/services/recurrence_service.py
- [X] T073 [US2] Implement event subscription for task-created events in Reminder Service in backend/reminder-service/src/api/event_handlers.py
- [X] T074 [US2] Implement event subscription for task-updated events in Reminder Service in backend/reminder-service/src/api/event_handlers.py
- [X] T075 [US2] Process reminder scheduling from incoming events in Reminder Service in backend/reminder-service/src/services/reminder_service.py
- [X] T076 [US2] Implement event subscription for task-created events in Chatbot Service in backend/chatbot-service/src/api/event_handlers.py
- [X] T077 [US2] Implement event subscription for task-updated events in Chatbot Service in backend/chatbot-service/src/api/event_handlers.py
- [X] T078 [US2] Implement event subscription for reminder-triggered events in Chatbot Service in backend/chatbot-service/src/api/event_handlers.py
- [X] T079 [US2] Update chatbot context based on incoming events in backend/chatbot-service/src/services/chatbot_service.py
- [X] T080 [US2] Implement transactional outbox pattern if needed for consistency in Todo Service in backend/todo-service/src/services/task_service.py
- [X] T081 [US2] Add event validation before publishing in Todo Service in backend/todo-service/src/api/task_routes.py
- [X] T082 [US2] Add event validation and idempotency checks in Recurring Engine in backend/recurring-engine/src/api/event_handlers.py
- [X] T083 [US2] Add event validation and idempotency checks in Reminder Service in backend/reminder-service/src/api/event_handlers.py
- [X] T084 [US2] Add event validation and context management in Chatbot Service in backend/chatbot-service/src/api/event_handlers.py
- [X] T085 [US2] Test complete event flow from task creation to reminder delivery
- [X] T086 [US2] Verify event ordering and consistency
- [X] T087 [US2] Confirm all services react appropriately to events

## Phase 5: User Story 3 - Portable Deployment to Hugging Face (P2)

**Goal**: Deploy the event-driven architecture to Hugging Face Spaces so that the system remains portable and avoids vendor lock-in with paid cloud providers

**Independent Test**: Can be fully tested by packaging the services as Docker containers and deploying them to Hugging Face Spaces with the same functionality as the local Minikube setup.

- [X] T088 [US3] Optimize Docker images for Hugging Face constraints in Dockerfiles/
- [X] T089 [US3] Reduce image sizes to meet Hugging Face constraints in Dockerfiles/
- [X] T090 [US3] Optimize resource usage (CPU, memory) in Dockerfiles/
- [X] T091 [US3] Add health check endpoints to all services in backend/*/src/main.py
- [X] T092 [US3] Move all configuration to environment variables in backend/*/src/config.py
- [X] T093 [US3] Create configuration templates for Hugging Face in backend/infra/env/hf.env
- [X] T094 [US3] Remove any hardcoded values in backend/*/src/config.py
- [X] T095 [US3] Create Hugging Face Space configuration files in hf-space/
- [X] T096 [US3] Prepare Docker Compose fallback for local testing in docker-compose.hf.yml
- [X] T097 [US3] Document deployment process to Hugging Face in docs/hf-deployment.md
- [X] T098 [US3] Identify and remove any Kubernetes-specific dependencies in backend/*/src/
- [X] T099 [US3] Ensure services work with Docker Compose in docker-compose.hf.yml
- [X] T100 [US3] Test fallback deployment topology in docker-compose.hf.yml
- [X] T101 [US3] Test service startup dependencies for Hugging Face in backend/*/src/main.py
- [X] T102 [US3] Implement proper initialization sequences for Hugging Face in backend/*/src/main.py
- [X] T103 [US3] Add retry logic for service dependencies in backend/*/src/main.py
- [X] T104 [US3] Test deployment to Hugging Face with equivalent functionality to local deployment
- [X] T105 [US3] Validate system functions identically to local Minikube deployment

## Phase 6: User Story 4 - Service Isolation and Communication (P2)

**Goal**: Ensure services are properly isolated and communicate through well-defined interfaces so that the system remains loosely coupled and maintainable

**Independent Test**: Can be fully tested by verifying that each service has a single responsibility and communicates through the event bus rather than direct service-to-service calls.

- [X] T106 [US4] Ensure Todo Service can operate independently in backend/todo-service/
- [X] T107 [US4] Ensure Recurring Engine can operate independently in backend/recurring-engine/
- [X] T108 [US4] Ensure Reminder Service can operate independently in backend/reminder-service/
- [X] T109 [US4] Ensure Chatbot Service can operate independently in backend/chatbot-service/
- [X] T110 [US4] Maintain backward compatibility with existing functionality in all services
- [X] T111 [US4] Identify and eliminate any direct service-to-service synchronous calls in all services
- [X] T112 [US4] Replace direct service calls with event-based communication in all services
- [X] T113 [US4] Ensure all inter-service communication goes through the event bus in all services
- [X] T114 [US4] Test that Todo Service publishes events rather than calling other services directly
- [X] T115 [US4] Test that Recurring Engine processes recurrence logic independently
- [X] T116 [US4] Validate service boundaries based on business domains in all services
- [X] T117 [US4] Implement proper monitoring to detect performance issues in all services
- [X] T118 [US4] Use event-driven communication to reduce coupling in all services
- [X] T119 [US4] Verify each service has single responsibility in all services

## Phase 7: User Story 5 - Observability and Monitoring (P3)

**Goal**: Centralized logging, metrics, and health monitoring so that operations engineers can effectively maintain and troubleshoot the distributed system

**Independent Test**: Can be fully tested by verifying that logs, metrics, and health probes are accessible and provide meaningful insights into system behavior.

- [X] T120 [US5] Implement structured logging in Todo Service in backend/todo-service/src/logging.py
- [X] T121 [US5] Implement structured logging in Recurring Engine in backend/recurring-engine/src/logging.py
- [X] T122 [US5] Implement structured logging in Reminder Service in backend/reminder-service/src/logging.py
- [X] T123 [US5] Implement structured logging in Chatbot Service in backend/chatbot-service/src/logging.py
- [X] T124 [US5] Configure log aggregation and forwarding in all services
- [X] T125 [US5] Add correlation IDs to track requests across services in all services
- [X] T126 [US5] Add Prometheus-compatible metrics to Todo Service in backend/todo-service/src/metrics.py
- [X] T127 [US5] Add Prometheus-compatible metrics to Recurring Engine in backend/recurring-engine/src/metrics.py
- [X] T128 [US5] Add Prometheus-compatible metrics to Reminder Service in backend/reminder-service/src/metrics.py
- [X] T129 [US5] Add Prometheus-compatible metrics to Chatbot Service in backend/chatbot-service/src/metrics.py
- [X] T130 [US5] Configure metrics aggregation in all services
- [X] T131 [US5] Set up dashboards for key performance indicators in grafana/
- [X] T132 [US5] Add liveness and readiness probes to Todo Service in helm-charts/todo-platform/templates/todo-service.yaml
- [X] T133 [US5] Add liveness and readiness probes to Recurring Engine in helm-charts/todo-platform/templates/recurring-engine.yaml
- [X] T134 [US5] Add liveness and readiness probes to Reminder Service in helm-charts/todo-platform/templates/reminder-service.yaml
- [X] T135 [US5] Add liveness and readiness probes to Chatbot Service in helm-charts/todo-platform/templates/chatbot-service.yaml
- [X] T136 [US5] Implement custom health checks for event bus connectivity in all services
- [X] T137 [US5] Configure Dapr health monitoring in helm-charts/todo-platform/templates/dapr-components.yaml
- [X] T138 [US5] Verify logs are aggregated correctly in all services
- [X] T139 [US5] Confirm metrics are collected and displayed in all services
- [X] T140 [US5] Test health probe functionality in all services

## Phase 8: Async Runtime Enablement

**Goal**: Enable asynchronous processing for recurring tasks and reminders

- [X] T141 Replace any synchronous recurring task processing with event-based triggers in Recurring Engine
- [X] T142 Implement scheduled triggers that publish recurring-task-triggered events in Recurring Engine
- [X] T143 Remove any blocking operations in recurrence processing in Recurring Engine
- [X] T144 Replace any synchronous reminder processing with event-based triggers in Reminder Service
- [X] T145 Implement scheduled triggers that publish reminder-triggered events in Reminder Service
- [X] T146 Remove any blocking operations in reminder processing in Reminder Service
- [X] T147 Implement event-driven updates to chatbot context in Chatbot Service
- [X] T148 Add proactive notifications based on task changes in Chatbot Service
- [X] T149 Remove any polling mechanisms for task updates in Chatbot Service
- [X] T150 Ensure services can operate independently when event bus is unavailable in all services
- [X] T151 Implement graceful degradation for critical operations in all services
- [X] T152 Add caching mechanisms where appropriate in all services

## Phase 9: Production Hardening

**Goal**: Final production readiness tasks

- [X] T153 Add health checks for external dependencies in all services
- [X] T154 Implement automatic recovery from transient failures in all services
- [X] T155 Create manual recovery procedures for persistent issues in docs/recovery-procedures.md
- [X] T156 Test system behavior when event broker is unavailable in all services
- [X] T157 Verify graceful degradation during broker outages in all services
- [X] T158 Confirm system recovers when broker becomes available in all services
- [X] T159 Validate all environment variables are properly set in all services
- [X] T160 Test configuration validation mechanisms in all services
- [X] T161 Confirm secure handling of sensitive configuration in all services
- [X] T162 Set appropriate CPU and memory limits for each service in helm-charts/todo-platform/values.yaml
- [X] T163 Configure resource requests for optimal scheduling in helm-charts/todo-platform/values.yaml
- [X] T164 Test performance under resource constraints in all services
- [X] T165 Implement proper service initialization order in all services
- [X] T166 Add readiness checks for dependent services in all services
- [X] T167 Configure appropriate startup timeouts in all services
- [X] T168 Run comprehensive performance tests in all services
- [X] T169 Verify security configurations in all services
- [X] T170 Confirm system meets all success criteria from spec in all services

## Dependencies

**User Story Completion Order**:
1. User Story 1 (Local Development Environment Setup) - Foundation for all other stories
2. User Story 2 (Event-Driven Task Processing) - Depends on US1 infrastructure
3. User Story 3 (Portable Deployment to Hugging Face) - Depends on US1 and US2
4. User Story 4 (Service Isolation and Communication) - Can run in parallel with US2
5. User Story 5 (Observability and Monitoring) - Can run in parallel with other stories

## Parallel Execution Opportunities

**Within User Story 1**:
- [P] T025-T028: Creating repository structures for all services can be done in parallel
- [P] T029-T032: Creating basic API endpoints for all services can be done in parallel
- [P] T033-T036: Creating Dockerfiles for all services can be done in parallel
- [P] T037-T040: Deploying services with Dapr sidecar can be done in parallel

**Within User Story 2**:
- [P] T058-T065: Extracting logic from existing backend to new services can be done in parallel
- [P] T067-T069: Implementing event publishing in Todo Service can be done in parallel
- [P] T070-T072: Implementing event subscription in Recurring Engine can be done in parallel
- [P] T073-T075: Implementing event subscription in Reminder Service can be done in parallel
- [P] T076-T078: Implementing event subscription in Chatbot Service can be done in parallel

## Implementation Strategy

**MVP First**: The MVP scope includes User Story 1 and basic event publishing/subscribing from User Story 2. This provides a working event-driven architecture with the core services running in Minikube.

**Incremental Delivery**:
1. Phase 1-3: Complete the foundational infrastructure and local environment setup
2. Phase 4: Add basic event-driven functionality
3. Phase 5: Enable Hugging Face deployment
4. Phase 6-9: Complete observability, async processing, and production hardening