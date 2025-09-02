#!/usr/bin/env python3
"""
Script to add missing timetable tables to existing database
"""
import sqlite3
import os

def add_timetable_tables():
    db_path = 'instance/timetabling.db'
    
    if not os.path.exists(db_path):
        print(f"Database file {db_path} does not exist!")
        return
    
    print(f"Adding timetable tables to: {db_path}")
    print("=" * 50)
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create timetable table
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS timetable (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(200) NOT NULL,
                algorithm_used VARCHAR(50) NOT NULL,
                fitness_score REAL NOT NULL,
                constraint_violations INTEGER NOT NULL,
                created_by INTEGER NOT NULL,
                FOREIGN KEY (created_by) REFERENCES userles(id)
            )
        """)
        print("✓ Created timetable table")
    except Exception as e:
        print(f"✗ Error creating timetable table: {e}")
    
    # Create timetable_entry table
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS timetable_entry (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timetable_id INTEGER NOT NULL,
                course_id INTEGER NOT NULL,
                room_id INTEGER NOT NULL,
                time_slot_id INTEGER NOT NULL,
                FOREIGN KEY (timetable_id) REFERENCES timetable(id),
                FOREIGN KEY (course_id) REFERENCES course(id),
                FOREIGN KEY (room_id) REFERENCES room(id),
                FOREIGN KEY (time_slot_id) REFERENCES time_slot(id)
            )
        """)
        print("✓ Created timetable_entry table")
    except Exception as e:
        print(f"✗ Error creating timetable_entry table: {e}")
    
    # Commit changes
    conn.commit()
    conn.close()
    
    print("\nDatabase update complete!")

if __name__ == "__main__":
    add_timetable_tables()
