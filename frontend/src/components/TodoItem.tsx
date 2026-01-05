'use client';

import React from 'react';
import { Todo } from '../services/api';

interface TodoItemProps {
  todo: Todo;
  onToggle: (id: string) => void;
  onEdit: (todo: Todo) => void;
  onDelete: (id: string) => void;
}

const TodoItem: React.FC<TodoItemProps> = ({ todo, onToggle, onEdit, onDelete }) => {
  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString();
  };

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'high':
        return 'bg-red-100 text-red-800';
      case 'medium':
        return 'bg-yellow-100 text-yellow-800';
      case 'low':
        return 'bg-green-100 text-green-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const isOverdue = todo.due_date && new Date(todo.due_date) < new Date() && !todo.completed;

  return (
    <div className={`p-4 mb-3 rounded-lg shadow-sm border-l-4 ${
      todo.completed
        ? 'bg-gray-50 border-gray-300'
        : isOverdue
          ? 'bg-red-50 border-red-500'
          : 'bg-white border-blue-500'
    }`}>
      <div className="flex items-start">
        <input
          type="checkbox"
          checked={todo.completed}
          onChange={() => onToggle(todo.id)}
          className="mt-1 h-5 w-5 text-blue-600 rounded focus:ring-blue-500"
        />

        <div className="ml-3 flex-1 min-w-0">
          <div className="flex items-center justify-between">
            <h3 className={`text-lg font-medium ${
              todo.completed ? 'line-through text-gray-500' : 'text-gray-900'
            }`}>
              {todo.title}
            </h3>

            <div className="flex space-x-2">
              <span className={`px-2 py-1 text-xs font-medium rounded-full ${getPriorityColor(todo.priority)}`}>
                {todo.priority}
              </span>

              <button
                onClick={() => onEdit(todo)}
                className="text-blue-600 hover:text-blue-900 text-sm font-medium"
              >
                Edit
              </button>

              <button
                onClick={() => onDelete(todo.id)}
                className="text-red-600 hover:text-red-900 text-sm font-medium"
              >
                Delete
              </button>
            </div>
          </div>

          {todo.description && (
            <p className={`mt-1 text-sm ${
              todo.completed ? 'text-gray-400' : 'text-gray-600'
            }`}>
              {todo.description}
            </p>
          )}

          <div className="mt-2 flex flex-wrap gap-2">
            {todo.tags && (
              <div className="flex flex-wrap gap-1">
                {todo.tags.split(',').map((tag, index) => (
                  <span
                    key={index}
                    className="px-2 py-1 text-xs bg-blue-100 text-blue-800 rounded-full"
                  >
                    {tag.trim()}
                  </span>
                ))}
              </div>
            )}

            {todo.due_date && (
              <div className={`text-xs px-2 py-1 rounded-full ${
                isOverdue
                  ? 'bg-red-100 text-red-800'
                  : 'bg-gray-100 text-gray-800'
              }`}>
                Due: {formatDate(todo.due_date)}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default TodoItem;