'use client';

import React from 'react';
import Link from 'next/link';
import { Button } from '@/components/ui/Button';
import { cn } from '@/lib/utils';
import { motion } from 'framer-motion';

export interface NavigationProps {
  className?: string;
}

const Navigation: React.FC<NavigationProps> = ({ className }) => {
  return (
    <motion.nav
      initial={{ opacity: 0, y: -20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      className={cn(
        "flex items-center justify-between py-6",
        className
      )}
    >
      <Link href="/" className="flex items-center space-x-2">
        <div className="bg-gradient-to-r from-brand-red to-brand-pink w-8 h-8 rounded-lg"></div>
        <span className="text-xl font-bold text-brand-white">Todo+AI</span>
      </Link>

      <div className="flex items-center space-x-4">
        <Button variant="ghost" className="text-brand-white hover:text-brand-pink" asChild>
          <Link href="/auth/signin">Sign In</Link>
        </Button>
        <Button variant="gradient" asChild>
          <Link href="/auth/signup">Join</Link>
        </Button>
      </div>
    </motion.nav>
  );
};

export { Navigation };