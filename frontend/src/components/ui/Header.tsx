'use client';

import React from 'react';
import Link from 'next/link';
import { Button } from '@/components/ui/Button';
import { cn } from '@/lib/utils';
import { FiLogOut, FiMenu } from 'react-icons/fi';

export interface HeaderProps {
  variant?: 'landing' | 'dashboard';
  isAuthenticated?: boolean;
  onSignOut?: () => void;
  onSidebarToggle?: () => void;
  isSidebarOpen?: boolean;
  className?: string;
}

const Header: React.FC<HeaderProps> = ({
  variant = 'landing',
  isAuthenticated = false,
  onSignOut,
  onSidebarToggle,
  isSidebarOpen,
  className
}) => {
  const renderAuthButtons = () => (
    <div className="flex items-center space-x-4">
      <Button variant="ghost" asChild className="text-brand-white hover:text-brand-pink">
        <Link href="/auth/signin">Sign In</Link>
      </Button>
      <Button variant="gradient" asChild>
        <Link href="/auth/signup">Join</Link>
      </Button>
    </div>
  );

  const renderDashboardControls = () => (
    <div className="flex items-center space-x-4">
      <Button
        variant="ghost"
        size="icon"
        onClick={onSidebarToggle}
        className="text-brand-white lg:hidden"
      >
        <FiMenu size={20} />
      </Button>
      <span className="text-brand-white hidden sm:inline">Welcome back!</span>
      <Button
        variant="outline"
        onClick={onSignOut}
        className="text-brand-white border-brand-gray-light hover:bg-brand-gray/20"
      >
        <FiLogOut className="mr-2" size={18} />
        Sign Out
      </Button>
    </div>
  );

  return (
    <header
      className={cn(
        "sticky top-0 z-50 w-full border-b border-brand-gray/20 bg-brand-darker/80 backdrop-blur-md",
        className
      )}
    >
      <div className="container mx-auto px-4 py-4 flex justify-between items-center">
        <Link href="/" className="flex items-center space-x-2">
          <div className="bg-gradient-to-r from-brand-red to-brand-pink w-8 h-8 rounded-lg"></div>
          <span className="text-xl font-bold text-brand-white">Todo+AI</span>
        </Link>

        {variant === 'landing' && !isAuthenticated ? renderAuthButtons() : renderDashboardControls()}
      </div>
    </header>
  );
};

export { Header };