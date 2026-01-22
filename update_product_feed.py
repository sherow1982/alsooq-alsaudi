#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
import re
from datetime import datetime
import html

def create_slug(product):
    """Create slug for product"""
    stop_words = ['من', 'في', 'على', 'الى', 'عن', 'و', 'مع', 'يا', 'أيها']
    title = product['title']
    
    # Remove stop words
    for word in stop_words:
        title = re.sub(f' {word} ', ' ', title, flags=re.IGNORECASE)
    
    # Clean title and create slug
    slug = title.lower().strip()
    slug = re.sub(r'[^\w\s\u0600-\u06FF-]', '', slug)  # Keep Arabic, English letters and numbers only
    slug = re.sub(r'\s+', '-', slug)  # Replace spaces with dashes
    
    # Shorten slug if too long
    if len(slug) > 100:
        slug = slug[:100].rstrip('-')
    
    return f"{product['id']}-{slug}"

def generate_product_feed():
    """Generate product-feed.xml for Google Merchant Center"""
    print("Generating product-feed.xml...")
    
    # Read products file
    try:
        with open('products.json', 'r', encoding='utf-8') as f:
            products = json.load(f)
    except Exception as e:
        print(f"Error reading products file: {e}")
        return
    
    # Start RSS feed
    feed_content = '''<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:g="http://base.google.com/ns/1.0">
    <channel>
        <title>السوق السعودي - منتجات أصلية</title>
        <link>https://sherow1982.github.io/alsooq-alsaudi/</link>
        <description>متجر السوق السعودي للمنتجات الأصلية - شحن مجاني لجميع أنحاء المملكة</description>
        <language>ar</language>
        <lastBuildDate>''' + datetime.now().strftime('%a, %d %b %Y %H:%M:%S +0000') + '''</lastBuildDate>
        
'''
    
    # Add product items
    for product in products:
        try:
            slug = create_slug(product)
            clean_title = html.escape(product['title'])
            clean_description = html.escape(f"{product['title']} - متوفر الآن في السوق السعودي بأفضل الأسعار. منتج أصلي 100% مع ضمان الجودة وشحن مجاني.")
            
            # Determine category based on title keywords
            category = "منتجات عامة"
            title_lower = product['title'].lower()
            if any(word in title_lower for word in ['شعر', 'بشرة', 'كريم', 'جمال', 'مكياج']):
                category = "الجمال والعناية"
            elif any(word in title_lower for word in ['صحة', 'فيتامين', 'علاج', 'مكمل']):
                category = "الصحة والعافية"
            elif any(word in title_lower for word in ['جهاز', 'ماكينة', 'كهربائي', 'جوال', 'ساعة']):
                category = "الإلكترونيات"
            elif any(word in title_lower for word in ['منزل', 'مطبخ', 'أدوات']):
                category = "المنزل والحديقة"
            
            feed_content += f'''        <item>
            <g:id>{product['id']}</g:id>
            <g:title>{clean_title}</g:title>
            <g:description>{clean_description}</g:description>
            <g:link>https://sherow1982.github.io/alsooq-alsaudi/products/{slug}.html</g:link>
            <g:image_link>{product['image_link']}</g:image_link>
            <g:condition>new</g:condition>
            <g:availability>in stock</g:availability>
            <g:price>{product['sale_price']} SAR</g:price>
            <g:sale_price>{product['sale_price']} SAR</g:sale_price>
            <g:brand>السوق السعودي</g:brand>
            <g:product_type>{category}</g:product_type>
            <g:google_product_category>{category}</g:google_product_category>
            <g:shipping>
                <g:country>SA</g:country>
                <g:service>شحن مجاني</g:service>
                <g:price>0 SAR</g:price>
            </g:shipping>
            <g:identifier_exists>false</g:identifier_exists>
        </item>
        
'''
        except Exception as e:
            print(f"Error adding product {product.get('id', 'unknown')} to feed: {e}")
            continue
    
    # Close RSS feed
    feed_content += '''    </channel>
</rss>'''
    
    # Write feed file
    try:
        with open('product-feed.xml', 'w', encoding='utf-8') as f:
            f.write(feed_content)
        print(f"Product feed generated successfully with {len(products)} products!")
    except Exception as e:
        print(f"Error writing product feed: {e}")

if __name__ == "__main__":
    generate_product_feed()