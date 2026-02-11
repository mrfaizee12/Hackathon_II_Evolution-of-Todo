# Quickstart Guide: Advanced Todo Features

## Overview
This guide covers the setup and basic usage of the new advanced features: recurring tasks, due dates, and reminders.

## Prerequisites
- Python 3.11+ with the existing Todo application running
- Access to the extended Todo API endpoints
- Existing user authentication system (Better Auth)

## New Features Setup

### 1. Recurring Tasks
Create or update a task with recurrence settings:

```bash
# Set a task to repeat daily
curl -X PUT http://localhost:8000/api/v1/todos/1/recurrence \
  -H "Content-Type: application/json" \
  -d '{
    "recurrence_type": "daily",
    "recurrence_interval": 1
  }'

# Set a task to repeat weekly
curl -X PUT http://localhost:8000/api/v1/todos/1/recurrence \
  -H "Content-Type: application/json" \
  -d '{
    "recurrence_type": "weekly",
    "recurrence_interval": 2,
    "end_date": "2025-12-31T23:59:59Z"
  }'
```

### 2. Due Dates
Set a due date for a task:

```bash
# Set due date for a task
curl -X PUT http://localhost:8000/api/v1/todos/1/due-date \
  -H "Content-Type: application/json" \
  -d '{
    "due_date": "2025-01-15T18:00:00Z"
  }'
```

### 3. Reminders
Configure a reminder for a task:

```bash
# Set a reminder 2 hours before due date
curl -X PUT http://localhost:8000/api/v1/todos/1/reminder \
  -H "Content-Type: application/json" \
  -d '{
    "reminder_at": "2025-01-15T16:00:00Z"
  }'
```

### 4. Fetch Upcoming Tasks
Get tasks with upcoming due dates:

```bash
# Get tasks due in the next 7 days
curl -X GET "http://localhost:8000/api/v1/todos/upcoming"

# Get tasks due in the next 30 days
curl -X GET "http://localhost:8000/api/v1/todos/upcoming?days_ahead=30"

# Include overdue tasks
curl -X GET "http://localhost:8000/api/v1/todos/upcoming?include_overdue=true"
```

## Data Model Changes
The Todo model now includes additional fields:
- `recurrence_type`: none, daily, weekly, or monthly
- `recurrence_interval`: integer for recurrence frequency
- `next_occurrence`: datetime for next task creation
- `due_date`: datetime for task deadline
- `reminder_at`: datetime for reminder notification

## Event Flow
1. When a recurring task is completed, the system automatically creates the next occurrence
2. Reminder notifications are triggered based on `reminder_at` time
3. Due date validation ensures only future dates are accepted

## Backward Compatibility
All existing Todo functionality remains unchanged. The new features are additive, and existing API endpoints continue to work as before.