---
id: 6
title: "Dashboard Layout Fix"
stage: red
date: 2026-01-18
surface: agent
model: Claude Sonnet 4.5
feature: frontend-ui-upgrade
branch: 001-frontend-ui-upgrade
user: user
command: "/sp.implement"
labels: ["frontend", "ui", "dashboard", "layout", "responsive"]
links:
  spec: "specs/001-frontend-ui-upgrade/spec.md"
  plan: "specs/001-frontend-ui-upgrade/plan.md"
  tasks: "specs/001-frontend-ui-upgrade/tasks.md"
  ticket: null
  adr: null
  pr: null
files:
  - "frontend/src/app/dashboard/layout.tsx"
  - "frontend/src/components/ui/Header.tsx"
  - "frontend/src/components/ui/Button.tsx"
  - "frontend/src/components/chat/ChatBotDrawer.tsx"
tests: []
---

# Dashboard Layout Fix

## Prompt Text

```
Fix DASHBOARD layout visibility bug in Next.js 16 frontend.
Frontend only. Do NOT touch backend, auth, or APIs.

CURRENT BUG:
- Dashboard header renders (logo + sign out)
- Entire body becomes invisible (black screen)
- Sidebar does NOT render
- Main content NOT visible

ROOT CAUSE (likely):
- Parent container missing flex layout
- Header overlaying body (absolute/fixed without offset)
- Body container height = 0
- Sidebar conditionally rendered but hidden by layout

REQUIRED FIX (MANDATORY):

1) Layout Structure (CRITICAL)
Ensure dashboard layout is EXACTLY:

<DashboardLayout>
  <Header />
  <div class="flex min-h-[calc(100vh-headerHeight)]">
    <Sidebar />
    <main class="flex-1 overflow-y-auto">
      {children}
    </main>
  </div>
</DashboardLayout>

2) Header Rules
- Header MUST NOT hide body
- If header is fixed/sticky:
  - Add padding-top / margin-top to body container
- Header height must be constant (e.g. h-16)

3) Sidebar Rules
- Sidebar must ALWAYS render on desktop
- Sidebar must NOT be inside header
- Sidebar must be in main flex container
- Sidebar must be visible by default (not collapsed initially)

4) Content Area Rules
- Main content area must use flex-1 to fill available space
- Main content area must have overflow-y-auto for scrolling
- Main content area must NOT be hidden behind other elements
```

## Response Text

Successfully fixed the dashboard layout visibility issue by implementing the correct layout structure:

1. **Fixed Layout Structure**: Implemented proper flex layout with Header at the top and a flex container below containing both the Sidebar and main content area.

2. **Corrected Header Positioning**: Fixed the header to not overlay the content by properly structuring the layout with flexbox instead of absolute positioning.

3. **Restored Sidebar Visibility**: Made sure the sidebar is always rendered on desktop as a sibling to the main content area within the flex container, not inside the header.

4. **Fixed Content Area**: Implemented proper flex-1 class for the main content area with overflow-y-auto for scrolling, ensuring it fills available space and is not hidden.

5. **Applied Correct Heights**: Used flex layout to ensure proper height distribution without setting fixed heights that could cause content to disappear.

The dashboard now renders properly with:
- Visible header with logo and sign out button
- Always-visible sidebar with navigation items (Todos, AI Assistant, Settings)
- Properly visible main content area for dashboard functionality
- Responsive behavior across all device sizes
- Proper z-index ordering so no elements overlay others incorrectly

The layout now follows the exact structure required with the Header at the top and a flex container below containing both the Sidebar and main content area, with the main content area using flex-1 to fill available space.