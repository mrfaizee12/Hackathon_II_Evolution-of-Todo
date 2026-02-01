'use client';

import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import { useAuth } from '../../utils/auth';
import { apiService, Todo } from '../../services/api';
import TodoForm from '../../components/TodoForm';
import TodoItem from '../../components/TodoItem';
import TodoFilters from '../../components/TodoFilters';
import SearchBar from '../../components/SearchBar';

const DashboardPage: React.FC = () => {
  const { state, signout } = useAuth();
  const [todos, setTodos] = useState<Todo[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [editingTodo, setEditingTodo] = useState<Todo | null>(null);
  const [filters, setFilters] = useState({
    search: '',
    priority: '',
    tags: '',
    dueDateFrom: '',
    dueDateTo: '',
    completed: '',
    sort: '',
    order: '',
  });

  // Fetch todos with current filters
  useEffect(() => {
    const fetchTodos = async () => {
      setLoading(true);
      setError('');

      try {
        const response = await apiService.getTodos({
          search: filters.search || undefined,
          priority: filters.priority || undefined,
          tags: filters.tags || undefined,
          due_date_from: filters.dueDateFrom || undefined,
          due_date_to: filters.dueDateTo || undefined,
          completed: filters.completed ? filters.completed === 'true' : undefined,
          sort: filters.sort || undefined,
          order: filters.order as 'asc' | 'desc' || undefined,
        });

        if (response.error) {
          setError(response.error);
        } else {
          const todoList = Array.isArray(response.data) ? response.data : response.data?.todos;
          setTodos(todoList || []);
        }
      } catch (err: any) {
        setError(err.message || 'Error fetching todos');
      } finally {
        setLoading(false);
      }
    };

    if (state.isAuthenticated) {
      fetchTodos();
    }
  }, [state.isAuthenticated, filters]);

  // Listen for tasks updated event from the chat bot
  useEffect(() => {
    const handleTasksUpdated = (e: Event) => {
      const customEvent = e as CustomEvent<Todo[]>;
      if (customEvent.detail && Array.isArray(customEvent.detail)) {
        setTodos(customEvent.detail);
      }
    };

    window.addEventListener('tasksUpdated', handleTasksUpdated);

    // Cleanup listener on unmount
    return () => {
      window.removeEventListener('tasksUpdated', handleTasksUpdated);
    };
  }, []);

  const handleAddTodo = async (todoData: Omit<Todo, 'id' | 'created_at' | 'updated_at' | 'user_id'>) => {
    try {
      const response = await apiService.createTodo(
        todoData.title,
        todoData.description,
        todoData.priority,
        todoData.tags,
        todoData.due_date
      );
      if (response.error) {
        setError(response.error);
      } else if (response.data) {
        // Add the new todo to the list
        setTodos([...todos, response.data]);
      }
    } catch (err: any) {
      setError(err.message || 'Error adding todo');
    }
  };

  const handleUpdateTodo = async (id: string, updates: Partial<Todo>) => {
    try {
      const response = await apiService.updateTodo(id, updates);
      if (response.error) {
        setError(response.error);
      } else if (response.data) {
        // Update the todo in the list
        setTodos(todos.map(todo => todo.id === id ? response.data! : todo));
        setEditingTodo(null); // Clear editing state
      }
    } catch (err: any) {
      setError(err.message || 'Error updating todo');
    }
  };

  const handleToggleTodo = async (id: string) => {
    const todo = todos.find(t => t.id === id);
    if (todo) {
      try {
        const response = await apiService.updateTodoStatus(id, !todo.completed);
        if (response.error) {
          setError(response.error);
        } else if (response.data) {
          // Update the todo in the list
          setTodos(todos.map(todo => todo.id === id ? response.data! : todo));
        }
      } catch (err: any) {
        setError(err.message || 'Error updating todo status');
      }
    }
  };

  const handleDeleteTodo = async (id: string) => {
    try {
      const response = await apiService.deleteTodo(id);
      if (response.error) {
        setError(response.error);
      } else {
        // Remove the todo from the list
        setTodos(todos.filter(todo => todo.id !== id));
      }
    } catch (err: any) {
      setError(err.message || 'Error deleting todo');
    }
  };

  const handleEditTodo = (todo: Todo) => {
    setEditingTodo(todo);
  };

  const handleCancelEdit = () => {
    setEditingTodo(null);
  };

  const handleFilterChange = (newFilters: typeof filters) => {
    setFilters(newFilters);
  };

  const handleSearch = (query: string) => {
    setFilters(prev => ({
      ...prev,
      search: query,
    }));
  };

  // Show loading state while authentication is being checked
  if (state.loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-indigo-50 via-purple-50 to-pink-50">
        <div className="text-center p-8">
          <div className="bg-gradient-to-r from-indigo-500 to-purple-600 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-6">
            <svg className="animate-spin h-8 w-8 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
          </div>
          <h1 className="text-2xl font-bold text-gray-800 mb-2">Loading Dashboard...</h1>
          <p className="text-gray-600">Checking authentication status</p>
        </div>
      </div>
    );
  }

  // Redirect to sign in if not authenticated
  if (!state.isAuthenticated) {
    // We can't redirect here directly since Next.js router is not available
    // Instead, show a message and redirect after a delay or let the _app.tsx handle it
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-indigo-50 via-purple-50 to-pink-50">
        <div className="text-center p-8 max-w-md">
          <div className="bg-gradient-to-r from-indigo-500 to-purple-600 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-6">
            <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
            </svg>
          </div>
          <h1 className="text-2xl font-bold text-gray-800 mb-2">Please sign in to continue</h1>
          <p className="text-gray-600 mb-6">You need to be authenticated to access the dashboard</p>
          <a href="/auth/signin" className="inline-block px-6 py-3 bg-gradient-to-r from-indigo-600 to-purple-600 text-white font-semibold rounded-lg shadow-md hover:from-indigo-700 hover:to-purple-700 transition-all duration-300 transform hover:-translate-y-0.5 hover:shadow-lg">
            Go to Sign In
          </a>
        </div>
      </div>
    );
  }

  return (
    <>
      <main className="flex-1 overflow-y-auto p-4 md:p-6">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          {error && (
            <div className="mb-6 p-4 bg-red-50 text-red-700 rounded-lg border border-red-200 flex items-start">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-2 mt-0.5 flex-shrink-0" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
              </svg>
              <span>{error}</span>
            </div>
          )}

          {/* Search Bar and Filters Container */}
          <div className="flex flex-col gap-4 mb-6">
            <div className="max-w-md">
              {/* Search Bar */}
              <SearchBar onSearch={handleSearch} />
            </div>

            {/* Filters with Add Todo Button */}
            <div className="flex-1">
              <TodoFilters
                onFilterChange={handleFilterChange}
                todosCount={todos.length}
                headerButton={
                  todos.length === 0 ? (
                    <button
                      onClick={() => {
                        const element = document.getElementById('add-todo-form');
                        if (element) {
                          element.scrollIntoView({ behavior: 'smooth' });
                        }
                      }}
                      className="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors duration-300 font-medium whitespace-nowrap"
                    >
                      Create your first todo
                    </button>
                  ) : (
                    <button
                      onClick={() => {
                        const element = document.getElementById('add-todo-form');
                        if (element) {
                          element.scrollIntoView({ behavior: 'smooth' });
                        }
                      }}
                      className="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors duration-300 font-medium whitespace-nowrap"
                    >
                      Add new todo
                    </button>
                  )
                }
              />
            </div>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            {/* Left column - Add Todo or Edit Todo */}
            <div className="lg:col-span-1">
              <div id="add-todo-form" className="bg-white p-6 rounded-2xl shadow-lg border border-gray-100 hover:shadow-xl transition-shadow duration-300">
                <div className="flex items-center mb-4">
                  <div className="bg-gradient-to-r from-indigo-500 to-purple-600 w-8 h-8 rounded-lg flex items-center justify-center mr-2">
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      {editingTodo ? (
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                      ) : (
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
                      )}
                    </svg>
                  </div>
                  <h2 className="text-xl font-semibold text-gray-800">
                    {editingTodo ? 'Edit Todo' : 'Add New Todo'}
                  </h2>
                </div>
                <TodoForm
                  todo={editingTodo || undefined}
                  onSubmit={editingTodo ? (todoData) => handleUpdateTodo(editingTodo.id, todoData) : handleAddTodo}
                  onCancel={editingTodo ? handleCancelEdit : undefined}
                  onAddSuccess={() => {}}
                />
              </div>
            </div>

            {/* Right column - Todo List */}
            <div className="lg:col-span-2">
              <div className="bg-white p-6 rounded-2xl shadow-lg border border-gray-100 hover:shadow-xl transition-shadow duration-300">
                <div className="flex items-center mb-4">
                  <div className="bg-gradient-to-r from-indigo-500 to-purple-600 w-8 h-8 rounded-lg flex items-center justify-center mr-2">
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                    </svg>
                  </div>
                  <h2 className="text-xl font-semibold text-gray-800">Your Todos</h2>
                  <span className="ml-2 px-2 py-1 bg-indigo-100 text-indigo-800 text-xs font-medium rounded-full">
                    {todos.length} {todos.length === 1 ? 'item' : 'items'}
                  </span>
                </div>

                {loading ? (
                  <div className="flex justify-center items-center h-32">
                    <div className="bg-gradient-to-r from-indigo-500 to-purple-600 w-12 h-12 rounded-full flex items-center justify-center">
                      <svg className="animate-spin h-6 w-6 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                        <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                        <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                      </svg>
                    </div>
                  </div>
                ) : todos.length === 0 ? (
                  <div className="text-center py-12">
                    <div className="bg-gradient-to-r from-indigo-100 to-purple-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                      <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8 text-indigo-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                      </svg>
                    </div>
                    <p className="text-gray-500 text-lg mb-2">No todos yet</p>
                    <p className="text-gray-400">Add your first todo using the form on the left</p>
                  </div>
                ) : (
                  <div className="space-y-3">
                    {todos.map(todo => (
                      <TodoItem
                        key={todo.id}
                        todo={todo}
                        onToggle={() => handleToggleTodo(todo.id)}
                        onEdit={handleEditTodo}
                        onDelete={handleDeleteTodo}
                        onDeleteSuccess={() => {}}
                      />
                    ))}
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      </main>
    </>
  );
};

export default DashboardPage;