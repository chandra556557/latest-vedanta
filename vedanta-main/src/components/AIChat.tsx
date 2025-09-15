import React, { useState, useRef, useEffect } from 'react';
import { Send, Bot, User, Loader2 } from 'lucide-react';
import { chatWithAI } from '../services/api';

interface Message {
  role: 'user' | 'assistant' | 'system';
  content: string;
  timestamp: string;
}

const AIChat: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Scroll to bottom of messages
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    const userMessage: Message = {
      role: 'user',
      content: input,
      timestamp: new Date().toISOString(),
    };

    // Update UI with user message
    setMessages((prev) => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      // Call the backend API
      const response = await chatWithAI(input, messages);
      
      const aiMessage: Message = {
        role: 'assistant',
        content: response.response,
        timestamp: new Date().toISOString(),
      };

      setMessages((prev) => [...prev, aiMessage]);
    } catch (error) {
      console.error('Error:', error);
      // Add error message to chat
      const errorMessage: Message = {
        role: 'assistant',
        content: 'Sorry, I encountered an error. Please try again.',
        timestamp: new Date().toISOString(),
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-[600px] max-w-4xl mx-auto bg-white rounded-lg shadow-lg overflow-hidden">
      {/* Header */}
      <div className="bg-blue-600 text-white p-4 flex items-center">
        <Bot className="h-6 w-6 mr-2" />
        <h2 className="text-xl font-semibold">AI Health Assistant</h2>
      </div>
      
      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4 bg-gray-50">
        {messages.length === 0 && (
          <div className="text-center text-gray-500 mt-10">
            <p>Ask me anything about kidney health and nephrology</p>
          </div>
        )}
        
        {messages.map((message, index) => (
          <div
            key={index}
            className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            <div
              className={`max-w-3/4 rounded-lg p-3 ${
                message.role === 'user'
                  ? 'bg-blue-500 text-white rounded-br-none'
                  : 'bg-white border border-gray-200 rounded-bl-none'
              }`}
            >
              <div className="flex items-center mb-1">
                {message.role === 'user' ? (
                  <User className="h-4 w-4 mr-2" />
                ) : (
                  <Bot className="h-4 w-4 mr-2 text-blue-500" />
                )}
                <span className="text-xs text-gray-500">
                  {new Date(message.timestamp).toLocaleTimeString()}
                </span>
              </div>
              <p className="whitespace-pre-wrap">{message.content}</p>
            </div>
          </div>
        ))}
        
        {isLoading && (
          <div className="flex justify-start">
            <div className="bg-white border border-gray-200 rounded-lg p-3 rounded-bl-none">
              <div className="flex items-center">
                <Bot className="h-4 w-4 mr-2 text-blue-500" />
                <div className="flex space-x-1">
                  <div className="h-2 w-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></div>
                  <div className="h-2 w-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></div>
                  <div className="h-2 w-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></div>
                </div>
              </div>
            </div>
          </div>
        )}
        
        <div ref={messagesEndRef} />
      </div>
      
      {/* Input */}
      <form onSubmit={handleSubmit} className="border-t border-gray-200 p-4 bg-white">
        <div className="flex items-center">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Type your message..."
            className="flex-1 border border-gray-300 rounded-l-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            disabled={isLoading}
          />
          <button
            type="submit"
            disabled={!input.trim() || isLoading}
            className="bg-blue-500 text-white px-4 py-2 rounded-r-lg hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {isLoading ? (
              <Loader2 className="h-5 w-5 animate-spin" />
            ) : (
              <Send className="h-5 w-5" />
            )}
          </button>
        </div>
      </form>
    </div>
  );
};

export default AIChat;
