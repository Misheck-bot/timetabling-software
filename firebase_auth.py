import os
import json
import firebase_admin
from firebase_admin import credentials, auth
from flask import current_app, request, jsonify
from models import User, db
from werkzeug.security import generate_password_hash
import uuid

class FirebaseAuth:
    def __init__(self):
        self.config = current_app.config
        self._initialize_firebase()
    
    def _initialize_firebase(self):
        """Initialize Firebase Admin SDK"""
        if not firebase_admin._apps:
            # Create credentials from environment variables
            cred_dict = {
                "type": "service_account",
                "project_id": self.config['FIREBASE_PROJECT_ID'],
                "private_key_id": self.config['FIREBASE_PRIVATE_KEY_ID'],
                "private_key": self.config['FIREBASE_PRIVATE_KEY'].replace('\\n', '\n') if self.config['FIREBASE_PRIVATE_KEY'] else None,
                "client_email": self.config['FIREBASE_CLIENT_EMAIL'],
                "client_id": self.config['FIREBASE_CLIENT_ID'],
                "auth_uri": self.config['FIREBASE_AUTH_URI'],
                "token_uri": self.config['FIREBASE_TOKEN_URI'],
            }
            
            cred = credentials.Certificate(cred_dict)
            firebase_admin.initialize_app(cred)
    
    def verify_token(self, id_token):
        """Verify Firebase ID token and return user data"""
        try:
            decoded_token = auth.verify_id_token(id_token)
            return decoded_token
        except Exception as e:
            print(f"Error verifying Firebase token: {e}")
            return None
    
    def get_or_create_user(self, firebase_user):
        """Get existing user or create new one from Firebase user data"""
        firebase_uid = firebase_user.get('uid')
        email = firebase_user.get('email')
        name = firebase_user.get('name', '')
        picture = firebase_user.get('picture', '')
        
        # Try to find existing user by Firebase UID
        user = User.query.filter_by(firebase_uid=firebase_uid).first()
        
        if user:
            # Update user info if needed
            if name and user.full_name != name:
                user.full_name = name
            if picture and user.avatar_url != picture:
                user.avatar_url = picture
            db.session.commit()
            return user
        
        # Try to find by email if no Firebase user found
        if email:
            user = User.query.filter_by(email=email).first()
            if user:
                # Link Firebase account to existing user
                user.firebase_uid = firebase_uid
                if name:
                    user.full_name = name
                if picture:
                    user.avatar_url = picture
                db.session.commit()
                return user
        
        # Create new user
        username = email.split('@')[0] if email else f"user_{firebase_uid[:8]}"
        
        # Ensure unique username
        base_username = username
        counter = 1
        while User.query.filter_by(username=username).first():
            username = f"{base_username}_{counter}"
            counter += 1
        
        new_user = User(
            username=username,
            email=email or f"{username}@firebase.auth",
            password_hash=generate_password_hash(str(uuid.uuid4())),  # Random password for Firebase users
            role='user',
            firebase_uid=firebase_uid,
            full_name=name,
            avatar_url=picture
        )
        
        db.session.add(new_user)
        db.session.commit()
        return new_user

def get_firebase_config():
    """Get Firebase configuration for frontend"""
    config = {
        'apiKey': current_app.config.get('FIREBASE_API_KEY'),
        'authDomain': current_app.config.get('FIREBASE_AUTH_DOMAIN'),
        'projectId': current_app.config.get('FIREBASE_PROJECT_ID'),
        'storageBucket': current_app.config.get('FIREBASE_STORAGE_BUCKET'),
        'messagingSenderId': current_app.config.get('FIREBASE_MESSAGING_SENDER_ID'),
        'appId': current_app.config.get('FIREBASE_APP_ID')
    }
    
    # Check for missing configuration
    missing = [key for key, value in config.items() if not value]
    if missing:
        raise ValueError(f"Missing Firebase configuration: {', '.join(missing)}")
    
    return config
