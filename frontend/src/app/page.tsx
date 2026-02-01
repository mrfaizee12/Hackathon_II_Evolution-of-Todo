'use client';

import React from 'react';
import Link from 'next/link';
import { useAuth } from '../utils/auth';
import { Navigation } from '@/components/landing/Navigation';
import { HeroSection } from '@/components/landing/HeroSection';
import { Button } from '@/components/ui/Button';
import { Card } from '@/components/ui/Card';
import { motion } from 'framer-motion';

const HomePage: React.FC = () => {
  const { state } = useAuth();

  return (
    <div className="min-h-screen bg-gradient-to-br from-brand-dark to-brand-darker">
      <Navigation />

      <HeroSection />

      {/* Features Section */}
      <section className="py-20">
        <div className="container mx-auto px-4">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
            className="text-center mb-16"
          >
            <h2 className="text-3xl md:text-4xl font-bold text-brand-white mb-4">
              Powerful Features for Better Organization
            </h2>
            <p className="text-xl text-brand-gray-light max-w-2xl mx-auto">
              Our todo app helps you stay organized with advanced features designed for productivity.
            </p>
          </motion.div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: 0.1 }}
            >
              <Card variant="elevated" className="h-full">
                <div className="w-12 h-12 bg-brand-pink/20 rounded-full flex items-center justify-center mb-4 mx-auto">
                  <svg className="w-6 h-6 text-brand-pink" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                  </svg>
                </div>
                <h3 className="text-xl font-semibold text-brand-white mb-2 text-center">Priority Management</h3>
                <p className="text-brand-gray-light text-center">
                  Set priorities (high, medium, low) to focus on what matters most and never miss important tasks.
                </p>
              </Card>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: 0.2 }}
            >
              <Card variant="elevated" className="h-full">
                <div className="w-12 h-12 bg-brand-red/20 rounded-full flex items-center justify-center mb-4 mx-auto">
                  <svg className="w-6 h-6 text-brand-red" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a2 2 0 012-2z" />
                  </svg>
                </div>
                <h3 className="text-xl font-semibold text-brand-white mb-2 text-center">Tag Organization</h3>
                <p className="text-brand-gray-light text-center">
                  Categorize tasks with tags for better organization and quick filtering of related items.
                </p>
              </Card>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: 0.3 }}
            >
              <Card variant="elevated" className="h-full">
                <div className="w-12 h-12 bg-gradient-to-r from-brand-red to-brand-pink rounded-full flex items-center justify-center mb-4 mx-auto">
                  <svg className="w-6 h-6 text-brand-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                  </svg>
                </div>
                <h3 className="text-xl font-semibold text-brand-white mb-2 text-center">Smart Search & Filter</h3>
                <p className="text-brand-gray-light text-center">
                  Quickly find tasks using powerful search and filter options by priority, tags, due dates, and more.
                </p>
              </Card>
            </motion.div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 bg-brand-darker/50">
        <div className="container mx-auto px-4">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
            className="max-w-3xl mx-auto text-center"
          >
            <h2 className="text-3xl font-bold text-brand-white mb-6">
              Ready to Transform Your Productivity?
            </h2>
            <p className="text-xl text-brand-gray-light mb-8">
              Join thousands of users who have transformed their productivity with our AI-powered todo app.
            </p>
            <div className="flex flex-col sm:flex-row justify-center gap-4">
              {state.isAuthenticated ? (
                <Button asChild>
                  <Link href="/dashboard">Go to Your Dashboard</Link>
                </Button>
              ) : (
                <Button variant="gradient" asChild>
                  <Link href="/auth/signup">Sign Up Free</Link>
                </Button>
              )}
              <Button variant="outline" className="text-brand-white border-brand-gray-light hover:bg-brand-gray/20" asChild>
                <Link href="/dashboard">Try Demo</Link>
              </Button>
            </div>
          </motion.div>
        </div>
      </section>
    </div>
  );
};

export default HomePage;