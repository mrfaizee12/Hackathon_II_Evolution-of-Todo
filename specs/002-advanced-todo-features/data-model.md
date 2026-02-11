# Data Model: Frontend Integration for Advanced Todo Features

**Feature**: Frontend Integration for Advanced Todo Features (Recurring, Due Dates, Reminders)
**Date**: 2026-02-08
**Author**: Senior Frontend Engineer

## Overview

This document defines the data model extensions required to support advanced todo features (recurring tasks, due dates, reminders) in the frontend application. The model extends the existing task structure while maintaining backward compatibility.

## Task Entity Extensions

### Extended Task Interface

```typescript
interface Task {
  id: string;
  title: string;
  description?: string;
  completed: boolean;
  priority: 'low' | 'medium' | 'high';
  tags: string[]; // comma-separated tags stored as array
  createdAt: string; // ISO date string
  updatedAt: string; // ISO date string
  
  // NEW FIELDS FOR ADVANCED FEATURES
  recurrence?: RecurrencePattern; // Recurrence pattern if task repeats
  dueDate?: string; // ISO date string for when task is due
  reminderDateTime?: string; // ISO date string for when to remind user
}

interface RecurrencePattern {
  type: 'none' | 'daily' | 'weekly' | 'monthly';
  interval?: number; // How often to repeat (e.g., every 2 weeks)
  endDate?: string; // Optional end date for recurrence
}
```

### Validation Rules

1. **Recurrence Validation**:
   - If recurrence.type is not 'none', the recurrence object must be valid
   - If recurrence.interval is provided, it must be a positive integer
   - If recurrence.endDate is provided, it must be after the task creation date

2. **Due Date Validation**:
   - If dueDate is provided, it must be a valid ISO date string
   - Due date can be in the past, present, or future

3. **Reminder Validation**:
   - If reminderDateTime is provided, it must be a valid ISO date string
   - If both reminderDateTime and dueDate are provided, reminderDateTime must be before or equal to dueDate
   - Reminder time cannot be in the past

4. **Combined Validation**:
   - If all three advanced fields are present, they must be logically consistent
   - Recurring tasks may have due dates and reminders, but this creates complex scheduling scenarios

### State Transitions

1. **Task Creation**:
   - New tasks can be created with or without advanced properties
   - If recurrence is set, the system acknowledges the pattern but doesn't create future instances in the frontend

2. **Task Editing**:
   - Existing tasks can have advanced properties added or modified
   - Changes to recurrence patterns only affect future instances (backend responsibility)

3. **Task Completion**:
   - Completing a recurring task marks the current instance as complete
   - Backend handles creation of next instance based on recurrence pattern

## API Contract Extensions

### Create Task Request

```json
{
  "title": "string (required)",
  "description": "string (optional)",
  "priority": "'low' | 'medium' | 'high' (default: 'medium')",
  "tags": "string (comma-separated)",
  "recurrence": {
    "type": "'none' | 'daily' | 'weekly' | 'monthly'",
    "interval": "number (optional)",
    "endDate": "ISO date string (optional)"
  },
  "dueDate": "ISO date string (optional)",
  "reminderDateTime": "ISO date string (optional)"
}
```

### Update Task Request

```json
{
  "id": "string (required)",
  "title": "string (optional)",
  "description": "string (optional)",
  "completed": "boolean (optional)",
  "priority": "'low' | 'medium' | 'high' (optional)",
  "tags": "string (optional)",
  "recurrence": {
    "type": "'none' | 'daily' | 'weekly' | 'monthly' (optional)",
    "interval": "number (optional)",
    "endDate": "ISO date string (optional)"
  },
  "dueDate": "ISO date string (optional)",
  "reminderDateTime": "ISO date string (optional)"
}
```

### Task Response

```json
{
  "id": "string",
  "title": "string",
  "description": "string",
  "completed": "boolean",
  "priority": "'low' | 'medium' | 'high'",
  "tags": "string",
  "createdAt": "ISO date string",
  "updatedAt": "ISO date string",
  "recurrence": {
    "type": "'none' | 'daily' | 'weekly' | 'monthly'",
    "interval": "number (optional)",
    "endDate": "ISO date string (optional)"
  },
  "dueDate": "ISO date string (optional)",
  "reminderDateTime": "ISO date string (optional)"
}
```

## Component State Models

### Task Form State

```typescript
interface TaskFormState {
  title: string;
  description: string;
  priority: 'low' | 'medium' | 'high';
  tags: string;
  recurrence: {
    type: 'none' | 'daily' | 'weekly' | 'monthly';
    interval: number | '';
    endDate: string;
  };
  dueDate: string; // ISO date string
  reminderDateTime: string; // ISO date string
}
```

### Task Card Display Data

```typescript
interface TaskCardDisplayData {
  task: Task;
  isRecurring: boolean;
  isDueSoon: boolean; // Within 24 hours
  hasReminder: boolean;
  isOverdue: boolean;
}
```