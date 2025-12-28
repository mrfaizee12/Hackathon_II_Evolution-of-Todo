# CLI Interface Contract: Phase I - Basic Todo Console Application

**Feature**: Phase I - Basic Todo Console Application
**Date**: 2025-12-28
**Status**: Complete
**Contract Type**: Command-Line Interface (CLI)

## Overview

This document defines the complete command-line interface contract for the Phase I todo application. It specifies exact menu options, input prompts, output formats, and error messages that users will encounter.

---

## Application Entry

### Startup

**Command**:
```bash
python src/main.py
```

**Welcome Message** (FR-013):
```
Welcome to Todo Application - Phase I
```

**Initial State**: Empty task list, ready to display main menu

---

## Main Menu

### Menu Display (FR-001)

**Format**:
```
Main Menu:
1. View all tasks
2. Add a new task
3. Update a task
4. Delete a task
5. Mark task complete/incomplete
6. Exit

Enter your choice:
```

**Prompt**: `Enter your choice: ` (with trailing space, cursor waits on same line)

### Menu Choice Input

**Expected Input**: Integer between 1 and 6

**Valid Inputs**: `1`, `2`, `3`, `4`, `5`, `6`

**Invalid Input Handling**:

| Invalid Input | Error Message |
|---------------|---------------|
| Non-integer (e.g., "abc", "1.5") | `Invalid input. Please enter a number.` |
| Out of range (e.g., 0, 7, -1) | `Invalid choice. Please enter a number between 1 and 6.` |
| Empty input (just Enter) | `Invalid input. Please enter a number.` |

**After Error**: Redisplay menu and prompt again

---

## Option 1: View All Tasks

### Command Flow

1. User selects `1` from main menu
2. Application displays all tasks or empty message
3. Returns to main menu (FR-012)

### Output Format: Task List

**When tasks exist** (FR-005):
```
--- All Tasks ---
ID: 1 | Title: Buy groceries | Status: Incomplete
Description: Milk, eggs, bread

ID: 2 | Title: Call dentist | Status: Complete
Description:

ID: 3 | Title: Finish report | Status: Incomplete
Description: Q4 financial summary for board meeting
```

**Format Rules**:
- Header: `--- All Tasks ---`
- Each task displays on 2 lines:
  - Line 1: `ID: <id> | Title: <title> | Status: <status>`
  - Line 2: `Description: <description>` (even if empty)
- Blank line between tasks
- Status values: exactly `Complete` or `Incomplete` (case-sensitive)

**When no tasks exist**:
```
--- All Tasks ---
No tasks found. Add a task to get started!
```

### Edge Cases

- Empty description: Display `Description:` with blank value (no placeholder text)
- Very long title/description: Display as-is (no truncation in Phase I)
- 100+ tasks: Display all (performance acceptable per spec SC-006)

---

## Option 2: Add a New Task

### Command Flow

1. User selects `2` from main menu
2. Application prompts for title
3. Application prompts for description
4. Application creates task or shows error
5. Returns to main menu (FR-012)

### Input Prompts (FR-002)

**Title Prompt**:
```
--- Add New Task ---
Enter task title:
```

**Expected Input**: Non-empty string

**Description Prompt**:
```
Enter task description (optional):
```

**Expected Input**: Any string (can be empty, just press Enter)

### Success Output

**Format**:
```
Task added successfully! (ID: <id>)
```

**Example**:
```
Task added successfully! (ID: 1)
```

### Error Output (FR-009, FR-010)

| Error Condition | Error Message |
|-----------------|---------------|
| Empty title (blank, whitespace only) | `Error: Task title cannot be empty` |

**After Error**: Return to main menu (do not create task)

### Examples

**Example 1: Task with title and description**
```
--- Add New Task ---
Enter task title: Buy groceries
Enter task description (optional): Milk, eggs, bread

Task added successfully! (ID: 1)
```

**Example 2: Task with title only**
```
--- Add New Task ---
Enter task title: Call dentist
Enter task description (optional):

Task added successfully! (ID: 2)
```

**Example 3: Empty title error**
```
--- Add New Task ---
Enter task title:
Error: Task title cannot be empty
```

---

## Option 3: Update a Task

### Command Flow

1. User selects `3` from main menu
2. Application prompts for task ID
3. Application prompts for new title
4. Application prompts for new description
5. Application updates task or shows error
6. Returns to main menu (FR-012)

### Input Prompts (FR-006)

**Task ID Prompt**:
```
--- Update Task ---
Enter task ID:
```

**Expected Input**: Positive integer (ID of existing task)

**New Title Prompt**:
```
Enter new title (or press Enter to keep current):
```

**Expected Input**: Non-empty string, or Enter to skip

**New Description Prompt**:
```
Enter new description (or press Enter to keep current):
```

**Expected Input**: Any string, or Enter to skip

### Success Output

**Format**:
```
Task updated successfully!
```

### Error Output (FR-010, FR-014)

| Error Condition | Error Message |
|-----------------|---------------|
| Non-integer ID | `Invalid input. Please enter a valid task ID.` |
| Task ID not found (FR-014) | `Error: Task not found (ID: <id>)` |
| New title is empty/whitespace | `Error: Task title cannot be empty` |
| Both title and description skipped | `No changes made.` |

**After Error**: Return to main menu (do not update task)

### Examples

**Example 1: Update title only**
```
--- Update Task ---
Enter task ID: 1
Enter new title (or press Enter to keep current): Buy groceries and toiletries
Enter new description (or press Enter to keep current):

Task updated successfully!
```

**Example 2: Update description only**
```
--- Update Task ---
Enter task ID: 2
Enter new title (or press Enter to keep current):
Enter new description (or press Enter to keep current): Appointment at 3 PM

Task updated successfully!
```

**Example 3: Update both**
```
--- Update Task ---
Enter task ID: 3
Enter new title (or press Enter to keep current): Complete Q4 report
Enter new description (or press Enter to keep current): Financial summary due Friday

Task updated successfully!
```

**Example 4: Task not found**
```
--- Update Task ---
Enter task ID: 999
Error: Task not found (ID: 999)
```

---

## Option 4: Delete a Task

### Command Flow

1. User selects `4` from main menu
2. Application prompts for task ID
3. Application deletes task or shows error
4. Returns to main menu (FR-012)

### Input Prompts (FR-008)

**Task ID Prompt**:
```
--- Delete Task ---
Enter task ID:
```

**Expected Input**: Positive integer (ID of existing task)

### Success Output

**Format**:
```
Task deleted successfully! (ID: <id>)
```

**Example**:
```
Task deleted successfully! (ID: 3)
```

### Error Output (FR-010, FR-014)

| Error Condition | Error Message |
|-----------------|---------------|
| Non-integer ID | `Invalid input. Please enter a valid task ID.` |
| Task ID not found (FR-014) | `Error: Task not found (ID: <id>)` |

**After Error**: Return to main menu (do not delete anything)

### Examples

**Example 1: Successful deletion**
```
--- Delete Task ---
Enter task ID: 2

Task deleted successfully! (ID: 2)
```

**Example 2: Task not found**
```
--- Delete Task ---
Enter task ID: 999
Error: Task not found (ID: 999)
```

**Example 3: Invalid ID**
```
--- Delete Task ---
Enter task ID: abc
Invalid input. Please enter a valid task ID.
```

---

## Option 5: Mark Task Complete/Incomplete

### Command Flow

1. User selects `5` from main menu
2. Application prompts for task ID
3. Application displays current status
4. Application prompts for new status (c/i)
5. Application toggles status or shows error
6. Returns to main menu (FR-012)

### Input Prompts (FR-007)

**Task ID Prompt**:
```
--- Mark Task Complete/Incomplete ---
Enter task ID:
```

**Expected Input**: Positive integer (ID of existing task)

**Current Status Display**:
```
Current status: <Complete|Incomplete>
```

**Status Choice Prompt**:
```
Mark as (c)omplete or (i)ncomplete?
```

**Expected Input**: Single character `c` or `i` (case-insensitive)

### Success Output

**Format**:
```
Task marked as <Complete|Incomplete>!
```

**Examples**:
```
Task marked as Complete!
Task marked as Incomplete!
```

### Error Output (FR-010, FR-014)

| Error Condition | Error Message |
|-----------------|---------------|
| Non-integer ID | `Invalid input. Please enter a valid task ID.` |
| Task ID not found (FR-014) | `Error: Task not found (ID: <id>)` |
| Invalid status choice (not c/i) | `Invalid choice. Please enter 'c' for complete or 'i' for incomplete.` |

**After Error**: Return to main menu (do not change status)

### Examples

**Example 1: Mark task complete**
```
--- Mark Task Complete/Incomplete ---
Enter task ID: 1
Current status: Incomplete
Mark as (c)omplete or (i)ncomplete? c

Task marked as Complete!
```

**Example 2: Mark task incomplete**
```
--- Mark Task Complete/Incomplete ---
Enter task ID: 1
Current status: Complete
Mark as (c)omplete or (i)ncomplete? i

Task marked as Incomplete!
```

**Example 3: Task not found**
```
--- Mark Task Complete/Incomplete ---
Enter task ID: 999
Error: Task not found (ID: 999)
```

**Example 4: Invalid status choice**
```
--- Mark Task Complete/Incomplete ---
Enter task ID: 1
Current status: Incomplete
Mark as (c)omplete or (i)ncomplete? x

Invalid choice. Please enter 'c' for complete or 'i' for incomplete.
```

---

## Option 6: Exit Application

### Command Flow

1. User selects `6` from main menu
2. Application displays goodbye message
3. Application terminates (FR-011)

### Output (FR-011)

**Format**:
```
Exiting application. All data will be lost.
Goodbye!
```

**Behavior**: Application exits, all task data is lost (NFR-004)

---

## Error Handling Summary

### Input Validation Errors

| Error Type | Context | Message |
|------------|---------|---------|
| Non-numeric menu choice | Main menu | `Invalid input. Please enter a number.` |
| Out-of-range menu choice | Main menu | `Invalid choice. Please enter a number between 1 and 6.` |
| Non-numeric task ID | Any operation requiring ID | `Invalid input. Please enter a valid task ID.` |
| Empty task title | Add/Update task | `Error: Task title cannot be empty` |
| Invalid status choice | Mark complete/incomplete | `Invalid choice. Please enter 'c' for complete or 'i' for incomplete.` |

### Business Logic Errors

| Error Type | Context | Message |
|------------|---------|---------|
| Task not found | Update/Delete/Toggle status | `Error: Task not found (ID: <id>)` |
| No changes in update | Update task (both inputs skipped) | `No changes made.` |

### Error Display Format

**Success Messages**: Plain text or green/bold if terminal supports
**Error Messages**: Prefix with `Error:` and display in red/bold if terminal supports, fallback to plain text

---

## Menu Loop Behavior (FR-012)

**After Every Operation**: Return to main menu automatically

**Exception**: Only option 6 (Exit) terminates the application

**Loop Structure**:
```
1. Display menu
2. Get user choice
3. Execute operation (options 1-6)
4. If not exit:
   a. Display blank line for spacing
   b. Go to step 1
5. If exit:
   a. Display goodbye message
   b. Terminate
```

---

## Terminal Requirements

### Minimum Terminal Support

- Standard input (stdin): Read user input line by line
- Standard output (stdout): Display text messages
- UTF-8 encoding: Support for standard ASCII and common Unicode characters

### Optional Terminal Features

- **Color support**: Green for success, red for errors
  - If not available: Fall back to plain text
- **Bold text**: Emphasize headers and important messages
  - If not available: Fall back to plain text

### Cross-Platform Compatibility

- Windows: Command Prompt, PowerShell, Windows Terminal
- Linux: bash, zsh, gnome-terminal, konsole
- macOS: Terminal.app, iTerm2

---

## Performance Expectations (SC-001, SC-002, SC-003)

| Operation | Expected Response Time |
|-----------|------------------------|
| Display menu | Instant (<10ms) |
| View all tasks | Instant (<10ms for 100 tasks) |
| Add task | <30 seconds total (user input time) |
| Update task | Instant operation (<10ms) |
| Delete task | Instant operation (<10ms) |
| Toggle status | <15 seconds total (user input time) |

**Note**: Times include user input duration for operations requiring input

---

## Complete Interaction Example

```
Welcome to Todo Application - Phase I

Main Menu:
1. View all tasks
2. Add a new task
3. Update a task
4. Delete a task
5. Mark task complete/incomplete
6. Exit

Enter your choice: 2

--- Add New Task ---
Enter task title: Buy groceries
Enter task description (optional): Milk, eggs, bread

Task added successfully! (ID: 1)

Main Menu:
1. View all tasks
2. Add a new task
3. Update a task
4. Delete a task
5. Mark task complete/incomplete
6. Exit

Enter your choice: 1

--- All Tasks ---
ID: 1 | Title: Buy groceries | Status: Incomplete
Description: Milk, eggs, bread

Main Menu:
1. View all tasks
2. Add a new task
3. Update a task
4. Delete a task
5. Mark task complete/incomplete
6. Exit

Enter your choice: 5

--- Mark Task Complete/Incomplete ---
Enter task ID: 1
Current status: Incomplete
Mark as (c)omplete or (i)ncomplete? c

Task marked as Complete!

Main Menu:
1. View all tasks
2. Add a new task
3. Update a task
4. Delete a task
5. Mark task complete/incomplete
6. Exit

Enter your choice: 6

Exiting application. All data will be lost.
Goodbye!
```

---

## Contract Validation

This CLI interface contract satisfies all Phase I requirements:

- [x] FR-001: Text-based menu with numbered options
- [x] FR-002: Add task with title and optional description
- [x] FR-005: Display tasks with ID, title, status, description
- [x] FR-006: Update task title and/or description
- [x] FR-007: Mark task complete or incomplete
- [x] FR-008: Delete task by ID
- [x] FR-009: Validate title is non-empty
- [x] FR-010: Clear error messages for invalid operations
- [x] FR-011: Exit application with data loss
- [x] FR-012: Return to menu after operations
- [x] FR-013: Display welcome message on startup
- [x] FR-014: Validate task IDs exist before operations

**Status**: CLI interface contract complete and ready for implementation.
