import os
import json
from datetime import datetime
import xml.etree.ElementTree as ET
from xml.dom import minidom

def generate_sitemap():
    base_url = "https://sherow1982.github.io/alsooq-alsaudi/"
    sitemap_file = "sitemap.xml"
    
    # Root elements
    urlset = ET.Element("urlset")
    urlset.set("xmlns", "http://www.sitemaps.org/schemas/sitemap/0.9")
    
    # 1. Main Static Pages
    main_pages = [
        "", "about.html", "contact.html", "shipping.html", 
        "return-policy.html", "terms.html", "privacy.html"
    ]
    
    for page in main_pages:
        url = ET.SubElement(urlset, "url")
        ET.SubElement(url, "loc").text = f"{base_url}{page}"
        ET.SubElement(url, "lastmod").text = datetime.now().strftime("%Y-%m-%d")
        ET.SubElement(url, "changefreq").text = "weekly"
        ET.SubElement(url, "priority").text = "1.0" if page == "" else "0.8"

    # 2. Product Pages
    products_dir = "products"
    if os.path.exists(products_dir):
        product_files = [f for f in os.listdir(products_dir) if f.endswith(".html")]
        print(f"Found {len(product_files)} product pages.")
        
        for p_file in product_files:
            url = ET.SubElement(urlset, "url")
            # Ensure proper URL encoding for Arabic characters happens via the generator if needed, 
            # but usually browser handled. 
            # We'll stick to the raw filename as generated previously.
            ET.SubElement(url, "loc").text = f"{base_url}products/{p_file}"
            ET.SubElement(url, "lastmod").text = datetime.now().strftime("%Y-%m-%d")
            ET.SubElement(url, "changefreq").text = "monthly"
            ET.SubElement(url, "priority").text = "0.7"

    # Save with pretty formatting
    xml_str = ET.tostring(urlset, encoding='utf-8')
    pretty_xml = minidom.parseString(xml_str).toprettyxml(indent="  ")
    
    with open(sitemap_file, "w", encoding="utf-8") as f:
        f.write(pretty_xml)
        
    print(f"Sitemap generated: {sitemap_file}")

if __name__ == "__main__":
    generate_sitemap()
