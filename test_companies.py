#!/usr/bin/env python3
from database_operations import DatabaseManager

db = DatabaseManager()
if db.connect():
    companies = db.get_companies()
    print('Available companies:')
    for c in companies:
        print(f'- {c["company_name"]} (ID: {c["id"]})')
    db.disconnect()
else:
    print("Failed to connect to database")
