/**
 * Validates that reminder time is not after due date
 * @param reminderDateTime The reminder date/time
 * @param dueDate The due date
 * @returns true if the reminder is valid (before or equal to due date)
 */
export const validateReminderBeforeDueDate = (reminderDateTime: string | undefined, dueDate: string | undefined): boolean => {
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

/**
 * Validates recurrence interval is a positive number
 * @param interval The recurrence interval
 * @returns true if the interval is valid (positive number)
 */
export const validateRecurrenceInterval = (interval: number | null | undefined): boolean => {
  if (interval === null || interval === undefined) return true; // Consider null/undefined as valid (not set)
  
  return typeof interval === 'number' && interval > 0;
};

/**
 * Validates that recurrence end date is after current date
 * @param endDate The end date for recurrence
 * @returns true if the end date is valid (after current date)
 */
export const validateRecurrenceEndDate = (endDate: string | undefined): boolean => {
  if (!endDate) return true; // If not set, consider it valid
  
  try {
    const end = new Date(endDate);
    const now = new Date();
    
    return end > now;
  } catch (error) {
    console.warn('Error validating recurrence end date:', error);
    return false;
  }
};

/**
 * Validates that due date is not in the past (for new tasks)
 * @param dueDate The due date
 * @returns true if the due date is valid (today or in the future)
 */
export const validateDueDateNotInPast = (dueDate: string | undefined): boolean => {
  if (!dueDate) return true; // If not set, consider it valid
  
  try {
    const due = new Date(dueDate);
    const now = new Date();
    // Set time to end of day for comparison to allow same-day due dates
    const todayEnd = new Date(now.getFullYear(), now.getMonth(), now.getDate(), 23, 59, 59, 999);
    
    return due >= todayEnd;
  } catch (error) {
    console.warn('Error validating due date:', error);
    return false;
  }
};

/**
 * Validates that reminder date is not in the past
 * @param reminderDateTime The reminder date/time
 * @returns true if the reminder date/time is valid (now or in the future)
 */
export const validateReminderNotInPast = (reminderDateTime: string | undefined): boolean => {
  if (!reminderDateTime) return true; // If not set, consider it valid
  
  try {
    const reminder = new Date(reminderDateTime);
    const now = new Date();
    
    return reminder >= now;
  } catch (error) {
    console.warn('Error validating reminder date:', error);
    return false;
  }
};

/**
 * Validates all advanced task fields together
 * @param recurrenceType The recurrence type
 * @param recurrenceInterval The recurrence interval
 * @param recurrenceEndDate The recurrence end date
 * @param dueDate The due date
 * @param reminderDateTime The reminder date/time
 * @returns Object with validation results for each field
 */
export const validateAdvancedTaskFields = (
  recurrenceType?: string,
  recurrenceInterval?: number | null,
  recurrenceEndDate?: string,
  dueDate?: string,
  reminderDateTime?: string
) => {
  return {
    recurrenceIntervalValid: validateRecurrenceInterval(recurrenceInterval),
    recurrenceEndDateValid: validateRecurrenceEndDate(recurrenceEndDate),
    dueDateValid: validateDueDateNotInPast(dueDate),
    reminderValid: validateReminderNotInPast(reminderDateTime),
    reminderBeforeDueDateValid: validateReminderBeforeDueDate(reminderDateTime, dueDate),
    allValid: 
      validateRecurrenceInterval(recurrenceInterval) &&
      validateRecurrenceEndDate(recurrenceEndDate) &&
      validateDueDateNotInPast(dueDate) &&
      validateReminderNotInPast(reminderDateTime) &&
      validateReminderBeforeDueDate(reminderDateTime, dueDate)
  };
};