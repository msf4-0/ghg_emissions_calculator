from database_operations import DatabaseManager

db = DatabaseManager()
if db.connect():
    print("=== Testing Database Categories ===")
    
    # Test the get_ghg_categories() method (no scope filter)
    all_categories = db.get_ghg_categories()
    print(f"Total categories from get_ghg_categories(): {len(all_categories)}")
    
    # Count by scope
    scope_counts = {}
    for cat in all_categories:
        scope = cat['scope_number']
        if scope not in scope_counts:
            scope_counts[scope] = []
        scope_counts[scope].append(cat)
    
    for scope, cats in scope_counts.items():
        print(f"\nScope {scope}: {len(cats)} categories")
        for i, cat in enumerate(cats[:5], 1):  # Show first 5
            print(f"  {i}. {cat['category_name']} - {cat['subcategory_name']}")
        if len(cats) > 5:
            print(f"  ... and {len(cats) - 5} more")
    
    print(f"\n=== Scope 3 Categories (All {len(scope_counts.get(3, []))}) ===")
    for i, cat in enumerate(scope_counts.get(3, []), 1):
        print(f"{i:2d}. {cat['category_name']} - {cat['subcategory_name']} (ID: {cat['id']})")
    
    db.disconnect()
else:
    print("Database connection failed")
