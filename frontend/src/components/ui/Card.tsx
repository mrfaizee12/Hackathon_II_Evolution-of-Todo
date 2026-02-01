'use client';

import React from 'react';
import { cn } from '@/lib/utils';

export interface CardProps extends React.HTMLAttributes<HTMLDivElement> {
  children: React.ReactNode;
  variant?: 'default' | 'elevated' | 'outlined';
}

const Card = React.forwardRef<HTMLDivElement, CardProps>(
  ({ className, variant = 'default', children, ...props }, ref) => {
    const variantClasses = {
      default: 'bg-brand-darker/50 backdrop-blur-sm border border-brand-gray/20',
      elevated: 'bg-brand-darker/70 backdrop-blur-md border border-brand-gray/30 shadow-lg shadow-black/20',
      outlined: 'bg-brand-darker/30 border border-brand-gray/40',
    };

    return (
      <div
        ref={ref}
        className={cn(
          'rounded-xl p-6',
          variantClasses[variant],
          className
        )}
        {...props}
      >
        {children}
      </div>
    );
  }
);
Card.displayName = 'Card';

export { Card };