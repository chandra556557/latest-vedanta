import os
import hashlib
import secrets
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import sqlite3
import json
from cryptography.fernet import Fernet
from passlib.context import CryptContext
import jwt
from functools import wraps

class SecurityManager:
    """Enterprise-grade security and compliance manager"""
    
    def __init__(self, db_path: str = "nephro_enterprise.db"):
        self.db_path = db_path
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.secret_key = os.getenv("SECRET_KEY", secrets.token_urlsafe(32))
        self.encryption_key = os.getenv("ENCRYPTION_KEY", Fernet.generate_key())
        self.cipher_suite = Fernet(self.encryption_key)
        self.setup_logging()
        
    def setup_logging(self):
        """Setup security audit logging"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('security_audit.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger('SecurityManager')
    
    def hash_password(self, password: str) -> str:
        """Hash password using bcrypt"""
        return self.pwd_context.hash(password)
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify password against hash"""
        return self.pwd_context.verify(plain_password, hashed_password)
    
    def encrypt_data(self, data: str) -> str:
        """Encrypt sensitive data"""
        return self.cipher_suite.encrypt(data.encode()).decode()
    
    def decrypt_data(self, encrypted_data: str) -> str:
        """Decrypt sensitive data"""
        return self.cipher_suite.decrypt(encrypted_data.encode()).decode()
    
    def generate_token(self, user_id: str, role: str, expires_hours: int = 24) -> str:
        """Generate JWT token"""
        payload = {
            'user_id': user_id,
            'role': role,
            'exp': datetime.utcnow() + timedelta(hours=expires_hours),
            'iat': datetime.utcnow()
        }
        return jwt.encode(payload, self.secret_key, algorithm='HS256')
    
    def verify_token(self, token: str) -> Optional[Dict]:
        """Verify JWT token"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=['HS256'])
            return payload
        except jwt.ExpiredSignatureError:
            self.logger.warning("Token expired")
            return None
        except jwt.InvalidTokenError:
            self.logger.warning("Invalid token")
            return None
    
    def log_security_event(self, event_type: str, user_id: str, details: Dict):
        """Log security events for audit"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO audit_logs (event_type, user_id, event_details, timestamp)
            VALUES (?, ?, ?, ?)
        """, (event_type, user_id, json.dumps(details), datetime.now().isoformat()))
        
        conn.commit()
        conn.close()
        
        self.logger.info(f"Security event: {event_type} for user {user_id}")
    
    def check_rate_limit(self, user_id: str, action: str, limit: int = 100, window_minutes: int = 60) -> bool:
        """Check if user has exceeded rate limit"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        window_start = datetime.now() - timedelta(minutes=window_minutes)
        
        cursor.execute("""
            SELECT COUNT(*) FROM api_usage 
            WHERE user_id = ? AND endpoint LIKE ? AND timestamp > ?
        """, (user_id, f"%{action}%", window_start.isoformat()))
        
        count = cursor.fetchone()[0]
        conn.close()
        
        return count < limit
    
    def validate_input(self, data: Dict, schema: Dict) -> Dict:
        """Validate and sanitize input data"""
        validated = {}
        
        for field, rules in schema.items():
            if field in data:
                value = data[field]
                
                # Type validation
                if 'type' in rules and not isinstance(value, rules['type']):
                    raise ValueError(f"Invalid type for {field}")
                
                # Length validation
                if 'max_length' in rules and len(str(value)) > rules['max_length']:
                    raise ValueError(f"Value too long for {field}")
                
                # Pattern validation
                if 'pattern' in rules:
                    import re
                    if not re.match(rules['pattern'], str(value)):
                        raise ValueError(f"Invalid format for {field}")
                
                validated[field] = value
            elif rules.get('required', False):
                raise ValueError(f"Missing required field: {field}")
        
        return validated

class ComplianceManager:
    """HIPAA and healthcare compliance manager"""
    
    def __init__(self, db_path: str = "nephro_enterprise.db"):
        self.db_path = db_path
        self.logger = logging.getLogger('ComplianceManager')
    
    def anonymize_patient_data(self, data: Dict) -> Dict:
        """Anonymize patient data for compliance"""
        anonymized = data.copy()
        
        # Remove direct identifiers
        sensitive_fields = ['name', 'email', 'phone', 'ssn', 'address']
        for field in sensitive_fields:
            if field in anonymized:
                anonymized[field] = self._hash_identifier(anonymized[field])
        
        # Age ranges instead of exact age
        if 'age' in anonymized:
            age = anonymized['age']
            if age < 18:
                anonymized['age_range'] = 'pediatric'
            elif age < 65:
                anonymized['age_range'] = 'adult'
            else:
                anonymized['age_range'] = 'elderly'
            del anonymized['age']
        
        return anonymized
    
    def _hash_identifier(self, identifier: str) -> str:
        """Hash identifier for anonymization"""
        return hashlib.sha256(identifier.encode()).hexdigest()[:8]
    
    def log_data_access(self, user_id: str, patient_id: str, data_type: str, purpose: str):
        """Log data access for audit trail"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO data_access_logs (user_id, patient_id, data_type, purpose, timestamp)
            VALUES (?, ?, ?, ?, ?)
        """, (user_id, patient_id, data_type, purpose, datetime.now().isoformat()))
        
        conn.commit()
        conn.close()
    
    def generate_compliance_report(self, start_date: str, end_date: str) -> Dict:
        """Generate compliance report"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Data access statistics
        cursor.execute("""
            SELECT data_type, COUNT(*) as access_count
            FROM data_access_logs
            WHERE timestamp BETWEEN ? AND ?
            GROUP BY data_type
        """, (start_date, end_date))
        
        data_access = dict(cursor.fetchall())
        
        # Security events
        cursor.execute("""
            SELECT event_type, COUNT(*) as event_count
            FROM audit_logs
            WHERE timestamp BETWEEN ? AND ?
            GROUP BY event_type
        """, (start_date, end_date))
        
        security_events = dict(cursor.fetchall())
        
        conn.close()
        
        return {
            'period': {'start': start_date, 'end': end_date},
            'data_access': data_access,
            'security_events': security_events,
            'generated_at': datetime.now().isoformat()
        }

class PerformanceMonitor:
    """Performance monitoring and optimization"""
    
    def __init__(self, db_path: str = "nephro_enterprise.db"):
        self.db_path = db_path
        self.logger = logging.getLogger('PerformanceMonitor')
    
    def log_api_performance(self, endpoint: str, response_time: float, status_code: int, user_id: str = None):
        """Log API performance metrics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO performance_metrics (endpoint, response_time, status_code, user_id, timestamp)
            VALUES (?, ?, ?, ?, ?)
        """, (endpoint, response_time, status_code, user_id, datetime.now().isoformat()))
        
        conn.commit()
        conn.close()
    
    def get_performance_stats(self, hours: int = 24) -> Dict:
        """Get performance statistics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        since = datetime.now() - timedelta(hours=hours)
        
        # Average response time by endpoint
        cursor.execute("""
            SELECT endpoint, AVG(response_time) as avg_time, COUNT(*) as request_count
            FROM performance_metrics
            WHERE timestamp > ?
            GROUP BY endpoint
        """, (since.isoformat(),))
        
        endpoint_stats = {}
        for row in cursor.fetchall():
            endpoint_stats[row[0]] = {
                'avg_response_time': round(row[1], 3),
                'request_count': row[2]
            }
        
        # Error rate
        cursor.execute("""
            SELECT 
                COUNT(CASE WHEN status_code >= 400 THEN 1 END) as errors,
                COUNT(*) as total
            FROM performance_metrics
            WHERE timestamp > ?
        """, (since.isoformat(),))
        
        error_stats = cursor.fetchone()
        error_rate = (error_stats[0] / error_stats[1]) * 100 if error_stats[1] > 0 else 0
        
        conn.close()
        
        return {
            'period_hours': hours,
            'endpoint_stats': endpoint_stats,
            'error_rate_percent': round(error_rate, 2),
            'total_requests': error_stats[1]
        }
    
    def check_system_health(self) -> Dict:
        """Check overall system health"""
        import psutil
        
        # System metrics
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        # Database health
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM users")
        user_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM consultations WHERE DATE(created_at) = DATE('now')")
        daily_consultations = cursor.fetchone()[0]
        
        conn.close()
        
        health_status = "healthy"
        if cpu_percent > 80 or memory.percent > 85:
            health_status = "warning"
        if cpu_percent > 95 or memory.percent > 95:
            health_status = "critical"
        
        return {
            'status': health_status,
            'cpu_percent': cpu_percent,
            'memory_percent': memory.percent,
            'disk_percent': disk.percent,
            'user_count': user_count,
            'daily_consultations': daily_consultations,
            'timestamp': datetime.now().isoformat()
        }

def require_auth(role: str = None):
    """Decorator for authentication and authorization"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # This would be implemented with FastAPI dependencies
            # For demonstration purposes
            return func(*args, **kwargs)
        return wrapper
    return decorator

def monitor_performance(func):
    """Decorator for performance monitoring"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = datetime.now()
        try:
            result = func(*args, **kwargs)
            status_code = 200
        except Exception as e:
            status_code = 500
            raise
        finally:
            end_time = datetime.now()
            response_time = (end_time - start_time).total_seconds()
            
            monitor = PerformanceMonitor()
            monitor.log_api_performance(
                endpoint=func.__name__,
                response_time=response_time,
                status_code=status_code
            )
        
        return result
    return wrapper