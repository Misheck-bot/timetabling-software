import os
import json
import requests
from urllib.parse import urlencode, parse_qs, urlparse
from flask import current_app, session, url_for, redirect, request
from models import User, db
from werkzeug.security import generate_password_hash
from flask_login import login_user
import uuid

class OAuthProvider:
    def __init__(self, provider_name):
        self.provider_name = provider_name
        self.config = current_app.config
        
    def get_authorization_url(self):
        """Get the authorization URL for the OAuth provider"""
        if self.provider_name == 'google':
            return self._get_google_auth_url()
        elif self.provider_name == 'facebook':
            return self._get_facebook_auth_url()
        elif self.provider_name == 'github':
            return self._get_github_auth_url()
        elif self.provider_name == 'microsoft':
            return self._get_microsoft_auth_url()
        else:
            raise ValueError(f"Unsupported OAuth provider: {self.provider_name}")
    
    def handle_callback(self, code):
        """Handle the OAuth callback and return user info"""
        if self.provider_name == 'google':
            return self._handle_google_callback(code)
        elif self.provider_name == 'facebook':
            return self._handle_facebook_callback(code)
        elif self.provider_name == 'github':
            return self._handle_github_callback(code)
        elif self.provider_name == 'microsoft':
            return self._handle_microsoft_callback(code)
        else:
            raise ValueError(f"Unsupported OAuth provider: {self.provider_name}")
    
    def _get_google_auth_url(self):
        """Get Google OAuth authorization URL"""
        params = {
            'client_id': self.config['GOOGLE_CLIENT_ID'],
            'redirect_uri': f"{self.config['OAUTH_REDIRECT_URI']}/oauth/google/callback",
            'scope': 'openid email profile',
            'response_type': 'code',
            'access_type': 'offline',
            'prompt': 'consent'
        }
        return f"https://accounts.google.com/o/oauth2/v2/auth?{urlencode(params)}&state={session.get('oauth_state', '')}"
    
    def _get_facebook_auth_url(self):
        """Get Facebook OAuth authorization URL"""
        params = {
            'client_id': self.config['FACEBOOK_CLIENT_ID'],
            'redirect_uri': f"{self.config['OAUTH_REDIRECT_URI']}/oauth/facebook/callback",
            'scope': 'email,public_profile',
            'response_type': 'code'
        }
        return f"https://www.facebook.com/v18.0/dialog/oauth?{urlencode(params)}&state={session.get('oauth_state', '')}"
    
    def _get_github_auth_url(self):
        """Get GitHub OAuth authorization URL"""
        params = {
            'client_id': self.config['GITHUB_CLIENT_ID'],
            'redirect_uri': f"{self.config['OAUTH_REDIRECT_URI']}/oauth/github/callback",
            'scope': 'user:email',
            'response_type': 'code'
        }
        return f"https://github.com/login/oauth/authorize?{urlencode(params)}&state={session.get('oauth_state', '')}"
    
    def _get_microsoft_auth_url(self):
        """Get Microsoft OAuth authorization URL"""
        params = {
            'client_id': self.config['MICROSOFT_CLIENT_ID'],
            'redirect_uri': f"{self.config['OAUTH_REDIRECT_URI']}/oauth/microsoft/callback",
            'scope': 'openid email profile',
            'response_type': 'code',
            'response_mode': 'query'
        }
        return f"{self.config['MICROSOFT_AUTHORITY']}/oauth2/v2.0/authorize?{urlencode(params)}&state={session.get('oauth_state', '')}"
    
    def _handle_google_callback(self, code):
        """Handle Google OAuth callback"""
        # Exchange code for access token
        token_url = "https://oauth2.googleapis.com/token"
        token_data = {
            'client_id': self.config['GOOGLE_CLIENT_ID'],
            'client_secret': self.config['GOOGLE_CLIENT_SECRET'],
            'code': code,
            'grant_type': 'authorization_code',
            'redirect_uri': f"{self.config['OAUTH_REDIRECT_URI']}/oauth/google/callback"
        }
        
        response = requests.post(token_url, data=token_data)
        if response.status_code != 200:
            return None
        
        token_info = response.json()
        access_token = token_info['access_token']
        
        # Get user info
        user_info_url = "https://www.googleapis.com/oauth2/v2/userinfo"
        headers = {'Authorization': f'Bearer {access_token}'}
        user_response = requests.get(user_info_url, headers=headers)
        
        if user_response.status_code != 200:
            return None
        
        user_data = user_response.json()
        return {
            'provider': 'google',
            'provider_id': user_data['id'],
            'email': user_data['email'],
            'username': user_data.get('given_name', user_data['email'].split('@')[0]),
            'full_name': user_data.get('name', ''),
            'avatar': user_data.get('picture', '')
        }
    
    def _handle_facebook_callback(self, code):
        """Handle Facebook OAuth callback"""
        # Exchange code for access token
        token_url = "https://graph.facebook.com/v18.0/oauth/access_token"
        token_data = {
            'client_id': self.config['FACEBOOK_CLIENT_ID'],
            'client_secret': self.config['FACEBOOK_CLIENT_SECRET'],
            'code': code,
            'redirect_uri': f"{self.config['OAUTH_REDIRECT_URI']}/oauth/facebook/callback"
        }
        
        response = requests.get(token_url, params=token_data)
        if response.status_code != 200:
            return None
        
        token_info = response.json()
        access_token = token_info['access_token']
        
        # Get user info
        user_info_url = "https://graph.facebook.com/me"
        params = {
            'fields': 'id,name,email',
            'access_token': access_token
        }
        user_response = requests.get(user_info_url, params=params)
        
        if user_response.status_code != 200:
            return None
        
        user_data = user_response.json()
        return {
            'provider': 'facebook',
            'provider_id': user_data['id'],
            'email': user_data.get('email', ''),
            'username': user_data.get('name', '').replace(' ', '_').lower(),
            'full_name': user_data.get('name', ''),
            'avatar': f"https://graph.facebook.com/{user_data['id']}/picture"
        }
    
    def _handle_github_callback(self, code):
        """Handle GitHub OAuth callback"""
        # Exchange code for access token
        token_url = "https://github.com/login/oauth/access_token"
        token_data = {
            'client_id': self.config['GITHUB_CLIENT_ID'],
            'client_secret': self.config['GITHUB_CLIENT_SECRET'],
            'code': code
        }
        headers = {'Accept': 'application/json'}
        
        response = requests.post(token_url, data=token_data, headers=headers)
        if response.status_code != 200:
            return None
        
        token_info = response.json()
        access_token = token_info['access_token']
        
        # Get user info
        user_info_url = "https://api.github.com/user"
        headers = {
            'Authorization': f'token {access_token}',
            'Accept': 'application/vnd.github.v3+json'
        }
        user_response = requests.get(user_info_url, headers=headers)
        
        if user_response.status_code != 200:
            return None
        
        user_data = user_response.json()
        
        # Get user email
        email_url = "https://api.github.com/user/emails"
        email_response = requests.get(email_url, headers=headers)
        email_data = email_response.json() if email_response.status_code == 200 else []
        primary_email = next((email['email'] for email in email_data if email['primary']), '')
        
        return {
            'provider': 'github',
            'provider_id': str(user_data['id']),
            'email': primary_email or user_data.get('email', ''),
            'username': user_data.get('login', ''),
            'full_name': user_data.get('name', ''),
            'avatar': user_data.get('avatar_url', '')
        }
    
    def _handle_microsoft_callback(self, code):
        """Handle Microsoft OAuth callback"""
        # Exchange code for access token
        token_url = f"{self.config['MICROSOFT_AUTHORITY']}/oauth2/v2.0/token"
        token_data = {
            'client_id': self.config['MICROSOFT_CLIENT_ID'],
            'client_secret': self.config['MICROSOFT_CLIENT_SECRET'],
            'code': code,
            'grant_type': 'authorization_code',
            'redirect_uri': f"{self.config['OAUTH_REDIRECT_URI']}/oauth/microsoft/callback",
            'scope': 'openid email profile'
        }
        
        response = requests.post(token_url, data=token_data)
        if response.status_code != 200:
            return None
        
        token_info = response.json()
        access_token = token_info['access_token']
        
        # Get user info
        user_info_url = "https://graph.microsoft.com/v1.0/me"
        headers = {'Authorization': f'Bearer {access_token}'}
        user_response = requests.get(user_info_url, headers=headers)
        
        if user_response.status_code != 200:
            return None
        
        user_data = user_response.json()
        return {
            'provider': 'microsoft',
            'provider_id': user_data['id'],
            'email': user_data.get('mail', user_data.get('userPrincipalName', '')),
            'username': user_data.get('displayName', '').replace(' ', '_').lower(),
            'full_name': user_data.get('displayName', ''),
            'avatar': ''
        }

def get_or_create_user(oauth_data):
    """Get existing user or create new one from OAuth data"""
    # Check if user exists by OAuth provider ID
    existing_user = User.query.filter_by(
        oauth_provider=oauth_data['provider'],
        oauth_provider_id=oauth_data['provider_id']
    ).first()
    
    if existing_user:
        return existing_user
    
    # Check if user exists by email
    if oauth_data['email']:
        existing_user = User.query.filter_by(email=oauth_data['email']).first()
        if existing_user:
            # Link OAuth account to existing user
            existing_user.oauth_provider = oauth_data['provider']
            existing_user.oauth_provider_id = oauth_data['provider_id']
            db.session.commit()
            return existing_user
    
    # Create new user
    username = oauth_data['username']
    if not username or User.query.filter_by(username=username).first():
        username = f"{oauth_data['provider']}_{oauth_data['provider_id']}"
    
    new_user = User(
        username=username,
        email=oauth_data['email'] or f"{username}@{oauth_data['provider']}.oauth",
        password_hash=generate_password_hash(str(uuid.uuid4())),  # Random password for OAuth users
        role='user',
        oauth_provider=oauth_data['provider'],
        oauth_provider_id=oauth_data['provider_id'],
        full_name=oauth_data['full_name'],
        avatar_url=oauth_data.get('avatar', '')
    )
    
    db.session.add(new_user)
    db.session.commit()
    return new_user

def get_or_create_user(oauth_data):
    """Get existing user or create new one from OAuth data"""
    # Try to find existing user by OAuth provider ID
    user = User.query.filter_by(
        oauth_provider=oauth_data['provider'],
        oauth_provider_id=oauth_data['provider_id']
    ).first()
    
    if user:
        # Update user info if needed
        if oauth_data.get('full_name'):
            user.full_name = oauth_data['full_name']
        if oauth_data.get('avatar'):
            user.avatar_url = oauth_data['avatar']
        db.session.commit()
        return user
    
    # Try to find by email if no OAuth user found
    if oauth_data.get('email'):
        user = User.query.filter_by(email=oauth_data['email']).first()
        if user:
            # Link OAuth account to existing user
            user.oauth_provider = oauth_data['provider']
            user.oauth_provider_id = oauth_data['provider_id']
            if oauth_data.get('full_name'):
                user.full_name = oauth_data['full_name']
            if oauth_data.get('avatar'):
                user.avatar_url = oauth_data['avatar']
            db.session.commit()
            return user
    
    # Create new user
    return create_oauth_user(oauth_data)
