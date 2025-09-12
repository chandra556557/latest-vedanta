// Deepseek API Configuration

interface DeepseekConfig {
  apiKey: string;
  baseUrl: string;
  model: string;
  maxTokens: number;
  temperature: number;
}

// These values should be set in your environment variables
const config: DeepseekConfig = {
  apiKey: process.env.REACT_APP_DEEPSEEK_API_KEY || '',
  baseUrl: process.env.REACT_APP_DEEPSEEK_BASE_URL || 'https://api.deepseek.com/v1',
  model: 'deepseek-chat',
  maxTokens: 1000,
  temperature: 0.7,
};

export default config;
