import mysql.connector
from mysql.connector import Error, pooling
import hashlib
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any, Union
import os
import streamlit as st
from config import Config
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize configuration
config = Config()

class DatabaseManager:
    def __init__(self):
        self.db_config = config.database_config
        self.connection_pool = None
        self.connection = None
        self._setup_connection_pool()
    
    def _setup_connection_pool(self):
        """Setup connection pool for production deployment"""
        try:
            if config.is_production:
                pool_config = self.db_config.copy()
                pool_config.update({
                    'pool_name': 'ghg_pool',
                    'pool_size': 10,
                    'pool_reset_session': True
                })
                self.connection_pool = pooling.MySQLConnectionPool(**pool_config)
                logger.info("Database connection pool created successfully")
            else:
                logger.info("Development mode: using direct connections")
        except Error as e:
            logger.error(f"Error creating connection pool: {e}")
            if config.is_production:
                st.error("Database connection pool setup failed")
                st.stop()
    
    def connect(self) -> bool:
        """Establish database connection"""
        try:
            if config.is_production and self.connection_pool:
                self.connection = self.connection_pool.get_connection()
            else:
                self.connection = mysql.connector.connect(**self.db_config)
            
            if self.connection and self.connection.is_connected():
                return True
        except Error as e:
            logger.error(f"Error connecting to MySQL: {e}")
            if config.is_production:
                st.error("Database connection failed. Please try again later.")
            else:
                st.error(f"Database connection failed: {e}")
            return False
    
    def disconnect(self):
        """Close database connection"""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            self.connection = None
    
    def execute_query(self, query: str, params: tuple = None, return_id: bool = False) -> Union[bool, int]:
        """Execute INSERT, UPDATE, DELETE queries"""
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params)
            self.connection.commit()
            
            if return_id:
                last_id = cursor.lastrowid
                cursor.close()
                return last_id
            
            cursor.close()
            return True
        except Error as e:
            logger.error(f"Error executing query: {e}")
            if self.connection:
                self.connection.rollback()
            return False
    
    def fetch_query(self, query: str, params: tuple = None) -> List[tuple]:
        """Execute SELECT queries and return results"""
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params)
            results = cursor.fetchall()
            cursor.close()
            return results
        except Error as e:
            logger.error(f"Error fetching data: {e}")
            return []
    
    def fetch_one(self, query: str, params: tuple = None) -> Optional[tuple]:
        """Execute SELECT query and return single result"""
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params)
            result = cursor.fetchone()
            cursor.close()
            return result
        except Error as e:
            logger.error(f"Error fetching data: {e}")
            return None
    
    def execute_transaction(self, queries: List[Tuple[str, tuple]]) -> bool:
        """Execute multiple queries in a transaction"""
        try:
            cursor = self.connection.cursor()
            self.connection.start_transaction()
            
            for query, params in queries:
                cursor.execute(query, params)
            
            self.connection.commit()
            cursor.close()
            return True
        except Error as e:
            logger.error(f"Transaction error: {e}")
            if self.connection:
                self.connection.rollback()
            return False

    # Enhanced User Management with security
    def create_user(self, username: str, email: str, password: str, role: str = 'normal_user', 
                   company_id: int = None, created_by: int = None) -> bool:
        """Create a new user with enhanced security"""
        # Validate password strength
        if not self._validate_password(password):
            return False
        
        password_hash = self._hash_password(password)
        query = """
        INSERT INTO users (username, email, password_hash, role, company_id)
        VALUES (%s, %s, %s, %s, %s)
        """
        
        success = self.execute_query(query, (username, email, password_hash, role, company_id))
        
        if success and created_by:
            # Log user creation
            self._log_audit_trail(created_by, 'CREATE_USER', 'users', 0, {}, {
                'username': username, 'email': email, 'role': role
            })
        
        return success
    
    def authenticate_user(self, username: str, password: str, ip_address: str = None) -> Optional[Dict]:
        """Authenticate user with enhanced security"""
        # Check for account lockout
        if self._is_account_locked(username):
            return None
        
        password_hash = self._hash_password(password)
        query = """
        SELECT u.id, u.username, u.email, u.role, u.company_id, c.company_name, 
               c.verification_status, u.is_active
        FROM users u
        LEFT JOIN companies c ON u.company_id = c.id
        WHERE u.username = %s AND u.password_hash = %s AND u.is_active = TRUE
        """
        result = self.fetch_one(query, (username, password_hash))
        
        if result:
            # Reset failed login attempts on successful login
            self._reset_failed_attempts(username)
            
            # Log successful login
            self._log_audit_trail(result[0], 'LOGIN_SUCCESS', 'users', result[0], {}, {
                'ip_address': ip_address
            })
            
            return {
                'id': result[0],
                'username': result[1],
                'email': result[2],
                'role': result[3],
                'company_id': result[4],
                'company_name': result[5],
                'company_verified': result[6] == 'verified',
                'is_active': result[7]
            }
        else:
            # Record failed login attempt
            self._record_failed_attempt(username, ip_address)
            return None
    
    def _validate_password(self, password: str) -> bool:
        """Validate password strength"""
        security_config = config.security_config
        
        if len(password) < security_config['password_min_length']:
            return False
        
        if security_config['password_require_special']:
            special_chars = "!@#$%^&*()_+-=[]{}|;:,.<>?"
            if not any(char in special_chars for char in password):
                return False
        
        return True
    
    def _hash_password(self, password: str) -> str:
        """Hash password with salt"""
        salt = config.app_config['secret_key']
        return hashlib.sha256((password + salt).encode()).hexdigest()
    
    def _is_account_locked(self, username: str) -> bool:
        """Check if account is locked due to failed attempts"""
        # Implementation for account lockout logic
        return False  # Simplified for now
    
    def _reset_failed_attempts(self, username: str):
        """Reset failed login attempts"""
        # Implementation for resetting failed attempts
        pass
    
    def _record_failed_attempt(self, username: str, ip_address: str = None):
        """Record failed login attempt"""
        # Implementation for recording failed attempts
        pass
    
    def _log_audit_trail(self, user_id: int, action: str, table_name: str, record_id: int, 
                        old_values: Dict, new_values: Dict, ip_address: str = None):
        """Log audit trail"""
        query = """
        INSERT INTO audit_trail (user_id, action, table_name, record_id, old_values, new_values, ip_address)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        self.execute_query(query, (
            user_id, action, table_name, record_id,
            json.dumps(old_values), json.dumps(new_values), ip_address
        ))

    # Enhanced Company Management
    def create_company(self, company_name: str, company_code: str, industry_sector: str = None, 
                      address: str = None, contact_email: str = None, contact_phone: str = None,
                      created_by: int = None) -> bool:
        """Create a new company"""
        query = """
        INSERT INTO companies (company_name, company_code, industry_sector, address, contact_email, contact_phone)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        success = self.execute_query(query, (company_name, company_code, industry_sector, 
                                           address, contact_email, contact_phone))
        
        if success and created_by:
            self._log_audit_trail(created_by, 'CREATE_COMPANY', 'companies', 0, {}, {
                'company_name': company_name, 'company_code': company_code
            })
        
        return success
    
    def get_companies(self, verification_status: str = None, limit: int = None) -> List[Dict]:
        """Get companies with optional filters"""
        base_query = "SELECT * FROM companies"
        params = []
        
        if verification_status:
            base_query += " WHERE verification_status = %s"
            params.append(verification_status)
        
        base_query += " ORDER BY created_at DESC"
        
        if limit:
            base_query += " LIMIT %s"
            params.append(limit)
        
        results = self.fetch_query(base_query, tuple(params) if params else None)
        
        return [
            {
                'id': row[0],
                'company_name': row[1],
                'company_code': row[2],
                'industry_sector': row[3],
                'address': row[4],
                'contact_email': row[5],
                'contact_phone': row[6],
                'verification_status': row[7],
                'verification_date': row[8],
                'verified_by': row[9],
                'created_at': row[10],
                'updated_at': row[11]
            }
            for row in results
        ]

    def verify_company(self, company_id: int, verified_by: int, status: str) -> bool:
        """Verify or reject a company"""
        query = """
        UPDATE companies 
        SET verification_status = %s, verification_date = CURRENT_TIMESTAMP, verified_by = %s 
        WHERE id = %s
        """
        success = self.execute_query(query, (status, verified_by, company_id))
        
        if success:
            self._log_audit_trail(verified_by, 'VERIFY_COMPANY', 'companies', company_id, {}, {
                'verification_status': status, 'verified_by': verified_by
            })
        
        return success
    
    def get_users(self, company_id: int = None, is_active: bool = None) -> List[Dict]:
        """Get users with optional filters"""
        base_query = """
        SELECT u.id, u.username, u.email, u.role, u.company_id, c.company_name, 
               u.is_active, u.last_login, u.created_at
        FROM users u
        LEFT JOIN companies c ON u.company_id = c.id
        """
        
        conditions = []
        params = []
        
        if company_id:
            conditions.append("u.company_id = %s")
            params.append(company_id)
        
        if is_active is not None:
            conditions.append("u.is_active = %s")
            params.append(is_active)
        
        if conditions:
            base_query += " WHERE " + " AND ".join(conditions)
        
        base_query += " ORDER BY u.created_at DESC"
        
        results = self.fetch_query(base_query, tuple(params) if params else None)
        
        return [
            {
                'id': row[0],
                'username': row[1],
                'email': row[2],
                'role': row[3],
                'company_id': row[4],
                'company_name': row[5],
                'is_active': row[6],
                'last_login': row[7],
                'created_at': row[8]
            }
            for row in results
        ]

    # Enhanced GHG Categories (cache removed to fix display issue)
    def get_ghg_categories(self, scope: int = None) -> List[Dict]:
        """Get GHG categories with caching for performance"""
        if not self.connect():
            return []
        
        try:
            if scope:
                query = """
                SELECT * FROM ghg_categories 
                WHERE scope_number = %s AND is_active = TRUE 
                ORDER BY category_code, subcategory_code
                """
                results = self.fetch_query(query, (scope,))
            else:
                query = """
                SELECT * FROM ghg_categories 
                WHERE is_active = TRUE 
                ORDER BY scope_number, category_code, subcategory_code
                """
                results = self.fetch_query(query)
            
            return [
                {
                    'id': row[0],
                    'scope_number': row[1],
                    'scope_name': row[2],
                    'category_code': row[3],
                    'category_name': row[4],
                    'subcategory_code': row[5],
                    'subcategory_name': row[6],
                    'emission_factor': float(row[7]) if row[7] else 0.0,
                    'unit': row[8],
                    'description': row[9],
                    'is_active': row[10]
                }
                for row in results
            ]
        finally:
            self.disconnect()

    # Enhanced Emissions Data Management
    def add_emission_data(self, company_id: int, user_id: int, category_id: int, 
                         reporting_period: str, activity_data: float, emission_factor: float,
                         data_source: str = None, calculation_method: str = None, 
                         notes: str = None) -> bool:
        """Add new emission data with validation"""
        # Validate input data
        if activity_data < 0 or emission_factor < 0:
            return False
        
        co2_equivalent = activity_data * emission_factor
        query = """
        INSERT INTO emissions_data 
        (company_id, user_id, category_id, reporting_period, activity_data, emission_factor, 
         co2_equivalent, data_source, calculation_method, notes)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        success = self.execute_query(query, (company_id, user_id, category_id, reporting_period, 
                                           activity_data, emission_factor, co2_equivalent, 
                                           data_source, calculation_method, notes))
        
        if success:
            self._log_audit_trail(user_id, 'ADD_EMISSION_DATA', 'emissions_data', 0, {}, {
                'company_id': company_id, 'category_id': category_id, 
                'reporting_period': reporting_period, 'co2_equivalent': co2_equivalent
            })
        
        return success
    
    def get_emissions_data(self, company_id: int = None, reporting_period: str = None, 
                          limit: int = None, offset: int = 0) -> List[Dict]:
        """Get emissions data with pagination"""
        base_query = """
        SELECT e.*, c.subcategory_name, c.scope_number, c.scope_name, c.unit, comp.company_name
        FROM emissions_data e
        JOIN ghg_categories c ON e.category_id = c.id
        JOIN companies comp ON e.company_id = comp.id
        """
        
        conditions = []
        params = []
        
        if company_id:
            conditions.append("e.company_id = %s")
            params.append(company_id)
        
        if reporting_period:
            conditions.append("e.reporting_period = %s")
            params.append(reporting_period)
        
        if conditions:
            base_query += " WHERE " + " AND ".join(conditions)
        
        base_query += " ORDER BY e.created_at DESC"
        
        if limit:
            base_query += " LIMIT %s OFFSET %s"
            params.extend([limit, offset])
        
        results = self.fetch_query(base_query, tuple(params))
        
        return [
            {
                'id': row[0],
                'company_id': row[1],
                'user_id': row[2],
                'category_id': row[3],
                'reporting_period': row[4],
                'activity_data': float(row[5]),
                'emission_factor': float(row[6]),
                'co2_equivalent': float(row[7]),
                'data_source': row[8],
                'calculation_method': row[9],
                'verification_status': row[10],
                'notes': row[11],
                'created_at': row[12],
                'updated_at': row[13],
                'subcategory_name': row[14],
                'scope_number': row[15],
                'scope_name': row[16],
                'unit': row[17],
                'company_name': row[18]
            }
            for row in results
        ]

    def get_emissions_summary(self, company_id: int = None, reporting_period: str = None) -> Dict:
        """Get emissions summary by scope with enhanced performance"""
        base_query = """
        SELECT c.scope_number, c.scope_name, SUM(e.co2_equivalent) as total_emissions,
               COUNT(e.id) as entry_count
        FROM emissions_data e
        JOIN ghg_categories c ON e.category_id = c.id
        """
        
        conditions = []
        params = []
        
        if company_id:
            conditions.append("e.company_id = %s")
            params.append(company_id)
        
        if reporting_period:
            conditions.append("e.reporting_period = %s")
            params.append(reporting_period)
        
        if conditions:
            base_query += " WHERE " + " AND ".join(conditions)
        
        base_query += " GROUP BY c.scope_number, c.scope_name ORDER BY c.scope_number"
        
        results = self.fetch_query(base_query, tuple(params))
        
        summary = {
            'scope_1': 0,
            'scope_2': 0,
            'scope_3': 0,
            'total': 0,
            'details': [],
            'entry_counts': {'scope_1': 0, 'scope_2': 0, 'scope_3': 0}
        }
        
        for row in results:
            scope_num = row[0]
            scope_name = row[1]
            emissions = float(row[2]) if row[2] else 0
            entry_count = row[3]
            
            summary['details'].append({
                'scope_number': scope_num,
                'scope_name': scope_name,
                'emissions': emissions,
                'entry_count': entry_count
            })
            
            if scope_num == 1:
                summary['scope_1'] = emissions
                summary['entry_counts']['scope_1'] = entry_count
            elif scope_num == 2:
                summary['scope_2'] = emissions
                summary['entry_counts']['scope_2'] = entry_count
            elif scope_num == 3:
                summary['scope_3'] = emissions
                summary['entry_counts']['scope_3'] = entry_count
            
            summary['total'] += emissions
        
        return summary

    def health_check(self) -> Dict[str, Any]:
        """Database health check for monitoring"""
        try:
            if self.connect():
                # Test basic query
                result = self.fetch_one("SELECT 1 as test")
                self.disconnect()
                
                if result and result[0] == 1:
                    return {
                        'status': 'healthy',
                        'timestamp': datetime.now().isoformat(),
                        'database': 'connected'
                    }
            
            return {
                'status': 'unhealthy',
                'timestamp': datetime.now().isoformat(),
                'database': 'connection_failed'
            }
        except Exception as e:
            return {
                'status': 'error',
                'timestamp': datetime.now().isoformat(),
                'error': str(e)
            }
