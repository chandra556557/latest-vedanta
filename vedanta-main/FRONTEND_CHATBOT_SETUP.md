# Frontend-Only Chatbot Setup

The Vedanta Smart Assist chatbot has been configured to work entirely in the frontend using Google Gemini API directly, eliminating the need for a backend server.

## Configuration

### 1. API Key Setup

Add your Google Gemini API key to the `.env` file:

```env
VITE_GOOGLE_GEMINI_API_KEY=your_actual_google_gemini_api_key_here
```

### 2. Get Your API Key

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Copy the key and add it to your `.env` file

### 3. How It Works

The chatbot now:
- ✅ Works entirely in the frontend
- ✅ Uses Google Gemini API directly
- ✅ No backend server required
- ✅ Provides medical information with appropriate disclaimers
- ✅ Handles errors gracefully

## Files Modified

### `public/nephro_widget.js`
- Removed dependency on `localhost:8002` backend
- Added direct Google Gemini API integration
- Enhanced error handling for API responses
- Added medical context prompting

### `public/widget-config.js` (New)
- Handles environment variable configuration
- Provides clean widget initialization
- Supports multiple API key sources

### `index.html`
- Updated widget initialization
- Removed backend API URL configuration
- Added environment variable passing

## Usage

### Basic Integration

```html
<!-- Include the widget files -->
<script src="/nephro_widget.js"></script>
<script src="/widget-config.js"></script>

<!-- The widget will auto-initialize with your API key -->
```

### Manual Integration

```javascript
// Initialize manually with custom options
new VedantaSmartAssist({
  geminiApiKey: 'your_api_key_here',
  position: 'bottom-right',
  theme: 'default',
  whatsappAware: true
});
```

### Alternative API Key Methods

1. **Meta Tag Method:**
```html
<meta name="gemini-api-key" content="your_api_key_here">
```

2. **Global Variable Method:**
```javascript
window.VITE_GOOGLE_GEMINI_API_KEY = 'your_api_key_here';
```

3. **Script Data Attribute Method:**
```html
<script src="/nephro_widget.js" data-vite-google-gemini-api-key="your_api_key_here"></script>
```

## Features

- **Medical Context**: Provides health information with appropriate disclaimers
- **Error Handling**: Graceful handling of API errors and network issues
- **Responsive Design**: Works on all device sizes
- **Professional UI**: Clean, modern interface matching Vedanta branding
- **Security**: API key is only used client-side for direct API calls

## Benefits of Frontend-Only Approach

1. **No Backend Required**: Eliminates server maintenance and hosting costs
2. **Faster Setup**: No need to configure and run backend services
3. **Direct API Access**: Faster response times with direct API calls
4. **Simplified Deployment**: Just deploy static files
5. **Better Reliability**: No backend server downtime issues

## Security Considerations

- API keys are visible in the frontend code
- Consider using API key restrictions in Google Cloud Console
- Limit API key usage to specific domains in production
- Monitor API usage to prevent abuse

## Troubleshooting

### Widget Not Appearing
- Check that both script files are loaded
- Verify API key is configured correctly
- Check browser console for errors

### API Errors
- Verify API key is valid and active
- Check API key permissions in Google Cloud Console
- Ensure you haven't exceeded rate limits

### Network Issues
- Check internet connection
- Verify CORS settings if hosting on different domain
- Check browser network tab for failed requests

## Support

For issues or questions:
1. Check browser console for error messages
2. Verify API key configuration
3. Test with a simple HTML page first
4. Contact Vedanta Hospitals technical support