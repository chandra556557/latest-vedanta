// Predefined responses for the Vedanta AI Assistant
const RESPONSES = {
  // Greetings
  greeting: [
    "Hello! I'm Vedanta's AI Assistant. How can I help you today?",
    "Hi there! Welcome to Vedanta. How may I assist you?",
    "Greetings! I'm here to help with any questions about Vedanta."
  ],
  
  // Appointments
  appointment: [
    "I can help you book an appointment. Our available hours are Monday to Friday, 9 AM to 6 PM. When would you like to schedule?",
    "To book an appointment, please provide your preferred date and time. We're available weekdays from 9 AM to 6 PM.",
    "I'd be happy to assist with your appointment. Could you let me know your preferred day and time?"
  ],
  
  // Doctor Information
  doctor_info: [
    "We have specialists in various fields. Could you tell me what kind of specialist you're looking for?",
    "Our team includes experts in cardiology, neurology, and general medicine. Who would you like to see?",
    "We can help you find the right specialist. Could you share what kind of medical assistance you need?"
  ],
  
  // Services
  services: [
    "We offer a range of healthcare services including general check-ups, specialist consultations, and diagnostic tests.",
    "Our services include primary care, specialty care, diagnostic imaging, and laboratory services.",
    "We provide comprehensive healthcare services. Could you let me know what specific service you're interested in?"
  ],
  
  // Location
  location: [
    "Our main clinic is located at 123 Healthcare Ave, Medical District, City. We're open Monday to Friday, 9 AM to 6 PM.",
    "You can find us at 123 Healthcare Ave. We're in the Medical District, near City Hospital.",
    "Our address is 123 Healthcare Ave, Medical District, City. Would you like directions?"
  ],
  
  // Contact
  contact: [
    "You can reach us at (123) 456-7890 or email info@vedanta.com. Our team is available to assist you.",
    "For general inquiries, call (123) 456-7890. For appointments, please use our online booking system.",
    "Contact us at (123) 456-7890 during business hours or email support@vedanta.com anytime."
  ],
  
  // Default fallback
  default: [
    "I'm not sure I understand. Could you please rephrase your question?",
    "I want to make sure I help you correctly. Could you provide more details?",
    "I'm here to help. Could you tell me more about what you're looking for?"
  ]
};

// Response patterns to match user queries
const RESPONSE_PATTERNS = [
  {
    patterns: [/hello|hi|hey|greetings|good morning|good afternoon|good evening/i],
    responseKey: 'greeting'
  },
  {
    patterns: [/appointment|schedule|book a visit|make an appointment/i],
    responseKey: 'appointment'
  },
  {
    patterns: [/doctor|specialist|physician|cardiologist|neurologist|dermatologist/i],
    responseKey: 'doctor_info'
  },
  {
    patterns: [/services|what do you offer|treatments|procedures/i],
    responseKey: 'services'
  },
  {
    patterns: [/location|address|where are you|how to get there|directions/i],
    responseKey: 'location'
  },
  {
    patterns: [/contact|phone|email|call|reach|get in touch/i],
    responseKey: 'contact'
  }
];

// Helper function to get a random response from an array
const getRandomResponse = (responses: string[]): string => {
  return responses[Math.floor(Math.random() * responses.length)];
};

// Helper function to find the best matching response
const findBestMatch = (prompt: string): string => {
  const lowerPrompt = prompt.toLowerCase();
  
  // Check for direct matches first
  for (const { patterns, responseKey } of RESPONSE_PATTERNS) {
    if (patterns.some(pattern => pattern.test(lowerPrompt))) {
      return getRandomResponse(RESPONSES[responseKey as keyof typeof RESPONSES] || RESPONSES.default);
    }
  }
  
  // If no direct match, check for keywords
  for (const { patterns, responseKey } of RESPONSE_PATTERNS) {
    for (const pattern of patterns) {
      if (lowerPrompt.includes(pattern.source.replace(/[^a-z0-9\s]/gi, '').trim())) {
        return getRandomResponse(RESPONSES[responseKey as keyof typeof RESPONSES] || RESPONSES.default);
      }
    }
  }
  
  // Return a default response if no match found
  return getRandomResponse(RESPONSES.default);
};

/**
 * Generate a response using predefined patterns
 * @param prompt The user's message
 * @param chatHistory Previous conversation history (not used in rule-based system)
 * @returns Generated response
 */
export const generateResponse = async (prompt: string, chatHistory: Array<{role: 'user' | 'model', parts: string}>) => {
  try {
    // Find the best matching response based on the prompt
    return findBestMatch(prompt);
  } catch (error) {
    console.error('Error generating response:', error);
    return getRandomResponse(RESPONSES.default);
  }
};

/**
 * Generate a quick response for common queries
 * @param queryType Type of query (e.g., 'greeting', 'appointment', 'doctor_info')
 * @param context Additional context for the query (not used in rule-based system)
 * @returns Generated response
 */
export const generateQuickResponse = async (queryType: string, context?: any) => {
  try {
    // Get a random response for the given query type
    const responses = RESPONSES[queryType as keyof typeof RESPONSES] || RESPONSES.default;
    return getRandomResponse(Array.isArray(responses) ? responses : [responses]);
  } catch (error) {
    console.error('Error generating quick response:', error);
    return getRandomResponse(RESPONSES.default);
  }
};
