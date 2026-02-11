# Quickstart Guide: Event-Driven Microservices Architecture

## Prerequisites

- Docker Desktop with Kubernetes enabled
- Minikube installed and running
- kubectl installed
- Dapr CLI installed
- Python 3.9+ installed

## Local Development Setup

### 1. Start Minikube Cluster
```bash
minikube start
```

### 2. Install Dapr in the cluster
```bash
dapr init -k
```

### 3. Clone and navigate to the project
```bash
git clone <repository-url>
cd todo-chatbot
```

### 4. Deploy the event-driven architecture
```bash
# Navigate to the deployment directory
cd helm-charts

# Install the platform using Helm
helm install todo-platform .
```

### 5. Verify the deployment
```bash
kubectl get pods
kubectl get services
dapr list
```

## Service Overview

### Available Services
- **Todo Service**: Manages task lifecycle (CRUD operations)
- **Recurring Engine**: Handles recurring task logic
- **Reminder/Notification Service**: Manages reminders and notifications
- **Chatbot Service**: Processes natural language interactions

### Service Endpoints
- Todo Service: `http://todo-service.local:3000`
- Recurring Engine: `http://recurring-engine.local:3001`
- Reminder Service: `http://reminder-service.local:3002`
- Chatbot Service: `http://chatbot-service.local:3003`

## Event Flow Examples

### Creating a Task
1. Send a POST request to the Todo Service:
```bash
curl -X POST http://todo-service.local:3000/api/v1/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Sample Task",
    "description": "This is a sample task",
    "due_date": "2026-12-31T23:59:59Z",
    "priority": "medium",
    "user_id": "user-123"
  }'
```

2. The Todo Service will publish a `task-created` event to the event bus

3. The Reminder Service will consume the event and schedule any required reminders

4. The Recurring Engine will consume the event and schedule any recurring tasks if applicable

### Checking Service Health
```bash
# Check all services
kubectl get pods

# Check specific service
kubectl logs <pod-name>

# Check Dapr sidecars
dapr status -k
```

## Development Workflow

### Adding New Event Types
1. Define the event schema in `contracts/openapi.yaml`
2. Update the data model in `data-model.md`
3. Modify services to publish/consume the new event
4. Update the relevant service's API contract

### Extending Service Functionality
1. Update the service's API contract in `contracts/openapi.yaml`
2. Implement the new functionality in the respective service
3. Update the data model if new entities are introduced
4. Add integration tests

## Troubleshooting

### Common Issues
- **Services not starting**: Check that Dapr is properly initialized in the cluster
- **Event delivery failures**: Verify the event bus is running and accessible
- **Service communication errors**: Ensure Dapr service invocation is configured correctly

### Useful Commands
```bash
# View all Dapr applications
dapr list -k

# Check Dapr logs
kubectl logs -l app=dapr-placement-server -n dapr-system

# Port forward to a service
kubectl port-forward svc/todo-service 3000:80

# Check event bus status (if using Kafka)
kubectl get pods -l app=kafka
```

## Clean Up
```bash
# Uninstall the platform
helm uninstall todo-platform

# Uninstall Dapr
dapr uninstall -k

# Stop Minikube
minikube stop
```