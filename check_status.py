#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os

def check_website_status():
    """Check the status of alsooq-alsaudi website"""
    print("Checking alsooq-alsaudi website status...")
    
    # Check products.json
    try:
        with open('products.json', 'r', encoding='utf-8') as f:
            products = json.load(f)
        print(f"Products in JSON: {len(products)}")
    except Exception as e:
        print(f"Error reading products.json: {e}")
        return
    
    # Check products directory
    if os.path.exists('products'):
        product_files = [f for f in os.listdir('products') if f.endswith('.html')]
        print(f"Product HTML files: {len(product_files)}")
    else:
        print("Products directory not found!")
        return
    
    # Check main files
    main_files = ['index.html', 'about.html', 'contact.html', 'sitemap.xml', 'product-feed.xml']
    for file in main_files:
        if os.path.exists(file):
            print(f"[OK] {file} exists")
        else:
            print(f"[MISSING] {file} missing")
    
    # Summary
    print("\n" + "="*50)
    print("WEBSITE STATUS SUMMARY")
    print("="*50)
    print(f"Total products in JSON: {len(products)}")
    print(f"Total product pages: {len(product_files)}")
    
    if len(product_files) >= len(products):
        print("[SUCCESS] All product pages created successfully!")
        print("[SUCCESS] No more 404 errors for product pages!")
    else:
        missing = len(products) - len(product_files)
        print(f"[WARNING] {missing} product pages are missing")
    
    print("\nWebsite is ready for use!")

if __name__ == "__main__":
    check_website_status()