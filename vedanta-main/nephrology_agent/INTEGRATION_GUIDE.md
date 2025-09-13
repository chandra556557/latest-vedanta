# Dr. Nephro - Website Integration Guide

This guide explains how to integrate the Dr. Nephro kidney health assistant into your website using three different methods.

## 🚀 Quick Start

### Prerequisites
1. **API Server Running**: Ensure the FastAPI backend is running on port 8002
2. **Google Gemini API Key**: Configure your API key in the `.env` file
3. **CORS Configuration**: The API allows all origins by default (configure for production)

### Start the API Server
```bash
cd nephrology_agent
python nephro_api.py
# Or using uvicorn
uvicorn nephro_api:app --host 0.0.0.0 --port 8002 --reload
```

## 📋 Integration Methods

### Method 1: JavaScript Widget (Recommended)

The easiest way to add Dr. Nephro to any website as a floating chat widget.

#### Basic Implementation
```html
<!DOCTYPE html>
<html>
<head>
    <title>Your Website</title>
</head>
<body>
    <!-- Your website content -->
    <h1>Welcome to Our Healthcare Website</h1>
    
    <!-- Dr. Nephro Widget -->
    <script src="path/to/nephro_widget.js"></script>
    <script>
        // Initialize the widget
        new NephroWidget({
            apiUrl: 'http://localhost:8002',
            position: 'bottom-right', // or 'bottom-left'
            theme: 'default'
        });
    </script>
</body>
</html>
```

#### Advanced Configuration
```javascript
const widget = new NephroWidget({
    apiUrl: 'https://your-api-domain.com',
    containerId: 'custom-container', // Optional: specific container
    position: 'bottom-right', // 'bottom-right' or 'bottom-left'
    theme: 'default'
});
```

#### Widget Features
- 🎨 **Responsive Design**: Works on desktop and mobile
- 💬 **Real-time Chat**: Instant responses from Dr. Nephro
- 🔔 **Notification Badge**: Shows unread messages
- 📱 **Mobile Optimized**: Adapts to smaller screens
- 🎯 **Easy Integration**: Just add two script tags

### Method 2: Iframe Embedding

Embed the full Dr. Nephro interface directly into your webpage.

#### Start the Embed Server
```bash
cd nephrology_agent
streamlit run nephro_embed.py --server.port 8503
```

#### Basic Iframe
```html
<iframe 
    src="http://localhost:8503" 
    width="100%" 
    height="600px" 
    frameborder="0"
    style="border-radius: 10px; box-shadow: 0 4px 12px rgba(0,0,0,0.1);"
    title="Dr. Nephro - Kidney Health Assistant">
</iframe>
```

#### Responsive Iframe
```html
<div style="position: relative; width: 100%; height: 0; padding-bottom: 75%;">
    <iframe 
        src="http://localhost:8503" 
        style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; border: none; border-radius: 10px;"
        title="Dr. Nephro - Kidney Health Assistant">
    </iframe>
</div>
```

#### Modal Integration
```html
<!-- Trigger Button -->
<button onclick="openNephroModal()">Chat with Dr. Nephro</button>

<!-- Modal -->
<div id="nephro-modal" style="display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.5); z-index: 9999;">
    <div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); width: 90%; max-width: 800px; height: 80%; background: white; border-radius: 10px;">
        <button onclick="closeNephroModal()" style="position: absolute; top: 10px; right: 15px; background: none; border: none; font-size: 24px; cursor: pointer;">×</button>
        <iframe 
            src="http://localhost:8503" 
            width="100%" 
            height="100%" 
            frameborder="0"
            style="border-radius: 10px;"
            title="Dr. Nephro">
        </iframe>
    </div>
</div>

<script>
function openNephroModal() {
    document.getElementById('nephro-modal').style.display = 'block';
}

function closeNephroModal() {
    document.getElementById('nephro-modal').style.display = 'none';
}
</script>
```

### Method 3: Direct API Integration

Build your own custom interface using the REST API.

#### API Endpoints

##### 1. Chat Endpoint
```javascript
// POST /chat
const response = await fetch('http://localhost:8002/chat', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({
        message: "What are the symptoms of kidney disease?",
        conversation_history: [
            {"role": "user", "content": "Hello"},
            {"role": "assistant", "content": "Hi! How can I help with kidney health?"}
        ]
    })
});

const data = await response.json();
console.log(data.response);
```

##### 2. Symptom Assessment
```javascript
// POST /assess-symptoms
const assessment = await fetch('http://localhost:8002/assess-symptoms', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({
        symptoms: ["frequent urination", "fatigue", "swelling"],
        medical_history: {
            "diabetes": true,
            "hypertension": false,
            "kidney_disease": false
        },
        age: 45,
        gender: "female"
    })
});

const result = await assessment.json();
console.log(result.assessment);
console.log(result.risk_level);
console.log(result.recommendations);
```

##### 3. Educational Content
```javascript
// POST /education
const education = await fetch('http://localhost:8002/education', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({
        topic: "Chronic Kidney Disease"
    })
});

const content = await education.json();
console.log(content.content);
console.log(content.related_topics);
```

##### 4. Available Topics
```javascript
// GET /topics
const topics = await fetch('http://localhost:8002/topics');
const topicsList = await topics.json();
console.log(topicsList.topics);
```

##### 5. Emergency Symptoms
```javascript
// GET /emergency-symptoms
const emergency = await fetch('http://localhost:8002/emergency-symptoms');
const symptoms = await emergency.json();
console.log(symptoms.emergency_symptoms);
```

#### Custom Chat Interface Example
```html
<!DOCTYPE html>
<html>
<head>
    <title>Custom Dr. Nephro Chat</title>
    <style>
        .chat-container {
            max-width: 600px;
            margin: 0 auto;
            border: 1px solid #ddd;
            border-radius: 10px;
            height: 500px;
            display: flex;
            flex-direction: column;
        }
        .messages {
            flex: 1;
            padding: 20px;
            overflow-y: auto;
        }
        .message {
            margin: 10px 0;
            padding: 10px;
            border-radius: 10px;
            max-width: 80%;
        }
        .user {
            background: #007bff;
            color: white;
            margin-left: auto;
        }
        .assistant {
            background: #f8f9fa;
            border: 1px solid #e9ecef;
        }
        .input-area {
            padding: 20px;
            border-top: 1px solid #ddd;
            display: flex;
            gap: 10px;
        }
        .input-area input {
            flex: 1;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 5px;
        }
        .input-area button {
            padding: 10px 20px;
            background: #007bff;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }
    </style>
</head>
<body>
    <div class="chat-container">
        <div class="messages" id="messages"></div>
        <div class="input-area">
            <input type="text" id="messageInput" placeholder="Ask Dr. Nephro about kidney health...">
            <button onclick="sendMessage()">Send</button>
        </div>
    </div>

    <script>
        let conversationHistory = [];

        async function sendMessage() {
            const input = document.getElementById('messageInput');
            const message = input.value.trim();
            if (!message) return;

            // Add user message to UI
            addMessage('user', message);
            input.value = '';

            try {
                const response = await fetch('http://localhost:8002/chat', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        message: message,
                        conversation_history: conversationHistory
                    })
                });

                const data = await response.json();
                addMessage('assistant', data.response);

                // Update conversation history
                conversationHistory.push({role: 'user', content: message});
                conversationHistory.push({role: 'assistant', content: data.response});

            } catch (error) {
                addMessage('assistant', 'Sorry, I\'m having trouble connecting. Please try again.');
            }
        }

        function addMessage(role, content) {
            const messagesDiv = document.getElementById('messages');
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${role}`;
            messageDiv.textContent = content;
            messagesDiv.appendChild(messageDiv);
            messagesDiv.scrollTop = messagesDiv.scrollHeight;
        }

        // Allow Enter key to send message
        document.getElementById('messageInput').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                sendMessage();
            }
        });

        // Add welcome message
        addMessage('assistant', 'Hello! I\'m Dr. Nephro, your AI kidney health assistant. How can I help you today?');
    </script>
</body>
</html>
```

## 🔧 Configuration Options

### Environment Variables
```bash
# .env file
GEMINI_API_KEY=your-google-gemini-api-key-here
```

### API Configuration
- **Default Port**: 8002
- **CORS**: Enabled for all origins (configure for production)
- **Rate Limiting**: Not implemented (add for production)

### Streamlit Embed Configuration
- **Default Port**: 8503
- **Optimized for**: Iframe embedding
- **UI Elements**: Hidden for clean embedding

## 🚀 Production Deployment

### Security Considerations
1. **API Key Security**: Never expose your Gemini API key in client-side code
2. **CORS Configuration**: Restrict origins to your domain
3. **Rate Limiting**: Implement rate limiting for API endpoints
4. **HTTPS**: Use HTTPS in production
5. **Input Validation**: Validate all user inputs

### Example Production CORS
```python
# In nephro_api.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com", "https://www.yourdomain.com"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)
```

### Docker Deployment
```dockerfile
# Dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8002
CMD ["uvicorn", "nephro_api:app", "--host", "0.0.0.0", "--port", "8002"]
```

## 📱 Mobile Optimization

All integration methods are mobile-responsive:
- **Widget**: Automatically adjusts size for mobile screens
- **Iframe**: Use responsive CSS for proper scaling
- **Custom API**: Implement responsive design in your interface

## 🔍 Troubleshooting

### Common Issues

1. **API Key Error**
   - Ensure your Google Gemini API key is correctly set in `.env`
   - Verify the API key has proper permissions

2. **CORS Errors**
   - Check that your domain is allowed in CORS configuration
   - Ensure you're making requests from the correct protocol (HTTP/HTTPS)

3. **Widget Not Loading**
   - Verify the API server is running on the correct port
   - Check browser console for JavaScript errors
   - Ensure the widget script is loaded properly

4. **Iframe Issues**
   - Check that the Streamlit embed server is running
   - Verify iframe src URL is correct
   - Some browsers block mixed content (HTTP iframe on HTTPS site)

### Health Check
Visit `http://localhost:8002/health` to verify API status.

## 📞 Support

For integration support:
1. Check the API health endpoint
2. Review browser console for errors
3. Verify all prerequisites are met
4. Test with the provided examples

## 🎯 Best Practices

1. **User Experience**
   - Always show loading states during API calls
   - Handle errors gracefully with user-friendly messages
   - Provide clear instructions for users

2. **Performance**
   - Implement caching for frequently requested topics
   - Use conversation history efficiently (limit to recent messages)
   - Consider implementing typing indicators

3. **Accessibility**
   - Ensure proper ARIA labels for screen readers
   - Maintain good color contrast
   - Support keyboard navigation

4. **Medical Compliance**
   - Always include medical disclaimers
   - Emphasize that this is for educational purposes
   - Direct users to seek professional medical advice

Choose the integration method that best fits your website's architecture and user experience requirements!