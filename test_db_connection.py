#!/usr/bin/env python3
"""
Database Connection Test Script
This script helps you test and configure your MySQL database connection.
"""

import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_database_connection():
    """Test database connection with different configurations"""
    
    print("🔍 Testing MySQL Database Connection...")
    print("=" * 50)
    
    # Configuration from environment variables
    config = {
        'host': os.getenv('DB_HOST', 'localhost'),
        'database': os.getenv('DB_NAME', 'ghg_emissions_db'),
        'user': os.getenv('DB_USER', 'root'),
        'password': os.getenv('DB_PASSWORD', ''),
        'port': int(os.getenv('DB_PORT', '3306')),
    }
    
    print(f"Host: {config['host']}")
    print(f"Port: {config['port']}")
    print(f"Database: {config['database']}")
    print(f"User: {config['user']}")
    print(f"Password: {'*' * len(config['password']) if config['password'] else '(empty)'}")
    print("-" * 50)
    
    # Test 1: Basic connection test
    try:
        print("🔐 Testing connection...")
        connection = mysql.connector.connect(**config)
        
        if connection.is_connected():
            print("✅ Connection successful!")
            
            # Get server info
            db_info = connection.get_server_info()
            print(f"📊 MySQL Server version: {db_info}")
            
            # Test database existence
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")
            database_name = cursor.fetchone()
            print(f"📦 Connected to database: {database_name[0] if database_name[0] else 'None'}")
            
            cursor.close()
            connection.close()
            print("🔒 Connection closed successfully")
            return True
            
    except Error as e:
        print(f"❌ Connection failed: {e}")
        
        if "Access denied" in str(e):
            print("\n💡 Troubleshooting Tips:")
            print("1. Check your MySQL password in the .env file")
            print("2. Make sure MySQL server is running")
            print("3. Verify the username has proper permissions")
            print("4. Try connecting with a MySQL client first")
            
        elif "Unknown database" in str(e):
            print(f"\n💡 Database '{config['database']}' doesn't exist.")
            print("Would you like to create it? (Check the create_database function)")
            
        elif "Can't connect to MySQL server" in str(e):
            print("\n💡 MySQL server is not running or not accessible.")
            print("1. Start your MySQL server")
            print("2. Check if the host and port are correct")
        
        return False

def create_database_if_not_exists():
    """Create the database if it doesn't exist"""
    config_without_db = {
        'host': os.getenv('DB_HOST', 'localhost'),
        'user': os.getenv('DB_USER', 'root'),
        'password': os.getenv('DB_PASSWORD', ''),
        'port': int(os.getenv('DB_PORT', '3306')),
    }
    
    database_name = os.getenv('DB_NAME', 'ghg_emissions_db')
    
    try:
        print(f"🏗️  Creating database '{database_name}'...")
        connection = mysql.connector.connect(**config_without_db)
        cursor = connection.cursor()
        
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{database_name}`")
        print(f"✅ Database '{database_name}' created successfully!")
        
        cursor.close()
        connection.close()
        return True
        
    except Error as e:
        print(f"❌ Failed to create database: {e}")
        return False

def interactive_config():
    """Interactive configuration helper"""
    print("\n🔧 Interactive Database Configuration")
    print("=" * 50)
    
    print("Please provide your MySQL connection details:")
    
    host = input(f"Host (default: localhost): ").strip() or "localhost"
    port = input(f"Port (default: 3306): ").strip() or "3306"  
    user = input(f"Username (default: root): ").strip() or "root"
    password = input(f"Password: ").strip()
    database = input(f"Database name (default: ghg_emissions_db): ").strip() or "ghg_emissions_db"
    
    # Update .env file
    env_content = f"""# Database Configuration
DB_HOST={host}
DB_NAME={database}
DB_USER={user}
DB_PASSWORD={password}
DB_PORT={port}

# Application Configuration
SECRET_KEY=your-secret-key-here-change-in-production
ENVIRONMENT=development"""
    
    with open('.env', 'w') as f:
        f.write(env_content)
    
    print("\n✅ Configuration saved to .env file")
    return True

if __name__ == "__main__":
    print("🚀 GHG Emissions Calculator - Database Setup")
    print("=" * 50)
    
    # Test current configuration
    if not test_database_connection():
        print("\n❓ Would you like to:")
        print("1. Update database configuration interactively")
        print("2. Create the database")
        print("3. Exit")
        
        choice = input("\nEnter your choice (1-3): ").strip()
        
        if choice == "1":
            interactive_config()
            print("\n🔄 Testing new configuration...")
            test_database_connection()
        elif choice == "2":
            create_database_if_not_exists()
        else:
            print("👋 Goodbye!")
    else:
        print("\n🎉 Database connection is working perfectly!")
        print("You can now run your Streamlit application.")
