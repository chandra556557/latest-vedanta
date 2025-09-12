import React, { useState, useRef, useEffect } from 'react';
import { motion } from 'framer-motion';
import { sendMessage } from '../services/healthoService';
import { X, Bot, Loader2, Send, MessageSquare } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

interface Message {
  id: number;
  text: string;
  isBot: boolean;
  timestamp: Date;
  actions?: Array<{
    label: string;
    action: string;
    icon?: React.ComponentType<any>;
  }>;
}

interface QuickActionProps {
  icon: React.ComponentType<{ className?: string }>;
  label: string;
  onClick: () => void;
  color?: 'blue' | 'green' | 'amber' | 'purple';
}

const QuickAction: React.FC<QuickActionProps> = ({ icon: Icon, label, onClick, color = 'blue' }) => {
  const colors = {
    blue: 'from-blue-500 to-blue-600',
    green: 'from-emerald-500 to-teal-600',
    amber: 'from-amber-500 to-orange-500',
    purple: 'from-purple-500 to-indigo-600'
  } as const;

  return (
    <button
      onClick={onClick}
      className={`flex items-center space-x-2 px-4 py-2 rounded-lg bg-gradient-to-r ${colors[color]} text-white text-sm font-medium hover:opacity-90 transition-opacity`}
    >
      <Icon className="w-4 h-4" />
      <span>{label}</span>
    </button>
  );
};

const TypingIndicator = () => (
  <div className="flex space-x-1 p-2">
    <motion.div
      animate={{ y: [0, -5, 0] }}
      transition={{ duration: 1, repeat: Infinity, delay: 0 }}
      className="w-2 h-2 bg-blue-500 rounded-full"
    />
    <motion.div
      animate={{ y: [0, -5, 0] }}
      transition={{ duration: 1, repeat: Infinity, delay: 0.2 }}
      className="w-2 h-2 bg-blue-500 rounded-full"
    />
    <motion.div
      animate={{ y: [0, -5, 0] }}
      transition={{ duration: 1, repeat: Infinity, delay: 0.4 }}
      className="w-2 h-2 bg-blue-500 rounded-full"
    />
  </div>
);

const SmartAIAssistant: React.FC = () => {
  const [isMinimized, setIsMinimized] = useState(false);
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputText, setInputText] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const navigate = useNavigate();

  // Scroll to bottom when messages change
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // Initial welcome message with quick actions
  useEffect(() => {
    if (messages.length === 0) {
      const welcome: Message = {
        id: Date.now(),
        text: "Hello! I'm Vedanta's AI Health Assistant. How can I help you today?",
        isBot: true,
        timestamp: new Date(),
        actions: [
          { label: 'Start Health Check', action: 'yes', icon: MessageSquare },
          { label: 'Book Appointment', action: 'book_appointment', icon: MessageSquare },
          { label: 'Find a Doctor', action: 'find_doctor', icon: MessageSquare },
        ],
      };
      setMessages([welcome]);
    }
  }, []);

  const handleSendMessage = async () => {
    if (!inputText.trim()) return;
    
    // Add user message
    const userMessage: Message = {
      id: Date.now(),
      text: inputText,
      isBot: false,
      timestamp: new Date()
    };
    
    setMessages(prev => [...prev, userMessage]);
    setInputText('');
    setIsTyping(true);
    
    try {
      // Send to Healtho service with current symptoms context
      const response = await sendMessage(inputText);
      
      // Add bot response
      const botMessage: Message = {
        id: Date.now() + 1,
        text: response.response || 'I received your message.',
        isBot: true,
        timestamp: new Date(),
        actions: Array.isArray((response as any).options)
          ? ((response as any).options as string[]).map((label) => ({
              label,
              action: label.toLowerCase(),
              icon: MessageSquare,
            }))
          : undefined,
      };
      
      setMessages(prev => [...prev, botMessage]);

      // If it's a final message (not a question), or even during questions, offer next-step suggestions
      if (!(response as any).is_question) {
        const suggestions: Message = {
          id: Date.now() + 2,
          text: 'Would you like to take any of these next steps?',
          isBot: true,
          timestamp: new Date(),
          actions: [
            { label: 'Book Appointment', action: 'book_appointment', icon: MessageSquare },
            { label: 'Find a Doctor', action: 'find_doctor', icon: MessageSquare },
          ],
        };
        setMessages((prev) => [...prev, suggestions]);
      } else {
        // During questioning, still give the user an out to take actions
        const helpNow: Message = {
          id: Date.now() + 3,
          text: 'Need help now? You can take these actions anytime:',
          isBot: true,
          timestamp: new Date(),
          actions: [
            { label: 'Book Appointment', action: 'book_appointment', icon: MessageSquare },
            { label: 'Find a Doctor', action: 'find_doctor', icon: MessageSquare },
          ],
        };
        setMessages((prev) => [...prev, helpNow]);
      }
    } catch (error) {
      console.error('Error sending message:', error);
      const errorMessage: Message = {
        id: Date.now() + 1,
        text: 'Sorry, I encountered an error. Please try again.',
        isBot: true,
        timestamp: new Date()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsTyping(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const handleQuickAction = async (action: string) => {
    // Handle quick actions like booking appointments, yes/no answers, etc.
    if (action === 'book_appointment') {
      // Navigate directly to the appointment form and minimize assistant
      setIsMinimized(true);
      navigate('/appointment');
      return;
    }

    if (action === 'find_doctor') {
      // Navigate directly to the Doctors page and minimize assistant
      setIsMinimized(true);
      navigate('/doctors');
      return;
    }

    if (action === 'yes' || action === 'no') {
      // Add user message for the quick reply
      const userMsg: Message = {
        id: Date.now(),
        text: action.charAt(0).toUpperCase() + action.slice(1),
        isBot: false,
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, userMsg]);
      setIsTyping(true);
      try {
        const response = await sendMessage(action);
        const botMessage: Message = {
          id: Date.now() + 1,
          text: response.response || 'I received your message.',
          isBot: true,
          timestamp: new Date(),
          actions: Array.isArray((response as any).options)
            ? ((response as any).options as string[]).map((label) => ({
                label,
                action: label.toLowerCase(),
                icon: MessageSquare,
              }))
            : undefined,
        };
        setMessages((prev) => [...prev, botMessage]);

        if (!(response as any).is_question) {
          const suggestions: Message = {
            id: Date.now() + 2,
            text: 'Would you like to take any of these next steps?',
            isBot: true,
            timestamp: new Date(),
            actions: [
              { label: 'Book Appointment', action: 'book_appointment', icon: MessageSquare },
              { label: 'Find a Doctor', action: 'find_doctor', icon: MessageSquare },
            ],
          };
          setMessages((prev) => [...prev, suggestions]);
        } else {
          const helpNow: Message = {
            id: Date.now() + 3,
            text: 'Need help now? You can take these actions anytime:',
            isBot: true,
            timestamp: new Date(),
            actions: [
              { label: 'Book Appointment', action: 'book_appointment', icon: MessageSquare },
              { label: 'Find a Doctor', action: 'find_doctor', icon: MessageSquare },
            ],
          };
          setMessages((prev) => [...prev, helpNow]);
        }
      } catch (err) {
        console.error('Quick action send failed:', err);
        const errorMsg: Message = {
          id: Date.now() + 3,
          text: "I'm having trouble connecting right now. Please try again.",
          isBot: true,
          timestamp: new Date(),
        };
        setMessages((prev) => [...prev, errorMsg]);
      } finally {
        setIsTyping(false);
      }
      return;
    }

    // Unknown action fallback
    const fallback: Message = {
      id: Date.now(),
      text: "I'm not sure how to help with that yet. Could you provide more details?",
      isBot: true,
      timestamp: new Date(),
    };
    setMessages((prev) => [...prev, fallback]);
  };

  // Removed appointment submit flow for now; can be reintroduced when form UI is added

  if (isMinimized) {
    return (
      <div className="fixed bottom-4 right-4 z-50">
        <button
          onClick={() => setIsMinimized(false)}
          className="bg-blue-600 text-white p-3 rounded-full shadow-lg hover:bg-blue-700 transition-colors"
        >
          <MessageSquare className="w-6 h-6" />
        </button>
      </div>
    );
  }

  return (
    <div className="fixed bottom-4 right-4 w-96 bg-white rounded-xl shadow-xl overflow-hidden flex flex-col z-50">
      {/* Header */}
      <div className="bg-gradient-to-r from-blue-600 to-blue-800 text-white p-4 flex justify-between items-center">
        <h2 className="font-semibold text-lg">Vedanta AI Assistant</h2>
        <button
          onClick={() => setIsMinimized(true)}
          className="text-white hover:bg-blue-700 p-1 rounded-full transition-colors"
        >
          <X size={20} />
        </button>
      </div>

      {/* Messages */}
      <div className="flex-1 p-4 space-y-4 overflow-y-auto h-96">
        {messages.length === 0 ? (
          <div className="flex flex-col items-center justify-center h-full text-gray-500 text-center p-4">
            <Bot size={48} className="text-blue-400 mb-4" />
            <h3 className="text-lg font-medium mb-2">How can I help you today?</h3>
            <p className="text-sm">Ask me anything about Vedanta or your health.</p>
          </div>
        ) : (
          messages.map((message) => (
            <div
              key={message.id}
              className={`flex ${message.isBot ? 'justify-start' : 'justify-end'}`}
            >
              <div
                className={`max-w-xs p-3 rounded-lg ${
                  message.isBot
                    ? 'bg-gray-100 text-gray-800 rounded-tl-none'
                    : 'bg-blue-600 text-white rounded-tr-none'
                }`}
              >
                <p className="text-sm">{message.text}</p>
                {message.actions && message.actions.filter(a => a.action !== 'book_appointment' && a.action !== 'find_doctor').length > 0 && (
                  <div className="mt-2 space-x-2">
                    {message.actions
                      .filter(a => a.action !== 'book_appointment' && a.action !== 'find_doctor')
                      .map((action, index) => (
                        <QuickAction
                          key={index}
                          icon={action.icon || MessageSquare}
                          label={action.label}
                          onClick={() => handleQuickAction(action.action)}
                          color="blue"
                        />
                      ))}
                  </div>
                )}
              </div>
            </div>
          ))
        )}
        {isTyping && <TypingIndicator />}
        <div ref={messagesEndRef} />
      </div>

      {/* Input */}
      <div className="border-t p-4 bg-gray-50">
        <form
          onSubmit={(e) => {
            e.preventDefault();
            handleSendMessage();
          }}
          className="relative"
        >
          <input
            type="text"
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Type your message..."
            className="w-full bg-white border border-gray-200 rounded-xl pl-4 pr-12 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 placeholder-gray-400"
          />
          <button
            type="submit"
            disabled={!inputText.trim() || isTyping}
            className="absolute right-2 top-1/2 -translate-y-1/2 text-blue-500 hover:text-blue-600 p-1.5 rounded-full hover:bg-blue-50 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {isTyping ? (
              <Loader2 className="w-5 h-5 animate-spin" />
            ) : (
              <Send className="w-5 h-5" />
            )}
          </button>
        </form>
      </div>
    </div>
  );
};

export default SmartAIAssistant;
