import { ChatResponse } from '../types/healtho';

const API_BASE_URL = import.meta.env.VITE_HEALTHO_API_BASE_URL || 'http://localhost:3001/api';

export const sendFitnessMessage = async (message: string): Promise<ChatResponse> => {
  try {
    const response = await fetch(`${API_BASE_URL}/fitness/chat`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        messages: [
          { role: 'user', content: message }
        ]
      })
    });

    if (!response.ok) throw new Error(`Error: ${response.status}`);
    return await response.json();
  } catch (error) {
    console.error('Error sending message to Fitness API:', error);
    return {
      response: "I'm having trouble connecting to the fitness assistant. Please try again later.",
      is_question: false
    };
  }
};