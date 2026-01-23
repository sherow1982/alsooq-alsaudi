#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fix all product page headers and footers in batch
Updates contact details to: Egypt, 6 October, Giza
Run this script locally to update all product files
"""

import os
import re
from pathlib import Path

MODERN_FOOTER_CONTACT = '''            <div class="footer-section">
                <h3>تواصل معنا</h3>
                <p>مؤسسة alsooq-alsaudi</p>
                <p>مصر، الجيزة، 6 أكتوبر</p>
                <p>الرمز البريدي: 12365</p>
                <p style="margin-top: 15px; color: var(--accent-color); font-weight: bold; font-size: 1.1rem;">واتساب: +201110760081</p>
                <p style="margin-top: 5px; font-size: 0.9rem;">البريد: sherow1982@gmail.com</p>
                <p style="margin-top: 10px; font-size: 0.9rem;">الموقع: <a href="https://sherow1982.github.io/alsooq-alsaudi" target="_blank" style="color: var(--primary-color);">https://sherow1982.github.io/alsooq-alsaudi</a></p>
            </div>'''

def fix_product_file(file_path):
    """
    Fix a single product file's footer contact details
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Pattern to find old footer contact section
        old_pattern = r'<div class="footer-section">\s*<h3>تواصل معنا</h3>.*?</div>\s*</div>\s*<div class="footer-bottom">'
        
        # Check if old pattern exists
        if re.search(old_pattern, content, re.DOTALL):
            # Replace with new footer contact section
            new_content = re.sub(
                old_pattern,
                MODERN_FOOTER_CONTACT + '\n            </div>\n        <div class="footer-bottom">',
                content,
                flags=re.DOTALL
            )
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            return True
        else:
            # Try simpler pattern
            if 'تواصل معنا' in content:
                # File has contact section but different format
                # Do manual replacement
                new_content = re.sub(
                    r'<h3>تواصل معنا</h3>.*?<p style="margin-top: 5px;.*?sherow1982@gmail.com.*?</p>',
                    '<h3>تواصل معنا</h3>\n                <p>مؤسسة alsooq-alsaudi</p>\n                <p>مصر، الجيزة، 6 أكتوبر</p>\n                <p>الرمز البريدي: 12365</p>\n                <p style="margin-top: 15px; color: var(--accent-color); font-weight: bold; font-size: 1.1rem;">واتساب: +201110760081</p>\n                <p style="margin-top: 5px; font-size: 0.9rem;">البريد: sherow1982@gmail.com</p>\n                <p style="margin-top: 10px; font-size: 0.9rem;">الموقع: <a href="https://sherow1982.github.io/alsooq-alsaudi" target="_blank" style="color: var(--primary-color);">https://sherow1982.github.io/alsooq-alsaudi</a></p>',
                    content,
                    flags=re.DOTALL
                )
                
                if new_content != content:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    return True
        
        return False
    except Exception as e:
        print(f"  ☹️ خطأ بالمعالجة: {str(e)}")
        return False

def main():
    products_dir = Path('products')
    
    if not products_dir.exists():
        print("❌ مجلد products غير موجود")
        return
    
    html_files = list(products_dir.glob('*.html'))
    print(f"🔍 وجدت {len(html_files)} ملف منتج")
    print(f"{'='*60}")
    
    fixed = 0
    failed = 0
    
    for html_file in html_files:
        try:
            if fix_product_file(html_file):
                fixed += 1
                print(f"✅ {html_file.name}")
            else:
                failed += 1
                print(f"⚠️ {html_file.name} - لم يطابق النمط")
        except Exception as e:
            failed += 1
            print(f"❌ {html_file.name}: {str(e)}")
    
    print(f"{'='*60}")
    print(f"✅ تم تصحيح: {fixed} ملف")
    print(f"❌ فشل أو بدون تغيير: {failed} ملف")
    print(f"{'='*60}")
    print(f"\n🎆 البيانات الجديدة:")
    print(f"  🏭 مؤسسة: alsooq-alsaudi")
    print(f"  🇪🇬 الدولة: مصر")
    print(f"  🌟 المدينة: الجيزة، 6 أكتوبر")
    print(f"  📋 الرمز البريدي: 12365")
    print(f"  📞 واتساب: +201110760081")
    print(f"  📧 بريد: sherow1982@gmail.com")

if __name__ == '__main__':
    main()
