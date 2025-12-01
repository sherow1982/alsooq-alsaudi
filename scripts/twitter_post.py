#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tweepy
import json
import os
import sys
import requests
from io import BytesIO
from PIL import Image
import re

# قائمة هاشتاج محافظات السعودية (يمكنك تعديلها/إضافة أخرى حسب الحاجة)
SAUDI_REGIONS = [
    "الرياض", "جدة", "مكة", "الدمام", "المدينة_المنورة", "الخبر", "الطائف", "الأحساء", "بريدة", "تبوك", 
    "الجبيل", "حائل", "خميس_مشيط", "أبها", "ينبع", "نجران", "جازان", "الظهران", "حفر_الباطن", "عنيزة"
]

# ---- إعداد المنتجات ----
with open('products.json', 'r', encoding='utf-8') as f:
    products = json.load(f)

if not products or not isinstance(products, list):
    print("❌ ملف المنتجات غير صالح")
    sys.exit(1)

index_file = 'scripts/post_index.txt'
if os.path.exists(index_file):
    with open(index_file, 'r') as f:
        last_index = int(f.read().strip())
else:
    last_index = -1

next_index = (last_index + 1) % len(products)
product = products[next_index]

# ---- بيانات تويتر ----
api_key = os.environ.get('TWITTER_API_KEY')
api_secret = os.environ.get('TWITTER_API_SECRET')
access_token = os.environ.get('TWITTER_ACCESS_TOKEN')
access_secret = os.environ.get('TWITTER_ACCESS_SECRET')

if not all([api_key, api_secret, access_token, access_secret]):
    print("❌ Twitter API keys missing!")
    sys.exit(1)

try:
    # v1.1 للميديا
    auth = tweepy.OAuth1UserHandler(api_key, api_secret, access_token, access_secret)
    api_v1 = tweepy.API(auth)

    # v2 للتويتات (بدون bearer token)
    client = tweepy.Client(
        consumer_key=api_key,
        consumer_secret=api_secret,
        access_token=access_token,
        access_token_secret=access_secret
    )

    # ---- تجهيز الصورة ----
    media_id = None
    if product.get('image_link'):
        try:
            response = requests.get(product['image_link'], timeout=15)
            if response.status_code == 200:
                image = Image.open(BytesIO(response.content))
                if image.mode in ('RGBA', 'LA', 'P'):
                    background = Image.new('RGB', image.size, (255, 255, 255))
                    background.paste(image, mask=image.split()[-1] if image.mode == 'RGBA' else None)
                    image = background
                img_byte_arr = BytesIO()
                image.save(img_byte_arr, format='JPEG', quality=90)
                img_byte_arr.seek(0)
                media = api_v1.media_upload(filename="product.jpg", file=img_byte_arr)
                media_id = media.media_id
        except Exception as e:
            print(f"⚠️ فشل رفع الصورة: {e}")
    
    # ---- معالجة هاشتاج اسم المنتج ----
    def sanitize_hashtag(text):
        text = re.sub(r'[\W]+', '_', text.strip())
        # حذف التكرار أو الunderscore الزائد
        text = re.sub(r'_+', '_', text)
        return text.strip('_')
    prod_tag = f"#{sanitize_hashtag(product.get('title',''))}"

    # هاشتاجات المناطق
    regions_tags = ' '.join(f"#{x}" for x in SAUDI_REGIONS)

    # ---- تجهيز نص التغريدة ----
    title = product['title']
    price = product.get('price', '')
    sale_price = product.get('sale_price', '')
    product_id = product['id']
    
    # رابط واتساب (مثال: الرقم هو 966XXXXXXXXX غيّره لرقمك)
    whatsapp_number = "966XXXXXXXXX"
    default_msg = f"مرحباً، أريد الاستفسار عن المنتج رقم {product_id} ({title})"
    whatsapp_link = f"https://api.whatsapp.com/send?phone={whatsapp_number}&text={requests.utils.quote(default_msg)}"

    # رابط المنتج
    product_url = f"https://sherow1982.github.io/alsooq-alsaudi/products/{product_id}.html"

    message = f"🔥 {title}\n\n"
    if sale_price and sale_price != price:
        message += f"💰 السعر: ~{price}~ ريال\n✨ العرض: {sale_price} ريال\n"
    else:
        message += f"💰 السعر: {price} ريال\n"
    message += f"\n📲 اطلب على واتساب: {whatsapp_link}\n"
    message += f"🛒 صفحة المنتج: {product_url}\n"
    message += f"\n{prod_tag} #السوق_السعودي #عروض #تسوق {regions_tags}"
    
    # ---- نشر التغريدة ----
    if media_id:
        result = client.create_tweet(text=message, media_ids=[media_id])
    else:
        result = client.create_tweet(text=message)
    print(f"✅ نشر التغريدة بنجاح (منتج {product_id}) - Tweet ID: {result.data['id']}")

    # ---- حفظ الفهرس التالي ----
    with open(index_file, 'w') as f:
        f.write(str(next_index))
except Exception as e:
    print(f"❌ خطأ: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
