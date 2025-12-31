'use client';

import '../styles/globals.css';
import type { AppProps } from 'next/app';
import { AuthProvider } from '../utils/auth';

function MyApp({ Component, pageProps }: AppProps) {
  return (
    <AuthProvider>
      <div className="bg-gradient-to-br from-indigo-50 via-purple-50 to-pink-50 min-h-screen">
        <Component {...pageProps} />
      </div>
    </AuthProvider>
  );
}

export default MyApp;