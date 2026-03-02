#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import shutil

# Problem IDs with case issues
files_to_fix = [
    ("909-MIONE-F6-جوال.html", "909-mione-f6-جوال.html"),
    ("1950-LED-شاشة-عرض.html", "1950-led-شاشة-عرض.html"),
    ("474-باودر-تبيض-الاسنان-5Days.html", "474-باودر-تبيض-الاسنان-5days.html"),
    ("170-جهاز-ازالة-شعر-الجسم-بالكامل-Blawless.html", "170-جهاز-ازالة-شعر-الجسم-بالكامل-blawless.html"),
    ("907-تابلت-للأطفال-Q75X-Proضمان-6-شهور.html", "907-تابلت-للأطفال-q75x-proضمان-6-شهور.html"),
    ("264-عرض-4-ماسك-Night-Wrapping-بالكولاجين.html", "264-عرض-4-ماسك-night-wrapping-بالكولاجين.html"),
    ("1517-عرض-3-معجون-عجيب-لأصلاح-البلاط-Tile-Reform.html", "1517-عرض-3-معجون-عجيب-لأصلاح-البلاط-tile-reform.html"),
    ("674-ساعة-سمارت-Ultra-T8.html", "674-ساعة-سمارت-ultra-t8.html"),
    ("1084-موقد-الرحلات-DLC-للتخييم-بضمان-عامين.html", "1084-موقد-الرحلات-dlc-للتخييم-بضمان-عامين.html"),
    ("742-هاتف-SU-Max-12.html", "742-هاتف-su-max-12.html"),
    ("1109-مصيدة-الحشرات-بمنفذ-USB.html", "1109-مصيدة-الحشرات-بمنفذ-usb.html"),
    ("675-ساعة-سمارت-Ultra-T8.html", "675-ساعة-سمارت-ultra-t8.html")
]

created = 0
for src_name, dst_name in files_to_fix:
    src = os.path.join('products', src_name)
    dst = os.path.join('products', dst_name)
    
    if os.path.exists(src) and not os.path.exists(dst):
        shutil.copy2(src, dst)
        print(f"Created: {dst_name}")
        created += 1

print(f"\nCreated {created} lowercase versions")
