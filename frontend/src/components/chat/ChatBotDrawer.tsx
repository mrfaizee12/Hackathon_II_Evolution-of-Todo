import React, { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { FiX, FiSend, FiLoader, FiChevronLeft } from 'react-icons/fi';
import chatService from '../../services/chatService';

interface Message {
  id: string;
  content: string;
  sender: 'user' | 'ai';
  timestamp: Date;
  isLoading?: boolean;
}

interface TodoTask {
  id: string;
  title: string;
  description?: string;
  completed: boolean;
  priority: string;
  tags?: string;
  due_date?: string;
  created_at: string;
}

interface ChatBotDrawerProps {
  isOpen: boolean;
  onClose: () => void;
  userId: string;
  onTasksUpdated?: (tasks: TodoTask[]) => void;
}

const ChatBotDrawer: React.FC<ChatBotDrawerProps> = ({ isOpen, onClose, userId, onTasksUpdated }) => {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      content: 'Hello! I\'m your AI assistant. How can I help you manage your todos today?',
      sender: 'ai',
      timestamp: new Date(),
    }
  ]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [currentConversationId, setCurrentConversationId] = useState<string | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Scroll to bottom when messages change
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const handleSendMessage = async () => {
    if (!inputValue.trim() || isLoading) return;

    // Add user message
    const userMessage: Message = {
      id: Date.now().toString(),
      content: inputValue,
      sender: 'user',
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);

    try {
      // Use chat service to send message
      const response = await chatService.sendMessage(userId, {
        message: inputValue,
        conversation_id: currentConversationId || undefined
      });

      // Update conversation ID in state
      if (response && response.conversation_id) {
        setCurrentConversationId(response.conversation_id);
      }

      // If the response includes updated tasks, notify the parent component
      if (response && response.tasks && onTasksUpdated) {
        onTasksUpdated(response.tasks);
      }

      // Also dispatch a custom event to notify any listening components (like the dashboard page)
      if (response && response.tasks) {
        window.dispatchEvent(new CustomEvent('tasksUpdated', { detail: response.tasks }));
      }

      // Add AI response
      const aiMessage: Message = {
        id: Date.now().toString(),
        content: response && response.response ? response.response : "Sorry, I'm having trouble connecting to my brain.",
        sender: 'ai',
        timestamp: new Date(),
      };

      setMessages(prev => [...prev, aiMessage]);
    } catch (error) {
      console.error('Error sending message:', error);

      // Add error message
      const errorMessage: Message = {
        id: Date.now().toString(),
        content: 'Sorry, I encountered an error. Please try again.',
        sender: 'ai',
        timestamp: new Date(),
      };

      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  return (
    <AnimatePresence>
      {isOpen && (
        <motion.div
          className="fixed inset-0 z-50 overflow-hidden"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
        >
          {/* Backdrop */}
          <motion.div
            className="absolute inset-0 bg-black bg-opacity-50"
            onClick={onClose}
            initial={{ opacity: 0 }}
            animate={{ opacity: 0.5 }}
            exit={{ opacity: 0 }}
          />

          {/* Drawer */}
          <motion.div
            className="absolute top-0 right-0 h-full w-full max-w-md bg-gradient-to-br from-gray-900 to-gray-800 shadow-xl rounded-l-2xl overflow-hidden flex flex-col"
            initial={{ x: '100%' }}
            animate={{ x: 0 }}
            exit={{ x: '100%' }}
            transition={{ type: 'spring', damping: 25, stiffness: 300 }}
          >
            {/* Header */}
            <div className="flex items-center justify-between p-4 border-b border-gray-700">
              <div className="flex items-center space-x-2">
                <FiChevronLeft
                  className="text-white cursor-pointer hover:text-blue-400 transition-colors"
                  onClick={onClose}
                  size={24}
                />
                <h2 className="text-xl font-bold text-white">AI Assistant</h2>
              </div>
              <button
                onClick={onClose}
                className="text-gray-400 hover:text-white transition-colors"
              >
                <FiX size={24} />
              </button>
            </div>

            {/* Messages container */}
            <div className="flex-1 overflow-y-auto p-4 space-y-4">
              {messages.map((message) => (
                <motion.div
                  key={message.id}
                  className={`flex ${message.sender === 'user' ? 'justify-end' : 'justify-start'}`}
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.3 }}
                >
                  <div
                    className={`max-w-[80%] rounded-2xl px-4 py-3 ${
                      message.sender === 'user'
                        ? 'bg-blue-600 text-white rounded-tr-none'
                        : 'bg-gray-700 text-gray-100 rounded-tl-none'
                    }`}
                  >
                    <div className="whitespace-pre-wrap">{message.content}</div>
                    <div className={`text-xs mt-1 ${message.sender === 'user' ? 'text-blue-200' : 'text-gray-400'}`}>
                      {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                    </div>
                  </div>
                </motion.div>
              ))}

              {isLoading && (
                <motion.div
                  className="flex justify-start"
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.3 }}
                >
                  <div className="bg-gray-700 text-gray-100 rounded-2xl rounded-tl-none px-4 py-3">
                    <div className="flex items-center space-x-2">
                      <FiLoader className="animate-spin" />
                      <span>Thinking...</span>
                    </div>
                  </div>
                </motion.div>
              )}
              <div ref={messagesEndRef} />
            </div>

            {/* Input area */}
            <div className="border-t border-gray-700 p-4">
              <div className="flex items-end space-x-2">
                <textarea
                  value={inputValue}
                  onChange={(e) => setInputValue(e.target.value)}
                  onKeyDown={handleKeyDown}
                  placeholder="Type your message..."
                  className="flex-1 bg-gray-700 text-white rounded-2xl px-4 py-3 resize-none focus:outline-none focus:ring-2 focus:ring-blue-500 min-h-[60px] max-h-[120px]"
                  rows={1}
                />
                <button
                  onClick={handleSendMessage}
                  disabled={isLoading || !inputValue.trim()}
                  className={`flex items-center justify-center w-12 h-12 rounded-full ${
                    isLoading || !inputValue.trim()
                      ? 'bg-gray-600 cursor-not-allowed'
                      : 'bg-blue-600 hover:bg-blue-700'
                  } transition-colors`}
                >
                  {isLoading ? (
                    <FiLoader className="animate-spin text-white" />
                  ) : (
                    <FiSend className="text-white" />
                  )}
                </button>
              </div>
              <p className="text-xs text-gray-500 mt-2 text-center">
                AI Assistant can help manage your todos using natural language
              </p>
            </div>
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>
  );
};

export default ChatBotDrawer;