#!/usr/bin/env python3
"""
Database Schema Setup for GHG Emissions Calculator
Creates all necessary tables for the application
"""

import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

def create_database_schema():
    """Create all database tables for the GHG emissions calculator"""
    
    print("🏗️  Setting up GHG Emissions Calculator Database Schema")
    print("=" * 60)
    
    # Database configuration
    config = {
        'host': os.getenv('DB_HOST', 'localhost'),
        'database': os.getenv('DB_NAME', 'ghg_emissions_db'),
        'user': os.getenv('DB_USER', 'root'),
        'password': os.getenv('DB_PASSWORD', ''),
        'port': int(os.getenv('DB_PORT', '3306')),
        'auth_plugin': 'mysql_native_password',
        'autocommit': True,
        'charset': 'utf8mb4'
    }
    
    try:
        print("🔐 Connecting to database...")
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()
        
        print("✅ Connected successfully!")
        
        # SQL statements to create tables
        tables = {
            'companies': """
            CREATE TABLE IF NOT EXISTS companies (
                id INT AUTO_INCREMENT PRIMARY KEY,
                company_name VARCHAR(255) NOT NULL UNIQUE,
                company_code VARCHAR(50) UNIQUE,
                industry_sector VARCHAR(100),
                address TEXT,
                contact_email VARCHAR(255),
                contact_phone VARCHAR(50),
                verification_status ENUM('pending', 'verified', 'rejected') DEFAULT 'pending',
                verification_date DATETIME NULL,
                verified_by INT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
            """,
            
            'users': """
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50) NOT NULL UNIQUE,
                email VARCHAR(255) NOT NULL UNIQUE,
                password_hash VARCHAR(255) NOT NULL,
                role ENUM('admin', 'manager', 'normal_user') DEFAULT 'normal_user',
                company_id INT NULL,
                is_active BOOLEAN DEFAULT TRUE,
                last_login TIMESTAMP NULL,
                failed_login_attempts INT DEFAULT 0,
                locked_until TIMESTAMP NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                FOREIGN KEY (company_id) REFERENCES companies(id) ON DELETE SET NULL
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
            """,
            
            'ghg_categories': """
            CREATE TABLE IF NOT EXISTS ghg_categories (
                id INT AUTO_INCREMENT PRIMARY KEY,
                scope_number INT NOT NULL,
                scope_name VARCHAR(50) NOT NULL,
                category_code VARCHAR(20) NOT NULL,
                category_name VARCHAR(255) NOT NULL,
                subcategory_code VARCHAR(20) NOT NULL,
                subcategory_name VARCHAR(255) NOT NULL,
                emission_factor DECIMAL(15,6) DEFAULT 0,
                unit VARCHAR(50) NOT NULL,
                description TEXT,
                is_active BOOLEAN DEFAULT TRUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                UNIQUE KEY unique_category (scope_number, category_code, subcategory_code)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
            """,
            
            'emissions_data': """
            CREATE TABLE IF NOT EXISTS emissions_data (
                id INT AUTO_INCREMENT PRIMARY KEY,
                company_id INT NOT NULL,
                user_id INT NOT NULL,
                category_id INT NOT NULL,
                reporting_period VARCHAR(20) NOT NULL,
                activity_data DECIMAL(15,4) NOT NULL,
                emission_factor DECIMAL(15,6) NOT NULL,
                co2_equivalent DECIMAL(15,4) NOT NULL,
                data_source VARCHAR(255),
                calculation_method VARCHAR(100),
                verification_status ENUM('pending', 'verified', 'rejected') DEFAULT 'pending',
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                FOREIGN KEY (company_id) REFERENCES companies(id) ON DELETE CASCADE,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                FOREIGN KEY (category_id) REFERENCES ghg_categories(id) ON DELETE CASCADE
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
            """,
            
            'audit_trail': """
            CREATE TABLE IF NOT EXISTS audit_trail (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                action VARCHAR(50) NOT NULL,
                table_name VARCHAR(50) NOT NULL,
                record_id INT NOT NULL,
                old_values JSON,
                new_values JSON,
                ip_address VARCHAR(45),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
            """
        }
        
        # Create tables
        for table_name, sql in tables.items():
            print(f"📋 Creating table: {table_name}")
            try:
                cursor.execute(sql)
                print(f"✅ Table '{table_name}' created successfully")
            except Error as e:
                print(f"⚠️  Table '{table_name}': {e}")
        
        # Insert sample GHG categories
        print("\n📊 Inserting sample GHG categories...")
        sample_categories = [
            # Scope 1 - Direct emissions
            (1, 'Scope 1 - Direct', 'S1-FC', 'Stationary Fuel Combustion', 'S1-FC-01', 'Natural Gas Combustion', 2.032, 'kg CO2e/m³'),
            (1, 'Scope 1 - Direct', 'S1-FC', 'Stationary Fuel Combustion', 'S1-FC-02', 'Diesel Fuel Combustion', 2.665, 'kg CO2e/L'),
            (1, 'Scope 1 - Direct', 'S1-MC', 'Mobile Fuel Combustion', 'S1-MC-01', 'Gasoline Vehicles', 2.310, 'kg CO2e/L'),
            (1, 'Scope 1 - Direct', 'S1-MC', 'Mobile Fuel Combustion', 'S1-MC-02', 'Diesel Vehicles', 2.665, 'kg CO2e/L'),
            
            # Scope 2 - Indirect emissions from energy
            (2, 'Scope 2 - Indirect Energy', 'S2-EC', 'Purchased Electricity', 'S2-EC-01', 'Grid Electricity', 0.499, 'kg CO2e/kWh'),
            (2, 'Scope 2 - Indirect Energy', 'S2-HC', 'Purchased Heating/Cooling', 'S2-HC-01', 'District Heating', 0.200, 'kg CO2e/kWh'),
            
            # Scope 3 - Other indirect emissions
            (3, 'Scope 3 - Other Indirect', 'S3-BT', 'Business Travel', 'S3-BT-01', 'Air Travel - Domestic', 0.255, 'kg CO2e/km'),
            (3, 'Scope 3 - Other Indirect', 'S3-BT', 'Business Travel', 'S3-BT-02', 'Air Travel - International', 0.195, 'kg CO2e/km'),
            (3, 'Scope 3 - Other Indirect', 'S3-EC', 'Employee Commuting', 'S3-EC-01', 'Car Commuting', 0.171, 'kg CO2e/km'),
            (3, 'Scope 3 - Other Indirect', 'S3-WG', 'Waste Generated', 'S3-WG-01', 'General Waste to Landfill', 0.494, 'kg CO2e/kg')
        ]
        
        insert_category_sql = """
        INSERT IGNORE INTO ghg_categories 
        (scope_number, scope_name, category_code, category_name, subcategory_code, subcategory_name, emission_factor, unit)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        cursor.executemany(insert_category_sql, sample_categories)
        print(f"✅ Inserted {cursor.rowcount} GHG categories")
        
        # Insert a sample company
        print("\n🏢 Creating sample company...")
        sample_company_sql = """
        INSERT IGNORE INTO companies (company_name, company_code, industry_sector, verification_status)
        VALUES ('Sample Company Ltd', 'SAMPLE001', 'Technology', 'verified')
        """
        cursor.execute(sample_company_sql)
        
        if cursor.rowcount > 0:
            print("✅ Sample company created")
        else:
            print("ℹ️  Sample company already exists")
        
        # Create an admin user
        print("\n👤 Creating admin user...")
        import hashlib
        
        # Hash password with simple method (same as in your app)
        admin_password = "admin123"
        salt = os.getenv('SECRET_KEY', 'your-secret-key-here-change-in-production')
        password_hash = hashlib.sha256((admin_password + salt).encode()).hexdigest()
        
        admin_user_sql = """
        INSERT IGNORE INTO users (username, email, password_hash, role, company_id)
        VALUES ('admin', 'admin@sample.com', %s, 'admin', 1)
        """
        cursor.execute(admin_user_sql, (password_hash,))
        
        if cursor.rowcount > 0:
            print("✅ Admin user created (username: admin, password: admin123)")
        else:
            print("ℹ️  Admin user already exists")
        
        print("\n🎉 Database schema setup completed successfully!")
        print("\nYou can now:")
        print("1. Register new users")
        print("2. Login with admin/admin123")
        print("3. Add emissions data")
        print("4. Generate reports")
        
        cursor.close()
        connection.close()
        return True
        
    except Error as e:
        print(f"❌ Database setup failed: {e}")
        return False

def show_table_info():
    """Show information about created tables"""
    config = {
        'host': os.getenv('DB_HOST', 'localhost'),
        'database': os.getenv('DB_NAME', 'ghg_emissions_db'),
        'user': os.getenv('DB_USER', 'root'),
        'password': os.getenv('DB_PASSWORD', ''),
        'port': int(os.getenv('DB_PORT', '3306')),
        'auth_plugin': 'mysql_native_password',
        'autocommit': True,
        'charset': 'utf8mb4'
    }
    
    try:
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()
        
        print("\n📊 Database Table Information:")
        print("=" * 40)
        
        # Show tables
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        
        for table in tables:
            table_name = table[0]
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = cursor.fetchone()[0]
            print(f"📋 {table_name}: {count} records")
        
        cursor.close()
        connection.close()
        
    except Error as e:
        print(f"❌ Failed to show table info: {e}")

if __name__ == "__main__":
    if create_database_schema():
        show_table_info()
    else:
        print("\n💡 Please check your database connection and try again.")
