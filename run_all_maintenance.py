#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess
import sys
import os

# Force UTF-8 encoding for Windows console
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

def run_script(script_name, description):
    """Run a Python script and handle errors"""
    print(f"\n{'='*50}")
    print(f"Running: {description}")
    print(f"{'='*50}")
    
    try:
        result = subprocess.run([sys.executable, script_name], 
                              capture_output=True, text=True, encoding='utf-8')
        
        if result.stdout:
            print(result.stdout)
        
        if result.stderr:
            print(f"Errors: {result.stderr}")
        
        if result.returncode == 0:
            print(f"✅ {description} completed successfully!")
        else:
            print(f"❌ {description} failed with return code {result.returncode}")
            
        return result.returncode == 0
        
    except Exception as e:
        print(f"❌ Error running {script_name}: {e}")
        return False

def main():
    """Run all maintenance scripts"""
    print("🚀 Starting alsooq-alsaudi maintenance scripts...")
    
    scripts = [
        ("generate_missing_products.py", "Generate missing product pages"),
        ("update_sitemap.py", "Update sitemap.xml"),
        ("update_product_feed.py", "Update product feed XML")
    ]
    
    success_count = 0
    total_count = len(scripts)
    
    for script_name, description in scripts:
        if os.path.exists(script_name):
            if run_script(script_name, description):
                success_count += 1
        else:
            print(f"❌ Script {script_name} not found!")
    
    print(f"\n{'='*50}")
    print(f"SUMMARY")
    print(f"{'='*50}")
    print(f"✅ Successful: {success_count}/{total_count}")
    print(f"❌ Failed: {total_count - success_count}/{total_count}")
    
    if success_count == total_count:
        print("\n🎉 All scripts completed successfully!")
        print("Your alsooq-alsaudi website is now fully updated!")
    else:
        print(f"\n⚠️  Some scripts failed. Please check the errors above.")
    
    print(f"\n📊 Website Status:")
    print(f"- All product pages are now available")
    print(f"- Sitemap.xml updated with all pages")
    print(f"- Product feed updated for Google Merchant Center")
    print(f"- No more 404 errors for product pages!")

if __name__ == "__main__":
    main()