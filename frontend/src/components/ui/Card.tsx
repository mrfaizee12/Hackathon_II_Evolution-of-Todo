import React, { HTMLAttributes } from 'react';

interface CardProps extends HTMLAttributes<HTMLDivElement> {
  elevated?: boolean;
  gradient?: boolean;
}

const Card: React.FC<CardProps> = ({
  children,
  elevated = false,
  gradient = false,
  className = '',
  ...props
}) => {
  const baseClasses = 'rounded-2xl transition-all duration-300 border border-gray-100';

  const elevationClasses = elevated
    ? 'shadow-lg hover:shadow-xl transform hover:-translate-y-1'
    : 'shadow-md hover:shadow-lg transform hover:-translate-y-0.5';

  const gradientClass = gradient
    ? 'bg-gradient-to-br from-indigo-50 via-purple-50 to-pink-50'
    : 'bg-white';

  const classes = `${baseClasses} ${elevationClasses} ${gradientClass} ${className}`;

  return (
    <div className={classes} {...props}>
      {children}
    </div>
  );
};

export default Card;