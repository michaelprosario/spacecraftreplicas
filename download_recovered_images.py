import json
import os
import urllib.parse
import urllib.request
import time

BASE_DIR = '/workspaces/spacecraftreplicas'
CDX_RAW = os.path.join(BASE_DIR, 'cdx_raw.json')
PUBLIC_IMAGES = os.path.join(BASE_DIR, 'public', 'images')

with open(CDX_RAW, 'r') as f:
    cdx_data = json.load(f)

header = cdx_data[0]
rows = cdx_data[1:]

url_map = {}
for r in rows:
    orig, ts, status = r[0], r[1], r[3]
    if status == '200':
        url_map[orig.lower()] = (orig, ts)

targets_to_fetch = [
    ("CNC2-252x300.jpg", "http://www.spacecraftreplicas.com/wp-content/uploads/2011/03/cnc2-252x300.jpg"),
    ("IMG_5322-113x150.jpg", "http://www.spacecraftreplicas.com/wp-content/uploads/2010/10/img_5322-113x150.jpg"),
    ("IMG_1159-300x225.jpg", "http://www.spacecraftreplicas.com/wp-content/uploads/2010/12/img_1159-300x225.jpg"),
    ("panel13e_small.jpg", "http://www.spacecraftreplicas.com/wp-content/uploads/2010/12/panel13e_small.jpg"),
    ("panel16_small.jpg", "http://www.spacecraftreplicas.com/wp-content/uploads/2010/12/panel16_small.jpg"),
    ("img_2192_small.jpg", "http://www.spacecraftreplicas.com/paper/periscope/img_2192_small.jpg"),
    ("Cockpit3_small.jpg", "http://www.spacecraftreplicas.com/wp-content/uploads/2010/12/cockpit31-150x112.jpg")
]

downloaded = 0
for target_name, clean_key in targets_to_fetch:
    if clean_key in url_map:
        orig_url, ts = url_map[clean_key]
        raw_url = f"https://web.archive.org/web/{ts}id_/{orig_url}"
        
        dest_filename = target_name.replace(' ', '_')
        dest_path = os.path.join(PUBLIC_IMAGES, dest_filename)
        
        print(f"Fetching '{target_name}' from {raw_url}...")
        req = urllib.request.Request(raw_url, headers={'User-Agent': 'Mozilla/5.0'})
        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = resp.read()
                if len(data) > 0:
                    with open(dest_path, 'wb') as out_f:
                        out_f.write(data)
                    downloaded += 1
                    print(f"  -> Saved {dest_filename} ({len(data)} bytes)")
        except Exception as e:
            print(f"  -> Error downloading: {e}")

print(f"\nSuccessfully recovered and downloaded {downloaded} missing images!")
