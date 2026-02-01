'use client';

import React, { useState } from 'react';
import Link from 'next/link';
import { Card } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import { motion } from 'framer-motion';
import { Eye, EyeOff } from 'lucide-react';

export interface AuthFormProps {
  type: 'signin' | 'signup';
  onSubmit: (formData: { email: string; password: string; name?: string }) => void;
  isLoading?: boolean;
}

const AuthForm: React.FC<AuthFormProps> = ({ type, onSubmit, isLoading = false }) => {
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    name: '',
  });
  const [showPassword, setShowPassword] = useState(false);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSubmit(formData);
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
      <Card variant="elevated" className="w-full max-w-md p-8">
        <div className="text-center mb-8">
          <div className="mx-auto bg-gradient-to-r from-brand-red to-brand-pink w-12 h-12 rounded-lg mb-4"></div>
          <h2 className="text-2xl font-bold text-brand-white">
            {type === 'signin' ? 'Welcome Back' : 'Create Account'}
          </h2>
          <p className="text-brand-gray-light mt-2">
            {type === 'signin'
              ? 'Sign in to your account to continue'
              : 'Create an account to get started'}
          </p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-6">
          {type === 'signup' && (
            <div>
              <label htmlFor="name" className="block text-sm font-medium text-brand-gray-light mb-2">
                Full Name
              </label>
              <input
                id="name"
                name="name"
                type="text"
                value={formData.name}
                onChange={handleChange}
                required={type === 'signup'}
                className="w-full px-4 py-3 bg-brand-darker border border-brand-gray/30 rounded-lg text-brand-white placeholder-brand-gray focus:outline-none focus:ring-2 focus:ring-brand-pink focus:border-transparent transition-all"
                placeholder="John Doe"
              />
            </div>
          )}

          <div>
            <label htmlFor="email" className="block text-sm font-medium text-brand-gray-light mb-2">
              Email Address
            </label>
            <input
              id="email"
              name="email"
              type="email"
              value={formData.email}
              onChange={handleChange}
              required
              className="w-full px-4 py-3 bg-brand-darker border border-brand-gray/30 rounded-lg text-brand-white placeholder-brand-gray focus:outline-none focus:ring-2 focus:ring-brand-pink focus:border-transparent transition-all"
              placeholder="you@example.com"
            />
          </div>

          <div>
            <label htmlFor="password" className="block text-sm font-medium text-brand-gray-light mb-2">
              Password
            </label>
            <div className="relative">
              <input
                id="password"
                name="password"
                type={showPassword ? 'text' : 'password'}
                value={formData.password}
                onChange={handleChange}
                required
                className="w-full px-4 py-3 pr-12 bg-brand-darker border border-brand-gray/30 rounded-lg text-brand-white placeholder-brand-gray focus:outline-none focus:ring-2 focus:ring-brand-pink focus:border-transparent transition-all"
                placeholder="••••••••"
              />
              <button
                type="button"
                onClick={() => setShowPassword(!showPassword)}
                className="absolute inset-y-0 right-0 pr-3 flex items-center text-brand-gray-light hover:text-brand-white"
              >
                {showPassword ? <EyeOff className="h-5 w-5" /> : <Eye className="h-5 w-5" />}
              </button>
            </div>
          </div>

          {type === 'signin' && (
            <div className="flex items-center justify-between">
              <label className="flex items-center">
                <input
                  type="checkbox"
                  className="rounded bg-brand-darker border-brand-gray/30 text-brand-pink focus:ring-brand-pink"
                />
                <span className="ml-2 text-sm text-brand-gray-light">Remember me</span>
              </label>
              <Link href="#" className="text-sm text-brand-pink hover:underline">
                Forgot password?
              </Link>
            </div>
          )}

          <Button
            type="submit"
            variant="gradient"
            className="w-full py-6 text-lg"
            disabled={isLoading}
          >
            {isLoading ? 'Processing...' : type === 'signin' ? 'Sign In' : 'Sign Up'}
          </Button>
        </form>

        <div className="mt-6 text-center">
          <p className="text-brand-gray-light">
            {type === 'signin' ? "Don't have an account? " : "Already have an account? "}
            <Link href={type === 'signin' ? '/auth/signup' : '/auth/signin'} className="text-brand-pink font-medium hover:underline">
              {type === 'signin' ? 'Sign up' : 'Sign in'}
            </Link>
          </p>
        </div>
      </Card>
    </motion.div>
  );
};

export { AuthForm };