from database_operations import DatabaseManager

db = DatabaseManager()
if db.connect():
    # Check all scopes
    for scope in [1, 2, 3]:
        categories = db.get_ghg_categories(scope)
        print(f'Scope {scope}: {len(categories)} categories')
        for cat in categories[:3]:  # Show first 3
            print(f'  - {cat["category_name"]} - {cat["subcategory_name"]}')
        if len(categories) > 3:
            print(f'  ... and {len(categories) - 3} more')
        print()
    db.disconnect()
else:
    print("Connection failed")
