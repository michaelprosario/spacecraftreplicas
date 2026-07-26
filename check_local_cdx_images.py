import json
import os
import urllib.parse

BASE_DIR = '/workspaces/spacecraftreplicas'
CDX_RAW = os.path.join(BASE_DIR, 'cdx_raw.json')

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

with open(CDX_RAW, 'r') as f:
    cdx_data = json.load(f)

header = cdx_data[0]
rows = cdx_data[1:]

all_cdx_urls = [r[0] for r in rows if r[3] == '200']
all_cdx_filenames = {}
for u in all_cdx_urls:
    clean_u = urllib.parse.unquote(u)
    fn = os.path.basename(clean_u.split('?')[0]).lower()
    if fn:
        all_cdx_filenames[fn] = u

print(f"Total indexed HTTP 200 URLs in CDX: {len(all_cdx_urls)}")
print(f"Total unique filenames in CDX: {len(all_cdx_filenames)}")

recovered_matches = []
truly_missing = []

for target in target_missing:
    target_clean = urllib.parse.unquote(target).lower()
    base_name = target_clean.split('-')[0].split('_')[0].split('.')[0]
    
    # Try exact match
    if target_clean in all_cdx_filenames:
        recovered_matches.append((target, all_cdx_filenames[target_clean], "Exact CDX match"))
    else:
        # Search for fuzzy match in CDX index
        fuzzy = [fn for fn in all_cdx_filenames.keys() if base_name in fn and len(base_name) > 3]
        if fuzzy:
            match_fn = fuzzy[0]
            recovered_matches.append((target, all_cdx_filenames[match_fn], f"Fuzzy CDX match ({match_fn})"))
        else:
            truly_missing.append(target)

print(f"\n--- Local CDX Index Search Results ---")
print(f"Found matches for {len(recovered_matches)}/{len(target_missing)} broken images in the archive!")
for orig, url, note in recovered_matches:
    print(f"  ✅ {orig} -> {url} ({note})")

print(f"\nTruly uncaptured images ({len(truly_missing)}):")
for tm in truly_missing:
    print(f"  ❌ {tm}")
