# Research: Frontend UI Upgrade

## Overview
This research document addresses the technical requirements for upgrading the frontend UI of the Todo + AI Chatbot application with a modern, flagship-level design featuring a dark gradient theme.

## Design System Implementation

### Color Palette
- **Primary Background**: Dark gradient using brownish/reddish/pinkish tones
  - Base: `#1a1a1a` to `#0f0f0f` (dark foundation)
  - Accent: `#dc2626` to `#db2777` (red/pink highlights)
  - Secondary: `#737373` (gray for text and borders)

### Typography
- **Font Family**: System fonts (Inter, Roboto, or similar for readability)
- **Weights**: Regular (400), Medium (500), Semi-bold (600) for hierarchy
- **Sizes**: Responsive scaling based on screen size

### Spacing & Layout
- **Grid System**: Tailwind CSS responsive grid with 12-column layout
- **Spacing Scale**: Powers of 2 (0.25rem, 0.5rem, 1rem, 2rem, etc.)
- **Breakpoints**: Mobile-first with sm: 640px, md: 768px, lg: 1024px, xl: 1280px

## Component Architecture

### Reusable UI Components
- **Button**: Primary, secondary, and ghost variants with hover states
- **Card**: With shadow and border-radius for content containers
- **Header**: Responsive header with logo and navigation
- **Sidebar**: Collapsible component with smooth animation
- **Footer**: Consistent across all pages

### Animation Strategy
- **Framer Motion**: For entrance animations and hover effects
- **CSS Transitions**: For micro-interactions and state changes
- **Staggered Animations**: For hero section text elements

## Page-Specific Implementations

### Landing Page
- **Header**: Fixed position with logo, sign in/up buttons
- **Hero Section**: Animated text with gradient background
- **Footer**: Standard footer with links and copyright

### Auth Pages
- **Layout**: Centered card with form elements
- **Styling**: Consistent with overall theme
- **Responsiveness**: Mobile-first approach

### Dashboard
- **Layout**: Header with sign out button, collapsible sidebar
- **Sidebar**: Contains AI assistant interface
- **Content Area**: Todo list and management controls

### Chat Interface
- **Chat Bubbles**: Different styles for user vs AI messages
- **Input Area**: Clean design with proper focus states
- **Message Flow**: Smooth scrolling and loading indicators

## Technology Integration

### Next.js 16.1 Features
- **App Router**: Leverage layout and loading states
- **Image Optimization**: For any visual assets
- **Metadata API**: For SEO and social sharing

### Tailwind CSS Configuration
- **Custom Theme**: Extend default theme with brand colors
- **Plugins**:
  - `@tailwindcss/forms` for consistent form styling
  - `@tailwindcss/typography` for content styling
  - Custom plugin for gradient utilities

### Framer Motion Usage
- **Animation Variants**: Predefined sets for consistent motion
- **Transition Properties**: Smooth easing and duration
- **Gesture Handling**: Hover and tap interactions

## Responsive Design Approach

### Mobile-First Strategy
- Start with mobile styles and enhance for larger screens
- Touch-friendly targets (minimum 44px)
- Appropriate spacing for small screens

### Breakpoint Strategy
- **Mobile**: 320px - 767px (full-width layouts)
- **Tablet**: 768px - 1023px (moderate spacing)
- **Desktop**: 1024px+ (full layouts with sidebar)

## Accessibility Considerations

### WCAG 2.1 AA Compliance
- **Color Contrast**: Minimum 4.5:1 for normal text
- **Focus Indicators**: Visible for keyboard navigation
- **Semantic HTML**: Proper heading hierarchy
- **ARIA Labels**: For interactive elements

### Keyboard Navigation
- Logical tab order
- Skip links for main content
- Accessible form controls

## Performance Optimizations

### Bundle Size Management
- **Code Splitting**: Per-route basis
- **Tree Shaking**: Remove unused CSS classes
- **Image Optimization**: Next.js built-in optimization

### Animation Performance
- **GPU Acceleration**: Use transform and opacity for animations
- **Debounced Interactions**: Prevent janky animations
- **Reduced Motion**: Respect user preferences

## Existing Codebase Integration Points

### Current Frontend Structure
- Location: `frontend/src/app/` and `frontend/src/components/`
- Framework: Next.js 16.1 with App Router
- Styling: Likely existing Tailwind setup

### Integration Strategy
- Maintain existing component interfaces
- Gradually replace UI elements
- Preserve all existing functionality and behavior