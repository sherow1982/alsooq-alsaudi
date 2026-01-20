#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
سكريبت تحسين السيو وإضافة السكيما لجميع صفحات المنتجات تلقائياً
يعمل على Windows - يعدل كل صفحات المنتجات دفعة واحدة - نسخة محسنة بالأداء
"""

import json
import os
import sys
from pathlib import Path
import re
from datetime import datetime, timedelta
from concurrent.futures import ProcessPoolExecutor, as_completed
from urllib.parse import quote

# Force UTF-8 for output to avoid encoding errors on Windows
if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

def create_slug(product):
    """توليد slug فريد للمنتج - يجب أن يطابق تماماً ما في generate_all_pages.py"""
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

def load_products():
    """تحميل بيانات المنتجات"""
    try:
        with open('products.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ Error loading products: {e}")
        sys.exit(1)

def create_product_schema(product):
    """إنشاء Product Schema JSON-LD متوافق مع معايير 2026"""
    product_id = product.get('id')
    title = product.get('title', '')
    description = product.get('description', title[:150])
    image = product.get('image_link', '')
    price = product.get('sale_price', product.get('price', 0))
    
    slug = create_slug(product)
    encoded_slug = quote(slug)
    product_url = f"https://sherow1982.github.io/alsooq-alsaudi/products/{encoded_slug}.html"
    
    # تاريخ انتهاء السعر (سنة من الآن)
    price_valid_until = (datetime.now() + timedelta(days=365)).strftime('%Y-%m-%d')
    
    schema = {
        "@context": "https://schema.org/",
        "@type": "Product",
        "name": title,
        "image": [image] if image else [],
        "description": description,
        "sku": f"ALS_{product_id}",
        "mpn": f"MPN_{product_id}",
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
            "hasMerchantReturnPolicy": {
                "@type": "MerchantReturnPolicy",
                "applicableCountry": "SA",
                "returnPolicyCategory": "https://schema.org/MerchantReturnFiniteReturnPeriod",
                "merchantReturnDays": 14,
                "returnMethod": "https://schema.org/ReturnByMail",
                "returnFees": "https://schema.org/FreeReturn"
            },
            "shippingDetails": {
                "@type": "OfferShippingDetails",
                "shippingRate": {
                    "@type": "MonetaryAmount",
                    "value": "0",
                    "currency": "SAR"
                },
                "deliveryTime": {
                    "@type": "ShippingDeliveryTime",
                    "handlingTime": {
                        "@type": "QuantitativeValue",
                        "minValue": 0,
                        "maxValue": 1,
                        "unitCode": "DAY"
                    },
                    "transitTime": {
                        "@type": "QuantitativeValue",
                        "minValue": 1,
                        "maxValue": 3,
                        "unitCode": "DAY"
                    }
                },
                "shippingDestination": {
                    "@type": "DefinedRegion",
                    "addressCountry": "SA"
                }
            },
            "seller": {
                "@type": "Organization",
                "name": "السوق السعودي"
            }
        },
        "aggregateRating": {
            "@type": "AggregateRating",
            "ratingValue": "4.8",
            "reviewCount": "120"
        }
    }
    
    return json.dumps(schema, ensure_ascii=False, indent=2)

def create_local_business_schema():
    """إنشاء LocalBusiness Schema للجيو"""
    schema = {
        "@context": "https://schema.org",
        "@type": "LocalBusiness",
        "name": "alsooq-alsaudi",
        "image": "https://sherow1982.github.io/alsooq-alsaudi/logo.png",
        "url": "https://sherow1982.github.io/alsooq-alsaudi/",
        "telephone": "+201110760081",
        "email": "sherow1982@gmail.com",
        "address": {
            "@type": "PostalAddress",
            "streetAddress": "المملكة العربية السعودية",
            "addressLocality": "الرياض",
            "addressRegion": "الرياض",
            "postalCode": "12211",
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
    """إنشاء Meta Tags احترافية للسوق السعودي"""
    title = product.get('title', '')
    description = product.get('description', title[:150])
    image = product.get('image_link', '')
    price = product.get('sale_price', product.get('price', 0))
    
    slug = create_slug(product)
    encoded_slug = quote(slug)
    product_url = f"https://sherow1982.github.io/alsooq-alsaudi/products/{encoded_slug}.html"
    
    # تنظيف العنوان
    clean_title = title.replace('عرض ', '').strip()
    
    # اختصار الوصد
    meta_desc = f"اشتري {clean_title} الآن بأفضل سعر في السعودية. {price} ر.س فقط. توصيل سريع، دفع عند الاستلام، ومنتجات أصلية 100%. تسوق الآن من السوق السعودي."
    if len(meta_desc) > 160:
        meta_desc = meta_desc[:157] + "..."
    
    meta_tags = f"""
    <!-- SEO Meta Tags -->
    <title>{clean_title} | أفضل سعر في السعودية | السوق السعودي</title>
    <meta name="description" content="{meta_desc}">
    <meta name="keywords" content="{clean_title}, السوق السعودي, عروض السعودية, توصيل الرياض, دفع عند الاستلام, {clean_title} سعر">
    <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="canonical" href="{product_url}">
    
    <!-- Open Graph Meta Tags -->
    <meta property="og:title" content="{clean_title} - السوق السعودي | تسوق باحترافية">
    <meta property="og:description" content="{meta_desc}">
    <meta property="og:image" content="{image}">
    <meta property="og:url" content="{product_url}">
    <meta property="og:type" content="product">
    <meta property="og:site_name" content="السوق السعودي">
    <meta property="product:price:amount" content="{price}">
    <meta property="product:price:currency" content="SAR">
    <meta property="product:availability" content="instock">
    <meta property="product:condition" content="new">
    
    <!-- Twitter Card Meta Tags -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{clean_title} - السوق السعودي">
    <meta name="twitter:description" content="{meta_desc}">
    <meta name="twitter:image" content="{image}">
    <meta name="twitter:label1" content="Price">
    <meta name="twitter:data1" content="{price} SAR">
    <meta name="twitter:label2" content="Availability">
    <meta name="twitter:data2" content="In Stock">
    """
    
    return meta_tags

def inject_seo_into_html(html_content, product, lb_schema):
    """حقن السيو والسكيما في HTML"""
    product_schema = create_product_schema(product)
    meta_tags = create_meta_tags(product)
    
    if '</head>' not in html_content:
        return html_content
    
    # 1. إزالة أي JSON-LD قديم
    html_content = re.sub(r'<script type="application/ld\+json">.*?</script>', '', html_content, flags=re.DOTALL)
    
    # 2. إزالة Meta Tags القديمة
    html_content = re.sub(r'<!-- SEO Meta Tags -->.*?<!-- Twitter Card Meta Tags -->.*?(?=</head>)', '', html_content, flags=re.DOTALL | re.IGNORECASE)

    # 3. إزالة التعليقات المتبقية
    html_content = html_content.replace('<!-- Product Schema JSON-LD -->', '')
    html_content = html_content.replace('<!-- LocalBusiness Schema JSON-LD -->', '')
    
    # إضافة السكيما والميتا
    seo_injection = f"""
{meta_tags}

<!-- Product Schema JSON-LD -->
<script type="application/ld+json">
{product_schema}
</script>

<!-- LocalBusiness Schema JSON-LD -->
<script type="application/ld+json">
{lb_schema}
</script>

</head>"""
    
    return html_content.replace('</head>', seo_injection)

def process_single_file(product, products_dir, lb_schema):
    """Worker function for single file processing"""
    try:
        slug = create_slug(product)
        file_path = products_dir / f"{slug}.html"
        
        if not file_path.exists():
            # Fallback search if exact slug doesn't match
            pattern = f"{product['id']}-*.html"
            matching_files = list(products_dir.glob(pattern))
            if matching_files:
                file_path = matching_files[0]
            else:
                return False, f"Not found: {product['id']}"

        with open(file_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        updated_content = inject_seo_into_html(html_content, product, lb_schema)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(updated_content)
            
        return True, file_path.name
    except Exception as e:
        return False, f"Error processing {product.get('id')}: {e}"

def main():
    """الدالة الرئيسية"""
    print("\n" + "="*60)
    print("Starting optimized SEO Optimization and Schema Injection")
    print("="*60 + "\n")
    
    products = load_products()
    products_dir = Path('products')
    lb_schema = create_local_business_schema()
    
    print(f"📦 Total Products: {len(products)}")
    print("Using Parallel Processing...\n")
    
    success_count = 0
    fail_count = 0
    
    import time
    start_time = time.time()
    
    with ProcessPoolExecutor() as executor:
        futures = {executor.submit(process_single_file, p, products_dir, lb_schema): p for p in products}
        
        processed_count = 0
        for future in as_completed(futures):
            processed_count += 1
            success, result = future.result()
            if success:
                success_count += 1
            else:
                fail_count += 1
                # Only print serious failures or missing files
                if "Not found" in result:
                     pass # Expected if files were moved/renamed previously but json not updated
                else:
                     print(f"❌ {result}")
            
            if processed_count % 200 == 0:
                print(f"Progress: {processed_count}/{len(products)} pages processed...")
    
    end_time = time.time()
    print(f"\nDone! Successfully updated {success_count} pages")
    if fail_count > 0:
        print(f"Skipped/Failed {fail_count} products")
    print(f"Execution Time: {end_time - start_time:.2f} seconds")
    
    print("\n📝 Final Steps:")
    print("1. Push changes to GitHub")
    print("2. Test rich results")
    print("\n")

if __name__ == '__main__':
    main()
