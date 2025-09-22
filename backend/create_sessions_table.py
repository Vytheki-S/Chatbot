#!/usr/bin/env python
"""
Create the missing chatbot_sessions table
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.db import connection

def create_sessions_table():
    with connection.cursor() as cursor:
        # Create the chatbot_sessions table
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS `chatbot_sessions` (
            `id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY,
            `user_id` varchar(100) NOT NULL,
            `created_at` datetime(6) NOT NULL,
            `updated_at` datetime(6) NOT NULL
        );
        """
        
        try:
            cursor.execute(create_table_sql)
            print("✅ Created chatbot_sessions table")
        except Exception as e:
            print(f"❌ Error creating table: {e}")
        
        # Create the chatbot_messages_new table
        create_messages_table_sql = """
        CREATE TABLE IF NOT EXISTS `chatbot_messages_new` (
            `id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY,
            `session_id` bigint NOT NULL,
            `sender_type` varchar(20) NOT NULL,
            `content` longtext NOT NULL,
            `created_at` datetime(6) NOT NULL,
            CONSTRAINT `chatbot_messages_new_session_id_fk` 
                FOREIGN KEY (`session_id`) REFERENCES `chatbot_sessions` (`id`) ON DELETE CASCADE
        );
        """
        
        try:
            cursor.execute(create_messages_table_sql)
            print("✅ Created chatbot_messages_new table")
        except Exception as e:
            print(f"❌ Error creating messages table: {e}")
        
        # Verify tables exist
        cursor.execute("SHOW TABLES LIKE 'chatbot_sessions'")
        if cursor.fetchall():
            print("✅ chatbot_sessions table verified")
        else:
            print("❌ chatbot_sessions table still missing")

if __name__ == "__main__":
    create_sessions_table()

