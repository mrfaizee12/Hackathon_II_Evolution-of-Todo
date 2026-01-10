# Quickstart: Phase II Intermediate Todo App

## Environment Setup
1. Clone the repo and checkout `003-phase-ii-todo`.
2. Configure `.env` with:
   - `DATABASE_URL` (Neon PostgreSQL)
   - `BETTER_AUTH_SECRET`
3. Install dependencies:
   - Backend: `poetry install`
   - Frontend: `npm install`

## Running Locally
1. Start Dev Server (Backend): `uvicorn backend.src.main:app --reload`
2. Start Dev Server (Frontend): `npm run dev`

## Deployment
- Backend: Vercel or Railway (containerized or serverless functions)
- Frontend: Vercel
- DB: Neon (serverless)
