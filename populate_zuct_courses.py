#!/usr/bin/env python3
"""
Script to populate the database with real courses from Zambia University College of Technology (ZUCT)
Based on official course data from their website
"""

import sqlite3
from datetime import datetime

def create_connection():
    """Create database connection"""
    try:
        conn = sqlite3.connect('timetabling.db')
        return conn
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
        return None

def clear_existing_courses(conn):
    """Clear existing course data"""
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM course")
        conn.commit()
        print("Cleared existing courses")
    except sqlite3.Error as e:
        print(f"Error clearing courses: {e}")

def populate_courses(conn):
    """Populate database with ZUCT courses"""
    
    # Bachelor of Accountancy (BAC) - 4 Year Program
    bac_courses = [
        # Year 1
        ("BAC 1200", "Principles of Economics", 3, 120, "Bachelor of Accountancy"),
        ("BAC 1300", "Mathematical Analysis", 3, 120, "Bachelor of Accountancy"),
        ("BAC 1410", "Business Communication & Academic Skills", 3, 120, "Bachelor of Accountancy"),
        ("BAC 1430", "Business Environment", 3, 120, "Bachelor of Accountancy"),
        ("BAC 1500", "Business Law", 3, 120, "Bachelor of Accountancy"),
        ("BAC 1100", "Financial Accounting", 3, 120, "Bachelor of Accountancy"),
        ("BAC 1400", "Principles of Management", 3, 120, "Bachelor of Accountancy"),
        
        # Year 2
        ("BAC 2100", "Financial Reporting", 3, 120, "Bachelor of Accountancy"),
        ("BAC 2820", "Taxation", 3, 120, "Bachelor of Accountancy"),
        ("BAC 2600", "Business Information Systems", 3, 120, "Bachelor of Accountancy"),
        ("BAC 2700", "Principles of Marketing", 3, 120, "Bachelor of Accountancy"),
        ("BAC 2900", "Cost Accounting", 3, 120, "Bachelor of Accountancy"),
        ("BAC 2500", "Company Law", 3, 120, "Bachelor of Accountancy"),
        ("BAC 2300", "Decision Making Techniques", 3, 120, "Bachelor of Accountancy"),
        
        # Year 3
        ("BAC 3000", "Research Methods", 3, 120, "Bachelor of Accountancy"),
        ("BAC 3100", "Advanced Financial Reporting", 3, 120, "Bachelor of Accountancy"),
        ("BAC 3200", "Auditing", 3, 120, "Bachelor of Accountancy"),
        ("BAC 3600", "Corporate Governance & Business Ethics", 3, 120, "Bachelor of Accountancy"),
        ("BAC 3800", "Financial Management", 3, 120, "Bachelor of Accountancy"),
        ("BAC 3820", "Advanced Taxation", 3, 120, "Bachelor of Accountancy"),
        ("BAC 3900", "Management Accounting", 3, 120, "Bachelor of Accountancy"),
        
        # Year 4
        ("BAC 4000", "Dissertation/Research Project", 6, 180, "Bachelor of Accountancy"),
        ("BAC 4200", "Advanced Audit & Assurance", 3, 120, "Bachelor of Accountancy"),
        ("BAC 4400", "Strategic Management", 3, 120, "Bachelor of Accountancy"),
        ("BAC 4600", "Entrepreneurship & Development", 3, 120, "Bachelor of Accountancy"),
        ("BAC 4800", "Advanced Financial Management", 3, 120, "Bachelor of Accountancy"),
        ("BAC 4490", "Advanced Management Accounting", 3, 120, "Bachelor of Accountancy"),
    ]
    
    # Bachelor of Engineering in Telecommunications and Electronics (ETE) - 5 Year Program
    ete_courses = [
        # Year 1
        ("MAT 1010", "Mathematics", 3, 120, "Engineering in Telecommunications and Electronics"),
        ("PHY 1010", "Applied Physics", 3, 120, "Engineering in Telecommunications and Electronics"),
        ("MEC 1012", "Engineering Graphics and CAD", 3, 120, "Engineering in Telecommunications and Electronics"),
        ("MEC 1013", "Engineering Workshop Practice", 3, 120, "Engineering in Telecommunications and Electronics"),
        ("EEE 1030", "Introduction to Electrical Engineering", 3, 120, "Engineering in Telecommunications and Electronics"),
        ("CMS 1011", "Communication Skills", 3, 120, "Engineering in Telecommunications and Electronics"),
        ("ICT 1011", "Introduction to Information Technology", 3, 120, "Engineering in Telecommunications and Electronics"),
        
        # Year 2
        ("EEE 2040", "Analog Electronics", 3, 120, "Engineering in Telecommunications and Electronics"),
        ("ICT 2010", "Introduction to Programming", 3, 120, "Engineering in Telecommunications and Electronics"),
        ("EMA 2010", "Engineering Mathematics I", 3, 120, "Engineering in Telecommunications and Electronics"),
        ("EEE 2021", "Electrical Circuits", 3, 120, "Engineering in Telecommunications and Electronics"),
        ("EEE 2011", "Electrical Measurements and Instrumentation", 3, 120, "Engineering in Telecommunications and Electronics"),
        ("ETE 2013", "Analogue Communications and Antenna Theory", 3, 120, "Engineering in Telecommunications and Electronics"),
        
        # Year 3
        ("ETE 3020", "Digital Communication Systems", 3, 120, "Engineering in Telecommunications and Electronics"),
        ("EEE 3030", "Digital Electronics and Logic Design", 3, 120, "Engineering in Telecommunications and Electronics"),
        ("ETE 3050", "Digital Signal Processing", 3, 120, "Engineering in Telecommunications and Electronics"),
        ("EEE 3041", "Microprocessors, Microcontrollers and Embedded Systems", 3, 120, "Engineering in Telecommunications and Electronics"),
        ("EMA 3010", "Engineering Mathematics II", 3, 120, "Engineering in Telecommunications and Electronics"),
        ("ETE 3081", "Communication Systems Design", 3, 120, "Engineering in Telecommunications and Electronics"),
        ("EEE 3021", "Control Systems Engineering", 3, 120, "Engineering in Telecommunications and Electronics"),
        
        # Year 4
        ("ETE 4020", "Switching Systems and Computer Networks", 3, 120, "Engineering in Telecommunications and Electronics"),
        ("ETE 4050", "Optical Transmission Networks", 3, 120, "Engineering in Telecommunications and Electronics"),
        ("ETE 4030", "Wireless Adhoc and Sensor Networks", 3, 120, "Engineering in Telecommunications and Electronics"),
        ("ETE 4051", "Cryptography and Network Security", 3, 120, "Engineering in Telecommunications and Electronics"),
        ("EMA 4021", "Numerical Computation", 3, 120, "Engineering in Telecommunications and Electronics"),
        ("EEE 4020", "Electro-Magnetic Field Theory", 3, 120, "Engineering in Telecommunications and Electronics"),
        ("ETE 4031", "Industrial Training", 6, 240, "Engineering in Telecommunications and Electronics"),
        ("ETE 4040", "Unified Communications & Video Conferencing", 3, 120, "Engineering in Telecommunications and Electronics"),
        ("EEE 4071", "Robotics Engineering", 3, 120, "Engineering in Telecommunications and Electronics"),
        ("BME 4061", "Biomedical Instrumentation", 3, 120, "Engineering in Telecommunications and Electronics"),
        
        # Year 5
        ("MGT 5050", "Business Management and Entrepreneurship", 3, 120, "Engineering in Telecommunications and Electronics"),
        ("ETE 5010", "Television and Video Engineering", 3, 120, "Engineering in Telecommunications and Electronics"),
        ("ETE 5020", "Satellite and Microwave Engineering", 3, 120, "Engineering in Telecommunications and Electronics"),
        ("ETE 5030", "Mobile Broadband Communications", 3, 120, "Engineering in Telecommunications and Electronics"),
        ("ETE 5000", "Final Year Project", 6, 180, "Engineering in Telecommunications and Electronics"),
        ("ICT 5051", "Cyber Security for Automation, Control & SCADA Systems", 3, 120, "Engineering in Telecommunications and Electronics"),
        ("EE 5081", "RF Network Design", 3, 120, "Engineering in Telecommunications and Electronics"),
        ("EEE 5031", "Mobile Application Development", 3, 120, "Engineering in Telecommunications and Electronics"),
    ]
    
    # Bachelor of Engineering in Electrical and Electronics (BEE) - 5 Year Program
    bee_courses = [
        # Year 1 (same as ETE)
        ("MAT 1010", "Mathematics", 3, 120, "Engineering in Electrical and Electronics"),
        ("PHY 1010", "Applied Physics", 3, 120, "Engineering in Electrical and Electronics"),
        ("MEC 1012", "Engineering Graphics and CAD", 3, 120, "Engineering in Electrical and Electronics"),
        ("MEC 1013", "Engineering Workshop Practice", 3, 120, "Engineering in Electrical and Electronics"),
        ("EEE 1030", "Introduction to Electrical Engineering", 3, 120, "Engineering in Electrical and Electronics"),
        ("CMS 1011", "Communication Skills", 3, 120, "Engineering in Electrical and Electronics"),
        ("ICT 1011", "Introduction to Information Technology", 3, 120, "Engineering in Electrical and Electronics"),
        
        # Year 2
        ("EEE 2040", "Analog Electronics", 3, 120, "Engineering in Electrical and Electronics"),
        ("ICT 2010", "Introduction to Programming", 3, 120, "Engineering in Electrical and Electronics"),
        ("EMA 2010", "Engineering Mathematics I", 3, 120, "Engineering in Electrical and Electronics"),
        ("EEE 2021", "Electrical Circuits", 3, 120, "Engineering in Electrical and Electronics"),
        ("EEE 2011", "Electrical Measurements and Instrumentation", 3, 120, "Engineering in Electrical and Electronics"),
        ("MEC 2013", "Applied Mechanics and Strength of Materials", 3, 120, "Engineering in Electrical and Electronics"),
        
        # Year 3
        ("EEE 3060", "Machines I", 3, 120, "Engineering in Electrical and Electronics"),
        ("EEE 3030", "Digital Electronics and Logic Design", 3, 120, "Engineering in Electrical and Electronics"),
        ("EEE 3031", "Renewable Energy Systems", 3, 120, "Engineering in Electrical and Electronics"),
        ("EEE 3041", "Microprocessors, Microcontrollers and Embedded Systems", 3, 120, "Engineering in Electrical and Electronics"),
        ("EMA 3010", "Engineering Mathematics II", 3, 120, "Engineering in Electrical and Electronics"),
        ("EEE 3081", "Electrical Engineering Design and CAM", 3, 120, "Engineering in Electrical and Electronics"),
        ("EEE 3021", "Control Systems Engineering", 3, 120, "Engineering in Electrical and Electronics"),
        
        # Year 4
        ("EEE 4060", "Electrical Machines II", 3, 120, "Engineering in Electrical and Electronics"),
        ("EEE 4030", "Power Systems Engineering I", 3, 120, "Engineering in Electrical and Electronics"),
        ("EEE 4040", "Power Electronics", 3, 120, "Engineering in Electrical and Electronics"),
        ("EEE 4081", "Energy Management and Energy Audit", 3, 120, "Engineering in Electrical and Electronics"),
        ("EEE 4010", "Protection Engineering", 3, 120, "Engineering in Electrical and Electronics"),
        ("EMA 4021", "Numerical Computation", 3, 120, "Engineering in Electrical and Electronics"),
        ("EEE 4020", "Electro-Magnetic Field Theory", 3, 120, "Engineering in Electrical and Electronics"),
        ("BME 4061", "Biomedical Instrumentation", 3, 120, "Engineering in Electrical and Electronics"),
        ("EEE 4071", "Robotics Engineering", 3, 120, "Engineering in Electrical and Electronics"),
        
        # Year 5
        ("MGT 5050", "Business Management and Entrepreneurship", 3, 120, "Engineering in Electrical and Electronics"),
        ("EEE 5091", "Smart Grid Technology", 3, 120, "Engineering in Electrical and Electronics"),
        ("EEE 5080", "Power Systems Engineering II", 3, 120, "Engineering in Electrical and Electronics"),
        ("EEE 5090", "Electric Drives", 3, 120, "Engineering in Electrical and Electronics"),
        ("EEE 5071", "Industrial Automation and SCADA Systems", 3, 120, "Engineering in Electrical and Electronics"),
        ("EEE 5000", "Final Year Project", 6, 180, "Engineering in Electrical and Electronics"),
        ("EEE 5081", "Power Plant Engineering", 3, 120, "Engineering in Electrical and Electronics"),
        ("ICT 5051", "Cyber Security for Automation, Control & SCADA Systems", 3, 120, "Engineering in Electrical and Electronics"),
        ("EEE 4031", "Industrial Training", 6, 240, "Engineering in Electrical and Electronics"),
    ]
    
    # Bachelor of Cyber Security (BSEC) - 4 Year Program
    bsec_courses = [
        # Year 1
        ("SEC 1101", "Introduction to Security Fundamentals", 3, 120, "Cyber Security"),
        ("BIT 1100", "Introduction to IT", 3, 120, "Cyber Security"),
        ("ICT 1110", "Introduction to Programming", 3, 120, "Cyber Security"),
        ("BIT 1111", "Communication and Technical Writing", 3, 120, "Cyber Security"),
        ("BIT 1120", "Mathematics", 3, 120, "Cyber Security"),
        ("BIT 1160", "Introduction to Systems Analysis and Design", 3, 120, "Cyber Security"),
        ("ICT 1100", "Introduction to Information Technology", 3, 120, "Cyber Security"),
        ("BIT 1131", "Fundamentals of Electrical and Electronics", 3, 120, "Cyber Security"),
        ("BIT 1140", "Introduction to Data Communications and Networks", 3, 120, "Cyber Security"),
        
        # Year 2
        ("SEC 2200", "System Programming and Computer Control", 3, 120, "Cyber Security"),
        ("SEC 2201", "Biometrics 1", 3, 120, "Cyber Security"),
        ("SEC 2202", "Cryptography", 3, 120, "Cyber Security"),
        ("SEC 2203", "Forensic Tools & Techniques", 3, 120, "Cyber Security"),
        ("SEC 2204", "Operating Systems Concepts", 3, 120, "Cyber Security"),
        ("BIT 2260", "Database Systems", 3, 120, "Cyber Security"),
        ("BIT 2220", "Computer Architecture and Organization", 3, 120, "Cyber Security"),
        ("BSE 2210", "Software Design", 3, 120, "Cyber Security"),
        
        # Year 3
        ("SEC 3301", "Network Security and Firewalls", 3, 120, "Cyber Security"),
        ("SEC 3302", "Computer Systems Security", 3, 120, "Cyber Security"),
        ("SEC 3303", "Biometrics 2", 3, 120, "Cyber Security"),
        ("SEC 3304", "Data Recovery Techniques and Evidence Gathering", 3, 120, "Cyber Security"),
        ("BIT 3300", "Object-Oriented Programming", 3, 120, "Cyber Security"),
        ("BIT 3360", "Advanced Database Systems", 3, 120, "Cyber Security"),
        
        # Year 4
        ("SEC 4400", "Digital Forensics and Incident Response", 3, 120, "Cyber Security"),
        ("SEC 4401", "Hacking, Countermeasures and Techniques", 3, 120, "Cyber Security"),
        ("SEC 4402", "Risk Management and Information Assurance", 3, 120, "Cyber Security"),
        ("SEC 4403", "Ethics and Cyber Law", 3, 120, "Cyber Security"),
        ("SEC 4404", "Final Year Project", 6, 180, "Cyber Security"),
    ]
    
    # Bachelor of Software Engineering (BSE) - 4 Year Program
    bse_courses = [
        # Year 1
        ("BSE 1010", "Software Requirements Engineering", 3, 120, "Software Engineering"),
        ("BIT 1100", "Introduction to IT", 3, 120, "Software Engineering"),
        ("ICT 1110", "Introduction to Programming", 3, 120, "Software Engineering"),
        ("BIT 1120", "Mathematics", 3, 120, "Software Engineering"),
        ("BIT 1111", "Communication and Technical Writing", 3, 120, "Software Engineering"),
        ("ICT 1100", "Introduction to Information Technology", 3, 120, "Software Engineering"),
        ("BIT 1140", "Introduction to Data Communications and Networks", 3, 120, "Software Engineering"),
        
        # Year 2
        ("BIT 2260", "Database Systems", 3, 120, "Software Engineering"),
        ("BSE 2201", "Software Engineering Foundations", 3, 120, "Software Engineering"),
        ("BIT 2240", "Fundamentals of Multimedia", 3, 120, "Software Engineering"),
        ("BSE 2210", "Software Design", 3, 120, "Software Engineering"),
        ("SEC 2204", "Operating Systems Concepts", 3, 120, "Software Engineering"),
        ("BIT 2250", "Fundamentals of Data Structures and Algorithms", 3, 120, "Software Engineering"),
        ("BIT 2230", "Web Design and Development", 3, 120, "Software Engineering"),
        
        # Year 3
        ("BIT 3300", "Object-Oriented Programming", 3, 120, "Software Engineering"),
        ("BSE 3310", "Software Testing", 3, 120, "Software Engineering"),
        ("BSE 3350", "Full Stack Web Development", 3, 120, "Software Engineering"),
        ("BSE 3010", "Software Engineering Management", 3, 120, "Software Engineering"),
        ("BSE 3340", "Mobile Application Development", 3, 120, "Software Engineering"),
        ("BIT 3360", "Advanced Database Systems", 3, 120, "Software Engineering"),
        
        # Year 4
        ("BIT 4421", "Entrepreneurship", 3, 120, "Software Engineering"),
        ("BSE 4040", "Designing & Developing Applications for the cloud", 3, 120, "Software Engineering"),
        ("BSE 4020", "Software Quality Engineering", 3, 120, "Software Engineering"),
        ("BSE 4050", "Distributed Computer Systems", 3, 120, "Software Engineering"),
        ("BSE 4400", "Final Year Software Engineering Project", 6, 180, "Software Engineering"),
    ]
    
    # Bachelor of Procurement and Supply (BPS) - 4 Year Program
    bps_courses = [
        # Year 1
        ("BPS 1100", "Financial Accounting", 3, 120, "Procurement and Supply"),
        ("BPS 1200", "Principles of Economics", 3, 120, "Procurement and Supply"),
        ("BPS 1300", "Mathematical Analysis", 3, 120, "Procurement and Supply"),
        ("BPS 1400", "Principles of Management", 3, 120, "Procurement and Supply"),
        ("BPS 1430", "Purchasing & Business Environment", 3, 120, "Procurement and Supply"),
        ("BPS 1500", "Business Law", 3, 120, "Procurement and Supply"),
        ("BPS 1410", "Business Communication", 3, 120, "Procurement and Supply"),
        ("BPS 1000", "Financial Accounting", 3, 120, "Procurement and Supply"),
        ("BPS 1600", "Principles of Procurement and Supply", 3, 120, "Procurement and Supply"),
        
        # Year 2
        ("BPS 2110", "Purchasing & Supply Administration", 3, 120, "Procurement and Supply"),
        ("BPS 2220", "Negotiating and Contract Management", 3, 120, "Procurement and Supply"),
        ("BPS 2300", "Business Statistics", 3, 120, "Procurement and Supply"),
        ("BPS 2410", "Sourcing in Procurement & Supply", 3, 120, "Procurement and Supply"),
        ("BPS 2600", "Business Information Systems", 3, 120, "Procurement and Supply"),
    ]
    
    # Combine all courses
    all_courses = bac_courses + ete_courses + bee_courses + bsec_courses + bse_courses + bps_courses
    
    try:
        cursor = conn.cursor()
        
        # Insert courses
        insert_query = """
        INSERT INTO course (code, name, duration, students, program) 
        VALUES (?, ?, ?, ?, ?)
        """
        
        cursor.executemany(insert_query, all_courses)
        conn.commit()
        
        print(f"Successfully inserted {len(all_courses)} ZUCT courses")
        print("\nPrograms added:")
        programs = set([course[4] for course in all_courses])
        for program in sorted(programs):
            count = len([c for c in all_courses if c[4] == program])
            print(f"  - {program}: {count} courses")
            
    except sqlite3.Error as e:
        print(f"Error inserting courses: {e}")

def main():
    """Main function"""
    print("Populating ZUCT Courses Database...")
    print("=" * 50)
    
    conn = create_connection()
    if conn is None:
        return
    
    try:
        # Clear existing courses
        clear_existing_courses(conn)
        
        # Populate with ZUCT courses
        populate_courses(conn)
        
        print("\n✅ Database populated successfully with ZUCT courses!")
        print("\nTo view the courses, run your Flask application and go to the Courses page.")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    main()
