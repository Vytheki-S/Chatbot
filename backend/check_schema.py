#!/usr/bin/env python
import os
import sys
import django

# Add the backend directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.db import connection

def check_complaint_categories():
    with connection.cursor() as cursor:
        cursor.execute("SHOW COLUMNS FROM complaints LIKE 'complaint_category'")
        result = cursor.fetchall()
        print("Complaint category column definition:")
        print(result)
        
        # Get the enum values
        if result:
            column_def = result[0][1]  # Get the column definition
            print(f"\nColumn definition: {column_def}")
            
            # Extract enum values
            if 'enum(' in column_def:
                enum_part = column_def.split('enum(')[1].split(')')[0]
                enum_values = [val.strip("'") for val in enum_part.split(',')]
                print(f"Valid enum values: {enum_values}")

if __name__ == "__main__":
    check_complaint_categories()
