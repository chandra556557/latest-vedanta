import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime, timedelta
import time
import json
from typing import Dict, List, Any, Optional
import sqlite3
from dataclasses import dataclass
from enum import Enum

class AlertSeverity(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

@dataclass
class Alert:
    id: str
    patient_id: str
    alert_type: str
    severity: AlertSeverity
    message: str
    timestamp: datetime
    acknowledged: bool = False
    resolved: bool = False
    
class RealTimeMonitoringSystem:
    """Real-time monitoring system for nephrology patients with intelligent alerts."""
    
    def __init__(self):
        self.alerts_db = "monitoring_alerts.db"
        self.init_alerts_database()
        self.alert_thresholds = {
            'creatinine_high': 2.0,
            'creatinine_rapid_rise': 0.3,  # mg/dL increase in 48h
            'gfr_low': 30,
            'gfr_rapid_decline': 5,  # mL/min/1.73m² decline in 30 days
            'blood_pressure_high': (160, 100),
            'proteinuria_high': 300,  # mg/g
            'potassium_high': 5.5,
            'potassium_low': 3.0
        }
    
    def init_alerts_database(self):
        """Initialize the alerts database."""
        conn = sqlite3.connect(self.alerts_db)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS alerts (
                id TEXT PRIMARY KEY,
                patient_id TEXT,
                alert_type TEXT,
                severity TEXT,
                message TEXT,
                timestamp TEXT,
                acknowledged INTEGER DEFAULT 0,
                resolved INTEGER DEFAULT 0
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS patient_vitals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_id TEXT,
                timestamp TEXT,
                vital_type TEXT,
                value REAL,
                unit TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def add_patient_vital(self, patient_id: str, vital_type: str, value: float, unit: str):
        """Add a new vital sign measurement for a patient."""
        conn = sqlite3.connect(self.alerts_db)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO patient_vitals (patient_id, timestamp, vital_type, value, unit)
            VALUES (?, ?, ?, ?, ?)
        ''', (patient_id, datetime.now().isoformat(), vital_type, value, unit))
        
        conn.commit()
        conn.close()
        
        # Check for alerts after adding new vital
        self.check_alerts_for_patient(patient_id)
    
    def get_patient_vitals(self, patient_id: str, hours_back: int = 24) -> pd.DataFrame:
        """Get recent vital signs for a patient."""
        conn = sqlite3.connect(self.alerts_db)
        
        cutoff_time = datetime.now() - timedelta(hours=hours_back)
        
        query = '''
            SELECT * FROM patient_vitals 
            WHERE patient_id = ? AND timestamp > ?
            ORDER BY timestamp DESC
        '''
        
        df = pd.read_sql_query(query, conn, params=(patient_id, cutoff_time.isoformat()))
        conn.close()
        
        if not df.empty:
            df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        return df
    
    def check_alerts_for_patient(self, patient_id: str):
        """Check for alert conditions for a specific patient."""
        vitals_df = self.get_patient_vitals(patient_id, hours_back=72)
        
        if vitals_df.empty:
            return
        
        # Check creatinine alerts
        creatinine_data = vitals_df[vitals_df['vital_type'] == 'creatinine'].sort_values('timestamp')
        if not creatinine_data.empty:
            latest_creatinine = creatinine_data.iloc[-1]['value']
            
            # High creatinine alert
            if latest_creatinine > self.alert_thresholds['creatinine_high']:
                self.create_alert(
                    patient_id=patient_id,
                    alert_type="high_creatinine",
                    severity=AlertSeverity.HIGH,
                    message=f"Creatinine elevated to {latest_creatinine} mg/dL (threshold: {self.alert_thresholds['creatinine_high']} mg/dL)"
                )
            
            # Rapid rise alert
            if len(creatinine_data) >= 2:
                time_diff = (creatinine_data.iloc[-1]['timestamp'] - creatinine_data.iloc[-2]['timestamp']).total_seconds() / 3600
                if time_diff <= 48:  # Within 48 hours
                    creat_change = latest_creatinine - creatinine_data.iloc[-2]['value']
                    if creat_change >= self.alert_thresholds['creatinine_rapid_rise']:
                        self.create_alert(
                            patient_id=patient_id,
                            alert_type="rapid_creatinine_rise",
                            severity=AlertSeverity.CRITICAL,
                            message=f"Rapid creatinine rise: {creat_change:.2f} mg/dL in {time_diff:.1f} hours"
                        )
        
        # Check GFR alerts
        gfr_data = vitals_df[vitals_df['vital_type'] == 'gfr'].sort_values('timestamp')
        if not gfr_data.empty:
            latest_gfr = gfr_data.iloc[-1]['value']
            
            if latest_gfr < self.alert_thresholds['gfr_low']:
                severity = AlertSeverity.CRITICAL if latest_gfr < 15 else AlertSeverity.HIGH
                self.create_alert(
                    patient_id=patient_id,
                    alert_type="low_gfr",
                    severity=severity,
                    message=f"eGFR critically low: {latest_gfr} mL/min/1.73m² (threshold: {self.alert_thresholds['gfr_low']})"
                )
        
        # Check blood pressure alerts
        bp_systolic = vitals_df[vitals_df['vital_type'] == 'bp_systolic'].sort_values('timestamp')
        bp_diastolic = vitals_df[vitals_df['vital_type'] == 'bp_diastolic'].sort_values('timestamp')
        
        if not bp_systolic.empty and not bp_diastolic.empty:
            latest_sys = bp_systolic.iloc[-1]['value']
            latest_dia = bp_diastolic.iloc[-1]['value']
            
            if (latest_sys > self.alert_thresholds['blood_pressure_high'][0] or 
                latest_dia > self.alert_thresholds['blood_pressure_high'][1]):
                self.create_alert(
                    patient_id=patient_id,
                    alert_type="high_blood_pressure",
                    severity=AlertSeverity.MEDIUM,
                    message=f"Blood pressure elevated: {latest_sys}/{latest_dia} mmHg"
                )
    
    def create_alert(self, patient_id: str, alert_type: str, severity: AlertSeverity, message: str):
        """Create a new alert."""
        alert_id = f"{patient_id}_{alert_type}_{int(time.time())}"
        
        conn = sqlite3.connect(self.alerts_db)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO alerts (id, patient_id, alert_type, severity, message, timestamp)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (alert_id, patient_id, alert_type, severity.value, message, datetime.now().isoformat()))
        
        conn.commit()
        conn.close()
    
    def get_active_alerts(self, patient_id: Optional[str] = None) -> List[Dict]:
        """Get all active (unresolved) alerts."""
        conn = sqlite3.connect(self.alerts_db)
        cursor = conn.cursor()
        
        if patient_id:
            cursor.execute('''
                SELECT * FROM alerts 
                WHERE patient_id = ? AND resolved = 0
                ORDER BY timestamp DESC
            ''', (patient_id,))
        else:
            cursor.execute('''
                SELECT * FROM alerts 
                WHERE resolved = 0
                ORDER BY timestamp DESC
            ''')
        
        alerts = cursor.fetchall()
        conn.close()
        
        return [{
            'id': alert[0],
            'patient_id': alert[1],
            'alert_type': alert[2],
            'severity': alert[3],
            'message': alert[4],
            'timestamp': alert[5],
            'acknowledged': bool(alert[6]),
            'resolved': bool(alert[7])
        } for alert in alerts]
    
    def acknowledge_alert(self, alert_id: str):
        """Mark an alert as acknowledged."""
        conn = sqlite3.connect(self.alerts_db)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE alerts SET acknowledged = 1 WHERE id = ?
        ''', (alert_id,))
        
        conn.commit()
        conn.close()
    
    def resolve_alert(self, alert_id: str):
        """Mark an alert as resolved."""
        conn = sqlite3.connect(self.alerts_db)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE alerts SET resolved = 1 WHERE id = ?
        ''', (alert_id,))
        
        conn.commit()
        conn.close()
    
    def create_monitoring_dashboard(self, patient_ids: List[str]) -> go.Figure:
        """Create a real-time monitoring dashboard for multiple patients."""
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Creatinine Trends', 'eGFR Trends', 'Blood Pressure', 'Alert Summary'),
            specs=[[{"secondary_y": False}, {"secondary_y": False}],
                   [{"secondary_y": False}, {"type": "bar"}]]
        )
        
        colors = px.colors.qualitative.Set1
        
        for i, patient_id in enumerate(patient_ids[:5]):  # Limit to 5 patients for readability
            vitals_df = self.get_patient_vitals(patient_id, hours_back=168)  # 1 week
            color = colors[i % len(colors)]
            
            if not vitals_df.empty:
                # Creatinine trend
                creat_data = vitals_df[vitals_df['vital_type'] == 'creatinine']
                if not creat_data.empty:
                    fig.add_trace(
                        go.Scatter(
                            x=creat_data['timestamp'],
                            y=creat_data['value'],
                            mode='lines+markers',
                            name=f'Patient {patient_id}',
                            line=dict(color=color),
                            legendgroup=patient_id
                        ),
                        row=1, col=1
                    )
                
                # eGFR trend
                gfr_data = vitals_df[vitals_df['vital_type'] == 'gfr']
                if not gfr_data.empty:
                    fig.add_trace(
                        go.Scatter(
                            x=gfr_data['timestamp'],
                            y=gfr_data['value'],
                            mode='lines+markers',
                            name=f'Patient {patient_id}',
                            line=dict(color=color),
                            showlegend=False,
                            legendgroup=patient_id
                        ),
                        row=1, col=2
                    )
                
                # Blood pressure (latest values)
                bp_sys = vitals_df[vitals_df['vital_type'] == 'bp_systolic']
                bp_dia = vitals_df[vitals_df['vital_type'] == 'bp_diastolic']
                
                if not bp_sys.empty and not bp_dia.empty:
                    latest_sys = bp_sys.iloc[-1]['value']
                    latest_dia = bp_dia.iloc[-1]['value']
                    
                    fig.add_trace(
                        go.Scatter(
                            x=[f'Patient {patient_id}'],
                            y=[latest_sys],
                            mode='markers',
                            name='Systolic',
                            marker=dict(color='red', size=10),
                            showlegend=i==0
                        ),
                        row=2, col=1
                    )
                    
                    fig.add_trace(
                        go.Scatter(
                            x=[f'Patient {patient_id}'],
                            y=[latest_dia],
                            mode='markers',
                            name='Diastolic',
                            marker=dict(color='blue', size=10),
                            showlegend=i==0
                        ),
                        row=2, col=1
                    )
        
        # Alert summary
        alert_counts = {'Critical': 0, 'High': 0, 'Medium': 0, 'Low': 0}
        for patient_id in patient_ids:
            alerts = self.get_active_alerts(patient_id)
            for alert in alerts:
                severity = alert['severity'].title()
                if severity in alert_counts:
                    alert_counts[severity] += 1
        
        fig.add_trace(
            go.Bar(
                x=list(alert_counts.keys()),
                y=list(alert_counts.values()),
                marker_color=['red', 'orange', 'yellow', 'green']
            ),
            row=2, col=2
        )
        
        # Update layout
        fig.update_layout(
            title="Real-Time Patient Monitoring Dashboard",
            height=600,
            showlegend=True
        )
        
        # Update axes labels
        fig.update_xaxes(title_text="Time", row=1, col=1)
        fig.update_yaxes(title_text="Creatinine (mg/dL)", row=1, col=1)
        fig.update_xaxes(title_text="Time", row=1, col=2)
        fig.update_yaxes(title_text="eGFR (mL/min/1.73m²)", row=1, col=2)
        fig.update_xaxes(title_text="Patients", row=2, col=1)
        fig.update_yaxes(title_text="Blood Pressure (mmHg)", row=2, col=1)
        fig.update_xaxes(title_text="Alert Severity", row=2, col=2)
        fig.update_yaxes(title_text="Count", row=2, col=2)
        
        return fig
    
    def generate_alert_summary_report(self, days_back: int = 7) -> Dict[str, Any]:
        """Generate a summary report of alerts over the specified period."""
        conn = sqlite3.connect(self.alerts_db)
        
        cutoff_date = datetime.now() - timedelta(days=days_back)
        
        query = '''
            SELECT alert_type, severity, COUNT(*) as count
            FROM alerts 
            WHERE timestamp > ?
            GROUP BY alert_type, severity
            ORDER BY count DESC
        '''
        
        df = pd.read_sql_query(query, conn, params=(cutoff_date.isoformat(),))
        conn.close()
        
        if df.empty:
            return {
                'total_alerts': 0,
                'by_severity': {},
                'by_type': {},
                'trends': 'No alerts in the specified period'
            }
        
        # Summary statistics
        total_alerts = df['count'].sum()
        by_severity = df.groupby('severity')['count'].sum().to_dict()
        by_type = df.groupby('alert_type')['count'].sum().to_dict()
        
        # Generate insights
        most_common_alert = df.loc[df['count'].idxmax()]
        trends = f"Most common alert: {most_common_alert['alert_type']} ({most_common_alert['severity']}) with {most_common_alert['count']} occurrences"
        
        return {
            'total_alerts': total_alerts,
            'by_severity': by_severity,
            'by_type': by_type,
            'trends': trends,
            'period_days': days_back
        }
    
    def simulate_patient_data(self, patient_id: str, num_points: int = 10):
        """Simulate patient vital signs data for demonstration purposes."""
        base_time = datetime.now() - timedelta(hours=num_points)
        
        # Simulate declining kidney function
        base_creatinine = 1.2
        base_gfr = 65
        
        for i in range(num_points):
            timestamp = base_time + timedelta(hours=i)
            
            # Add some realistic variation
            creatinine = base_creatinine + (i * 0.1) + np.random.normal(0, 0.05)
            gfr = base_gfr - (i * 2) + np.random.normal(0, 2)
            bp_sys = 140 + np.random.normal(0, 10)
            bp_dia = 90 + np.random.normal(0, 5)
            
            # Add to database
            conn = sqlite3.connect(self.alerts_db)
            cursor = conn.cursor()
            
            vitals = [
                (patient_id, timestamp.isoformat(), 'creatinine', creatinine, 'mg/dL'),
                (patient_id, timestamp.isoformat(), 'gfr', gfr, 'mL/min/1.73m²'),
                (patient_id, timestamp.isoformat(), 'bp_systolic', bp_sys, 'mmHg'),
                (patient_id, timestamp.isoformat(), 'bp_diastolic', bp_dia, 'mmHg')
            ]
            
            cursor.executemany('''
                INSERT INTO patient_vitals (patient_id, timestamp, vital_type, value, unit)
                VALUES (?, ?, ?, ?, ?)
            ''', vitals)
            
            conn.commit()
            conn.close()
        
        # Check for alerts after simulation
        self.check_alerts_for_patient(patient_id)