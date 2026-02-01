import { ClassValue, clsx } from "clsx";
import { twMerge } from "tailwind-merge";

// Utility function to merge class names with Tailwind CSS
export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

// Breakpoint constants for responsive design
export const BREAKPOINTS = {
  xs: 475,
  sm: 640,
  md: 768,
  lg: 1024,
  xl: 1280,
  '2xl': 1536,
} as const;

// Helper function to check if screen matches a breakpoint
export function useBreakpoint(breakpoint: keyof typeof BREAKPOINTS): boolean {
  if (typeof window !== 'undefined') {
    return window.matchMedia(`(min-width: ${BREAKPOINTS[breakpoint]}px)`).matches;
  }
  return false;
}

// Animation variants for Framer Motion
export const fadeInVariant = {
  hidden: { opacity: 0 },
  visible: { opacity: 1, transition: { duration: 0.5 } },
};

export const slideInFromLeftVariant = {
  hidden: { x: -100, opacity: 0 },
  visible: { x: 0, opacity: 1, transition: { duration: 0.5 } },
};

export const slideInFromRightVariant = {
  hidden: { x: 100, opacity: 0 },
  visible: { x: 0, opacity: 1, transition: { duration: 0.5 } },
};

export const sidebarVariants = {
  open: {
    x: 0,
    transition: {
      type: "spring",
      damping: 25,
      stiffness: 200,
      duration: 0.3
    }
  },
  closed: {
    x: "-100%",
    transition: {
      type: "spring",
      damping: 25,
      stiffness: 200,
      duration: 0.3
    }
  },
};

export const containerVariants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.1
    }
  }
};

export const itemVariants = {
  hidden: { y: 20, opacity: 0 },
  visible: {
    y: 0,
    opacity: 1
  }
};