from database_operations import DatabaseManager

# All 15 Scope 3 categories according to GHG Protocol
scope3_categories = [
    # Upstream
    (3, "Scope 3 (Value chain emissions)", "3.1", "Purchased Goods and Services", "3.1.1", "Purchased Goods and Services", 0.5, "USD", "Emissions from production of purchased goods and services"),
    (3, "Scope 3 (Value chain emissions)", "3.2", "Capital Goods", "3.2.1", "Capital Goods", 0.8, "USD", "Emissions from production of capital goods"),
    (3, "Scope 3 (Value chain emissions)", "3.3", "Fuel- and Energy-Related Activities", "3.3.1", "Fuel and Energy Related Activities", 0.4, "kWh", "Emissions from fuel and energy activities not included in Scope 1 or 2"),
    (3, "Scope 3 (Value chain emissions)", "3.4", "Upstream Transportation and Distribution", "3.4.1", "Upstream Transportation and Distribution", 0.6, "tonne-km", "Emissions from transportation and distribution of purchased products"),
    (3, "Scope 3 (Value chain emissions)", "3.5", "Waste Generated in Operations", "3.5.1", "Waste Generated in Operations", 0.3, "tonnes", "Emissions from waste disposal and treatment"),
    (3, "Scope 3 (Value chain emissions)", "3.6", "Business Travel", "3.6.1", "Air Travel - Domestic", 0.2, "km", "Emissions from business travel"),
    (3, "Scope 3 (Value chain emissions)", "3.6", "Business Travel", "3.6.2", "Air Travel - International", 0.15, "km", "Emissions from international business travel"),
    (3, "Scope 3 (Value chain emissions)", "3.7", "Employee Commuting", "3.7.1", "Car Commuting", 0.18, "km", "Emissions from employee commuting"),
    (3, "Scope 3 (Value chain emissions)", "3.8", "Upstream Leased Assets", "3.8.1", "Upstream Leased Assets", 0.7, "sqm", "Emissions from leased assets not included in Scope 1 or 2"),
    
    # Downstream
    (3, "Scope 3 (Value chain emissions)", "3.9", "Downstream Transportation and Distribution", "3.9.1", "Downstream Transportation and Distribution", 0.6, "tonne-km", "Emissions from transportation and distribution of sold products"),
    (3, "Scope 3 (Value chain emissions)", "3.10", "Processing of Sold Products", "3.10.1", "Processing of Sold Products", 0.9, "tonnes", "Emissions from processing of sold intermediate products"),
    (3, "Scope 3 (Value chain emissions)", "3.11", "Use of Sold Products", "3.11.1", "Use of Sold Products", 1.2, "units", "Emissions from use of sold products"),
    (3, "Scope 3 (Value chain emissions)", "3.12", "End-of-Life Treatment of Sold Products", "3.12.1", "End-of-Life Treatment of Sold Products", 0.4, "tonnes", "Emissions from end-of-life treatment of sold products"),
    (3, "Scope 3 (Value chain emissions)", "3.13", "Downstream Leased Assets", "3.13.1", "Downstream Leased Assets", 0.7, "sqm", "Emissions from leased assets not owned or controlled"),
    (3, "Scope 3 (Value chain emissions)", "3.14", "Franchises", "3.14.1", "Franchises", 0.8, "units", "Emissions from franchise operations"),
    (3, "Scope 3 (Value chain emissions)", "3.15", "Investments", "3.15.1", "Investments", 1.0, "USD", "Emissions from investments"),
]

db = DatabaseManager()

if db.connect():
    print("Connected to database. Adding missing Scope 3 categories...")
    
    # First, let's see which categories already exist
    existing_categories = db.get_ghg_categories(3)
    existing_subcategories = [cat['subcategory_name'] for cat in existing_categories]
    print(f"Existing Scope 3 subcategories: {existing_subcategories}")
    
    # Add new categories using direct cursor operations
    added_count = 0
    try:
        cursor = db.connection.cursor()
        
        for cat in scope3_categories:
            scope_number, scope_name, category_code, category_name, subcategory_code, subcategory_name, emission_factor, unit, description = cat
            
            # Check if this subcategory already exists
            if subcategory_name not in existing_subcategories:
                try:
                    query = """
                    INSERT INTO ghg_categories 
                    (scope_number, scope_name, category_code, category_name, subcategory_code, subcategory_name, emission_factor, unit, description)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """
                    
                    cursor.execute(query, cat)
                    print(f"✅ Added: {category_name} - {subcategory_name}")
                    added_count += 1
                except Exception as e:
                    print(f"❌ Error adding {subcategory_name}: {e}")
            else:
                print(f"⏭️  Already exists: {subcategory_name}")
        
        # Commit all changes
        db.connection.commit()
        cursor.close()
        
    except Exception as e:
        print(f"❌ Database operation error: {e}")
        if db.connection:
            db.connection.rollback()
    
    print(f"\n✅ Added {added_count} new Scope 3 categories")
    
    # Verify the total count
    updated_categories = db.get_ghg_categories(3)
    print(f"✅ Total Scope 3 categories now: {len(updated_categories)}")
    
    db.disconnect()
else:
    print("❌ Database connection failed")
