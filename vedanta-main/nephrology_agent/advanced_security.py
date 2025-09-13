import hashlib
import secrets
import time
import jwt
import sqlite3
from datetime import datetime, timedelta
from typing import Dict, Optional, List, Tuple
import streamlit as st
import re
from dataclasses import dataclass
from enum import Enum
import logging

class SecurityLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class AuthenticationMethod(Enum):
    PASSWORD = "password"
    TWO_FACTOR = "2fa"
    BIOMETRIC = "biometric"
    SSO = "sso"

@dataclass
class SecurityEvent:
    event_type: str
    user_id: str
    ip_address: str
    timestamp: datetime
    details: Dict
    risk_level: SecurityLevel

class AdvancedSecurityManager:
    def __init__(self, db_path: str = "nephro_security.db"):
        self.db_path = db_path
        self.secret_key = self._get_or_create_secret_key()
        self.failed_attempts = {}
        self.session_tokens = {}
        self.security_events = []
        self.init_security_database()
        
        # Security configuration
        self.config = {
            'max_failed_attempts': 5,
            'lockout_duration': 900,  # 15 minutes
            'session_timeout': 3600,  # 1 hour
            'password_min_length': 8,
            'require_special_chars': True,
            'require_numbers': True,
            'require_uppercase': True,
            'token_expiry': 86400,  # 24 hours
            'enable_2fa': True,
            'enable_audit_logging': True,
            'max_concurrent_sessions': 3
        }
    
    def _get_or_create_secret_key(self) -> str:
        """Get or create a secret key for JWT tokens"""
        try:
            with open('.security_key', 'r') as f:
                return f.read().strip()
        except FileNotFoundError:
            key = secrets.token_urlsafe(32)
            with open('.security_key', 'w') as f:
                f.write(key)
            return key
    
    def init_security_database(self):
        """Initialize security database tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Users table with enhanced security fields
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS secure_users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                salt TEXT NOT NULL,
                role TEXT DEFAULT 'user',
                is_active BOOLEAN DEFAULT 1,
                is_locked BOOLEAN DEFAULT 0,
                failed_attempts INTEGER DEFAULT 0,
                last_failed_attempt TIMESTAMP,
                last_login TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                two_factor_enabled BOOLEAN DEFAULT 0,
                two_factor_secret TEXT,
                password_reset_token TEXT,
                password_reset_expires TIMESTAMP,
                security_questions TEXT,  -- JSON string
                login_history TEXT  -- JSON string
            )
        """)
        
        # Sessions table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                session_token TEXT UNIQUE NOT NULL,
                ip_address TEXT,
                user_agent TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                expires_at TIMESTAMP,
                is_active BOOLEAN DEFAULT 1,
                last_activity TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES secure_users (id)
            )
        """)
        
        # Security events table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS security_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                event_type TEXT NOT NULL,
                user_id INTEGER,
                ip_address TEXT,
                user_agent TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                details TEXT,  -- JSON string
                risk_level TEXT,
                resolved BOOLEAN DEFAULT 0
            )
        """)
        
        # Audit log table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS audit_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                action TEXT NOT NULL,
                resource TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                ip_address TEXT,
                user_agent TEXT,
                details TEXT,  -- JSON string
                success BOOLEAN DEFAULT 1
            )
        """)
        
        conn.commit()
        conn.close()
    
    def hash_password(self, password: str, salt: str = None) -> Tuple[str, str]:
        """Hash password with salt"""
        if salt is None:
            salt = secrets.token_hex(16)
        
        # Use PBKDF2 with SHA-256
        password_hash = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt.encode('utf-8'),
            100000  # iterations
        )
        
        return password_hash.hex(), salt
    
    def verify_password(self, password: str, password_hash: str, salt: str) -> bool:
        """Verify password against hash"""
        computed_hash, _ = self.hash_password(password, salt)
        return secrets.compare_digest(computed_hash, password_hash)
    
    def validate_password_strength(self, password: str) -> Tuple[bool, List[str]]:
        """Validate password strength"""
        errors = []
        
        if len(password) < self.config['password_min_length']:
            errors.append(f"Password must be at least {self.config['password_min_length']} characters long")
        
        if self.config['require_uppercase'] and not re.search(r'[A-Z]', password):
            errors.append("Password must contain at least one uppercase letter")
        
        if self.config['require_numbers'] and not re.search(r'\d', password):
            errors.append("Password must contain at least one number")
        
        if self.config['require_special_chars'] and not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            errors.append("Password must contain at least one special character")
        
        # Check for common weak passwords
        weak_passwords = ['password', '123456', 'qwerty', 'admin', 'letmein']
        if password.lower() in weak_passwords:
            errors.append("Password is too common and easily guessable")
        
        return len(errors) == 0, errors
    
    def create_user(self, username: str, email: str, password: str, role: str = 'user') -> Tuple[bool, str]:
        """Create a new user with enhanced security"""
        # Validate password strength
        is_strong, errors = self.validate_password_strength(password)
        if not is_strong:
            return False, "; ".join(errors)
        
        # Hash password
        password_hash, salt = self.hash_password(password)
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO secure_users (username, email, password_hash, salt, role)
                VALUES (?, ?, ?, ?, ?)
            """, (username, email, password_hash, salt, role))
            
            user_id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            # Log security event
            self.log_security_event(
                'user_created',
                str(user_id),
                self._get_client_ip(),
                {'username': username, 'email': email, 'role': role},
                SecurityLevel.LOW
            )
            
            return True, "User created successfully"
            
        except sqlite3.IntegrityError as e:
            if 'username' in str(e):
                return False, "Username already exists"
            elif 'email' in str(e):
                return False, "Email already exists"
            else:
                return False, "User creation failed"
        except Exception as e:
            return False, f"Error creating user: {str(e)}"
    
    def authenticate_user(self, username: str, password: str) -> Tuple[bool, Optional[Dict], str]:
        """Authenticate user with enhanced security checks"""
        ip_address = self._get_client_ip()
        
        # Check for account lockout
        if self._is_account_locked(username):
            self.log_security_event(
                'login_attempt_locked_account',
                username,
                ip_address,
                {'username': username},
                SecurityLevel.HIGH
            )
            return False, None, "Account is temporarily locked due to multiple failed attempts"
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT id, username, email, password_hash, salt, role, is_active, failed_attempts
                FROM secure_users WHERE username = ? OR email = ?
            """, (username, username))
            
            user = cursor.fetchone()
            
            if not user:
                self._record_failed_attempt(username, ip_address)
                return False, None, "Invalid username or password"
            
            user_id, db_username, email, password_hash, salt, role, is_active, failed_attempts = user
            
            if not is_active:
                self.log_security_event(
                    'login_attempt_inactive_account',
                    str(user_id),
                    ip_address,
                    {'username': db_username},
                    SecurityLevel.MEDIUM
                )
                return False, None, "Account is inactive"
            
            # Verify password
            if self.verify_password(password, password_hash, salt):
                # Reset failed attempts on successful login
                cursor.execute("""
                    UPDATE secure_users 
                    SET failed_attempts = 0, last_failed_attempt = NULL, last_login = CURRENT_TIMESTAMP
                    WHERE id = ?
                """, (user_id,))
                
                conn.commit()
                conn.close()
                
                # Create session token
                session_token = self._create_session_token(user_id, ip_address)
                
                user_data = {
                    'id': user_id,
                    'username': db_username,
                    'email': email,
                    'role': role,
                    'session_token': session_token
                }
                
                self.log_security_event(
                    'successful_login',
                    str(user_id),
                    ip_address,
                    {'username': db_username},
                    SecurityLevel.LOW
                )
                
                return True, user_data, "Login successful"
            else:
                self._record_failed_attempt(username, ip_address, user_id)
                conn.close()
                return False, None, "Invalid username or password"
                
        except Exception as e:
            return False, None, f"Authentication error: {str(e)}"
    
    def _create_session_token(self, user_id: int, ip_address: str) -> str:
        """Create a secure session token"""
        payload = {
            'user_id': user_id,
            'ip_address': ip_address,
            'iat': datetime.utcnow(),
            'exp': datetime.utcnow() + timedelta(seconds=self.config['token_expiry'])
        }
        
        token = jwt.encode(payload, self.secret_key, algorithm='HS256')
        
        # Store session in database
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO user_sessions (user_id, session_token, ip_address, expires_at)
            VALUES (?, ?, ?, ?)
        """, (
            user_id, 
            token, 
            ip_address, 
            datetime.utcnow() + timedelta(seconds=self.config['token_expiry'])
        ))
        
        conn.commit()
        conn.close()
        
        return token
    
    def validate_session_token(self, token: str) -> Tuple[bool, Optional[Dict]]:
        """Validate session token"""
        try:
            # Decode JWT token
            payload = jwt.decode(token, self.secret_key, algorithms=['HS256'])
            
            # Check if session exists in database
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT s.user_id, s.expires_at, s.is_active, u.username, u.role
                FROM user_sessions s
                JOIN secure_users u ON s.user_id = u.id
                WHERE s.session_token = ? AND s.is_active = 1
            """, (token,))
            
            session = cursor.fetchone()
            conn.close()
            
            if not session:
                return False, None
            
            user_id, expires_at, is_active, username, role = session
            
            # Check if session has expired
            if datetime.fromisoformat(expires_at) < datetime.utcnow():
                self._invalidate_session(token)
                return False, None
            
            return True, {
                'user_id': user_id,
                'username': username,
                'role': role,
                'token': token
            }
            
        except jwt.ExpiredSignatureError:
            self._invalidate_session(token)
            return False, None
        except jwt.InvalidTokenError:
            return False, None
        except Exception:
            return False, None
    
    def _invalidate_session(self, token: str):
        """Invalidate a session token"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE user_sessions SET is_active = 0 WHERE session_token = ?
        """, (token,))
        
        conn.commit()
        conn.close()
    
    def logout_user(self, token: str):
        """Logout user and invalidate session"""
        self._invalidate_session(token)
        
        # Log security event
        is_valid, user_data = self.validate_session_token(token)
        if user_data:
            self.log_security_event(
                'user_logout',
                str(user_data['user_id']),
                self._get_client_ip(),
                {'username': user_data['username']},
                SecurityLevel.LOW
            )
    
    def _record_failed_attempt(self, username: str, ip_address: str, user_id: int = None):
        """Record failed login attempt"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if user_id:
            cursor.execute("""
                UPDATE secure_users 
                SET failed_attempts = failed_attempts + 1, last_failed_attempt = CURRENT_TIMESTAMP
                WHERE id = ?
            """, (user_id,))
        
        conn.commit()
        conn.close()
        
        self.log_security_event(
            'failed_login_attempt',
            str(user_id) if user_id else username,
            ip_address,
            {'username': username, 'user_id': user_id},
            SecurityLevel.MEDIUM
        )
    
    def _is_account_locked(self, username: str) -> bool:
        """Check if account is locked due to failed attempts"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT failed_attempts, last_failed_attempt, is_locked
            FROM secure_users WHERE username = ? OR email = ?
        """, (username, username))
        
        result = cursor.fetchone()
        conn.close()
        
        if not result:
            return False
        
        failed_attempts, last_failed_attempt, is_locked = result
        
        if is_locked:
            return True
        
        if failed_attempts >= self.config['max_failed_attempts']:
            if last_failed_attempt:
                last_attempt_time = datetime.fromisoformat(last_failed_attempt)
                if (datetime.utcnow() - last_attempt_time).seconds < self.config['lockout_duration']:
                    return True
        
        return False
    
    def log_security_event(self, event_type: str, user_id: str, ip_address: str, 
                          details: Dict, risk_level: SecurityLevel):
        """Log security event"""
        if not self.config['enable_audit_logging']:
            return
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO security_events (event_type, user_id, ip_address, details, risk_level)
            VALUES (?, ?, ?, ?, ?)
        """, (event_type, user_id, ip_address, str(details), risk_level.value))
        
        conn.commit()
        conn.close()
    
    def get_security_events(self, limit: int = 100) -> List[Dict]:
        """Get recent security events"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT event_type, user_id, ip_address, timestamp, details, risk_level
            FROM security_events
            ORDER BY timestamp DESC
            LIMIT ?
        """, (limit,))
        
        events = []
        for row in cursor.fetchall():
            events.append({
                'event_type': row[0],
                'user_id': row[1],
                'ip_address': row[2],
                'timestamp': row[3],
                'details': row[4],
                'risk_level': row[5]
            })
        
        conn.close()
        return events
    
    def _get_client_ip(self) -> str:
        """Get client IP address from Streamlit context"""
        try:
            # Try to get real IP from headers
            if hasattr(st, 'context') and hasattr(st.context, 'headers'):
                headers = st.context.headers
                return (headers.get('X-Forwarded-For', '') or 
                       headers.get('X-Real-IP', '') or 
                       headers.get('Remote-Addr', '127.0.0.1')).split(',')[0].strip()
            return '127.0.0.1'
        except:
            return '127.0.0.1'
    
    def generate_security_report(self) -> Dict:
        """Generate comprehensive security report"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get user statistics
        cursor.execute("SELECT COUNT(*) FROM secure_users")
        total_users = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM secure_users WHERE is_active = 1")
        active_users = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM secure_users WHERE is_locked = 1")
        locked_users = cursor.fetchone()[0]
        
        # Get session statistics
        cursor.execute("SELECT COUNT(*) FROM user_sessions WHERE is_active = 1")
        active_sessions = cursor.fetchone()[0]
        
        # Get security event statistics
        cursor.execute("""
            SELECT risk_level, COUNT(*) 
            FROM security_events 
            WHERE timestamp > datetime('now', '-7 days')
            GROUP BY risk_level
        """)
        
        risk_stats = {}
        for row in cursor.fetchall():
            risk_stats[row[0]] = row[1]
        
        # Get failed login attempts in last 24 hours
        cursor.execute("""
            SELECT COUNT(*) FROM security_events 
            WHERE event_type = 'failed_login_attempt' 
            AND timestamp > datetime('now', '-1 day')
        """)
        
        failed_logins_24h = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            'total_users': total_users,
            'active_users': active_users,
            'locked_users': locked_users,
            'active_sessions': active_sessions,
            'risk_statistics': risk_stats,
            'failed_logins_24h': failed_logins_24h,
            'security_config': self.config
        }

# Global instance
_security_manager = None

def get_security_manager() -> AdvancedSecurityManager:
    """Get the global security manager instance"""
    global _security_manager
    if _security_manager is None:
        _security_manager = AdvancedSecurityManager()
    return _security_manager