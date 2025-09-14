// Debug script to test Gemini API key loading
import { isGeminiConfigured, getGeminiConfig } from './services/geminiService';

console.log('🚀 Debug Gemini Configuration:');
console.log('🔧 Is Configured:', isGeminiConfigured());
console.log('📊 Config Details:', getGeminiConfig());
console.log('🌍 Environment Variables:', {
  VITE_GOOGLE_GEMINI_API_KEY: import.meta.env.VITE_GOOGLE_GEMINI_API_KEY,
  hasKey: !!import.meta.env.VITE_GOOGLE_GEMINI_API_KEY,
  keyLength: import.meta.env.VITE_GOOGLE_GEMINI_API_KEY?.length || 0
});