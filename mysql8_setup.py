#!/usr/bin/env python3
"""
MySQL 8.0 Connection Helper
Specifically designed for MySQL 8.0 authentication issues
"""

import mysql.connector
from mysql.connector import Error
import getpass

def test_mysql8_connection():
    """Test MySQL 8.0 connection with proper authentication"""
    
    print("🔍 MySQL 8.0 Connection Test")
    print("=" * 40)
    
    # Get password from user
    print("Please enter your MySQL root password.")
    print("(If you don't know it, we'll help you reset it)")
    password = getpass.getpass("MySQL root password: ")
    
    # MySQL 8.0 compatible configuration
    config = {
        'host': 'localhost',
        'user': 'root',
        'password': password,
        'port': 3306,
        'auth_plugin': 'mysql_native_password',  # Important for MySQL 8.0
        'autocommit': True,
        'charset': 'utf8mb4'
    }
    
    try:
        print("🔐 Testing connection...")
        connection = mysql.connector.connect(**config)
        
        if connection.is_connected():
            print("✅ SUCCESS! Connected to MySQL 8.0")
            
            # Get server info
            db_info = connection.get_server_info()
            print(f"📊 MySQL Server version: {db_info}")
            
            # Create database if it doesn't exist
            cursor = connection.cursor()
            database_name = 'ghg_emissions_db'
            
            try:
                cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{database_name}`")
                print(f"✅ Database '{database_name}' created/verified")
                
                cursor.execute(f"USE `{database_name}`")
                print(f"✅ Using database '{database_name}'")
                
            except Error as e:
                print(f"⚠️  Database creation warning: {e}")
            
            cursor.close()
            connection.close()
            
            # Update .env file with working configuration
            env_content = f"""# Database Configuration - MySQL 8.0
DB_HOST=localhost
DB_NAME={database_name}
DB_USER=root
DB_PASSWORD={password}
DB_PORT=3306

# Application Configuration
SECRET_KEY=your-secret-key-here-change-in-production
ENVIRONMENT=development"""
            
            with open('.env', 'w') as f:
                f.write(env_content)
            
            print("✅ .env file updated with working configuration!")
            print("\n🎉 Your database is now ready!")
            print("\nYou can now run your Streamlit app:")
            print("streamlit run main_app.py")
            
            return True
            
    except Error as e:
        print(f"❌ Connection failed: {e}")
        
        if "Access denied" in str(e):
            print("\n💡 The password is incorrect or the user doesn't exist.")
            print("Here are your options:")
            print("1. Try a different password")
            print("2. Reset the MySQL root password")
            print("3. Create a new MySQL user for this application")
            
            return False
        else:
            print(f"\n💡 Connection error: {e}")
            return False

def reset_mysql_password_instructions():
    """Provide instructions for resetting MySQL password"""
    print("\n🔧 How to Reset MySQL Root Password:")
    print("=" * 50)
    print("1. Stop MySQL service:")
    print("   net stop MySQL80")
    print("\n2. Start MySQL in safe mode:")
    print("   cd \"C:\\Program Files\\MySQL\\MySQL Server 8.0\\bin\"")
    print("   mysqld --init-file=C:\\mysql-init.txt")
    print("\n3. Create C:\\mysql-init.txt with content:")
    print("   ALTER USER 'root'@'localhost' IDENTIFIED BY 'your_new_password';")
    print("\n4. Restart MySQL normally:")
    print("   net start MySQL80")
    print("\n🔗 Full guide: https://dev.mysql.com/doc/refman/8.0/en/resetting-permissions.html")

def create_new_user_option():
    """Create a new MySQL user instead of using root"""
    print("\n👤 Alternative: Create New MySQL User")
    print("=" * 40)
    print("Instead of using root, we can create a dedicated user for your app.")
    print("\nIf you know the MySQL root password, we can create a new user:")
    
    root_password = getpass.getpass("Enter MySQL root password (to create new user): ")
    
    try:
        # Connect as root to create new user
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password=root_password,
            port=3306,
            auth_plugin='mysql_native_password'
        )
        
        cursor = connection.cursor()
        
        # Create new user
        app_user = 'ghg_app_user'
        app_password = 'ghg_app_password_123'
        database_name = 'ghg_emissions_db'
        
        # Create database
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{database_name}`")
        
        # Create user
        cursor.execute(f"CREATE USER IF NOT EXISTS '{app_user}'@'localhost' IDENTIFIED BY '{app_password}'")
        
        # Grant permissions
        cursor.execute(f"GRANT ALL PRIVILEGES ON `{database_name}`.* TO '{app_user}'@'localhost'")
        cursor.execute("FLUSH PRIVILEGES")
        
        print(f"✅ Created user '{app_user}' with password '{app_password}'")
        print(f"✅ Granted permissions on database '{database_name}'")
        
        # Update .env file
        env_content = f"""# Database Configuration - New User
DB_HOST=localhost
DB_NAME={database_name}
DB_USER={app_user}
DB_PASSWORD={app_password}
DB_PORT=3306

# Application Configuration  
SECRET_KEY=your-secret-key-here-change-in-production
ENVIRONMENT=development"""
        
        with open('.env', 'w') as f:
            f.write(env_content)
        
        print("✅ .env file updated with new user credentials!")
        
        cursor.close()
        connection.close()
        return True
        
    except Error as e:
        print(f"❌ Failed to create user: {e}")
        return False

if __name__ == "__main__":
    print("🚀 MySQL 8.0 Setup Helper")
    print("=" * 30)
    
    if not test_mysql8_connection():
        print("\n❓ What would you like to do?")
        print("1. Try again with different password")
        print("2. Show password reset instructions") 
        print("3. Create new MySQL user (if you know root password)")
        print("4. Exit")
        
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == "1":
            test_mysql8_connection()
        elif choice == "2":
            reset_mysql_password_instructions()
        elif choice == "3":
            create_new_user_option()
        else:
            print("👋 Goodbye! Come back when you're ready to set up the database.")
    else:
        print("\n🎉 Setup complete! You can now run your application.")
