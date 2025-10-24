#!/usr/bin/env python3
import sys
import traceback

print("Testing imports...")

try:
    print("1. Testing database_operations import...")
    from database_operations import DatabaseManager
    print("   ✓ DatabaseManager imported successfully")
except Exception as e:
    print(f"   ✗ Error importing DatabaseManager: {e}")
    traceback.print_exc()
    
try:
    print("2. Testing data_visualization module import...")
    import data_visualization
    print("   ✓ data_visualization module imported")
    print(f"   Available in module: {[x for x in dir(data_visualization) if not x.startswith('_')]}")
except Exception as e:
    print(f"   ✗ Error importing data_visualization: {e}")
    traceback.print_exc()

try:
    print("3. Testing specific class import...")
    from data_visualization import DataVisualization
    print("   ✓ DataVisualization class imported successfully")
except Exception as e:
    print(f"   ✗ Error importing DataVisualization: {e}")
    traceback.print_exc()

print("Debug complete.")
