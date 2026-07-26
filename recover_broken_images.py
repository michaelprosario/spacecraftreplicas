import json
import os
import urllib.parse
import urllib.request
import time

BASE_DIR = '/workspaces/spacecraftreplicas'
CDX_RAW = os.path.join(BASE_DIR, 'cdx_raw.json')
PUBLIC_IMAGES = os.path.join(BASE_DIR, 'public', 'images')
BROKEN_MD = os.path.join(BASE_DIR, 'brokenImages.md')

# List of missing image target filenames
target_missing = [
    "IMG_0203-150x112.jpg", "IMG_0204-150x112.jpg", "IMG_0205-150x112.jpg",
    "IMG_0206-150x112.jpg", "IMG_0207-150x112.jpg", "IMG_0208-150x112.jpg",
    "IMG_0209-150x112.jpg", "IMG_0210-150x112.jpg", "CNC2-252x300.jpg",
    "IMG_5322-113x150.jpg", "N42BP in LV RM_small.jpg", "Cockpit1_small.jpg",
    "Cockpit3_small.jpg", "Front2_small.jpg", "560A0061_small.JPG",
    "IMG_0122-300x225.jpg", "IMG_1159-300x225.jpg", "image003_small.jpg",
    "image005_small.jpg", "image007_small.jpg", "heatshield1_small.jpg",
    "heatshield2_small.jpg", "panel13e_small.jpg", "panel16_small.jpg",
    "panel18_small.jpg", "panel20a_small.jpg", "img_2192_small.jpg",
    "periscope0_small.jpg"
]

print(f"Targeting recovery for {len(target_missing)} broken image files...")

with open(CDX_RAW, 'r') as f:
    cdx_data = json.load(f)

header = cdx_data[0]
rows = cdx_data[1:]

found_in_cdx = {}

for r in rows:
    orig, ts, mime, status, digest = r[0], r[1], r[2], r[3], r[4]
    if status == '200':
        orig_clean = urllib.parse.unquote(orig)
        filename = os.path.basename(orig_clean.split('?')[0])
        
        for target in target_missing:
            target_clean = urllib.parse.unquote(target)
            # Check exact or partial match
            base_target = target_clean.split('-')[0].split('_')[0].lower()
            
            if target_clean.lower() == filename.lower() or (len(base_target) > 3 and base_target in filename.lower() and ('image' in mime or filename.lower().endswith(('.jpg','.png','.gif')))):
                if target not in found_in_cdx:
                    found_in_cdx[target] = []
                found_in_cdx[target].append({
                    'orig': orig,
                    'ts': ts,
                    'mime': mime,
                    'filename': filename
                })

print("\n--- CDX Search Results for Missing Images ---")
recovered_count = 0
downloaded_files = []

for target in target_missing:
    if target in found_in_cdx:
        best_match = found_in_cdx[target][-1]
        print(f"✅ Found match for '{target}': {best_match['filename']} (TS: {best_match['ts']})")
        
        # Attempt to download
        ts = best_match['ts']
        orig_url = best_match['orig']
        wayback_url = f"https://web.archive.org/web/{ts}id_/{orig_url}"
        
        sanitized_filename = target.replace(' ', '_').replace('%20', '_')
        dest_path = os.path.join(PUBLIC_IMAGES, sanitized_filename)
        
        req = urllib.request.Request(wayback_url, headers={'User-Agent': 'Mozilla/5.0'})
        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = resp.read()
                if len(data) > 0:
                    with open(dest_path, 'wb') as out_f:
                        out_f.write(data)
                    recovered_count += 1
                    downloaded_files.append(sanitized_filename)
                    print(f"   -> Successfully downloaded and saved to {dest_path} ({len(data)} bytes)")
        except Exception as e:
            print(f"   -> Download failed: {e}")
    else:
        # Try live query CDX API with wildcard
        base_keyword = target.split('-')[0].split('_')[0].split('.')[0]
        if len(base_keyword) >= 3:
            cdx_query = f"https://web.archive.org/cdx/search/cdx?url=spacecraftreplicas.com/*{base_keyword}*&output=json&statuscode=200"
            try:
                time.sleep(0.2)
                req = urllib.request.Request(cdx_query, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req, timeout=10) as resp:
                    live_data = json.loads(resp.read().decode('utf-8'))
                    if len(live_data) > 1:
                        match_row = live_data[1]
                        orig_u, ts_u = match_row[2], match_row[1]
                        wayback_url = f"https://web.archive.org/web/{ts_u}id_/{orig_u}"
                        sanitized_filename = target.replace(' ', '_').replace('%20', '_')
                        dest_path = os.path.join(PUBLIC_IMAGES, sanitized_filename)
                        
                        req_img = urllib.request.Request(wayback_url, headers={'User-Agent': 'Mozilla/5.0'})
                        with urllib.request.urlopen(req_img, timeout=10) as img_resp:
                            data = img_resp.read()
                            if len(data) > 0:
                                with open(dest_path, 'wb') as out_f:
                                    out_f.write(data)
                                recovered_count += 1
                                downloaded_files.append(sanitized_filename)
                                print(f"✅ Found via CDX Wildcard for '{target}': {orig_u}")
                    else:
                        print(f"❌ Uncaptured in archive: '{target}'")
            except Exception as e:
                print(f"❌ Uncaptured in archive: '{target}' ({e})")
        else:
            print(f"❌ Uncaptured in archive: '{target}'")

print(f"\n--- Recovery Summary ---")
print(f"Recovered {recovered_count}/{len(target_missing)} broken images from Wayback Machine!")
