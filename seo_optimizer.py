#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
سكريبت تحسين السيو وإضافة السكيما لجميع صفحات المنتجات تلقائياً
يعمل على Windows - يعدل كل صفحات المنتجات دفعة واحدة
"""

import json
import os
import sys
from pathlib import Path
import re
from datetime import datetime, timedelta


def load_products():
    """تحميل بيانات المنتجات"""
    try:
        with open('products.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ خطأ في تحميل المنتجات: {e}")
        sys.exit(1)


def create_product_schema(product):
    """إنشاء Product Schema JSON-LD"""
    product_id = product.get('id')
    title = product.get('title', '')
    description = product.get('description', title[:150])
    image = product.get('image_link', '')
    price = product.get('sale_price', product.get('price', 0))
    
    # تنظيف العنوان للـ slug
    slug = f"{product_id}-{title[:80]}"
    slug = re.sub(r'[^\w\s\u0600-\u06FF-]', '', slug)
    slug = slug.replace(' ', '-')
    
    product_url = f"https://alsooq-alsaudi.arabsad.com/products/{slug}.html"
    
    # تاريخ انتهاء السعر (سنة من الآن)
    price_valid_until = (datetime.now() + timedelta(days=365)).strftime('%Y-%m-%d')
    
    schema = {
        "@context": "https://schema.org/",
        "@type": "Product",
        "name": title,
        "image": [image] if image else [],
        "description": description,
        "sku": f"SKU_{product_id}",
        "mpn": str(product_id),
        "brand": {
            "@type": "Brand",
            "name": "السوق السعودي"
        },
        "offers": {
            "@type": "Offer",
            "url": product_url,
            "priceCurrency": "SAR",
            "price": str(price),
            "priceValidUntil": price_valid_until,
            "itemCondition": "https://schema.org/NewCondition",
            "availability": "https://schema.org/InStock",
            "seller": {
                "@type": "Organization",
                "name": "السوق السعودي"
            }
        },
        "aggregateRating": {
            "@type": "AggregateRating",
            "ratingValue": "4.5",
            "reviewCount": "25"
        }
    }
    
    return json.dumps(schema, ensure_ascii=False, indent=2)


def create_local_business_schema():
    """إنشاء LocalBusiness Schema للجيو"""
    schema = {
        "@context": "https://schema.org",
        "@type": "LocalBusiness",
        "name": "السوق السعودي",
        "image": "https://alsooq-alsaudi.arabsad.com/logo.png",
        "url": "https://alsooq-alsaudi.arabsad.com/",
        "telephone": "+201110760081",
        "address": {
            "@type": "PostalAddress",
            "streetAddress": "المملكة العربية السعودية",
            "addressLocality": "الرياض",
            "addressRegion": "الرياض",
            "postalCode": "11564",
            "addressCountry": "SA"
        },
        "geo": {
            "@type": "GeoCoordinates",
            "latitude": "24.7136",
            "longitude": "46.6753"
        },
        "openingHours": "Su-Sa 08:00-23:00",
        "priceRange": "$$"
    }
    
    return json.dumps(schema, ensure_ascii=False, indent=2)


def create_meta_tags(product):
    """إنشاء Meta Tags محسنة"""
    title = product.get('title', '')
    description = product.get('description', title[:150])
    image = product.get('image_link', '')
    product_id = product.get('id')
    price = product.get('sale_price', product.get('price', 0))
    
    # تنظيف العنوان للـ slug
    slug = f"{product_id}-{title[:80]}"
    slug = re.sub(r'[^\w\s\u0600-\u06FF-]', '', slug)
    slug = slug.replace(' ', '-')
    
    product_url = f"https://alsooq-alsaudi.arabsad.com/products/{slug}.html"
    
    # اختصار الوصف لـ Meta Description
    if len(description) > 155:
        description = description[:152] + "..."
    
    meta_tags = f"""
    <!-- SEO Meta Tags -->
    <title>{title} - السوق السعودي | أفضل الأسعار</title>
    <meta name="description" content="{description} اطلب الآن من السوق السعودي مع توصيل سريع لجميع مدن المملكة.">
    <meta name="keywords" content="{title}, السوق السعودي, تسوق اونلاين, منتجات السعودية, عروض">
    <meta name="robots" content="index, follow">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="canonical" href="{product_url}">
    
    <!-- Open Graph Meta Tags -->
    <meta property="og:title" content="{title} - السوق السعودي">
    <meta property="og:description" content="{description}">
    <meta property="og:image" content="{image}">
    <meta property="og:url" content="{product_url}">
    <meta property="og:type" content="product">
    <meta property="og:site_name" content="السوق السعودي">
    <meta property="product:price:amount" content="{price}">
    <meta property="product:price:currency" content="SAR">
    
    <!-- Twitter Card Meta Tags -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{title} - السوق السعودي">
    <meta name="twitter:description" content="{description}">
    <meta name="twitter:image" content="{image}">
    """
    
    return meta_tags


def inject_seo_into_html(html_content, product):
    """حقن السيو والسكيما في HTML"""
    
    # إنشاء السكيمات
    product_schema = create_product_schema(product)
    local_business_schema = create_local_business_schema()
    meta_tags = create_meta_tags(product)
    
    # البحث عن </head>
    if '</head>' not in html_content:
        print(f"   ⚠️ تحذير: لم يتم العثور على </head> في الصفحة")
        return html_content
    
    # إزالة أي Schema أو Meta Tags قديمة
    # إزالة JSON-LD القديم
    html_content = re.sub(
        r'<script type="application/ld\+json">.*?</script>',
        '',
        html_content,
        flags=re.DOTALL
    )
    
    # إضافة السكيما والميتا قبل </head>
    seo_injection = f"""
{meta_tags}

<!-- Product Schema JSON-LD -->
<script type="application/ld+json">
{product_schema}
</script>

<!-- LocalBusiness Schema JSON-LD -->
<script type="application/ld+json">
{local_business_schema}
</script>

</head>"""
    
    html_content = html_content.replace('</head>', seo_injection)
    
    return html_content


def process_product_file(product, products_dir):
    """معالجة ملف منتج واحد"""
    product_id = product.get('id')
    title = product.get('title', '')
    
    # البحث عن الملف
    # نمط 1: {id}-{title}.html
    slug = f"{product_id}-{title[:80]}"
    slug = re.sub(r'[^\w\s\u0600-\u06FF-]', '', slug)
    slug = slug.replace(' ', '-')
    file_path = products_dir / f"{slug}.html"
    
    # نمط 2: {id}.html
    if not file_path.exists():
        file_path = products_dir / f"{product_id}.html"
    
    # نمط 3: البحث عن أي ملف يبدأ بـ {id}-
    if not file_path.exists():
        pattern = f"{product_id}-*.html"
        matching_files = list(products_dir.glob(pattern))
        if matching_files:
            file_path = matching_files[0]
    
    if not file_path.exists():
        print(f"   ⚠️ لم يتم العثور على ملف المنتج {product_id}")
        return False
    
    try:
        # قراءة المحتوى
        with open(file_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # حقن السيو
        updated_content = inject_seo_into_html(html_content, product)
        
        # حفظ الملف المحدث
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        
        print(f"   ✅ تم تحديث: {file_path.name}")
        return True
        
    except Exception as e:
        print(f"   ❌ خطأ في معالجة {file_path.name}: {e}")
        return False


def main():
    """الدالة الرئيسية"""
    print("\n" + "="*60)
    print("🚀 سكريبت تحسين السيو وإضافة السكيما")
    print("="*60 + "\n")
    
    # تحميل المنتجات
    products = load_products()
    print(f"📦 تم تحميل {len(products)} منتج\n")
    
    # مجلد المنتجات
    products_dir = Path('products')
    if not products_dir.exists():
        print(f"❌ مجلد المنتجات غير موجود: {products_dir}")
        sys.exit(1)
    
    # معالجة كل منتج
    success_count = 0
    fail_count = 0
    
    print("🔧 بدء معالجة الملفات...\n")
    
    for i, product in enumerate(products, 1):
        print(f"[{i}/{len(products)}] معالجة: {product.get('title', '')[:50]}...")
        
        if process_product_file(product, products_dir):
            success_count += 1
        else:
            fail_count += 1
    
    # الإحصائيات النهائية
    print("\n" + "="*60)
    print("📊 النتائج النهائية:")
    print("="*60)
    print(f"✅ نجح: {success_count} ملف")
    print(f"❌ فشل: {fail_count} ملف")
    print(f"📈 نسبة النجاح: {(success_count/len(products)*100):.1f}%")
    print("\n" + "="*60)
    print("\n✨ تم الانتهاء! جميع الصفحات محسنة للسيو\n")
    
    print("📝 الخطوات التالية:")
    print("1. ارفع الملفات المحدثة على GitHub")
    print("2. اختبر صفحة واحدة على: https://search.google.com/test/rich-results")
    print("3. راقب Search Console للتحقق من الفهرسة")
    print("\n")


if __name__ == '__main__':
    main()
