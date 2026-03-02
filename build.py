#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
سكريبت موحد لبناء المشروع بالكامل
"""
import sys
import subprocess

if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

def run(script):
    print(f"\n▶ {script}")
    subprocess.run([sys.executable, script], check=True)

if __name__ == "__main__":
    run("generate_all_pages.py")
    run("seo_optimizer.py")
    run("fix_feed_gmc.py")
    run("generate_sitemap.py")
    print("\n✅ تم بناء المشروع بنجاح")
