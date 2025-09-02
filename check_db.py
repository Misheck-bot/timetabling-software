#!/usr/bin/env python3
"""
Script to check the actual database structure
"""
import sqlite3
import os

def check_database():
    db_path = 'instance/timetabling.db'
    
    if not os.path.exists(db_path):
        print(f"Database file {db_path} does not exist!")
        return
    
    print(f"Checking database: {db_path}")
    print("=" * 50)
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Get all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    print(f"Found {len(tables)} tables:")
    for table in tables:
        table_name = table[0]
        print(f"\nTable: {table_name}")
        print("-" * 30)
        
        # Get table schema
        cursor.execute(f"PRAGMA table_info({table_name});")
        columns = cursor.fetchall()
        
        for col in columns:
            col_id, col_name, col_type, not_null, default_val, pk = col
            print(f"  {col_name}: {col_type} {'NOT NULL' if not_null else 'NULL'} {'PK' if pk else ''}")
    
    conn.close()

if __name__ == "__main__":
    check_database()
