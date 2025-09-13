import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime, timedelta
import hashlib
import secrets
from typing import Dict, List, Optional
import plotly.express as px
import plotly.graph_objects as go
from dataclasses import dataclass

@dataclass
class PatientRecord:
    patient_id: str
    name: str
    email: str
    phone: str
    date_of_birth: str
    medical_record_number: str
    emergency_contact: str

@dataclass
class Appointment:
    appointment_id: str
    patient_id: str
    doctor_name: str
    appointment_date: str
    appointment_time: str
    status: str
    notes: str

@dataclass
class LabResult:
    result_id: str
    patient_id: str
    test_name: str
    result_value: str
    reference_range: str
    date_collected: str
    status: str

class PatientPortalSystem:
    def __init__(self, db_path: str = "patient_portal.db"):
        self.db_path = db_path
        self.init_database()
        
    def init_database(self):
        """Initialize the patient portal database with required tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Patient authentication table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS patient_auth (
                patient_id TEXT PRIMARY KEY,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                salt TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_login TIMESTAMP,
                is_active BOOLEAN DEFAULT 1
            )
        """)
        
        # Patient records table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS patient_records (
                patient_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                phone TEXT,
                date_of_birth DATE,
                medical_record_number TEXT UNIQUE,
                emergency_contact TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Appointments table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS appointments (
                appointment_id TEXT PRIMARY KEY,
                patient_id TEXT,
                doctor_name TEXT NOT NULL,
                appointment_date DATE NOT NULL,
                appointment_time TIME NOT NULL,
                status TEXT DEFAULT 'scheduled',
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (patient_id) REFERENCES patient_records (patient_id)
            )
        """)
        
        # Lab results table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS lab_results (
                result_id TEXT PRIMARY KEY,
                patient_id TEXT,
                test_name TEXT NOT NULL,
                result_value TEXT NOT NULL,
                reference_range TEXT,
                date_collected DATE NOT NULL,
                status TEXT DEFAULT 'completed',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (patient_id) REFERENCES patient_records (patient_id)
            )
        """)
        
        # Messages table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                message_id TEXT PRIMARY KEY,
                patient_id TEXT,
                sender_type TEXT NOT NULL,
                sender_name TEXT NOT NULL,
                subject TEXT NOT NULL,
                message_body TEXT NOT NULL,
                is_read BOOLEAN DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (patient_id) REFERENCES patient_records (patient_id)
            )
        """)
        
        conn.commit()
        conn.close()
        
        # Add sample data if tables are empty
        self.add_sample_data()
    
    def add_sample_data(self):
        """Add sample data for demonstration"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Check if data already exists
        cursor.execute("SELECT COUNT(*) FROM patient_records")
        if cursor.fetchone()[0] > 0:
            conn.close()
            return
        
        # Sample patients
        sample_patients = [
            ("P001", "John Smith", "john.smith@email.com", "+1-555-0101", "1980-05-15", "MRN001", "Jane Smith +1-555-0102"),
            ("P002", "Maria Garcia", "maria.garcia@email.com", "+1-555-0201", "1975-08-22", "MRN002", "Carlos Garcia +1-555-0202"),
            ("P003", "David Johnson", "david.johnson@email.com", "+1-555-0301", "1990-12-03", "MRN003", "Sarah Johnson +1-555-0302")
        ]
        
        for patient in sample_patients:
            cursor.execute("""
                INSERT INTO patient_records 
                (patient_id, name, email, phone, date_of_birth, medical_record_number, emergency_contact)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, patient)
            
            # Add authentication for each patient
            password = "password123"  # In real implementation, this would be set by patient
            salt = secrets.token_hex(16)
            password_hash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000)
            
            cursor.execute("""
                INSERT INTO patient_auth (patient_id, email, password_hash, salt)
                VALUES (?, ?, ?, ?)
            """, (patient[0], patient[2], password_hash.hex(), salt))
        
        # Sample appointments
        sample_appointments = [
            ("A001", "P001", "Dr. Sarah Wilson", "2024-01-25", "10:00", "scheduled", "Routine checkup"),
            ("A002", "P001", "Dr. Michael Brown", "2024-01-30", "14:30", "scheduled", "Follow-up consultation"),
            ("A003", "P002", "Dr. Sarah Wilson", "2024-01-28", "09:15", "completed", "Blood pressure monitoring"),
            ("A004", "P003", "Dr. Emily Davis", "2024-02-02", "11:00", "scheduled", "Kidney function assessment")
        ]
        
        for appointment in sample_appointments:
            cursor.execute("""
                INSERT INTO appointments 
                (appointment_id, patient_id, doctor_name, appointment_date, appointment_time, status, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, appointment)
        
        # Sample lab results
        sample_lab_results = [
            ("L001", "P001", "Creatinine", "1.2", "0.6-1.3 mg/dL", "2024-01-20", "completed"),
            ("L002", "P001", "BUN", "18", "7-20 mg/dL", "2024-01-20", "completed"),
            ("L003", "P001", "eGFR", "75", ">60 mL/min/1.73m²", "2024-01-20", "completed"),
            ("L004", "P002", "Creatinine", "0.9", "0.6-1.3 mg/dL", "2024-01-22", "completed"),
            ("L005", "P002", "Protein (Urine)", "150", "<150 mg/day", "2024-01-22", "completed"),
            ("L006", "P003", "Creatinine", "1.8", "0.6-1.3 mg/dL", "2024-01-18", "completed")
        ]
        
        for lab_result in sample_lab_results:
            cursor.execute("""
                INSERT INTO lab_results 
                (result_id, patient_id, test_name, result_value, reference_range, date_collected, status)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, lab_result)
        
        # Sample messages
        sample_messages = [
            ("M001", "P001", "doctor", "Dr. Sarah Wilson", "Lab Results Available", "Your recent lab results are now available in your portal. Please review and contact us if you have any questions.", 0),
            ("M002", "P001", "nurse", "Nurse Jennifer", "Appointment Reminder", "This is a reminder for your upcoming appointment on January 25th at 10:00 AM.", 0),
            ("M003", "P002", "doctor", "Dr. Sarah Wilson", "Follow-up Required", "Based on your recent visit, we recommend scheduling a follow-up appointment in 3 months.", 1),
            ("M004", "P003", "admin", "Patient Services", "Insurance Update", "We have updated your insurance information in our system. Please verify the details are correct.", 0)
        ]
        
        for message in sample_messages:
            cursor.execute("""
                INSERT INTO messages 
                (message_id, patient_id, sender_type, sender_name, subject, message_body, is_read)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, message)
        
        conn.commit()
        conn.close()
    
    def authenticate_patient(self, email: str, password: str) -> Optional[str]:
        """Authenticate patient login"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT patient_id, password_hash, salt FROM patient_auth 
            WHERE email = ? AND is_active = 1
        """, (email,))
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            patient_id, stored_hash, salt = result
            password_hash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000)
            
            if password_hash.hex() == stored_hash:
                # Update last login
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE patient_auth SET last_login = CURRENT_TIMESTAMP 
                    WHERE patient_id = ?
                """, (patient_id,))
                conn.commit()
                conn.close()
                return patient_id
        
        return None
    
    def get_patient_record(self, patient_id: str) -> Optional[PatientRecord]:
        """Get patient record by ID"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT patient_id, name, email, phone, date_of_birth, 
                   medical_record_number, emergency_contact
            FROM patient_records WHERE patient_id = ?
        """, (patient_id,))
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return PatientRecord(*result)
        return None
    
    def get_patient_appointments(self, patient_id: str) -> List[Appointment]:
        """Get all appointments for a patient"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT appointment_id, patient_id, doctor_name, appointment_date, 
                   appointment_time, status, notes
            FROM appointments WHERE patient_id = ?
            ORDER BY appointment_date DESC, appointment_time DESC
        """, (patient_id,))
        
        results = cursor.fetchall()
        conn.close()
        
        return [Appointment(*result) for result in results]
    
    def get_patient_lab_results(self, patient_id: str) -> List[LabResult]:
        """Get all lab results for a patient"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT result_id, patient_id, test_name, result_value, 
                   reference_range, date_collected, status
            FROM lab_results WHERE patient_id = ?
            ORDER BY date_collected DESC
        """, (patient_id,))
        
        results = cursor.fetchall()
        conn.close()
        
        return [LabResult(*result) for result in results]
    
    def get_patient_messages(self, patient_id: str) -> List[Dict]:
        """Get all messages for a patient"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT message_id, sender_type, sender_name, subject, 
                   message_body, is_read, created_at
            FROM messages WHERE patient_id = ?
            ORDER BY created_at DESC
        """, (patient_id,))
        
        results = cursor.fetchall()
        conn.close()
        
        return [{
            'message_id': result[0],
            'sender_type': result[1],
            'sender_name': result[2],
            'subject': result[3],
            'message_body': result[4],
            'is_read': bool(result[5]),
            'created_at': result[6]
        } for result in results]
    
    def mark_message_as_read(self, message_id: str):
        """Mark a message as read"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE messages SET is_read = 1 WHERE message_id = ?
        """, (message_id,))
        
        conn.commit()
        conn.close()
    
    def create_lab_results_chart(self, patient_id: str, test_name: str):
        """Create a chart for lab results over time"""
        lab_results = self.get_patient_lab_results(patient_id)
        
        # Filter results for specific test
        filtered_results = [r for r in lab_results if r.test_name == test_name]
        
        if not filtered_results:
            return None
        
        dates = [r.date_collected for r in filtered_results]
        values = [float(r.result_value) for r in filtered_results if r.result_value.replace('.', '').isdigit()]
        
        if not values:
            return None
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=dates,
            y=values,
            mode='lines+markers',
            name=test_name,
            line=dict(color='#1f77b4', width=2),
            marker=dict(size=8)
        ))
        
        fig.update_layout(
            title=f'{test_name} Trends Over Time',
            xaxis_title='Date',
            yaxis_title='Value',
            hovermode='x unified',
            showlegend=True
        )
        
        return fig
    
    def get_dashboard_summary(self, patient_id: str) -> Dict:
        """Get dashboard summary for patient"""
        appointments = self.get_patient_appointments(patient_id)
        lab_results = self.get_patient_lab_results(patient_id)
        messages = self.get_patient_messages(patient_id)
        
        # Count upcoming appointments
        today = datetime.now().date()
        upcoming_appointments = [a for a in appointments if datetime.strptime(a.appointment_date, '%Y-%m-%d').date() >= today]
        
        # Count unread messages
        unread_messages = [m for m in messages if not m['is_read']]
        
        # Recent lab results (last 30 days)
        thirty_days_ago = today - timedelta(days=30)
        recent_labs = [l for l in lab_results if datetime.strptime(l.date_collected, '%Y-%m-%d').date() >= thirty_days_ago]
        
        return {
            'total_appointments': len(appointments),
            'upcoming_appointments': len(upcoming_appointments),
            'total_lab_results': len(lab_results),
            'recent_lab_results': len(recent_labs),
            'total_messages': len(messages),
            'unread_messages': len(unread_messages)
        }