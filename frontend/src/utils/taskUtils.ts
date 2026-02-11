import { Todo } from '../services/api';

/**
 * Determines if a task is recurring
 * @param task The task to check
 * @returns true if the task has a recurrence pattern other than 'none'
 */
export const isRecurring = (task: Todo): boolean => {
  return task.recurrence_type !== undefined && task.recurrence_type !== 'none';
};

/**
 * Determines if a task is due soon (within 24 hours)
 * @param task The task to check
 * @returns true if the task's due date is within 24 hours from now
 */
export const isDueSoon = (task: Todo): boolean => {
  if (!task.due_date) return false;
  
  const dueDate = new Date(task.due_date);
  const now = new Date();
  const twentyFourHours = 24 * 60 * 60 * 1000; // 24 hours in milliseconds
  
  return dueDate > now && dueDate <= new Date(now.getTime() + twentyFourHours);
};

/**
 * Determines if a task has a reminder set
 * @param task The task to check
 * @returns true if the task has a reminder date/time set
 */
export const hasReminder = (task: Todo): boolean => {
  return task.reminder_at !== undefined && task.reminder_at !== null && task.reminder_at !== '';
};

/**
 * Determines if a task is overdue
 * @param task The task to check
 * @returns true if the task's due date has passed
 */
export const isOverdue = (task: Todo): boolean => {
  if (!task.due_date) return false;
  
  const dueDate = new Date(task.due_date);
  const now = new Date();
  
  return dueDate < now && !task.completed;
};

/**
 * Formats a date string for display
 * @param dateString The date string to format
 * @returns Formatted date string or empty string if invalid
 */
export const formatDateForDisplay = (dateString: string | undefined): string => {
  if (!dateString) return '';
  
  try {
    const date = new Date(dateString);
    return date.toLocaleDateString();
  } catch (error) {
    console.warn('Invalid date string provided:', dateString);
    return '';
  }
};

/**
 * Validates that reminder time is not after due date
 * @param reminderDateTime The reminder date/time
 * @param dueDate The due date
 * @returns true if the reminder is valid (before or equal to due date)
 */
export const isValidReminder = (reminderDateTime: string | undefined, dueDate: string | undefined): boolean => {
  if (!reminderDateTime || !dueDate) return true; // If either is missing, consider it valid
  
  try {
    const reminder = new Date(reminderDateTime);
    const due = new Date(dueDate);
    
    return reminder <= due;
  } catch (error) {
    console.warn('Error validating reminder time:', error);
    return false;
  }
};