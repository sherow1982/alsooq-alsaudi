#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
سكريبت تشغيل جميع العمليات بالتسلسل الصحيح
"""

import subprocess
import sys
import os
from pathlib import Path

def run_script(script_name, description):
    """تشغيل سكريبت واحد مع معالجة الأخطاء"""
    print(f"\n{'='*50}")
    print(f"تشغيل: {description}")
    print(f"{'='*50}")
    
    script_path = Path(script_name)
    if not script_path.exists():
        print(f"❌ الملف غير موجود: {script_name}")
        return False
    
    try:
        result = subprocess.run([sys.executable, script_name], 
                              capture_output=True, 
                              text=True, 
                              encoding='utf-8',
                              cwd=os.getcwd())
        
        if result.stdout:
            print(result.stdout)
        
        if result.stderr:
            print(f"تحذيرات: {result.stderr}")
        
        if result.returncode == 0:
            print(f"✅ تم بنجاح: {description}")
            return True
        else:
            print(f"❌ فشل: {description} (Exit code: {result.returncode})")
            return False
            
    except Exception as e:
        print(f"❌ خطأ في تشغيل {script_name}: {e}")
        return False

def main():
    """الدالة الرئيسية"""
    print("بدء تشغيل جميع السكريبتات...")
    
    scripts = [
        ("generate_all_pages.py", "توليد صفحات المنتجات"),
        ("seo_optimizer.py", "تحسين السيو والسكيما"),
        ("fix_feed.py", "إنشاء ملف المنتجات XML"),
        ("generate_sitemap.py", "إنشاء خريطة الموقع")
    ]
    
    success_count = 0
    total_scripts = len(scripts)
    
    for script_name, description in scripts:
        if run_script(script_name, description):
            success_count += 1
        else:
            print(f"\n⚠️ فشل في تشغيل {script_name}")
            user_input = input("هل تريد المتابعة؟ (y/n): ").lower()
            if user_input != 'y':
                break
    
    print(f"\n{'='*60}")
    print(f"النتيجة النهائية: {success_count}/{total_scripts} سكريبت تم بنجاح")
    print(f"{'='*60}")
    
    if success_count == total_scripts:
        print("🎉 تم تشغيل جميع السكريبتات بنجاح!")
    else:
        print("⚠️ بعض السكريبتات لم تكتمل بنجاح")

if __name__ == "__main__":
    main()