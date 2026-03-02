#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
import re
import shutil

# Read products.json
with open('products.json', 'r', encoding='utf-8') as f:
    products = json.load(f)

# IDs to check
problem_ids = [727, 1272, 639, 816, 1240, 270, 1133, 852, 125, 1031, 1042, 314, 2074, 1919, 784, 276, 1265, 1158]

print("Finding and fixing missing product pages...")
print("=" * 70)

for pid in problem_ids:
    # Find product in JSON
    product = next((p for p in products if p.get('id') == pid), None)
    
    if not product:
        print(f"Product {pid} not found in JSON")
        continue
    
    # Check existing files
    existing_files = [f for f in os.listdir('products') if f.startswith(f"{pid}-")]
    
    if existing_files:
        print(f"\nProduct {pid}: {product['title']}")
        print(f"  Existing file: {existing_files[0]}")
    else:
        print(f"\nProduct {pid}: {product['title']}")
        print(f"  NO FILE FOUND - needs generation")

print("\n" + "=" * 70)
print("Run generate_missing_products.py to create missing pages")
