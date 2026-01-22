#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import glob
import re

def fix_schema_return_policy():
    """Fix returnPolicyCategory schema issue in all product files"""
    
    products_dir = "products"
    html_files = glob.glob(os.path.join(products_dir, "*.html"))
    
    print(f"Found {len(html_files)} product files to fix...")
    
    # Fix the returnPolicyCategory value
    old_value = '"returnPolicyCategory": "https://schema.org/MerchantReturnFiniteReturnPeriod"'
    new_value = '"returnPolicyCategory": "https://schema.org/MerchantReturnFiniteReturnWindow"'
    
    fixed_count = 0
    
    for file_path in html_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if old_value in content:
                content = content.replace(old_value, new_value)
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                fixed_count += 1
                print(f"Fixed schema in file #{fixed_count}")
                
        except Exception as e:
            print(f"Error processing file: {str(e)[:50]}...")
    
    print(f"\nFixed schema in {fixed_count} out of {len(html_files)} product files!")

if __name__ == "__main__":
    fix_schema_return_policy()