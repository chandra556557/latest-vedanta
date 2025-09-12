import React, { createContext, useContext, useState } from 'react';

interface ChatContextType {
  isChatOpen: boolean;
  openChat: () => void;
  closeChat: () => void;
}

const ChatContext = createContext<ChatContextType | undefined>(undefined);

export const ChatProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [isChatOpen, setIsChatOpen] = useState(false);

  const openChat = () => {
    setIsChatOpen(true);
    // Add any additional logic when chat opens
  };

  const closeChat = () => {
    setIsChatOpen(false);
    // Add any additional logic when chat closes
  };

  return (
    <ChatContext.Provider value={{ isChatOpen, openChat, closeChat }}>
      {children}
    </ChatContext.Provider>
  );
};

export const useChat = (): ChatContextType => {
  const context = useContext(ChatContext);
  if (!context) {
    throw new Error('useChat must be used within a ChatProvider');
  }
  return context;
};
