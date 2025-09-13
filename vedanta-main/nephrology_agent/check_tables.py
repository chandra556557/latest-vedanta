#!/usr/bin/env python3
"""
Check available tables in the database
"""

import sqlite3

def check_tables():
    """Check what tables exist in the database"""
    conn = sqlite3.connect('nephro_enterprise.db')
    cursor = conn.cursor()
    
    # Get all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    print("Available tables:")
    for table in tables:
        print(f"  - {table[0]}")
        
        # Get column info for each table
        cursor.execute(f"PRAGMA table_info({table[0]});")
        columns = cursor.fetchall()
        print(f"    Columns: {len(columns)}")
        for col in columns[:5]:  # Show first 5 columns
            print(f"      - {col[1]} ({col[2]})")
        if len(columns) > 5:
            print(f"      ... and {len(columns) - 5} more columns")
        print()
    
    conn.close()

if __name__ == "__main__":
    check_tables()