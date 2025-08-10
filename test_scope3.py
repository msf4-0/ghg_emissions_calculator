from database_operations import DatabaseManager

db = DatabaseManager()

if db.connect():
    # Get all Scope 3 categories
    scope3_categories = db.get_ghg_categories(3)
    print(f'Total Scope 3 categories: {len(scope3_categories)}')
    print('\nScope 3 Categories:')
    for i, cat in enumerate(scope3_categories, 1):
        print(f'{i}. {cat["category_name"]} - {cat["subcategory_name"]} (ID: {cat["id"]})')
    
    # Get all categories
    all_categories = db.get_ghg_categories()
    scope_counts = {}
    for cat in all_categories:
        scope = cat['scope_number']
        if scope not in scope_counts:
            scope_counts[scope] = 0
        scope_counts[scope] += 1
    
    print(f'\nTotal categories by scope:')
    for scope, count in sorted(scope_counts.items()):
        print(f'Scope {scope}: {count} categories')
    
    db.disconnect()
else:
    print('Database connection failed')
