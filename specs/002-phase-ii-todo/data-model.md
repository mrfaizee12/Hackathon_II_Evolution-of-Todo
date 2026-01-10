# Data Model: Phase II Todo Web Application

## User Entity

**Entity Name**: User
**Description**: Represents an authenticated user with credentials
**Fields**:
- id: UUID (Primary Key, auto-generated)
- email: String (Required, unique, valid email format)
- password_hash: String (Required, hashed password)
- created_at: DateTime (Auto-generated timestamp)
- updated_at: DateTime (Auto-generated timestamp, updated on changes)

**Relationships**:
- One-to-Many: User → Todo (one user can have many todos)

**Validation Rules**:
- Email must be valid email format
- Email must be unique across all users
- Password must meet security requirements (min 8 characters)
- All required fields must be present

## Todo Entity

**Entity Name**: Todo
**Description**: Represents a task item with content, completion status, and user association
**Fields**:
- id: UUID (Primary Key, auto-generated)
- title: String (Required, max 255 characters)
- description: Text (Optional, max 1000 characters)
- completed: Boolean (Required, default: false)
- user_id: UUID (Foreign Key, references User.id)
- created_at: DateTime (Auto-generated timestamp)
- updated_at: DateTime (Auto-generated timestamp, updated on changes)

**Relationships**:
- Many-to-One: Todo → User (many todos belong to one user)

**Validation Rules**:
- Title is required and must not be empty
- Title must be less than 256 characters
- Description must be less than 1001 characters if provided
- User_id must reference an existing user
- Completed status must be a boolean value

## State Transitions

**Todo State Transitions**:
- Incomplete → Complete (when user marks todo as complete)
- Complete → Incomplete (when user marks todo as incomplete)

## Data Isolation

**User Data Isolation**:
- Each user can only access todos associated with their user_id
- Backend must enforce user_id matching for all todo operations
- Unauthorized access attempts must return appropriate error responses