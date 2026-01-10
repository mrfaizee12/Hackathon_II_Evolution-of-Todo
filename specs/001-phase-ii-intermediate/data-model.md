# Data Model: Phase II INTERMEDIATE - Todo Organization & Usability Enhancement

## Entity: Todo

### Fields
- **id** (UUID/Integer): Unique identifier for the todo
- **title** (String): Title of the todo (required)
- **description** (String): Optional description of the todo
- **completed** (Boolean): Whether the todo is completed (default: false)
- **priority** (Enum): Priority level of the todo (values: "high", "medium", "low"; default: "medium")
- **tags** (Array of Strings): List of tags associated with the todo (default: empty array)
- **due_date** (DateTime): Optional due date for the todo (nullable)
- **completed_at** (DateTime): Timestamp when the todo was completed (nullable)
- **created_at** (DateTime): Timestamp when the todo was created (auto-generated)
- **updated_at** (DateTime): Timestamp when the todo was last updated (auto-generated)
- **user_id** (UUID/Integer): Foreign key linking to the user who owns this todo

### Validation Rules
- title: Required, minimum 1 character, maximum 255 characters
- description: Optional, maximum 1000 characters
- priority: Must be one of "high", "medium", "low"
- tags: Maximum 10 tags per todo, each tag maximum 50 characters
- due_date: If provided, must be a valid future or past date
- completed_at: Only set when completed is true

### State Transitions
- New todo: completed=false, completed_at=null
- Todo completed: completed=true, completed_at=timestamp
- Todo uncompleted: completed=false, completed_at=null

## Entity: User

### Fields
- **id** (UUID/Integer): Unique identifier for the user
- **email** (String): User's email address (required, unique)
- **password_hash** (String): Hashed password (required)
- **name** (String): User's display name (required)
- **created_at** (DateTime): Timestamp when the user was created (auto-generated)
- **updated_at** (DateTime): Timestamp when the user was last updated (auto-generated)

## Relationships
- User (1) → Todo (Many): One user can have many todos
- Todo belongs to exactly one User

## Indexes
- todos.user_id: Index for efficient user-based queries
- todos.priority: Index for priority-based filtering
- todos.due_date: Index for due date-based queries
- todos.completed: Index for completion status filtering
- todos.created_at: Index for chronological sorting
- todos.title, todos.description: Full-text search index for search functionality