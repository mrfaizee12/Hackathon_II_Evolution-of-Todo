'use client';

import { createContext, useContext, useEffect, useReducer, ReactNode } from 'react';
import { apiService } from '../services/api';

interface AuthState {
  user: any | null;
  loading: boolean;
  isAuthenticated: boolean;
}

interface AuthAction {
  type: string;
  payload?: any;
}

const initialState: AuthState = {
  user: null,
  loading: true,
  isAuthenticated: false,
};

const AuthContext = createContext<{
  state: AuthState;
  signin: (email: string, password: string) => Promise<void>;
  signup: (email: string, password: string, name: string) => Promise<void>;
  signout: () => Promise<void>;
  checkAuthStatus: () => Promise<void>;
} | undefined>(undefined);

const authReducer = (state: AuthState, action: AuthAction): AuthState => {
  switch (action.type) {
    case 'AUTH_START':
      return { ...state, loading: true };
    case 'AUTH_SUCCESS':
      return { ...state, loading: false, isAuthenticated: true, user: action.payload };
    case 'AUTH_FAILURE':
      return { ...state, loading: false, isAuthenticated: false, user: null };
    case 'SIGNOUT':
      return { ...state, loading: false, isAuthenticated: false, user: null };
    default:
      return state;
  }
};

interface AuthProviderProps {
  children: ReactNode;
}

export const AuthProvider = ({ children }: AuthProviderProps) => {
  const [state, dispatch] = useReducer(authReducer, initialState);

  const checkAuthStatus = async () => {
    const token = apiService.getToken();
    if (!token) {
      dispatch({ type: 'AUTH_FAILURE' });
      return;
    }

    try {
      dispatch({ type: 'AUTH_START' });
      const response = await apiService.getMe();
      if (response.error) {
        dispatch({ type: 'AUTH_FAILURE' });
        return;
      }
      dispatch({ type: 'AUTH_SUCCESS', payload: response.data });
    } catch (error) {
      dispatch({ type: 'AUTH_FAILURE' });
    }
  };

  useEffect(() => {
    checkAuthStatus();
  }, []);

  const signin = async (email: string, password: string) => {
    try {
      dispatch({ type: 'AUTH_START' });
      const response = await apiService.signin(email, password);
      if (response.error) {
        dispatch({ type: 'AUTH_FAILURE' });
        throw new Error(response.error);
      }

      if (response.data && response.data.token) {
        apiService.setToken(response.data.token);
      }

      if (response.data) {
        dispatch({ type: 'AUTH_SUCCESS', payload: response.data.user });
      }
      window.location.href = '/dashboard';
    } catch (error: any) {
      dispatch({ type: 'AUTH_FAILURE' });
      throw error;
    }
  };

  const signup = async (email: string, password: string, name: string) => {
    try {
      dispatch({ type: 'AUTH_START' });
      const response = await apiService.signup(email, password, name);
      if (response.error) {
        dispatch({ type: 'AUTH_FAILURE' });
        throw new Error(response.error);
      }

      // After successful signup, immediately sign in to get the token
      const signinResponse = await apiService.signin(email, password);
      if (signinResponse.error) {
        dispatch({ type: 'AUTH_FAILURE' });
        throw new Error(signinResponse.error);
      }

      if (signinResponse.data && signinResponse.data.token) {
        apiService.setToken(signinResponse.data.token);
      }

      if (signinResponse.data) {
        dispatch({ type: 'AUTH_SUCCESS', payload: signinResponse.data.user });
      }
      window.location.href = '/dashboard';
    } catch (error: any) {
      dispatch({ type: 'AUTH_FAILURE' });
      throw error;
    }
  };

  const signout = async () => {
    try {
      await apiService.signout();
      apiService.clearToken();
      dispatch({ type: 'SIGNOUT' });
      window.location.href = '/auth/signin';
    } catch (error) {
      apiService.clearToken();
      dispatch({ type: 'SIGNOUT' });
      window.location.href = '/auth/signin';
    }
  };

  return (
    <AuthContext.Provider value={{ state, signin, signup, signout, checkAuthStatus }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};