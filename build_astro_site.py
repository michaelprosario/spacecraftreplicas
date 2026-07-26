import os
import shutil
import glob

BASE_DIR = '/workspaces/spacecraftreplicas'
RECOVERED_DIR = os.path.join(BASE_DIR, 'recovered_site')
PUBLIC_DIR = os.path.join(BASE_DIR, 'public')
SRC_DIR = os.path.join(BASE_DIR, 'src')
DIST_DIR = os.path.join(BASE_DIR, 'dist')

os.makedirs(os.path.join(PUBLIC_DIR, 'images'), exist_ok=True)
os.makedirs(os.path.join(PUBLIC_DIR, 'pdfs'), exist_ok=True)
os.makedirs(os.path.join(SRC_DIR, 'components'), exist_ok=True)
os.makedirs(os.path.join(SRC_DIR, 'layouts'), exist_ok=True)
os.makedirs(os.path.join(SRC_DIR, 'styles'), exist_ok=True)
os.makedirs(os.path.join(SRC_DIR, 'pages'), exist_ok=True)

# Clean dist directory to ensure fresh build
if os.path.exists(DIST_DIR):
    shutil.rmtree(DIST_DIR, ignore_errors=True)

# Clean existing public/ assets
for img in glob.glob(os.path.join(PUBLIC_DIR, 'images', '*')):
    if os.path.isfile(img):
        os.remove(img)
for pdf in glob.glob(os.path.join(PUBLIC_DIR, 'pdfs', '*')):
    if os.path.isfile(pdf):
        os.remove(pdf)

print("Copying recovered images and PDFs to public/...")
for img in glob.glob(os.path.join(RECOVERED_DIR, 'assets', 'images', '*')):
    orig_name = os.path.basename(img)
    clean_name = orig_name.replace(' ', '_')
    shutil.copy(img, os.path.join(PUBLIC_DIR, 'images', orig_name))
    if clean_name != orig_name:
        shutil.copy(img, os.path.join(PUBLIC_DIR, 'images', clean_name))

for pdf in glob.glob(os.path.join(RECOVERED_DIR, 'assets', 'pdfs', '*')):
    orig_name = os.path.basename(pdf)
    clean_name = orig_name.replace(' ', '_')
    shutil.copy(pdf, os.path.join(PUBLIC_DIR, 'pdfs', orig_name))
    if clean_name != orig_name:
        shutil.copy(pdf, os.path.join(PUBLIC_DIR, 'pdfs', clean_name))

print(f"Copied images and PDFs to public/.")
