import json
import re
import sys
import os
from urllib.parse import quote
from datetime import datetime

def create_slug(product):
    """توليد slug فريد للمنتج"""
    stop_words = ['من', 'في', 'على', 'الى', 'عن', 'و', 'مع', 'يا', 'أيها']
    
    title = product['title']
    for word in stop_words:
        title = title.replace(f' {word} ', ' ')

    slug = re.sub(r'[^\w\s-]', '', title).strip().lower()
    slug = re.sub(r'\s+', '-', slug)
    return f"{product['id']}-{slug}"

def fix_image_url(url):
    """إصلاح رابط الصورة واستبدال الامتدادات غير المدعومة"""
    if not url:
        return ""
    
    lower_url = url.lower()
    if lower_url.endswith('.mp4'):
        return url[:-4] + '.jpg'
    elif lower_url.endswith('.webp'):
        return url[:-5] + '.jpg'
    return url

def get_product_category(title):
    """تحديد فئة المنتج بناءً على العنوان"""
    title_lower = title.lower()
    
    if any(word in title_lower for word in ['شعر', 'شامبو', 'بلسم', 'زيت', 'ماسك', 'صبغة', 'حلاقة']):
        return 'Health & Beauty > Personal Care > Hair Care', 'العناية بالشعر'
    elif any(word in title_lower for word in ['بشرة', 'كريم', 'سيروم', 'واقي', 'مرطب', 'تفتيح', 'صابون', 'غسول', 'مكياج', 'روج', 'شفاه']):
        return 'Health & Beauty > Personal Care > Cosmetics', 'العناية بالجمال'
    elif any(word in title_lower for word in ['جهاز', 'ماكينة', 'آلة', 'كهربائي', 'قابل للشحن', 'شاحن', 'سماعة', 'كاميرا', 'جوال', 'تابلت', 'ساعة']):
        return 'Electronics', 'الإلكترونيات'
    elif any(word in title_lower for word in ['فيتامين', 'مكمل', 'كبسولات', 'حبوب', 'علاج', 'مشد', 'مصحح', 'ركبة', 'ظهر']):
        return 'Health & Beauty > Health Care', 'الصحة والعافية'
    elif any(word in title_lower for word in ['ملابس', 'شورت', 'قميص', 'حقيبة', 'نظارة', 'حذاء', 'جورب']):
        return 'Apparel & Accessories', 'الأزياء والموضة'
    else:
        return 'Home & Garden', 'المنزل والأدوات'

def fix_product_feed():
    """إصلاح ملف product-feed.xml وإعادة توليده"""
    base_url = "https://sherow1982.github.io/alsooq-alsaudi"
    
    # فحص وجود ملف المنتجات
    if not os.path.exists('products.json'):
        print("❌ products.json not found")
        return
    
    try:
        with open('products.json', 'r', encoding='utf-8') as f:
            products = json.load(f)
    except (json.JSONDecodeError, UnicodeDecodeError) as e:
        print(f"❌ Error reading products.json: {e}")
        return
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return
    
    if not products:
        print("⚠️ No products found")
        return
    
    xml = ['<?xml version="1.0" encoding="UTF-8"?>']
    xml.append('<rss xmlns:g="http://base.google.com/ns/1.0" version="2.0">')
    xml.append('  <channel>')
    xml.append('    <title>السوق السعودي</title>')
    xml.append(f'    <link>{base_url}/</link>')
    xml.append('    <description>أفضل العروض والمنتجات الأصلية بأسعار تنافسية</description>')
    
    for product in products:
        slug = create_slug(product)
        encoded_slug = quote(slug)
        product_link = f"{base_url}/products/{encoded_slug}.html"
        
        image_link = fix_image_url(product['image_link'])
        google_cat, product_type = get_product_category(product['title'])
        
        discount = product['price'] - product['sale_price']
        description = f"{product['title']} - منتج أصلي بضمان الجودة. وفر {discount} ريال الآن!"
        
        xml.append('    <item>')
        xml.append(f'      <g:id>{product["id"]}</g:id>')
        xml.append(f'      <g:title><![CDATA[{product["title"]}]]></g:title>')
        xml.append(f'      <g:description><![CDATA[{description}]]></g:description>')
        xml.append(f'      <g:link>{product_link}</g:link>')
        xml.append(f'      <g:image_link>{image_link}</g:image_link>')
        xml.append('      <g:condition>new</g:condition>')
        xml.append('      <g:availability>in stock</g:availability>')
        xml.append(f'      <g:price>{product["price"]} SAR</g:price>')
        xml.append(f'      <g:sale_price>{product["sale_price"]} SAR</g:sale_price>')
        xml.append('      <g:brand>السوق السعودي</g:brand>')
        xml.append(f'      <g:google_product_category>{google_cat}</g:google_product_category>')
        xml.append(f'      <g:product_type>{product_type}</g:product_type>')
        xml.append('      <g:shipping>')
        xml.append('        <g:country>SA</g:country>')
        xml.append('        <g:service>Standard</g:service>')
        xml.append('        <g:price>0 SAR</g:price>')
        xml.append('      </g:shipping>')
        xml.append('    </item>')
        
    xml.append('  </channel>')
    xml.append('</rss>')
    
    try:
        with open('product-feed.xml', 'w', encoding='utf-8') as f:
            f.write('\n'.join(xml))
        print("Done! product-feed.xml generated successfully")
    except (OSError, IOError) as e:
        print(f"❌ Error writing product-feed.xml: {e}")
    except Exception as e:
        print(f"❌ Unexpected error writing file: {e}")

if __name__ == "__main__":
    fix_product_feed()
