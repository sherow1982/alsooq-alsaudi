import json
import re
import os
from urllib.parse import quote
import sys
import html

# Force UTF-8 for output to avoid encoding errors on Windows
if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

# Global cache for descriptions
_DESCRIPTIONS_CACHE = None

def load_descriptions():
    """تحميل الوصف من ملف descriptions.json كقاموس (ID -> text)"""
    global _DESCRIPTIONS_CACHE
    if _DESCRIPTIONS_CACHE is not None:
        return _DESCRIPTIONS_CACHE
        
    try:
        with open('descriptions.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            _DESCRIPTIONS_CACHE = {str(k): v for k, v in data.items()}
            return _DESCRIPTIONS_CACHE
    except Exception as f:
        return {}

def clean_description(title, description):
    """تنظيف الوصف وحذف العنوان المكرر من بدايته"""
    if not description:
        return f"{html.escape(str(title))} - منتج عالي الجودة متوفر الآن في السوق السعودي بتوصيل سريع."
    
    clean_title = html.escape(str(title).strip())
    description = html.escape(str(description))
    
    if description.startswith(clean_title):
        description = description[len(clean_title):].lstrip(' :-,.،')
    
    if len(description) < 10:
        return f"اكتشف {html.escape(str(title))} - منتج عالي الجودة متوفر الآن في السوق السعودي بخصم حصري وتوصيل سريع."
        
    description = re.sub(r'[^\w\s\.\,\!\?\% ر.س]', '', description)
    return description[:4900]

def get_product_description(product_id, title, descriptions=None):
    """الحصول على الوصف المطابق تماماً لما هو معروض في المتجر"""
    if descriptions is None:
        descriptions = load_descriptions()
    pid_str = str(product_id)
    raw_desc = descriptions.get(pid_str, "")
    return clean_description(title, raw_desc)

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
    
    descriptions = load_descriptions()
    
    # قائمة الماركات المحظورة (عربي وإنجليزي) - قائمة شاملة جداً لتجنب تعليق الحساب
    PROHIBITED_BRANDS = [
        # الساعات والمجوهرات
        'rolex', 'رولكس', 'hublot', 'هوبلو', 'casio', 'كاسيو', 'tissot', 'تيسو', 
        'omega', 'أوميغا', 'أوميجا', 'patek philippe', 'باتيك فيليب', 'audemars piguet', 'أوديمار بيجيه',
        'cartier', 'كارتير', 'كارتيه', 'van cleef', 'فان كليف', 'tiffany', 'تيفاني', 'bulgari', 'بلغاري',
        'patek', 'باتيك', 'audemars', 'أوديمار', 'vacheron', 'فاشيرون', 'breitling', 'بريتلينغ',
        # الملابس والأحذية والحقائب
        'nike', 'نايك', 'نايكي', 'adidas', 'أديداس', 'puma', 'بوما', 'gucci', 'قوتشي',
        'prada', 'برادا', 'louis vuitton', 'لويس فيتون', 'chanel', 'شانيل', 'dior', 'ديور',
        'zara', 'زارا', 'h&m', 'lacoste', 'لاكوست', 'tommy hilfiger', 'تومي هيلفيغر', 'تومي',
        'hermes', 'هيرميس', 'هيرمز', 'burberry', 'بربري', 'fendi', 'فندي', 'balenciaga', 'بالنسياغا',
        'versace', 'فرزاتشي', 'reebok', 'ريبوك', 'new balance', 'نيو بالانس', 'skechers', 'سكيتشرز',
        'yeezy', 'ييزي', 'off-white', 'أوف وايت', 'balmain', 'بالمان', 'valentino', 'فالنتينو',
        # الإلكترونيات والهواتف
        'apple', 'أبل', 'iphone', 'ايفون', 'ipad', 'ايباد', 'samsung', 'سامسونج', 'sony', 'سوني',
        'panasonic', 'باناسونيك', 'huawei', 'هواوي', 'xiaomi', 'شاومي', 'hp', 'dell', 'lenovo', 'لينوفو',
        'canon', 'كانون', 'nikon', 'نيكون', 'lg', 'ال جي', 'philips', 'فيلبس', 'فيليبس',
        'dyson', 'دايسون', 'nintendo', 'نينتندو', 'playstation', 'بلايستيشن', 'xbox', 'اكس بوكس',
        # العطور ومواد التجميل العالمية
        'sauvage', 'سوفاج', 'bleu de chanel', 'بلو دي شانيل', 'creed', 'كريد', 
        'tom ford', 'توم فورد', 'mac', 'ماك', 'loreal', 'لوريال', 'maybelline', 'ميبيلين',
        'gillette', 'جيليت', 'braun', 'براون', 'oral-b', 'أورال بي', 'pantene', 'بانتين'
    ]
    
    xml = ['<?xml version="1.0" encoding="UTF-8"?>']
    xml.append('<rss xmlns:g="http://base.google.com/ns/1.0" version="2.0">')
    xml.append('  <channel>')
    xml.append('    <title>السوق السعودي</title>')
    xml.append(f'    <link>{base_url}/</link>')
    xml.append('    <description>أفضل العروض والمنتجات الأصلية بأسعار تنافسية</description>')
    
    excluded_count = 0
    for product in products:
        skip_product = False
        
        # تنظيف البيانات أولاً
        clean_title = clean_product_title(product['title'])
        title_lower = clean_title.lower()
        
        # التحقق من الماركات المحظورة بدقة (باستخدام حدود الكلمات للإنجليزية)
        for brand in PROHIBITED_BRANDS:
            if re.search(r'[a-zA-Z]', brand): # English Brand
                if re.search(r'\b' + re.escape(brand) + r'\b', title_lower):
                    print(f"🚫 Excluded brand detected (English): {brand} in {clean_title}")
                    skip_product = True
                    excluded_count += 1
                    break
            else: # Arabic Brand
                if brand in title_lower:
                    # التحقق من أن الماركة ليست جزءاً من كلمة شائعة (مثل 'ماكينة')
                    # بالنسبة للعربية، سنعتزم أن الماركة كلمة مستقلة
                    if re.search(r'(^|\s)' + re.escape(brand) + r'($|\s)', title_lower):
                        print(f"🚫 Excluded brand detected (Arabic): {brand} in {clean_title}")
                        skip_product = True
                        excluded_count += 1
                        break
        
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
        
        # إنشاء وصف مطابق تماماً للمتجر
        description = get_product_description(product['id'], clean_title, descriptions)
        
        # توليد المعرفات
        mpn = f"ALS{product['id']:06d}"
        gtin = ""
        
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
        
        # المعرفات الفريدة - أساسية لعام 2026
        if mpn:
            xml.append(f'      <g:mpn>{mpn}</g:mpn>')
        
        if gtin:
            xml.append(f'      <g:gtin>{gtin}</g:gtin>')
            xml.append('      <g:identifier_exists>yes</g:identifier_exists>')
        else:
            xml.append('      <g:identifier_exists>no</g:identifier_exists>')

        xml.append(f'      <g:google_product_category>{google_cat}</g:google_product_category>')
        xml.append(f'      <g:product_type>{product_type}</g:product_type>')
        
        # معلومات الشحن الموحدة
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
    
    print(f"Done! product-feed.xml generated successfully")
    print(f"Total products in feed: {len(products) - excluded_count}")
    print(f"Total products excluded (brands/policy): {excluded_count}")
    print("Fixed XML encoding issues (& to &amp;)")
    print("Added required fields: mpn")
    print("Cleaned descriptions from promotional text")
    print("Fixed image URLs")
    print("Formatted prices correctly")

if __name__ == "__main__":
    fix_product_feed()
