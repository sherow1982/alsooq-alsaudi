#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
import sys
import requests
import re
from datetime import datetime

# قائمة هاشتاج محافظات السعودية
SAUDI_REGIONS = [
    "الرياض", "جدة", "مكة", "الدمام", "المدينة_المنورة", "الخبر", "الطائف", "الأحساء", "بريدة", "تبوك", 
    "الجبيل", "حائل", "خميس_مشيط", "أبها", "ينبع", "نجران", "جازان", "الظهران", "حفر_الباطن", "عنيزة"
]

print("🚀 بدء تجهيز محتوى المنشور...")

# تحميل المنتجات
try:
    with open('products.json', 'r', encoding='utf-8') as f:
        products = json.load(f)
    print(f"✅ تم تحميل {len(products)} منتج")
except Exception as e:
    print(f"❌ خطأ في تحميل المنتجات: {e}")
    sys.exit(1)

# قراءة آخر منتج تم نشره
index_file = 'scripts/post_index.txt'
if os.path.exists(index_file):
    with open(index_file, 'r') as f:
        last_index = int(f.read().strip())
    print(f"📊 آخر منتج تم نشره: {last_index}")
else:
    last_index = -1
    print("📊 هذا أول نشر")

next_index = (last_index + 1) % len(products)
product = products[next_index]
print(f"📦 المنتج المختار: #{product['id']} - {product['title'][:50]}...")

# معالجة هاشتاج اسم المنتج
def sanitize_hashtag(text):
    text = re.sub(r'[\W]+', '_', text.strip())
    text = re.sub(r'_+', '_', text)
    return text.strip('_')

prod_tag = f"#{sanitize_hashtag(product.get('title',''))}"
regions_tags = ' '.join(f"#{x}" for x in SAUDI_REGIONS)

# تجهيز نص التغريدة
title = product['title']
price = product.get('price', '')
sale_price = product.get('sale_price', '')
product_id = product['id']

# رابط واتساب
whatsapp_number = "201110760081"
default_msg = f"مرحباً، أريد الاستفسار عن المنتج رقم {product_id} ({title})"
whatsapp_link = f"https://wa.me/{whatsapp_number}?text={requests.utils.quote(default_msg)}"

# رابط المنتج
product_url = f"https://sherow1982.github.io/alsooq-alsaudi/products/{product_id}.html"

# بناء الرسالة
message = f"🔥 {title}\n\n"
if sale_price and sale_price != price:
    message += f"💰 السعر: ~{price}~ ريال\n✨ العرض: {sale_price} ريال\n"
else:
    message += f"💰 السعر: {price} ريال\n"
message += f"\n📲 اطلب على واتساب: {whatsapp_link}\n"
message += f"🛒 صفحة المنتج: {product_url}\n"
message += f"\n{prod_tag} #السوق_السعودي #عروض #تسوق {regions_tags}"

print(f"📝 طول التغريدة: {len(message)} حرف")

# حفظ البيانات في ملف JSON
post_data = {
    "id": product_id,
    "title": title,
    "image_url": product.get('image_link', ''),
    "price": price,
    "sale_price": sale_price,
    "whatsapp_link": whatsapp_link,
    "product_url": product_url,
    "tweet_text": message,
    "timestamp": datetime.now().isoformat(),
    "index": next_index
}

# حفظ في ملف للاستخدام
with open('scripts/ready_post.json', 'w', encoding='utf-8') as f:
    json.dump(post_data, f, ensure_ascii=False, indent=2)

print("\n" + "="*60)
print("✅ تم تجهيز المنشور بنجاح!")
print("="*60)
print(f"\n📸 رابط الصورة:\n{post_data['image_url']}")
print(f"\n📝 النص الكامل للتغريدة:\n{message}")
print(f"\n📲 رابط الواتساب المباشر:\n{whatsapp_link}")
print("\n" + "="*60)
print("💡 المنشور محفوظ في: scripts/ready_post.json")
print("💡 يمكنك نسخه ونشره يدوياً على تويتر")
print("="*60)

# حفظ الفهرس التالي
with open(index_file, 'w') as f:
    f.write(str(next_index))
print(f"\n✅ تم حفظ الفهرس: {next_index}")
print(f"📊 المنتج التالي سيكون: {(next_index + 1) % len(products)}")

print("\n🎉 تم إكمال العملية بنجاح!")
