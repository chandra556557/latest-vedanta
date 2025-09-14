import React, { useEffect } from 'react';
import { isGeminiConfigured, getGeminiConfig, testGeminiConnection } from '../services/geminiService';

const GeminiTest: React.FC = () => {
  useEffect(() => {
    console.log('🧪 GeminiTest Component Loaded');
    console.log('🌍 import.meta.env:', import.meta.env);
    console.log('🔑 VITE_GOOGLE_GEMINI_API_KEY:', import.meta.env.VITE_GOOGLE_GEMINI_API_KEY);
    console.log('🔧 Is Configured:', isGeminiConfigured());
    console.log('📊 Config Details:', getGeminiConfig());
    
    // Test connection
    testGeminiConnection().then(result => {
      console.log('🔗 Connection Test Result:', result);
    }).catch(error => {
      console.error('❌ Connection Test Error:', error);
    });
  }, []);

  const handleTestClick = async () => {
    console.log('🖱️ Test Button Clicked');
    
    // Direct environment check
    const apiKey = import.meta.env.VITE_GOOGLE_GEMINI_API_KEY;
    console.log('Direct API Key Check:', apiKey);
    
    if (!apiKey) {
      alert('❌ API Key not found in environment variables!');
      return;
    }
    
    if (apiKey === 'your_google_gemini_api_key_here') {
      alert('❌ API Key is still the placeholder value!');
      return;
    }
    
    try {
      const result = await testGeminiConnection();
      console.log('🔗 Manual Test Result:', result);
      alert(`Test Result: ${result.success ? 'Success' : 'Failed'} - ${result.message}`);
    } catch (error) {
      console.error('❌ Manual Test Error:', error);
      alert(`Test Error: ${error}`);
    }
  };

  return (
    <div style={{ position: 'fixed', top: '10px', right: '10px', zIndex: 9999, background: 'white', padding: '10px', border: '1px solid #ccc' }}>
      <h4>Gemini API Test</h4>
      <p>Configured: {isGeminiConfigured() ? '✅ Yes' : '❌ No'}</p>
      <button onClick={handleTestClick}>Test Connection</button>
    </div>
  );
};

export default GeminiTest;