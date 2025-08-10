-- Create database
CREATE DATABASE IF NOT EXISTS ghg_emissions_db;
USE ghg_emissions_db;

-- Users table with role-based authentication
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role ENUM('admin', 'manager', 'normal_user') NOT NULL DEFAULT 'normal_user',
    company_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE
);

-- Companies table
CREATE TABLE IF NOT EXISTS companies (
    id INT AUTO_INCREMENT PRIMARY KEY,
    company_name VARCHAR(200) NOT NULL,
    company_code VARCHAR(50) UNIQUE NOT NULL,
    industry_sector VARCHAR(100),
    address TEXT,
    contact_email VARCHAR(100),
    contact_phone VARCHAR(20),
    verification_status ENUM('pending', 'verified', 'rejected') DEFAULT 'pending',
    verification_date TIMESTAMP NULL,
    verified_by INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (verified_by) REFERENCES users(id)
);

-- GHG Emission Categories (UK System)
CREATE TABLE IF NOT EXISTS ghg_categories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    scope_number INT NOT NULL,
    scope_name VARCHAR(100) NOT NULL,
    category_code VARCHAR(20) NOT NULL,
    category_name VARCHAR(200) NOT NULL,
    subcategory_code VARCHAR(20),
    subcategory_name VARCHAR(200),
    emission_factor DECIMAL(10, 6),
    unit VARCHAR(50),
    description TEXT
);

-- Emissions data table
CREATE TABLE IF NOT EXISTS emissions_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    company_id INT NOT NULL,
    user_id INT NOT NULL,
    category_id INT NOT NULL,
    reporting_period VARCHAR(20) NOT NULL,
    activity_data DECIMAL(15, 4) NOT NULL,
    emission_factor DECIMAL(10, 6) NOT NULL,
    co2_equivalent DECIMAL(15, 4) NOT NULL,
    data_source VARCHAR(200),
    calculation_method VARCHAR(100),
    verification_status ENUM('draft', 'submitted', 'verified') DEFAULT 'draft',
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (company_id) REFERENCES companies(id),
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (category_id) REFERENCES ghg_categories(id)
);

-- Audit trail table
CREATE TABLE IF NOT EXISTS audit_trail (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    action VARCHAR(100) NOT NULL,
    table_name VARCHAR(50) NOT NULL,
    record_id INT NOT NULL,
    old_values JSON,
    new_values JSON,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Add foreign key constraint for companies
ALTER TABLE users ADD FOREIGN KEY (company_id) REFERENCES companies(id);
