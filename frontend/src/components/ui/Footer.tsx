'use client';

import React from 'react';
import Link from 'next/link';
import { cn } from '@/lib/utils';
import { motion } from 'framer-motion';

export interface FooterProps {
  className?: string;
}

const Footer: React.FC<FooterProps> = ({ className }) => {
  const currentYear = new Date().getFullYear();

  return (
    <motion.footer
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ delay: 0.5, duration: 0.5 }}
      className={cn(
        "bg-brand-darker border-t border-brand-gray/20 py-12 mt-16",
        className
      )}
    >
      <div className="container mx-auto px-4">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          <div>
            <div className="flex items-center space-x-2 mb-4">
              <div className="bg-gradient-to-r from-brand-red to-brand-pink w-6 h-6 rounded-lg"></div>
              <span className="text-lg font-bold text-brand-white">Todo+AI</span>
            </div>
            <p className="text-brand-gray-light text-sm">
              The smartest way to manage your tasks with AI assistance.
            </p>
          </div>

          <div>
            <h3 className="text-brand-white font-semibold mb-4">Product</h3>
            <ul className="space-y-2">
              <li><Link href="/" className="text-brand-gray-light hover:text-brand-pink-light text-sm">Features</Link></li>
              <li><Link href="/pricing" className="text-brand-gray-light hover:text-brand-pink-light text-sm">Pricing</Link></li>
              <li><Link href="/demo" className="text-brand-gray-light hover:text-brand-pink-light text-sm">Demo</Link></li>
            </ul>
          </div>

          <div>
            <h3 className="text-brand-white font-semibold mb-4">Company</h3>
            <ul className="space-y-2">
              <li><Link href="/about" className="text-brand-gray-light hover:text-brand-pink-light text-sm">About</Link></li>
              <li><Link href="/blog" className="text-brand-gray-light hover:text-brand-pink-light text-sm">Blog</Link></li>
              <li><Link href="/contact" className="text-brand-gray-light hover:text-brand-pink-light text-sm">Contact</Link></li>
            </ul>
          </div>

          <div>
            <h3 className="text-brand-white font-semibold mb-4">Legal</h3>
            <ul className="space-y-2">
              <li><Link href="/terms" className="text-brand-gray-light hover:text-brand-pink-light text-sm">Terms</Link></li>
              <li><Link href="/privacy" className="text-brand-gray-light hover:text-brand-pink-light text-sm">Privacy</Link></li>
              <li><Link href="/security" className="text-brand-gray-light hover:text-brand-pink-light text-sm">Security</Link></li>
            </ul>
          </div>
        </div>

        <div className="border-t border-brand-gray/20 mt-8 pt-8 text-center">
          <p className="text-brand-gray-light text-sm">
            © {currentYear} Todo+AI. All rights reserved.
          </p>
        </div>
      </div>
    </motion.footer>
  );
};

export { Footer };