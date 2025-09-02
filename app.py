from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import os
from datetime import datetime, timedelta
import json
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Import models after db initialization
from models import User, Course, Room, TimeSlot, Exam, Constraint, Timetable

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def home():
    """Home page with attractive design and project overview"""
    return render_template('home.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        # Check if passwords match
        if password != confirm_password:
            flash('Passwords do not match!')
            return render_template('signup.html')
        
        # Check if user already exists
        if User.query.filter_by(email=email).first():
            flash('Email already registered!')
            return render_template('signup.html')
        
        if User.query.filter_by(username=username).first():
            flash('Username already taken!')
            return render_template('signup.html')
        
        # Create new user
        new_user = User(
            username=username,
            email=email,
            password_hash=generate_password_hash(password),
            role='user'  # Default role for new users
        )
        
        db.session.add(new_user)
        db.session.commit()
        
        flash('Account created successfully! Please login.')
        return redirect(url_for('login'))
    
    return render_template('signup.html')

# OAuth Routes
@app.route('/oauth/<provider>/login')
def oauth_login(provider):
    """Redirect to OAuth provider for authentication"""
    if provider not in ['google', 'facebook', 'github', 'microsoft']:
        flash('Unsupported OAuth provider')
        return redirect(url_for('login'))
    
    try:
        from oauth_auth import OAuthProvider
        oauth = OAuthProvider(provider)
        auth_url = oauth.get_authorization_url()
        return redirect(auth_url)
    except Exception as e:
        flash(f'Error initiating {provider} authentication: {str(e)}')
        return redirect(url_for('login'))

@app.route('/oauth/<provider>/callback')
def oauth_callback(provider):
    """Handle OAuth callback from provider"""
    if provider not in ['google', 'facebook', 'github', 'microsoft']:
        flash('Unsupported OAuth provider')
        return redirect(url_for('login'))
    
    try:
        from oauth_auth import OAuthProvider, get_or_create_user
        code = request.args.get('code')
        if not code:
            flash('Authorization code not received')
            return redirect(url_for('login'))
        
        oauth = OAuthProvider(provider)
        oauth_data = oauth.handle_callback(code)
        
        if not oauth_data:
            flash(f'Failed to authenticate with {provider}')
            return redirect(url_for('login'))
        
        # Get or create user
        user = get_or_create_user(oauth_data)
        
        # Log in the user
        login_user(user)
        flash(f'Successfully signed in with {provider}!')
        return redirect(url_for('dashboard'))
        
    except Exception as e:
        flash(f'Error during {provider} authentication: {str(e)}')
        return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/dashboard')
@login_required
def dashboard():
    """Main dashboard for timetabling operations"""
    courses = Course.query.all()
    rooms = Room.query.all()
    time_slots = TimeSlot.query.all()
    constraints = Constraint.query.all()
    
    return render_template('dashboard.html', 
                         courses=courses, 
                         rooms=rooms, 
                         time_slots=time_slots,
                         constraints=constraints)

@app.route('/courses', methods=['GET', 'POST'])
@login_required
def manage_courses():
    """Manage courses and their properties"""
    if request.method == 'POST':
        name = request.form.get('name')
        code = request.form.get('code')
        students = int(request.form.get('students', 0))
        duration = int(request.form.get('duration', 120))
        
        course = Course(name=name, code=code, students=students, duration=duration)
        db.session.add(course)
        db.session.commit()
        flash('Course added successfully!')
        return redirect(url_for('manage_courses'))
    
    courses = Course.query.all()
    return render_template('courses.html', courses=courses)

@app.route('/rooms', methods=['GET', 'POST'])
@login_required
def manage_rooms():
    """Manage rooms and their capacities"""
    if request.method == 'POST':
        name = request.form.get('name')
        capacity = int(request.form.get('capacity', 0))
        building = request.form.get('building', '')
        
        room = Room(name=name, capacity=capacity, building=building)
        db.session.add(room)
        db.session.commit()
        flash('Room added successfully!')
        return redirect(url_for('manage_rooms'))
    
    rooms = Room.query.all()
    return render_template('rooms.html', rooms=rooms)

@app.route('/constraints', methods=['GET', 'POST'])
@login_required
def manage_constraints():
    """Manage scheduling constraints"""
    if request.method == 'POST':
        name = request.form.get('name')
        constraint_type = request.form.get('constraint_type')
        description = request.form.get('description')
        parameters = request.form.get('parameters', '{}')
        
        constraint = Constraint(
            name=name,
            constraint_type=constraint_type, 
            description=description, 
            parameters=parameters
        )
        db.session.add(constraint)
        db.session.commit()
        flash('Constraint added successfully!')
        return redirect(url_for('manage_constraints'))
    
    constraints = Constraint.query.all()
    return render_template('constraints.html', constraints=constraints)

@app.route('/optimize', methods=['POST'])
@login_required
def optimize_timetable():
    """Run the optimization algorithms"""
    try:
        # Get parameters from request
        algorithm = request.form.get('algorithm', 'hybrid')
        population_size = int(request.form.get('population_size', 50))
        generations = int(request.form.get('generations', 100))
        mutation_rate = float(request.form.get('mutation_rate', 0.1))
        temperature = float(request.form.get('temperature', 1000))
        cooling_rate = float(request.form.get('cooling_rate', 0.95))
        
        # Get data from database
        courses = Course.query.all()
        rooms = Room.query.all()
        time_slots = TimeSlot.query.all()
        constraints = Constraint.query.all()
        
        # Import algorithms here to avoid circular imports
        if algorithm == 'genetic':
            from algorithms.genetic_algorithm import GeneticAlgorithm
            optimizer = GeneticAlgorithm(courses, rooms, time_slots, constraints)
        elif algorithm == 'simulated_annealing':
            from algorithms.simulated_annealing import SimulatedAnnealing
            optimizer = SimulatedAnnealing(courses, rooms, time_slots, constraints)
        else:
            from algorithms.hybrid_optimizer import HybridOptimizer
            optimizer = HybridOptimizer(courses, rooms, time_slots, constraints)
        
        # Run optimization
        best_timetable, fitness_history = optimizer.optimize(
            population_size=population_size,
            generations=generations,
            mutation_rate=mutation_rate,
            temperature=temperature,
            cooling_rate=cooling_rate
        )
        
        # Save best timetable to database
        timetable = Timetable(
            data=json.dumps(best_timetable),
            fitness_score=best_timetable['fitness'],
            algorithm_used=algorithm,
            created_by=current_user.id,
            created_at=datetime.utcnow()
        )
        db.session.add(timetable)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'timetable': best_timetable,
            'fitness_history': fitness_history,
            'message': 'Optimization completed successfully!'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/timetables')
@login_required
def view_timetables():
    """View all generated timetables"""
    timetables = Timetable.query.order_by(Timetable.created_at.desc()).all()
    return render_template('timetables.html', timetables=timetables)

@app.route('/timetable/<int:timetable_id>')
@login_required
def view_timetable(timetable_id):
    """View a specific timetable"""
    timetable = Timetable.query.get_or_404(timetable_id)
    timetable_data = json.loads(timetable.data)
    return render_template('timetable_view.html', timetable=timetable, data=timetable_data)

@app.route('/export/<int:timetable_id>')
@login_required
def export_timetable(timetable_id):
    """Export timetable in various formats"""
    timetable = Timetable.query.get_or_404(timetable_id)
    format_type = request.args.get('format', 'pdf')
    
    # Implementation for export functionality
    # This would generate PDF, Excel, or other formats
    return jsonify({'message': f'Export to {format_type} not yet implemented'})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)
