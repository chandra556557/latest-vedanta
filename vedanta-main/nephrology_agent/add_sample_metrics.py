#!/usr/bin/env python3
"""
Add sample performance metrics data
"""

import sqlite3
from datetime import datetime, timedelta
import random

def add_sample_metrics():
    """Add sample performance metrics data"""
    conn = sqlite3.connect('nephro_enterprise.db')
    cursor = conn.cursor()
    
    # Check if we already have performance metrics
    cursor.execute("SELECT COUNT(*) FROM performance_metrics;")
    count = cursor.fetchone()[0]
    
    if count == 0:
        print("Adding sample performance metrics...")
        
        # Generate sample metrics for the last 7 days
        base_time = datetime.now() - timedelta(days=7)
        
        metrics_data = []
        
        for i in range(168):  # 24 hours * 7 days
            timestamp = base_time + timedelta(hours=i)
            
            # Response time metrics (in seconds)
            response_time = random.uniform(0.2, 1.5)
            metrics_data.append((
                'response_time', response_time, 'seconds', 'performance',
                timestamp.strftime('%Y-%m-%d %H:%M:%S'), '{}'
            ))
            
            # CPU usage metrics (percentage)
            if i % 4 == 0:  # Every 4 hours
                cpu_usage = random.uniform(20, 80)
                metrics_data.append((
                    'cpu_usage', cpu_usage, 'percentage', 'system',
                    timestamp.strftime('%Y-%m-%d %H:%M:%S'), '{}'
                ))
            
            # Memory usage metrics (percentage)
            if i % 6 == 0:  # Every 6 hours
                memory_usage = random.uniform(30, 70)
                metrics_data.append((
                    'memory_usage', memory_usage, 'percentage', 'system',
                    timestamp.strftime('%Y-%m-%d %H:%M:%S'), '{}'
                ))
            
            # Active users (count)
            if i % 2 == 0:  # Every 2 hours
                active_users = random.randint(5, 50)
                metrics_data.append((
                    'active_users', active_users, 'count', 'usage',
                    timestamp.strftime('%Y-%m-%d %H:%M:%S'), '{}'
                ))
        
        # Insert all metrics
        cursor.executemany("""
            INSERT INTO performance_metrics 
            (metric_name, metric_value, metric_unit, metric_category, timestamp, additional_data)
            VALUES (?, ?, ?, ?, ?, ?)
        """, metrics_data)
        
        conn.commit()
        print(f"Added {len(metrics_data)} performance metrics")
    else:
        print(f"Performance metrics already exist ({count} records)")
    
    # Also add some analytics events
    cursor.execute("SELECT COUNT(*) FROM analytics_events;")
    event_count = cursor.fetchone()[0]
    
    if event_count == 0:
        print("Adding sample analytics events...")
        
        events_data = []
        base_time = datetime.now() - timedelta(days=30)
        
        for i in range(100):  # 100 sample events
            timestamp = base_time + timedelta(hours=random.randint(0, 720))  # Random time in 30 days
            
            event_types = ['consultation_started', 'consultation_completed', 'user_login', 'report_generated']
            event_type = random.choice(event_types)
            
            events_data.append((
                1,  # user_id
                f'session_{random.randint(1000, 9999)}',  # session_id
                event_type,
                'user_interaction',  # event_category
                f'User performed {event_type}',  # description
                timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                '{}',  # event_data
                'web',  # source
                '192.168.1.100',  # ip_address
                'Mozilla/5.0',  # user_agent
                None,  # referrer
                random.randint(1, 10),  # duration_seconds
                'success',  # status
                None,  # error_message
                '{}',  # custom_properties
                timestamp.strftime('%Y-%m-%d %H:%M:%S'),  # created_at
                timestamp.strftime('%Y-%m-%d %H:%M:%S')   # updated_at
            ))
        
        cursor.executemany("""
            INSERT INTO analytics_events 
            (user_id, session_id, event_type, event_category, description, timestamp, 
             event_data, source, ip_address, user_agent, referrer, duration_seconds, 
             status, error_message, custom_properties, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, events_data)
        
        conn.commit()
        print(f"Added {len(events_data)} analytics events")
    else:
        print(f"Analytics events already exist ({event_count} records)")
    
    conn.close()
    print("Sample metrics data setup complete")

if __name__ == "__main__":
    add_sample_metrics()