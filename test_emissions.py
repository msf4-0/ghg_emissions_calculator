#!/usr/bin/env python3
"""
Test the emissions input form functionality
"""

from database_operations import DatabaseManager
from ghg_calculator import GHGCalculator

def test_emissions_functionality():
    print("🧪 Testing Emissions Functionality")
    print("=" * 40)
    
    db = DatabaseManager()
    
    if not db.connect():
        print("❌ Database connection failed")
        return False
    
    # Test getting GHG categories
    print("📊 Testing GHG categories...")
    categories = db.get_ghg_categories()
    
    if categories:
        print(f"✅ Found {len(categories)} GHG categories")
        for i, cat in enumerate(categories[:3]):  # Show first 3
            print(f"  - {cat['scope_name']}: {cat['subcategory_name']} ({cat['unit']})")
        if len(categories) > 3:
            print(f"  ... and {len(categories) - 3} more")
    else:
        print("❌ No GHG categories found")
        return False
    
    # Test calculator
    print("\n🧮 Testing GHG calculator...")
    calculator = GHGCalculator(db)
    
    # Test calculation with first category
    test_category = categories[0]
    test_activity_data = 100.0
    
    try:
        co2_equiv, calc_details = calculator.calculate_emissions(
            test_category['id'], 
            test_activity_data
        )
        print(f"✅ Calculation successful:")
        print(f"  Category: {test_category['subcategory_name']}")
        print(f"  Activity Data: {test_activity_data} {test_category['unit']}")
        print(f"  CO2 Equivalent: {co2_equiv:.4f} kg CO2e")
    except Exception as e:
        print(f"❌ Calculation failed: {e}")
        return False
    
    db.disconnect()
    print("\n🎉 Emissions functionality test completed successfully!")
    return True

if __name__ == "__main__":
    test_emissions_functionality()
