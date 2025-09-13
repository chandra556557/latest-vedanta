/**
 * Dr. Nephro Chatbot Widget
 * Embeddable JavaScript widget for website integration
 */

class NephroWidget {
    constructor(options = {}) {
        this.apiUrl = options.apiUrl || 'http://localhost:8002';
        this.containerId = options.containerId || 'nephro-widget';
        this.theme = options.theme || 'default';
        this.position = options.position || 'bottom-right';
        this.whatsappAware = options.whatsappAware || false;
        this.isOpen = false;
        this.messages = [];
        
        this.init();
    }
    
    init() {
        this.createWidget();
        this.attachEventListeners();
        this.addWelcomeMessage();
    }
    
    createWidget() {
        // Create widget container
        const widgetContainer = document.createElement('div');
        widgetContainer.id = 'nephro-widget-container';
        const whatsappClass = this.whatsappAware ? ' whatsapp-aware' : '';
        widgetContainer.className = `nephro-widget ${this.position}${whatsappClass}`;
        
        widgetContainer.innerHTML = `
            <div class="nephro-widget-toggle" id="nephro-toggle">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M12 2C13.1 2 14 2.9 14 4C14 5.1 13.1 6 12 6C10.9 6 10 5.1 10 4C10 2.9 10.9 2 12 2ZM21 9V7L15 1H5C3.89 1 3 1.89 3 3V21C3 22.11 3.89 23 5 23H19C20.11 23 21 22.11 21 21V9M19 9H14V4H5V21H19V9Z" fill="white"/>
                </svg>
                <span class="nephro-widget-badge" id="nephro-badge" style="display: none;">1</span>
            </div>
            
            <div class="nephro-widget-chat" id="nephro-chat" style="display: none;">
                <div class="nephro-widget-header">
                    <div class="nephro-header-content">
                        <div class="nephro-avatar">🩺</div>
                        <div class="nephro-header-text">
                            <h4>Dr. Nephro</h4>
                            <span>Kidney Health Assistant</span>
                        </div>
                    </div>
                    <button class="nephro-close-btn" id="nephro-close">×</button>
                </div>
                
                <div class="nephro-widget-messages" id="nephro-messages"></div>
                
                <div class="nephro-widget-input">
                    <input type="text" id="nephro-input" placeholder="Ask about kidney health..." />
                    <button id="nephro-send">Send</button>
                </div>
                
                <div class="nephro-widget-footer">
                    <small>⚠️ For educational purposes only. Consult your doctor for medical advice.</small>
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
            .nephro-widget {
                position: fixed;
                z-index: 9999;
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            }
            
            .nephro-widget.bottom-right {
                bottom: 20px;
                right: 20px;
            }
            
            .nephro-widget.bottom-right.whatsapp-aware {
                bottom: 90px;
                right: 20px;
            }
            
            .nephro-widget.bottom-left {
                bottom: 20px;
                left: 20px;
            }
            
            .nephro-widget.bottom-left.whatsapp-aware {
                bottom: 90px;
                left: 20px;
            }
            
            /* Mobile responsive positioning */
            @media (max-width: 768px) {
                .nephro-widget.bottom-right.whatsapp-aware {
                    bottom: 100px;
                    right: 15px;
                }
                
                .nephro-widget.bottom-left.whatsapp-aware {
                    bottom: 100px;
                    left: 15px;
                }
                
                .nephro-widget-chat {
                    width: 320px;
                    height: 450px;
                }
            }
            
            @media (max-width: 480px) {
                .nephro-widget.bottom-right.whatsapp-aware {
                    bottom: 110px;
                    right: 10px;
                }
                
                .nephro-widget.bottom-left.whatsapp-aware {
                    bottom: 110px;
                    left: 10px;
                }
                
                .nephro-widget-chat {
                    width: 300px;
                    height: 400px;
                }
            }
            
            .nephro-widget-toggle {
                width: 60px;
                height: 60px;
                background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                cursor: pointer;
                box-shadow: 0 4px 12px rgba(0,0,0,0.15);
                transition: all 0.3s ease;
                position: relative;
            }
            
            .nephro-widget-toggle:hover {
                transform: scale(1.1);
                box-shadow: 0 6px 20px rgba(0,0,0,0.2);
            }
            
            .nephro-widget-badge {
                position: absolute;
                top: -5px;
                right: -5px;
                background: #ff4757;
                color: white;
                border-radius: 50%;
                width: 20px;
                height: 20px;
                font-size: 12px;
                display: flex;
                align-items: center;
                justify-content: center;
                font-weight: bold;
            }
            
            .nephro-widget-chat {
                position: absolute;
                bottom: 70px;
                right: 0;
                width: 350px;
                height: 500px;
                background: white;
                border-radius: 12px;
                box-shadow: 0 8px 30px rgba(0,0,0,0.12);
                display: flex;
                flex-direction: column;
                overflow: hidden;
            }
            
            .nephro-widget-header {
                background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
                color: white;
                padding: 15px;
                display: flex;
                align-items: center;
                justify-content: space-between;
            }
            
            .nephro-header-content {
                display: flex;
                align-items: center;
                gap: 10px;
            }
            
            .nephro-avatar {
                font-size: 24px;
            }
            
            .nephro-header-text h4 {
                margin: 0;
                font-size: 16px;
            }
            
            .nephro-header-text span {
                font-size: 12px;
                opacity: 0.9;
            }
            
            .nephro-close-btn {
                background: none;
                border: none;
                color: white;
                font-size: 24px;
                cursor: pointer;
                padding: 0;
                width: 30px;
                height: 30px;
                display: flex;
                align-items: center;
                justify-content: center;
                border-radius: 50%;
                transition: background 0.2s;
            }
            
            .nephro-close-btn:hover {
                background: rgba(255,255,255,0.1);
            }
            
            .nephro-widget-messages {
                flex: 1;
                padding: 15px;
                overflow-y: auto;
                display: flex;
                flex-direction: column;
                gap: 10px;
            }
            
            .nephro-message {
                max-width: 80%;
                padding: 10px 12px;
                border-radius: 12px;
                font-size: 14px;
                line-height: 1.4;
            }
            
            .nephro-message.user {
                background: #007bff;
                color: white;
                align-self: flex-end;
                border-bottom-right-radius: 4px;
            }
            
            .nephro-message.assistant {
                background: #f8f9fa;
                color: #333;
                align-self: flex-start;
                border-bottom-left-radius: 4px;
                border: 1px solid #e9ecef;
            }
            
            .nephro-widget-input {
                padding: 15px;
                border-top: 1px solid #e9ecef;
                display: flex;
                gap: 10px;
            }
            
            .nephro-widget-input input {
                flex: 1;
                padding: 10px 12px;
                border: 1px solid #ddd;
                border-radius: 20px;
                outline: none;
                font-size: 14px;
            }
            
            .nephro-widget-input input:focus {
                border-color: #007bff;
            }
            
            .nephro-widget-input button {
                background: #007bff;
                color: white;
                border: none;
                padding: 10px 16px;
                border-radius: 20px;
                cursor: pointer;
                font-size: 14px;
                transition: background 0.2s;
            }
            
            .nephro-widget-input button:hover {
                background: #0056b3;
            }
            
            .nephro-widget-footer {
                padding: 10px 15px;
                background: #f8f9fa;
                border-top: 1px solid #e9ecef;
                text-align: center;
            }
            
            .nephro-widget-footer small {
                color: #666;
                font-size: 11px;
            }
            
            .nephro-typing {
                display: flex;
                align-items: center;
                gap: 5px;
                padding: 10px 12px;
                background: #f8f9fa;
                border-radius: 12px;
                align-self: flex-start;
                border: 1px solid #e9ecef;
            }
            
            .nephro-typing-dots {
                display: flex;
                gap: 3px;
            }
            
            .nephro-typing-dot {
                width: 6px;
                height: 6px;
                background: #666;
                border-radius: 50%;
                animation: nephro-typing 1.4s infinite;
            }
            
            .nephro-typing-dot:nth-child(2) {
                animation-delay: 0.2s;
            }
            
            .nephro-typing-dot:nth-child(3) {
                animation-delay: 0.4s;
            }
            
            @keyframes nephro-typing {
                0%, 60%, 100% {
                    transform: translateY(0);
                    opacity: 0.4;
                }
                30% {
                    transform: translateY(-10px);
                    opacity: 1;
                }
            }
            
            @media (max-width: 480px) {
                .nephro-widget-chat {
                    width: 300px;
                    height: 400px;
                }
            }
        `;
        
        const styleSheet = document.createElement('style');
        styleSheet.textContent = styles;
        document.head.appendChild(styleSheet);
    }
    
    attachEventListeners() {
        const toggle = document.getElementById('nephro-toggle');
        const close = document.getElementById('nephro-close');
        const input = document.getElementById('nephro-input');
        const send = document.getElementById('nephro-send');
        
        toggle.addEventListener('click', () => this.toggleWidget());
        close.addEventListener('click', () => this.closeWidget());
        send.addEventListener('click', () => this.sendMessage());
        input.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.sendMessage();
            }
        });
    }
    
    toggleWidget() {
        const chat = document.getElementById('nephro-chat');
        const badge = document.getElementById('nephro-badge');
        
        if (this.isOpen) {
            chat.style.display = 'none';
            this.isOpen = false;
        } else {
            chat.style.display = 'flex';
            this.isOpen = true;
            badge.style.display = 'none';
            document.getElementById('nephro-input').focus();
        }
    }
    
    closeWidget() {
        document.getElementById('nephro-chat').style.display = 'none';
        this.isOpen = false;
    }
    
    addWelcomeMessage() {
        const welcomeMsg = "👋 Hello! I'm Dr. Nephro, your AI kidney health assistant. I can help with questions about kidney health, CKD, dialysis, and more. How can I assist you today?";
        this.addMessage('assistant', welcomeMsg);
        this.showBadge();
    }
    
    addMessage(role, content) {
        const messagesContainer = document.getElementById('nephro-messages');
        const messageDiv = document.createElement('div');
        messageDiv.className = `nephro-message ${role}`;
        messageDiv.textContent = content;
        
        messagesContainer.appendChild(messageDiv);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
        
        this.messages.push({ role, content });
    }
    
    showTyping() {
        const messagesContainer = document.getElementById('nephro-messages');
        const typingDiv = document.createElement('div');
        typingDiv.className = 'nephro-typing';
        typingDiv.id = 'nephro-typing-indicator';
        typingDiv.innerHTML = `
            <span>Dr. Nephro is typing</span>
            <div class="nephro-typing-dots">
                <div class="nephro-typing-dot"></div>
                <div class="nephro-typing-dot"></div>
                <div class="nephro-typing-dot"></div>
            </div>
        `;
        
        messagesContainer.appendChild(typingDiv);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }
    
    hideTyping() {
        const typingIndicator = document.getElementById('nephro-typing-indicator');
        if (typingIndicator) {
            typingIndicator.remove();
        }
    }
    
    showBadge() {
        if (!this.isOpen) {
            document.getElementById('nephro-badge').style.display = 'flex';
        }
    }
    
    async sendMessage() {
        const input = document.getElementById('nephro-input');
        const message = input.value.trim();
        
        if (!message) return;
        
        // Add user message
        this.addMessage('user', message);
        input.value = '';
        
        // Show typing indicator
        this.showTyping();
        
        try {
            // Send to API
            const response = await fetch(`${this.apiUrl}/chat`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    message: message,
                    conversation_history: this.messages.slice(-10) // Last 10 messages for context
                })
            });
            
            const data = await response.json();
            
            // Hide typing indicator
            this.hideTyping();
            
            if (response.ok) {
                this.addMessage('assistant', data.response);
            } else {
                this.addMessage('assistant', 'I apologize, but I\'m having trouble processing your request. Please try again later.');
            }
        } catch (error) {
            this.hideTyping();
            this.addMessage('assistant', 'I\'m currently unable to connect to my knowledge base. Please check your internet connection and try again.');
        }
    }
}

// Auto-initialize if configuration is provided
if (typeof window !== 'undefined') {
    window.NephroWidget = NephroWidget;
    
    // Auto-initialize if config is found
    if (window.nephroWidgetConfig) {
        new NephroWidget(window.nephroWidgetConfig);
    }
}