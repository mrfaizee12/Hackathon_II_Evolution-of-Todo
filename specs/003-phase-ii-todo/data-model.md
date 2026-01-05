# Data Model: Phase II Intermediate Todo App

## Entities

### User (managed by Better Auth)
- `id`: UUID (Primary Key)
- `email`: string (Unique)
- `hashed_password`: string

### Todo
- `id`: UUID (Primary Key)
- `user_id`: UUID (Foreign Key -> User.id)
- `title`: string (len 1-200)
- `status`: boolean (default: False)
- `priority`: string (enum: "low", "medium", "high", default: "medium")
- `tags`: string (comma-separated or JSON list, default: "")
- `due_date`: datetime (optional, timezone-aware)
- `created_at`: datetime (auto-now)
- `updated_at`: datetime (auto-now-on-update)

## Validation Rules
- **Priority**: Must be one of ["low", "medium", "high"].
- **Title**: Cannot be empty or purely whitespace.
- **User Scope**: Every backend query MUST filter by `user_id` derived from the session token.
- **Due Date**: Must be a valid ISO 8601 string if provided.

## Relationships
- One-to-Many: User -> Todo (A user has many todos; a todo belongs to one user).
