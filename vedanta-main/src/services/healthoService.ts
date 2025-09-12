import { ChatResponse } from '../types/healtho';

// Types for health tips
type HealthTip = {
  id: number;
  category: string;
  title: string;
  tip: string;
  details?: string;
  source?: string;
  tags?: string[];
  priority?: 'high' | 'medium' | 'low';
};

// Point to the backend server; use env var if provided
const API_BASE_URL = import.meta.env.VITE_HEALTHO_API_BASE_URL || 'http://localhost:3001/api';

/**
 * Send a message to the Healtho chatbot
 * @param message The user's message
 * @param symptoms Current list of symptoms collected so far
 * @returns The chatbot's response
 */
export const sendMessage = async (
  message: string
): Promise<ChatResponse> => {
  try {
    const response = await fetch(`${API_BASE_URL}/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        messages: [
          {
            role: 'user',
            content: message
          }
        ]
      }),
    });

    if (!response.ok) {
      throw new Error(`Error: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error('Error sending message to Healtho API:', error);
    return {
      response: "I'm having trouble connecting to the health assistant. Please try again later.",
      is_question: false
    };
  }
};

/**
 * Check if the Healtho API is available
 * @returns Promise that resolves to true if the API is available
 */
export const checkHealthoHealth = async (): Promise<boolean> => {
  try {
    const response = await fetch(`${API_BASE_URL}/health`);
    return response.ok;
  } catch (error) {
    console.error('Health check failed:', error);
    return false;
  }
};

/**
 * Get a random health tip
 * @param category Optional filter for specific category of tips
 * @returns A health tip object
 */
export const getHealthTip = async (category?: string): Promise<HealthTip> => {
  const tips: HealthTip[] = [
    {
      id: 1,
      title: 'Stay Hydrated',
      category: 'Hydration',
      tip: 'Drink at least 8 glasses of water daily to stay properly hydrated.',
      details: 'Proper hydration is essential for maintaining healthy body functions, including temperature regulation and joint lubrication.',
      source: 'WHO Guidelines',
      tags: ['water', 'hydration', 'health'],
      priority: 'high'
    },
    {
      id: 2,
      title: 'Quality Sleep Matters',
      category: 'Sleep',
      tip: 'Aim for 7-9 hours of quality sleep each night for optimal health and cognitive function.',
      details: 'Consistent, restful sleep helps with memory consolidation, immune function, and overall well-being.',
      tags: ['sleep', 'rest', 'recovery'],
      priority: 'high'
    },
    {
      id: 3,
      title: 'Regular Exercise',
      category: 'Exercise',
      tip: 'Incorporate at least 30 minutes of moderate exercise into your daily routine.',
      details: 'Regular physical activity can help prevent chronic diseases and improve mental health.',
      tags: ['fitness', 'activity', 'health'],
      priority: 'high'
    },
    {
      id: 4,
      title: 'Balanced Nutrition',
      category: 'Nutrition',
      tip: 'Eat a balanced diet with plenty of fruits, vegetables, and whole grains.',
      details: 'A varied diet provides essential nutrients your body needs to function properly.',
      tags: ['diet', 'nutrition', 'healthy eating'],
      priority: 'high'
    },
    {
      id: 5,
      title: 'Mindfulness Practice',
      category: 'Mental Health',
      tip: 'Practice mindfulness or meditation for 10 minutes daily to reduce stress.',
      details: 'Mindfulness can help reduce anxiety, improve focus, and enhance emotional well-being.',
      tags: ['mental health', 'stress relief', 'meditation'],
      priority: 'medium'
    },
    {
      id: 6,
      title: 'Hygiene First',
      category: 'Prevention',
      tip: 'Wash your hands frequently with soap and water for at least 20 seconds.',
      details: 'Proper hand hygiene is one of the most effective ways to prevent the spread of infections.',
      tags: ['hygiene', 'prevention', 'health'],
      priority: 'high'
    },
    {
      id: 7,
      title: 'Eye Care',
      category: 'Screen Time',
      tip: 'Take a 20-second break from screens every 20 minutes to rest your eyes.',
      details: 'Following the 20-20-20 rule can help prevent digital eye strain and fatigue.',
      tags: ['eye health', 'screen time', 'prevention'],
      priority: 'medium'
    },
    {
      id: 8,
      title: 'Posture Check',
      category: 'Posture',
      tip: 'Maintain good posture to prevent back and neck pain, especially when sitting for long periods.',
      details: 'Proper alignment reduces strain on your spine and can prevent chronic pain.',
      tags: ['ergonomics', 'back pain', 'workplace health'],
      priority: 'medium'
    }
  ];

  // Filter by category if provided
  const filteredTips = category 
    ? tips.filter(tip => tip.category.toLowerCase() === category.toLowerCase())
    : tips;

  // Return a random tip from the filtered list
  const randomIndex = Math.floor(Math.random() * filteredTips.length);
  return filteredTips[randomIndex];
};

/**
 * Get all available health tip categories
 * @returns Array of unique health tip categories
 */
export const getHealthTipCategories = (): string[] => {
  return [
    'All',
    'Hydration',
    'Sleep',
    'Exercise',
    'Nutrition',
    'Mental Health',
    'Prevention',
    'Screen Time',
    'Posture'
  ];
};
