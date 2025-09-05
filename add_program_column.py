#!/usr/bin/env python3
"""
Database migration script to add 'program' column to Course table
and update existing courses with program information.
"""

import sqlite3
import os

def add_program_column():
    """Add program column to Course table and update existing data"""
    
    # Database path
    db_path = 'timetabling.db'
    
    if not os.path.exists(db_path):
        print(f"Database {db_path} not found. Please ensure the database exists.")
        return
    
    try:
        # Connect to database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if program column already exists
        cursor.execute("PRAGMA table_info(course)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'program' in columns:
            print("Program column already exists in Course table.")
        else:
            # Add program column
            cursor.execute("ALTER TABLE course ADD COLUMN program VARCHAR(200) DEFAULT 'General'")
            print("Added 'program' column to Course table.")
        
        # Update existing courses with program information based on department
        # Map departments to programs
        department_to_program = {
            'IT': 'Software Engineering',
            'CS': 'Software Engineering', 
            'SE': 'Software Engineering',
            'CE': 'Engineering in Electrical and Electronics',
            'EE': 'Engineering in Electrical and Electronics',
            'TE': 'Engineering in Telecommunications and Electronics',
            'CYB': 'Cyber Security',
            'ACC': 'Bachelor of Accountancy',
            'PROC': 'Procurement and Supply'
        }
        
        # Update courses based on department mapping
        for dept, program in department_to_program.items():
            cursor.execute(
                "UPDATE course SET program = ? WHERE department = ? AND (program IS NULL OR program = 'General')",
                (program, dept)
            )
            updated = cursor.rowcount
            if updated > 0:
                print(f"Updated {updated} courses from department '{dept}' to program '{program}'")
        
        # Update any remaining courses with 'General' department to a default program
        cursor.execute(
            "UPDATE course SET program = 'General Studies' WHERE department = 'General' AND (program IS NULL OR program = 'General')"
        )
        
        # Commit changes
        conn.commit()
        
        # Verify the changes
        cursor.execute("SELECT COUNT(*) FROM course WHERE program IS NOT NULL AND program != 'General'")
        updated_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM course")
        total_count = cursor.fetchone()[0]
        
        print(f"\nMigration completed successfully!")
        print(f"Total courses: {total_count}")
        print(f"Courses with program assigned: {updated_count}")
        
        # Show program distribution
        cursor.execute("SELECT program, COUNT(*) FROM course GROUP BY program ORDER BY COUNT(*) DESC")
        programs = cursor.fetchall()
        
        print("\nProgram distribution:")
        for program, count in programs:
            print(f"  {program}: {count} courses")
        
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    add_program_column()
