#!/usr/bin/env python
"""
Check database tables
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.db import connection

def check_tables():
    with connection.cursor() as cursor:
        # Check for chatbot tables
        cursor.execute("SHOW TABLES LIKE 'chatbot_%'")
        chatbot_tables = cursor.fetchall()
        print("Chatbot tables found:")
        for table in chatbot_tables:
            print(f"  - {table[0]}")
        
        # Check for all tables
        cursor.execute("SHOW TABLES")
        all_tables = cursor.fetchall()
        print(f"\nTotal tables in database: {len(all_tables)}")
        
        # Check if chatbot_sessions specifically exists
        cursor.execute("SHOW TABLES LIKE 'chatbot_sessions'")
        sessions_table = cursor.fetchall()
        if sessions_table:
            print("✅ chatbot_sessions table exists")
        else:
            print("❌ chatbot_sessions table does NOT exist")

if __name__ == "__main__":
    check_tables()

