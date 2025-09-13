-- Enterprise Nephrology AI Agent Database Schema
-- SQLite Database Schema for Enhanced Features

-- Users table for multi-user support
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(100),
    role VARCHAR(20) DEFAULT 'patient' CHECK (role IN ('patient', 'doctor', 'nurse', 'admin')),
    specialization VARCHAR(100),
    license_number VARCHAR(50),
    hospital_affiliation VARCHAR(200),
    phone VARCHAR(20),
    date_of_birth DATE,
    gender VARCHAR(10),
    is_active BOOLEAN DEFAULT TRUE,
    is_verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP,
    profile_picture_url VARCHAR(500),
    preferences TEXT, -- JSON string for user preferences
    emergency_contact TEXT, -- JSON string for emergency contact info
    medical_history TEXT, -- JSON string for medical history
    allergies TEXT, -- JSON string for allergies
    current_medications TEXT -- JSON string for current medications
);

-- Sessions table for user authentication
CREATE TABLE IF NOT EXISTS user_sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    session_token VARCHAR(255) UNIQUE NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ip_address VARCHAR(45),
    user_agent TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Consultations table for storing chat sessions
CREATE TABLE IF NOT EXISTS consultations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    session_id VARCHAR(100) UNIQUE NOT NULL,
    title VARCHAR(200),
    chief_complaint TEXT,
    consultation_type VARCHAR(50) DEFAULT 'general' CHECK (consultation_type IN ('general', 'emergency', 'follow_up', 'second_opinion')),
    status VARCHAR(20) DEFAULT 'active' CHECK (status IN ('active', 'completed', 'cancelled', 'archived')),
    priority VARCHAR(10) DEFAULT 'normal' CHECK (priority IN ('low', 'normal', 'high', 'urgent')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP,
    duration_minutes INTEGER,
    satisfaction_rating INTEGER CHECK (satisfaction_rating BETWEEN 1 AND 5),
    feedback TEXT,
    diagnosis_summary TEXT,
    recommendations TEXT,
    follow_up_required BOOLEAN DEFAULT FALSE,
    follow_up_date DATE,
    assigned_doctor_id INTEGER,
    tags TEXT, -- JSON array of tags
    metadata TEXT, -- JSON string for additional metadata
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (assigned_doctor_id) REFERENCES users(id)
);

-- Messages table for storing individual chat messages
CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    consultation_id INTEGER NOT NULL,
    sender_type VARCHAR(10) NOT NULL CHECK (sender_type IN ('user', 'ai', 'doctor')),
    sender_id INTEGER,
    message_text TEXT NOT NULL,
    message_type VARCHAR(20) DEFAULT 'text' CHECK (message_type IN ('text', 'image', 'file', 'assessment', 'recommendation')),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_edited BOOLEAN DEFAULT FALSE,
    edited_at TIMESTAMP,
    attachments TEXT, -- JSON array of attachment URLs
    metadata TEXT, -- JSON string for additional data
    confidence_score REAL, -- AI confidence in response
    response_time_ms INTEGER, -- Response generation time
    tokens_used INTEGER, -- Number of tokens used for AI response
    FOREIGN KEY (consultation_id) REFERENCES consultations(id) ON DELETE CASCADE,
    FOREIGN KEY (sender_id) REFERENCES users(id)
);

-- Assessments table for storing health assessments
CREATE TABLE IF NOT EXISTS assessments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    consultation_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    assessment_type VARCHAR(50) NOT NULL,
    symptoms TEXT NOT NULL, -- JSON array of symptoms
    severity_scores TEXT, -- JSON object with severity scores
    risk_factors TEXT, -- JSON array of risk factors
    medical_history TEXT, -- JSON object with relevant medical history
    current_medications TEXT, -- JSON array of current medications
    vital_signs TEXT, -- JSON object with vital signs
    lab_results TEXT, -- JSON object with lab results
    imaging_results TEXT, -- JSON object with imaging results
    assessment_results TEXT NOT NULL, -- JSON object with assessment results
    risk_score REAL,
    risk_category VARCHAR(20),
    recommendations TEXT, -- JSON array of recommendations
    urgency_level VARCHAR(20) DEFAULT 'normal' CHECK (urgency_level IN ('low', 'normal', 'high', 'emergency')),
    requires_immediate_attention BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    reviewed_by_doctor_id INTEGER,
    doctor_notes TEXT,
    doctor_approval BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (consultation_id) REFERENCES consultations(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (reviewed_by_doctor_id) REFERENCES users(id)
);

-- Risk calculations table
CREATE TABLE IF NOT EXISTS risk_calculations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    assessment_id INTEGER NOT NULL,
    calculator_type VARCHAR(50) NOT NULL,
    input_parameters TEXT NOT NULL, -- JSON object with input parameters
    calculated_risk REAL NOT NULL,
    risk_category VARCHAR(20),
    interpretation TEXT,
    recommendations TEXT, -- JSON array of recommendations
    confidence_interval TEXT, -- JSON object with confidence intervals
    calculation_method VARCHAR(100),
    reference_studies TEXT, -- JSON array of reference studies
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (assessment_id) REFERENCES assessments(id) ON DELETE CASCADE
);

-- Clinical guidelines table
CREATE TABLE IF NOT EXISTS clinical_guidelines (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    guideline_name VARCHAR(200) NOT NULL,
    organization VARCHAR(100),
    version VARCHAR(20),
    publication_date DATE,
    category VARCHAR(50),
    subcategory VARCHAR(50),
    condition_keywords TEXT, -- JSON array of condition keywords
    guideline_content TEXT NOT NULL,
    evidence_level VARCHAR(20),
    recommendation_strength VARCHAR(20),
    target_population TEXT,
    contraindications TEXT,
    special_considerations TEXT,
    references TEXT, -- JSON array of references
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Analytics and metrics table
CREATE TABLE IF NOT EXISTS analytics_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    session_id VARCHAR(100),
    event_type VARCHAR(50) NOT NULL,
    event_category VARCHAR(50),
    event_action VARCHAR(100),
    event_label VARCHAR(200),
    event_value REAL,
    event_data TEXT, -- JSON object with event data
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ip_address VARCHAR(45),
    user_agent TEXT,
    page_url VARCHAR(500),
    referrer_url VARCHAR(500),
    device_type VARCHAR(20),
    browser VARCHAR(50),
    operating_system VARCHAR(50),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
);

-- System performance metrics
CREATE TABLE IF NOT EXISTS performance_metrics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    metric_name VARCHAR(100) NOT NULL,
    metric_value REAL NOT NULL,
    metric_unit VARCHAR(20),
    metric_category VARCHAR(50),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    additional_data TEXT -- JSON object with additional metric data
);

-- Audit logs for security and compliance
CREATE TABLE IF NOT EXISTS audit_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    action VARCHAR(100) NOT NULL,
    resource_type VARCHAR(50),
    resource_id VARCHAR(100),
    old_values TEXT, -- JSON object with old values
    new_values TEXT, -- JSON object with new values
    ip_address VARCHAR(45),
    user_agent TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    success BOOLEAN DEFAULT TRUE,
    error_message TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
);

-- Notifications table
CREATE TABLE IF NOT EXISTS notifications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    notification_type VARCHAR(50) NOT NULL,
    title VARCHAR(200) NOT NULL,
    message TEXT NOT NULL,
    priority VARCHAR(10) DEFAULT 'normal' CHECK (priority IN ('low', 'normal', 'high', 'urgent')),
    is_read BOOLEAN DEFAULT FALSE,
    is_sent BOOLEAN DEFAULT FALSE,
    delivery_method VARCHAR(20) DEFAULT 'in_app' CHECK (delivery_method IN ('in_app', 'email', 'sms', 'push')),
    scheduled_at TIMESTAMP,
    sent_at TIMESTAMP,
    read_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP,
    action_url VARCHAR(500),
    metadata TEXT, -- JSON object with additional data
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- System configuration table
CREATE TABLE IF NOT EXISTS system_config (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    config_key VARCHAR(100) UNIQUE NOT NULL,
    config_value TEXT NOT NULL,
    config_type VARCHAR(20) DEFAULT 'string' CHECK (config_type IN ('string', 'integer', 'float', 'boolean', 'json')),
    description TEXT,
    is_sensitive BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_by INTEGER,
    FOREIGN KEY (updated_by) REFERENCES users(id)
);

-- File uploads table
CREATE TABLE IF NOT EXISTS file_uploads (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    consultation_id INTEGER,
    filename VARCHAR(255) NOT NULL,
    original_filename VARCHAR(255) NOT NULL,
    file_path VARCHAR(500) NOT NULL,
    file_size INTEGER NOT NULL,
    file_type VARCHAR(100) NOT NULL,
    mime_type VARCHAR(100),
    upload_purpose VARCHAR(50),
    is_processed BOOLEAN DEFAULT FALSE,
    processing_status VARCHAR(20) DEFAULT 'pending',
    processing_results TEXT, -- JSON object with processing results
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (consultation_id) REFERENCES consultations(id) ON DELETE CASCADE
);

-- API usage tracking
CREATE TABLE IF NOT EXISTS api_usage (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    endpoint VARCHAR(200) NOT NULL,
    method VARCHAR(10) NOT NULL,
    status_code INTEGER NOT NULL,
    response_time_ms INTEGER,
    request_size INTEGER,
    response_size INTEGER,
    ip_address VARCHAR(45),
    user_agent TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    rate_limit_remaining INTEGER,
    error_message TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
);

-- Feedback and ratings
CREATE TABLE IF NOT EXISTS feedback (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    consultation_id INTEGER,
    feedback_type VARCHAR(50) NOT NULL,
    rating INTEGER CHECK (rating BETWEEN 1 AND 5),
    feedback_text TEXT,
    category VARCHAR(50),
    is_anonymous BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    response_text TEXT,
    responded_at TIMESTAMP,
    responded_by INTEGER,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (consultation_id) REFERENCES consultations(id) ON DELETE CASCADE,
    FOREIGN KEY (responded_by) REFERENCES users(id)
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);
CREATE INDEX IF NOT EXISTS idx_users_role ON users(role);
CREATE INDEX IF NOT EXISTS idx_sessions_token ON user_sessions(session_token);
CREATE INDEX IF NOT EXISTS idx_sessions_user_id ON user_sessions(user_id);
CREATE INDEX IF NOT EXISTS idx_consultations_user_id ON consultations(user_id);
CREATE INDEX IF NOT EXISTS idx_consultations_status ON consultations(status);
CREATE INDEX IF NOT EXISTS idx_consultations_created_at ON consultations(created_at);
CREATE INDEX IF NOT EXISTS idx_messages_consultation_id ON messages(consultation_id);
CREATE INDEX IF NOT EXISTS idx_messages_timestamp ON messages(timestamp);
CREATE INDEX IF NOT EXISTS idx_assessments_user_id ON assessments(user_id);
CREATE INDEX IF NOT EXISTS idx_assessments_consultation_id ON assessments(consultation_id);
CREATE INDEX IF NOT EXISTS idx_analytics_user_id ON analytics_events(user_id);
CREATE INDEX IF NOT EXISTS idx_analytics_timestamp ON analytics_events(timestamp);
CREATE INDEX IF NOT EXISTS idx_analytics_event_type ON analytics_events(event_type);
CREATE INDEX IF NOT EXISTS idx_audit_logs_user_id ON audit_logs(user_id);
CREATE INDEX IF NOT EXISTS idx_audit_logs_timestamp ON audit_logs(timestamp);
CREATE INDEX IF NOT EXISTS idx_notifications_user_id ON notifications(user_id);
CREATE INDEX IF NOT EXISTS idx_notifications_is_read ON notifications(is_read);
CREATE INDEX IF NOT EXISTS idx_file_uploads_user_id ON file_uploads(user_id);
CREATE INDEX IF NOT EXISTS idx_api_usage_user_id ON api_usage(user_id);
CREATE INDEX IF NOT EXISTS idx_api_usage_timestamp ON api_usage(timestamp);
CREATE INDEX IF NOT EXISTS idx_feedback_user_id ON feedback(user_id);

-- Create triggers for automatic timestamp updates
CREATE TRIGGER IF NOT EXISTS update_users_timestamp 
    AFTER UPDATE ON users
    BEGIN
        UPDATE users SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
    END;

CREATE TRIGGER IF NOT EXISTS update_consultations_timestamp 
    AFTER UPDATE ON consultations
    BEGIN
        UPDATE consultations SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
    END;

CREATE TRIGGER IF NOT EXISTS update_assessments_timestamp 
    AFTER UPDATE ON assessments
    BEGIN
        UPDATE assessments SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
    END;

CREATE TRIGGER IF NOT EXISTS update_guidelines_timestamp 
    AFTER UPDATE ON clinical_guidelines
    BEGIN
        UPDATE clinical_guidelines SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
    END;

CREATE TRIGGER IF NOT EXISTS update_config_timestamp 
    AFTER UPDATE ON system_config
    BEGIN
        UPDATE system_config SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
    END;

-- Insert default system configuration
INSERT OR IGNORE INTO system_config (config_key, config_value, config_type, description) VALUES
('app_name', 'Enterprise Nephrology AI Agent', 'string', 'Application name'),
('app_version', '2.0.0', 'string', 'Application version'),
('max_consultation_duration', '3600', 'integer', 'Maximum consultation duration in seconds'),
('max_file_upload_size', '10485760', 'integer', 'Maximum file upload size in bytes (10MB)'),
('session_timeout', '86400', 'integer', 'Session timeout in seconds (24 hours)'),
('rate_limit_requests', '100', 'integer', 'Rate limit requests per minute'),
('enable_analytics', 'true', 'boolean', 'Enable analytics tracking'),
('enable_audit_logging', 'true', 'boolean', 'Enable audit logging'),
('emergency_contact_email', 'emergency@nephroai.com', 'string', 'Emergency contact email'),
('support_email', 'support@nephroai.com', 'string', 'Support contact email'),
('maintenance_mode', 'false', 'boolean', 'Maintenance mode flag'),
('feature_flags', '{"advanced_analytics": true, "risk_calculators": true, "clinical_guidelines": true}', 'json', 'Feature flags configuration');

-- Insert default clinical guidelines
INSERT OR IGNORE INTO clinical_guidelines (guideline_name, organization, version, category, guideline_content, evidence_level, is_active) VALUES
('CKD Management Guidelines', 'KDIGO', '2024', 'Chronic Kidney Disease', 'Comprehensive guidelines for CKD management including staging, monitoring, and treatment recommendations.', 'High', TRUE),
('AKI Prevention and Management', 'KDIGO', '2024', 'Acute Kidney Injury', 'Evidence-based guidelines for AKI prevention, early detection, and management strategies.', 'High', TRUE),
('Dialysis Adequacy Standards', 'NKF', '2024', 'Dialysis', 'Standards for dialysis adequacy assessment and optimization for both hemodialysis and peritoneal dialysis.', 'High', TRUE),
('Hypertension in CKD', 'AHA/ACC', '2024', 'Hypertension', 'Guidelines for blood pressure management in patients with chronic kidney disease.', 'High', TRUE),
('Diabetes and Kidney Disease', 'ADA/KDIGO', '2024', 'Diabetic Nephropathy', 'Comprehensive approach to managing diabetes-related kidney disease.', 'High', TRUE);

-- Create views for common queries
CREATE VIEW IF NOT EXISTS active_consultations AS
SELECT 
    c.*,
    u.username,
    u.full_name,
    u.email,
    COUNT(m.id) as message_count,
    MAX(m.timestamp) as last_message_time
FROM consultations c
JOIN users u ON c.user_id = u.id
LEFT JOIN messages m ON c.id = m.consultation_id
WHERE c.status = 'active'
GROUP BY c.id;

CREATE VIEW IF NOT EXISTS user_statistics AS
SELECT 
    u.id,
    u.username,
    u.full_name,
    u.role,
    COUNT(DISTINCT c.id) as total_consultations,
    COUNT(DISTINCT a.id) as total_assessments,
    AVG(c.satisfaction_rating) as avg_satisfaction,
    MAX(c.created_at) as last_consultation_date,
    u.created_at as registration_date
FROM users u
LEFT JOIN consultations c ON u.id = c.user_id
LEFT JOIN assessments a ON u.id = a.user_id
GROUP BY u.id;

CREATE VIEW IF NOT EXISTS system_health_metrics AS
SELECT 
    DATE(timestamp) as date,
    COUNT(*) as total_requests,
    AVG(response_time_ms) as avg_response_time,
    COUNT(CASE WHEN status_code >= 400 THEN 1 END) as error_count,
    COUNT(DISTINCT user_id) as active_users
FROM api_usage
WHERE timestamp >= datetime('now', '-30 days')
GROUP BY DATE(timestamp)
ORDER BY date DESC;

-- Insert sample data for testing (optional)
-- Uncomment the following lines if you want sample data

/*
-- Sample admin user (password: admin123)
INSERT OR IGNORE INTO users (username, email, password_hash, full_name, role, is_active, is_verified) VALUES
('admin', 'admin@nephroai.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj/RK.PmvlJO', 'System Administrator', 'admin', TRUE, TRUE);

-- Sample doctor user (password: doctor123)
INSERT OR IGNORE INTO users (username, email, password_hash, full_name, role, specialization, license_number, is_active, is_verified) VALUES
('dr_smith', 'dr.smith@hospital.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj/RK.PmvlJO', 'Dr. John Smith', 'doctor', 'Nephrology', 'MD12345', TRUE, TRUE);

-- Sample patient user (password: patient123)
INSERT OR IGNORE INTO users (username, email, password_hash, full_name, role, is_active, is_verified) VALUES
('patient1', 'patient@email.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj/RK.PmvlJO', 'Jane Doe', 'patient', TRUE, TRUE);
*/

-- Database schema version tracking
CREATE TABLE IF NOT EXISTS schema_version (
    version INTEGER PRIMARY KEY,
    applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    description TEXT
);

INSERT OR IGNORE INTO schema_version (version, description) VALUES
(1, 'Initial enterprise schema with comprehensive tables and indexes');

-- Commit the transaction
COMMIT;