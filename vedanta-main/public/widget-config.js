/**
 * Widget Configuration Script
 * This script helps configure the Vedanta Smart Assist widget with backend API
 */

// Function to get backend API URL from multiple sources
function getBackendApiUrl() {
  // Try multiple sources for the API URL
  return (
    // From global window object
    window.VEDANTA_API_URL ||
    // From meta tag
    document.querySelector('meta[name="vedanta-api-url"]')?.content ||
    // From script data attribute
    document.querySelector('script[data-vedanta-api-url]')?.dataset.vedantaApiUrl ||
    // From localStorage (for development)
    localStorage.getItem('VEDANTA_API_URL') ||
    // Default backend URL
    'http://localhost:8002'
  );
}

// Initialize widget configuration
function initializeVedantaWidget() {
  const apiUrl = getBackendApiUrl();
  
  // Make API URL available globally for the widget
  if (typeof window !== 'undefined') {
    window.VEDANTA_API_URL = apiUrl;
  }
  
  // Initialize the widget
  if (typeof VedantaSmartAssist !== 'undefined') {
    new VedantaSmartAssist({
      apiUrl: apiUrl,
      position: 'bottom-right',
      theme: 'default',
      whatsappAware: true
    });
    console.log('Vedanta Smart Assist widget initialized with Llama 3.2 backend!');
  } else if (typeof NephroWidget !== 'undefined') {
    new NephroWidget({
      apiUrl: apiUrl,
      position: 'bottom-right',
      theme: 'default',
      whatsappAware: true
    });
    console.log('Nephro widget initialized with Llama 3.2 backend!');
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