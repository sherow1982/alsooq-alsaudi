#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
سكريبت شامل لتشغيل جميع الإصلاحات دفعة واحدة
"""

import subprocess
import sys
import os

# Force UTF-8 encoding for Windows console
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

def run_script(script_name, description):
    """تشغيل سكريبت واحد"""
    print(f"\n{'='*60}")
    print(f"▶ {description}")
    print(f"{'='*60}")
    
    if not os.path.exists(script_name):
        print(f"⚠️  الملف غير موجود: {script_name}")
        return False
    
    try:
        result = subprocess.run(
            [sys.executable, script_name],
            capture_output=True,
            text=True,
            encoding='utf-8'
        )
        
        if result.stdout:
            print(result.stdout)
        
        if result.returncode == 0:
            print(f"✅ تم بنجاح")
            return True
        else:
            if result.stderr:
                print(f"❌ خطأ: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ خطأ: {e}")
        return False

def main():
    """الدالة الرئيسية"""
    print("\n" + "="*60)
    print("🚀 بدء تشغيل جميع الإصلاحات - السوق السعودي")
    print("="*60)
    
    scripts = [
        ("fix_feed_gmc.py", "1️⃣  إصلاح ملف المنتجات XML (Google Merchant)"),
        ("fix_products.py", "2️⃣  إصلاح مسارات CSS في صفحات المنتجات"),
        ("fix_schema.py", "3️⃣  إصلاح Schema.org في صفحات المنتجات"),
        ("fix_html_encoding.py", "4️⃣  إصلاح ترميز HTML"),
        ("generate_all_pages.py", "5️⃣  توليد جميع صفحات المنتجات"),
        ("seo_optimizer.py", "6️⃣  تحسين SEO والسكيما"),
        ("generate_sitemap.py", "7️⃣  توليد خريطة الموقع"),
        ("update_product_feed.py", "8️⃣  تحديث ملف المنتجات"),
        ("check_status.py", "9️⃣  فحص حالة الموقع")
    ]
    
    success_count = 0
    failed_scripts = []
    
    for script_name, description in scripts:
        if run_script(script_name, description):
            success_count += 1
        else:
            failed_scripts.append(script_name)
    
    # النتيجة النهائية
    print("\n" + "="*60)
    print("📊 النتيجة النهائية")
    print("="*60)
    print(f"✅ نجح: {success_count}/{len(scripts)}")
    print(f"❌ فشل: {len(failed_scripts)}/{len(scripts)}")
    
    if failed_scripts:
        print("\n⚠️  السكريبتات الفاشلة:")
        for script in failed_scripts:
            print(f"   - {script}")
    
    if success_count == len(scripts):
        print("\n🎉 تم تنفيذ جميع الإصلاحات بنجاح!")
        print("\n✨ الموقع جاهز الآن:")
        print("   ✓ جميع صفحات المنتجات تم إنشاؤها")
        print("   ✓ ملف المنتجات XML محدث")
        print("   ✓ خريطة الموقع محدثة")
        print("   ✓ SEO والسكيما محسنة")
        print("   ✓ لا توجد أخطاء 404")
    else:
        print("\n⚠️  بعض الإصلاحات لم تكتمل")
    
    print("\n" + "="*60)

if __name__ == "__main__":
    main()
