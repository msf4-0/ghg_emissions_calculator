from typing import Dict, List, Tuple
from database_operations import DatabaseManager
import pandas as pd

class GHGCalculator:
    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager
    
    def calculate_emissions(self, category_id: int, activity_data: float, 
                          custom_emission_factor: float = None) -> Tuple[float, Dict]:
        """Calculate CO2 equivalent emissions"""
        if not self.db.connect():
            return 0.0, {}
        
        # Get category details
        category_query = "SELECT * FROM ghg_categories WHERE id = %s"
        category_result = self.db.fetch_one(category_query, (category_id,))
        
        if not category_result:
            self.db.disconnect()
            return 0.0, {}
        
        category_data = {
            'id': category_result[0],
            'scope_number': category_result[1],
            'scope_name': category_result[2],
            'category_code': category_result[3],
            'category_name': category_result[4],
            'subcategory_code': category_result[5],
            'subcategory_name': category_result[6],
            'emission_factor': float(category_result[7]) if category_result[7] else 0.0,
            'unit': category_result[8],
            'description': category_result[9]
        }
        
        self.db.disconnect()
        
        # Use custom emission factor if provided, otherwise use default
        emission_factor = custom_emission_factor if custom_emission_factor is not None else category_data['emission_factor']
        
        # Calculate CO2 equivalent
        co2_equivalent = activity_data * emission_factor
        
        calculation_details = {
            'activity_data': activity_data,
            'emission_factor': emission_factor,
            'co2_equivalent': co2_equivalent,
            'category': category_data,
            'calculation_method': 'Activity Data × Emission Factor'
        }
        
        return co2_equivalent, calculation_details
    
    def get_scope_totals(self, company_id: int, reporting_period: str) -> Dict:
        """Get total emissions by scope for a company and period"""
        if not self.db.connect():
            return {}
        
        summary = self.db.get_emissions_summary(company_id, reporting_period)
        self.db.disconnect()
        
        return summary
    
    def get_category_breakdown(self, company_id: int, reporting_period: str) -> List[Dict]:
        """Get detailed breakdown by category"""
        if not self.db.connect():
            return []
        
        query = """
        SELECT 
            c.scope_number,
            c.scope_name,
            c.category_name,
            c.subcategory_name,
            SUM(e.activity_data) as total_activity,
            AVG(e.emission_factor) as avg_emission_factor,
            SUM(e.co2_equivalent) as total_emissions,
            c.unit,
            COUNT(e.id) as entry_count
        FROM emissions_data e
        JOIN ghg_categories c ON e.category_id = c.id
        WHERE e.company_id = %s AND e.reporting_period = %s
        GROUP BY c.id, c.scope_number, c.scope_name, c.category_name, c.subcategory_name, c.unit
        ORDER BY c.scope_number, c.category_name, c.subcategory_name
        """
        
        results = self.db.fetch_query(query, (company_id, reporting_period))
        self.db.disconnect()
        
        breakdown = []
        for row in results:
            breakdown.append({
                'scope_number': row[0],
                'scope_name': row[1],
                'category_name': row[2],
                'subcategory_name': row[3],
                'total_activity': float(row[4]),
                'avg_emission_factor': float(row[5]),
                'total_emissions': float(row[6]),
                'unit': row[7],
                'entry_count': row[8]
            })
        
        return breakdown
    
    def validate_activity_data(self, activity_data: float, category_id: int) -> Tuple[bool, str]:
        """Validate activity data input"""
        if activity_data < 0:
            return False, "Activity data cannot be negative"
        
        if activity_data == 0:
            return False, "Activity data cannot be zero"
        
        # Add more specific validations based on category if needed
        return True, "Valid"
    
    def get_emission_factors_by_scope(self, scope: int) -> List[Dict]:
        """Get all emission factors for a specific scope"""
        if not self.db.connect():
            return []
        
        categories = self.db.get_ghg_categories(scope)
        self.db.disconnect()
        
        return categories
    
    def calculate_percentage_by_scope(self, emissions_summary: Dict) -> Dict:
        """Calculate percentage contribution by scope"""
        total = emissions_summary.get('total', 0)
        if total == 0:
            return {'scope_1_pct': 0, 'scope_2_pct': 0, 'scope_3_pct': 0}
        
        return {
            'scope_1_pct': (emissions_summary.get('scope_1', 0) / total) * 100,
            'scope_2_pct': (emissions_summary.get('scope_2', 0) / total) * 100,
            'scope_3_pct': (emissions_summary.get('scope_3', 0) / total) * 100
        }

def create_emissions_input_form(db_manager: DatabaseManager, calculator: GHGCalculator, 
                               user_data: Dict):
    """Create form for inputting emissions data"""
    import streamlit as st
    
    st.subheader("Add Emission Data")
    
    # Add a button to refresh categories if needed
    if st.button("🔄 Refresh Categories", help="Click if categories don't appear correctly"):
        st.cache_data.clear()
        st.rerun()
    
    # Get categories for selection
    if db_manager.connect():
        all_categories = db_manager.get_ghg_categories()
        db_manager.disconnect()
        
        # Debug: Show what we actually got from database (simplified)
        if len(all_categories) > 0:
            st.info(f"📊 Database contains {len(all_categories)} total emission categories")
        else:
            st.error("No categories found in database")
        
    else:
        st.error("Database connection failed")
        return
    
    if not all_categories:
        st.error("No GHG categories found. Please contact your administrator.")
        return
    
    # Organize categories by scope
    scope_categories = {}
    for cat in all_categories:
        scope_key = f"Scope {cat['scope_number']}"
        if scope_key not in scope_categories:
            scope_categories[scope_key] = []
        scope_categories[scope_key].append(cat)
    
    # Create two columns for layout
    col1, col2 = st.columns(2)
    
    # Initialize variables
    selected_category = None
    selected_category_id = None
    
    with col1:
        reporting_period = st.selectbox(
            "Reporting Period",
            ["2024", "2023", "2022", "Q4-2024", "Q3-2024", "Q2-2024", "Q1-2024"]
        )
        
        # Show available scopes
        scope_options = list(scope_categories.keys())
        selected_scope = st.selectbox("Select Scope", scope_options)
        
        # Show category count for selected scope
        if selected_scope in scope_categories:
            st.info(f"� {len(scope_categories[selected_scope])} categories available in {selected_scope}")
            
            # Create category options for the selected scope
            category_options = []
            category_ids = []
            
            for cat in scope_categories[selected_scope]:
                display_name = f"{cat['category_name']} - {cat['subcategory_name']}"
                category_options.append(display_name)
                category_ids.append(cat['id'])
            
            if category_options:
                # Show available categories count
                if len(category_options) != len(scope_categories[selected_scope]):
                    st.warning(f"⚠️ Showing {len(category_options)} of {len(scope_categories[selected_scope])} categories")
                
                # Use a simpler key structure to avoid JS conflicts
                category_selectbox_key = f"cat_sel_{selected_scope.replace(' ', '_').replace('-', '_')}"
                
                selected_category_display = st.selectbox(
                    "Select Category",
                    category_options,
                    key=category_selectbox_key,
                    help=f"Choose from {len(category_options)} available categories",
                    label_visibility="visible"
                )
                
                # Find the selected category ID
                selected_index = category_options.index(selected_category_display)
                selected_category_id = category_ids[selected_index]
                selected_category = next((cat for cat in all_categories if cat['id'] == selected_category_id), None)
                
                if selected_category:
                    st.success(f"✅ Selected: {selected_category['subcategory_name']}")
            else:
                st.warning(f"No categories available for {selected_scope}")
        else:
            st.error("Invalid scope selection")
    
    with col2:
        if selected_category:
            activity_data = st.number_input(
                f"Activity Data ({selected_category['unit']})",
                min_value=0.0,
                step=0.01,
                format="%.4f"
            )
            
            # Show default emission factor but allow override
            default_ef = selected_category['emission_factor']
            st.info(f"Default Emission Factor: {default_ef} kg CO2e/{selected_category['unit']}")
            
            use_custom_ef = st.checkbox("Use Custom Emission Factor")
            if use_custom_ef:
                emission_factor = st.number_input(
                    "Custom Emission Factor",
                    min_value=0.0,
                    value=float(default_ef),
                    step=0.000001,
                    format="%.6f"
                )
            else:
                emission_factor = default_ef
        else:
            st.info("Select a scope and category first to input activity data.")
            activity_data = 0.0
            emission_factor = 0.0
            use_custom_ef = False
    
    # Additional fields
    data_source = st.text_input("Data Source (optional)")
    calculation_method = st.text_input("Calculation Method (optional)", value="Activity Data × Emission Factor")
    notes = st.text_area("Notes (optional)")
    
    # Submit button
    if st.button("Calculate and Add Emission Data", type="primary"):
        if not selected_category:
            st.error("❌ Please select a scope and category before submitting.")
        elif activity_data <= 0:
            st.error("❌ Please enter valid activity data (greater than 0).")
        else:
            # Calculate emissions
            custom_ef = emission_factor if use_custom_ef else None
            co2_equivalent, calc_details = calculator.calculate_emissions(
                selected_category_id, activity_data, custom_ef
            )
            
            # Display calculation results
            st.success(f"Calculated CO2 Equivalent: {co2_equivalent:.4f} kg CO2e")
            
            with st.expander("Calculation Details"):
                st.write(f"**Category:** {calc_details['category']['subcategory_name']}")
                st.write(f"**Activity Data:** {calc_details['activity_data']} {calc_details['category']['unit']}")
                st.write(f"**Emission Factor:** {calc_details['emission_factor']}")
                if use_custom_ef:
                    st.write("**Note:** Using custom emission factor")
                else:
                    st.write("**Note:** Using default emission factor")
                st.write(f"**CO2 Equivalent:** {calc_details['co2_equivalent']:.4f} kg CO2e")
                st.write(f"**Method:** {calc_details['calculation_method']}")
            
            # Save to database
            if db_manager.connect():
                success = db_manager.add_emission_data(
                    company_id=user_data['company_id'],
                    user_id=user_data['id'],
                    category_id=selected_category_id,
                    reporting_period=reporting_period,
                    activity_data=activity_data,
                    emission_factor=calc_details['emission_factor'],
                    data_source=data_source,
                    calculation_method=calculation_method,
                    notes=notes
                )
                db_manager.disconnect()
                
                if success:
                    st.success("✅ Emission data saved successfully!")
                    st.balloons()
                else:
                    st.error("❌ Failed to save emission data")
            else:
                st.error("❌ Database connection failed")
