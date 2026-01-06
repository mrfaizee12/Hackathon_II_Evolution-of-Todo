'use client';

import React, { useEffect, useState } from 'react';

interface NotificationProps {
  message: string;
  type?: 'success' | 'error' | 'info' | 'warning';
  duration?: number;
  onClose?: () => void;
}

const Notification: React.FC<NotificationProps> = ({
  message,
  type = 'success',
  duration = 3000,
  onClose
}) => {
  const [visible, setVisible] = useState(true);

  const typeStyles = {
    success: 'bg-green-500',
    error: 'bg-red-500',
    info: 'bg-blue-500',
    warning: 'bg-yellow-500',
  };

  useEffect(() => {
    if (duration > 0) {
      const timer = setTimeout(() => {
        setVisible(false);
        if (onClose) onClose();
      }, duration);

      return () => clearTimeout(timer);
    }
  }, [duration, onClose]);

  if (!visible) return null;

  return (
    <div
      className={`
        fixed top-4 right-4 z-50 px-6 py-4 rounded-lg shadow-lg text-white
        ${typeStyles[type]}
        transform transition-all duration-300
        animate-fade-in
      `}
    >
      <div className="flex items-center">
        <span className="mr-2">
          {type === 'success' && '✓'}
          {type === 'error' && '✗'}
          {type === 'warning' && '!'}
          {type === 'info' && 'ℹ'}
        </span>
        <span>{message}</span>
        <button
          onClick={() => {
            setVisible(false);
            if (onClose) onClose();
          }}
          className="ml-4 text-white hover:text-gray-200 focus:outline-none"
        >
          ✕
        </button>
      </div>
    </div>
  );
};

export default Notification;