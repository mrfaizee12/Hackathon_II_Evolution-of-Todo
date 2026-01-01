# Feature Specification: Phase I Advanced (Revised) - Task Scheduling and Organization

**Feature Branch**: `004-phase-i-advanced-v2`
**Created**: 2026-01-01
**Status**: Draft
**Input**: User description: "Create revised Phase I Advanced specification with recurrence and reminders for Evolution of Todo project. This specification includes due dates with date & time, console-based reminders for overdue and upcoming tasks, recurring tasks (daily/weekly/custom days), and auto-creation of next task on completion of recurring task. Constraints: CLI only, in-memory only, no background services, no notification APIs, no web or persistence, Phase I only. This specification supersedes previous Phase I Advanced spec."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Task Due Date Management (Priority: P1)

As a user managing tasks, I want to set due dates and times on my tasks so I can track deadlines with both date and time specificity.

**Why this priority**: Due dates with times are fundamental task management features that transform a task list from an unorganized collection into a time-aware productivity tool. This feature addresses critical need to manage precise deadlines (not just dates) and provides clear urgency indicators. It's the foundation for time-based features (overdue tracking, reminders, recurrence) and delivers immediate, measurable value.

**Independent Test**: Can be fully tested by creating tasks with various due dates and times and verifying they display correctly in task list with appropriate formatting. Delivers value by helping users identify deadline-driven tasks and track upcoming work.

**Acceptance Scenarios**:

1. **Given** creating a new task, **When** user specifies a due date and time, **Then** task is created with specified due date and time
2. **Given** creating a new task, **When** user creates task without specifying due date, **Then** task is created with no due date
3. **Given** task exists with due date and time, **When** user views task details, **Then** due date and time are displayed in human-readable format
4. **Given** task exists with due date and time, **When** user edits task and changes due date, **Then** task's due date is updated to new date and time
5. **Given** task exists with due date and time, **When** user edits task and removes due date, **Then** task's due date is cleared
6. **Given** creating a new task, **When** user specifies a due date in the past, **Then** system rejects the date and time with error message and task is not created
7. **Given** user enters invalid date or time format, **When** user attempts to save due date, **Then** system rejects with clear error message explaining correct format

---

### User Story 2 - Task Progress Tracking and Statistics (Priority: P2)

As a user managing multiple tasks, I want to see summary statistics about my task list so I can understand my productivity and workload at a glance.

**Why this priority**: Statistics provide visibility into task management patterns and help users make informed decisions about workload. This feature builds on existing data (completion status, priorities, tags, due dates) to deliver new insights without requiring additional user input. It's independently testable and provides measurable value for self-tracking and productivity improvement.

**Independent Test**: Can be fully tested by creating tasks with various states and due dates and verifying statistics accurately reflect current task list. Delivers value by providing users with quick insights into their task completion rate and distribution.

**Acceptance Scenarios**:

1. **Given** tasks exist in various states, **When** user views task statistics, **Then** total task count, completed count, and incomplete count are displayed
2. **Given** tasks exist with different priorities, **When** user views task statistics, **Then** distribution by priority (High/Medium/Low) is displayed
3. **Given** no tasks exist, **When** user views task statistics, **Then** all counts are zero with appropriate message
4. **Given** tasks exist with tags, **When** user views task statistics, **Then** tag usage statistics (tasks per tag) are displayed
5. **Given** tasks have due dates, **When** user views task statistics, **Then** due date statistics (overdue count, due today count, due within next 7 days count) are displayed
6. **Given** user completes a task, **When** user views task statistics again, **Then** completion percentage is updated to reflect new state
7. **Given** user creates and then immediately deletes a task, **When** user views task statistics, **Then** deleted task is not included in statistics

---

### User Story 3 - Recurring Task Management (Priority: P2)

As a user managing regular tasks, I want to set up recurring tasks (daily, weekly, or custom interval) so the system automatically creates the next instance when I complete the current one.

**Why this priority**: Recurring tasks address the productivity challenge of managing repetitive work (e.g., daily standups, weekly reports, monthly reviews). They save time and ensure regular tasks are never forgotten. This feature is independently testable and provides measurable value by automating routine task creation. While more complex than simple tasks, it builds on the foundation laid by due date management.

**Independent Test**: Can be fully tested by creating a recurring task, completing it, and verifying the next instance is created with the correct due date based on the recurrence rule. Delivers value by reducing repetitive data entry for routine tasks.

**Acceptance Scenarios**:

1. **Given** creating a new task, **When** user sets recurrence to "daily", **Then** next due date is automatically set to tomorrow after the current due date
2. **Given** creating a new task, **When** user sets recurrence to "weekly", **Then** next due date is automatically set to 7 days after the current due date
3. **Given** creating a new task, **When** user sets recurrence to custom interval (e.g., every 3 days), **Then** next due date is automatically set based on the custom interval
4. **Given** task with daily recurrence exists and is completed today, **When** user marks the task as complete, **Then** a new task instance is created with due date tomorrow
5. **Given** task with weekly recurrence exists with due date on Monday, **When** user marks the task as complete, **Then** a new task instance is created with due date next Monday
6. **Given** task with custom recurrence (every 5 days) exists, **When** user marks the task as complete, **Then** a new task instance is created with due date 5 days after the original due date
7. **Given** user sets recurrence on existing task, **When** user completes the task, **Then** the next task instance follows the recurrence rule

---

### User Story 4 - Console Reminders (Priority: P3)

As a user working on tasks, I want to see console-based reminders about overdue and upcoming tasks so I can stay on top of deadlines without needing notification systems.

**Why this priority**: Reminders provide proactive awareness of task deadlines without relying on external notification systems. This feature displays reminders during normal CLI operation (when viewing tasks, after actions), keeping users informed within the application itself. It's independently testable and provides measurable value by reducing missed deadlines and improving task completion rates.

**Independent Test**: Can be fully tested by creating tasks with various due dates, running the application, and verifying reminders are displayed at appropriate times (on task view, after actions). Delivers value by keeping users informed without needing external notification services.

**Acceptance Scenarios**:

1. **Given** tasks exist with due dates in the past, **When** user views all tasks or performs any action, **Then** overdue tasks are highlighted or displayed in a reminder section
2. **Given** tasks exist due today, **When** user views all tasks or performs any action, **Then** tasks due today are highlighted or displayed in a reminder section
3. **Given** tasks exist due within the next 7 days, **When** user views all tasks or performs any action, **Then** upcoming tasks are displayed in a reminder section
4. **Given** no overdue or upcoming tasks exist, **When** user views all tasks or performs any action, **Then** no reminders are displayed
5. **Given** user completes a task that becomes overdue, **When** task is marked complete, **Then** the task is removed from overdue reminders
6. **Given** user creates a new task due tomorrow, **When** user views tasks, **Then** the task appears in upcoming reminders

---

### User Story 5 - Task Templates (Priority: P3)

As a user who frequently creates similar tasks, I want to define and use task templates so I can quickly create consistent tasks with pre-filled information.

**Why this priority**: Task templates provide efficiency for repetitive task creation workflows (e.g., weekly meetings, monthly reports, standard processes). This feature saves time and ensures consistency, but is not essential for core task management. It's independently testable and delivers value by reducing data entry for common task patterns.

**Independent Test**: Can be fully tested by creating a template with predefined values, then using it to create tasks and verifying all predefined values are applied correctly. Delivers value by accelerating task creation for recurring task patterns.

**Acceptance Scenarios**:

1. **Given** user creates a task template with title, description, priority, tags, and recurrence, **When** user uses template to create a task, **Then** new task has all template values applied
2. **Given** template exists with predefined values, **When** user creates task from template but overrides a field, **Then** override value takes precedence over template value
3. **Given** user creates task from template, **When** template does not specify due date, **Then** task is created without due date
4. **Given** user creates task from template, **When** template specifies default priority and recurrence, **Then** task uses template values unless user explicitly changes them
5. **Given** multiple templates exist, **When** user views available templates, **Then** template names and descriptions are displayed
6. **Given** user deletes a template, **When** user attempts to use that template, **Then** template is no longer available
7. **Given** user creates a template with empty title, **When** user saves template, **Then** system rejects template with error message

---

### User Story 6 - Command History and Undo (Priority: P3)

As a user working through tasks, I want to undo recent actions so I can recover from mistakes without having to manually recreate or restore state.

**Why this priority**: Undo functionality provides a safety net for user errors and encourages experimentation. This feature improves user confidence and reduces the cost of mistakes. It's independently testable and provides measurable value by enabling quick recovery from unintended changes.

**Independent Test**: Can be fully tested by performing various actions (create, update, delete, toggle status, complete recurring tasks) and then using undo to verify operations are reversed correctly. Delivers value by providing a recovery mechanism for user mistakes.

**Acceptance Scenarios**:

1. **Given** user deletes a task, **When** user performs undo, **Then** deleted task is restored with all original properties
2. **Given** user updates task priority from Medium to High, **When** user performs undo, **Then** task priority returns to Medium
3. **Given** user completes a task, **When** user performs undo, **Then** task status returns to incomplete
4. **Given** user performs undo multiple times, **When** user continues undoing, **Then** operations are reversed in reverse chronological order
5. **Given** user performs undo after creating a new task, **When** undo completes, **Then** new task is deleted and its ID is no longer available
6. **Given** user completes a recurring task which auto-created a new task, **When** user performs undo, **Then** both the completion and the auto-created task are reverted
7. **Given** user has no undo history available, **When** user attempts undo, **Then** system displays message indicating no actions to undo

---

### Edge Cases

**Due Date and Time Edge Cases**:
- What happens when user tries to set due date/time to today's date/time? Should be allowed (today is valid deadline)
- How does system handle leap years and varying month lengths? Must correctly validate all valid calendar dates and times
- What happens when user sets due date/time for February 29 on a non-leap year? Should reject with clear error message
- How does system handle time zone differences in due dates/times? Should not consider time zones (local datetime only)
- What happens when due date is set for a task that already has a due date? Should replace existing due date with new one

**Statistics Edge Cases**:
- What happens when task list is empty and user views statistics? Should display all zeros with appropriate message
- How does system handle division by zero when calculating percentages? Should display 0% or "N/A" for empty state
- What happens when tags contain special characters or very long strings? Statistics should display tags accurately without truncation affecting readability
- How does system handle overdue task count when no tasks have due dates? Should display 0 for all due date categories

**Recurring Task Edge Cases**:
- What happens when user completes a recurring task but the calculated next due date is in the past? Should calculate next valid due date after today
- How does system handle leap years when calculating weekly recurrence on February 29? Should correctly advance to next occurrence (March 1st or February 28th of next leap year)
- What happens when user changes recurrence rule on an existing task? Should recalculate next due date based on new rule from original due date
- What happens when recurring task due date falls on a non-existent day (e.g., February 30th)? Should adjust to last valid day in month (February 28th or 29th)
- What happens when user completes recurring task multiple times before noticing it completed? System should create one new instance only, not duplicate multiple instances
- How does system handle DST (Daylight Saving Time) transitions? Should use datetime without explicit timezone to allow system to handle transitions naturally

**Reminder Display Edge Cases**:
- What happens when user has 10 overdue tasks and 15 upcoming tasks? Reminders should display counts or show top N most urgent tasks to avoid overwhelming display
- How does system handle tasks with due dates far in the future (months ahead)? Only show in reminders when within the 7-day window
- What happens when no tasks exist? Reminders section should be empty or display "No overdue or upcoming tasks"
- How frequently are reminders evaluated? On every task view, after every action, or at menu refresh only

**Task Templates Edge Cases**:
- What happens when user creates template with no fields specified? Should reject template with error message requiring at least title
- How does system handle templates with tags that don't exist on any task yet? Tags should be stored in template and applied to new tasks
- What happens when user creates template from a task with due date and recurrence, then uses template tomorrow? Due date should be relative to today (not absolute to original date)
- How does system handle duplicate template names? Should allow duplicates or enforce uniqueness with clear behavior

**Undo/Redo Edge Cases**:
- What happens when undo history exceeds reasonable limit (e.g., 100 operations)? Should limit history size with FIFO behavior or grow until memory constraint
- How does system handle undo after application restart? History should be lost (in-memory only) with appropriate user feedback
- What happens when user performs new action after several undos? New actions should be appended to history (redo history cleared)
- How does system handle undo on auto-created recurring task instances? Should undo both the completion action and the auto-creation action together

## Requirements *(mandatory)*

### Functional Requirements

**Due Date Requirements**:
- **FR-001**: System MUST allow users to optionally specify a due date and time when creating or editing tasks
- **FR-002**: System MUST validate that due dates are not in the past (must be current or future date/time)
- **FR-003**: System MUST accept due dates in standard date-time format (YYYY-MM-DD HH:MM)
- **FR-004**: System MUST display due dates and times in user-friendly format in task list and detail views
- **FR-005**: System MUST allow users to clear or remove due dates from tasks
- **FR-006**: System MUST reject invalid date or time formats with clear error message and expected format
- **FR-007**: System MUST correctly validate calendar dates and times including leap years and varying month lengths
- **FR-008**: System MUST allow today's date and current time as a valid due date/time

**Statistics and Reporting Requirements**:
- **FR-009**: System MUST provide summary statistics showing total task count
- **FR-010**: System MUST provide statistics showing completed task count and incomplete task count
- **FR-011**: System MUST calculate and display completion percentage (completed / total * 100)
- **FR-012**: System MUST provide statistics showing task distribution by priority (High/Medium/Low)
- **FR-013**: System MUST provide statistics showing tag usage (number of tasks per tag)
- **FR-014**: System MUST provide due date statistics (overdue count, due today count, due within next 7 days count)
- **FR-015**: System MUST handle empty task list gracefully (display all zeros or appropriate message)
- **FR-016**: System MUST handle division by zero for percentages (display 0% or "N/A")

**Recurring Task Requirements**:
- **FR-017**: System MUST allow users to set recurrence rules on tasks (none, daily, weekly, or custom interval)
- **FR-018**: System MUST store recurrence rule with each task (part of task data model)
- **FR-019**: System MUST automatically calculate the next due date based on recurrence rule when a recurring task is completed
- **FR-020**: System MUST automatically create a new task instance when a recurring task is completed
- **FR-021**: System MUST copy all task properties (title, description, priority, tags) from completed task to new instance
- **FR-022**: System MUST set the due date for the new task instance based on the recurrence rule
- **FR-023**: For daily recurrence, new task due date must be next day at the same time
- **FR-024**: For weekly recurrence, new task due date must be 7 days after the original due date
- **FR-025**: For custom interval recurrence, new task due date must be calculated by adding the interval days to the original due date
- **FR-026**: System MUST handle edge cases (leap years, month end dates, DST transitions) when calculating next due dates

**Reminder Requirements**:
- **FR-027**: System MUST display console-based reminders when overdue tasks exist
- **FR-028**: System MUST display console-based reminders when tasks due today exist
- **FR-029**: System MUST display console-based reminders when tasks due within next 7 days exist
- **FR-030**: System MUST display reminders during normal CLI operation (on task view, after actions, or menu refresh)
- **FR-031**: System MUST highlight or group overdue, due today, and upcoming tasks distinctly in reminders
- **FR-032**: System MUST update reminders automatically when task states change (completion, deletion, due date changes)
- **FR-033**: System MUST limit reminder display to avoid overwhelming user (show counts or top N urgent tasks if many)
- **FR-034**: System MUST display clear message when no overdue or upcoming tasks exist

**Task Template Requirements**:
- **FR-035**: System MUST allow users to create task templates with predefined values
- **FR-036**: System MUST allow templates to specify title (required field)
- **FR-037**: System MUST allow templates to specify description, priority, tags, due date, and recurrence rule (optional fields)
- **FR-038**: System MUST allow users to create tasks from templates with all template values applied
- **FR-039**: System MUST allow users to override template values when creating task from template
- **FR-040**: System MUST display available templates to user for selection
- **FR-041**: System MUST allow users to delete templates
- **FR-042**: System MUST reject templates without a title
- **FR-043**: For templates with due dates, the due date should be calculated as relative offset from current date (not absolute to original date)

**Undo and History Requirements**:
- **FR-044**: System MUST maintain history of recent user actions (create, update, delete, toggle status, recurring task completion)
- **FR-045**: System MUST allow users to undo the most recent action
- **FR-046**: System MUST allow users to undo multiple actions in reverse chronological order
- **FR-047**: System MUST correctly reverse delete operations by restoring deleted tasks
- **FR-048**: System MUST correctly reverse update operations by restoring previous values
- **FR-049**: System MUST correctly reverse create operations by deleting created task
- **FR-050**: System MUST correctly reverse recurring task completion by restoring the original task and deleting the auto-created instance
- **FR-051**: System MUST display message when no actions are available to undo
- **FR-052**: System MUST clear redo history when user performs new action after undoing

**Backward Compatibility Requirements**:
- **FR-053**: System MUST preserve all existing Phase I Basic and Intermediate functionality without modification
- **FR-054**: System MUST allow tasks created before due date feature to function correctly (no due date)
- **FR-055**: System MUST allow tasks created before recurrence feature to function correctly (no recurrence)
- **FR-056**: System MUST allow tasks created before reminder feature to function correctly (no reminders displayed for old tasks without due dates)

### Key Entities

**Task** (Extended from Phase I Intermediate):
- **id**: Unique identifier for the task
- **title**: Brief name of the task (required)
- **description**: Detailed information about the task
- **completion_status**: Whether task is completed or incomplete
- **priority**: Task importance level (High, Medium, or Low; defaults to Medium)
- **tags**: Collection of text labels used for categorization and filtering
- **due_date**: Optional deadline for task completion (YYYY-MM-DD HH:MM format, must be current or future)
- **recurrence_rule**: Optional recurrence pattern for the task (none, daily, weekly, or custom_interval_days)

**RecurrenceRule**:
- **type**: Type of recurrence ("none", "daily", "weekly", or "custom")
- **interval_days**: For custom recurrence, the number of days between instances (e.g., 3, 7, 14, etc.)
- **next_due_date_offset**: For convenience, store the offset to add for next instance (for daily: +1 day, weekly: +7 days, custom: +interval_days)

**TaskTemplate**:
- **id**: Unique identifier for the template
- **name**: Human-readable name for the template (required)
- **title**: Predefined title for tasks created from this template (required)
- **description**: Optional predefined description
- **priority**: Optional predefined priority level
- **tags**: Optional predefined tags
- **due_date**: Optional relative due date offset (e.g., "today", "tomorrow", "next week")
- **recurrence_rule**: Optional predefined recurrence rule (none, daily, weekly, or custom_interval_days)

**ActionHistoryEntry**:
- **action_type**: Type of action performed (create, update, delete, toggle_status, recurring_task_complete)
- **task_ids**: List of task IDs affected by the action
- **previous_state**: Snapshot of task state before the action (for undo)
- **timestamp**: When the action was performed

**TaskStatistics**:
- **total_tasks**: Total count of all tasks
- **completed_tasks**: Count of completed tasks
- **incomplete_tasks**: Count of incomplete tasks
- **completion_percentage**: Percentage of tasks completed
- **priority_distribution**: Count of tasks per priority level (High/Medium/Low)
- **tag_distribution**: Count of tasks per tag
- **overdue_count**: Count of tasks with due dates and times in the past
- **due_today_count**: Count of tasks with due date equal to today
- **due_this_week_count**: Count of tasks due within the next 7 days

## Constraints & Assumptions

### Constraints

**Technology Constraints** (from Constitution):
- System MUST remain an in-memory console application (Phase I scope)
- System MUST NOT introduce databases, files, or persistence mechanisms
- System MUST NOT introduce web, API, or network concepts
- System MUST NOT introduce AI, reminders, or notification APIs
- System MUST NOT reference future phase features (Phase II-V)
- System MUST NOT use background services or scheduled jobs

**Functional Constraints**:
- System MUST NOT modify or remove any existing Phase I Basic or Intermediate functionality
- All new features MUST be additive (extensions only)
- Due date format: YYYY-MM-DD HH:MM (standard ISO date-time format)
- Due date validation: Current time or future dates/times only (no past dates/times)
- Recurrence rules: Only support none, daily, weekly, or custom interval (no hourly, no complex schedules)
- Undo history limit: Maximum 50 actions stored in memory (configurable if needed)
- Maximum templates: 10 templates (reasonable limit for in-memory storage)
- Reminder evaluation: Only during normal CLI operation (not background scheduled jobs)

**User Interface Constraints**:
- System MUST continue using menu-driven CLI interface
- All new features MUST be accessible through existing menu structure
- Display MUST remain console-based (no graphical interface)
- Statistics MUST be viewable via dedicated menu option
- Reminders MUST be displayed inline during normal CLI operation (not separate notification system)
- Templates MUST be manageable via menu options

### Assumptions

- User is familiar with standard date and time format (YYYY-MM-DD HH:MM) or can learn with brief guidance
- User understands concept of "today" and "now" as valid deadline
- User recognizes that all data is lost when application exits (Phase I scope includes undo history)
- User expects templates to save time for repetitive task creation
- User expects recurrence to automate routine task creation without manual intervention
- User expects reminders to be visible during normal CLI operation (not background notifications)
- User typically manages fewer than 100 tasks at a time (in-memory constraint)
- User accepts that undo history is limited and older actions cannot be undone after 50 new actions
- User understands that templates store default values that can be overridden during task creation
- User expects statistics to update immediately when task state changes
- User does not need persistent storage of templates, history, or statistics (Phase I scope)
- User expects recurring tasks to auto-create the next instance immediately upon completion

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can set due dates with times on tasks within 10 seconds per task using standard date-time format
- **SC-002**: Users can view task statistics and understand current workload within 2 seconds
- **SC-003**: Users can set recurrence rules on tasks within 15 seconds per task
- **SC-004**: Users can create task from template within 5 seconds (reducing task creation time by 60%+ compared to manual entry)
- **SC-005**: Users can undo most recent action within 2 seconds
- **SC-006**: Users can view overdue, due today, and upcoming task reminders during normal CLI operation without waiting for notifications
- **SC-007**: 100% of existing Phase I Basic and Intermediate user workflows function identically after Advanced features are added
- **SC-008**: Due date and time validation rejects 100% of past dates/times with clear error message
- **SC-009**: Statistics accurately reflect current task state for 100% of operations (completion percentage, distribution, due date categories)
- **SC-010**: Templates apply all predefined values correctly to new tasks (0% missing values, 0% incorrect values)
- **SC-011**: Recurring tasks correctly calculate and create next instances for 100% of completions
- **SC-012**: Recurring tasks handle edge cases (leap years, DST transitions) correctly

### User Experience Outcomes

- **SC-013**: 90% of users correctly enter valid due date and time format on first attempt without reading documentation
- **SC-014**: 90% of users successfully set up their first recurring task within 2 minutes of discovering the feature
- **SC-015**: 90% of users successfully create task from template within 1 minute of first attempting template usage
- **SC-016**: 90% of users successfully undo a mistake within 30 seconds of discovering undo feature
- **SC-017**: 90% of users report that reminders help them avoid missing deadlines (qualitative feedback)
- **SC-018**: 90% of users report that recurring tasks save them significant time on routine tasks (qualitative feedback)
- **SC-019**: Users report that statistics provide useful insights into their productivity (qualitative feedback)

### Technical Outcomes

- **SC-020**: All due date and time validations complete in under 200ms per date
- **SC-021**: All statistics calculations complete in under 500ms for task lists up to 100 tasks
- **SC-022**: All recurring task calculations and instance creation complete in under 300ms per completion
- **SC-023**: All undo operations complete in under 300ms regardless of action type
- **SC-024**: No memory leaks occur when repeatedly creating and using templates
- **SC-025**: No memory leaks occur when repeatedly performing and undoing operations
- **SC-026**: All task data remains consistent when creating recurring task instances
- **SC-027**: System gracefully handles edge cases (empty templates, zero selection, invalid dates/times, DST transitions) with clear user feedback

## Out of Scope

The following features are explicitly **NOT** part of Phase I Advanced (Revised):

- Due date reminders or notifications via external APIs (email, push notifications, SMS, etc.)
- Background services or scheduled jobs running independently of CLI operation
- Complex recurrence schedules (hourly, bi-weekly, monthly patterns, cron-style expressions)
- Task dependencies or subtasks
- Task assignments to other users (multi-user support is Phase II)
- Calendar views or visual timeline displays
- Time tracking (hours spent, time estimates)
- Project or workspace management features beyond tags
- Advanced statistics (velocity, burn-down charts, historical trends)
- Email or notification integration
- Task comments or collaborative notes
- File attachments to tasks
- Rich text formatting in descriptions
- Task archiving or soft delete
- Search within templates
- Template versioning or history
- Redo functionality beyond basic undo
- Persistent storage of templates, history, or statistics
- Web interface or mobile app
- API or integration with calendar applications
- Integration with external task management systems
- Export of statistics or reports
- Advanced undo (granular undo of specific field changes)
- Task cloning (copy task with or without modifications)
- Bulk operations beyond delete, status toggle, and priority update
