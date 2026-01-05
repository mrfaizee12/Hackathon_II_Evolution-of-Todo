'use client';

// API service for backend communication

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

interface ApiResponse<T> {
  data?: T;
  error?: string;
  status: number;
}

export interface Todo {
  id: string;
  title: string;
  description?: string;
  completed: boolean;
  priority: 'low' | 'medium' | 'high';
  tags: string; // comma-separated string
  due_date?: string;
  created_at: string;
  updated_at: string;
  user_id: string;
}

export interface User {
  id: string;
  email: string;
  name: string;
  created_at: string;
}

export interface AuthResponse {
  token: string;
  user: User;
}

export interface GetTodosResponse {
  todos: Todo[];
}

class ApiService {
  private token: string | null = null;

  setToken(token: string) {
    this.token = token;
    // Store token in localStorage for persistence
    localStorage.setItem('authToken', token);
  }

  getToken(): string | null {
    if (this.token) {
      return this.token;
    }
    // Retrieve token from localStorage
    return localStorage.getItem('authToken');
  }

  clearToken() {
    this.token = null;
    localStorage.removeItem('authToken');
  }

  private async request<T>(endpoint: string, options: RequestInit = {}): Promise<ApiResponse<T>> {
    const url = `${API_BASE_URL}/api/v1${endpoint}`;

    const headers = {
      'Content-Type': 'application/json',
      ...options.headers,
    };

    // Add authorization header if token exists
    const token = this.getToken();
    if (token) {
      (headers as any)['Authorization'] = `Bearer ${token}`;
    }

    try {
      const response = await fetch(url, {
        ...options,
        headers,
      });

      // For 204 No Content responses, return early with no data
      if (response.status === 204) {
        return {
          status: response.status,
        } as ApiResponse<T>;
      }

      // Check if response has content before trying to parse JSON
      const contentType = response.headers.get('content-type');
      let data: string | object | null = null;

      if (contentType && contentType.includes('application/json')) {
        data = await response.json();
      } else {
        // For other non-JSON responses, try to get text
        data = await response.text();
      }

      if (!response.ok) {
        const errorMessage = (typeof data === 'object' && data && 'detail' in data)
          ? (data as any).detail
          : `HTTP error! status: ${response.status}`;
        return {
          error: errorMessage,
          status: response.status,
        };
      }

      return {
        data: data as T,
        status: response.status,
      };
    } catch (error: any) {
      return {
        error: error.message || 'Network error occurred',
        status: 500,
      };
    }
  }

  // Authentication methods
  async signup(email: string, password: string, name: string): Promise<ApiResponse<AuthResponse>> {
    return this.request('/auth/signup', {
      method: 'POST',
      body: JSON.stringify({ email, password, name }),
    });
  }

  async signin(email: string, password: string): Promise<ApiResponse<AuthResponse>> {
    return this.request('/auth/signin', {
      method: 'POST',
      body: JSON.stringify({ email, password }),
    });
  }

  async signout(): Promise<ApiResponse<void>> {
    return this.request('/auth/signout', {
      method: 'POST',
    });
  }

  async getMe(): Promise<ApiResponse<User>> {
    return this.request('/auth/me');
  }

  // Todo methods
  async getTodos(params?: {
    search?: string;
    priority?: string;
    tags?: string;
    due_date_from?: string;
    due_date_to?: string;
    completed?: boolean;
    sort?: string;
    order?: 'asc' | 'desc';
  }): Promise<ApiResponse<{todos: Todo[]; total: number}>> {
    let endpoint = '/todos';
    if (params) {
      const queryParams = new URLSearchParams();
      Object.entries(params).forEach(([key, value]) => {
        if (value !== undefined) {
          queryParams.append(key, value.toString());
        }
      });
      const queryString = queryParams.toString();
      if (queryString) {
        endpoint += `?${queryString}`;
      }
    }
    return this.request(endpoint);
  }

  async createTodo(
    title: string,
    description?: string,
    priority: string = 'medium',
    tags: string = '', // comma-separated string
    due_date?: string
  ): Promise<ApiResponse<Todo>> {
    // Process tags to ensure they are properly formatted (comma-separated)
    let processedTags = '';
    if (tags) {
      const tagList = tags.split(',').map(tag => tag.trim()).filter(tag => tag);
      processedTags = tagList.join(',');
    }

    return this.request('/todos', {
      method: 'POST',
      body: JSON.stringify({ title, description, priority, tags: processedTags, due_date }),
    });
  }

  async updateTodo(
    id: string,
    updates: {
      title?: string;
      description?: string;
      completed?: boolean;
      priority?: string;
      tags?: string;
      due_date?: string;
    }
  ): Promise<ApiResponse<Todo>> {
    // Process tags if they are being updated to ensure they are properly formatted (comma-separated)
    const processedUpdates = { ...updates };
    if (updates.tags !== undefined) {
      if (updates.tags) {
        const tagList = updates.tags.split(',').map(tag => tag.trim()).filter(tag => tag);
        processedUpdates.tags = tagList.join(',');
      } else {
        processedUpdates.tags = '';
      }
    }

    return this.request(`/todos/${id}`, {
      method: 'PUT',
      body: JSON.stringify(processedUpdates),
    });
  }

  async deleteTodo(id: string): Promise<ApiResponse<void>> {
    return this.request(`/todos/${id}`, {
      method: 'DELETE',
    });
  }

  async updateTodoStatus(id: string, completed: boolean): Promise<ApiResponse<Todo>> {
    return this.request(`/todos/${id}/status`, {
      method: 'PATCH',
      body: JSON.stringify({ completed }),
    });
  }
}

export const apiService = new ApiService();