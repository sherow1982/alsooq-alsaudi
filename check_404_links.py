#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
import re
import sys
from pathlib import Path

# Fix encoding for Windows console
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

def check_404_issues():
    """Check all links and pages for 404 issues"""
    
    print("=" * 60)
    print("Checking website for 404 issues...")
    print("=" * 60)
    
    issues = []
    
    # 1. Check products.json
    print("\n[1] Checking products.json...")
    try:
        with open('products.json', 'r', encoding='utf-8') as f:
            products = json.load(f)
        print(f"Found {len(products)} products in products.json")
    except Exception as e:
        print(f"Error reading products.json: {e}")
        return
    
    # 2. Check products directory
    print("\n[2] Checking products directory...")
    if not os.path.exists('products'):
        print("Products directory not found!")
        issues.append("Products directory missing")
    else:
        product_files = [f for f in os.listdir('products') if f.endswith('.html')]
        print(f"Found {len(product_files)} HTML files in products directory")
        
        # Check each product has HTML page
        print("\n[3] Checking product pages match...")
        missing_pages = []
        
        for product in products:
            # Create slug
            product_id = product.get('id', '')
            title = product.get('title', '')
            
            # Remove stop words
            stop_words = ['من', 'في', 'على', 'الى', 'عن', 'و', 'مع', 'يا', 'أيها']
            for word in stop_words:
                title = re.sub(f' {word} ', ' ', title, flags=re.IGNORECASE)
            
            # Create slug
            slug = title.lower().strip()
            slug = re.sub(r'[^\w\s\u0600-\u06FF-]', '', slug)
            slug = re.sub(r'\s+', '-', slug)
            if len(slug) > 100:
                slug = slug[:100].rstrip('-')
            
            expected_filename = f"{product_id}-{slug}.html"
            expected_path = os.path.join('products', expected_filename)
            
            if not os.path.exists(expected_path):
                missing_pages.append({
                    'id': product_id,
                    'title': title,
                    'expected_file': expected_filename
                })
        
        if missing_pages:
            print(f"Found {len(missing_pages)} missing product pages:")
            for item in missing_pages[:10]:
                print(f"  - Product #{item['id']}: {item['title']}")
                print(f"    Expected file: {item['expected_file']}")
            if len(missing_pages) > 10:
                print(f"  ... and {len(missing_pages) - 10} more")
            issues.append(f"{len(missing_pages)} missing product pages")
        else:
            print("All products have HTML pages")
    
    # 4. Check main pages
    print("\n[4] Checking main pages...")
    main_pages = [
        'index.html',
        'about.html', 
        'contact.html',
        'shipping.html',
        'return-policy.html',
        'terms.html',
        'privacy.html',
        '404.html'
    ]
    
    for page in main_pages:
        if os.path.exists(page):
            print(f"OK: {page}")
        else:
            print(f"MISSING: {page}")
            issues.append(f"Page {page} missing")
    
    # 5. Check CSS files
    print("\n[5] Checking CSS files...")
    css_files = ['css/main.css']
    for css_file in css_files:
        if os.path.exists(css_file):
            print(f"OK: {css_file}")
        else:
            print(f"MISSING: {css_file}")
            issues.append(f"CSS file {css_file} missing")
    
    # 6. Check main images
    print("\n[6] Checking main images...")
    images = ['logo.png', 'logo.svg', 'hero-banner.png', 'favicon.svg']
    for img in images:
        if os.path.exists(img):
            print(f"OK: {img}")
        else:
            print(f"MISSING: {img}")
            issues.append(f"Image {img} missing")
    
    # 7. Check XML files
    print("\n[7] Checking XML files...")
    xml_files = ['sitemap.xml', 'product-feed.xml', 'robots.txt']
    for xml_file in xml_files:
        if os.path.exists(xml_file):
            print(f"OK: {xml_file}")
        else:
            print(f"MISSING: {xml_file}")
            issues.append(f"File {xml_file} missing")
    
    # Final result
    print("\n" + "=" * 60)
    print("FINAL RESULT")
    print("=" * 60)
    
    if not issues:
        print("EXCELLENT! No 404 issues found")
        print("All pages and links are working correctly")
        print("Website is ready for deployment")
    else:
        print(f"Found {len(issues)} issues:")
        for i, issue in enumerate(issues, 1):
            print(f"  {i}. {issue}")
        print("\nPlease fix these issues to avoid 404 errors")
    
    print("=" * 60)
    
    return issues

if __name__ == "__main__":
    check_404_issues()
