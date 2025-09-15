const API_BASE_URL = 'http://localhost:8000';

export interface ChatMessage {
  role: 'user' | 'assistant' | 'system';
  content: string;
  timestamp?: string;
}

export const chatWithAI = async (message: string, conversationHistory: ChatMessage[] = []) => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        message,
        conversation_history: conversationHistory,
      }),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Failed to get response from AI');
    }

    return await response.json();
  } catch (error) {
    console.error('Error in chatWithAI:', error);
    throw error;
  }
};

export const checkHealth = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/health`);
    return await response.json();
  } catch (error) {
    console.error('Error checking backend health:', error);
    throw error;
  }
};
