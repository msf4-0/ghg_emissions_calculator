#!/usr/bin/env python3
"""
Debug user registration issues
"""

from database_operations import DatabaseManager
from config import Config

def debug_registration():
    print("🔍 Debugging User Registration")
    print("=" * 40)
    
    # Check configuration
    config = Config()
    security_config = config.security_config
    
    print("🔧 Security Configuration:")
    print(f"- Min password length: {security_config['password_min_length']}")
    print(f"- Require special chars: {security_config['password_require_special']}")
    
    db = DatabaseManager()
    
    if not db.connect():
        print("❌ Database connection failed")
        return False
    
    # Test password validation
    test_passwords = [
        'password123',      # No special chars
        'password123!',     # With special chars
        'pass',            # Too short
        'Password123!@'    # Strong password
    ]
    
    print(f"\n🔑 Testing password validation:")
    for pwd in test_passwords:
        is_valid = db._validate_password(pwd)
        print(f"- '{pwd}': {'✅ Valid' if is_valid else '❌ Invalid'}")
    
    # Test with valid password
    print(f"\n👤 Testing user creation with valid password...")
    
    test_user = {
        'username': 'testuser_debug',
        'email': 'testdebug@example.com',
        'password': 'Password123!',  # Valid password with special chars
        'role': 'normal_user',
        'company_id': 1
    }
    
    try:
        result = db.create_user(
            username=test_user['username'],
            email=test_user['email'],
            password=test_user['password'],
            role=test_user['role'],
            company_id=test_user['company_id']
        )
        
        if result:
            print("✅ User created successfully!")
            
            # Test authentication
            auth_result = db.authenticate_user(test_user['username'], test_user['password'])
            if auth_result:
                print("✅ Authentication successful!")
                print(f"User data: {auth_result}")
            else:
                print("❌ Authentication failed")
        else:
            print("❌ User creation failed")
            
    except Exception as e:
        print(f"❌ Exception during user creation: {e}")
    
    db.disconnect()

if __name__ == "__main__":
    debug_registration()
