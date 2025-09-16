import React, { useState, useRef, useEffect } from 'react';
import { Send, Bot, X, MessageCircle } from 'lucide-react';
import { useChat } from '../contexts/ChatContext';
import { sendMessageToGemini, isGeminiConfigured, testGeminiConnection } from '../services/geminiService';
import { sendMessageToNephroAgent, isNephrologyConfigured, testNephrologyConnection } from '../services/nephrologyService';
import { getHealthTip } from '../services/healthoService';

interface Message {
  id: number;
  text: string;
  sender: 'user' | 'bot';
  isTyping?: boolean;
  isHealthTip?: boolean;
  tipCategory?: string;
  options?: string[];
}

const Chatbot = () => {
  const { isChatOpen, openChat, closeChat } = useChat();
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputValue, setInputValue] = useState('');
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Initialize with welcome message and API status
  useEffect(() => {
    if (messages.length === 0) {
      const initializeChat = async () => {
        let welcomeText = "Hello! I'm Vedanta's AI Assistant. ";
        
        // Check both AI services
        const geminiAvailable = isGeminiConfigured();
        const nephroAvailable = isNephrologyConfigured();
        
        if (nephroAvailable) {
          const nephroTest = await testNephrologyConnection();
          if (nephroTest.success) {
            welcomeText += "I'm powered by our specialized Nephrology AI (Phi model) and ready to help with kidney health questions. ";
          }
        }
        
        if (geminiAvailable) {
          const geminiTest = await testGeminiConnection();
          if (geminiTest.success) {
            welcomeText += "I also have access to Google Gemini for general health questions. ";
          }
        }
        
        if (!nephroAvailable && !geminiAvailable) {
          welcomeText += "Note: My advanced AI features are currently unavailable. I can still provide basic health tips. ";
        }
        
        welcomeText += "How can I assist you today?";
        
        const welcomeMessage: Message = {
          id: Date.now(),
          text: welcomeText,
          sender: 'bot',
          options: ['Kidney/Nephrology questions', 'General health questions', 'Get health tips', 'Contact info']
        };
        setMessages([welcomeMessage]);
      };
      
      initializeChat();
    }
  }, []);

  // Core flow for sending a user message (used by submit and quick-reply buttons)
  const sendUserMessage = async (text: string) => {
    const trimmed = text.trim();
    if (!trimmed) return;

    // Add user message
    const userMessage: Message = { 
      id: Date.now(), 
      text: trimmed, 
      sender: 'user' 
    };
    setMessages(prev => [...prev, userMessage]);

    // Show typing indicator
    const typingMessage: Message = { 
      id: Date.now() + 1, 
      text: '...', 
      sender: 'bot',
      isTyping: true 
    };
    setMessages(prev => [...prev, typingMessage]);

    try {
      const lowerInput = trimmed.toLowerCase();

      // Health tips branch
      if (
        lowerInput.includes('health tip') ||
        lowerInput.includes('healthy') ||
        lowerInput.includes('advice') ||
        lowerInput.includes('suggestion')
      ) {
        const tip = await getHealthTip();
        const botMessage: Message = {
          id: Date.now() + 2,
          text: `💡 ${tip.title}\n\n${tip.tip}${tip.details ? '\n\n' + tip.details : ''}`,
          sender: 'bot',
          isHealthTip: true,
          tipCategory: tip.category,
          options: ['Get another tip', 'Learn more about ' + tip.category]
        };
        setMessages(prev => [
          ...prev.filter(msg => !msg.isTyping),
          botMessage
        ]);
      } else if (
        // Nephrology/Kidney related queries - use Phi model
        lowerInput.includes('kidney') ||
        lowerInput.includes('nephro') ||
        lowerInput.includes('dialysis') ||
        lowerInput.includes('creatinine') ||
        lowerInput.includes('urea') ||
        lowerInput.includes('renal') ||
        lowerInput.includes('urinary') ||
        lowerInput.includes('bladder') ||
        lowerInput.includes('urine')
      ) {
        if (isNephrologyConfigured()) {
          const response = await sendMessageToNephroAgent(trimmed);
          const botMessage: Message = {
            id: Date.now() + 2,
            text: `🩺 **Nephrology AI (Phi Model):**\n\n${response.response}`,
            sender: 'bot',
            options: ['Ask another kidney question', 'Get general health info', 'Contact nephrology dept']
          };
          setMessages(prev => [
            ...prev.filter(msg => !msg.isTyping),
            botMessage
          ]);
        } else {
          // Fallback to Gemini if nephrology service unavailable
          const response = await sendMessageToGemini(trimmed);
          const botMessage: Message = {
            id: Date.now() + 2,
            text: response.response + "\n\n*Note: Specialized nephrology AI is currently unavailable.*",
            sender: 'bot',
            options: response.options
          };
          setMessages(prev => [
            ...prev.filter(msg => !msg.isTyping),
            botMessage
          ]);
        }
      } else {
        // Use Google Gemini API for other queries
        const response = await sendMessageToGemini(trimmed);
        const botMessage: Message = {
          id: Date.now() + 2,
          text: response.response,
          sender: 'bot',
          options: response.options
        };
        setMessages(prev => [
          ...prev.filter(msg => !msg.isTyping),
          botMessage
        ]);
      }
    } catch (error) {
      console.error('Error getting response:', error);
      
      // Provide more specific error messages
      let errorText = 'Sorry, I encountered an error. ';
      
      if (error instanceof TypeError && error.message.includes('fetch')) {
        errorText = "I'm currently unable to connect to my knowledge base. Please check your internet connection and try again, or contact Vedanta Hospitals directly for urgent matters.";
      } else if (error instanceof Error) {
        if (error.message.includes('403') || error.message.includes('401')) {
          errorText += 'There seems to be an authentication issue. Please contact support.';
        } else if (error.message.includes('429')) {
          errorText += 'I\'m receiving too many requests right now. Please wait a moment and try again.';
        } else {
          errorText += 'Please try again in a moment.';
        }
      } else {
        errorText += 'Please try again or contact Vedanta Hospitals for assistance.';
      }
      
      const errorMessage: Message = {
        id: Date.now() + 2,
        text: errorText,
        sender: 'bot',
        options: ['Try again', 'Get health tips', 'Contact Vedanta']
      };
      setMessages(prev => [
        ...prev.filter(msg => !msg.isTyping),
        errorMessage
      ]);
    }
  };

  // Form submit handler
  const handleSendMessage = async (e: React.FormEvent) => {
    e.preventDefault();
    const current = inputValue; // capture before clearing
    setInputValue('');
    await sendUserMessage(current);
  };

  // Quick-reply option click
  const handleOptionClick = async (option: string) => {
    await sendUserMessage(option);
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  return (
    <div className="fixed bottom-8 right-8 z-50">
      {isChatOpen ? (
        <div className="w-80 h-[500px] bg-white rounded-2xl shadow-2xl flex flex-col overflow-hidden border border-gray-200">
          {/* Header */}
          <div className="bg-gradient-to-r from-purple-600 to-indigo-600 text-white p-4 flex justify-between items-center">
            <div className="flex items-center space-x-2">
              <Bot className="h-6 w-6" />
              <h3 className="font-semibold">Vedanta AI Assistant</h3>
            </div>
            <button 
              onClick={closeChat}
              className="text-white hover:text-amber-100 transition-colors"
              aria-label="Close chat"
            >
              <X className="h-5 w-5" />
            </button>
          </div>

          {/* Messages */}
          <div className="flex-1 overflow-y-auto p-4 space-y-4 bg-gray-50">
            {messages.map((message) => (
              <div
                key={message.id}
                className={`flex ${message.sender === 'user' ? 'justify-end' : 'justify-start'} mb-4`}
              >
                <div
                  className={`max-w-[80%] rounded-2xl px-4 py-2 ${
                    message.sender === 'user' 
                      ? 'bg-blue-500 text-white' 
                      : message.isHealthTip
                        ? 'bg-green-100 text-gray-800 border-l-4 border-green-500'
                        : 'bg-gray-100 text-gray-800'
                  }`}
                >
                  <div className="whitespace-pre-wrap">{message.text}</div>

                  {message.isHealthTip && message.tipCategory && (
                    <div className="mt-1 text-xs text-gray-500">
                      Category: {message.tipCategory}
                    </div>
                  )}

                  {/* Quick reply options */}
                  {message.options && message.options.length > 0 && (
                    <div className="mt-2 flex flex-wrap gap-2">
                      {message.options.map((opt, idx) => (
                        <button
                          key={idx}
                          onClick={() => handleOptionClick(opt)}
                          className="bg-white text-gray-700 border border-gray-300 rounded-full px-3 py-1 text-xs hover:bg-gray-100"
                        >
                          {opt}
                        </button>
                      ))}
                    </div>
                  )}
                </div>
              </div>
            ))}
            <div ref={messagesEndRef} />
          </div>

          {/* Input */}
          <form onSubmit={handleSendMessage} className="p-4 border-t border-gray-200 bg-white">
            <div className="flex space-x-2">
              <input
                type="text"
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                placeholder="Ask me about Vedanta or your health..."
                className="flex-1 border border-gray-300 rounded-full px-4 py-2 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent"
              />
              <button
                type="submit"
                className="bg-purple-50 text-purple-800 px-2 py-1 rounded-full text-xs font-medium hover:bg-indigo-600 transition-colors"
                aria-label="Send message"
              >
                <Send className="h-5 w-5" />
              </button>
            </div>
          </form>
        </div>
      ) : (
        <button
          onClick={openChat}
          className="bg-gradient-to-r from-purple-600 to-indigo-600 text-white rounded-full p-4 shadow-lg hover:from-purple-700 hover:to-indigo-700 transition-all hover:scale-110"
          aria-label="Open Vedanta AI Assistant"
        >
          <MessageCircle className="h-8 w-8" />
        </button>
      )}
    </div>
  );
};

export default Chatbot;
