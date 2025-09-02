#!/usr/bin/env python3
"""
Test script to verify all navigation routes are working
"""

from simple_app import app

def test_routes():
    """Test that all navigation routes are accessible"""
    
    with app.test_client() as client:
        print("Testing navigation routes...")
        
        # Test public routes
        routes_to_test = [
            ('/', 'Home'),
            ('/signup', 'Signup'),
            ('/login', 'Login'),
        ]
        
        for route, name in routes_to_test:
            try:
                response = client.get(route)
                if response.status_code == 200:
                    print(f"✅ {name} route ({route}) - OK")
                else:
                    print(f"❌ {name} route ({route}) - Status: {response.status_code}")
            except Exception as e:
                print(f"❌ {name} route ({route}) - Error: {e}")
        
        # Test authenticated routes (should redirect to login)
        auth_routes = [
            ('/dashboard', 'Dashboard'),
            ('/courses', 'Courses'),
            ('/rooms', 'Rooms'),
            ('/constraints', 'Constraints'),
            ('/timetables', 'Timetables'),
            ('/profile', 'Profile'),
            ('/settings', 'Settings'),
        ]
        
        print("\nTesting authenticated routes (should redirect to login):")
        for route, name in auth_routes:
            try:
                response = client.get(route)
                if response.status_code == 302:  # Redirect to login
                    print(f"✅ {name} route ({route}) - Redirects to login (OK)")
                else:
                    print(f"❌ {name} route ({route}) - Unexpected status: {response.status_code}")
            except Exception as e:
                print(f"❌ {name} route ({route}) - Error: {e}")
        
        # Test OAuth routes
        oauth_routes = [
            ('/oauth/google/login', 'Google OAuth Login'),
            ('/oauth/facebook/login', 'Facebook OAuth Login'),
            ('/oauth/github/login', 'GitHub OAuth Login'),
            ('/oauth/microsoft/login', 'Microsoft OAuth Login'),
        ]
        
        print("\nTesting OAuth routes:")
        for route, name in oauth_routes:
            try:
                response = client.get(route)
                if response.status_code == 302:  # Redirect to login
                    print(f"✅ {name} route ({route}) - Redirects to login (OK)")
                else:
                    print(f"❌ {name} route ({route}) - Unexpected status: {response.status_code}")
            except Exception as e:
                print(f"❌ {name} route ({route}) - Error: {e}")
        
        print("\n✅ Navigation test completed!")

if __name__ == '__main__':
    test_routes()
