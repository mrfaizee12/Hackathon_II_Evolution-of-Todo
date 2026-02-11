'use client';

import React, { useState, useEffect } from 'react';
import { Todo } from '../services/api';
import { validateAdvancedTaskFields } from '../utils/validation';
import Notification from './Notification';

interface TodoFormProps {
  todo?: Todo;
  onSubmit: (todo: Omit<Todo, 'id' | 'created_at' | 'updated_at' | 'user_id'> | Partial<Todo>) => void;
  onCancel?: () => void;
  onAddSuccess?: () => void; // Callback for successful addition
}

const TodoForm: React.FC<TodoFormProps> = ({ todo, onSubmit, onCancel, onAddSuccess }) => {
  const [title, setTitle] = useState(todo?.title || '');
  const [description, setDescription] = useState(todo?.description || '');
  const [priority, setPriority] = useState<'low' | 'medium' | 'high'>(todo?.priority || 'medium');
  const [tags, setTags] = useState(todo?.tags || '');
  const [dueDate, setDueDate] = useState(todo?.due_date || '');
  const [recurrenceType, setRecurrenceType] = useState<'none' | 'daily' | 'weekly' | 'monthly'>(todo?.recurrence_type || 'none');
  const [recurrenceInterval, setRecurrenceInterval] = useState<number>(todo?.recurrence_interval || 1);
  const [reminderAt, setReminderAt] = useState(todo?.reminder_at || '');
  const [showNotification, setShowNotification] = useState(false);
  const [notificationMessage, setNotificationMessage] = useState('');
  const [validationError, setValidationError] = useState('');

  // Sync state with todo prop when it changes (for editing)
  useEffect(() => {
    if (todo) {
      setTitle(todo.title || '');
      setDescription(todo.description || '');
      setPriority(todo.priority || 'medium');
      setTags(todo.tags || '');
      setDueDate(todo.due_date || '');
      setRecurrenceType(todo.recurrence_type || 'none');
      setRecurrenceInterval(todo.recurrence_interval || 1);
      setReminderAt(todo.reminder_at || '');
    } else {
      // Reset form when todo is null (adding new todo)
      setTitle('');
      setDescription('');
      setPriority('medium');
      setTags('');
      setDueDate('');
      setRecurrenceType('none');
      setRecurrenceInterval(1);
      setReminderAt('');
    }
  }, [todo]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    // Validate advanced fields
    const validation = validateAdvancedTaskFields(
      recurrenceType,
      recurrenceInterval,
      undefined, // recurrenceEndDate not implemented in form
      dueDate,
      reminderAt
    );

    if (!validation.allValid) {
      setValidationError('Please check your inputs. Reminder must be before due date if both are set.');
      return;
    }

    // Call the original onSubmit function
    onSubmit({
      title,
      description,
      priority,
      tags,
      due_date: dueDate || undefined,
      recurrence_type: recurrenceType,
      recurrence_interval: recurrenceType !== 'none' ? recurrenceInterval : undefined,
      reminder_at: reminderAt || undefined,
      completed: todo?.completed || false, // Keep existing completion status if editing
    });

    // Reset the form after submission (both for adding and updating)
    resetForm();

    // Show success message based on whether we're adding or updating
    if (!todo) {
      setNotificationMessage('Todo added successfully');
      // Call the success callback if provided (only for new todos)
      if (onAddSuccess) {
        onAddSuccess();
      }
    } else {
      setNotificationMessage('Todo updated successfully');
    }

    setShowNotification(true);
    setValidationError(''); // Clear any validation errors

    // If onCancel is provided (meaning we're in edit mode), call it to clear editing state
    if (onCancel && todo) {
      onCancel(); // This will clear the editing state in the parent component
    }
  };

  const resetForm = () => {
    setTitle('');
    setDescription('');
    setPriority('medium');
    setTags('');
    setDueDate('');
  };

  const handleNotificationClose = () => {
    setShowNotification(false);
  };

  return (
    <div>
      {showNotification && (
        <Notification
          message={notificationMessage}
          type="success"
          onClose={handleNotificationClose}
        />
      )}
      <form onSubmit={handleSubmit} className="mb-6 p-4 bg-white rounded-lg shadow">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Title *</label>
            <input
              type="text"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              required
              placeholder="What needs to be done?"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Priority</label>
            <select
              value={priority}
              onChange={(e) => setPriority(e.target.value as 'low' | 'medium' | 'high')}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="low">Low</option>
              <option value="medium">Medium</option>
              <option value="high">High</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Due Date</label>
            <input
              type="date"
              value={dueDate.split('T')[0]} // Format date for input
              onChange={(e) => setDueDate(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Recurrence</label>
            <select
              value={recurrenceType}
              onChange={(e) => setRecurrenceType(e.target.value as 'none' | 'daily' | 'weekly' | 'monthly')}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="none">None</option>
              <option value="daily">Daily</option>
              <option value="weekly">Weekly</option>
              <option value="monthly">Monthly</option>
            </select>
          </div>

          {recurrenceType !== 'none' && (
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Repeat Every</label>
              <input
                type="number"
                min="1"
                value={recurrenceInterval}
                onChange={(e) => setRecurrenceInterval(parseInt(e.target.value) || 1)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
          )}

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Reminder</label>
            <input
              type="datetime-local"
              value={reminderAt}
              onChange={(e) => setReminderAt(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Tags</label>
            <input
              type="text"
              value={tags}
              onChange={(e) => setTags(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="work, personal, urgent..."
            />
            <p className="mt-1 text-xs text-gray-500">Separate tags with commas</p>
          </div>
        </div>

        <div className="mt-4">
          <label className="block text-sm font-medium text-gray-700 mb-1">Description</label>
          <textarea
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            rows={3}
            placeholder="Add details..."
          />
        </div>

        {validationError && (
          <div className="mt-2 p-2 bg-red-100 text-red-700 rounded-md text-sm">
            {validationError}
          </div>
        )}
        <div className="mt-6 flex space-x-3">
          <button
            type="submit"
            className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
          >
            {todo ? 'Update Todo' : 'Add Todo'}
          </button>
          {onCancel && (
            <button
              type="button"
              onClick={onCancel}
              className="px-4 py-2 bg-gray-300 text-gray-700 rounded-md hover:bg-gray-400 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2"
            >
              Cancel
            </button>
          )}
        </div>
      </form>
    </div>
  );
};

export default TodoForm;