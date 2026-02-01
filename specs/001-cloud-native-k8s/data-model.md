# Data Model: Phase IV Cloud-Native Deployment

**Feature**: Phase IV Cloud-Native Deployment
**Date**: 2026-01-29
**Status**: Completed

## Key Entities

### Kubernetes Resources

**Deployment**
- **Description**: Defines desired state for application pods
- **Fields**: replicas, selector, template
- **Relationships**: Connects to Service and ConfigMap/Secret resources
- **Validation**: Replica count must match requirements (2 for backend, 1 for frontend)

**Service**
- **Description**: Provides network access to pods
- **Fields**: type, ports, selector
- **Relationships**: Connected to Deployment resources
- **Validation**: Service type must support Minikube exposure

**Secret**
- **Description**: Stores sensitive information securely
- **Fields**: data, type
- **Relationships**: Referenced by Deployments for API keys and credentials
- **Validation**: Must contain required keys for application operation

**PersistentVolumeClaim**
- **Description**: Requests storage for stateful components
- **Fields**: resources, accessModes
- **Relationships**: Used by PostgreSQL deployment
- **Validation**: Must provide sufficient storage for database

### Application Components

**Backend Service**
- **Description**: FastAPI application container
- **Fields**: image, replicas, environment variables
- **Relationships**: Depends on PostgreSQL, connects to frontend
- **State Transitions**: Pending → Running → Terminated

**Frontend Service**
- **Description**: Next.js application container
- **Fields**: image, replicas, environment variables
- **Relationships**: Connects to backend service
- **State Transitions**: Pending → Running → Terminated

**Database Service**
- **Description**: PostgreSQL database container
- **Fields**: image, storage, environment variables
- **Relationships**: Used by backend service
- **State Transitions**: Pending → Running → Terminated

### Container Images

**Backend Image**
- **Description**: Container image for FastAPI application
- **Fields**: name, tag, registry
- **Relationships**: Used by Backend Service deployment
- **Validation**: Must match faizananjum/backend:v1 naming convention

**Frontend Image**
- **Description**: Container image for Next.js application
- **Fields**: name, tag, registry
- **Relationships**: Used by Frontend Service deployment
- **Validation**: Must match faizananjum/frontend:v1 naming convention

## Relationships

- Backend Service connects to Database Service for data persistence
- Frontend Service communicates with Backend Service for API calls
- All services exist within the todo-chatbot namespace
- Secrets provide configuration to Backend and Frontend services
- Services use Kubernetes DNS for internal communication

## State Transitions

**Pod Lifecycle**:
Pending → Running → Terminating → Terminated

**Deployment Lifecycle**:
Created → Updating → Active → Suspended

## Validation Rules

- All Kubernetes resources must be deployed to the todo-chatbot namespace
- Replica counts must match specifications (2 backend, 1 frontend)
- Container images must be pulled from Docker Hub (faizananjum/ namespace)
- Secrets must be properly referenced without exposing sensitive data in logs
- Services must be accessible within the cluster and externally via LoadBalancer