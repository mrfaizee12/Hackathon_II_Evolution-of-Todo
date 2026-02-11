# API Contract: Advanced Todo Features

**Feature**: Frontend Integration for Advanced Todo Features (Recurring, Due Dates, Reminders)
**Date**: 2026-02-08
**Author**: Senior Frontend Engineer

## Overview

This document defines the API contracts for the advanced todo features (recurring tasks, due dates, reminders). It specifies the request/response formats for all relevant endpoints.

## Task Creation Endpoint

### POST /api/tasks

**Request Body:**
```json
{
  "title": "string (required)",
  "description": "string (optional)",
  "completed": "boolean (default: false)",
  "priority": "'low' | 'medium' | 'high' (default: 'medium')",
  "tags": "string (comma-separated tags)",
  "recurrence": {
    "type": "'none' | 'daily' | 'weekly' | 'monthly' (default: 'none')",
    "interval": "integer (optional, positive)",
    "endDate": "ISO date string (optional)"
  },
  "dueDate": "ISO date string (optional)",
  "reminderDateTime": "ISO date string (optional)",
  "ai_generated": "boolean (default: false)",
  "ai_context": "string (optional)"
}
```

**Response (201 Created):**
```json
{
  "success": true,
  "message": "Task created successfully",
  "task": {
    "id": "string (UUID)",
    "title": "string",
    "description": "string",
    "completed": "boolean",
    "priority": "string",
    "tags": "string",
    "created_at": "ISO date string",
    "updated_at": "ISO date string",
    "recurrence_type": "'none' | 'daily' | 'weekly' | 'monthly'",
    "recurrence_interval": "integer (nullable)",
    "due_date": "ISO date string (nullable)",
    "next_occurrence": "ISO date string (nullable)",
    "reminder_at": "ISO date string (nullable)",
    "ai_generated": "boolean",
    "ai_context": "string (nullable)"
  }
}
```

**Validation Errors (400 Bad Request):**
```json
{
  "success": false,
  "message": "string (descriptive error message)",
  "errors": [
    {
      "field": "string (field name)",
      "message": "string (validation error)"
    }
  ]
}
```

## Task Update Endpoint

### PUT /api/tasks/{taskId}

**Request Body:**
```json
{
  "title": "string (optional)",
  "description": "string (optional)",
  "completed": "boolean (optional)",
  "priority": "'low' | 'medium' | 'high' (optional)",
  "tags": "string (optional)",
  "recurrence": {
    "type": "'none' | 'daily' | 'weekly' | 'monthly' (optional)",
    "interval": "integer (optional, positive)",
    "endDate": "ISO date string (optional)"
  },
  "dueDate": "ISO date string (optional)",
  "reminderDateTime": "ISO date string (optional)",
  "ai_context": "string (optional)"
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Task updated successfully",
  "task": {
    "id": "string (UUID)",
    "title": "string",
    "description": "string",
    "completed": "boolean",
    "priority": "string",
    "tags": "string",
    "created_at": "ISO date string",
    "updated_at": "ISO date string",
    "recurrence_type": "'none' | 'daily' | 'weekly' | 'monthly'",
    "recurrence_interval": "integer (nullable)",
    "due_date": "ISO date string (nullable)",
    "next_occurrence": "ISO date string (nullable)",
    "reminder_at": "ISO date string (nullable)",
    "ai_context": "string (nullable)"
  }
}
```

## Get All Tasks Endpoint

### GET /api/tasks

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Retrieved X tasks",
  "tasks": [
    {
      "id": "string (UUID)",
      "title": "string",
      "description": "string",
      "completed": "boolean",
      "priority": "string",
      "tags": "string",
      "created_at": "ISO date string",
      "updated_at": "ISO date string",
      "recurrence_type": "'none' | 'daily' | 'weekly' | 'monthly'",
      "recurrence_interval": "integer (nullable)",
      "due_date": "ISO date string (nullable)",
      "next_occurrence": "ISO date string (nullable)",
      "reminder_at": "ISO date string (nullable)",
      "ai_context": "string (nullable)"
    }
  ],
  "total_count": "integer"
}
```

## Validation Rules

1. **Recurrence Validation**:
   - If recurrence.type is not 'none', the recurrence object must be valid
   - If recurrence.interval is provided, it must be a positive integer
   - If recurrence.endDate is provided, it must be after the current date

2. **Due Date Validation**:
   - If dueDate is provided, it must be a valid ISO date string
   - Due date can be in the past, present, or future

3. **Reminder Validation**:
   - If reminderDateTime is provided, it must be a valid ISO date string
   - If both reminderDateTime and dueDate are provided, reminderDateTime must be before or equal to dueDate
   - Reminder time cannot be in the past

4. **Combined Validation**:
   - If all three advanced fields are present, they must be logically consistent