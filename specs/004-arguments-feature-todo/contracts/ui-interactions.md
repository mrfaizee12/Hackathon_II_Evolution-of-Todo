# UI Interaction Contracts: Todo UX Feedback, Form Reset & Dark Gradient UI

## Notification Service Contract

### Success Notification Creation
- **Event**: Todo successfully added or deleted
- **Input**:
  - message: string ("Todo added successfully" or "Todo deleted successfully")
  - type: "success"
  - duration: number (default 3000ms)
- **Output**: Notification displayed to user
- **Post-condition**: Notification appears on screen and auto-dismisses after duration

### Notification Dismissal
- **Event**: Auto-dismiss timer expires OR user clicks dismiss
- **Input**: notificationId: string
- **Output**: Notification removed from display
- **Post-condition**: Notification no longer visible to user

## Form State Management Contract

### Form Reset
- **Event**: Todo successfully added to backend
- **Input**: None
- **Output**: All form fields reset to initial state
- **Post-condition**: Form fields are empty/cleared for next input

### Form Validation
- **Event**: User submits form
- **Input**: Form data object
- **Output**: Validation result (valid/invalid)
- **Post-condition**: If valid, todo is sent to backend; if invalid, error shown to user

## UI State Contract

### Gradient Application
- **Event**: Page loads
- **Input**: None
- **Output**: Dark gradient background applied to main layout
- **Post-condition**: Entire dashboard area has dark gradient background

### Card Contrast Maintenance
- **Event**: Gradient applied
- **Input**: None
- **Output**: Todo cards remain light/white with sufficient contrast
- **Post-condition**: Text remains readable with WCAG AA compliance