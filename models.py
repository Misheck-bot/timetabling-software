from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

# Import db from app.py to avoid circular imports
from app import db

class User(UserMixin, db.Model):
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
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

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
    
    # Relationships
    exams = db.relationship('Exam', backref='course', lazy=True)

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
    
    # Relationships
    exams = db.relationship('Exam', backref='room', lazy=True)

class TimeSlot(db.Model):
    """Time slot model for scheduling"""
    __tablename__ = 'time_slot'
    id = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.String(20), nullable=False)  # Monday, Tuesday, etc.
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    slot_type = db.Column(db.String(20), default='Regular')  # Regular, Break, Special
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    exams = db.relationship('Exam', backref='time_slot', lazy=True)
    
    def __repr__(self):
        return f'<TimeSlot {self.day} {self.start_time}-{self.end_time}>'

class Exam(db.Model):
    """Exam model representing scheduled examinations"""
    __tablename__ = 'exam'
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'), nullable=False)
    time_slot_id = db.Column(db.Integer, db.ForeignKey('time_slot.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    duration = db.Column(db.Integer, default=120)  # in minutes
    invigilators = db.Column(db.Text)  # JSON string of invigilator IDs
    status = db.Column(db.String(20), default='Scheduled')  # Scheduled, Completed, Cancelled
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

class Timetable(db.Model):
    """Timetable model for storing generated schedules"""
    __tablename__ = 'timetable'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), default='Generated Timetable')
    data = db.Column(db.Text, nullable=False)  # JSON string of timetable data
    fitness_score = db.Column(db.Float, default=0.0)
    algorithm_used = db.Column(db.String(50), nullable=False)
    parameters = db.Column(db.Text)  # JSON string of algorithm parameters
    status = db.Column(db.String(20), default='Generated')  # Generated, Approved, Implemented
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    creator = db.relationship('User', backref='timetables')

class Student(db.Model):
    """Student model for tracking enrollments"""
    __tablename__ = 'student'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    department = db.Column(db.String(100), default='IT')
    year_level = db.Column(db.Integer, default=1)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class StudentCourse(db.Model):
    """Many-to-many relationship between students and courses"""
    __tablename__ = 'student_course'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    semester = db.Column(db.String(20), default='Fall')
    academic_year = db.Column(db.String(10), default='2024')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    student = db.relationship('Student', backref='enrollments')
    course = db.relationship('Course', backref='enrollments')

class Faculty(db.Model):
    """Faculty model for staff management"""
    __tablename__ = 'faculty'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    department = db.Column(db.String(100), default='IT')
    role = db.Column(db.String(50), default='Lecturer')
    availability = db.Column(db.Text)  # JSON string of availability schedule
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
