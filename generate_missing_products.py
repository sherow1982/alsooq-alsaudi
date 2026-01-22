#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
import re
from urllib.parse import quote

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

def generate_product_page(product):
    """Generate HTML page for product"""
    slug = create_slug(product)
    discount = round(((product['price'] - product['sale_price']) / product['price']) * 100) if product['price'] > product['sale_price'] else 0
    
    # Clean title from special characters for meta tags
    clean_title = re.sub(r'[<>"\']', '', product['title'])
    
    html_content = f'''<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="{clean_title} - متوفر الآن في السوق السعودي بسعر {product['sale_price']} ريال سعودي. شحن مجاني لجميع أنحاء المملكة.">
    <meta name="keywords" content="{clean_title}, السوق السعودي, تسوق اونلاين, منتجات أصلية">
    <title>{clean_title} | السوق السعودي</title>
    <link rel="stylesheet" href="../css/main.css">
    <link rel="icon" type="image/png" href="../logo.png">
    
    <!-- Open Graph Meta Tags -->
    <meta property="og:title" content="{clean_title}">
    <meta property="og:description" content="متوفر الآن في السوق السعودي بسعر {product['sale_price']} ريال سعودي">
    <meta property="og:image" content="{product['image_link']}">
    <meta property="og:type" content="product">
    
    <!-- Structured Data -->
    <script type="application/ld+json">
    {{
        "@context": "https://schema.org/",
        "@type": "Product",
        "name": "{clean_title}",
        "image": "{product['image_link']}",
        "description": "{clean_title}",
        "brand": {{
            "@type": "Brand",
            "name": "السوق السعودي"
        }},
        "offers": {{
            "@type": "Offer",
            "url": "https://sherow1982.github.io/alsooq-alsaudi/products/{slug}.html",
            "priceCurrency": "SAR",
            "price": "{product['sale_price']}",
            "priceValidUntil": "2025-12-31",
            "availability": "https://schema.org/InStock",
            "seller": {{
                "@type": "Organization",
                "name": "السوق السعودي"
            }}
        }}
    }}
    </script>
</head>

<body>
    <div class="topbar">
        <div class="topbar-content">
            <div class="topbar-left">
                <span>🏅 منتجات أصلية 100% بضمان السوق السعودي</span>
            </div>
            <div class="topbar-right">
                <span>📞 خدمة العملاء: +201110760081</span>
            </div>
        </div>
    </div>

    <header class="header">
        <div class="header-content">
            <div class="logo">
                <a href="../index.html">
                    <img src="../logo.png" alt="السوق السعودي">
                </a>
            </div>
            <nav class="nav-links" id="navLinks">
                <a href="../index.html">الرئيسية</a>
                <a href="../about.html">من نحن</a>
                <a href="../contact.html">تواصل معنا</a>
                <a href="https://wa.me/201110760081" class="whatsapp-cta" target="_blank">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                        <path d="M12.031 6.172c-3.181 0-5.767 2.586-5.768 5.766-.001 1.298.38 2.27 1.019 3.287l-.582 2.128 2.182-.573c.978.58 1.911.928 3.145.929 3.178 0 5.767-2.587 5.768-5.766 0-3.18-2.587-5.771-5.764-5.771zm3.392 8.244c-.144.405-.837.774-1.17.824-.299.045-.677.063-1.092-.069-.252-.08-.575-.187-.988-.365-1.739-.751-2.874-2.502-2.961-2.617-.087-.116-.708-.94-.708-1.793s.448-1.273.607-1.446c.159-.173.346-.217.462-.217s.231.006.332.012c.109.006.252-.041.397.308.145.348.499 1.223.541 1.312.041.089.068.191.008.312-.06.121-.09.197-.181.302-.09.105-.19.235-.272.316-.09.09-.184.188-.079.365.105.177.465.766.997 1.239.685.611 1.26.802 1.437.89.177.089.282.075.387-.041.105-.116.443-.518.562-.695.119-.177.239-.148.405-.087.166.061 1.054.497 1.234.587s.3.135.344.209c.044.075.044.436-.1.841z"/>
                    </svg>
                    <span>اطلب عبر واتساب</span>
                </a>
            </nav>
            <div class="menu-toggle" id="menuToggle">
                <span></span>
                <span></span>
                <span></span>
            </div>
        </div>
    </header>

    <main class="product-page">
        <div class="container">
            <nav class="breadcrumb">
                <a href="../index.html">الرئيسية</a>
                <span>/</span>
                <span>{clean_title}</span>
            </nav>

            <div class="product-details">
                <div class="product-image">
                    <img src="{product['image_link']}" alt="{clean_title}" loading="lazy">
                    {f'<span class="discount-badge">خصم {discount}%</span>' if discount > 0 else ''}
                </div>

                <div class="product-info">
                    <h1>{product['title']}</h1>
                    
                    <div class="price-section">
                        <div class="current-price">{product['sale_price']} ر.س</div>
                        {f'<div class="original-price">{product["price"]} ر.س</div>' if product['price'] > product['sale_price'] else ''}
                        {f'<div class="savings">توفر {product["price"] - product["sale_price"]} ر.س</div>' if product['price'] > product['sale_price'] else ''}
                    </div>

                    <div class="product-features">
                        <div class="feature">
                            <span class="icon">✅</span>
                            <span>منتج أصلي 100%</span>
                        </div>
                        <div class="feature">
                            <span class="icon">🚚</span>
                            <span>شحن مجاني لجميع أنحاء المملكة</span>
                        </div>
                        <div class="feature">
                            <span class="icon">💰</span>
                            <span>دفع عند الاستلام</span>
                        </div>
                        <div class="feature">
                            <span class="icon">🔄</span>
                            <span>إمكانية الإرجاع خلال 14 يوم</span>
                        </div>
                    </div>

                    <div class="order-section">
                        <a href="https://wa.me/201110760081?text=مرحباً، أريد طلب: {quote(product['title'])}" 
                           class="order-btn" target="_blank">
                            <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
                                <path d="M12.031 6.172c-3.181 0-5.767 2.586-5.768 5.766-.001 1.298.38 2.27 1.019 3.287l-.582 2.128 2.182-.573c.978.58 1.911.928 3.145.929 3.178 0 5.767-2.587 5.768-5.766 0-3.18-2.587-5.771-5.764-5.771zm3.392 8.244c-.144.405-.837.774-1.17.824-.299.045-.677.063-1.092-.069-.252-.08-.575-.187-.988-.365-1.739-.751-2.874-2.502-2.961-2.617-.087-.116-.708-.94-.708-1.793s.448-1.273.607-1.446c.159-.173.346-.217.462-.217s.231.006.332.012c.109.006.252-.041.397.308.145.348.499 1.223.541 1.312.041.089.068.191.008.312-.06.121-.09.197-.181.302-.09.105-.19.235-.272.316-.09.09-.184.188-.079.365.105.177.465.766.997 1.239.685.611 1.26.802 1.437.89.177.089.282.075.387-.041.105-.116.443-.518.562-.695.119-.177.239-.148.405-.087.166.061 1.054.497 1.234.587s.3.135.344.209c.044.075.044.436-.1.841z"/>
                            </svg>
                            اطلب الآن عبر واتساب
                        </a>
                        
                        <div class="contact-info">
                            <p>📞 للطلب والاستفسار: +201110760081</p>
                            <p>⏰ ساعات العمل: من السبت إلى الخميس 9 صباحاً - 10 مساءً</p>
                        </div>
                    </div>
                </div>
            </div>

            <div class="product-description">
                <h2>وصف المنتج</h2>
                <p>{product['title']} متوفر الآن في السوق السعودي بأفضل الأسعار. منتج أصلي 100% مع ضمان الجودة.</p>
                
                <h3>مميزات المنتج:</h3>
                <ul>
                    <li>منتج أصلي ومضمون الجودة</li>
                    <li>شحن سريع ومجاني لجميع مدن المملكة</li>
                    <li>خدمة عملاء متاحة 24/7</li>
                    <li>إمكانية الدفع عند الاستلام</li>
                    <li>ضمان الإرجاع خلال 14 يوم</li>
                </ul>
            </div>
        </div>
    </main>

    <!-- Floating WhatsApp -->
    <a href="https://wa.me/201110760081?text=مرحباً، أريد الاستفسار عن: {quote(product['title'])}" 
       class="floating-whatsapp" target="_blank" title="تواصل معنا بالواتساب">
        <svg viewBox="0 0 24 24" fill="currentColor">
            <path d="M12.031 6.172c-3.181 0-5.767 2.586-5.768 5.766-.001 1.298.38 2.27 1.019 3.287l-.582 2.128 2.182-.573c.978.58 1.911.928 3.145.929 3.178 0 5.767-2.587 5.768-5.766 0-3.18-2.587-5.771-5.764-5.771zm3.392 8.244c-.144.405-.837.774-1.17.824-.299.045-.677.063-1.092-.069-.252-.08-.575-.187-.988-.365-1.739-.751-2.874-2.502-2.961-2.617-.087-.116-.708-.94-.708-1.793s.448-1.273.607-1.446c.159-.173.346-.217.462-.217s.231.006.332.012c.109.006.252-.041.397.308.145.348.499 1.223.541 1.312.041.089.068.191.008.312-.06.121-.09.197-.181.302-.09.105-.19.235-.272.316-.09.09-.184.188-.079.365.105.177.465.766.997 1.239.685.611 1.26.802 1.437.89.177.089.282.075.387-.041.105-.116.443-.518.562-.695.119-.177.239-.148.405-.087.166.061 1.054.497 1.234.587s.3.135.344.209c.044.075.044.436-.1.841z"/>
        </svg>
    </a>

    <footer>
        <div class="footer-content">
            <div class="footer-section">
                <h3>عن السوق السعودي</h3>
                <p>نحن وجهتك الأولى لتسوق أفضل المنتجات الأصلية في المملكة، نجمع بين الجودة والفخامة وخدمة التوصيل السريع لضمان أفضل تجربة تسوق.</p>
            </div>
            <div class="footer-section">
                <h3>روابط سريعة</h3>
                <ul class="footer-links">
                    <li><a href="../index.html">الرئيسية</a></li>
                    <li><a href="../about.html">من نحن</a></li>
                    <li><a href="../contact.html">تواصل معنا</a></li>
                </ul>
            </div>
            <div class="footer-section">
                <h3>السياسات القانونية</h3>
                <ul class="footer-links">
                    <li><a href="../shipping.html">سياسة الشحن</a></li>
                    <li><a href="../return-policy.html">سياسة الإرجاع</a></li>
                    <li><a href="../terms.html">الشروط والأحكام</a></li>
                    <li><a href="../privacy.html">سياسة الخصوصية</a></li>
                </ul>
            </div>
            <div class="footer-section">
                <h3>تواصل معنا</h3>
                <p>السوق السعودي للتجارة الإلكترونية</p>
                <p>مركز خدمة العملاء: مصر</p>
                <p>نخدم عملاء المملكة العربية السعودية</p>
                <p style="margin-top: 15px; color: var(--accent-color); font-weight: bold; font-size: 1.1rem;">واتساب: +201110760081</p>
                <p style="margin-top: 5px; font-size: 0.9rem;">البريد: sherow1982@gmail.com</p>
            </div>
        </div>
        <div class="footer-bottom">
            <p>جميع الحقوق محفوظة © 2024 السوق السعودي - فخامة التسوق بين يديك</p>
        </div>
    </footer>

    <script>
        // Mobile menu
        const menuToggle = document.getElementById('menuToggle');
        const navLinks = document.getElementById('navLinks');
        menuToggle?.addEventListener('click', () => {{
            navLinks.classList.toggle('active');
            menuToggle.classList.toggle('active');
        }});
    </script>
</body>
</html>'''
    
    return html_content

def main():
    """Main function to create all product pages"""
    print("Starting product pages creation...")
    
    # Read products file
    try:
        with open('products.json', 'r', encoding='utf-8') as f:
            products = json.load(f)
    except Exception as e:
        print(f"Error reading products file: {e}")
        return
    
    # Ensure products directory exists
    if not os.path.exists('products'):
        os.makedirs('products')
        print("Created products directory")
    
    created_count = 0
    skipped_count = 0
    
    # Create page for each product
    for product in products:
        try:
            slug = create_slug(product)
            file_path = f"products/{slug}.html"
            
            # Check if file exists
            if os.path.exists(file_path):
                skipped_count += 1
                continue
            
            # Generate page content
            html_content = generate_product_page(product)
            
            # Write file
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            created_count += 1
            
            if created_count % 100 == 0:
                print(f"Created {created_count} pages...")
                
        except Exception as e:
            print(f"Error creating page for product {product.get('id', 'unknown')}: {e}")
            continue
    
    print(f"Finished!")
    print(f"Created {created_count} new pages")
    print(f"Skipped {skipped_count} existing pages")
    print(f"Total products: {len(products)}")

if __name__ == "__main__":
    main()