# Quickstart Guide: Frontend UI Upgrade

## Prerequisites

- Node.js 18+ installed
- npm or yarn package manager
- Git for version control
- Code editor with TypeScript support

## Setup Instructions

### 1. Clone the Repository
```bash
git clone <repository-url>
cd <project-directory>
```

### 2. Navigate to Frontend Directory
```bash
cd frontend
```

### 3. Install Dependencies
```bash
npm install
# OR if using yarn
yarn install
```

### 4. Install Additional Dependencies for UI Upgrade
```bash
# Framer Motion for animations
npm install framer-motion
# Lucide icons (optional as per spec)
npm install lucide-react
# Additional Tailwind plugins if needed
npm install @tailwindcss/forms @tailwindcss/typography
```

### 5. Configure Tailwind CSS
The project should already have Tailwind configured. Verify in `frontend/tailwind.config.js`:

```javascript
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      backgroundImage: {
        'gradient-radial': 'radial-gradient(var(--tw-gradient-stops))',
        'gradient-conic': 'conic-gradient(from 180deg at 50% 50%, var(--tw-gradient-stops))',
      },
      colors: {
        // Dark gradient theme colors
        'brand-dark': '#0f0f0f',
        'brand-darker': '#0a0a0a',
        'brand-red': '#dc2626',
        'brand-pink': '#db2777',
        'brand-gray': '#737373',
      }
    },
  },
  plugins: [],
}
```

### 6. Run the Development Server
```bash
npm run dev
# OR if using yarn
yarn dev
```

The application will be available at http://localhost:3000

## Development Workflow

### 1. Understanding the Structure
- `frontend/src/app/` - Main application routes and layouts
- `frontend/src/components/` - Reusable UI components
- `frontend/src/styles/` - Global styles and Tailwind configuration
- `frontend/src/lib/` - Utility functions

### 2. Component Development
1. Create new UI components in `frontend/src/components/ui/`
2. Create page-specific components in respective folders
3. Use TypeScript interfaces for component props
4. Follow Tailwind utility-first approach for styling

### 3. Animation Implementation
1. Use Framer Motion for complex animations
2. Use Tailwind transitions for simple hover/interactive states
3. Follow consistent animation durations and easing

### 4. Responsive Design
1. Implement mobile-first design approach
2. Use Tailwind's responsive prefixes (sm:, md:, lg:, xl:)
3. Test on various screen sizes

## Key Files to Modify

### Landing Page
- `frontend/src/app/page.tsx` - Main landing page
- `frontend/src/components/landing/HeroSection.tsx` - Animated hero section
- `frontend/src/components/landing/Navigation.tsx` - Header with auth buttons

### Auth Pages
- `frontend/src/app/auth/signin/page.tsx` - Sign in page
- `frontend/src/app/auth/signup/page.tsx` - Sign up page

### Dashboard
- `frontend/src/app/dashboard/page.tsx` - Dashboard page
- `frontend/src/app/dashboard/layout.tsx` - Dashboard layout with sidebar
- `frontend/src/components/ui/Sidebar.tsx` - Collapsible AI assistant sidebar

### Chat Interface
- `frontend/src/components/chat/ChatBubble.tsx` - Modern chat bubbles
- `frontend/src/components/chat/ChatInput.tsx` - Clean input area

## Testing the UI Changes

### 1. Visual Testing
- Navigate through all pages to ensure consistent design
- Test on different screen sizes (mobile, tablet, desktop)
- Verify animations work smoothly

### 2. Functional Testing
- Ensure all existing functionality still works
- Test authentication flows
- Verify AI chat interface still functions properly

### 3. Accessibility Testing
- Use keyboard navigation to ensure all elements are accessible
- Test with screen readers if possible
- Verify color contrast meets WCAG 2.1 AA standards

## Build and Production

### Build for Production
```bash
npm run build
# OR if using yarn
yarn build
```

### Run Production Build
```bash
npm start
# OR if using yarn
yarn start
```

## Troubleshooting

### Common Issues
1. **Tailwind classes not applying**: Ensure all component paths are included in `tailwind.config.js`
2. **Animations not working**: Check that Framer Motion is properly imported and used
3. **Responsive design broken**: Verify breakpoint usage and mobile-first approach

### Performance Tips
- Use React.memo() for components that rarely change
- Optimize images with Next.js Image component
- Lazy load components that aren't immediately visible