# Tasks: AI Todo Chatbot - MCP Server and OpenRouter Integration

## Overview
Implementation of MCP Server and OpenRouter integration for AI Todo Chatbot. This document breaks down the approved implementation plan into atomic, actionable tasks organized by user story priority.

## Dependencies
- Setup (Phase 1) must complete before any User Story can begin
- User Story 1 (P1) must complete before User Story 2 (P2) can begin effectively
- User Story 2 (P2) must complete before User Story 3 (P2) can begin effectively

## Parallel Execution Examples
- T001 [P] and T002 [P] can run in parallel (different file types)
- T007 [P] [US1] and T008 [P] [US1] can run in parallel (different components)
- T015 [P] [US2] and T016 [P] [US2] can run in parallel (different tools)

## Implementation Strategy
Start with User Story 1 (MCP Server Integration) as the MVP, which includes the core MCP server, basic tool registration, and OpenRouter integration. Subsequent stories build upon this foundation with enhanced functionality and stateless operation.

---

## Phase 1: Setup Tasks

- [ ] T001 [P] Update backend/requirements.txt to include 'mcp' (Official SDK) and 'openai' libraries
- [ ] T002 [P] Create backend/src/models/conversation.py with AIConversation SQLModel class
- [ ] T003 [P] Create backend/src/models/message.py with AIMessage SQLModel class
- [ ] T004 [P] Create backend/src/services/openrouter_service.py skeleton
- [ ] T005 [P] Create backend/src/services/mcp_tool_server.py skeleton
- [ ] T006 Update backend/src/tools/todo_tools.py to include MCP-compatible function signatures

## Phase 2: Foundational Tasks

- [ ] T007 Implement AIConversation SQLModel with all fields and relationships in backend/src/models/conversation.py
- [ ] T008 Implement AIMessage SQLModel with all fields and relationships in backend/src/models/message.py
- [ ] T009 Create TodoAction SQLModel class in backend/src/models/todo_action.py
- [ ] T010 Update existing Todo model in backend/src/models/todo.py with AI-specific fields
- [ ] T011 Create database migration script for new AI models in backend/src/database/migrations/
- [ ] T012 Initialize MCP server instance in backend/src/services/mcp_tool_server.py
- [ ] T013 Implement OpenRouter API client in backend/src/services/openrouter_service.py
- [ ] T014 Register 5 MCP tools (add_task, list_tasks, complete_task, delete_task, update_task) in MCP server

## Phase 3: User Story 1 - MCP Server Integration (P1)

**Goal**: System operates as an MCP server that exposes 5 standardized tools for AI consumption.

**Independent Test**: Can be tested by making direct calls to the MCP server endpoints and verifying that all 5 tools are properly registered and accessible.

**Implementation Tasks**:

- [ ] T015 [P] [US1] Implement add_task MCP tool with proper schema and database integration
- [ ] T016 [P] [US1] Implement list_tasks MCP tool with proper schema and database integration
- [ ] T017 [US1] Implement complete_task MCP tool with proper schema and database integration
- [ ] T018 [US1] Implement delete_task MCP tool with proper schema and database integration
- [ ] T019 [US1] Implement update_task MCP tool with proper schema and database integration
- [ ] T020 [US1] Update chat_router.py to use MCP server for processing user requests
- [ ] T021 [US1] Implement basic chat loop in OpenRouterService for tool calling
- [ ] T022 [US1] Test "Add a task to buy groceries" scenario works with add_task tool
- [ ] T023 [US1] Test "Show me my pending tasks" scenario works with list_tasks tool
- [ ] T024 [US1] Test "Complete the project proposal task" scenario works with complete_task tool

## Phase 4: User Story 2 - OpenRouter Integration (P1)

**Goal**: System integrates with OpenRouter API using OpenAI Agents SDK pattern for natural language processing.

**Independent Test**: Can be tested by sending various natural language commands to the AI and verifying that appropriate MCP tools are called.

**Implementation Tasks**:

- [ ] T025 [P] [US2] Implement OpenAI Agents SDK pattern in OpenRouterService
- [ ] T026 [P] [US2] Configure OpenRouter API with specified model and base URL (constitutions)
- [ ] T027 [US2] Implement robust tool execution loops in OpenRouterService
- [ ] T028 [US2] Add proper authentication and authorization for all operations (FR-025)
- [ ] T029 [US2] Test "Add a task to buy milk" scenario calls add_task tool (SC-004)
- [ ] T030 [US2] Test "Show all my tasks" scenario calls list_tasks tool (SC-004)
- [ ] T031 [US2] Test "Delete the third task" scenario calls delete_task tool (SC-004)
- [ ] T032 [US2] Measure AI response time under 5 seconds p95 latency (SC-006)
- [ ] T033 [US2] Verify 90% accuracy in processing natural language commands (SC-004)

## Phase 5: User Story 3 - Stateless Operation (P2)

**Goal**: System maintains 100% statelessness by fetching conversation history from Neon DB on every request.

**Independent Test**: Can be verified by checking that no session state is maintained between requests and all data is retrieved from the database for each operation.

**Implementation Tasks**:

- [ ] T034 [US3] Remove any remaining in-memory session storage from chat_router.py
- [ ] T035 [US3] Implement conversation history fetching from database in each request
- [ ] T036 [US3] Update OpenRouterService to fetch user context from DB on each request
- [ ] T037 [US3] Ensure no session state is maintained between requests (FR-004, FR-005)
- [ ] T038 [US3] Test that all data is fetched from Neon DB rather than in-memory storage (SC-002)
- [ ] T039 [US3] Verify concurrent requests fetch data independently without conflicts (SC-011)
- [ ] T040 [US3] Measure performance to ensure DB fetches complete under 2 seconds (SC-003)

## Phase 6: Polish & Cross-Cutting Concerns

- [ ] T041 [P] Store all conversation history and messages in database (FR-017)
- [ ] T042 [P] Ensure all user identity information requests work through tools (FR-015)
- [ ] T043 [P] Add polite acknowledgment messages from AI for all actions (FR-016)
- [ ] T044 [P] Implement proper loading and typing states during AI processing (FR-022)
- [ ] T045 [P] Update frontend dashboard to include AI Assistant sidebar item (FR-018, FR-019)
- [ ] T046 [P] Ensure AI chat interface is responsive and works on mobile (FR-021)
- [ ] T047 [P] Verify existing Phase II functionality remains unchanged (FR-020)
- [ ] T048 [P] Clean up any old broken code or unused imports from previous attempts
- [ ] T049 [P] Add comprehensive error handling for MCP server unavailability (edge case)
- [ ] T050 [P] Add graceful handling for AI service unavailability (edge case)
- [ ] T051 [P] Add database connection limiting and queuing for concurrent requests (edge case)
- [ ] T052 [P] Final integration test ensuring all user stories work together seamlessly

## Dependencies & Execution Order

### Phase Dependencies
- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies
- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P1)**: Can start after Foundational (Phase 2) - May integrate with US1 but should be independently testable
- **User Story 3 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1/US2 but should be independently testable

### Within Each User Story
- Tests (if included) MUST be written and FAIL before implementation
- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities
- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- All tests for a user story marked [P] can run in parallel
- Models within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

### Parallel Example: User Story 1
```bash
# Launch all tools for User Story 1 together:
Task: "Implement add_task MCP tool with proper schema and database integration"
Task: "Implement list_tasks MCP tool with proper schema and database integration"
Task: "Implement complete_task MCP tool with proper schema and database integration"
Task: "Implement delete_task MCP tool with proper schema and database integration"
Task: "Implement update_task MCP tool with proper schema and database integration"
```

## Implementation Strategy

### MVP First (User Story 1 Only)
1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery
1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Each story adds value without breaking previous stories

### Parallel Team Strategy
With multiple developers:
1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
3. Stories complete and integrate independently

## Notes
- [P] tasks = different files, no dependencies
- [US#] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence