import os
import glob
import re
import urllib.parse
from bs4 import BeautifulSoup

BASE_DIR = '/workspaces/spacecraftreplicas'
PAGES_DIR = os.path.join(BASE_DIR, 'src', 'pages')
PUBLIC_IMAGES_DIR = os.path.join(BASE_DIR, 'public', 'images')
DIST_DIR = os.path.join(BASE_DIR, 'dist')

existing_images = set(os.listdir(PUBLIC_IMAGES_DIR))
existing_images_lower = {img.lower(): img for img in existing_images}

routes = []
if os.path.exists(DIST_DIR):
    for root, dirs, files in os.walk(DIST_DIR):
        for f in files:
            if f.endswith('.html'):
                routes.append(os.path.join(root, f))

broken_by_page = {}
total_images_checked = 0
total_broken = 0

for rpath in sorted(routes):
    rel_route = os.path.relpath(rpath, DIST_DIR)
    page_url = '/' + rel_route.replace('index.html', '').rstrip('/')
    if page_url == '/':
        page_url = '/'
        
    with open(rpath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
        
    soup = BeautifulSoup(content, 'html.parser')
    page_broken = []
    
    for img in soup.find_all('img'):
        total_images_checked += 1
        src = img.get('src', '')
        if not src:
            page_broken.append({
                'src': '(empty)',
                'img_name': '(empty)',
                'reason': 'Missing src attribute'
            })
            total_broken += 1
            continue
            
        unquoted_src = urllib.parse.unquote(src)
        img_name = os.path.basename(unquoted_src.split('?')[0])
        
        if img_name not in existing_images:
            if img_name.lower() in existing_images_lower:
                reason = f'Case mismatch (Available as `{existing_images_lower[img_name.lower()]}`)'
            else:
                reason = 'Missing from archive (`public/images/`)'
                
            page_broken.append({
                'src': src,
                'img_name': img_name,
                'reason': reason
            })
            total_broken += 1
            
    if page_broken:
        broken_by_page[page_url] = page_broken

# Generate Markdown Document
md_content = f"""# Broken Images Report: SpacecraftReplicas.com

This document contains the complete audit of broken image references across all subpages of **SpacecraftReplicas.com** (`https://opulent-spoon-r4xj95r6w5f5pw4-4321.app.github.dev/`).

---

## 📊 Summary Statistics
- **Total Pages Audited**: {len(routes)}
- **Total `<img>` Tags Inspected**: {total_images_checked}
- **Total Valid Images Loaded**: {total_images_checked - total_broken}
- **Total Broken Image References**: {total_broken}

---

## ❌ Broken Images by Page Route

"""

for page, items in broken_by_page.items():
    md_content += f"### Page: `{page}`\n"
    md_content += f"**URL**: `https://opulent-spoon-r4xj95r6w5f5pw4-4321.app.github.dev{page}`\n\n"
    md_content += "| Image Reference | Missing Filename | Reason / Status |\n"
    md_content += "| :--- | :--- | :--- |\n"
    for item in items:
        md_content += f"| `{item['src']}` | `{item['img_name']}` | {item['reason']} |\n"
    md_content += "\n---\n\n"

md_content += """
## 💡 Recommendations & Next Steps
1. **Fallback Image Placeholder**: Implement a clean CSS/SVG placeholder for missing archive photos (`onerror="this.src='/images/placeholder.svg'"`).
2. **Snapshot Search**: Search secondary Wayback Machine capture dates for missing thumbnail files (`-150x112.jpg`, `_small.jpg`).
"""

with open(os.path.join(BASE_DIR, 'brokenImages.md'), 'w', encoding='utf-8') as f:
    f.write(md_content)

print(f"Saved broken images report to brokenImages.md with {total_broken} broken image entries!")
