# Recovery Procedures

This document outlines the manual recovery procedures for persistent issues in the event-driven microservices architecture.

## Table of Contents
1. [General Recovery Guidelines](#general-recovery-guidelines)
2. [Service-Specific Recovery Procedures](#service-specific-recovery-procedures)
3. [Event Bus Recovery](#event-bus-recovery)
4. [Database Recovery](#database-recovery)
5. [Dapr Component Recovery](#dapr-component-recovery)

## General Recovery Guidelines

### Before Taking Action
1. Assess the scope of the issue
2. Check logs for error details
3. Determine if the issue affects one service or multiple services
4. Document the current state before making changes

### Common Recovery Steps
1. Restart the affected service(s)
2. Check service health endpoints
3. Verify connectivity to dependencies (database, event bus, etc.)
4. Monitor for resolution

## Service-Specific Recovery Procedures

### Todo Service
**Symptoms**: 
- API requests returning 5xx errors
- Task creation/update/deletion failing
- Events not being published

**Recovery Steps**:
1. Check the service health endpoint: `GET /health`
2. Verify database connectivity
3. Check event bus connectivity
4. Restart the service if needed:
   ```
   kubectl rollout restart deployment/todo-service
   ```
5. Monitor logs for errors after restart

### Recurring Engine
**Symptoms**:
- Recurring tasks not being created
- Scheduled triggers not firing
- Event processing delays

**Recovery Steps**:
1. Check the service health endpoint: `GET /health`
2. Verify event bus connectivity
3. Check for any stuck recurring tasks in the database
4. Restart the service if needed:
   ```
   kubectl rollout restart deployment/recurring-engine
   ```
5. Monitor logs for errors after restart

### Reminder Service
**Symptoms**:
- Reminders not being sent
- Scheduled notifications failing
- Event processing delays

**Recovery Steps**:
1. Check the service health endpoint: `GET /health`
2. Verify event bus connectivity
3. Check for any pending reminders in the database
4. Restart the service if needed:
   ```
   kubectl rollout restart deployment/reminder-service
   ```
5. Monitor logs for errors after restart

### Chatbot Service
**Symptoms**:
- Chat messages not being processed
- Context not being updated
- Event processing delays

**Recovery Steps**:
1. Check the service health endpoint: `GET /health`
2. Verify event bus connectivity
3. Check for any stuck conversations in the database
4. Restart the service if needed:
   ```
   kubectl rollout restart deployment/chatbot-service
   ```
5. Monitor logs for errors after restart

## Event Bus Recovery

### Redpanda/Kafka Issues
**Symptoms**:
- All services reporting event publishing/subscribing failures
- High latency in event processing
- Event queue buildup

**Recovery Steps**:
1. Check Redpanda cluster status:
   ```
   kubectl get pods -l app=redpanda
   ```
2. Check Redpanda logs for errors:
   ```
   kubectl logs -l app=redpanda
   ```
3. Restart Redpanda cluster if needed:
   ```
   kubectl rollout restart statefulset/redpanda
   ```
4. Verify topic health and partitions
5. Monitor services for recovery

### Event Processing Delays
**Recovery Steps**:
1. Check consumer lag for each service
2. Scale up the affected service if needed
3. Check for any dead letters in the event bus
4. Verify that event handlers are processing events correctly

## Database Recovery

### Connection Issues
**Symptoms**:
- All services reporting database connection errors
- Slow query responses
- Connection pool exhaustion

**Recovery Steps**:
1. Check database pod status:
   ```
   kubectl get pods -l app=postgres
   ```
2. Check database logs:
   ```
   kubectl logs -l app=postgres
   ```
3. Verify database connectivity from services
4. Restart database if needed:
   ```
   kubectl rollout restart deployment/postgres
   ```
5. Check connection pool settings in services

### Data Corruption
**Recovery Steps**:
1. Restore from the latest backup
2. Verify data integrity after restore
3. Check application logs for any inconsistencies
4. Update any cached data if needed

## Dapr Component Recovery

### Sidecar Issues
**Symptoms**:
- Services unable to communicate via Dapr
- State store operations failing
- Secret retrieval failing

**Recovery Steps**:
1. Check Dapr sidecar status in each pod:
   ```
   kubectl get pods --selector=dapr.io/enabled=true
   ```
2. Check Dapr control plane status:
   ```
   kubectl get pods -n dapr-system
   ```
3. Restart Dapr control plane if needed:
   ```
   kubectl rollout restart deployment/dapr-operator -n dapr-system
   kubectl rollout restart deployment/dapr-placement-server -n dapr-system
   kubectl rollout restart deployment/dapr-sidecar-injector -n dapr-system
   ```
4. Restart affected services to refresh Dapr sidecars

### Component Failures
**Recovery Steps**:
1. Check Dapr component status:
   ```
   kubectl get components.dapr.io -A
   ```
2. Verify component configurations are valid
3. Update component configurations if needed
4. Restart services that use the affected components

## Emergency Contacts

For issues that cannot be resolved with these procedures:
- Platform Team: [contact information]
- DevOps Team: [contact information]
- Database Admin: [contact information]