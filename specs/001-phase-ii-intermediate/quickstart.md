# Quickstart Guide: Phase II INTERMEDIATE - Todo Organization & Usability Enhancement

## Prerequisites

- Python 3.11+
- Node.js 18+
- UV package manager (for Python dependencies)
- PostgreSQL-compatible database (Neon Serverless PostgreSQL recommended)
- Better Auth account setup

## Setup Instructions

### 1. Clone and Initialize Repository

```bash
git clone <repository-url>
cd todo_app
```

### 2. Backend Setup

```bash
cd backend

# Install dependencies using UV
uv pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your database URL and Better Auth configuration

# Run database migrations
python -m src.database.migrate

# Start the backend server
uvicorn src.main:app --reload --port 8000
```

### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Set up environment variables
cp .env.example .env.local
# Edit .env.local with your backend API URL

# Start the development server
npm run dev
```

## API Endpoints

### Todo Operations

- `GET /api/todos` - List todos with optional query parameters:
  - `?search=keyword` - Search by title/description
  - `?priority=high,medium,low` - Filter by priority
  - `?tags=work,personal` - Filter by tags
  - `?due_date_from=2023-01-01` - Filter by due date range start
  - `?due_date_to=2023-12-31` - Filter by due date range end
  - `?completed=true/false` - Filter by completion status
  - `?sort=priority,created_at,due_date,title` - Sort results
  - `?order=asc,desc` - Sort order (default: asc)

- `POST /api/todos` - Create a new todo with:
  - `title` (required)
  - `description` (optional)
  - `priority` (optional, default: "medium")
  - `tags` (optional, array of strings)
  - `due_date` (optional, ISO 8601 datetime)

- `PUT /api/todos/{id}` - Update an existing todo
- `DELETE /api/todos/{id}` - Delete a todo
- `PATCH /api/todos/{id}/toggle_complete` - Toggle completion status

### Authentication

- `POST /api/auth/signup` - User registration
- `POST /api/auth/signin` - User login
- All todo endpoints require authentication

## Environment Variables

### Backend (.env)
```
DATABASE_URL=postgresql://user:password@localhost:5432/todo_db
BETTER_AUTH_SECRET=your_secret_key
BETTER_AUTH_URL=http://localhost:8000
```

### Frontend (.env.local)
```
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:8000
```

## Running Tests

### Backend Tests
```bash
cd backend
pytest tests/
```

### Frontend Tests
```bash
cd frontend
npm test
```

## Key Features

### Priority Management
- Todos can be assigned priorities: high, medium, low
- Priority is displayed visually in the UI
- Todos can be filtered and sorted by priority

### Tagging System
- Todos can have multiple tags
- Tags can be searched and filtered
- Tag suggestions available in the UI

### Search and Filtering
- Full-text search across title and description
- Advanced filtering by priority, tags, due date, and completion status
- Sorting options by various attributes

### Due Date Management
- Todos can have optional due dates
- Visual indicators for upcoming and overdue tasks
- Filtering by due date ranges

## Development Workflow

1. Make changes to the codebase
2. Run backend tests: `cd backend && pytest`
3. Run frontend tests: `cd frontend && npm test`
4. Start both servers and test manually
5. Commit changes following conventional commits format
6. Push to the feature branch