import os
import re

def fix_paths():
    products_dir = "products"
    files = [f for f in os.listdir(products_dir) if f.endswith('.html')]
    
    replacements = [
        (r'href="/css/main\.css"', 'href="../css/main.css"'),
        (r'href="/favicon\.svg"', 'href="../favicon.svg"'),
        (r'href="/index\.html"', 'href="../index.html"'),
        (r'src="/logo\.png"', 'src="../logo.png"'),
        (r'href="/about\.html"', 'href="../about.html"'),
        (r'href="/contact\.html"', 'href="../contact.html"'),
        (r'href="/shipping\.html"', 'href="../shipping.html"'),
        (r'href="/return-policy\.html"', 'href="../return-policy.html"'),
        (r'href="/terms\.html"', 'href="../terms.html"'),
        (r'href="/privacy\.html"', 'href="../privacy.html"'),
    ]
    
    fixed = 0
    for filename in files:
        filepath = os.path.join(products_dir, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original = content
        for pattern, replacement in replacements:
            content = re.sub(pattern, replacement, content)
        
        if content != original:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            fixed += 1
    
    print(f"Fixed {fixed} files")

if __name__ == "__main__":
    fix_paths()
