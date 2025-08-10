#!/usr/bin/env python3
"""
AWS RDS Database Setup Script
Run this after creating your RDS instance to initialize the database
"""
import os
import sys
import mysql.connector
from mysql.connector import Error

def create_database_and_user():
    """Create the application database"""
    
    # Get RDS connection details
    host = input("Enter your RDS endpoint (e.g., mydb.abc123.us-east-1.rds.amazonaws.com): ")
    master_user = input("Enter RDS master username (usually 'admin'): ")
    master_password = input("Enter RDS master password: ")
    
    try:
        # Connect to RDS instance
        print("🔌 Connecting to RDS instance...")
        connection = mysql.connector.connect(
            host=host,
            user=master_user,
            password=master_password,
            port=3306
        )
        
        if connection.is_connected():
            cursor = connection.cursor()
            
            # Create database
            print("📦 Creating database 'ghg_emissions_db'...")
            cursor.execute("CREATE DATABASE IF NOT EXISTS ghg_emissions_db")
            
            # Use the database
            cursor.execute("USE ghg_emissions_db")
            
            print("✅ Database created successfully!")
            print("\n📋 Use these details in your App Runner environment variables:")
            print(f"DB_HOST = {host}")
            print(f"DB_NAME = ghg_emissions_db")
            print(f"DB_USER = {master_user}")
            print(f"DB_PASSWORD = {master_password}")
            print(f"DB_PORT = 3306")
            
            return True
            
    except Error as e:
        print(f"❌ Error: {e}")
        return False
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

def setup_aws_database():
    """Complete AWS database setup"""
    print("🚀 AWS RDS Database Setup for GHG Emissions Calculator")
    print("=" * 60)
    
    if create_database_and_user():
        print("\n✅ AWS RDS setup completed!")
        print("\n📝 Next steps:")
        print("1. Copy the database details above")
        print("2. Add them as environment variables in AWS App Runner")
        print("3. Deploy your application")
        print("4. The app will automatically create tables on first run")
    else:
        print("\n❌ Setup failed. Please check your RDS configuration.")

if __name__ == "__main__":
    setup_aws_database()
