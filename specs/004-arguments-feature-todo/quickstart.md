# Quickstart: Todo UX Feedback, Form Reset & Dark Gradient UI

## Development Setup

### Prerequisites
- Node.js 18+
- Python 3.11+
- UV package manager
- npm or pnpm

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd todo_app
   ```

2. **Install backend dependencies**
   ```bash
   cd backend
   uv venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   uv pip install -r requirements.txt
   ```

3. **Install frontend dependencies**
   ```bash
   cd frontend
   npm install
   # or
   pnpm install
   ```

### Environment Setup

1. **Backend Environment**
   ```bash
   cd backend
   cp .env.example .env
   # Update environment variables in .env file
   ```

2. **Frontend Environment**
   ```bash
   cd frontend
   cp .env.example .env
   # Update environment variables in .env file
   ```

## Running the Application

### Development Mode

**Backend:**
```bash
cd backend
uv run python -m src.main
```

**Frontend:**
```bash
cd frontend
npm run dev
# or
pnpm dev
```

### Building for Production

**Frontend:**
```bash
cd frontend
npm run build
# or
pnpm build
```

## Feature Implementation

### Dark Gradient Background
- Located in `frontend/src/styles/globals.css` and `frontend/src/app/layout.tsx`
- Implemented with Tailwind CSS classes
- Uses radial gradient with deep black edges and purple/blue/teal blend

### Form Reset Functionality
- Implemented in `frontend/src/components/TodoForm.tsx`
- Form state automatically resets after successful todo creation
- Uses React state management to clear form fields

### Success Notifications
- New component: `frontend/src/components/Notification.tsx`
- Toast-style notifications for add/delete operations
- Auto-dismiss after 3 seconds
- Accessible and WCAG compliant

## Testing

### Frontend Tests
```bash
cd frontend
npm run test
# or
pnpm test
```

### Backend Tests
```bash
cd backend
pytest
```

## Key Files for This Feature

- `frontend/src/styles/globals.css` - Global gradient styles
- `frontend/src/app/layout.tsx` - Layout with gradient background
- `frontend/src/components/TodoForm.tsx` - Form with reset functionality
- `frontend/src/components/Notification.tsx` - Success notification component
- `frontend/src/components/TodoList.tsx` - Delete success notifications