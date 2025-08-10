import streamlit as st
from database_operations import DatabaseManager
from typing import Optional, Dict

class AuthenticationManager:
    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager
    
    def login_user(self, username: str, password: str) -> bool:
        """Login user and store session data"""
        if not self.db.connect():
            st.error("Database connection failed")
            return False
        
        user_data = self.db.authenticate_user(username, password)
        self.db.disconnect()
        
        if user_data:
            # Store user data in session state
            st.session_state.user_authenticated = True
            st.session_state.user_data = user_data
            return True
        return False
    
    def logout_user(self):
        """Logout user and clear session data"""
        for key in ['user_authenticated', 'user_data']:
            if key in st.session_state:
                del st.session_state[key]
    
    def is_authenticated(self) -> bool:
        """Check if user is authenticated"""
        return st.session_state.get('user_authenticated', False)
    
    def get_current_user(self) -> Optional[Dict]:
        """Get current user data"""
        if self.is_authenticated():
            return st.session_state.get('user_data')
        return None
    
    def has_role(self, required_role: str) -> bool:
        """Check if current user has required role"""
        user = self.get_current_user()
        if not user:
            return False
        
        role_hierarchy = {
            'admin': 3,
            'manager': 2,
            'normal_user': 1
        }
        
        user_level = role_hierarchy.get(user['role'], 0)
        required_level = role_hierarchy.get(required_role, 0)
        
        return user_level >= required_level
    
    def require_authentication(self):
        """Decorator-like function to require authentication"""
        if not self.is_authenticated():
            st.warning("Please login to access this page")
            st.stop()
    
    def require_role(self, required_role: str):
        """Require specific role"""
        self.require_authentication()
        if not self.has_role(required_role):
            st.error(f"Access denied. {required_role.title()} role required.")
            st.stop()
    
    def require_company_verification(self):
        """Require company to be verified"""
        self.require_authentication()
        user = self.get_current_user()
        if not user.get('company_verified', False):
            st.warning("Your company needs to be verified before you can add emission data.")
            st.stop()

def create_login_form(auth_manager: AuthenticationManager):
    """Create login form"""
    st.subheader("Login")
    
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit_button = st.form_submit_button("Login")
        
        if submit_button:
            if username and password:
                if auth_manager.login_user(username, password):
                    st.success("Login successful!")
                    st.rerun()
                else:
                    st.error("Invalid username or password")
            else:
                st.error("Please enter both username and password")

def create_registration_form(db_manager: DatabaseManager):
    """Create user registration form"""
    st.subheader("Register New User")
    
    # Display password requirements
    with st.expander("📋 Password Requirements", expanded=False):
        st.write("Your password must meet the following requirements:")
        st.write("• At least 8 characters long")
        st.write("• Include at least one special character: !@#$%^&*()_+-=[]{}|;:,.<>?")
        st.write("• Example: `MyPassword123!`")
    
    with st.form("registration_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            username = st.text_input("Username *")
            email = st.text_input("Email *")
            password = st.text_input("Password *", type="password", help="Must be at least 8 characters with special characters")
        
        with col2:
            role = st.selectbox("Role", ["normal_user", "manager", "admin"])
            
            # Get companies for selection
            company_id = None
            try:
                if db_manager.connect():
                    companies = db_manager.get_companies(verification_status='verified')
                    db_manager.disconnect()
                    
                    if companies:
                        company_options = {comp['company_name']: comp['id'] for comp in companies}
                        company_options['None (No Company)'] = None
                        
                        selected_company = st.selectbox("Company", list(company_options.keys()))
                        company_id = company_options[selected_company]
                    else:
                        st.warning("No verified companies available")
                else:
                    st.error("Cannot load companies - database connection failed")
            except Exception as e:
                st.error(f"Error loading companies: {e}")
        
        submit_button = st.form_submit_button("Register")
        
        if submit_button:
            if username and email and password:
                try:
                    if db_manager.connect():
                        success = db_manager.create_user(username, email, password, role, company_id)
                        db_manager.disconnect()
                        
                        if success:
                            st.success("✅ User registered successfully!")
                            st.info("You can now login with your credentials.")
                        else:
                            st.error("❌ Registration failed. This could be because:")
                            st.write("• Username or email already exists")
                            st.write("• Password doesn't meet requirements")
                            st.write("• Database error occurred")
                    else:
                        st.error("❌ Database connection failed")
                except Exception as e:
                    st.error(f"❌ Registration error: {e}")
            else:
                st.error("❌ Please fill in all required fields marked with *")
