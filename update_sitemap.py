#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
import re
from datetime import datetime

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

def generate_sitemap():
    """Generate sitemap.xml with all pages"""
    print("Generating sitemap.xml...")
    
    # Read products file
    try:
        with open('products.json', 'r', encoding='utf-8') as f:
            products = json.load(f)
    except Exception as e:
        print(f"Error reading products file: {e}")
        return
    
    # Get current date
    current_date = datetime.now().strftime('%Y-%m-%d')
    
    # Start sitemap XML
    sitemap_content = '''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    <!-- Main Pages -->
    <url>
        <loc>https://sherow1982.github.io/alsooq-alsaudi/</loc>
        <lastmod>''' + current_date + '''</lastmod>
        <changefreq>daily</changefreq>
        <priority>1.0</priority>
    </url>
    <url>
        <loc>https://sherow1982.github.io/alsooq-alsaudi/about.html</loc>
        <lastmod>''' + current_date + '''</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.8</priority>
    </url>
    <url>
        <loc>https://sherow1982.github.io/alsooq-alsaudi/contact.html</loc>
        <lastmod>''' + current_date + '''</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.8</priority>
    </url>
    <url>
        <loc>https://sherow1982.github.io/alsooq-alsaudi/shipping.html</loc>
        <lastmod>''' + current_date + '''</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.6</priority>
    </url>
    <url>
        <loc>https://sherow1982.github.io/alsooq-alsaudi/return-policy.html</loc>
        <lastmod>''' + current_date + '''</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.6</priority>
    </url>
    <url>
        <loc>https://sherow1982.github.io/alsooq-alsaudi/terms.html</loc>
        <lastmod>''' + current_date + '''</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.5</priority>
    </url>
    <url>
        <loc>https://sherow1982.github.io/alsooq-alsaudi/privacy.html</loc>
        <lastmod>''' + current_date + '''</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.5</priority>
    </url>
    <url>
        <loc>https://sherow1982.github.io/alsooq-alsaudi/reviews.html</loc>
        <lastmod>''' + current_date + '''</lastmod>
        <changefreq>weekly</changefreq>
        <priority>0.7</priority>
    </url>
    
    <!-- Product Pages -->
'''
    
    # Add product pages
    for product in products:
        try:
            slug = create_slug(product)
            sitemap_content += f'''    <url>
        <loc>https://sherow1982.github.io/alsooq-alsaudi/products/{slug}.html</loc>
        <lastmod>{current_date}</lastmod>
        <changefreq>weekly</changefreq>
        <priority>0.9</priority>
    </url>
'''
        except Exception as e:
            print(f"Error adding product {product.get('id', 'unknown')} to sitemap: {e}")
            continue
    
    # Close sitemap XML
    sitemap_content += '</urlset>'
    
    # Write sitemap file
    try:
        with open('sitemap.xml', 'w', encoding='utf-8') as f:
            f.write(sitemap_content)
        print(f"Sitemap generated successfully with {len(products)} product pages!")
    except Exception as e:
        print(f"Error writing sitemap: {e}")

if __name__ == "__main__":
    generate_sitemap()