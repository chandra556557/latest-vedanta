import { ChatResponse } from '../types/healtho';

// Google Gemini API configuration
const GEMINI_API_KEY = import.meta.env.VITE_GOOGLE_GEMINI_API_KEY;
const GEMINI_API_URL = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent';

// Enhanced debug logging
console.log('🔍 Gemini Service Debug - Environment Variables Start 🔍');
console.log('VITE_GOOGLE_GEMINI_API_KEY exists:', 'VITE_GOOGLE_GEMINI_API_KEY' in import.meta.env);
console.log('All Vite env variables:', Object.keys(import.meta.env)
  .filter(key => key.startsWith('VITE_'))
  .reduce((obj, key) => ({
    ...obj,
    [key]: key.includes('KEY') ? '***REDACTED***' : import.meta.env[key]
  }), {}));

const debugInfo = {
  rawKey: GEMINI_API_KEY ? '***REDACTED***' : 'NOT FOUND',
  keyLength: GEMINI_API_KEY?.length || 0,
  keyType: typeof GEMINI_API_KEY,
  isConfigured: !!(GEMINI_API_KEY && GEMINI_API_KEY !== 'your_google_gemini_api_key_here'),
  allEnvKeys: Object.keys(import.meta.env).filter(key => key.startsWith('VITE_'))
};

console.log('🔍 Gemini Service Debug:', JSON.stringify(debugInfo, null, 2));
console.log('🔍 Gemini Service Debug - Environment Variables End 🔍');

// Also try to send this info to server if possible
if (typeof window !== 'undefined') {
  (window as any).geminiDebugInfo = debugInfo;
}

interface GeminiRequest {
  contents: {
    parts: {
      text: string;
    }[];
  }[];
  generationConfig?: {
    temperature?: number;
    topK?: number;
    topP?: number;
    maxOutputTokens?: number;
  };
}

interface GeminiResponse {
  candidates: {
    content: {
      parts: {
        text: string;
      }[];
    };
    finishReason: string;
  }[];
}

/**
 * Send a message to Google Gemini API directly from frontend
 * @param message The user's message
 * @returns The chatbot's response
 */
export const sendMessageToGemini = async (message: string): Promise<ChatResponse> => {
  // Check if API key is configured
  console.log('🔍 API Key Check:', {
    hasKey: !!GEMINI_API_KEY,
    keyValue: GEMINI_API_KEY,
    keyLength: GEMINI_API_KEY?.length,
    isPlaceholder: GEMINI_API_KEY === 'your_google_gemini_api_key_here'
  });
  
  if (!GEMINI_API_KEY || GEMINI_API_KEY === 'your_google_gemini_api_key_here') {
    return {
      response: `⚠️ Google Gemini API key is not configured. Debug: hasKey=${!!GEMINI_API_KEY}, keyLength=${GEMINI_API_KEY?.length || 0}, keyType=${typeof GEMINI_API_KEY}`,
      is_question: false
    };
  }

  try {
    // Prepare the request with medical context
    const systemPrompt = `You are a helpful medical AI assistant for Vedanta Hospitals. You provide general health information and guidance, but always remind users to consult healthcare professionals for serious medical concerns. Keep responses concise, helpful, and professional. Focus on:
    - General health tips and wellness advice
    - Basic medical information and explanations
    - Preventive care recommendations
    - When to seek professional medical help
    
    Always include appropriate medical disclaimers when giving health advice.`;
    
    const requestBody: GeminiRequest = {
      contents: [
        {
          parts: [
            {
              text: `${systemPrompt}\n\nUser question: ${message}`
            }
          ]
        }
      ],
      generationConfig: {
        temperature: 0.7,
        topK: 40,
        topP: 0.95,
        maxOutputTokens: 1024
      }
    };

    const response = await fetch(`${GEMINI_API_URL}?key=${GEMINI_API_KEY}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(requestBody)
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      console.error('Gemini API error:', errorData);
      
      if (response.status === 400) {
        return {
          response: "I'm having trouble understanding your request. Could you please rephrase it?",
          is_question: false
        };
      } else if (response.status === 403) {
        return {
          response: "⚠️ API access denied. Please check your Google Gemini API key and permissions.",
          is_question: false
        };
      } else {
        throw new Error(`API request failed with status ${response.status}`);
      }
    }

    const data: GeminiResponse = await response.json();
    
    if (!data.candidates || data.candidates.length === 0) {
      return {
        response: "I'm sorry, I couldn't generate a response. Please try again with a different question.",
        is_question: false
      };
    }

    const generatedText = data.candidates[0].content.parts[0].text;
    
    // Add medical disclaimer if the response contains medical advice
    const medicalKeywords = ['symptom', 'treatment', 'medicine', 'diagnosis', 'disease', 'condition', 'pain', 'health'];
    const containsMedicalContent = medicalKeywords.some(keyword => 
      generatedText.toLowerCase().includes(keyword) || message.toLowerCase().includes(keyword)
    );
    
    let finalResponse = generatedText;
    if (containsMedicalContent && !generatedText.toLowerCase().includes('consult')) {
      finalResponse += "\n\n⚠️ *This information is for educational purposes only. Please consult with a healthcare professional for personalized medical advice.*";
    }

    return {
      response: finalResponse,
      is_question: false,
      options: ['Ask another question', 'Get health tips', 'Contact Vedanta Hospitals']
    };

  } catch (error) {
    console.error('Error calling Gemini API:', error);
    return {
      response: "I'm experiencing technical difficulties. Please try again later or contact our support team.",
      is_question: false
    };
  }
};

/**
 * Check if Google Gemini API is properly configured
 * @returns boolean indicating if API key is available
 */
export const isGeminiConfigured = (): boolean => {
  return !!(GEMINI_API_KEY && GEMINI_API_KEY !== 'your_google_gemini_api_key_here');
};

/**
 * Get configuration status for debugging
 * @returns object with configuration details
 */
export const getGeminiConfig = () => {
  return {
    hasApiKey: !!GEMINI_API_KEY,
    isConfigured: isGeminiConfigured(),
    apiUrl: GEMINI_API_URL
  };
};

/**
 * Test the Google Gemini API connection
 * @returns Promise with connection test results
 */
export const testGeminiConnection = async (): Promise<{success: boolean, message: string, error?: any}> => {
  console.log('🔍 Testing Gemini Connection...');
  console.log('🔑 API Key configured:', !!GEMINI_API_KEY);
  console.log('🔗 API URL:', GEMINI_API_URL);
  console.log('🌐 Environment check:', {
    hasViteKey: !!import.meta.env.VITE_GOOGLE_GEMINI_API_KEY,
    keyLength: GEMINI_API_KEY?.length || 0
  });
  
  if (!isGeminiConfigured()) {
    console.error('❌ API key not configured');
    return {
      success: false,
      message: "Google Gemini API key is not configured"
    };
  }

  try {
    const testRequest: GeminiRequest = {
      contents: [
        {
          parts: [
            {
              text: "Hello, this is a connection test. Please respond with 'Connection successful'."
            }
          ]
        }
      ],
      generationConfig: {
        temperature: 0.1,
        maxOutputTokens: 50
      }
    };

    console.log('📤 Sending test request to:', `${GEMINI_API_URL}?key=${GEMINI_API_KEY?.substring(0, 10)}...`);
    const response = await fetch(`${GEMINI_API_URL}?key=${GEMINI_API_KEY}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(testRequest)
    });
    
    console.log('📥 Response status:', response.status);
    console.log('📥 Response headers:', Object.fromEntries(response.headers.entries()));

    if (!response.ok) {
      const errorText = await response.text().catch(() => 'Unable to read error response');
      console.error('❌ API Error Response:', errorText);
      let errorData;
      try {
        errorData = JSON.parse(errorText);
        console.error('❌ Parsed Error Data:', errorData);
      } catch (e) {
        console.error('❌ Could not parse error as JSON');
        errorData = { rawError: errorText };
      }
      return {
        success: false,
        message: `API request failed with status ${response.status}: ${errorText.substring(0, 100)}`,
        error: errorData
      };
    }

    const data: GeminiResponse = await response.json();
    console.log('✅ API Response received:', data);
    
    if (!data.candidates || data.candidates.length === 0) {
      console.error('❌ No candidates in response');
      return {
        success: false,
        message: "No response candidates received from API"
      };
    }

    console.log('✅ Connection test successful!');
    return {
      success: true,
      message: "Connection successful - Google Gemini API is working properly"
    };

  } catch (error) {
    console.error('❌ Network or other error:', error);
    return {
      success: false,
      message: `Network error or API unavailable: ${error instanceof Error ? error.message : 'Unknown error'}`,
      error: error
    };
  }
};

// Legacy functions for backward compatibility
export const generateResponse = async (prompt: string, chatHistory: Array<{role: 'user' | 'model', parts: string}>) => {
  const response = await sendMessageToGemini(prompt);
  return response.response;
};

export const generateQuickResponse = async (queryType: string, context?: any) => {
  const response = await sendMessageToGemini(queryType);
  return response.response;
};
