import mysql.connector
from config import Config
import os

# Create configuration
config = Config()

# Database connection parameters
db_config = {
    'host': config.database_config['host'],
    'port': config.database_config['port'],
    'user': config.database_config['user'],
    'password': config.database_config['password'],
    'database': config.database_config['database']
}

print("Connecting to database...")
print(f"Host: {db_config['host']}")
print(f"Database: {db_config['database']}")

try:
    # Connect to database
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    
    print("✅ Connected successfully!")
    
    # SQL for adding new Scope 3 categories
    insert_queries = [
        "INSERT IGNORE INTO ghg_categories (scope_number, scope_name, category_code, category_name, subcategory_code, subcategory_name, emission_factor, unit, description) VALUES (3, 'Scope 3 (Value chain emissions)', '3.1', 'Purchased Goods and Services', '3.1.1', 'Purchased Goods and Services', 0.5, 'USD', 'Emissions from production of purchased goods and services')",
        "INSERT IGNORE INTO ghg_categories (scope_number, scope_name, category_code, category_name, subcategory_code, subcategory_name, emission_factor, unit, description) VALUES (3, 'Scope 3 (Value chain emissions)', '3.2', 'Capital Goods', '3.2.1', 'Capital Goods', 0.8, 'USD', 'Emissions from production of capital goods')",
        "INSERT IGNORE INTO ghg_categories (scope_number, scope_name, category_code, category_name, subcategory_code, subcategory_name, emission_factor, unit, description) VALUES (3, 'Scope 3 (Value chain emissions)', '3.3', 'Fuel- and Energy-Related Activities', '3.3.1', 'Fuel and Energy Related Activities', 0.4, 'kWh', 'Emissions from fuel and energy activities not included in Scope 1 or 2')",
        "INSERT IGNORE INTO ghg_categories (scope_number, scope_name, category_code, category_name, subcategory_code, subcategory_name, emission_factor, unit, description) VALUES (3, 'Scope 3 (Value chain emissions)', '3.4', 'Upstream Transportation and Distribution', '3.4.1', 'Upstream Transportation and Distribution', 0.6, 'tonne-km', 'Emissions from transportation and distribution of purchased products')",
        "INSERT IGNORE INTO ghg_categories (scope_number, scope_name, category_code, category_name, subcategory_code, subcategory_name, emission_factor, unit, description) VALUES (3, 'Scope 3 (Value chain emissions)', '3.5', 'Waste Generated in Operations', '3.5.1', 'Waste Generated in Operations', 0.3, 'tonnes', 'Emissions from waste disposal and treatment')",
        "INSERT IGNORE INTO ghg_categories (scope_number, scope_name, category_code, category_name, subcategory_code, subcategory_name, emission_factor, unit, description) VALUES (3, 'Scope 3 (Value chain emissions)', '3.8', 'Upstream Leased Assets', '3.8.1', 'Upstream Leased Assets', 0.7, 'sqm', 'Emissions from leased assets not included in Scope 1 or 2')",
        "INSERT IGNORE INTO ghg_categories (scope_number, scope_name, category_code, category_name, subcategory_code, subcategory_name, emission_factor, unit, description) VALUES (3, 'Scope 3 (Value chain emissions)', '3.9', 'Downstream Transportation and Distribution', '3.9.1', 'Downstream Transportation and Distribution', 0.6, 'tonne-km', 'Emissions from transportation and distribution of sold products')",
        "INSERT IGNORE INTO ghg_categories (scope_number, scope_name, category_code, category_name, subcategory_code, subcategory_name, emission_factor, unit, description) VALUES (3, 'Scope 3 (Value chain emissions)', '3.10', 'Processing of Sold Products', '3.10.1', 'Processing of Sold Products', 0.9, 'tonnes', 'Emissions from processing of sold intermediate products')",
        "INSERT IGNORE INTO ghg_categories (scope_number, scope_name, category_code, category_name, subcategory_code, subcategory_name, emission_factor, unit, description) VALUES (3, 'Scope 3 (Value chain emissions)', '3.11', 'Use of Sold Products', '3.11.1', 'Use of Sold Products', 1.2, 'units', 'Emissions from use of sold products')",
        "INSERT IGNORE INTO ghg_categories (scope_number, scope_name, category_code, category_name, subcategory_code, subcategory_name, emission_factor, unit, description) VALUES (3, 'Scope 3 (Value chain emissions)', '3.12', 'End-of-Life Treatment of Sold Products', '3.12.1', 'End-of-Life Treatment of Sold Products', 0.4, 'tonnes', 'Emissions from end-of-life treatment of sold products')",
        "INSERT IGNORE INTO ghg_categories (scope_number, scope_name, category_code, category_name, subcategory_code, subcategory_name, emission_factor, unit, description) VALUES (3, 'Scope 3 (Value chain emissions)', '3.13', 'Downstream Leased Assets', '3.13.1', 'Downstream Leased Assets', 0.7, 'sqm', 'Emissions from leased assets not owned or controlled')",
        "INSERT IGNORE INTO ghg_categories (scope_number, scope_name, category_code, category_name, subcategory_code, subcategory_name, emission_factor, unit, description) VALUES (3, 'Scope 3 (Value chain emissions)', '3.14', 'Franchises', '3.14.1', 'Franchises', 0.8, 'units', 'Emissions from franchise operations')",
        "INSERT IGNORE INTO ghg_categories (scope_number, scope_name, category_code, category_name, subcategory_code, subcategory_name, emission_factor, unit, description) VALUES (3, 'Scope 3 (Value chain emissions)', '3.15', 'Investments', '3.15.1', 'Investments', 1.0, 'USD', 'Emissions from investments')"
    ]
    
    # Execute all insert queries
    added_count = 0
    for query in insert_queries:
        try:
            cursor.execute(query)
            if cursor.rowcount > 0:
                added_count += 1
                print(f"✅ Added new category")
            else:
                print(f"⏭️  Category already exists")
        except Exception as e:
            print(f"❌ Error executing query: {e}")
    
    # Commit changes
    connection.commit()
    
    # Verify the count
    cursor.execute("SELECT COUNT(*) FROM ghg_categories WHERE scope_number = 3")
    total_scope3 = cursor.fetchone()[0]
    
    print(f"\n✅ Added {added_count} new categories")
    print(f"✅ Total Scope 3 categories: {total_scope3}")
    
    # Show all Scope 3 categories
    cursor.execute("SELECT category_name, subcategory_name FROM ghg_categories WHERE scope_number = 3 ORDER BY category_name, subcategory_name")
    categories = cursor.fetchall()
    
    print(f"\nAll Scope 3 Categories:")
    for i, (cat_name, subcat_name) in enumerate(categories, 1):
        print(f"{i}. {cat_name} - {subcat_name}")
    
    cursor.close()
    connection.close()
    print("\n✅ Database operations completed successfully!")
    
except mysql.connector.Error as e:
    print(f"❌ MySQL Error: {e}")
except Exception as e:
    print(f"❌ Error: {e}")
