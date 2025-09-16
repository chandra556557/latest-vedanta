import { ChatResponse } from '../types/healtho';

// Nephrology API Configuration - connects to our backend on port 8002
const NEPHRO_API_BASE_URL = import.meta.env.VITE_NEPHRO_API_BASE_URL || 'http://localhost:8002';

interface ChatMessage {
  role: string;
  content: string;
  timestamp?: string;
}

interface ChatRequest {
  message: string;
  conversation_history?: ChatMessage[];
}

interface NephroChatResponse {
  response: string;
  timestamp: string;
  conversation_id?: string;
}

/**
 * Send a message to the Nephrology AI Agent (Phi model)
 * @param message The user's message
 * @param conversationHistory Optional conversation history
 * @returns The AI agent's response
 */
export const sendMessageToNephroAgent = async (
  message: string, 
  conversationHistory: ChatMessage[] = []
): Promise<ChatResponse> => {
  try {
    const requestBody: ChatRequest = {
      message,
      conversation_history: conversationHistory
    };

    const response = await fetch(`${NEPHRO_API_BASE_URL}/api/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(requestBody)
    });

    if (!response.ok) {
      const errorData = await response.text();
      console.error('Nephrology API error:', response.status, errorData);
      throw new Error(`Nephrology API error: ${response.status}`);
    }

    const data: NephroChatResponse = await response.json();
    
    return {
      response: data.response,
      is_question: false // You can enhance this based on your needs
    };
  } catch (error) {
    console.error('Error calling Nephrology API:', error);
    
    // Provide helpful error messages
    if (error instanceof TypeError && error.message.includes('fetch')) {
      return {
        response: "I'm currently unable to connect to the nephrology AI service. Please check if the backend server is running on port 8002, or try again in a moment.",
        is_question: false
      };
    }
    
    return {
      response: "I'm experiencing technical difficulties. Please try again in a moment or contact Vedanta Hospitals directly for urgent nephrology concerns.",
      is_question: false
    };
  }
};

/**
 * Check if the Nephrology API is available
 * @returns Promise that resolves to true if the API is available
 */
export const checkNephrologyHealth = async (): Promise<boolean> => {
  try {
    const response = await fetch(`${NEPHRO_API_BASE_URL}/health`);
    return response.ok;
  } catch (error) {
    console.error('Nephrology health check failed:', error);
    return false;
  }
};

/**
 * Test connection to the Nephrology API
 * @returns Promise with connection test results
 */
export const testNephrologyConnection = async (): Promise<{ success: boolean; message: string }> => {
  try {
    const response = await fetch(`${NEPHRO_API_BASE_URL}/health`);
    
    if (response.ok) {
      return {
        success: true,
        message: 'Successfully connected to Nephrology AI Agent (Phi model)'
      };
    } else {
      return {
        success: false,
        message: `Nephrology API returned status: ${response.status}`
      };
    }
  } catch (error) {
    return {
      success: false,
      message: `Failed to connect to Nephrology API: ${error instanceof Error ? error.message : 'Unknown error'}`
    };
  }
};

/**
 * Check if the Nephrology service is configured
 * @returns boolean indicating if the service is properly configured
 */
export const isNephrologyConfigured = (): boolean => {
  return !!NEPHRO_API_BASE_URL;
};