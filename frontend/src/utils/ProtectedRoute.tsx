'use client';

import React, { ReactNode } from 'react';
import { useRouter } from 'next/router';
import { useAuth } from './auth';

interface ProtectedRouteProps {
  children: ReactNode;
  fallback?: ReactNode;
}

const ProtectedRoute: React.FC<ProtectedRouteProps> = ({ children, fallback = null }) => {
  const { state } = useAuth();
  const router = useRouter();

  // Show fallback while checking authentication
  if (state.loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-indigo-100">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-indigo-500 mx-auto mb-4"></div>
          <h1 className="text-2xl font-bold text-gray-800 mb-2">Loading...</h1>
          <p className="text-gray-600">Checking authentication status</p>
        </div>
      </div>
    );
  }

  // Redirect to sign in if not authenticated
  if (!state.isAuthenticated) {
    if (typeof window !== 'undefined') {
      router.push('/signin');
    }
    return fallback;
  }

  // Render children if authenticated
  return <>{children}</>;
};

export default ProtectedRoute;