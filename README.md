# Phase II Todo Web Application

A full-stack web application for todo management with user authentication.

## Features

- User authentication (signup/signin)
- Todo management (create, read, update, delete)
- Todo completion tracking
- User-specific data isolation
- Responsive UI with gradient theme and animations
- Modern SaaS-style interface

## Tech Stack

### Backend
- **Framework**: FastAPI (Python 3.11+)
- **Database**: Neon Serverless PostgreSQL
- **ORM**: SQLModel
- **Authentication**: Built-in JWT authentication system

### Frontend
- **Framework**: Next.js (React with TypeScript)
- **Styling**: Tailwind CSS with custom gradient theme
- **State Management**: React Context API

## API Endpoints

### Authentication
- `POST /api/v1/auth/signup` - Create new user account
- `POST /api/v1/auth/signin` - Authenticate user
- `POST /api/v1/auth/signout` - Sign out user
- `GET /api/v1/auth/me` - Get current user info

### Todo Management
- `GET /api/v1/todos` - Get all user's todos
- `POST /api/v1/todos` - Create new todo
- `PUT /api/v1/todos/{id}` - Update todo
- `DELETE /api/v1/todos/{id}` - Delete todo
- `PATCH /api/v1/todos/{id}/status` - Update todo completion status

## Setup Instructions

### Backend Setup
```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables
cp .env.example .env
# Edit .env with your Neon PostgreSQL connection string and other settings

# Run the application
python -m src.main
```

### Frontend Setup
```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install
# or
yarn install

# Set environment variables
cp .env.example .env
# Edit .env with your backend API URL and other settings

# Run the development server
npm run dev
# or
yarn dev
```

## Environment Variables

### Backend (.env)
```
DATABASE_URL=your_neon_postgresql_connection_string
SECRET_KEY=your_secret_key_for_jwt_tokens
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Frontend (.env)
```
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
```

## Development

### Backend
- API documentation available at `http://localhost:8000/docs`
- Use `uvicorn src.main:app --reload` for development with auto-reload

### Frontend
- Available at `http://localhost:3000`
- Hot reloading enabled in development mode

## Project Structure

```
backend/
├── src/
│   ├── models/          # Data models (User, Todo)
│   ├── services/        # Business logic
│   ├── api/             # API route definitions
│   ├── database/        # Database configuration
│   ├── middleware/      # Authentication middleware
│   ├── utils/           # Utility functions
│   └── main.py          # Application entry point
├── tests/
└── requirements.txt

frontend/
├── src/
│   ├── components/      # React components
│   ├── pages/           # Next.js pages
│   ├── services/        # API service layer
│   ├── styles/          # CSS and styling
│   ├── utils/           # Utility functions
│   └── types/           # TypeScript type definitions
├── public/
├── package.json
└── next.config.js
```

## Architecture

The application follows a clean architecture pattern with clear separation of concerns:

- **Models**: Define data structures and validation rules
- **Services**: Contain business logic and data access operations
- **API**: Define routes and handle HTTP requests
- **Middleware**: Handle cross-cutting concerns like authentication
- **Frontend**: Handle UI rendering and user interactions

## Security

- Passwords are hashed using bcrypt
- JWT tokens for authentication
- User-specific data access enforcement
- Input validation and sanitization
- CORS configured for frontend integration

## Error Handling

- Comprehensive error responses with appropriate HTTP status codes
- User-friendly error messages
- Proper logging for debugging and monitoring
