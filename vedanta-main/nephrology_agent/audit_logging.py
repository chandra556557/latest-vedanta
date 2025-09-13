import sqlite3
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from enum import Enum
from dataclasses import dataclass, asdict
import hashlib
import uuid
import streamlit as st
import pandas as pd
from pathlib import Path

class AuditEventType(Enum):
    """Types of audit events"""
    USER_LOGIN = "user_login"
    USER_LOGOUT = "user_logout"
    USER_REGISTRATION = "user_registration"
    PASSWORD_CHANGE = "password_change"
    PROFILE_UPDATE = "profile_update"
    DATA_ACCESS = "data_access"
    DATA_MODIFICATION = "data_modification"
    DATA_DELETION = "data_deletion"
    SYSTEM_ACCESS = "system_access"
    CONFIGURATION_CHANGE = "configuration_change"
    SECURITY_EVENT = "security_event"
    ERROR_EVENT = "error_event"
    CONSULTATION_START = "consultation_start"
    CONSULTATION_END = "consultation_end"
    REPORT_GENERATION = "report_generation"
    EXPORT_DATA = "export_data"
    IMPORT_DATA = "import_data"
    ADMIN_ACTION = "admin_action"
    API_ACCESS = "api_access"
    FILE_UPLOAD = "file_upload"
    FILE_DOWNLOAD = "file_download"

class AuditSeverity(Enum):
    """Severity levels for audit events"""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"

@dataclass
class AuditEvent:
    """Audit event data structure"""
    event_id: str
    event_type: AuditEventType
    timestamp: datetime
    user_id: Optional[str]
    username: Optional[str]
    ip_address: str
    user_agent: str
    session_id: Optional[str]
    resource: Optional[str]
    action: str
    details: Dict[str, Any]
    severity: AuditSeverity
    success: bool
    duration_ms: Optional[int]
    request_id: Optional[str]
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for storage"""
        data = asdict(self)
        data['event_type'] = self.event_type.value
        data['severity'] = self.severity.value
        data['timestamp'] = self.timestamp.isoformat()
        data['details'] = json.dumps(self.details)
        return data

class AuditLogger:
    """Comprehensive audit logging system"""
    
    def __init__(self, db_path: str = "nephro_audit.db", log_file: str = "audit.log"):
        self.db_path = db_path
        self.log_file = log_file
        self.init_database()
        self.init_file_logger()
        
        # Configuration
        self.config = {
            'retention_days': 365,  # Keep audit logs for 1 year
            'max_log_size_mb': 100,
            'enable_file_logging': True,
            'enable_db_logging': True,
            'enable_real_time_alerts': True,
            'sensitive_fields': ['password', 'ssn', 'credit_card', 'token'],
            'log_level': logging.INFO
        }
        
        # In-memory cache for recent events
        self.recent_events = []
        self.max_recent_events = 1000
    
    def init_database(self):
        """Initialize audit database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Main audit log table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS audit_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                event_id TEXT UNIQUE NOT NULL,
                event_type TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                user_id TEXT,
                username TEXT,
                ip_address TEXT NOT NULL,
                user_agent TEXT,
                session_id TEXT,
                resource TEXT,
                action TEXT NOT NULL,
                details TEXT,
                severity TEXT NOT NULL,
                success BOOLEAN NOT NULL,
                duration_ms INTEGER,
                request_id TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Index for performance
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_audit_timestamp ON audit_log(timestamp)
        """)
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_audit_user_id ON audit_log(user_id)
        """)
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_audit_event_type ON audit_log(event_type)
        """)
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_audit_severity ON audit_log(severity)
        """)
        
        # Audit summary table for quick statistics
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS audit_summary (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                event_type TEXT NOT NULL,
                severity TEXT NOT NULL,
                count INTEGER NOT NULL,
                success_count INTEGER NOT NULL,
                failure_count INTEGER NOT NULL,
                unique_users INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(date, event_type, severity)
            )
        """)
        
        # Data integrity table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS audit_integrity (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                total_events INTEGER NOT NULL,
                checksum TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(date)
            )
        """)
        
        conn.commit()
        conn.close()
    
    def init_file_logger(self):
        """Initialize file-based logging"""
        if not self.config['enable_file_logging']:
            return
        
        # Create logs directory if it doesn't exist
        log_dir = Path(self.log_file).parent
        log_dir.mkdir(exist_ok=True)
        
        # Configure file logger
        self.file_logger = logging.getLogger('audit_file_logger')
        self.file_logger.setLevel(self.config['log_level'])
        
        # Create file handler with rotation
        handler = logging.FileHandler(self.log_file)
        formatter = logging.Formatter(
            '%(asctime)s | %(levelname)s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        handler.setFormatter(formatter)
        self.file_logger.addHandler(handler)
    
    def log_event(self, 
                  event_type: AuditEventType,
                  action: str,
                  user_id: Optional[str] = None,
                  username: Optional[str] = None,
                  resource: Optional[str] = None,
                  details: Dict[str, Any] = None,
                  severity: AuditSeverity = AuditSeverity.INFO,
                  success: bool = True,
                  duration_ms: Optional[int] = None) -> str:
        """Log an audit event"""
        
        # Generate unique event ID
        event_id = str(uuid.uuid4())
        
        # Get request context
        ip_address = self._get_client_ip()
        user_agent = self._get_user_agent()
        session_id = self._get_session_id()
        request_id = self._get_request_id()
        
        # Sanitize details
        if details:
            details = self._sanitize_sensitive_data(details)
        else:
            details = {}
        
        # Create audit event
        event = AuditEvent(
            event_id=event_id,
            event_type=event_type,
            timestamp=datetime.utcnow(),
            user_id=user_id,
            username=username,
            ip_address=ip_address,
            user_agent=user_agent,
            session_id=session_id,
            resource=resource,
            action=action,
            details=details,
            severity=severity,
            success=success,
            duration_ms=duration_ms,
            request_id=request_id
        )
        
        # Store in database
        if self.config['enable_db_logging']:
            self._store_in_database(event)
        
        # Log to file
        if self.config['enable_file_logging']:
            self._log_to_file(event)
        
        # Add to recent events cache
        self.recent_events.append(event)
        if len(self.recent_events) > self.max_recent_events:
            self.recent_events.pop(0)
        
        # Real-time alerts for critical events
        if (self.config['enable_real_time_alerts'] and 
            severity in [AuditSeverity.ERROR, AuditSeverity.CRITICAL]):
            self._send_alert(event)
        
        return event_id
    
    def _store_in_database(self, event: AuditEvent):
        """Store audit event in database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            event_dict = event.to_dict()
            
            cursor.execute("""
                INSERT INTO audit_log (
                    event_id, event_type, timestamp, user_id, username,
                    ip_address, user_agent, session_id, resource, action,
                    details, severity, success, duration_ms, request_id
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                event_dict['event_id'],
                event_dict['event_type'],
                event_dict['timestamp'],
                event_dict['user_id'],
                event_dict['username'],
                event_dict['ip_address'],
                event_dict['user_agent'],
                event_dict['session_id'],
                event_dict['resource'],
                event_dict['action'],
                event_dict['details'],
                event_dict['severity'],
                event_dict['success'],
                event_dict['duration_ms'],
                event_dict['request_id']
            ))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            # Log error but don't fail the main operation
            print(f"Error storing audit event: {e}")
    
    def _log_to_file(self, event: AuditEvent):
        """Log audit event to file"""
        try:
            log_message = (
                f"ID:{event.event_id} | "
                f"TYPE:{event.event_type.value} | "
                f"USER:{event.username or 'anonymous'} | "
                f"ACTION:{event.action} | "
                f"RESOURCE:{event.resource or 'N/A'} | "
                f"SUCCESS:{event.success} | "
                f"IP:{event.ip_address} | "
                f"DETAILS:{json.dumps(event.details)}"
            )
            
            if event.severity == AuditSeverity.INFO:
                self.file_logger.info(log_message)
            elif event.severity == AuditSeverity.WARNING:
                self.file_logger.warning(log_message)
            elif event.severity == AuditSeverity.ERROR:
                self.file_logger.error(log_message)
            elif event.severity == AuditSeverity.CRITICAL:
                self.file_logger.critical(log_message)
                
        except Exception as e:
            print(f"Error logging to file: {e}")
    
    def _sanitize_sensitive_data(self, details: Dict[str, Any]) -> Dict[str, Any]:
        """Remove or mask sensitive data from details"""
        sanitized = details.copy()
        
        for key, value in sanitized.items():
            key_lower = key.lower()
            
            # Check if key contains sensitive field names
            for sensitive_field in self.config['sensitive_fields']:
                if sensitive_field in key_lower:
                    if isinstance(value, str) and len(value) > 4:
                        # Mask all but last 4 characters
                        sanitized[key] = '*' * (len(value) - 4) + value[-4:]
                    else:
                        sanitized[key] = '***MASKED***'
                    break
        
        return sanitized
    
    def _send_alert(self, event: AuditEvent):
        """Send real-time alert for critical events"""
        # In a real implementation, this would send emails, SMS, or push notifications
        # For now, we'll just log it
        alert_message = (
            f"CRITICAL AUDIT EVENT: {event.event_type.value} | "
            f"User: {event.username} | "
            f"Action: {event.action} | "
            f"Time: {event.timestamp}"
        )
        print(f"ALERT: {alert_message}")
    
    def get_audit_events(self, 
                        start_date: Optional[datetime] = None,
                        end_date: Optional[datetime] = None,
                        user_id: Optional[str] = None,
                        event_type: Optional[AuditEventType] = None,
                        severity: Optional[AuditSeverity] = None,
                        limit: int = 1000) -> List[Dict]:
        """Retrieve audit events with filtering"""
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        query = "SELECT * FROM audit_log WHERE 1=1"
        params = []
        
        if start_date:
            query += " AND timestamp >= ?"
            params.append(start_date.isoformat())
        
        if end_date:
            query += " AND timestamp <= ?"
            params.append(end_date.isoformat())
        
        if user_id:
            query += " AND user_id = ?"
            params.append(user_id)
        
        if event_type:
            query += " AND event_type = ?"
            params.append(event_type.value)
        
        if severity:
            query += " AND severity = ?"
            params.append(severity.value)
        
        query += " ORDER BY timestamp DESC LIMIT ?"
        params.append(limit)
        
        cursor.execute(query, params)
        
        columns = [description[0] for description in cursor.description]
        events = []
        
        for row in cursor.fetchall():
            event_dict = dict(zip(columns, row))
            # Parse JSON details
            if event_dict['details']:
                try:
                    event_dict['details'] = json.loads(event_dict['details'])
                except:
                    event_dict['details'] = {}
            events.append(event_dict)
        
        conn.close()
        return events
    
    def get_audit_statistics(self, days: int = 30) -> Dict:
        """Get audit statistics for the specified period"""
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=days)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Total events
        cursor.execute("""
            SELECT COUNT(*) FROM audit_log 
            WHERE timestamp >= ? AND timestamp <= ?
        """, (start_date.isoformat(), end_date.isoformat()))
        total_events = cursor.fetchone()[0]
        
        # Events by type
        cursor.execute("""
            SELECT event_type, COUNT(*) FROM audit_log 
            WHERE timestamp >= ? AND timestamp <= ?
            GROUP BY event_type
            ORDER BY COUNT(*) DESC
        """, (start_date.isoformat(), end_date.isoformat()))
        events_by_type = dict(cursor.fetchall())
        
        # Events by severity
        cursor.execute("""
            SELECT severity, COUNT(*) FROM audit_log 
            WHERE timestamp >= ? AND timestamp <= ?
            GROUP BY severity
        """, (start_date.isoformat(), end_date.isoformat()))
        events_by_severity = dict(cursor.fetchall())
        
        # Unique users
        cursor.execute("""
            SELECT COUNT(DISTINCT user_id) FROM audit_log 
            WHERE timestamp >= ? AND timestamp <= ? AND user_id IS NOT NULL
        """, (start_date.isoformat(), end_date.isoformat()))
        unique_users = cursor.fetchone()[0]
        
        # Failed events
        cursor.execute("""
            SELECT COUNT(*) FROM audit_log 
            WHERE timestamp >= ? AND timestamp <= ? AND success = 0
        """, (start_date.isoformat(), end_date.isoformat()))
        failed_events = cursor.fetchone()[0]
        
        # Top users by activity
        cursor.execute("""
            SELECT username, COUNT(*) FROM audit_log 
            WHERE timestamp >= ? AND timestamp <= ? AND username IS NOT NULL
            GROUP BY username
            ORDER BY COUNT(*) DESC
            LIMIT 10
        """, (start_date.isoformat(), end_date.isoformat()))
        top_users = dict(cursor.fetchall())
        
        conn.close()
        
        return {
            'period_days': days,
            'total_events': total_events,
            'events_by_type': events_by_type,
            'events_by_severity': events_by_severity,
            'unique_users': unique_users,
            'failed_events': failed_events,
            'success_rate': ((total_events - failed_events) / total_events * 100) if total_events > 0 else 0,
            'top_users': top_users
        }
    
    def generate_audit_report(self, start_date: datetime, end_date: datetime) -> Dict:
        """Generate comprehensive audit report"""
        events = self.get_audit_events(start_date, end_date, limit=10000)
        
        # Convert to DataFrame for analysis
        df = pd.DataFrame(events)
        
        if df.empty:
            return {'error': 'No audit events found for the specified period'}
        
        # Basic statistics
        total_events = len(df)
        unique_users = df['user_id'].nunique()
        success_rate = (df['success'].sum() / total_events * 100) if total_events > 0 else 0
        
        # Events by day
        df['date'] = pd.to_datetime(df['timestamp']).dt.date
        events_by_day = df.groupby('date').size().to_dict()
        
        # Most active users
        top_users = df[df['username'].notna()]['username'].value_counts().head(10).to_dict()
        
        # Most common actions
        top_actions = df['action'].value_counts().head(10).to_dict()
        
        # Error analysis
        error_events = df[df['success'] == False]
        error_types = error_events['event_type'].value_counts().to_dict()
        
        # Security events
        security_events = df[df['event_type'] == 'security_event']
        security_count = len(security_events)
        
        return {
            'period': {
                'start_date': start_date.isoformat(),
                'end_date': end_date.isoformat()
            },
            'summary': {
                'total_events': total_events,
                'unique_users': unique_users,
                'success_rate': round(success_rate, 2),
                'security_events': security_count
            },
            'trends': {
                'events_by_day': {str(k): v for k, v in events_by_day.items()},
                'top_users': top_users,
                'top_actions': top_actions
            },
            'security': {
                'error_types': error_types,
                'failed_logins': len(df[df['event_type'] == 'user_login'][df['success'] == False]),
                'security_events': security_count
            }
        }
    
    def cleanup_old_logs(self, retention_days: int = None):
        """Clean up old audit logs based on retention policy"""
        if retention_days is None:
            retention_days = self.config['retention_days']
        
        cutoff_date = datetime.utcnow() - timedelta(days=retention_days)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Count events to be deleted
        cursor.execute(
            "SELECT COUNT(*) FROM audit_log WHERE timestamp < ?",
            (cutoff_date.isoformat(),)
        )
        count_to_delete = cursor.fetchone()[0]
        
        if count_to_delete > 0:
            # Delete old events
            cursor.execute(
                "DELETE FROM audit_log WHERE timestamp < ?",
                (cutoff_date.isoformat(),)
            )
            
            # Log the cleanup action
            self.log_event(
                AuditEventType.ADMIN_ACTION,
                "cleanup_old_logs",
                details={
                    'deleted_events': count_to_delete,
                    'retention_days': retention_days,
                    'cutoff_date': cutoff_date.isoformat()
                },
                severity=AuditSeverity.INFO
            )
        
        conn.commit()
        conn.close()
        
        return count_to_delete
    
    def _get_client_ip(self) -> str:
        """Get client IP address"""
        try:
            # Try to get real IP from Streamlit context
            if hasattr(st, 'context') and hasattr(st.context, 'headers'):
                headers = st.context.headers
                return (headers.get('X-Forwarded-For', '') or 
                       headers.get('X-Real-IP', '') or 
                       headers.get('Remote-Addr', '127.0.0.1')).split(',')[0].strip()
            return '127.0.0.1'
        except:
            return '127.0.0.1'
    
    def _get_user_agent(self) -> str:
        """Get user agent string"""
        try:
            if hasattr(st, 'context') and hasattr(st.context, 'headers'):
                return st.context.headers.get('User-Agent', 'Unknown')
            return 'Unknown'
        except:
            return 'Unknown'
    
    def _get_session_id(self) -> Optional[str]:
        """Get session ID"""
        try:
            return getattr(st.session_state, 'session_id', None)
        except:
            return None
    
    def _get_request_id(self) -> Optional[str]:
        """Get request ID"""
        try:
            return getattr(st.session_state, 'request_id', None)
        except:
            return None

# Global instance
_audit_logger = None

def get_audit_logger() -> AuditLogger:
    """Get the global audit logger instance"""
    global _audit_logger
    if _audit_logger is None:
        _audit_logger = AuditLogger()
    return _audit_logger

# Convenience functions
def log_user_action(action: str, user_id: str = None, username: str = None, 
                   resource: str = None, details: Dict = None, success: bool = True):
    """Log a user action"""
    logger = get_audit_logger()
    logger.log_event(
        AuditEventType.DATA_ACCESS,
        action,
        user_id=user_id,
        username=username,
        resource=resource,
        details=details,
        success=success
    )

def log_security_event(action: str, details: Dict = None, severity: AuditSeverity = AuditSeverity.WARNING):
    """Log a security event"""
    logger = get_audit_logger()
    logger.log_event(
        AuditEventType.SECURITY_EVENT,
        action,
        details=details,
        severity=severity
    )

def log_system_event(action: str, details: Dict = None, success: bool = True):
    """Log a system event"""
    logger = get_audit_logger()
    logger.log_event(
        AuditEventType.SYSTEM_ACCESS,
        action,
        details=details,
        success=success
    )