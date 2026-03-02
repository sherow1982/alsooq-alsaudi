#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

urls = [
    "products/909-mione-f6-جوال.html",
    "products/1950-led-شاشة-عرض.html",
    "products/474-باودر-تبيض-الاسنان-5days.html",
    "products/170-جهاز-ازالة-شعر-الجسم-بالكامل-blawless.html",
    "products/907-تابلت-للأطفال-q75x-proضمان-6-شهور.html",
    "products/264-عرض-4-ماسك-night-wrapping-بالكولاجين.html",
    "products/1517-عرض-3-معجون-عجيب-لأصلاح-البلاط-tile-reform.html",
    "products/674-ساعة-سمارت-ultra-t8.html",
    "products/1084-موقد-الرحلات-dlc-للتخييم-بضمان-عامين.html",
    "products/742-هاتف-su-max-12.html",
    "products/1109-مصيدة-الحشرات-بمنفذ-usb.html",
    "products/675-ساعة-سمارت-ultra-t8.html",
    "products/727-كشاف-و-كاميرا-بواى-فاى-تدعم-شريحة-بالطاقة-الشمسية.html",
    "products/1272-عرض-10--حبات-جهاز-طارد-الفئران-و-الحشرات-الالكترونى.html",
    "products/639-سماعة-حديثة-يمكن-استخدمها-فى-الترجمة-من-خلال-تطبيق.html",
    "products/816-وصلة-HDMI-محاكية-للشاشة-4K-لتحسين-العرض-والتحكم-عن-بعد.html",
    "products/1240-ماكينة-صنع-الآيس-كريم-من-DLC-بضمان-عامين.html",
    "products/270-كريم-التخلص-من-تجاعيد-منطقة-العين-gua-sha-لعلاج-الانتفاخ-وشد-الوجه.html",
    "products/1133-غطاء-طاولة-مقاوم-للماء-من-البلاستيك.html",
    "products/852-عرض-بديل-الريموت-للجوال-IOS--بديل-الريموت-للجوال-TYPE-C.html",
    "products/125-مجموعة-العناية-الطبيعية-بالشفاه----4-مرطب-شفاه-بزبدة-الشيا-وجهاز-تكبير-الشفاه-هد.html",
    "products/1031-مفرمة-اللحوم-والخضروات-الكهربائية--DLC-بضمان-عامين.html",
    "products/1042-كشاف-الطاقة-الشمسية-للمنزل-من-DLC-بضمان-عامين.html",
    "products/314-فرشاة-فرد-الشعر5-في-1-المتطورة,-ضمان-سنتين.html",
    "products/2074-وسادة-تبريد-و-تكييف-فورى-لمقعد-السيارة.html",
    "products/1919-سفينة-قارب-سريعة-تعمل-بالتحكم-عن-بعد.html",
    "products/784-سماعات-هيدفون--لاسلكية-بخاصية-الغاء--الضوضاء.html",
    "products/276-شاي-القوام-المثالي--100-جرام.html",
    "products/1265-مقعد-صلاة-للركوع-في-المنزل.html",
    "products/1158-ميكروويف-وقلاية-وصانعه-قهوة-من-اولمبيا بضمان عامين.html"
]

print("=" * 70)
print("Checking specific URLs reported as 404")
print("=" * 70)

missing = []
found = []

for url in urls:
    if os.path.exists(url):
        found.append(url)
        print(f"OK: {url}")
    else:
        missing.append(url)
        print(f"MISSING: {url}")

print("\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)
print(f"Total URLs checked: {len(urls)}")
print(f"Found: {len(found)}")
print(f"Missing: {len(missing)}")

if missing:
    print(f"\nMISSING FILES ({len(missing)}):")
    for m in missing:
        print(f"  - {m}")
else:
    print("\nAll files exist!")
