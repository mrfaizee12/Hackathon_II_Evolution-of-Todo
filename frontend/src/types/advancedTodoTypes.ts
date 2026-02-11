/**
 * Extended task interface with advanced features
 */
export interface Task {
  id: string;
  title: string;
  description?: string;
  completed: boolean;
  priority: 'low' | 'medium' | 'high';
  tags: string; // comma-separated tags
  created_at: string; // ISO date string
  updated_at: string; // ISO date string

  // NEW FIELDS FOR ADVANCED FEATURES
  recurrence_type?: 'none' | 'daily' | 'weekly' | 'monthly'; // Recurrence pattern if task repeats
  recurrence_interval?: number; // How often to repeat (e.g., every 2 weeks)
  due_date?: string; // ISO date string for when task is due
  reminder_at?: string; // ISO date string for when to remind user
  next_occurrence?: string; // Next occurrence for recurring tasks
  ai_generated?: boolean;
  ai_context?: string;
}

/**
 * Interface for recurrence pattern
 */
export interface RecurrencePattern {
  type: 'none' | 'daily' | 'weekly' | 'monthly';
  interval?: number; // How often to repeat (e.g., every 2 weeks)
  endDate?: string; // Optional end date for recurrence
}

/**
 * Type for recurrence options
 */
export type RecurrenceOption = 'none' | 'daily' | 'weekly' | 'monthly';

/**
 * Interface for task form state
 */
export interface TaskFormState {
  title: string;
  description: string;
  priority: 'low' | 'medium' | 'high';
  tags: string;
  recurrence_type: 'none' | 'daily' | 'weekly' | 'monthly';
  recurrence_interval: number | null;
  due_date: string; // ISO date string
  reminder_at: string; // ISO date string
  completed: boolean;
  ai_context?: string;
}