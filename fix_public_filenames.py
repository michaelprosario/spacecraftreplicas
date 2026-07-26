import os
import glob
import urllib.parse

def sanitize_folder(folder_path):
    print(f"Sanitizing filenames in {folder_path}...")
    for fpath in glob.glob(os.path.join(folder_path, '*')):
        fname = os.path.basename(fpath)
        # Decode %20
        unquoted = urllib.parse.unquote(fname)
        # Replace spaces and %20 with underscores
        clean_name = unquoted.replace('%20', '_').replace(' ', '_')
        
        target_path = os.path.join(folder_path, clean_name)
        if target_path != fpath:
            if os.path.exists(target_path):
                os.remove(fpath)
            else:
                os.rename(fpath, target_path)
            print(f"Renamed: {fname} -> {clean_name}")

if __name__ == '__main__':
    sanitize_folder('/workspaces/spacecraftreplicas/public/pdfs')
    sanitize_folder('/workspaces/spacecraftreplicas/public/images')
