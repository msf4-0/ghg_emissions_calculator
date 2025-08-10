#!/usr/bin/env python3
"""
Database setup script for production deployment
"""
import os
import sys
from database_operations import DatabaseManager
from config import Config

def setup_production_database():
    """Setup database for production deployment"""
    print("🚀 Setting up production database...")
    
    config = Config()
    db_manager = DatabaseManager()
    
    try:
        # Test connection
        if not db_manager.connect():
            print("❌ Failed to connect to database")
            return False
            
        print("✅ Database connection successful")
        
        # Run database setup
        from setup_database import setup_complete_database
        success = setup_complete_database()
        
        if success:
            print("✅ Database setup completed successfully")
            return True
        else:
            print("❌ Database setup failed")
            return False
            
    except Exception as e:
        print(f"❌ Error during setup: {e}")
        return False
    finally:
        db_manager.disconnect()

if __name__ == "__main__":
    if setup_production_database():
        print("🎉 Production database is ready!")
        sys.exit(0)
    else:
        print("💥 Production database setup failed!")
        sys.exit(1)
