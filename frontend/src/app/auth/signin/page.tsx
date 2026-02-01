'use client';

import React from 'react';
import Link from 'next/link';
import { AuthForm } from '@/components/auth/AuthForm';
import { Button } from '@/components/ui/Button';
import { useAuth } from '../../../utils/auth';
import { useRouter } from 'next/navigation';
import { motion } from 'framer-motion';

const SigninPage: React.FC = () => {
  const { signin } = useAuth();
  const router = useRouter();
  const [isLoading, setIsLoading] = React.useState(false);
  const [error, setError] = React.useState<string | null>(null);

  const handleSignIn = async (formData: { email: string; password: string }) => {
    setIsLoading(true);
    setError(null);

    try {
      await signin(formData.email, formData.password);
      router.push('/dashboard');
      router.refresh();
    } catch (err: any) {
      setError(err.message || 'An error occurred during sign in');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-brand-dark to-brand-darker flex items-center justify-center p-4">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="w-full max-w-4xl grid md:grid-cols-2 gap-12 items-center"
      >
        <div className="hidden md:block">
          <div className="bg-gradient-to-br from-brand-darker/50 to-brand-dark/50 p-8 rounded-2xl border border-brand-gray/20">
            <h1 className="text-3xl font-bold text-brand-white mb-4">Welcome Back to Todo+AI</h1>
            <p className="text-brand-gray-light mb-6">
              Sign in to access your personalized dashboard and continue managing your tasks with our AI assistant.
            </p>
            <div className="space-y-4">
              <div className="flex items-start space-x-3">
                <div className="bg-brand-pink/20 p-2 rounded-lg">
                  <div className="bg-gradient-to-r from-brand-red to-brand-pink w-6 h-6 rounded"></div>
                </div>
                <div>
                  <h3 className="font-medium text-brand-white">AI-Powered Insights</h3>
                  <p className="text-sm text-brand-gray-light">Get smart recommendations for your tasks</p>
                </div>
              </div>
              <div className="flex items-start space-x-3">
                <div className="bg-brand-pink/20 p-2 rounded-lg">
                  <div className="bg-gradient-to-r from-brand-red to-brand-pink w-6 h-6 rounded"></div>
                </div>
                <div>
                  <h3 className="font-medium text-brand-white">Priority Management</h3>
                  <p className="text-sm text-brand-gray-light">Organize tasks by importance and deadline</p>
                </div>
              </div>
              <div className="flex items-start space-x-3">
                <div className="bg-brand-pink/20 p-2 rounded-lg">
                  <div className="bg-gradient-to-r from-brand-red to-brand-pink w-6 h-6 rounded"></div>
                </div>
                <div>
                  <h3 className="font-medium text-brand-white">Smart Notifications</h3>
                  <p className="text-sm text-brand-gray-light">Stay on top of your tasks with intelligent alerts</p>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div>
          <div className="text-center md:text-left mb-8">
            <h1 className="text-3xl font-bold text-brand-white mb-2">Sign in to your account</h1>
            <p className="text-brand-gray-light">
              Enter your credentials to access your dashboard
            </p>
          </div>

          {error && (
            <div className="mb-6 p-4 bg-red-500/20 border border-red-500/30 rounded-lg text-red-300">
              {error}
            </div>
          )}

          <AuthForm type="signin" onSubmit={handleSignIn} isLoading={isLoading} />

          <div className="mt-8 text-center text-brand-gray-light">
            <p>
              By signing in, you agree to our{' '}
              <Link href="/terms" className="text-brand-pink hover:underline">
                Terms of Service
              </Link>{' '}
              and{' '}
              <Link href="/privacy" className="text-brand-pink hover:underline">
                Privacy Policy
              </Link>
              .
            </p>
          </div>
        </div>
      </motion.div>
    </div>
  );
};

export default SigninPage;