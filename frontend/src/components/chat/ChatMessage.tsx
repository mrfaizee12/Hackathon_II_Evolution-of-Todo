import React from 'react';
import { FiLoader } from 'react-icons/fi';

interface ChatMessageProps {
  content: string;
  sender: 'user' | 'ai';
  timestamp: Date;
  isLoading?: boolean;
}

const ChatMessage: React.FC<ChatMessageProps> = ({ content, sender, timestamp, isLoading = false }) => {
  return (
    <div className={`flex ${sender === 'user' ? 'justify-end' : 'justify-start'}`}>
      <div
        className={`max-w-[80%] rounded-2xl px-4 py-3 ${
          sender === 'user'
            ? 'bg-blue-600 text-white rounded-tr-none'
            : 'bg-gray-700 text-gray-100 rounded-tl-none'
        }`}
      >
        <div className="whitespace-pre-wrap">
          {isLoading ? (
            <div className="flex items-center space-x-2">
              <FiLoader className="animate-spin" />
              <span>Processing...</span>
            </div>
          ) : (
            content
          )}
        </div>
        <div className={`text-xs mt-1 ${sender === 'user' ? 'text-blue-200' : 'text-gray-400'}`}>
          {timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
        </div>
      </div>
    </div>
  );
};

export default ChatMessage;