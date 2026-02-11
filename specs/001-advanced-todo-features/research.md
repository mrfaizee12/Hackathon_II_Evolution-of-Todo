# Research: Advanced Todo Features Implementation

## Overview
This research document addresses the technical requirements for implementing Recurring Tasks, Due Dates, and Reminder system for the Todo application while maintaining backward compatibility with existing features.

## Decision: Data Model Extensions for Advanced Features
**Rationale**: Need to extend the existing Todo schema to support recurring tasks, due dates, and reminders without breaking existing functionality.
**Approach**: Add nullable fields to existing Todo model to maintain backward compatibility.
**Fields to add**:
- `recurrence_type`: Enum ('none', 'daily', 'weekly', 'monthly') - default 'none'
- `recurrence_interval`: Integer - defines interval for recurrence pattern
- `next_occurrence`: DateTime - when next instance should be created
- `due_date`: DateTime - when task is due (nullable)
- `reminder_at`: DateTime - when to send reminder (nullable)

**Alternatives considered**:
- Separate tables for advanced features - would complicate joins and queries
- Completely new models - would break existing code
- JSON fields for recurrence data - would lose type safety

## Decision: Recurring Task Engine Architecture
**Rationale**: Need a mechanism to automatically create next task instance when current one is completed.
**Approach**: Event-driven architecture where task completion triggers next instance creation.
**Implementation**: When a recurring task is marked as complete, check if it has recurrence settings and create the next instance based on the schedule.
**Alternative approaches**:
- Background cron job - potential for missed recurrences if job fails
- Request-time generation - could cause slow responses
- Hybrid approach - complexity without clear benefits

## Decision: Due Date Validation Approach
**Rationale**: Ensure only future dates are accepted for due dates to prevent confusion.
**Approach**: Validate at API layer and database constraints to enforce future dates only.
**Implementation**:
- Client-side validation with visual feedback
- Server-side validation with proper error responses
- Database constraints where possible

## Decision: Reminder System Architecture
**Rationale**: Need to notify users before due dates without affecting request/response cycle.
**Approach**: Event-driven notification system that can scale with Kafka/Dapr in future phases.
**Implementation**:
- Create reminder events when due dates are set
- Use background worker or event queue for notification delivery
- Configurable timing preferences per user
- Prevent spam by deduplication logic

**Alternatives considered**:
- Polling system - inefficient and causes unnecessary load
- Direct email sending during request - blocking and unreliable
- Third-party scheduling service - adds external dependency

## Decision: API Extension Strategy
**Rationale**: Add new functionality without breaking existing API contracts.
**Approach**: Extend existing Todo API with new endpoints for advanced features.
**Endpoints to add**:
- POST/PUT `/todos/{id}/recurrence` - set/update recurrence
- PUT `/todos/{id}/due-date` - set due date
- PUT `/todos/{id}/reminder` - configure reminder
- GET `/todos/upcoming` - fetch tasks with due dates

**Backward Compatibility**: All existing endpoints remain unchanged with new optional fields.

## Decision: Chatbot Integration Approach
**Rationale**: Enable chatbot to understand and process advanced todo commands.
**Approach**: Extend existing chatbot tools with new structured functions for advanced features.
**Implementation**:
- Add new tools for recurrence, due dates, and reminders
- Update NLP patterns to recognize advanced user intents
- Maintain backward compatibility with existing commands

## Decision: Event System Preparation
**Rationale**: Prepare architecture for Phase V Kafka/Dapr integration.
**Approach**: Design event system with clear contracts that can be implemented with different backends.
**Events to publish**:
- `task.created` - when new task is created
- `task.completed` - when task is marked complete (triggers recurring logic)
- `reminder.triggered` - when reminder is ready to be sent

**Future readiness**: Abstract event publishing behind interface to easily swap implementations.

## Decision: Safety and Idempotency Measures
**Rationale**: Prevent duplicate reminders and recurring task instances.
**Approach**: Use idempotency keys and state tracking to ensure operations are safe to retry.
**Implementation**:
- Track processed events with unique identifiers
- Use database transactions for critical operations
- Add retry mechanisms with exponential backoff