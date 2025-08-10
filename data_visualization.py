import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from typing import Dict, List
from database_operations import DatabaseManager
from ghg_calculator import GHGCalculator

class DataVisualization:
    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager
    
    def create_scope_pie_chart(self, emissions_summary: Dict, title: str = "GHG Emissions by Scope"):
        """Create pie chart showing emissions by scope"""
        if not emissions_summary or emissions_summary['total'] == 0:
            st.warning("No emission data available for visualization")
            return
        
        # Prepare data for pie chart
        scopes = []
        values = []
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1']  # Red, Teal, Blue
        
        for detail in emissions_summary['details']:
            scopes.append(f"Scope {detail['scope_number']}")
            values.append(detail['emissions'])
        
        # Create pie chart
        fig = px.pie(
            values=values,
            names=scopes,
            title=title,
            color_discrete_sequence=colors
        )
        
        fig.update_traces(
            textposition='inside',
            textinfo='percent+label',
            hovertemplate='<b>%{label}</b><br>Emissions: %{value:.2f} kg CO2e<br>Percentage: %{percent}<extra></extra>'
        )
        
        fig.update_layout(
            showlegend=True,
            height=500,
            font=dict(size=12)
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Display summary statistics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Scope 1", f"{emissions_summary['scope_1']:.2f} kg CO2e")
        with col2:
            st.metric("Scope 2", f"{emissions_summary['scope_2']:.2f} kg CO2e")
        with col3:
            st.metric("Scope 3", f"{emissions_summary['scope_3']:.2f} kg CO2e")
        with col4:
            st.metric("Total", f"{emissions_summary['total']:.2f} kg CO2e")
    
    def create_category_bar_chart(self, category_breakdown: List[Dict], title: str = "Emissions by Category"):
        """Create bar chart showing emissions by category"""
        if not category_breakdown:
            st.warning("No category data available for visualization")
            return
        
        # Prepare data
        df = pd.DataFrame(category_breakdown)
        
        # Create combined category names
        df['full_category'] = df['category_name'] + ' - ' + df['subcategory_name']
        df['scope_label'] = 'Scope ' + df['scope_number'].astype(str)
        
        # Create bar chart
        fig = px.bar(
            df,
            x='full_category',
            y='total_emissions',
            color='scope_label',
            title=title,
            labels={
                'full_category': 'Category',
                'total_emissions': 'CO2 Equivalent (kg)',
                'scope_label': 'Scope'
            },
            color_discrete_map={
                'Scope 1': '#FF6B6B',
                'Scope 2': '#4ECDC4',
                'Scope 3': '#45B7D1'
            }
        )
        
        fig.update_layout(
            xaxis_tickangle=-45,
            height=600,
            showlegend=True,
            xaxis_title="Categories",
            yaxis_title="CO2 Equivalent (kg)"
        )
        
        fig.update_traces(
            hovertemplate='<b>%{x}</b><br>Emissions: %{y:.2f} kg CO2e<extra></extra>'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    def create_time_series_chart(self, company_id: int, periods: List[str]):
        """Create time series chart showing emissions over time"""
        if not self.db.connect():
            st.error("Database connection failed")
            return
        
        time_data = []
        for period in periods:
            summary = self.db.get_emissions_summary(company_id, period)
            if summary['total'] > 0:
                time_data.append({
                    'period': period,
                    'scope_1': summary['scope_1'],
                    'scope_2': summary['scope_2'],
                    'scope_3': summary['scope_3'],
                    'total': summary['total']
                })
        
        self.db.disconnect()
        
        if not time_data:
            st.warning("No time series data available")
            return
        
        df = pd.DataFrame(time_data)
        
        # Create line chart
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=df['period'],
            y=df['scope_1'],
            mode='lines+markers',
            name='Scope 1',
            line=dict(color='#FF6B6B', width=3),
            marker=dict(size=8)
        ))
        
        fig.add_trace(go.Scatter(
            x=df['period'],
            y=df['scope_2'],
            mode='lines+markers',
            name='Scope 2',
            line=dict(color='#4ECDC4', width=3),
            marker=dict(size=8)
        ))
        
        fig.add_trace(go.Scatter(
            x=df['period'],
            y=df['scope_3'],
            mode='lines+markers',
            name='Scope 3',
            line=dict(color='#45B7D1', width=3),
            marker=dict(size=8)
        ))
        
        fig.add_trace(go.Scatter(
            x=df['period'],
            y=df['total'],
            mode='lines+markers',
            name='Total',
            line=dict(color='#2C3E50', width=4, dash='dash'),
            marker=dict(size=10)
        ))
        
        fig.update_layout(
            title="GHG Emissions Trend Over Time",
            xaxis_title="Reporting Period",
            yaxis_title="CO2 Equivalent (kg)",
            height=500,
            hovermode='x unified'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    def create_comparison_chart(self, companies_data: List[Dict]):
        """Create comparison chart between companies"""
        if not companies_data:
            st.warning("No comparison data available")
            return
        
        df = pd.DataFrame(companies_data)
        
        fig = px.bar(
            df,
            x='company_name',
            y=['scope_1', 'scope_2', 'scope_3'],
            title="Company Emissions Comparison",
            labels={'value': 'CO2 Equivalent (kg)', 'company_name': 'Company'},
            color_discrete_map={
                'scope_1': '#FF6B6B',
                'scope_2': '#4ECDC4',
                'scope_3': '#45B7D1'
            }
        )
        
        fig.update_layout(
            barmode='stack',
            height=500,
            xaxis_tickangle=-45
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    def display_data_table(self, emissions_data: List[Dict], title: str = "Emissions Data"):
        """Display emissions data in a formatted table"""
        if not emissions_data:
            st.warning("No data available")
            return
        
        # Prepare data for display
        display_data = []
        for item in emissions_data:
            display_data.append({
                'Date': item['created_at'].strftime('%Y-%m-%d') if item['created_at'] else 'N/A',
                'Period': item['reporting_period'],
                'Scope': f"Scope {item['scope_number']}",
                'Category': item['subcategory_name'],
                'Activity Data': f"{item['activity_data']:.4f}",
                'Unit': item['unit'],
                'Emission Factor': f"{item['emission_factor']:.6f}",
                'CO2 Equivalent': f"{item['co2_equivalent']:.4f} kg",
                'Status': item['verification_status'].title(),
                'Company': item['company_name']
            })
        
        df = pd.DataFrame(display_data)
        
        st.subheader(title)
        st.dataframe(df, use_container_width=True)
        
        # Add download button
        csv = df.to_csv(index=False)
        st.download_button(
            label="Download as CSV",
            data=csv,
            file_name=f"emissions_data_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )

def create_dashboard(db_manager: DatabaseManager, user_data: Dict):
    """Create main dashboard with visualizations"""
    st.title("GHG Emissions Dashboard")
    
    # Filters
    col1, col2 = st.columns(2)
    with col1:
        reporting_periods = ["2024", "2023", "2022", "Q4-2024", "Q3-2024", "Q2-2024", "Q1-2024"]
        selected_period = st.selectbox("Select Reporting Period", reporting_periods)
    
    with col2:
        if user_data['role'] == 'admin':
            # Admin can see all companies
            if db_manager.connect():
                companies = db_manager.get_companies(verification_status='verified')
                db_manager.disconnect()
                
                company_options = {comp['company_name']: comp['id'] for comp in companies}
                company_options['All Companies'] = None
                
                selected_company_name = st.selectbox("Select Company", list(company_options.keys()))
                selected_company_id = company_options[selected_company_name]
            else:
                selected_company_id = None
        else:
            # Non-admin users see only their company
            selected_company_id = user_data['company_id']
            st.info(f"Viewing data for: {user_data['company_name']}")
    
    # Get data and create visualizations
    if db_manager.connect():
        # Get emissions summary
        emissions_summary = db_manager.get_emissions_summary(selected_company_id, selected_period)
        
        # Get category breakdown
        if selected_company_id:
            calculator = GHGCalculator(db_manager)
            category_breakdown = calculator.get_category_breakdown(selected_company_id, selected_period)
        else:
            category_breakdown = []
        
        db_manager.disconnect()
        
        # Create visualizations
        viz = DataVisualization(db_manager)
        
        if emissions_summary['total'] > 0:
            # Pie chart
            st.subheader("Emissions by Scope")
            viz.create_scope_pie_chart(emissions_summary)
            
            # Bar chart
            if category_breakdown:
                st.subheader("Emissions by Category")
                viz.create_category_bar_chart(category_breakdown)
            
            # Time series (if single company selected)
            if selected_company_id:
                st.subheader("Emissions Trend")
                viz.create_time_series_chart(selected_company_id, reporting_periods[:4])
        else:
            st.info("No emission data found for the selected filters.")
    else:
        st.error("Database connection failed")
