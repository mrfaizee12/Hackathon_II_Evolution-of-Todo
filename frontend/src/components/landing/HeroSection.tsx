'use client';

import React from 'react';
import { Button } from '@/components/ui/Button';
import { Card } from '@/components/ui/Card';
import { cn } from '@/lib/utils';
import { motion } from 'framer-motion';

export interface HeroSectionProps {
  className?: string;
}

const HeroSection: React.FC<HeroSectionProps> = ({ className }) => {
  const container = {
    hidden: { opacity: 0 },
    show: {
      opacity: 1,
      transition: {
        staggerChildren: 0.1
      }
    }
  };

  const item = {
    hidden: { opacity: 0, y: 20 },
    show: { opacity: 1, y: 0 }
  };

  return (
    <motion.section
      initial="hidden"
      animate="show"
      variants={container}
      className={cn(
        "py-20 md:py-32 flex flex-col items-center text-center",
        className
      )}
    >
      <motion.div variants={item} className="mb-8">
        <span className="bg-gradient-to-r from-brand-red to-brand-pink text-brand-white px-4 py-2 rounded-full text-sm font-medium">
          AI-Powered Productivity
        </span>
      </motion.div>

      <motion.h1
        variants={item}
        className="text-4xl md:text-6xl font-bold text-brand-white mb-6 max-w-3xl leading-tight"
      >
        Transform Your <span className="bg-gradient-to-r from-brand-red to-brand-pink bg-clip-text text-transparent">Productivity</span> with AI
      </motion.h1>

      <motion.p
        variants={item}
        className="text-xl text-brand-gray-light mb-10 max-w-2xl"
      >
        Experience the future of task management with our intelligent assistant that learns your habits and helps you achieve more with less effort.
      </motion.p>

      <motion.div
        variants={item}
        className="flex flex-col sm:flex-row gap-4"
      >
        <Button size="lg" className="px-8 py-6 text-lg">
          Get Started Free
        </Button>
        <Button variant="outline" size="lg" className="px-8 py-6 text-lg">
          Watch Demo
        </Button>
      </motion.div>

      <motion.div
        variants={item}
        className="mt-16 w-full max-w-5xl"
      >
        <Card variant="elevated" className="p-0 overflow-hidden">
          <div className="bg-gradient-to-r from-brand-dark to-brand-darker h-64 md:h-96 flex items-center justify-center">
            <div className="text-center">
              <div className="inline-block bg-gradient-to-r from-brand-red to-brand-pink p-1 rounded-lg">
                <div className="bg-brand-darker rounded-md px-4 py-2 text-brand-white">
                  AI Assistant Preview
                </div>
              </div>
            </div>
          </div>
        </Card>
      </motion.div>
    </motion.section>
  );
};

export { HeroSection };