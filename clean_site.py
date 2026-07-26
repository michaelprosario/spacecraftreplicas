import os
import re
import glob
from bs4 import BeautifulSoup

BASE_DIR = '/workspaces/spacecraftreplicas/recovered_site'
PAGES_DIR = os.path.join(BASE_DIR, 'pages')
IMAGES_DIR = os.path.join(BASE_DIR, 'assets', 'images')
PDFS_DIR = os.path.join(BASE_DIR, 'assets', 'pdfs')

def clean_html_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        # Remove Wayback Machine JS injections & headers
        # Remove comment blocks starting with <!-- BEGIN WAYBACK TOOLBAR INSERT -->
        content = re.sub(r'<!-- BEGIN WAYBACK TOOLBAR INSERT -->.*?<!-- END WAYBACK TOOLBAR INSERT -->', '', content, flags=re.DOTALL)
        content = re.sub(r'<script[^>]*web\.archive\.org[^>]*>.*?</script>', '', content, flags=re.DOTALL)
        content = re.sub(r'https?://web\.archive\.org/web/\d+(?:id_)?/', '', content)

        # BeautifulSoup parsing to fix links and images
        soup = BeautifulSoup(content, 'html.parser')

        # Clean script tags pointing to archive.org
        for script in soup.find_all('script'):
            src = script.get('src', '')
            if 'archive.org' in src or '__wm' in str(script):
                script.decompose()

        # Clean links
        for a in soup.find_all('a'):
            href = a.get('href', '')
            if href:
                if 'spacecraftreplicas.com' in href:
                    clean_href = re.sub(r'https?://(?:www\.)?spacecraftreplicas\.com(?::80)?', '', href)
                    if clean_href.endswith('.pdf'):
                        pdf_name = os.path.basename(clean_href)
                        a['href'] = f"../assets/pdfs/{pdf_name}"
                    elif clean_href.endswith(('.jpg', '.png', '.gif')):
                        img_name = os.path.basename(clean_href)
                        a['href'] = f"../assets/images/{img_name}"
                    else:
                        page_name = os.path.basename(clean_href)
                        if not page_name:
                            page_name = 'index.html'
                        elif not page_name.endswith('.html'):
                            page_name += '.html'
                        a['href'] = f"./{page_name}"

        # Clean images
        for img in soup.find_all('img'):
            src = img.get('src', '')
            if src:
                img_name = os.path.basename(src.split('?')[0])
                if img_name:
                    img['src'] = f"../assets/images/{img_name}"

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(str(soup.prettify()))
            
        return True
    except Exception as e:
        print(f"Error cleaning {filepath}: {e}")
        return False

def main():
    html_files = glob.glob(os.path.join(PAGES_DIR, '*.html'))
    print(f"Found {len(html_files)} HTML files to clean in {PAGES_DIR}")
    cleaned = 0
    for f in html_files:
        if clean_html_file(f):
            cleaned += 1
    print(f"Cleaned {cleaned}/{len(html_files)} HTML pages.")

if __name__ == '__main__':
    main()
