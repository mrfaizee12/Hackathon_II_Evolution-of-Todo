# Quickstart Guide: Phase II Todo Web Application

## Prerequisites

- Python 3.11+
- Node.js 18+
- npm or yarn
- TypeScript 5+
- Neon Serverless PostgreSQL account

## Setup Instructions

### 1. Clone the Repository
```bash
git clone <repository-url>
cd <repository-name>
```

### 2. Backend Setup
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
```

### 3. Frontend Setup
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
```

### 4. Database Setup
```bash
# From backend directory
python -m src.database.migrate  # Run database migrations
```

### 5. Running the Application

#### Backend:
```bash
# From backend directory
python -m src.main
```

#### Frontend:
```bash
# From frontend directory
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

## Development Commands

### Backend
```bash
# Run tests
pytest

# Format code
black src/

# Lint code
ruff check src/
```

### Frontend
```bash
# Run tests
npm test
# or
yarn test

# Format code
npx prettier --write src/

# Lint code
npx eslint src/ --fix
```

## Project Structure
```
backend/
├── src/
│   ├── models/          # Data models (User, Todo)
│   ├── services/        # Business logic
│   ├── api/             # API route definitions
│   ├── database/        # Database configuration
│   └── main.py          # Application entry point
├── tests/
│   ├── unit/
│   ├── integration/
│   └── contract/
└── requirements.txt

frontend/
├── src/
│   ├── components/      # React components
│   ├── pages/           # Next.js pages
│   ├── services/        # API service layer
│   ├── styles/          # CSS and styling
│   └── utils/           # Utility functions
├── public/
├── tests/
│   ├── unit/
│   └── integration/
├── package.json
└── next.config.js
```