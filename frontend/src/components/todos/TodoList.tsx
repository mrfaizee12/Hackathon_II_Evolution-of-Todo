'use client';

import React, { useState } from 'react';
import EditTodo from './EditTodo';
import Notification from '../Notification';
import { Todo } from '../../services/api';
import { isRecurring, isDueSoon, hasReminder, isOverdue, formatDateForDisplay } from '../../utils/taskUtils';

interface TodoListProps {
  todos: Todo[];
  onUpdateTodo: (id: string, updates: { title?: string; description?: string; completed?: boolean }) => void;
  onToggleTodo: (id: string, completed: boolean) => void;
  onDeleteTodo: (id: string) => void;
  onDeleteSuccess?: () => void; // Callback for successful deletion
}

const TodoList: React.FC<TodoListProps> = ({ todos, onUpdateTodo, onToggleTodo, onDeleteTodo, onDeleteSuccess }) => {
  const [editingTodoId, setEditingTodoId] = useState<string | null>(null);
  const [newTitle, setNewTitle] = useState('');
  const [newDescription, setNewDescription] = useState('');
  const [showNotification, setShowNotification] = useState(false);
  const [notificationMessage, setNotificationMessage] = useState('');

  const handleEdit = (todo: Todo) => {
    setEditingTodoId(todo.id);
    setNewTitle(todo.title);
    setNewDescription(todo.description || '');
  };

  const handleSave = (id: string) => {
    onUpdateTodo(id, { title: newTitle, description: newDescription });
    setEditingTodoId(null);
  };

  const handleCancel = () => {
    setEditingTodoId(null);
  };

  const handleDelete = (id: string) => {
    // Call the original delete function
    onDeleteTodo(id);

    // Show success notification
    setNotificationMessage('Todo deleted successfully');
    setShowNotification(true);

    // Call the success callback if provided
    if (onDeleteSuccess) {
      onDeleteSuccess();
    }
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
      <div className="space-y-4">
        {todos.map((todo) => (
          <div
            key={todo.id}
            className={`p-5 rounded-xl border ${
              todo.completed
                ? 'bg-gradient-to-r from-green-50 to-emerald-50 border-green-200'
                : 'bg-white border-gray-200'
            } shadow-md transition-all duration-300 hover:shadow-lg transform hover:-translate-y-0.5`}
          >
            {editingTodoId === todo.id ? (
              <EditTodo
                title={newTitle}
                description={newDescription}
                onTitleChange={setNewTitle}
                onDescriptionChange={setNewDescription}
                onSave={() => handleSave(todo.id)}
                onCancel={handleCancel}
              />
            ) : (
              <div className="flex items-start">
                <input
                  type="checkbox"
                  checked={todo.completed}
                  onChange={(e) => onToggleTodo(todo.id, e.target.checked)}
                  className="mt-1 h-6 w-6 text-indigo-600 rounded focus:ring-indigo-500 focus:ring-2"
                />
                <div className="ml-4 flex-1">
                  <h3
                    className={`text-lg font-semibold ${
                      todo.completed ? 'line-through text-gray-500' : 'text-gray-800'
                    }`}
                  >
                    {todo.title}
                  </h3>
                  {todo.description && (
                    <p className={`mt-2 ${todo.completed ? 'text-gray-400' : 'text-gray-600'}`}>
                      {todo.description}
                    </p>
                  )}
                  <div className="flex flex-wrap items-center gap-2 mt-3">
                    <div className="flex items-center text-xs text-gray-500">
                      <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                      </svg>
                      <span>Created: {new Date(todo.created_at).toLocaleString()}</span>
                    </div>
                    
                    {/* Badges for advanced features */}
                    <div className="flex flex-wrap gap-1 mt-1">
                      {isRecurring(todo) && (
                        <span className="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-purple-100 text-purple-800">
                          🔁 Recurring
                        </span>
                      )}
                      
                      {todo.due_date && (
                        <span className={`inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium ${
                          isOverdue(todo) ? 'bg-red-100 text-red-800' : 
                          isDueSoon(todo) ? 'bg-yellow-100 text-yellow-800' : 'bg-blue-100 text-blue-800'
                        }`}>
                          📅 {isOverdue(todo) ? 'Overdue' : isDueSoon(todo) ? 'Due Soon' : `Due: ${formatDateForDisplay(todo.due_date)}`}
                        </span>
                      )}
                      
                      {hasReminder(todo) && (
                        <span className="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-teal-100 text-teal-800">
                          🔔 Reminder Set
                        </span>
                      )}
                    </div>
                  </div>
                </div>
                <div className="flex space-x-2 ml-4">
                  <button
                    onClick={() => handleEdit(todo)}
                    className="p-2 bg-indigo-100 text-indigo-700 rounded-lg hover:bg-indigo-200 transition duration-300 hover:shadow-sm"
                    title="Edit todo"
                  >
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                    </svg>
                  </button>
                  <button
                    onClick={() => handleDelete(todo.id)}
                    className="p-2 bg-red-100 text-red-700 rounded-lg hover:bg-red-200 transition duration-300 hover:shadow-sm"
                    title="Delete todo"
                  >
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                    </svg>
                  </button>
                </div>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};

export default TodoList;