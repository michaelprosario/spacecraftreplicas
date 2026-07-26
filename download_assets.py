import json
import os
import sys
import time
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed

BASE_DIR = '/workspaces/spacecraftreplicas/recovered_site'
RAW_CDX = '/workspaces/spacecraftreplicas/cdx_raw.json'

os.makedirs(os.path.join(BASE_DIR, 'pages'), exist_ok=True)
os.makedirs(os.path.join(BASE_DIR, 'assets', 'images'), exist_ok=True)
os.makedirs(os.path.join(BASE_DIR, 'assets', 'pdfs'), exist_ok=True)
os.makedirs(os.path.join(BASE_DIR, 'assets', 'css'), exist_ok=True)
os.makedirs(os.path.join(BASE_DIR, 'assets', 'js'), exist_ok=True)
os.makedirs(os.path.join(BASE_DIR, 'assets', 'other'), exist_ok=True)

def categorize_and_get_target(url):
    parsed = urllib.parse.urlparse(url)
    path = parsed.path
    if not path or path == '/':
        filename = 'index.html'
        category = 'pages'
    else:
        filename = os.path.basename(path)
        if not filename or '.' not in filename:
            filename = (filename if filename else 'page') + '.html'
            category = 'pages'
        else:
            ext = os.path.splitext(filename)[1].lower()
            if ext in ['.pdf', '.doc', '.zip']:
                category = 'assets/pdfs'
            elif ext in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.ico', '.svg']:
                category = 'assets/images'
            elif ext in ['.css']:
                category = 'assets/css'
            elif ext in ['.js']:
                category = 'assets/js'
            elif ext in ['.html', '.htm']:
                category = 'pages'
            else:
                category = 'assets/other'
    
    target_dir = os.path.join(BASE_DIR, category)
    os.makedirs(target_dir, exist_ok=True)
    target_path = os.path.join(target_dir, filename)
    return category, filename, target_path

def load_cdx_items():
    with open(RAW_CDX, 'r') as f:
        data = json.load(f)
    
    rows = data[1:] # Skip header
    url_map = {}
    
    for r in rows:
        orig, ts, mime, status, digest = r[0], r[1], r[2], r[3], r[4]
        if status == '200':
            clean_url = orig.lower().split('?')[0] # ignore query params for deduplication
            if clean_url not in url_map:
                url_map[clean_url] = []
            url_map[clean_url].append({
                'orig': orig,
                'ts': ts,
                'mime': mime,
                'digest': digest
            })
            
    download_tasks = []
    seen_target_paths = set()
    
    for clean_url, snaps in url_map.items():
        latest = snaps[-1]
        orig_url = latest['orig']
        ts = latest['ts']
        
        category, filename, target_path = categorize_and_get_target(orig_url)
        
        if target_path in seen_target_paths:
            base, ext = os.path.splitext(filename)
            filename = f"{base}_{ts[-6:]}{ext}"
            target_path = os.path.join(BASE_DIR, category, filename)
            
        seen_target_paths.add(target_path)
        wayback_raw_url = f"https://web.archive.org/web/{ts}id_/{orig_url}"
        
        download_tasks.append({
            'orig_url': orig_url,
            'wayback_url': wayback_raw_url,
            'target_path': target_path,
            'category': category,
            'filename': filename
        })
        
    return download_tasks

def download_file(task):
    target_path = task['target_path']
    if os.path.exists(target_path) and os.path.getsize(target_path) > 0:
        return 'SKIP', task['filename']
    
    url = task['wayback_url']
    req = urllib.request.Request(url, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    })
    
    for attempt in range(4):
        try:
            time.sleep(0.15 * (attempt + 1)) # polite rate limiting delay
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = resp.read()
                with open(target_path, 'wb') as f:
                    f.write(data)
                return 'OK', task['filename']
        except Exception as e:
            if attempt == 3:
                return f'FAIL: {e}', task['filename']
            time.sleep(1.0 * (attempt + 1))

def main():
    tasks = load_cdx_items()
    print(f"Prepared {len(tasks)} files for download with polite rate limiting.")
    
    success = 0
    skipped = 0
    failed = 0
    
    # 2 concurrent workers to respect archive.org rate limits
    with ThreadPoolExecutor(max_workers=2) as executor:
        futures = {executor.submit(download_file, task): task for task in tasks}
        for future in as_completed(futures):
            res, fname = future.result()
            if res == 'OK':
                success += 1
            elif res == 'SKIP':
                skipped += 1
            else:
                failed += 1
                
            total_done = success + skipped + failed
            if total_done % 10 == 0 or total_done == len(tasks):
                print(f"Progress: {total_done}/{len(tasks)} (Downloaded: {success}, Skipped: {skipped}, Failed: {failed})")

    print("\n--- Download Summary ---")
    print(f"Successfully downloaded: {success}")
    print(f"Already existed (skipped): {skipped}")
    print(f"Failed downloads: {failed}")

if __name__ == '__main__':
    main()
