#!/usr/bin/env python
"""
Check URL patterns
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.urls import get_resolver

def check_urls():
    resolver = get_resolver()
    print("URL patterns:")
    for pattern in resolver.url_patterns:
        print(f"  {pattern}")
        if hasattr(pattern, 'url_patterns'):
            for sub_pattern in pattern.url_patterns:
                print(f"    {sub_pattern}")

if __name__ == "__main__":
    check_urls()
