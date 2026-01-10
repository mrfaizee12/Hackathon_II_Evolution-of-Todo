'use client';

import React from 'react';
import Link from 'next/link';
import { useAuth } from '../utils/auth';

const HomePage: React.FC = () => {
  const { state } = useAuth();

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Hero Section */}
      <div className="bg-gradient-to-r from-indigo-600 to-purple-700 text-white">
        <div className="container mx-auto px-4 py-16 md:py-24">
          <div className="max-w-3xl mx-auto text-center">
            <h1 className="text-4xl md:text-6xl font-bold mb-6">
              Organize Your Life with Ease
            </h1>
            <p className="text-xl md:text-2xl mb-8 text-indigo-100">
              A powerful todo app that helps you manage tasks efficiently with priorities, tags, and smart filtering.
            </p>
            <div className="flex flex-col sm:flex-row justify-center gap-4">
              {state.isAuthenticated ? (
                <Link
                  href="/dashboard"
                  className="px-8 py-4 bg-white text-indigo-600 font-semibold rounded-lg shadow-lg hover:bg-gray-100 transition duration-300 transform hover:-translate-y-0.5 hover:shadow-xl"
                >
                  Go to Dashboard
                </Link>
              ) : (
                <>
                  <Link
                    href="/auth/signup"
                    className="px-8 py-4 bg-white text-indigo-600 font-semibold rounded-lg shadow-lg hover:bg-gray-100 transition duration-300 transform hover:-translate-y-0.5 hover:shadow-xl"
                  >
                    Get Started
                  </Link>
                  <Link
                    href="/auth/signin"
                    className="px-8 py-4 bg-transparent border-2 border-white text-white font-semibold rounded-lg hover:bg-white hover:text-indigo-600 transition duration-300"
                  >
                    Sign In
                  </Link>
                </>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* Features Section */}
      <section className="py-16 bg-white">
        <div className="container mx-auto px-4">
          <div className="text-center mb-12">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              Powerful Features for Better Organization
            </h2>
            <p className="text-xl text-gray-600 max-w-2xl mx-auto">
              Our todo app helps you stay organized with advanced features designed for productivity.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="bg-gray-50 p-6 rounded-lg shadow-sm">
              <div className="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center mb-4 mx-auto">
                <svg className="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                </svg>
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-2 text-center">Priority Management</h3>
              <p className="text-gray-600 text-center">
                Set priorities (high, medium, low) to focus on what matters most and never miss important tasks.
              </p>
            </div>

            <div className="bg-gray-50 p-6 rounded-lg shadow-sm">
              <div className="w-12 h-12 bg-green-100 rounded-full flex items-center justify-center mb-4 mx-auto">
                <svg className="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a2 2 0 012-2z" />
                </svg>
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-2 text-center">Tag Organization</h3>
              <p className="text-gray-600 text-center">
                Categorize tasks with tags for better organization and quick filtering of related items.
              </p>
            </div>

            <div className="bg-gray-50 p-6 rounded-lg shadow-sm">
              <div className="w-12 h-12 bg-purple-100 rounded-full flex items-center justify-center mb-4 mx-auto">
                <svg className="w-6 h-6 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                </svg>
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-2 text-center">Smart Search & Filter</h3>
              <p className="text-gray-600 text-center">
                Quickly find tasks using powerful search and filter options by priority, tags, due dates, and more.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-16 bg-gray-50">
        <div className="container mx-auto px-4">
          <div className="max-w-3xl mx-auto text-center">
            <h2 className="text-3xl font-bold text-gray-900 mb-6">
              Ready to Get Organized?
            </h2>
            <p className="text-xl text-gray-600 mb-8">
              Join thousands of users who have transformed their productivity with our todo app.
            </p>
            <div className="flex flex-col sm:flex-row justify-center gap-4">
              {state.isAuthenticated ? (
                <Link
                  href="/dashboard"
                  className="px-8 py-4 bg-gradient-to-r from-indigo-600 to-purple-600 text-white font-semibold rounded-lg shadow-md hover:from-indigo-700 hover:to-purple-700 transition duration-300 transform hover:-translate-y-0.5"
                >
                  Go to Your Dashboard
                </Link>
              ) : (
                <Link
                  href="/auth/signup"
                  className="px-8 py-4 bg-gradient-to-r from-indigo-600 to-purple-600 text-white font-semibold rounded-lg shadow-md hover:from-indigo-700 hover:to-purple-700 transition duration-300 transform hover:-translate-y-0.5"
                >
                  Sign Up Free
                </Link>
              )}
              <Link
                href="/dashboard"
                className="px-8 py-4 bg-white text-indigo-600 font-semibold rounded-lg shadow-md border border-indigo-200 hover:bg-gray-50 transition duration-300"
              >
                Try Demo
              </Link>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};

export default HomePage;