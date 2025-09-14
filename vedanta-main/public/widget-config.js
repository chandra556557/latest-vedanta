/**
 * Widget Configuration Script
 * This script helps configure the Vedanta Smart Assist widget with environment variables
 */

// Function to get Gemini API key from multiple sources
function getGeminiApiKey() {
  // Try multiple sources for the API key
  return (
    // From global window object (set by Vite during build)
    window.VITE_GOOGLE_GEMINI_API_KEY ||
    // From meta tag
    document.querySelector('meta[name="gemini-api-key"]')?.content ||
    // From script data attribute
    document.querySelector('script[data-vite-google-gemini-api-key]')?.dataset.viteGoogleGeminiApiKey ||
    // From localStorage (for development)
    localStorage.getItem('VITE_GOOGLE_GEMINI_API_KEY') ||
    // Fallback placeholder
    'your_google_gemini_api_key_here'
  );
}

// Initialize widget configuration
function initializeVedantaWidget() {
  const geminiApiKey = getGeminiApiKey();
  
  // Make API key available globally for the widget
  if (typeof window !== 'undefined') {
    window.VITE_GOOGLE_GEMINI_API_KEY = geminiApiKey;
  }
  
  // Initialize the widget
  if (typeof VedantaSmartAssist !== 'undefined') {
    new VedantaSmartAssist({
      geminiApiKey: geminiApiKey,
      position: 'bottom-right',
      theme: 'default',
      whatsappAware: true
    });
    console.log('Vedanta Smart Assist widget initialized with frontend-only mode!');
  } else if (typeof NephroWidget !== 'undefined') {
    new NephroWidget({
      geminiApiKey: geminiApiKey,
      position: 'bottom-right',
      theme: 'default',
      whatsappAware: true
    });
    console.log('Nephro widget initialized with frontend-only mode!');
  } else {
    console.error('Widget class not found. Make sure nephro_widget.js is loaded first.');
  }
}

// Auto-initialize when DOM is ready
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initializeVedantaWidget);
} else {
  initializeVedantaWidget();
}

// Export for manual initialization
if (typeof window !== 'undefined') {
  window.initializeVedantaWidget = initializeVedantaWidget;
}