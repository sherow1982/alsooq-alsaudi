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

# قائمة هاشتاج محافظات السعودية
SAUDI_REGIONS = [
    "الرياض", "جدة", "مكة", "الدمام", "المدينة_المنورة", "الخبر", "الطائف", "الأحساء", "بريدة", "تبوك", 
    "الجبيل", "حائل", "خميس_مشيط", "أبها", "ينبع", "نجران", "جازان", "الظهران", "حفر_الباطن", "عنيزة"
]

# تحميل المنتجات
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

# بيانات تويتر
api_key = os.environ.get('TWITTER_API_KEY')
api_secret = os.environ.get('TWITTER_API_SECRET')
access_token = os.environ.get('TWITTER_ACCESS_TOKEN')
access_secret = os.environ.get('TWITTER_ACCESS_SECRET')

if not all([api_key, api_secret, access_token, access_secret]):
    print("❌ Twitter API keys missing!")
    sys.exit(1)

try:
    # استخدام Twitter API v1.1 فقط
    auth = tweepy.OAuth1UserHandler(api_key, api_secret, access_token, access_secret)
    api = tweepy.API(auth)
    
    # التحقق من الاتصال
    api.verify_credentials()
    print("✅ تم التحقق من بيانات الاعتماد بنجاح")

    # تجهيز الصورة
    media_id = None
    if product.get('image_link'):
        try:
            response = requests.get(product['image_link'], timeout=15)
            if response.status_code == 200:
                image = Image.open(BytesIO(response.content))
                # تحويل لـ RGB إذا لزم
                if image.mode in ('RGBA', 'LA', 'P'):
                    background = Image.new('RGB', image.size, (255, 255, 255))
                    if image.mode == 'RGBA':
                        background.paste(image, mask=image.split()[-1])
                    else:
                        background.paste(image)
                    image = background
                
                # حفظ الصورة كـ JPEG
                img_byte_arr = BytesIO()
                image.save(img_byte_arr, format='JPEG', quality=90)
                img_byte_arr.seek(0)
                
                # رفع الصورة
                media = api.media_upload(filename="product.jpg", file=img_byte_arr)
                media_id = media.media_id
                print(f"✅ تم رفع الصورة: {media_id}")
        except Exception as e:
            print(f"⚠️ فشل رفع الصورة: {e}")
    
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
    
    # نشر التغريدة باستخدام API v1.1
    if media_id:
        status = api.update_status(status=message, media_ids=[media_id])
    else:
        status = api.update_status(status=message)
    
    print(f"✅ نشر التغريدة بنجاح (منتج {product_id})")
    print(f"📊 Tweet ID: {status.id}")
    print(f"🔗 الرابط: https://twitter.com/{status.user.screen_name}/status/{status.id}")

    # حفظ الفهرس التالي
    with open(index_file, 'w') as f:
        f.write(str(next_index))
    print(f"✅ تم حفظ الفهرس: {next_index}")

except tweepy.errors.Unauthorized as e:
    print(f"❌ خطأ في المصادقة: {e}")
    print("تأكد من صحة API Keys و Access Tokens")
    sys.exit(1)
except tweepy.errors.Forbidden as e:
    print(f"❌ خطأ 403 Forbidden: {e}")
    print("حسابك لا يملك صلاحيات الكتابة. تحتاج إلى:")
    print("1. App permissions مضبوطة على 'Read and Write'")
    print("2. إعادة إنشاء Access Token & Secret بعد تغيير الصلاحيات")
    sys.exit(1)
except Exception as e:
    print(f"❌ خطأ: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
