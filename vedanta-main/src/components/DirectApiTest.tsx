import React, { useState } from 'react';

const DirectApiTest: React.FC = () => {
  const [result, setResult] = useState<string>('');
  const [loading, setLoading] = useState(false);

  const testDirectApi = async () => {
    setLoading(true);
    setResult('');
    
    // Get the API key directly from environment
    const apiKey = import.meta.env.VITE_GOOGLE_GEMINI_API_KEY;
    
    if (!apiKey) {
      setResult('❌ API Key not found in environment variables!');
      setLoading(false);
      return;
    }
    
    if (apiKey === 'your_google_gemini_api_key_here') {
      setResult('❌ API Key is still the placeholder value!');
      setLoading(false);
      return;
    }
    
    setResult(`✅ API Key found: ${apiKey.substring(0, 10)}...${apiKey.substring(apiKey.length - 4)}`);
    
    try {
      // Direct API call to Google Gemini
      const response = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=${apiKey}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          contents: [{
            parts: [{
              text: 'Hello, this is a test. Please respond with "API connection successful"'
            }]
          }]
        })
      });
      
      if (!response.ok) {
        const errorText = await response.text();
        setResult(prev => prev + `\n❌ API Error: ${response.status} - ${errorText}`);
        setLoading(false);
        return;
      }
      
      const data = await response.json();
      const responseText = data.candidates?.[0]?.content?.parts?.[0]?.text || 'No response text';
      setResult(prev => prev + `\n✅ API Response: ${responseText}`);
      
    } catch (error) {
      setResult(prev => prev + `\n❌ Network Error: ${error}`);
    }
    
    setLoading(false);
  };

  return (
    <div style={{ 
      position: 'fixed', 
      top: '60px', 
      right: '10px', 
      zIndex: 9999, 
      background: 'white', 
      padding: '15px', 
      border: '1px solid #ccc',
      borderRadius: '8px',
      maxWidth: '400px',
      boxShadow: '0 2px 10px rgba(0,0,0,0.1)'
    }}>
      <h4>Direct API Test</h4>
      <button 
        onClick={testDirectApi} 
        disabled={loading}
        style={{
          padding: '8px 16px',
          backgroundColor: loading ? '#ccc' : '#007bff',
          color: 'white',
          border: 'none',
          borderRadius: '4px',
          cursor: loading ? 'not-allowed' : 'pointer'
        }}
      >
        {loading ? 'Testing...' : 'Test Direct API Call'}
      </button>
      {result && (
        <pre style={{ 
          marginTop: '10px', 
          padding: '10px', 
          backgroundColor: '#f5f5f5', 
          borderRadius: '4px',
          fontSize: '12px',
          whiteSpace: 'pre-wrap',
          maxHeight: '200px',
          overflow: 'auto'
        }}>
          {result}
        </pre>
      )}
    </div>
  );
};

export default DirectApiTest;