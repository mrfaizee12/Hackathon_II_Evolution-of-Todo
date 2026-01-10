# Quickstart: Next.js 14+ to 16+ Upgrade

## Prerequisites
- Node.js 18+ installed
- npm or yarn package manager
- Access to the project repository

## Setup Instructions

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd todo_app0
   ```

2. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

3. Install dependencies:
   ```bash
   npm install
   ```

4. For the Next.js upgrade, update the dependencies:
   ```bash
   npm install next@latest react@latest react-dom@latest
   ```

5. Start the development server:
   ```bash
   npm run dev
   ```

## Development Commands
- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run start` - Start production server
- `npm run lint` - Run linter

## Configuration Files
- `next.config.js` - Next.js configuration
- `tsconfig.json` - TypeScript configuration
- `.env` - Environment variables

## Troubleshooting
- If build fails after upgrade, check for breaking changes in Next.js documentation
- Verify all dependencies are compatible with Next.js 16
- Ensure API endpoints remain unchanged during upgrade