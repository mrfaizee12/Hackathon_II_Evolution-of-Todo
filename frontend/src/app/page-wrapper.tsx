'use client';

import { AuthProvider } from '../utils/auth';
import { ReactNode } from 'react';

interface PageWrapperProps {
  children: ReactNode;
}

export default function PageWrapper({ children }: PageWrapperProps) {
  return (
    <AuthProvider>
      {children}
    </AuthProvider>
  );
}