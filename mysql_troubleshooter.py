#!/usr/bin/env python3
"""
MySQL Connection Troubleshooter
Tests common MySQL configurations to help identify the correct settings.
"""

import mysql.connector
from mysql.connector import Error
import getpass

def test_mysql_configs():
    """Test common MySQL configurations"""
    
    print("🔍 MySQL Connection Troubleshooter")
    print("=" * 50)
    
    # Common configurations to test
    configs = [
        {
            'name': 'No password (empty)',
            'host': 'localhost',
            'user': 'root',
            'password': '',
            'port': 3306
        },
        {
            'name': 'Password = "root"',
            'host': 'localhost', 
            'user': 'root',
            'password': 'root',
            'port': 3306
        },
        {
            'name': 'Password = "password"',
            'host': 'localhost',
            'user': 'root', 
            'password': 'password',
            'port': 3306
        },
        {
            'name': 'Password = ""',
            'host': 'localhost',
            'user': 'root',
            'password': '',
            'port': 3306
        }
    ]
    
    successful_config = None
    
    for config in configs:
        print(f"\n🧪 Testing: {config['name']}")
        try:
            # Remove name from config for connection
            conn_config = {k: v for k, v in config.items() if k != 'name'}
            connection = mysql.connector.connect(**conn_config)
            
            if connection.is_connected():
                print(f"✅ SUCCESS! Connection worked with: {config['name']}")
                successful_config = conn_config
                
                # Get server info
                db_info = connection.get_server_info()
                print(f"📊 MySQL Server version: {db_info}")
                
                connection.close()
                break
                
        except Error as e:
            print(f"❌ Failed: {e}")
    
    if successful_config:
        print(f"\n🎉 Found working configuration!")
        print("Update your .env file with these settings:")
        print("-" * 40)
        print(f"DB_HOST={successful_config['host']}")
        print(f"DB_USER={successful_config['user']}")
        print(f"DB_PASSWORD={successful_config['password']}")
        print(f"DB_PORT={successful_config['port']}")
        print(f"DB_NAME=ghg_emissions_db")
        
        # Update .env file
        env_content = f"""# Database Configuration
DB_HOST={successful_config['host']}
DB_NAME=ghg_emissions_db
DB_USER={successful_config['user']}
DB_PASSWORD={successful_config['password']}
DB_PORT={successful_config['port']}

# Application Configuration
SECRET_KEY=your-secret-key-here-change-in-production
ENVIRONMENT=development"""
        
        with open('.env', 'w') as f:
            f.write(env_content)
        print("\n✅ .env file updated automatically!")
        
        return successful_config
    else:
        print(f"\n❌ None of the common configurations worked.")
        print("This might mean:")
        print("1. MySQL server is not running")
        print("2. You need to set/reset the root password")
        print("3. MySQL is configured differently")
        
        return None

def manual_password_test():
    """Allow user to manually enter password"""
    print(f"\n🔑 Manual Password Test")
    print("Let's try with a password you provide:")
    
    password = getpass.getpass("Enter MySQL root password (hidden): ")
    
    config = {
        'host': 'localhost',
        'user': 'root', 
        'password': password,
        'port': 3306
    }
    
    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            print("✅ SUCCESS! Password is correct.")
            connection.close()
            
            # Update .env file
            env_content = f"""# Database Configuration
DB_HOST=localhost
DB_NAME=ghg_emissions_db
DB_USER=root
DB_PASSWORD={password}
DB_PORT=3306

# Application Configuration
SECRET_KEY=your-secret-key-here-change-in-production
ENVIRONMENT=development"""
            
            with open('.env', 'w') as f:
                f.write(env_content)
            print("✅ .env file updated with correct password!")
            return True
            
    except Error as e:
        print(f"❌ Still failed: {e}")
        return False

if __name__ == "__main__":
    result = test_mysql_configs()
    
    if not result:
        print("\n❓ Would you like to try entering the password manually? (y/n): ", end="")
        choice = input().strip().lower()
        
        if choice == 'y':
            manual_password_test()
        else:
            print("\n💡 Troubleshooting suggestions:")
            print("1. Check if MySQL/XAMPP/WAMP is running")
            print("2. Reset MySQL root password")
            print("3. Check MySQL installation")
            print("4. Try using MySQL Workbench to connect first")
