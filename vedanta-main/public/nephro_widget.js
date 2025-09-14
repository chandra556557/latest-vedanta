/**
 * Vedanta Smart Assist Widget
 * Advanced AI-powered healthcare assistant for website integration
 */

class VedantaSmartAssist {
    constructor(options = {}) {
        // Use Gemini API directly instead of backend
        this.geminiApiKey = options.geminiApiKey || this.getGeminiApiKey();
        this.geminiApiUrl = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent';
        this.containerId = options.containerId || 'vedanta-widget';
        this.theme = options.theme || 'vedanta';
        this.position = options.position || 'bottom-right';
        this.whatsappAware = options.whatsappAware || false;
        this.isOpen = false;
        this.messages = [];
        this.isTyping = false;
        
        this.init();
    }
    
    getGeminiApiKey() {
        // Try to get API key from various sources
        if (typeof window !== 'undefined') {
            // From global config
            if (window.VITE_GOOGLE_GEMINI_API_KEY) {
                return window.VITE_GOOGLE_GEMINI_API_KEY;
            }
            // From meta tag
            const metaTag = document.querySelector('meta[name="gemini-api-key"]');
            if (metaTag) {
                return metaTag.getAttribute('content');
            }
        }
        return null;
    }
    
    init() {
        this.createWidget();
        this.attachEventListeners();
        this.addWelcomeMessage();
    }
    
    createWidget() {
        // Create widget container
        const widgetContainer = document.createElement('div');
        widgetContainer.id = 'vedanta-widget-container';
        const whatsappClass = this.whatsappAware ? ' whatsapp-aware' : '';
        widgetContainer.className = `vedanta-widget ${this.position}${whatsappClass}`;
        
        widgetContainer.innerHTML = `
            <div class="vedanta-widget-toggle" id="vedanta-toggle">
                <div class="vedanta-toggle-icon">
                    <svg width="28" height="28" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M12 2L13.09 8.26L22 9L13.09 9.74L12 16L10.91 9.74L2 9L10.91 8.26L12 2Z" fill="white"/>
                        <circle cx="12" cy="12" r="3" fill="white" opacity="0.8"/>
                    </svg>
                </div>
                <div class="vedanta-pulse-ring"></div>
                <span class="vedanta-widget-badge" id="vedanta-badge" style="display: none;">1</span>
            </div>
            
            <div class="vedanta-widget-chat" id="vedanta-chat" style="display: none;">
                <div class="vedanta-widget-header">
                    <div class="vedanta-header-content">
                        <div class="vedanta-avatar">
                            <div class="vedanta-avatar-inner">
                                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                                    <path d="M12 2L13.09 8.26L22 9L13.09 9.74L12 16L10.91 9.74L2 9L10.91 8.26L12 2Z" fill="#C9A227"/>
                                </svg>
                            </div>
                        </div>
                        <div class="vedanta-header-text">
                            <h4>Vedanta Smart Assist</h4>
                            <span class="vedanta-status">🟢 Online • AI Healthcare Assistant</span>
                        </div>
                    </div>
                    <button class="vedanta-close-btn" id="vedanta-close">
                        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                            <path d="M18 6L6 18M6 6L18 18" stroke="white" stroke-width="2" stroke-linecap="round"/>
                        </svg>
                    </button>
                </div>
                
                <div class="vedanta-widget-messages" id="vedanta-messages">
                    <div class="vedanta-quick-actions">
                        <button class="vedanta-quick-btn" data-action="health-check">🏥 Health Checkup</button>
                        <button class="vedanta-quick-btn" data-action="appointment">📅 Book Appointment</button>
                        <button class="vedanta-quick-btn" data-action="emergency">🚨 Emergency</button>
                    </div>
                </div>
                
                <div class="vedanta-widget-input">
                    <div class="vedanta-input-container">
                        <input type="text" id="vedanta-input" placeholder="Ask me anything about your health..." />
                        <button id="vedanta-send" class="vedanta-send-btn">
                            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                                <path d="M22 2L11 13M22 2L15 22L11 13M22 2L2 9L11 13" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                            </svg>
                        </button>
                    </div>
                </div>
                
                <div class="vedanta-widget-footer">
                    <div class="vedanta-footer-content">
                        <span class="vedanta-powered">Powered by Vedanta Hospitals</span>
                        <small>⚠️ For informational purposes. Consult healthcare professionals for medical advice.</small>
                    </div>
                </div>
            </div>
        `;
        
        // Add CSS styles
        this.addStyles();
        
        // Append to body or specified container
        const container = document.getElementById(this.containerId) || document.body;
        container.appendChild(widgetContainer);
    }
    
    addStyles() {
        const styles = `
            .vedanta-widget {
                position: fixed;
                z-index: 9999;
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Inter', sans-serif;
            }
            
            .vedanta-widget.bottom-right {
                bottom: 24px;
                right: 24px;
            }
            
            .vedanta-widget.bottom-right.whatsapp-aware {
                bottom: 100px;
                right: 24px;
            }
            
            .vedanta-widget.bottom-left {
                bottom: 24px;
                left: 24px;
            }
            
            .vedanta-widget.bottom-left.whatsapp-aware {
                bottom: 100px;
                left: 24px;
            }
            
            .vedanta-widget-toggle {
                width: 64px;
                height: 64px;
                background: linear-gradient(135deg, #C9A227 0%, #A98500 50%, #8B6F00 100%);
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                cursor: pointer;
                box-shadow: 0 8px 32px rgba(201, 162, 39, 0.3);
                transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
                position: relative;
                overflow: hidden;
            }
            
            .vedanta-widget-toggle::before {
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: linear-gradient(45deg, transparent 30%, rgba(255,255,255,0.1) 50%, transparent 70%);
                transform: translateX(-100%);
                transition: transform 0.6s;
            }
            
            .vedanta-widget-toggle:hover::before {
                transform: translateX(100%);
            }
            
            .vedanta-widget-toggle:hover {
                transform: scale(1.05) rotate(5deg);
                box-shadow: 0 12px 40px rgba(201, 162, 39, 0.4);
            }
            
            .vedanta-toggle-icon {
                z-index: 2;
                animation: vedanta-float 3s ease-in-out infinite;
            }
            
            .vedanta-pulse-ring {
                position: absolute;
                width: 100%;
                height: 100%;
                border: 2px solid #C9A227;
                border-radius: 50%;
                animation: vedanta-pulse 2s infinite;
                opacity: 0;
            }
            
            @keyframes vedanta-float {
                0%, 100% { transform: translateY(0px); }
                50% { transform: translateY(-3px); }
            }
            
            @keyframes vedanta-pulse {
                0% {
                    transform: scale(1);
                    opacity: 0.8;
                }
                100% {
                    transform: scale(1.4);
                    opacity: 0;
                }
            }
            
            .vedanta-widget-badge {
                position: absolute;
                top: -8px;
                right: -8px;
                background: linear-gradient(135deg, #ff4757, #ff3742);
                color: white;
                border-radius: 50%;
                width: 24px;
                height: 24px;
                font-size: 12px;
                display: flex;
                align-items: center;
                justify-content: center;
                font-weight: 600;
                box-shadow: 0 4px 12px rgba(255, 71, 87, 0.4);
                animation: vedanta-bounce 0.6s ease-in-out;
            }
            
            @keyframes vedanta-bounce {
                0%, 20%, 53%, 80%, 100% {
                    transform: translate3d(0,0,0);
                }
                40%, 43% {
                    transform: translate3d(0, -8px, 0);
                }
                70% {
                    transform: translate3d(0, -4px, 0);
                }
                90% {
                    transform: translate3d(0, -2px, 0);
                }
            }
            
            .vedanta-widget-chat {
                position: absolute;
                bottom: 80px;
                right: 0;
                width: 380px;
                height: 580px;
                background: white;
                border-radius: 20px;
                box-shadow: 0 20px 60px rgba(0,0,0,0.15), 0 8px 20px rgba(0,0,0,0.1);
                display: flex;
                flex-direction: column;
                overflow: hidden;
                transform: scale(0.8) translateY(20px);
                opacity: 0;
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
                backdrop-filter: blur(10px);
                border: 1px solid rgba(201, 162, 39, 0.1);
            }
            
            .vedanta-widget-chat[style*="flex"] {
                transform: scale(1) translateY(0);
                opacity: 1;
            }
            
            .vedanta-widget-header {
                background: linear-gradient(135deg, #C9A227 0%, #A98500 100%);
                color: white;
                padding: 20px;
                display: flex;
                align-items: center;
                justify-content: space-between;
                position: relative;
                overflow: hidden;
            }
            
            .vedanta-widget-header::before {
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="grain" width="100" height="100" patternUnits="userSpaceOnUse"><circle cx="25" cy="25" r="1" fill="%23ffffff" opacity="0.05"/><circle cx="75" cy="75" r="1" fill="%23ffffff" opacity="0.05"/><circle cx="50" cy="10" r="0.5" fill="%23ffffff" opacity="0.03"/></pattern></defs><rect width="100" height="100" fill="url(%23grain)"/></svg>') repeat;
                opacity: 0.3;
            }
            
            .vedanta-header-content {
                display: flex;
                align-items: center;
                gap: 12px;
                z-index: 1;
            }
            
            .vedanta-avatar {
                width: 48px;
                height: 48px;
                background: rgba(255, 255, 255, 0.15);
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                backdrop-filter: blur(10px);
                border: 2px solid rgba(255, 255, 255, 0.2);
            }
            
            .vedanta-avatar-inner {
                animation: vedanta-rotate 8s linear infinite;
            }
            
            @keyframes vedanta-rotate {
                from { transform: rotate(0deg); }
                to { transform: rotate(360deg); }
            }
            
            .vedanta-header-text h4 {
                margin: 0;
                font-size: 18px;
                font-weight: 600;
                letter-spacing: -0.02em;
            }
            
            .vedanta-status {
                font-size: 13px;
                opacity: 0.9;
                font-weight: 500;
            }
            
            .vedanta-close-btn {
                background: rgba(255, 255, 255, 0.15);
                border: none;
                color: white;
                cursor: pointer;
                padding: 8px;
                width: 32px;
                height: 32px;
                display: flex;
                align-items: center;
                justify-content: center;
                border-radius: 50%;
                transition: all 0.2s;
                backdrop-filter: blur(10px);
                z-index: 1;
            }
            
            .vedanta-close-btn:hover {
                background: rgba(255, 255, 255, 0.25);
                transform: scale(1.1);
            }
            
            .vedanta-widget-messages {
                flex: 1;
                padding: 20px;
                overflow-y: auto;
                display: flex;
                flex-direction: column;
                gap: 16px;
                background: linear-gradient(180deg, #fafafa 0%, #ffffff 100%);
            }
            
            .vedanta-quick-actions {
                display: flex;
                flex-wrap: wrap;
                gap: 8px;
                margin-bottom: 16px;
            }
            
            .vedanta-quick-btn {
                background: linear-gradient(135deg, #C9A227, #A98500);
                color: white;
                border: none;
                padding: 8px 12px;
                border-radius: 20px;
                font-size: 12px;
                font-weight: 500;
                cursor: pointer;
                transition: all 0.2s;
                box-shadow: 0 2px 8px rgba(201, 162, 39, 0.2);
            }
            
            .vedanta-quick-btn:hover {
                transform: translateY(-1px);
                box-shadow: 0 4px 12px rgba(201, 162, 39, 0.3);
            }
            
            .vedanta-message {
                max-width: 85%;
                padding: 12px 16px;
                border-radius: 18px;
                font-size: 14px;
                line-height: 1.5;
                position: relative;
                animation: vedanta-message-in 0.3s ease-out;
            }
            
            @keyframes vedanta-message-in {
                from {
                    opacity: 0;
                    transform: translateY(10px);
                }
                to {
                    opacity: 1;
                    transform: translateY(0);
                }
            }
            
            .vedanta-message.user {
                background: linear-gradient(135deg, #C9A227, #A98500);
                color: white;
                align-self: flex-end;
                border-bottom-right-radius: 6px;
                box-shadow: 0 4px 12px rgba(201, 162, 39, 0.2);
            }
            
            .vedanta-message.assistant {
                background: white;
                color: #333;
                align-self: flex-start;
                border-bottom-left-radius: 6px;
                border: 1px solid #e9ecef;
                box-shadow: 0 2px 8px rgba(0,0,0,0.05);
            }
            
            .vedanta-widget-input {
                padding: 20px;
                border-top: 1px solid #e9ecef;
                background: white;
            }
            
            .vedanta-input-container {
                display: flex;
                gap: 12px;
                align-items: center;
                background: #f8f9fa;
                border-radius: 25px;
                padding: 4px;
                border: 2px solid transparent;
                transition: all 0.2s;
            }
            
            .vedanta-input-container:focus-within {
                border-color: #C9A227;
                box-shadow: 0 0 0 3px rgba(201, 162, 39, 0.1);
            }
            
            .vedanta-input-container input {
                flex: 1;
                padding: 12px 16px;
                border: none;
                background: transparent;
                outline: none;
                font-size: 14px;
                color: #333;
            }
            
            .vedanta-input-container input::placeholder {
                color: #999;
            }
            
            .vedanta-send-btn {
                background: linear-gradient(135deg, #C9A227, #A98500);
                color: white;
                border: none;
                padding: 10px;
                border-radius: 50%;
                cursor: pointer;
                display: flex;
                align-items: center;
                justify-content: center;
                transition: all 0.2s;
                box-shadow: 0 2px 8px rgba(201, 162, 39, 0.2);
            }
            
            .vedanta-send-btn:hover {
                transform: scale(1.05);
                box-shadow: 0 4px 12px rgba(201, 162, 39, 0.3);
            }
            
            .vedanta-widget-footer {
                padding: 16px 20px;
                background: #f8f9fa;
                border-top: 1px solid #e9ecef;
            }
            
            .vedanta-footer-content {
                text-align: center;
            }
            
            .vedanta-powered {
                display: block;
                font-size: 12px;
                font-weight: 600;
                color: #C9A227;
                margin-bottom: 4px;
            }
            
            .vedanta-footer-content small {
                color: #666;
                font-size: 11px;
                line-height: 1.3;
            }
            
            .vedanta-typing {
                display: flex;
                align-items: center;
                gap: 8px;
                padding: 12px 16px;
                background: white;
                border-radius: 18px;
                align-self: flex-start;
                border: 1px solid #e9ecef;
                box-shadow: 0 2px 8px rgba(0,0,0,0.05);
                animation: vedanta-message-in 0.3s ease-out;
            }
            
            .vedanta-typing-text {
                font-size: 14px;
                color: #666;
                font-style: italic;
            }
            
            .vedanta-typing-dots {
                display: flex;
                gap: 4px;
            }
            
            .vedanta-typing-dot {
                width: 8px;
                height: 8px;
                background: #C9A227;
                border-radius: 50%;
                animation: vedanta-typing 1.4s infinite;
            }
            
            .vedanta-typing-dot:nth-child(2) {
                animation-delay: 0.2s;
            }
            
            .vedanta-typing-dot:nth-child(3) {
                animation-delay: 0.4s;
            }
            
            @keyframes vedanta-typing {
                0%, 60%, 100% {
                    transform: translateY(0);
                    opacity: 0.4;
                }
                30% {
                    transform: translateY(-8px);
                    opacity: 1;
                }
            }
            
            /* Mobile Responsive */
            @media (max-width: 768px) {
                .vedanta-widget.bottom-right.whatsapp-aware {
                    bottom: 110px;
                    right: 16px;
                }
                
                .vedanta-widget.bottom-left.whatsapp-aware {
                    bottom: 110px;
                    left: 16px;
                }
                
                .vedanta-widget-chat {
                    width: 340px;
                    height: 520px;
                }
            }
            
            @media (max-width: 480px) {
                .vedanta-widget.bottom-right,
                .vedanta-widget.bottom-right.whatsapp-aware {
                    bottom: 20px;
                    right: 16px;
                }
                
                .vedanta-widget.bottom-left,
                .vedanta-widget.bottom-left.whatsapp-aware {
                    bottom: 20px;
                    left: 16px;
                }
                
                .vedanta-widget-chat {
                    width: calc(100vw - 32px);
                    height: calc(100vh - 100px);
                    max-width: 320px;
                    max-height: 500px;
                }
            }
        `;
        
        const styleSheet = document.createElement('style');
        styleSheet.textContent = styles;
        document.head.appendChild(styleSheet);
    }
    
    attachEventListeners() {
        const toggle = document.getElementById('vedanta-toggle');
        const close = document.getElementById('vedanta-close');
        const input = document.getElementById('vedanta-input');
        const send = document.getElementById('vedanta-send');
        const quickBtns = document.querySelectorAll('.vedanta-quick-btn');
        
        toggle.addEventListener('click', () => this.toggleWidget());
        close.addEventListener('click', () => this.closeWidget());
        send.addEventListener('click', () => this.sendMessage());
        input.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.sendMessage();
            }
        });
        
        // Quick action buttons
        quickBtns.forEach(btn => {
            btn.addEventListener('click', (e) => {
                const action = e.target.dataset.action;
                this.handleQuickAction(action);
            });
        });
    }
    
    handleQuickAction(action) {
        const actions = {
            'health-check': 'I would like to know about health checkup packages and services.',
            'appointment': 'I want to book an appointment with a doctor.',
            'emergency': 'This is an emergency. I need immediate medical assistance.'
        };
        
        if (actions[action]) {
            document.getElementById('vedanta-input').value = actions[action];
            this.sendMessage();
        }
    }
    
    toggleWidget() {
        const chat = document.getElementById('vedanta-chat');
        const badge = document.getElementById('vedanta-badge');
        
        if (this.isOpen) {
            chat.style.display = 'none';
            this.isOpen = false;
        } else {
            chat.style.display = 'flex';
            this.isOpen = true;
            badge.style.display = 'none';
            document.getElementById('vedanta-input').focus();
        }
    }
    
    closeWidget() {
        document.getElementById('vedanta-chat').style.display = 'none';
        this.isOpen = false;
    }
    
    addWelcomeMessage() {
        const welcomeMsg = "👋 Hello! I'm Vedanta Smart Assist, your intelligent healthcare companion. I can help you with health information, appointment booking, emergency assistance, and connecting you with our medical experts. How can I assist you today?";
        this.addMessage('assistant', welcomeMsg);
        this.showBadge();
    }
    
    addMessage(role, content) {
        const messagesContainer = document.getElementById('vedanta-messages');
        const messageDiv = document.createElement('div');
        messageDiv.className = `vedanta-message ${role}`;
        messageDiv.textContent = content;
        
        messagesContainer.appendChild(messageDiv);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
        
        this.messages.push({ role, content });
    }
    
    showTyping() {
        if (this.isTyping) return;
        
        const messagesContainer = document.getElementById('vedanta-messages');
        const typingDiv = document.createElement('div');
        typingDiv.className = 'vedanta-typing';
        typingDiv.id = 'vedanta-typing-indicator';
        typingDiv.innerHTML = `
            <span class="vedanta-typing-text">Vedanta Smart Assist is thinking</span>
            <div class="vedanta-typing-dots">
                <div class="vedanta-typing-dot"></div>
                <div class="vedanta-typing-dot"></div>
                <div class="vedanta-typing-dot"></div>
            </div>
        `;
        
        messagesContainer.appendChild(typingDiv);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
        this.isTyping = true;
    }
    
    hideTyping() {
        const typingIndicator = document.getElementById('vedanta-typing-indicator');
        if (typingIndicator) {
            typingIndicator.remove();
            this.isTyping = false;
        }
    }
    
    showBadge() {
        if (!this.isOpen) {
            document.getElementById('vedanta-badge').style.display = 'flex';
        }
    }
    
    async sendMessage() {
        const input = document.getElementById('vedanta-input');
        const message = input.value.trim();
        
        if (!message) return;
        
        // Add user message
        this.addMessage('user', message);
        input.value = '';
        
        // Show typing indicator
        this.showTyping();
        
        try {
            // Check if API key is configured
            if (!this.geminiApiKey || this.geminiApiKey === 'your_google_gemini_api_key_here') {
                this.hideTyping();
                this.addMessage('assistant', '⚠️ Google Gemini API key is not configured. Please add your API key to use the chatbot.');
                return;
            }
            
            // Prepare the request with medical context
            const systemPrompt = `You are a helpful medical AI assistant for Vedanta Hospitals. You provide general health information and guidance, but always remind users to consult healthcare professionals for serious medical concerns. Keep responses concise, helpful, and professional. Focus on:
            - General health tips and wellness advice
            - Basic medical information and explanations
            - Preventive care recommendations
            - When to seek professional medical help
            
            Always include appropriate medical disclaimers when giving health advice.`;
            
            const requestBody = {
                contents: [{
                    parts: [{
                        text: `${systemPrompt}\n\nUser question: ${message}`
                    }]
                }],
                generationConfig: {
                    temperature: 0.7,
                    topK: 40,
                    topP: 0.95,
                    maxOutputTokens: 1024
                }
            };
            
            // Send to Gemini API
            const response = await fetch(`${this.geminiApiUrl}?key=${this.geminiApiKey}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(requestBody)
            });
            
            // Hide typing indicator
            this.hideTyping();
            
            if (response.ok) {
                const data = await response.json();
                
                if (data.candidates && data.candidates[0] && data.candidates[0].content) {
                    const aiResponse = data.candidates[0].content.parts[0].text;
                    this.addMessage('assistant', aiResponse);
                } else {
                    this.addMessage('assistant', 'I apologize, but I received an unexpected response. Please try rephrasing your question.');
                }
            } else {
                const errorData = await response.json().catch(() => ({}));
                let errorMessage = 'I apologize, but I\'m experiencing some technical difficulties.';
                
                if (response.status === 403) {
                    errorMessage = 'API access is restricted. Please check your API key permissions.';
                } else if (response.status === 429) {
                    errorMessage = 'I\'m receiving too many requests right now. Please wait a moment and try again.';
                } else if (response.status === 400) {
                    errorMessage = 'There was an issue with your request. Please try rephrasing your question.';
                }
                
                this.addMessage('assistant', errorMessage);
            }
        } catch (error) {
            this.hideTyping();
            console.error('Gemini API error:', error);
            
            let errorMessage = 'I\'m currently unable to connect to my knowledge base.';
            if (error.name === 'TypeError' && error.message.includes('fetch')) {
                errorMessage += ' Please check your internet connection and try again.';
            } else {
                errorMessage += ' Please try again in a moment.';
            }
            errorMessage += ' For urgent matters, contact Vedanta Hospitals directly.';
            
            this.addMessage('assistant', errorMessage);
        }
    }
    
    // Public methods for external control
    open() {
        if (!this.isOpen) {
            this.toggleWidget();
        }
    }
    
    close() {
        if (this.isOpen) {
            this.closeWidget();
        }
    }
    
    sendPredefinedMessage(message) {
        if (this.isOpen) {
            document.getElementById('vedanta-input').value = message;
            this.sendMessage();
        }
    }
}

// Auto-initialize if configuration is provided
if (typeof window !== 'undefined') {
    window.VedantaSmartAssist = VedantaSmartAssist;
    
    // Backward compatibility
    window.NephroWidget = VedantaSmartAssist;
    
    // Auto-initialize if config is found
    if (window.vedantaWidgetConfig) {
        new VedantaSmartAssist(window.vedantaWidgetConfig);
    } else if (window.nephroWidgetConfig) {
        new VedantaSmartAssist(window.nephroWidgetConfig);
    }
}