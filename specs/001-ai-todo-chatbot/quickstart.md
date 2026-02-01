# Quickstart Guide: AI Todo Chatbot

## Overview
This guide provides instructions for setting up and running the AI Todo Chatbot feature in the development environment.

## Prerequisites

- Python 3.11+
- Node.js 18+
- npm or pnpm
- UV package manager
- PostgreSQL-compatible database (Neon recommended)
- OpenRouter API key

## Environment Setup

### 1. Clone the Repository
```bash
git clone <repository-url>
cd <repository-name>
```

### 2. Set Up Backend Environment
```bash
# Navigate to backend directory
cd backend

# Install UV package manager if not already installed
pip install uv

# Install dependencies
uv pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your configuration
```

### 3. Set Up Frontend Environment
```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install
# or
pnpm install
```

## Environment Variables

Create a `.env` file in the backend directory with the following variables:

```env
DATABASE_URL=postgresql://username:password@localhost:5432/todo_db
OPENROUTER_API_KEY=your_openrouter_api_key_here
OPENROUTER_MODEL=openrouter/deepseek/deepseek-r1-0528-qwen3-8b:free
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
SECRET_KEY=your_secret_key_for_auth
```

## Database Setup

### 1. Run Migrations
```bash
# From backend directory
python -m src.main db migrate
```

### 2. Seed Initial Data (Optional)
```bash
# From backend directory
python -m src.main db seed
```

## Running the Application

### 1. Start the Backend Server
```bash
# From backend directory
python -m src.main server run
```

### 2. Start the Frontend Server
```bash
# From frontend directory
npm run dev
# or
pnpm dev
```

## API Endpoints

### Chat Endpoint
- POST `/api/v1/chat/{user_id}`
- Handles AI conversation requests
- Requires authentication

### Todo Endpoints
- GET `/api/v1/todos`
- POST `/api/v1/todos`
- PUT `/api/v1/todos/{id}`
- DELETE `/api/v1/todos/{id}`

## MCP Tool Server

The MCP tool server runs separately and provides AI tools for todo management:

```bash
# From backend directory
python -m src.tools.todo_tools
```

## Testing

### Backend Tests
```bash
# From backend directory
pytest tests/
```

### Frontend Tests
```bash
# From frontend directory
npm run test
# or
pnpm test
```

## Development Workflow

1. Make code changes
2. Run tests to ensure functionality
3. Format code using Black (Python) and Prettier (JavaScript/TypeScript)
4. Commit changes with conventional commit messages
5. Push to feature branch
6. Create pull request with reference to specification

## Troubleshooting

### Common Issues

**Issue**: "OpenRouter API key not found"
**Solution**: Ensure OPENROUTER_API_KEY is set in your environment variables

**Issue**: "Database connection failed"
**Solution**: Verify DATABASE_URL is correct and database is running

**Issue**: "Frontend cannot connect to backend"
**Solution**: Ensure backend is running and CORS settings are configured properly

## Next Steps

1. Explore the dashboard with the new AI Assistant sidebar item
2. Interact with the AI chatbot to manage todos
3. Review the API documentation for integration possibilities
4. Check the test suite to understand expected behaviors