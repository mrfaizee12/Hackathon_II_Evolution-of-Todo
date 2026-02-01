'use client';

import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Button } from '@/components/ui/Button';
import { cn } from '@/lib/utils';
import { Menu, X } from 'lucide-react';

export interface SidebarProps {
  isOpen: boolean;
  onToggle: () => void;
  children: React.ReactNode;
  className?: string;
}

const Sidebar: React.FC<SidebarProps> = ({
  isOpen,
  onToggle,
  children,
  className
}) => {
  return (
    <>
      {/* Mobile menu button */}
      <Button
        variant="ghost"
        size="icon"
        onClick={onToggle}
        className="md:hidden text-brand-white"
      >
        {isOpen ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
      </Button>

      {/* Sidebar overlay for mobile */}
      <AnimatePresence>
        {isOpen && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={onToggle}
            className="fixed inset-0 z-40 bg-black/50 md:hidden"
          />
        )}
      </AnimatePresence>

      {/* Sidebar */}
      <motion.aside
        initial={false}
        animate={{
          x: isOpen ? 0 : '-100%',
        }}
        transition={{
          type: 'spring',
          damping: 25,
          stiffness: 200,
          duration: 0.3
        }}
        className={cn(
          "fixed inset-y-0 left-0 z-50 w-80 bg-brand-darker/90 backdrop-blur-lg border-r border-brand-gray/20 overflow-y-auto",
          "transform transition-transform duration-300 ease-in-out",
          className
        )}
      >
        <div className="p-6">
          <div className="flex items-center justify-between mb-8">
            <h2 className="text-xl font-bold text-brand-white">AI Assistant</h2>
            <Button
              variant="ghost"
              size="icon"
              onClick={onToggle}
              className="md:hidden text-brand-white"
            >
              <X className="h-5 w-5" />
            </Button>
          </div>

          {children}
        </div>
      </motion.aside>
    </>
  );
};

export { Sidebar };