import json
import urllib.request
import urllib.parse
import os

def fetch_cdx():
    print("Fetching CDX index from Wayback Machine...")
    # Request CDX index for both www.spacecraftreplicas.com and spacecraftreplicas.com
    url = "http://web.archive.org/cdx/search/cdx?url=*.spacecraftreplicas.com/*&output=json&fl=original,timestamp,mimetype,statuscode,digest,length"
    
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            data = json.loads(response.read().decode('utf-8'))
            with open('cdx_index.json', 'w') as f:
                json.dump(data, f, indent=2)
            print(f"Saved {len(data)-1} index entries to cdx_index.json")
            return data
    except Exception as e:
        print(f"Error fetching CDX index: {e}")
        return None

def analyze_cdx():
    if not os.path.exists('cdx_index.json'):
        return
    with open('cdx_index.json', 'r') as f:
        data = json.load(f)
    
    header = data[0]
    rows = data[1:]
    
    url_map = {}
    for r in rows:
        orig, ts, mime, status, digest, length = r[0], r[1], r[2], r[3], r[4], r[5]
        if status == '200':
            # Clean url key for grouping
            clean_url = orig.lower()
            if clean_url not in url_map:
                url_map[clean_url] = []
            url_map[clean_url].append({
                'orig': orig,
                'ts': ts,
                'mime': mime,
                'digest': digest,
                'length': length
            })
            
    print(f"\n--- CDX Index Summary ---")
    print(f"Total HTTP 200 URLs: {len(url_map)}")
    
    mime_counts = {}
    extensions = {}
    
    for url, snaps in url_map.items():
        latest = snaps[-1]
        m = latest['mime']
        mime_counts[m] = mime_counts.get(m, 0) + 1
        
        # Ext
        path = urllib.parse.urlparse(url).path
        ext = os.path.splitext(path)[1].lower()
        if not ext:
            ext = '(no ext / html)'
        extensions[ext] = extensions.get(ext, 0) + 1

    print("\nMime-type counts:")
    for m, c in sorted(mime_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"  {m}: {c}")

    print("\nFile extension counts:")
    for ext, c in sorted(extensions.items(), key=lambda x: x[1], reverse=True):
        print(f"  {ext}: {c}")

if __name__ == '__main__':
    fetch_cdx()
    analyze_cdx()
