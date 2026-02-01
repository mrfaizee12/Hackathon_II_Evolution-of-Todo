'use client';

import React from 'react';
import { motion } from 'framer-motion';

export interface ChatBubbleProps {
  message: string;
  sender: 'user' | 'ai';
  timestamp?: Date;
  isPending?: boolean;
  className?: string;
}

const ChatBubble: React.FC<ChatBubbleProps> = ({
  message,
  sender,
  timestamp,
  isPending = false,
  className = ''
}) => {
  const isUser = sender === 'user';

  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
      className={`flex ${isUser ? 'justify-end' : 'justify-start'} mb-4 ${className}`}
    >
      <div
        className={`max-w-[80%] rounded-2xl px-4 py-3 ${
          isUser
            ? 'bg-gradient-to-r from-brand-pink to-brand-red text-brand-white rounded-br-none'
            : 'bg-brand-darker/50 text-brand-white rounded-bl-none border border-brand-gray/20'
        }`}
      >
        <div className="whitespace-pre-wrap break-words">{message}</div>

        {isPending && (
          <div className="flex space-x-1 mt-2">
            <div className="w-2 h-2 bg-brand-gray-light rounded-full animate-bounce"></div>
            <div className="w-2 h-2 bg-brand-gray-light rounded-full animate-bounce delay-100"></div>
            <div className="w-2 h-2 bg-brand-gray-light rounded-full animate-bounce delay-200"></div>
          </div>
        )}

        {timestamp && (
          <div className={`text-xs mt-1 ${isUser ? 'text-brand-pink-light' : 'text-brand-gray'}`}>
            {timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
          </div>
        )}
      </div>
    </motion.div>
  );
};

export { ChatBubble };