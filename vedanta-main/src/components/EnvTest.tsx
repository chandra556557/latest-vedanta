import { useEffect, useState } from 'react';

const EnvTest = () => {
  const [env, setEnv] = useState<any>({});
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [apiTest, setApiTest] = useState<any>(null);

  useEffect(() => {
    // Get all environment variables that start with VITE_
    const viteEnv = Object.entries(import.meta.env)
      .filter(([key]) => key.startsWith('VITE_'))
      .reduce((acc, [key, value]) => ({
        ...acc,
        [key]: key.includes('KEY') ? `${value?.toString().substring(0, 10)}...` : value
      }), {});

    setEnv(viteEnv);
    setIsLoading(false);

    // Test the Gemini API
    testGeminiApi();
  }, []);

  const testGeminiApi = async () => {
    try {
      const response = await fetch('https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=AIzaSyA8iDDI7_9A8GtPB40yyCBQ1UtXg2UvD_w', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          contents: [{
            parts: [{
              text: 'Hello, are you working?'
            }]
          }]
        })
      });

      const data = await response.json();
      setApiTest({
        status: response.status,
        statusText: response.statusText,
        data: data
      });
    } catch (error) {
      setError(error instanceof Error ? error.message : 'Unknown error occurred');
    }
  };

  if (isLoading) {
    return <div>Loading environment variables...</div>;
  }

  return (
    <div style={{ padding: '20px', fontFamily: 'monospace' }}>
      <h2>Environment Variables</h2>
      <pre>{JSON.stringify(env, null, 2)}</pre>
      
      <h2>API Test</h2>
      {error ? (
        <div style={{ color: 'red' }}>Error: {error}</div>
      ) : apiTest ? (
        <div>
          <div>Status: {apiTest.status} {apiTest.statusText}</div>
          <pre>{JSON.stringify(apiTest.data, null, 2)}</pre>
        </div>
      ) : (
        <div>Testing API connection...</div>
      )}
    </div>
  );
};

export default EnvTest;
