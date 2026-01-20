import json
import re
import random
from pathlib import Path
from urllib.parse import quote
from datetime import datetime
import sys
from concurrent.futures import ProcessPoolExecutor, as_completed

# Force UTF-8 for output to avoid encoding errors on Windows
if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

# Global cache for descriptions to avoid redundant loading in workers
_DESCRIPTIONS_CACHE = None

def load_descriptions():
    """تحميل الوصف من ملف descriptions.json"""
    global _DESCRIPTIONS_CACHE
    if _DESCRIPTIONS_CACHE is not None:
        return _DESCRIPTIONS_CACHE
        
    try:
        with open('descriptions.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            _DESCRIPTIONS_CACHE = list(data.values())
            return _DESCRIPTIONS_CACHE
    except Exception as e:
        print(f"⚠️ Error loading descriptions: {e}")
        return []

def get_random_description(title, descriptions=None):
    """الحصول على وصف عشوائي مناسب للمنتج"""
    if descriptions is None:
        descriptions = load_descriptions()
    if not descriptions:
        return f"{title} - منتج أصلي بضمان الجودة. اطلب الآن من السوق السعودي!"
    return random.choice(descriptions)

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

def generate_product_html(product, descriptions=None):
    """توليد صفحة HTML لمنتج واحد"""
    slug = create_slug(product)
    encoded_slug = quote(slug)
    image_link = fix_image_url(product['image_link'])
    
    discount = product['price'] - product['sale_price']
    discount_percentage = int((discount / product['price']) * 100) if product['price'] > 0 else 0
    
    description = get_random_description(product['title'], descriptions)
    
    product_url = f"https://sherow1982.github.io/alsooq-alsaudi/products/{encoded_slug}.html"
    whatsapp_message = f"""مرحباً، أريد طلب المنتج التالي:

📦 المنتج: {product['title']}
💰 السعر: {product['sale_price']} ريال (السعر الأصلي: {product['price']} ريال)
💵 التوفير: {discount} ريال ({discount_percentage}% خصم)
🔗 الرابط: {product_url}

يرجى تأكيد التوفر والتوصيل."""
    
    whatsapp_link = f"https://wa.me/201110760081?text={quote(whatsapp_message)}"
    
    google_cat, product_type = get_product_category(product['title'])
    
    html = f"""<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="{description[:160]}">
    <meta property="og:title" content="{product['title']}">
    <meta property="og:description" content="{description[:200]}">
    <meta property="og:image" content="{image_link}">
    <title>{product['title']} | السوق السعودي</title>

    <link rel="stylesheet" href="../css/main.css">

    <!-- Google Tag Manager -->
    <script>(function(w,d,s,l,i){{w[l]=w[l]||[];w[l].push({{'gtm.start':
    new Date().getTime(),event:'gtm.js'}});var f=d.getElementsByTagName(s)[0],
    j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
    'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
    }})(window,document,'script','dataLayer','GTM-KD9H36GM');</script>
    <!-- End Google Tag Manager -->
</head>
<body>
    <!-- Google Tag Manager (noscript) -->
    <noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-KD9H36GM"
    height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
    <!-- End Google Tag Manager (noscript) -->

    <div class="topbar">
        <div class="topbar-content">
            <div class="topbar-left">
                <span>🏅 منتجات أصلية 100% بضمان السوق السعودي</span>
            </div>
            <div class="topbar-right">
                <span>📞 خدمة العملاء: 201110760081</span>
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
            <nav class="nav-links">
                <a href="../index.html">الرئيسية</a>
                <a href="../about.html">من نحن</a>
                <a href="../contact.html">تواصل معنا</a>
                <a href="https://wa.me/201110760081" class="whatsapp-cta" target="_blank">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M12.031 6.172c-3.181 0-5.767 2.586-5.768 5.766-.001 1.298.38 2.27 1.019 3.287l-.582 2.128 2.182-.573c.978.58 1.911.928 3.145.929 3.178 0 5.767-2.587 5.768-5.766 0-3.18-2.587-5.771-5.764-5.771zm3.392 8.244c-.144.405-.837.774-1.17.824-.299.045-.677.063-1.092-.069-.252-.08-.575-.187-.988-.365-1.739-.751-2.874-2.502-2.961-2.617-.087-.116-.708-.94-.708-1.793s.448-1.273.607-1.446c.159-.173.346-.217.462-.217s.231.006.332.012c.109.006.252-.041.397.308.145.348.499 1.223.541 1.312.041.089.068.191.008.312-.06.121-.09.197-.181.302-.09.105-.19.235-.272.316-.09.09-.184.188-.079.365.105.177.465.766.997 1.239.685.611 1.26.802 1.437.89.177.089.282.075.387-.041.105-.116.443-.518.562-.695.119-.177.239-.148.405-.087.166.061 1.054.497 1.234.587s.3.135.344.209c.044.075.044.436-.1.841z"/></svg>
                    <span>اطلب عبر واتساب</span>
                </a>
            </nav>
        </div>
    </header>

    <main class="product-container">
        <div class="product-layout">
            <div class="product-gallery">
                <img src="{image_link}" alt="{product['title']}" loading="lazy">
            </div>
            <div class="product-details">
                <h1>{product['title']}</h1>
                
                <div class="product-price-box">
                    <div style="display: flex; flex-direction: column;">
                        <span style="font-size: 0.9rem; color: #666;">السعر الحالي</span>
                        <span class="price-current" style="font-size: 2.5rem;">{product['sale_price']} ر.س</span>
                    </div>
                    <div style="display: flex; flex-direction: column; opacity: 0.6;">
                        <span style="font-size: 0.8rem; text-decoration: line-through;">{product['price']} ر.س</span>
                        <span style="color: #e74c3c; font-weight: bold;">وفر {product['price'] - product['sale_price']} ر.س</span>
                    </div>
                </div>

                <div style="margin-bottom: 30px; color: #555; line-height: 1.8;">
                    {description}
                </div>

                <a href="{whatsapp_link}" class="whatsapp-order-btn" target="_blank">
                    <span>اطلب الآن عبر واتساب</span>
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor"><path d="M12.031 6.172c-3.181 0-5.767 2.586-5.768 5.766-.001 1.298.38 2.27 1.019 3.287l-.582 2.128 2.182-.573c.978.58 1.911.928 3.145.929 3.178 0 5.767-2.587 5.768-5.766 0-3.18-2.587-5.771-5.764-5.771zm3.392 8.244c-.144.405-.837.774-1.17.824-.299.045-.677.063-1.092-.069-.252-.08-.575-.187-.988-.365-1.739-.751-2.874-2.502-2.961-2.617-.087-.116-.708-.94-.708-1.793s.448-1.273.607-1.446c.159-.173.346-.217.462-.217s.231.006.332.012c.109.006.252-.041.397.308.145.348.499 1.223.541 1.312.041.089.068.191.008.312-.06.121-.09.197-.181.302-.09.105-.19.235-.272.316-.09.09-.184.188-.079.365.105.177.465.766.997 1.239.685.611 1.26.802 1.437.89.177.089.282.075.387-.041.105-.116.443-.518.562-.695.119-.177.239-.148.405-.087.166.061 1.054.497 1.234.587s.3.135.344.209c.044.075.044.436-.1.841z"/></svg>
                </a>

                <div class="trust-badges">
                    <div class="badge-item">✅ أصلي 100%</div>
                    <div class="badge-item">🚚 شحن مجاني</div>
                    <div class="badge-item">🔄 إرجاع سهل</div>
                    <div class="badge-item">💳 دفع عند الاستلام</div>
                </div>
            </div>
        </div>
    </main>

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
                <p>مؤسسة alsooq-alsaudi</p>
                <p>المملكة العربية السعودية، السعودية</p>
                <p>الرياض 12211</p>
                <p style="margin-top: 15px; color: var(--accent-color); font-weight: bold; font-size: 1.1rem;">واتساب: +201110760081</p>
                <p style="margin-top: 5px; font-size: 0.9rem;">البريد: sherow1982@gmail.com</p>
            </div>
        </div>
        <div class="footer-bottom">
            <p>جميع الحقوق محفوظة &copy; 2026 السوق السعودي - فخامة التسوق بين يديك</p>
        </div>
    </footer>
</body>
</html>"""

    
    return html

def process_single_product(product, descriptions):
    """Worker function to process a single product"""
    try:
        slug = create_slug(product)
        html = generate_product_html(product, descriptions)
        
        products_dir = Path('products')
        file_path = products_dir / f"{slug}.html"
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(html)
        return True, product['id']
    except Exception as e:
        return False, f"Product {product['id']}: {e}"

def main():
    """Main function to run the script"""
    print("Starting optimized product page generation...\n")
    
    products_dir = Path('products')
    products_dir.mkdir(exist_ok=True)
    
    with open('products.json', 'r', encoding='utf-8') as f:
        products = json.load(f)
    
    descriptions = load_descriptions()
    
    print(f"Total Products: {len(products)}")
    print("Using Parallel Processing...")
    
    success_count = 0
    fail_count = 0
    
    import time
    start_time = time.time()
    
    with ProcessPoolExecutor() as executor:
        # Submit all tasks
        futures = {executor.submit(process_single_product, p, descriptions): p for p in products}
        
        processed_count = 0
        for future in as_completed(futures):
            processed_count += 1
            success, result = future.result()
            if success:
                success_count += 1
            else:
                fail_count += 1
                print(f"❌ {result}")
            
            if processed_count % 200 == 0:
                print(f"Progress: {processed_count}/{len(products)} pages processed...")
    
    end_time = time.time()
    print(f"\nSuccessfully generated {success_count} product pages")
    if fail_count > 0:
        print(f"Failed to generate {fail_count} product pages")
    print(f"Execution Time: {end_time - start_time:.2f} seconds")

    print("\n" + "="*60)
    print("DONE!")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()
