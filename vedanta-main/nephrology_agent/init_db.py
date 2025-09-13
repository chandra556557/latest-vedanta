#!/usr/bin/env python3
"""
Database initialization script for Nephrology AI Agent
"""

import sqlite3
import os

def init_database():
    """Initialize the database with required tables"""
    db_path = 'nephro_enterprise.db'
    schema_path = 'database_schema.sql'
    
    # Check if database exists
    db_exists = os.path.exists(db_path)
    print(f"Database exists: {db_exists}")
    
    # Connect to database (creates if doesn't exist)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Check if consultations table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='consultations';")
    result = cursor.fetchone()
    
    if result:
        print("Consultations table exists")
        # Check table structure
        cursor.execute("PRAGMA table_info(consultations);")
        columns = cursor.fetchall()
        print(f"Consultations table has {len(columns)} columns")
        for col in columns:
            print(f"  - {col[1]} ({col[2]})")
    else:
        print("Consultations table missing - initializing database")
        
        # Read and execute schema
        if os.path.exists(schema_path):
            with open(schema_path, 'r', encoding='utf-8') as f:
                schema_sql = f.read()
            
            # Execute schema in chunks
            statements = schema_sql.split(';')
            for statement in statements:
                statement = statement.strip()
                if statement:
                    try:
                        cursor.execute(statement)
                        print(f"Executed: {statement[:50]}...")
                    except Exception as e:
                        print(f"Error executing statement: {e}")
                        print(f"Statement: {statement[:100]}...")
            
            conn.commit()
            print("Database schema initialized successfully")
        else:
            print(f"Schema file {schema_path} not found")
    
    # Insert some sample data if tables are empty
    cursor.execute("SELECT COUNT(*) FROM consultations;")
    count = cursor.fetchone()[0]
    
    if count == 0:
        print("Adding sample consultation data")
        sample_consultations = [
            (1, 'session_001', 'Initial CKD Assessment', 'Routine checkup for kidney function', 'general', 'completed', 'normal', '2024-01-15 10:00:00', '2024-01-15 10:30:00', '2024-01-15 10:30:00', 30, 5, 'Very helpful consultation', 'Stage 3 CKD', 'Continue current medications, follow-up in 3 months', 1, '2024-04-15', None),
            (1, 'session_002', 'Follow-up Visit', 'Checking progress on treatment plan', 'follow_up', 'completed', 'normal', '2024-01-20 14:00:00', '2024-01-20 14:25:00', '2024-01-20 14:25:00', 25, 4, 'Good follow-up', 'Stable CKD', 'Continue monitoring', 0, None, None),
            (1, 'session_003', 'Medication Review', 'Reviewing current medications and side effects', 'general', 'completed', 'normal', '2024-01-25 09:00:00', '2024-01-25 09:20:00', '2024-01-25 09:20:00', 20, 5, 'Excellent service', 'No issues', 'Adjust dosage as discussed', 0, None, None)
        ]
        
        # First ensure we have a user
        cursor.execute("SELECT COUNT(*) FROM users;")
        user_count = cursor.fetchone()[0]
        
        if user_count == 0:
            cursor.execute("""
                INSERT INTO users (username, email, password_hash, full_name, role, is_active)
                VALUES ('demo_user', 'demo@example.com', 'hashed_password', 'Demo User', 'patient', 1)
            """)
            conn.commit()
            print("Added demo user")
        
        # Insert sample consultations
        for consultation in sample_consultations:
            cursor.execute("""
                INSERT INTO consultations 
                (user_id, session_id, title, chief_complaint, consultation_type, status, priority, 
                 created_at, updated_at, completed_at, duration_minutes, satisfaction_rating, 
                 feedback, diagnosis_summary, recommendations, follow_up_required, follow_up_date, assigned_doctor_id)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, consultation)
        
        conn.commit()
        print(f"Added {len(sample_consultations)} sample consultations")
    
    conn.close()
    print("Database initialization complete")

if __name__ == "__main__":
    init_database()