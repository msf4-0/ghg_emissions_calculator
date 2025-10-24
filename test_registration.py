#!/usr/bin/env python3
"""
Test user registration functionality
"""

from database_operations import DatabaseManager

def test_user_registration():
    print("🧪 Testing User Registration")
    print("=" * 30)
    
    db = DatabaseManager()
    
    if not db.connect():
        print("❌ Database connection failed")
        return False
    
    # Test user data
    test_users = [
        {
            'username': 'testuser1',
            'email': 'test1@example.com',
            'password': 'password123',
            'role': 'normal_user',
            'company_id': 1
        },
        {
            'username': 'testmanager',
            'email': 'manager@example.com', 
            'password': 'manager123',
            'role': 'manager',
            'company_id': 2
        }
    ]
    
    for user in test_users:
        print(f"\n👤 Testing registration for: {user['username']}")
        
        result = db.create_user(
            username=user['username'],
            email=user['email'],
            password=user['password'],
            role=user['role'],
            company_id=user['company_id']
        )
        
        if result:
            print(f"✅ User '{user['username']}' registered successfully")
        else:
            print(f"❌ Failed to register user '{user['username']}'")
    
    # Test authentication
    print(f"\n🔐 Testing authentication...")
    auth_result = db.authenticate_user('testuser1', 'password123')
    
    if auth_result:
        print("✅ Authentication successful")
        print(f"User data: {auth_result}")
    else:
        print("❌ Authentication failed")
    
    db.disconnect()
    print(f"\n🎉 Registration test completed!")

if __name__ == "__main__":
    test_user_registration()
