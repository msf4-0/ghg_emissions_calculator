#!/usr/bin/env python3
import sys
import traceback

print("Testing import with exception handling...")

try:
    # Import each dependency separately
    print("Importing streamlit...")
    import streamlit as st
    print("✓ streamlit imported")
    
    print("Importing plotly...")
    import plotly.express as px
    import plotly.graph_objects as go
    print("✓ plotly imported")
    
    print("Importing pandas...")
    import pandas as pd
    print("✓ pandas imported")
    
    print("Importing typing...")
    from typing import Dict, List
    print("✓ typing imported")
    
    print("Importing database_operations...")
    from database_operations import DatabaseManager
    print("✓ database_operations imported")
    
    print("Now executing data_visualization.py content...")
    with open('data_visualization.py', 'r') as f:
        content = f.read()
    
    exec(content)
    print("✓ File executed successfully")
    print(f"DataVisualization available: {'DataVisualization' in locals()}")
    print(f"create_dashboard available: {'create_dashboard' in locals()}")
    
except Exception as e:
    print(f"✗ Error during execution: {e}")
    traceback.print_exc()

print("Test complete.")
