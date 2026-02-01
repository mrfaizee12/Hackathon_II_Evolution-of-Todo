'use client';

import React, { useState } from 'react';
import Link from 'next/link';
import { usePathname, useRouter } from 'next/navigation';
import { FiHome, FiMessageSquare, FiSettings, FiLogOut } from 'react-icons/fi';
import ChatBotDrawer from '../../components/chat/ChatBotDrawer';
import { useAuth } from '../../utils/auth';
import { Header } from '@/components/ui/Header';
import { Button } from '@/components/ui/Button';

const DashboardLayout = ({ children }: { children: React.ReactNode }) => {
  const [sidebarOpen, setSidebarOpen] = useState(true); // Default to open
  const [chatOpen, setChatOpen] = useState(false);
  const pathname = usePathname();
  const { state, signout } = useAuth();
  const router = useRouter();

  const handleSignout = () => {
    signout();
  };

  return (
    <div className="flex flex-col min-h-screen bg-gradient-to-br from-brand-dark to-brand-darker">
      {/* Dashboard Header - Always visible with logo and sign out button */}
      <Header
        variant="dashboard"
        isAuthenticated={true}
        onSignOut={handleSignout}
        onSidebarToggle={() => setSidebarOpen(!sidebarOpen)}
        isSidebarOpen={sidebarOpen}
      />

      {/* Flex container for sidebar and main content */}
      <div className="flex flex-1 min-h-[calc(100vh-4rem)] overflow-hidden">
        {/* Sidebar with AI Assistant and other navigation - always visible on desktop */}
        <aside
          className={`bg-brand-darker/50 backdrop-blur-sm border-r border-brand-gray/20 transition-all duration-300 ease-in-out ${
            sidebarOpen ? 'w-64' : 'w-20'
          } flex flex-col`}
        >
          <nav className="p-4 space-y-2">
            <Link
              href="/dashboard"
              className={`flex items-center space-x-3 px-4 py-3 rounded-lg transition-colors ${
                pathname === '/dashboard'
                  ? 'bg-gradient-to-r from-brand-red to-brand-pink text-brand-white'
                  : 'text-brand-gray-light hover:bg-brand-gray/20 hover:text-brand-white'
              }`}
            >
              <FiHome size={20} />
              {sidebarOpen && <span>Todos</span>}
            </Link>
            <button
              className={`w-full flex items-center space-x-3 px-4 py-3 rounded-lg transition-colors ${
                (pathname?.includes('/chat') || pathname?.startsWith('/chat'))
                  ? 'bg-gradient-to-r from-brand-red to-brand-pink text-brand-white'
                  : 'text-brand-gray-light hover:bg-brand-gray/20 hover:text-brand-white'
              }`}
              onClick={() => {
                setChatOpen(true);
              }}
            >
              <FiMessageSquare size={20} />
              {sidebarOpen && <span>AI Assistant 🤖</span>}
            </button>
            <Link
              href="/dashboard/settings"
              className={`flex items-center space-x-3 px-4 py-3 rounded-lg transition-colors ${
                pathname?.includes('/settings')
                  ? 'bg-gradient-to-r from-brand-red to-brand-pink text-brand-white'
                  : 'text-brand-gray-light hover:bg-brand-gray/20 hover:text-brand-white'
              }`}
            >
              <FiSettings size={20} />
              {sidebarOpen && <span>Settings</span>}
            </Link>
          </nav>

          <div className="mt-auto p-4 border-t border-brand-gray/20">
            {sidebarOpen && (
              <div className="text-sm text-brand-gray-light mb-4">
                Welcome, {state.user?.name || state.user?.email || 'User'}!
              </div>
            )}
            <Button
              variant="ghost"
              size="icon"
              onClick={handleSignout}
              title="Sign out"
              className="w-full justify-start"
            >
              <FiLogOut size={18} className="text-brand-gray-light" />
              {sidebarOpen && <span className="ml-3 text-brand-gray-light">Sign out</span>}
            </Button>
          </div>
        </aside>

        {/* Main content area */}
        <main className="flex-1 overflow-y-auto p-4 md:p-6 bg-brand-darker/30">
          {children}
        </main>
      </div>

      {/* AI Chatbot Drawer */}
      {state.user && (
        <ChatBotDrawer
          isOpen={chatOpen}
          onClose={() => setChatOpen(false)}
          userId={state.user.id}
        />
      )}
    </div>
  );
};

export default DashboardLayout;