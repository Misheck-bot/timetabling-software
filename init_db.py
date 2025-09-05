#!/usr/bin/env python3
"""
Database initialization script for the Examination Timetabling System.
This script creates the database tables and populates them with sample data.
"""

import os
import sys
from datetime import time, datetime

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash

# Create a minimal Flask app for database operations
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///timetabling.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define models locally to avoid circular imports
class User(db.Model):
    """User model for authentication and role management"""
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default='user')  # admin, user
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # OAuth fields
    oauth_provider = db.Column(db.String(50), nullable=True)  # google, facebook, github, microsoft
    oauth_provider_id = db.Column(db.String(100), nullable=True)
    full_name = db.Column(db.String(200), nullable=True)
    avatar_url = db.Column(db.String(500), nullable=True)
    
    # OAuth provider unique constraint
    __table_args__ = (
        db.UniqueConstraint('oauth_provider', 'oauth_provider_id', name='uq_oauth_provider_id'),
    )

class Course(db.Model):
    """Course model representing academic courses"""
    __tablename__ = 'course'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    code = db.Column(db.String(20), unique=True, nullable=False)
    students = db.Column(db.Integer, default=0)
    duration = db.Column(db.Integer, default=120)  # in minutes
    department = db.Column(db.String(100), default='IT')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Room(db.Model):
    """Room model for examination venues"""
    __tablename__ = 'room'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    building = db.Column(db.String(100), default='Main Building')
    room_type = db.Column(db.String(50), default='Classroom')  # Classroom, Lab, Auditorium
    facilities = db.Column(db.Text)  # JSON string of available facilities
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class TimeSlot(db.Model):
    """Time slot model for scheduling"""
    __tablename__ = 'time_slot'
    id = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.String(20), nullable=False)  # Monday, Tuesday, etc.
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    slot_type = db.Column(db.String(20), default='Regular')  # Regular, Break, Special
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Constraint(db.Model):
    """Constraint model for scheduling rules"""
    __tablename__ = 'constraint'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    constraint_type = db.Column(db.String(50), nullable=False)  # hard, soft
    description = db.Column(db.Text, nullable=False)
    parameters = db.Column(db.Text)  # JSON string of constraint parameters
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

def init_database():
    """Initialize the database with tables and admin user only"""
    with app.app_context():
        # Create all tables
        print("Creating database tables...")
        db.create_all()
        
        # Check if admin user already exists
        if User.query.filter_by(role='admin').first():
            print("Admin user already exists. Skipping initialization.")
            return
        
        print("Creating admin user...")
        
        # Database initialized with empty tables
        print("Database initialized successfully!")
        print("\nPlease create an admin account by signing up through the web interface.")
        print("The first user to register will need to be manually set as admin in the database.")

def reset_database():
    """Reset the database and recreate empty tables"""
    print("Resetting database...")
    
    # Drop all tables
    db.drop_all()
    
    # Recreate tables
    db.create_all()
    
    print("Database reset complete! All tables are now empty.")

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == '--reset':
        reset_database()
    init_database()
