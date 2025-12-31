'use client';

// API service for backend communication

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

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
    const url = `${API_BASE_URL}${endpoint}`;

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

      // Check if response has content before trying to parse JSON
      const contentType = response.headers.get('content-type');
      let data = null;

      if (contentType && contentType.includes('application/json')) {
        data = await response.json();
      } else {
        // For non-JSON responses (like 204 No Content), just return status
        if(response.status === 204) {
          return {
            status: response.status,
          } as ApiResponse<T>;
        }
        // For other non-JSON responses, try to get text
        data = await response.text();
      }

      if (!response.ok) {
        return {
          error: (data && data.detail) ? data.detail : `HTTP error! status: ${response.status}`,
          status: response.status,
        };
      }

      return {
        data,
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
  async getTodos(): Promise<ApiResponse<GetTodosResponse>> {
    return this.request('/todos');
  }

  async createTodo(title: string, description?: string): Promise<ApiResponse<Todo>> {
    return this.request('/todos', {
      method: 'POST',
      body: JSON.stringify({ title, description }),
    });
  }

  async updateTodo(id: string, title?: string, description?: string, completed?: boolean): Promise<ApiResponse<Todo>> {
    return this.request(`/todos/${id}`, {
      method: 'PUT',
      body: JSON.stringify({ title, description, completed }),
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