import streamlit as st
from database_operations import DatabaseManager
from authentication import AuthenticationManager, create_login_form, create_registration_form
from ghg_calculator import GHGCalculator, create_emissions_input_form
from data_visualization import DataVisualization, create_dashboard

# Configuration
DB_CONFIG = {
    'host': 'localhost',
    'database': 'ghg_emissions_db',
    'user': 'root',
    'password': ''  # Update with your MySQL password
}

def initialize_session_state():
    """Initialize session state variables"""
    if 'user_authenticated' not in st.session_state:
        st.session_state.user_authenticated = False
    if 'user_data' not in st.session_state:
        st.session_state.user_data = None

def create_sidebar_navigation(auth_manager: AuthenticationManager):
    """Create sidebar navigation"""
    st.sidebar.title("GHG Emission Calculator")
    
    if auth_manager.is_authenticated():
        user = auth_manager.get_current_user()
        st.sidebar.success(f"Welcome, {user['username']}!")
        st.sidebar.info(f"Role: {user['role'].title()}")
        if user['company_name']:
            st.sidebar.info(f"Company: {user['company_name']}")
        
        # Navigation menu
        menu_options = ["Dashboard", "Add Emissions", "View Data"]
        
        if auth_manager.has_role('manager'):
            menu_options.append("Company Management")
        
        if auth_manager.has_role('admin'):
            menu_options.extend(["User Management", "System Settings"])
        
        selected_page = st.sidebar.selectbox("Navigate to:", menu_options)
        
        if st.sidebar.button("Logout"):
            auth_manager.logout_user()
            st.rerun()
        
        return selected_page
    else:
        return "Login"

def create_company_management_page(db_manager: DatabaseManager, user_data: dict):
    """Create company management page"""
    st.title("Company Management")
    
    tab1, tab2, tab3 = st.tabs(["Pending Verification", "Verified Companies", "Add New Company"])
    
    with tab1:
        st.subheader("Companies Pending Verification")
        if db_manager.connect():
            pending_companies = db_manager.get_companies(verification_status='pending')
            db_manager.disconnect()
            
            if pending_companies:
                for company in pending_companies:
                    with st.expander(f"{company['company_name']} ({company['company_code']})"):
                        col1, col2 = st.columns(2)
                        with col1:
                            st.write(f"**Industry:** {company['industry_sector']}")
                            st.write(f"**Contact:** {company['contact_email']}")
                            st.write(f"**Phone:** {company['contact_phone']}")
                        with col2:
                            st.write(f"**Address:** {company['address']}")
                            st.write(f"**Created:** {company['created_at']}")
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            if st.button(f"Verify {company['company_name']}", key=f"verify_{company['id']}"):
                                if db_manager.connect():
                                    if db_manager.verify_company(company['id'], user_data['id'], 'verified'):
                                        st.success("Company verified successfully!")
                                        st.rerun()
                                    db_manager.disconnect()
                        with col2:
                            if st.button(f"Reject {company['company_name']}", key=f"reject_{company['id']}"):
                                if db_manager.connect():
                                    if db_manager.verify_company(company['id'], user_data['id'], 'rejected'):
                                        st.success("Company rejected!")
                                        st.rerun()
                                    db_manager.disconnect()
            else:
                st.info("No companies pending verification.")
    
    with tab2:
        st.subheader("Verified Companies")
        if db_manager.connect():
            verified_companies = db_manager.get_companies(verification_status='verified')
            db_manager.disconnect()
            
            if verified_companies:
                for company in verified_companies:
                    with st.expander(f"{company['company_name']} ✅"):
                        st.write(f"**Code:** {company['company_code']}")
                        st.write(f"**Industry:** {company['industry_sector']}")
                        st.write(f"**Verified:** {company['verification_date']}")
            else:
                st.info("No verified companies found.")
    
    with tab3:
        st.subheader("Add New Company")
        with st.form("add_company_form"):
            col1, col2 = st.columns(2)
            with col1:
                company_name = st.text_input("Company Name")
                company_code = st.text_input("Company Code")
                industry_sector = st.text_input("Industry Sector")
            with col2:
                contact_email = st.text_input("Contact Email")
                contact_phone = st.text_input("Contact Phone")
                address = st.text_area("Address")
            
            if st.form_submit_button("Add Company"):
                if company_name and company_code:
                    if db_manager.connect():
                        if db_manager.create_company(company_name, company_code, industry_sector, 
                                                   address, contact_email, contact_phone):
                            st.success("Company added successfully!")
                        else:
                            st.error("Failed to add company. Company code might already exist.")
                        db_manager.disconnect()
                else:
                    st.error("Please provide company name and code.")

def create_user_management_page(db_manager: DatabaseManager):
    """Create user management page (admin only)"""
    st.title("User Management")
    
    tab1, tab2 = st.tabs(["View Users", "Add New User"])
    
    with tab1:
        st.subheader("All Users")
        if db_manager.connect():
            users = db_manager.get_users()
            db_manager.disconnect()
            
            if users:
                import pandas as pd
                df = pd.DataFrame(users)
                st.dataframe(df, use_container_width=True)
            else:
                st.info("No users found.")
    
    with tab2:
        create_registration_form(db_manager)

def main():
    """Main application function"""
    st.set_page_config(
        page_title="GHG Emission Calculator",
        page_icon="🌱",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Initialize
    initialize_session_state()
    db_manager = DatabaseManager(**DB_CONFIG)
    auth_manager = AuthenticationManager(db_manager)
    calculator = GHGCalculator(db_manager)
    
    # Navigation
    selected_page = create_sidebar_navigation(auth_manager)
    
    # Page routing
    if selected_page == "Login":
        st.title("GHG Emission Calculator")
        st.markdown("### Greenhouse Gas Emission Tracking and Reporting System")
        
        tab1, tab2 = st.tabs(["Login", "Register"])
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
        
        st.title("Emissions Data")
        
        # Filters
        col1, col2 = st.columns(2)
        with col1:
            periods = ["All", "2024", "2023", "2022", "Q4-2024", "Q3-2024"]
            selected_period = st.selectbox("Reporting Period", periods)
            period_filter = None if selected_period == "All" else selected_period
        
        # Get and display data
        if db_manager.connect():
            company_id = user['company_id'] if user['role'] != 'admin' else None
            emissions_data = db_manager.get_emissions_data(company_id, period_filter)
            db_manager.disconnect()
            
            viz = DataVisualization(db_manager)
            viz.display_data_table(emissions_data)
        else:
            st.error("Database connection failed")
    
    elif selected_page == "Company Management":
        auth_manager.require_role('manager')
        create_company_management_page(db_manager, auth_manager.get_current_user())
    
    elif selected_page == "User Management":
        auth_manager.require_role('admin')
        create_user_management_page(db_manager)
    
    elif selected_page == "System Settings":
        auth_manager.require_role('admin')
        st.title("System Settings")
        st.info("System settings and configuration options will be implemented here.")

if __name__ == "__main__":
    main()
