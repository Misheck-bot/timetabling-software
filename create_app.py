from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

# Create extensions
db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    """Application factory function"""
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'login'
    
    # Import and register blueprints
    from app import main_bp
    app.register_blueprint(main_bp)
    
    return app

def init_db(app):
    """Initialize database with app context"""
    with app.app_context():
        db.create_all()
