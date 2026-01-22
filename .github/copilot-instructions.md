# AI Coding Assistant Instructions for alsooq-alsaudi

## Project Overview
This is a static e-commerce website generator for an Arabic/Saudi marketplace. The site generates product pages from JSON data sources using Python scripts, with WhatsApp integration for orders and comprehensive SEO optimization.

## Architecture & Data Flow
- **Data Sources**: `products.json` (product catalog), `descriptions.json` (product descriptions), `reviews.json` (customer reviews)
- **Generation**: Python scripts transform JSON data into HTML pages in the `products/` directory
- **Static Site**: Hosted on GitHub Pages with Arabic RTL layout and responsive design
- **Integration**: WhatsApp ordering system, Google Analytics, Google Tag Manager

## Key Components
- **Product Pages**: Individual HTML files in `products/` directory, generated from templates in `generate_all_pages.py`
- **Main Pages**: Static HTML files (index.html, about.html, contact.html, etc.)
- **SEO Tools**: Sitemap generation, schema markup addition, feed optimization
- **Social Media**: Automated posting scripts in `scripts/` directory

## Critical Patterns & Conventions

### Product URL Structure
- **Slug Generation**: `{product_id}-{cleaned_title}.html`
- **Cleaning Rules**: Remove Arabic stop words (`من`, `في`, `على`, etc.), replace spaces with hyphens, limit to 100 chars
- **Example**: Product ID 1 "زيت شعر الحلزون" → `1-زيت-شعر-الحلزون.html`

### Image Handling
- **Format Conversion**: Convert `.webp` and `.mp4` extensions to `.jpg` in image URLs
- **Fallback**: Use product title as alt text if image fails

### Product Categorization
Use keyword matching in Arabic titles:
- Hair care: `شعر`, `شامبو`, `بلسم`, `زيت`, `ماسك`
- Beauty: `بشرة`, `كريم`, `سيروم`, `مكياج`
- Electronics: `جهاز`, `ماكينة`, `كهربائي`, `قابل للشحن`
- Health: `فيتامين`, `مكمل`, `علاج`

### WhatsApp Integration
- **Order Format**: Pre-formatted message with product details, pricing, and discount
- **Phone Number**: +201110760081 (hardcoded in scripts)
- **URL Encoding**: Use `urllib.parse.quote()` for Arabic text in WhatsApp links

### Encoding & Internationalization
- **UTF-8 Required**: Force UTF-8 output on Windows with `sys.stdout.reconfigure(encoding='utf-8')`
- **Arabic Text**: Handle RTL layout, Arabic numerals, proper escaping in HTML
- **File Operations**: Always specify `encoding='utf-8'` when reading/writing files

### Performance Optimization
- **Parallel Processing**: Use `ProcessPoolExecutor` for batch operations (page generation, SEO optimization)
- **Caching**: Cache descriptions in global variables to avoid redundant file reads
- **Progress Tracking**: Print progress every 200 items during batch processing

## Developer Workflows

### Content Generation Pipeline
1. Update `products.json` with new products
2. Update `descriptions.json` with corresponding descriptions
3. Run `python generate_all_pages.py` to create/update product pages
4. Run `python generate_sitemap.py` to update sitemap.xml
5. Run `python seo_optimizer.py` to add schema markup

### Feed Management
- **Google Merchant**: `fix_feed_gmc.py` for Google Merchant Center feed
- **Full Feed**: `fix_feed_full.py` for complete product feed
- **XML Structure**: Standard product feed format with Arabic categories

### Social Media Automation
- **Twitter Bot**: `scripts/twitter_bot.py` for automated posting
- **Post Preparation**: `scripts/prepare_post.py` to prepare content
- **Tracking**: `scripts/posted_products.json` tracks posted products

## Code Quality Standards

### Error Handling
- **Graceful Degradation**: Continue processing on individual product failures
- **Detailed Logging**: Print error messages with product IDs and titles
- **Validation**: Check file existence before processing

### HTML Generation
- **Template Consistency**: Maintain identical structure across all product pages
- **Meta Tags**: Include Open Graph tags, Arabic descriptions, proper encoding
- **Accessibility**: Alt text for images, semantic HTML structure

### Dependencies
- **Requirements**: Listed in `requirements.txt` (beautifulsoup4, lxml, requests, jinja2)
- **Python Version**: Compatible with Python 3.x, tested on Windows

## Common Tasks & Commands

### Generate All Product Pages
```bash
python generate_all_pages.py
```
Processes all products in parallel, creates HTML files in `products/` directory.

### Update SEO Optimization
```bash
python seo_optimizer.py
```
Adds JSON-LD schema markup to existing product pages.

### Generate Sitemap
```bash
python generate_sitemap.py
```
Creates `sitemap.xml` with all pages and products.

### Fix Product Feeds
```bash
python fix_feed_gmc.py  # For Google Merchant
python fix_feed_full.py  # For complete feed
```

## File Structure Reference
- `products.json`: Product catalog (id, title, price, sale_price, image_link)
- `descriptions.json`: Product descriptions keyed by ID
- `reviews.json`: Customer reviews data
- `products/`: Generated product HTML pages
- `scripts/`: Social media automation tools
- `css/main.css`: Main stylesheet for Arabic RTL layout