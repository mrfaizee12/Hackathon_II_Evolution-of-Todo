# Hugging Face Deployment Guide

This document explains how to deploy the event-driven microservices architecture to Hugging Face Spaces.

## Overview

The system consists of four main microservices:
- **Todo Service**: Handles task CRUD operations
- **Recurring Engine**: Processes recurring task logic
- **Reminder Service**: Manages reminder scheduling and notifications
- **Chatbot Service**: Processes natural language interactions

All services communicate through an event bus using Dapr for pub/sub and state management.

## Deployment Steps

### 1. Prepare Your Hugging Face Space

1. Create a new Space on Hugging Face with the Docker option
2. Add your source code to the repository
3. Ensure your `.env` file contains the required environment variables

### 2. Environment Variables

Make sure your `.env` file includes:

```
DATABASE_URL=
SECRET_KEY=a5fc2776eecd3988b703c53fa959331099a9fc24d7190b0d62a244b5f4b09c54
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
OPENROUTER_API_KEY=
```

### 3. Docker Configuration

The system uses the `docker-compose.hf.yml` file to orchestrate the services. This configuration:

- Sets up a PostgreSQL database
- Configures Redpanda as the event bus
- Runs all four microservices
- Sets up proper networking between services

### 4. API Access

The services are accessible through these endpoints:

- Todo Service: `/api/v1/tasks`
- Recurring Engine: `/api/v1/recurring`
- Reminder Service: `/api/v1/reminders` and `/api/v1/notifications`
- Chatbot Service: `/api/v1/chat`

### 5. Event Flow

The system follows this event-driven flow:

1. When a task is created, the Todo Service publishes a `task-created` event
2. The Reminder Service listens for `task-created` events to schedule reminders
3. The Recurring Engine listens for `task-created` events to handle recurring tasks
4. The Chatbot Service listens for various events to maintain context

## Architecture Benefits

- **Loose Coupling**: Services communicate through events, reducing dependencies
- **Scalability**: Each service can be scaled independently
- **Maintainability**: Clear separation of concerns
- **Resilience**: Failure in one service doesn't bring down others
- **Portability**: Designed to run in containerized environments like Hugging Face

## Troubleshooting

### Common Issues

1. **Database Connection Issues**: Verify your DATABASE_URL is correct and accessible
2. **Event Bus Issues**: Check that Redpanda is running and services can connect
3. **Service Communication**: Ensure all services are on the same network

### Logs

Check service logs with:
```
docker-compose -f docker-compose.hf.yml logs [service-name]
```

## Scaling

To scale individual services, you can modify the compose file or use Hugging Face's scaling options in the Space settings.