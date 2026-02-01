'use client';

import React, { useState } from 'react';
import { Button } from '@/components/ui/Button';
import { Send, Bot } from 'lucide-react';

export interface ChatInputProps {
  onSubmit: (message: string) => void;
  placeholder?: string;
  disabled?: boolean;
  autoFocus?: boolean;
}

const ChatInput: React.FC<ChatInputProps> = ({
  onSubmit,
  placeholder = 'Type your message...',
  disabled = false,
  autoFocus = true
}) => {
  const [inputValue, setInputValue] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (inputValue.trim() && !disabled) {
      onSubmit(inputValue.trim());
      setInputValue('');
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="w-full">
      <div className="flex items-center space-x-2 bg-brand-darker border border-brand-gray/20 rounded-xl px-4 py-3">
        <div className="bg-brand-pink/20 p-2 rounded-lg">
          <Bot className="h-5 w-5 text-brand-pink" />
        </div>
        <input
          type="text"
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder={placeholder}
          disabled={disabled}
          autoFocus={autoFocus}
          className="flex-1 bg-transparent text-brand-white placeholder-brand-gray focus:outline-none"
        />
        <Button
          type="submit"
          variant="ghost"
          size="icon"
          disabled={!inputValue.trim() || disabled}
          className="text-brand-white hover:bg-brand-pink/20"
        >
          <Send className="h-5 w-5" />
        </Button>
      </div>
    </form>
  );
};

export { ChatInput };