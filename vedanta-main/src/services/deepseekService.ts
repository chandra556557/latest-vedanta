const API_BASE_URL = 'http://localhost:3001/api';

interface Message {
  role: 'user' | 'assistant' | 'system';
  content: string;
}

export const sendMessageToPerplexity = async (messages: Message[]) => {
  try {
    const response = await fetch(`${API_BASE_URL}/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ messages }),
    });

    if (!response.ok) {
      const errorData = await response.json();
      console.error('API error:', errorData);
      throw new Error(errorData.error || 'Failed to get response from the AI service');
    }

    const data = await response.json();
    return data.choices[0]?.message?.content || 'I received an empty response. Could you please rephrase your question?';
  } catch (error) {
    console.error('Error calling backend API:', error);
    throw error;
  }
};

export const processUserQuery = async (query: string, context: Message[] = []) => {
  const messages: Message[] = [
    {
      role: 'system',
      content: 'You are Vedanta AI Assistant, a helpful and knowledgeable AI trained to provide information about Vedanta philosophy, meditation, and spiritual practices. Be concise, clear, and maintain a friendly, professional tone.'
    },
    ...context,
    { 
      role: 'system',
      content: 'You are also Vedanta Hospitals AI Assistant. Provide helpful, accurate, and concise medical information. For serious medical concerns, always recommend consulting a healthcare professional.'
    },
    { 
      role: 'user', 
      content: query 
    }
  ];

  return await sendMessageToPerplexity(messages);
};
