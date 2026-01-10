# Tasks: Phase II Intermediate Todo App

**Input**: Design documents from `/specs/003-phase-ii-todo/`
**Prerequisites**: plan.md, spec.md, data-model.md, contracts/

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel
- **[Story]**: [US1] Authentication, [US2] Advanced Creation, [US3] Search/Filter/Sort

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 Create project structure for `backend/` and `frontend/` per plan.md
- [ ] T002 Initialize FastAPI backend with SQLModel and Better Auth dependencies in `backend/`
- [ ] T003 [P] Initialize Next.js frontend with Tailwind CSS and TypeScript in `frontend/`
- [ ] T004 [P] Configure linting (Ruff for backend, ESLint for frontend) in respective directories

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before user stories

- [ ] T005 [P] Setup Neon PostgreSQL database schema and migrations framework for the extended Todo model in `backend/src/models/`
- [ ] T006 Implement Better Auth signup/signin logic and session management in `backend/src/api/auth.py`
- [ ] T007 Configure generic error handling and RESTful JSON response middleware in `backend/src/main.py`
- [ ] T008 [P] Setup base API client and authentication hooks in `frontend/src/services/api.ts`

## Phase 3: User Story 1 - User Authentication (Priority: P1) 🎯 MVP

**Goal**: Enable users to sign up and sign in securely

- [ ] T009 [P] [US1] Create Landing Page with hero section and footer branding in `frontend/src/pages/index.tsx`
- [ ] T010 [US1] Implement Signup page with validation in `frontend/src/pages/signup.tsx`
- [ ] T011 [US1] Implement Signin page with validation in `frontend/src/pages/signin.tsx`
- [ ] T012 [US1] Verify auth-protected routes redirect correctly to signin in `frontend/src/middleware/auth.ts`

**Checkpoint**: Users can now register, log in, and see a basic authenticated layout.

## Phase 4: User Story 2 - Advanced Todo Creation (Priority: P1)

**Goal**: Create todos with priority, tags, and due dates

- [ ] T013 [P] [US2] Extend Todo SQLModel with `priority`, `tags`, and `due_date` in `backend/src/models/todo.py`
- [ ] T014 [US2] Update POST `/todos` and PATCH `/todos/{id}` endpoints to handle new fields in `backend/src/api/todos.py`
- [ ] T015 [US2] Add input validation for enum priorities and ISO dates in `backend/src/services/todo_service.py`
- [ ] T016 [US2] Enhance "Add Todo" form UI with priority and tag selection in `frontend/src/components/TodoForm.tsx`
- [ ] T017 [US2] Enhance "Edit Todo" modal with priority and tag selection in `frontend/src/components/EditTodoModal.tsx`

**Checkpoint**: Users can create and edit tasks with intermediate-level metadata.

## Phase 5: User Story 3 - Search, Filter, and Sort (Priority: P2)

**Goal**: Find and organize tasks efficiently

- [ ] T018 [US3] Implement search query support (`q` param) in `backend/src/api/todos.py`
- [ ] T019 [US3] Implement filter logic for `status`, `priority`, and `date` in `backend/src/services/todo_service.py`
- [ ] T020 [US3] Implement sorting logic for `due_date`, `priority`, and `title` in `backend/src/api/todos.py`
- [ ] T021 [P] [US3] Add search bar UI to the dashboard in `frontend/src/components/SearchBar.tsx`
- [ ] T022 [P] [US3] Add filter dropdowns (priority, status) to the dashboard in `frontend/src/components/FilterControls.tsx`
- [ ] T023 [P] [US3] Add sort controls (priority, due date) in `frontend/src/components/SortControls.tsx`
- [ ] T024 [US3] Connect frontend controls to backend API query parameters in `frontend/src/pages/dashboard.tsx`

**Checkpoint**: The dashboard is now fully functional with organization and search capabilities.

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Finalizing the Phase II experience

- [ ] T025 [P] Verify responsive behavior across mobile, tablet, and desktop in `frontend/`
- [ ] T026 Apply gradient-based theme and Framer Motion animations to all pages/components in `frontend/src/styles/`
- [ ] T027 Regression testing of Phase I basic features (CRUD) to ensure no breakage
- [ ] T028 Validate all API endpoints return semantic HTTP status codes per success criteria

## Dependencies & Execution Order

1. **Setup (Phase 1)** -> **Foundational (Phase 2)**: Mandatory start.
2. **User Story 1 (P1)**: Prerequisite for accessing the dashboard.
3. **User Story 2 (P1)**: Can run after US1.
4. **User Story 3 (P2)**: Depends on US2 fields (priority, tags) being available.
5. **Polish (Phase 6)**: Final step.

## Implementation Strategy

- **MVP First**: Complete US1 and US2 (Auth + Advanced Creation) to deliver a viable multi-user tool.
- **Incremental Delivery**: Add US3 (Search/Filter/Sort) last to optimize large task lists.
- **Parallelization**: Frontend UI tasks (T021-T023) can run in parallel with Backend logic (T018-T020).
