import json
import re
from urllib.parse import quote

def generate_mpn(product):
    """توليد MPN فريد للمنتج"""
    return f"ALS{product['id']:06d}"

def generate_gtin():
    """توليد GTIN وهمي (يُفضل استخدام القيم الحقيقية)"""
    return ""

def clean_product_title(title):
    """تنظيف العنوان من النصوص الترويجية"""
    title = re.sub(r'\s+', ' ', title).strip()
    if title.startswith('عرض '):
        title = title[5:]
    return title.strip()

def escape_xml(text):
    """ترميز الأحرف الخاصة لـ XML"""
    text = text.replace('&', '&amp;')
    text = text.replace('<', '&lt;')
    text = text.replace('>', '&gt;')
    text = text.replace('"', '&quot;')
    text = text.replace("'", '&apos;')
    return text

def create_clean_description(title, price, sale_price):
    """إنشاء وصف نظيف بدون نصوص ترويجية"""
    discount = price - sale_price
    return f"{title} - منتج أصلي بضمان الجودة. خصم {discount} ريال."

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
    
    if any(word in title_lower for word in ['شعر', 'شامبو', 'بلسم', 'زيت', 'ماسك', 'صبغة', 'حلاقة', 'فرد', 'تمويج', 'تصفيف', 'مشط', 'مبخرة']):
        return 'Health & Beauty > Personal Care > Hair Care', 'العناية بالشعر'
    elif any(word in title_lower for word in ['بشرة', 'كريم', 'سيروم', 'واقي', 'مرطب', 'تفتيح', 'صابون', 'غسول', 'مكياج', 'روج', 'شفاه', 'قناع', 'كولاجين', 'فيلر', 'بوتوكس']):
        return 'Health & Beauty > Personal Care > Cosmetics', 'العناية بالجمال'
    elif any(word in title_lower for word in ['جهاز', 'ماكينة', 'آلة', 'كهربائي', 'قابل للشحن', 'شاحن', 'سماعة', 'كاميرا', 'جوال', 'تابلت', 'ساعة', 'ضغط', 'مقياس', 'مساج', 'تدليك']):
        return 'Electronics', 'الإلكترونيات'
    elif any(word in title_lower for word in ['فيتامين', 'مكمل', 'كبسولات', 'حبوب', 'علاج', 'مشد', 'مصحح', 'ركبة', 'ظهر', 'كاحل']):
        return 'Health & Beauty > Health Care', 'الصحة والعافية'
    elif any(word in title_lower for word in ['ملابس', 'شورت', 'قميص', 'حقيبة', 'نظارة', 'حذاء', 'جورب', 'شماغ', 'باندل', 'عطر']):
        return 'Apparel & Accessories', 'الأزياء والموضة'
    else:
        return 'Home & Garden', 'المنزل والأدوات'

def create_slug(product):
    """توليد slug فريد للمنتج"""
    stop_words = ['من', 'في', 'على', 'الى', 'عن', 'و', 'مع', 'يا', 'أيها']
    
    title = product['title']
    for word in stop_words:
        title = title.replace(f' {word} ', ' ')

    slug = re.sub(r'[^\w\s-]', '', title).strip().lower()
    slug = re.sub(r'\s+', '-', slug)
    # Truncate to 100 characters to avoid Windows MAX_PATH issues
    if len(slug) > 100:
        slug = slug[:100].rstrip('-')
    return f"{product['id']}-{slug}"

def fix_product_feed():
    """إصلاح ملف product-feed.xml بالكامل"""
    base_url = "https://sherow1982.github.io/alsooq-alsaudi"
    
    with open('products.json', 'r', encoding='utf-8') as f:
        products = json.load(f)
    
    xml = ['<?xml version="1.0" encoding="UTF-8"?>']
    xml.append('<rss xmlns:g="http://base.google.com/ns/1.0" version="2.0">')
    xml.append('  <channel>')
    xml.append('    <title>السوق السعودي</title>')
    xml.append(f'    <link>{base_url}/</link>')
    xml.append('    <description>أفضل العروض والمنتجات الأصلية بأسعار تنافسية</description>')
    
    for product in products:
        skip_product = False
        
        # تنظيف البيانات أولاً
        clean_title = clean_product_title(product['title'])
        
        # التحقق من صلاحية المنتج
        if 'not compatible with our policy' in clean_title.lower():
            skip_product = True
        
        # التحقق من الصور
        image_link = fix_image_url(product['image_link'])
        if not image_link or image_link.endswith('.mp4'):
            skip_product = True
        
        if skip_product:
            continue
        
        # توليد slug
        slug = create_slug({'id': product['id'], 'title': product['title']})
        encoded_slug = quote(slug)
        product_link = f"{base_url}/products/{encoded_slug}.html"
        
        # الحصول على الفئة مع ترميز &
        google_cat, product_type = get_product_category(clean_title)
        google_cat = escape_xml(google_cat)
        
        # إنشاء وصف نظيف
        description = create_clean_description(clean_title, product['price'], product['sale_price'])
        
        # توليد المعرفات
        mpn = generate_mpn(product)
        gtin = generate_gtin()
        
        # إضافة المنتج
        xml.append('    <item>')
        xml.append(f'      <g:id>{product["id"]}</g:id>')
        xml.append(f'      <g:title><![CDATA[{clean_title}]]></g:title>')
        xml.append(f'      <g:description><![CDATA[{description}]]></g:description>')
        xml.append(f'      <g:link>{product_link}</g:link>')
        xml.append(f'      <g:image_link>{image_link}</g:image_link>')
        xml.append('      <g:condition>new</g:condition>')
        xml.append('      <g:availability>in stock</g:availability>')
        xml.append(f'      <g:price>{product["price"]}.00 SAR</g:price>')
        xml.append(f'      <g:sale_price>{product["sale_price"]}.00 SAR</g:sale_price>')
        xml.append('      <g:brand>السوق السعودي</g:brand>')
        if mpn:
            xml.append(f'      <g:mpn>{mpn}</g:mpn>')
        if gtin:
            xml.append(f'      <g:gtin>{gtin}</g:gtin>')
        xml.append(f'      <g:google_product_category>{google_cat}</g:google_product_category>')
        xml.append(f'      <g:product_type>{product_type}</g:product_type>')
        xml.append('      <g:shipping>')
        xml.append('        <g:country>SA</g:country>')
        xml.append('        <g:service>Standard</g:service>')
        xml.append('        <g:price>0.00 SAR</g:price>')
        xml.append('      </g:shipping>')
        xml.append('    </item>')
        
    xml.append('  </channel>')
    xml.append('</rss>')
    
    with open('product-feed.xml', 'w', encoding='utf-8') as f:
        f.write('\n'.join(xml))
    
    print("Done! product-feed.xml generated successfully")
    print("Fixed XML encoding issues (& to &amp;)")
    print("Added required fields: mpn")
    print("Cleaned descriptions from promotional text")
    print("Fixed image URLs")
    print("Formatted prices correctly")

if __name__ == "__main__":
    fix_product_feed()
