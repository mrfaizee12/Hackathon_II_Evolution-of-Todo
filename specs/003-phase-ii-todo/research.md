# Research: Phase II Intermediate Todo App

## Decision: Full-Stack Web Architecture
**Rationale**: Aligns with Phase II constitutional requirements for a Next.js frontend and FastAPI backend.
**Alternatives considered**:
- Single-page app (React) + API: Rejected because Next.js is mandated.
- Monolithic Python app: Rejected because Next.js is mandated.

## Decision: SQLModel Extension
**Rationale**: Phase II mandates SQLModel. We will extend the existing `Todo` base model with `priority`, `tags`, and `due_date`.
**Alternatives considered**:
- Raw SQLAlchemy: Rejected because SQLModel is mandated.

## Decision: Better Auth Integration
**Rationale**: Mandated by constitution for Phase II. Provides robust signup/signin out of the box.
**Alternatives considered**:
- FastApi Users: Rejected because Better Auth is mandated.

## Decision: Query Parameter Standards
**Rationale**:
- Search: `q` parameter for keyword matching.
- Filter: `status`, `priority`, `date` (ISO range or exact).
- Sort: `sort_by` (field) and `order` (asc/desc).
**Alternatives considered**:
- GraphQL: Rejected because RESTful JSON is mandated.

## Decision: UI/UX Theme (Gradients & Animations)
**Rationale**: Tailwind CSS gradients will be used for the background and primary actions. Framer Motion (or Next.js native transitions) for subtle animations.
**Alternatives considered**:
- Standard CSS modules: Less efficient for complex gradients and animations compared to Tailwind + Framer Motion.
