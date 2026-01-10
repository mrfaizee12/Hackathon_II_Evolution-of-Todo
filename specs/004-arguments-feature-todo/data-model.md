# Data Model: Todo UX Feedback, Form Reset & Dark Gradient UI

## Entities

### Success Message
- **Type**: UI Component State
- **Fields**:
  - id: string (unique identifier for the message)
  - text: string (the message content - "Todo added successfully" or "Todo deleted successfully")
  - type: string ("success")
  - duration: number (auto-dismiss duration in ms, default 3000)
  - visible: boolean (current visibility state)

### Todo Form State
- **Type**: UI Component State
- **Fields**:
  - title: string (todo title input)
  - description: string (todo description input)
  - priority: string ("high" | "medium" | "low")
  - dueDate: string | null (due date in ISO format)
  - tags: string[] (array of tags for the todo)

### Notification Queue
- **Type**: UI State Management
- **Fields**:
  - messages: Success Message[] (array of active notifications)
  - maxVisible: number (maximum number of notifications visible at once, default 3)

## State Transitions

### Todo Form State
1. **Initial State**: All fields empty/default
2. **User Input**: Fields populated by user interaction
3. **Submission**: State preserved during API call
4. **Success**: State reset to initial state after successful API response
5. **Error**: State preserved for user correction

### Success Message State
1. **Trigger**: Created after successful todo add/delete operation
2. **Display**: Visible for duration specified
3. **Auto-dismiss**: Automatically removed after duration expires
4. **Manual Dismiss**: User can dismiss before auto-dismiss

## Validation Rules

### Success Message
- Text must not be empty
- Duration must be between 1000ms and 10000ms
- Type must be one of allowed values ("success")

### Todo Form State
- Title must not be empty when submitting
- Due date must be valid date format if provided
- Priority must be one of allowed values ("high", "medium", "low")