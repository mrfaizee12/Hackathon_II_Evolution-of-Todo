# Data Model: Advanced Todo Features

## Overview
Extended Todo entity with recurrence, due date, and reminder capabilities while maintaining backward compatibility.

## Todo Entity Extensions

### Fields
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `recurrence_type` | String enum | Values: 'none', 'daily', 'weekly', 'monthly' | Defines recurrence frequency pattern |
| `recurrence_interval` | Integer | Positive integers only | Interval multiplier for recurrence (e.g., every 2 weeks) |
| `next_occurrence` | DateTime | Nullable | When the next recurring instance should be created |
| `due_date` | DateTime | Nullable | When the task is due (future dates only) |
| `reminder_at` | DateTime | Nullable, ≤ due_date | When to send reminder notification |

### Validation Rules
1. **Due Date Validation**: `due_date` must be in the future when set
2. **Reminder Timing**: `reminder_at` must be before or equal to `due_date`
3. **Recurrence Integrity**: If `recurrence_type` ≠ 'none', `recurrence_interval` must be positive
4. **Recurrence Chain**: Only one task in a recurrence series can be 'active' at a time
5. **Backward Compatibility**: All new fields are nullable with appropriate defaults

### State Transitions
- **Active Task** → **Completed** → **Triggers Next Occurrence Creation** (for recurring tasks)
- **Pending Due Date** → **Due Soon** → **Reminder Triggered** → **Due Date Reached**

### Relationships
- Maintains existing relationships (user, tags, priority, etc.)
- New fields are independent attributes of individual Todo records

## Recurrence Logic

### Recurrence Patterns
- **Daily**: Every X days from last completion
- **Weekly**: Same day of week X weeks from last completion
- **Monthly**: Same day of month X months from last completion
- **End Conditions**: Either indefinite or until specified end date

### Next Occurrence Calculation
- When current instance is completed, calculate next occurrence based on:
  - Recurrence type and interval
  - Completion timestamp
  - End date (if set)
- Create new instance with same title, recurrence settings, and calculated due date

## Indexes
- Composite index on `(user_id, due_date)` for efficient due date queries
- Composite index on `(user_id, reminder_at)` for reminder scheduling
- Index on `next_occurrence` for recurrence engine