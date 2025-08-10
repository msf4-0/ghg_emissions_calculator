import streamlit as st
import sys
import os
from datetime import datetime
import logging

# Add the scripts directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import Config, setup_streamlit_config, validate_environment

# Initialize configuration
config = Config()
from database_operations import DatabaseManager
from authentication import AuthenticationManager, create_login_form, create_registration_form
from ghg_calculator import GHGCalculator, create_emissions_input_form
from data_visualization import DataVisualization, create_dashboard

# Setup logging
logging.basicConfig(
    level=logging.INFO if config.is_production else logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def initialize_app():
    """Initialize the application with proper configuration"""
    try:
        # Setup Streamlit configuration
        setup_streamlit_config()
        
        # Validate environment variables
        validate_environment()
        
        # Initialize session state
        initialize_session_state()
        
        logger.info("Application initialized successfully")
        return True
    except Exception as e:
        logger.error(f"Application initialization failed: {e}")
        st.error("Application initialization failed. Please contact support.")
        return False

def initialize_session_state():
    """Initialize session state variables"""
    default_values = {
        'user_authenticated': False,
        'user_data': None,
        'current_page': 'Login',
        'last_activity': datetime.now(),
        'session_id': None
    }
    
    for key, value in default_values.items():
        if key not in st.session_state:
            st.session_state[key] = value

def check_session_timeout():
    """Check for session timeout"""
    if 'last_activity' in st.session_state:
        timeout_duration = config.app_config['session_timeout']
        time_diff = (datetime.now() - st.session_state.last_activity).total_seconds()
        
        if time_diff > timeout_duration:
            # Session expired
            for key in ['user_authenticated', 'user_data']:
                if key in st.session_state:
                    del st.session_state[key]
            st.warning("Session expired. Please login again.")
            st.rerun()
        else:
            # Update last activity
            st.session_state.last_activity = datetime.now()

def create_sidebar_navigation(auth_manager: AuthenticationManager):
    """Create sidebar navigation with enhanced features"""
    st.sidebar.title("🌱 GHG Calculator")
    st.sidebar.markdown(f"**Version:** {config.app_config['app_version']}")
    
    if auth_manager.is_authenticated():
        user = auth_manager.get_current_user()
        
        # User info section
        with st.sidebar.expander("👤 User Information", expanded=False):
            st.write(f"**Username:** {user['username']}")
            st.write(f"**Role:** {user['role'].title()}")
            if user['company_name']:
                st.write(f"**Company:** {user['company_name']}")
                if user['company_verified']:
                    st.success("✅ Company Verified")
                else:
                    st.warning("⏳ Company Pending Verification")
        
        # Navigation menu
        menu_options = ["📊 Dashboard", "➕ Add Emissions", "📋 View Data"]
        
        if auth_manager.has_role('manager'):
            menu_options.append("🏢 Company Management")
        
        if auth_manager.has_role('admin'):
            menu_options.extend(["👥 User Management", "⚙️ System Settings"])
        
        selected_page = st.sidebar.selectbox("Navigate to:", menu_options)
        
        # Quick stats (if user has company)
        if user['company_id']:
            with st.sidebar.expander("📈 Quick Stats", expanded=False):
                try:
                    db_manager = DatabaseManager()
                    if db_manager.connect():
                        summary = db_manager.get_emissions_summary(
                            user['company_id'], "2024"
                        )
                        db_manager.disconnect()
                        
                        if summary['total'] > 0:
                            st.metric("Total 2024 Emissions", f"{summary['total']:.2f} kg CO2e")
                            st.metric("Scope 1", f"{summary['scope_1']:.2f} kg CO2e")
                            st.metric("Scope 2", f"{summary['scope_2']:.2f} kg CO2e")
                            st.metric("Scope 3", f"{summary['scope_3']:.2f} kg CO2e")
                        else:
                            st.info("No emission data for 2024")
                except Exception as e:
                    st.error("Unable to load stats")
        
        # Logout button
        if st.sidebar.button("🚪 Logout", type="secondary"):
            auth_manager.logout_user()
            st.rerun()
        
        return selected_page.split(" ", 1)[1]  # Remove emoji from page name
    else:
        st.sidebar.info("Please login to access the application")
        return "Login"

def create_company_management_page(db_manager: DatabaseManager, user_data: dict):
    """Enhanced company management page"""
    st.title("🏢 Company Management")
    
    tab1, tab2, tab3, tab4 = st.tabs([
        "⏳ Pending Verification", 
        "✅ Verified Companies", 
        "➕ Add New Company",
        "📊 Company Statistics"
    ])
    
    with tab1:
        st.subheader("Companies Pending Verification")
        if db_manager.connect():
            pending_companies = db_manager.get_companies(verification_status='pending')
            db_manager.disconnect()
            
            if pending_companies:
                for company in pending_companies:
                    with st.expander(f"🏢 {company['company_name']} ({company['company_code']})"):
                        col1, col2 = st.columns(2)
                        with col1:
                            st.write(f"**Industry:** {company['industry_sector'] or 'Not specified'}")
                            st.write(f"**Contact:** {company['contact_email'] or 'Not provided'}")
                            st.write(f"**Phone:** {company['contact_phone'] or 'Not provided'}")
                        with col2:
                            st.write(f"**Address:** {company['address'] or 'Not provided'}")
                            st.write(f"**Created:** {company['created_at'].strftime('%Y-%m-%d %H:%M') if company['created_at'] else 'Unknown'}")
                        
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            if st.button(f"✅ Verify", key=f"verify_{company['id']}", type="primary"):
                                if db_manager.connect():
                                    if db_manager.verify_company(company['id'], user_data['id'], 'verified'):
                                        st.success("Company verified successfully!")
                                        st.rerun()
                                    else:
                                        st.error("Failed to verify company")
                                    db_manager.disconnect()
                        with col2:
                            if st.button(f"❌ Reject", key=f"reject_{company['id']}", type="secondary"):
                                if db_manager.connect():
                                    if db_manager.verify_company(company['id'], user_data['id'], 'rejected'):
                                        st.success("Company rejected!")
                                        st.rerun()
                                    else:
                                        st.error("Failed to reject company")
                                    db_manager.disconnect()
                        with col3:
                            if st.button(f"📧 Contact", key=f"contact_{company['id']}", type="secondary"):
                                st.info(f"Contact: {company['contact_email'] or 'No email provided'}")
            else:
                st.info("✨ No companies pending verification.")
    
    with tab2:
        st.subheader("Verified Companies")
        if db_manager.connect():
            verified_companies = db_manager.get_companies(verification_status='verified')
            db_manager.disconnect()
            
            if verified_companies:
                # Search functionality
                search_term = st.text_input("🔍 Search companies...")
                
                filtered_companies = verified_companies
                if search_term:
                    filtered_companies = [
                        comp for comp in verified_companies 
                        if search_term.lower() in comp['company_name'].lower() or 
                           search_term.lower() in (comp['company_code'] or '').lower()
                    ]
                
                for company in filtered_companies:
                    with st.expander(f"🏢 {company['company_name']} ✅"):
                        col1, col2 = st.columns(2)
                        with col1:
                            st.write(f"**Code:** {company['company_code']}")
                            st.write(f"**Industry:** {company['industry_sector'] or 'Not specified'}")
                            st.write(f"**Contact:** {company['contact_email'] or 'Not provided'}")
                        with col2:
                            st.write(f"**Verified:** {company['verification_date'].strftime('%Y-%m-%d') if company['verification_date'] else 'Unknown'}")
                            st.write(f"**Address:** {company['address'] or 'Not provided'}")
            else:
                st.info("No verified companies found.")
    
    with tab3:
        st.subheader("Add New Company")
        with st.form("add_company_form"):
            col1, col2 = st.columns(2)
            with col1:
                company_name = st.text_input("Company Name *", help="Full legal company name")
                company_code = st.text_input("Company Code *", help="Unique identifier (e.g., COMP001)")
                industry_sector = st.selectbox("Industry Sector", [
                    "", "Technology", "Manufacturing", "Healthcare", "Finance", 
                    "Retail", "Energy", "Transportation", "Construction", "Other"
                ])
            with col2:
                contact_email = st.text_input("Contact Email", help="Primary contact email")
                contact_phone = st.text_input("Contact Phone", help="Primary contact phone")
                address = st.text_area("Address", help="Company address")
            
            auto_verify = st.checkbox("Auto-verify company", help="Automatically verify this company")
            
            if st.form_submit_button("➕ Add Company", type="primary"):
                if company_name and company_code:
                    if db_manager.connect():
                        success = db_manager.create_company(
                            company_name, company_code, industry_sector, 
                            address, contact_email, contact_phone, user_data['id']
                        )
                        
                        if success and auto_verify:
                            # Get the company ID and verify it
                            companies = db_manager.get_companies()
                            new_company = next((c for c in companies if c['company_code'] == company_code), None)
                            if new_company:
                                db_manager.verify_company(new_company['id'], user_data['id'], 'verified')
                        
                        db_manager.disconnect()
                        
                        if success:
                            st.success("✅ Company added successfully!")
                            if auto_verify:
                                st.success("✅ Company automatically verified!")
                        else:
                            st.error("❌ Failed to add company. Company code might already exist.")
                    else:
                        st.error("❌ Database connection failed")
                else:
                    st.error("❌ Please provide company name and code.")
    
    with tab4:
        st.subheader("Company Statistics")
        if db_manager.connect():
            all_companies = db_manager.get_companies()
            db_manager.disconnect()
            
            if all_companies:
                # Statistics
                total_companies = len(all_companies)
                verified_count = len([c for c in all_companies if c['verification_status'] == 'verified'])
                pending_count = len([c for c in all_companies if c['verification_status'] == 'pending'])
                rejected_count = len([c for c in all_companies if c['verification_status'] == 'rejected'])
                
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Total Companies", total_companies)
                with col2:
                    st.metric("Verified", verified_count)
                with col3:
                    st.metric("Pending", pending_count)
                with col4:
                    st.metric("Rejected", rejected_count)
                
                # Industry breakdown
                if verified_count > 0:
                    st.subheader("Industry Breakdown")
                    verified_companies = [c for c in all_companies if c['verification_status'] == 'verified']
                    industry_counts = {}
                    for company in verified_companies:
                        industry = company['industry_sector'] or 'Not Specified'
                        industry_counts[industry] = industry_counts.get(industry, 0) + 1
                    
                    import plotly.express as px
                    import pandas as pd
                    
                    df = pd.DataFrame(list(industry_counts.items()), columns=['Industry', 'Count'])
                    fig = px.pie(df, values='Count', names='Industry', title="Companies by Industry")
                    st.plotly_chart(fig, use_container_width=True)

def create_user_management_page(db_manager: DatabaseManager):
    """Enhanced user management page (admin only)"""
    st.title("👥 User Management")
    
    tab1, tab2, tab3 = st.tabs(["👀 View Users", "➕ Add New User", "📊 User Statistics"])
    
    with tab1:
        st.subheader("All Users")
        if db_manager.connect():
            users = db_manager.get_users()
            db_manager.disconnect()
            
            if users:
                # Search and filter
                col1, col2 = st.columns(2)
                with col1:
                    search_term = st.text_input("🔍 Search users...")
                with col2:
                    role_filter = st.selectbox("Filter by role", ["All", "admin", "manager", "normal_user"])
                
                # Filter users
                filtered_users = users
                if search_term:
                    filtered_users = [
                        user for user in filtered_users 
                        if search_term.lower() in user['username'].lower() or 
                           search_term.lower() in user['email'].lower()
                    ]
                
                if role_filter != "All":
                    filtered_users = [user for user in filtered_users if user['role'] == role_filter]
                
                # Display users
                import pandas as pd
                df = pd.DataFrame(filtered_users)
                
                # Format the dataframe for better display
                if not df.empty:
                    df['created_at'] = pd.to_datetime(df['created_at']).dt.strftime('%Y-%m-%d %H:%M')
                    df['is_active'] = df['is_active'].map({True: '✅ Active', False: '❌ Inactive'})
                    df = df[['username', 'email', 'role', 'company_name', 'created_at', 'is_active']]
                    df.columns = ['Username', 'Email', 'Role', 'Company', 'Created', 'Status']
                    
                    st.dataframe(df, use_container_width=True)
                else:
                    st.info("No users found matching the criteria.")
            else:
                st.info("No users found.")
    
    with tab2:
        create_registration_form(db_manager)
    
    with tab3:
        st.subheader("User Statistics")
        if db_manager.connect():
            users = db_manager.get_users()
            db_manager.disconnect()
            
            if users:
                # Role distribution
                role_counts = {}
                for user in users:
                    role = user['role']
                    role_counts[role] = role_counts.get(role, 0) + 1
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Admin Users", role_counts.get('admin', 0))
                with col2:
                    st.metric("Manager Users", role_counts.get('manager', 0))
                with col3:
                    st.metric("Normal Users", role_counts.get('normal_user', 0))
                
                # Activity chart
                import plotly.express as px
                import pandas as pd
                
                df = pd.DataFrame(list(role_counts.items()), columns=['Role', 'Count'])
                fig = px.bar(df, x='Role', y='Count', title="User Distribution by Role")
                st.plotly_chart(fig, use_container_width=True)

def create_system_settings_page():
    """System settings page (admin only)"""
    st.title("⚙️ System Settings")
    
    tab1, tab2, tab3 = st.tabs(["🔧 Configuration", "📊 Health Check", "📋 Audit Trail"])
    
    with tab1:
        st.subheader("System Configuration")
        
        col1, col2 = st.columns(2)
        with col1:
            st.info("**Environment**")
            st.write(f"Mode: {config.environment}")
            st.write(f"Debug: {config.app_config['debug']}")
            st.write(f"Version: {config.app_config['app_version']}")
        
        with col2:
            st.info("**Security Settings**")
            st.write(f"Session Timeout: {config.app_config['session_timeout']} seconds")
            st.write(f"Max File Size: {config.app_config['max_file_size']} bytes")
            st.write(f"Password Min Length: {config.security_config['password_min_length']}")
    
    with tab2:
        st.subheader("System Health Check")
        
        if st.button("🔍 Run Health Check", type="primary"):
            with st.spinner("Running health check..."):
                db_manager = DatabaseManager()
                health_status = db_manager.health_check()
                
                if health_status['status'] == 'healthy':
                    st.success("✅ System is healthy")
                    st.json(health_status)
                else:
                    st.error("❌ System health issues detected")
                    st.json(health_status)
    
    with tab3:
        st.subheader("Audit Trail")
        st.info("Audit trail functionality will be implemented here.")
        st.write("This section will show system activity logs, user actions, and security events.")

def main():
    """Main application function with error handling"""
    try:
        # Initialize application
        if not initialize_app():
            return
        
        # Check session timeout
        check_session_timeout()
        
        # Initialize managers
        db_manager = DatabaseManager()
        auth_manager = AuthenticationManager(db_manager)
        calculator = GHGCalculator(db_manager)
        
        # Navigation
        selected_page = create_sidebar_navigation(auth_manager)
        
        # Page routing with error handling
        try:
            if selected_page == "Login":
                st.title("🌱 GHG Emission Calculator")
                st.markdown("### Greenhouse Gas Emission Tracking and Reporting System")
                st.markdown("---")
                
                col1, col2 = st.columns([2, 1])
                with col1:
                    st.markdown("""
                    **Features:**
                    - ✅ Complete GHG Protocol compliance (Scope 1, 2, 3)
                    - ✅ UK emission factors database
                    - ✅ Role-based access control
                    - ✅ Company verification system
                    - ✅ Interactive data visualization
                    - ✅ Comprehensive reporting
                    """)
                
                with col2:
                    tab1, tab2 = st.tabs(["🔐 Login", "📝 Register"])
                    with tab1:
                        create_login_form(auth_manager)
                    with tab2:
                        create_registration_form(db_manager)
            
            elif selected_page == "Dashboard":
                auth_manager.require_authentication()
                create_dashboard(db_manager, auth_manager.get_current_user())
            
            elif selected_page == "Add Emissions":
                auth_manager.require_company_verification()
                create_emissions_input_form(db_manager, calculator, auth_manager.get_current_user())
            
            elif selected_page == "View Data":
                auth_manager.require_authentication()
                user = auth_manager.get_current_user()
                
                st.title("📋 Emissions Data")
                
                # Enhanced filters
                col1, col2, col3 = st.columns(3)
                with col1:
                    periods = ["All", "2024", "2023", "2022", "Q4-2024", "Q3-2024", "Q2-2024", "Q1-2024"]
                    selected_period = st.selectbox("📅 Reporting Period", periods)
                    period_filter = None if selected_period == "All" else selected_period
                
                with col2:
                    scopes = ["All", "Scope 1", "Scope 2", "Scope 3"]
                    selected_scope = st.selectbox("🎯 Scope Filter", scopes)
                
                with col3:
                    page_size = st.selectbox("📄 Items per page", [10, 25, 50, 100])
                
                # Get and display data
                if db_manager.connect():
                    company_id = user['company_id'] if user['role'] != 'admin' else None
                    emissions_data = db_manager.get_emissions_data(
                        company_id, period_filter, limit=page_size
                    )
                    db_manager.disconnect()
                    
                    # Filter by scope if selected
                    if selected_scope != "All":
                        scope_num = int(selected_scope.split()[1])
                        emissions_data = [e for e in emissions_data if e['scope_number'] == scope_num]
                    
                    viz = DataVisualization(db_manager)
                    viz.display_data_table(emissions_data, f"Emissions Data ({len(emissions_data)} records)")
                else:
                    st.error("❌ Database connection failed")
            
            elif selected_page == "Company Management":
                auth_manager.require_role('manager')
                create_company_management_page(db_manager, auth_manager.get_current_user())
            
            elif selected_page == "User Management":
                auth_manager.require_role('admin')
                create_user_management_page(db_manager)
            
            elif selected_page == "System Settings":
                auth_manager.require_role('admin')
                create_system_settings_page()
            
        except Exception as page_error:
            logger.error(f"Page error: {page_error}")
            st.error("An error occurred while loading the page. Please try again.")
            if not config.is_production:
                st.exception(page_error)
    
    except Exception as app_error:
        logger.error(f"Application error: {app_error}")
        st.error("A critical error occurred. Please contact support.")
        if not config.is_production:
            st.exception(app_error)

if __name__ == "__main__":
    main()
