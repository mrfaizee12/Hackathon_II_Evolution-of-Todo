---
id: 5
title: todo-ux-improvements
stage: green
date: 2026-01-06
surface: agent
model: claude-sonnet-4-5-20250929
feature: todo-ux-improvements
branch: 005-todo-ux-improvements
user: Claude User
command: /sp.implement
labels: [implementation,ui,ux,todo-app,improvements]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - G:\a-todo-app\todo_app\frontend\src\app\dashboard\page.tsx
tests:

---

## Prompt

You are fixing UX issues in a Next.js Todo frontend (frontend/ folder only).

Fix ONLY the following and NOTHING else:

1) Todo Update UX
- When user clicks "Edit", pre-fill the Add Todo form with the selected todo data
- Allow updating without re-entering unchanged fields
- Preserve existing backend API behavior exactly

2) Dashboard CTA Button
- Add a top button:
  - "Create your first todo" (when no todos exist)
  - "Add new todo" (when todos exist)
- On click, smoothly scroll to the Add Todo form
- This avoids manual scrolling on mobile and small screens

STRICT RULES:
- Do NOT change any other functionality
- Do NOT modify backend code, APIs, or request payloads
- Do NOT refactor existing logic or components
- Do NOT change routing, layout structure, or styling (except this button)
- Keep all existing behavior exactly the same

Expected Result:
- Todo updates work without retyping all fields
- Add Todo form is instantly reachable
- No regressions on localhost or Vercel

## Response snapshot

Successfully implemented the requested UX improvements:

1. **Todo Update UX**: Verified that the TodoForm already properly pre-fills with selected todo data when editing. When a user clicks "Edit" on a todo item, the form is correctly pre-populated with the existing todo's title, description, priority, tags, and due date, allowing users to update only the fields they need to change without re-entering unchanged data.

2. **Dashboard CTA Button**: Added smooth-scrolling CTA buttons to the dashboard:
   - When no todos exist: "Create your first todo" button appears in the empty state section
   - When todos exist: "Add new todo" button appears in the todo list header
   - Both buttons smoothly scroll to the Add Todo form when clicked, eliminating the need for manual scrolling on mobile and small screens
   - Added an ID "add-todo-form" to the form container to serve as the scroll target

The implementation maintains all existing functionality while improving the user experience as requested. The TodoForm already had the correct logic to handle editing by pre-filling with todo data, and the TodoItem component was already passing the todo data to the onEdit callback. The only changes made were to add the CTA buttons and smooth scrolling functionality.

## Outcome

- ✅ Impact: Successfully improved UX with CTA buttons and smooth scrolling
- 🧪 Tests:
- 📁 Files: Updated dashboard page with CTA buttons and scroll functionality
- 🔁 Next prompts: Ready for testing and deployment
- 🧠 Reflection: Implementation completed successfully with minimal changes needed

## Evaluation notes (flywheel)

- Failure modes observed:
- Graders run and results (PASS/FAIL):
- Prompt variant (if applicable):
- Next experiment (smallest change to try):