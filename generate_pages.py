import os
import glob
import re
import json
from bs4 import BeautifulSoup

BASE_DIR = '/workspaces/spacecraftreplicas'
RECOVERED_PAGES = os.path.join(BASE_DIR, 'recovered_site', 'pages')
PUBLIC_DIR = os.path.join(BASE_DIR, 'public')
PAGES_DIR = os.path.join(BASE_DIR, 'src', 'pages')

os.makedirs(os.path.join(PAGES_DIR, 'mercury'), exist_ok=True)
os.makedirs(os.path.join(PAGES_DIR, 'shuttle'), exist_ok=True)
os.makedirs(os.path.join(PAGES_DIR, 'paper-models'), exist_ok=True)
os.makedirs(os.path.join(PAGES_DIR, 'community'), exist_ok=True)

def extract_text_blocks(filepath):
    if not os.path.exists(filepath):
        fname = os.path.basename(filepath)
        matches = glob.glob(os.path.join(RECOVERED_PAGES, f"*{fname.replace('.html','')}*"))
        if matches:
            filepath = matches[0]
        else:
            return "Content currently being restored from archive.", []

    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    # Sanitize any link hrefs with spaces to underscores
    content = re.sub(r'href=["\']([^"\']+\.(?:pdf|doc|zip|jpg|png|gif))["\']', 
                     lambda m: f'href="{m.group(1).replace(" ", "_")}"', content, flags=re.IGNORECASE)

    soup = BeautifulSoup(content, 'html.parser')
    
    # Decompose header, footer, nav, sidebar, and widget elements
    for tag in soup(['script', 'style', 'nav', 'header', 'footer', 'aside']):
        tag.decompose()
        
    for widget in soup.find_all(['div', 'ul', 'section'], class_=re.compile(r'menu|widget|sidebar|nav|branding|header|footer', re.I)):
        widget.decompose()
        
    for widget in soup.find_all(['div', 'ul', 'section'], id=re.compile(r'menu|widget|sidebar|nav|header|footer', re.I)):
        widget.decompose()

    # Locate main entry content container
    entry = soup.find(['article', 'div', 'main'], class_=re.compile(r'entry-content|post-content|main-content|type-page|type-post', re.I))
    if not entry:
        entry = soup.find('body') or soup

    paragraphs = []
    for elem in entry.find_all(['p', 'h2', 'h3', 'h4', 'li']):
        txt = elem.get_text().strip()
        txt = re.sub(r'\s+', ' ', txt)
        if txt and len(txt) > 10:
            if not any(nav_kw in txt for nav_kw in ['Skip to content', 'Home Gallery', 'CollectSpace Mercury', 'Spacecraft Replicas Flight', 'Updated 12/20/2008']):
                if txt not in paragraphs:
                    paragraphs.append(txt)

    imgs = []
    for img in entry.find_all('img'):
        src = img.get('src', '')
        if src:
            img_name = os.path.basename(src.split('?')[0]).replace(' ', '_')
            if img_name and img_name not in imgs:
                imgs.append(img_name)

    clean_html = "\n\n".join([f"<p>{p}</p>" for p in paragraphs])
    clean_html = re.sub(r'(/pdfs/[^"\s>]+)', lambda m: m.group(1).replace(' ', '_'), clean_html)
    return clean_html, imgs

def create_astro_page(target_route, title, category, source_file):
    html_content, images = extract_text_blocks(os.path.join(RECOVERED_PAGES, source_file))
    
    img_gallery_code = ""
    if images:
        img_gallery_code = f"""
        <div style="margin-top: 2rem; display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 1rem;">
            {"".join([f'<img src="/images/{img}" alt="{title}" style="width:100%; border-radius:8px; border:1px solid var(--border-color);" />' for img in images[:8]])}
        </div>
        """

    slash_count = target_route.count('/')
    if slash_count == 0:
        layout_import = "../layouts/MainLayout.astro"
    elif slash_count == 1:
        layout_import = "../../layouts/MainLayout.astro"
    else:
        layout_import = "../../../layouts/MainLayout.astro"

    astro_code = f"""---
import MainLayout from '{layout_import}';
---

<MainLayout title="{title}">
  <div style="max-width: 900px; margin: 0 auto;">
    <span class="badge">{category}</span>
    <h1 style="font-size: 2.5rem; margin-bottom: 1.5rem;">{title}</h1>
    
    <div class="article-content">
      {html_content}
      {img_gallery_code}
    </div>
  </div>
</MainLayout>
"""

    fpath = os.path.join(PAGES_DIR, target_route)
    os.makedirs(os.path.dirname(fpath), exist_ok=True)
    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(astro_code)
    print(f"Created Clean Astro Route: src/pages/{target_route}")

routes = [
    ('about.astro', 'About Andy & Spacecraft Replicas', 'About', 'andy.html'),
    ('faq.astro', 'Frequently Asked Questions', 'FAQ', 'faq.html'),
    ('contact.astro', 'Contact Spacecraft Replicas', 'Contact', 'contact.html'),
    
    ('mercury/main-structure.astro', 'Mercury Capsule Main Structure', 'Project Mercury', 'main-structure.html'),
    ('mercury/heat-shield.astro', 'Heat Shield Construction', 'Project Mercury', 'heat-shield.html'),
    ('mercury/shingles.astro', 'Exterior Corrugated Shingles', 'Project Mercury', 'shingles.html'),
    ('mercury/aft-bulkhead.astro', 'Aft Bulkhead Assembly', 'Project Mercury', 'aft-bulkhead.html'),
    ('mercury/instrument-panels.astro', 'Cockpit Instrument Panels', 'Project Mercury', 'instrument-panels.html'),
    ('mercury/periscope.astro', 'Periscope Assembly & Fixtures', 'Project Mercury', 'periscope.html'),
    ('mercury/antenna-fairing.astro', 'Top Antenna Fairing', 'Project Mercury', 'antenna-fairing.html'),
    ('mercury/recovery-section.astro', 'Parachute Recovery System', 'Project Mercury', 'recovery-section.html'),
    ('mercury/hallmark.astro', 'Hallmark Friendship 7 Ornament Mod', 'Project Mercury', 'Hallmark1.html'),
    
    ('shuttle/1-40-shuttle.astro', '1:40 Scale Space Shuttle Build', 'Space Shuttle', 'shuttle.html'),
    ('shuttle/x-37-x-40.astro', 'X-37 & X-40A Glide Lander', 'Experimental Craft', 'x-37.html'),
    
    ('paper-models/index.astro', 'Paper Craft Models Overview', 'Paper Models', 'paper-model.html'),
    
    ('community/builders.astro', 'Community Builders Showcase', 'Community', 'builders.html'),
    ('community/collectspace.astro', 'CollectSpace Forum Collaboration', 'Community', 'collectspace.html'),
    ('community/cnc-router.astro', 'CNC Router Construction Guide', 'Community', 'cnc-router.html'),
    ('community/homebuilts.astro', 'Homebuilt Aircraft Projects', 'Community', 'homebuilts.html')
]

for route, title, cat, source in routes:
    create_astro_page(route, title, cat, source)

# Special 1: Homepage (src/pages/index.astro)
index_astro = """---
import MainLayout from '../layouts/MainLayout.astro';

const pdfCount = 112;
const imgCount = 152;
const pageCount = 125;
---

<MainLayout title="Spacecraft Replicas Historical Archive">
  <div style="text-align: center; margin: 3rem auto 2rem auto; max-width: 800px;">
    <span class="badge">Astro Rebuilt Archive</span>
    <h1 style="font-size: 3.2rem; margin: 1rem 0; background: linear-gradient(135deg, #fff 0%, var(--primary) 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
      Flight makes the imagination limitless...
    </h1>
    <p style="font-size: 1.2rem; color: var(--text-muted);">
      Historical restoration of SpacecraftReplicas.com. Featuring scale spacecraft models, blueprints, paper craft templates, Project Mercury capsules, and Space Shuttle builds.
    </p>
  </div>

  <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 1.5rem; margin: 3rem 0;">
    <div class="card" style="text-align: center;">
      <div style="font-size: 2.5rem; font-weight: 800; color: var(--primary); font-family: 'Outfit';">{pdfCount}</div>
      <div style="color: var(--text-muted); font-size: 0.9rem; text-transform: uppercase;">PDF Blueprints</div>
    </div>
    <div class="card" style="text-align: center;">
      <div style="font-size: 2.5rem; font-weight: 800; color: var(--primary); font-family: 'Outfit';">{imgCount}</div>
      <div style="color: var(--text-muted); font-size: 0.9rem; text-transform: uppercase;">Restored Photos</div>
    </div>
    <div class="card" style="text-align: center;">
      <div style="font-size: 2.5rem; font-weight: 800; color: var(--primary); font-family: 'Outfit';">{pageCount}</div>
      <div style="color: var(--text-muted); font-size: 0.9rem; text-transform: uppercase;">Archived Pages</div>
    </div>
  </div>

  <section style="margin-top: 4rem;">
    <h2 style="font-size: 2rem; margin-bottom: 1.5rem;">🚀 Explore Replica Projects</h2>
    <div class="grid-cards">
      <a href="/mercury/main-structure" class="card" style="text-decoration: none;">
        <span class="badge">Project Mercury</span>
        <h3 style="margin: 0.5rem 0;">Mercury Capsule Build</h3>
        <p style="color: var(--text-muted); font-size: 0.9rem;">Full scale & model build guides for heat shield, shingles, periscope, and instrument panels.</p>
      </a>

      <a href="/paper-models/blueprints" class="card" style="text-decoration: none;">
        <span class="badge">Blueprints & Downloads</span>
        <h3 style="margin: 0.5rem 0;">112 PDF Blueprints</h3>
        <p style="color: var(--text-muted); font-size: 0.9rem;">Downloadable PDF templates, schematics, and instructional paper craft manuals.</p>
      </a>

      <a href="/shuttle/1-40-shuttle" class="card" style="text-decoration: none;">
        <span class="badge">Space Shuttle</span>
        <h3 style="margin: 0.5rem 0;">1:40 Scale Space Shuttle</h3>
        <p style="color: var(--text-muted); font-size: 0.9rem;">Detailed 1:40 scale model construction and X-37 / X-40A glide lander project notes.</p>
      </a>

      <a href="/community/cnc-router" class="card" style="text-decoration: none;">
        <span class="badge">Special Projects</span>
        <h3 style="margin: 0.5rem 0;">CNC Router & Aviation</h3>
        <p style="color: var(--text-muted); font-size: 0.9rem;">Custom CNC router fabrication and homebuilt aircraft construction logs.</p>
      </a>
    </div>
  </section>
</MainLayout>
"""

with open(os.path.join(PAGES_DIR, 'index.astro'), 'w', encoding='utf-8') as f:
    f.write(index_astro)
print("Created Astro Homepage: src/pages/index.astro")

# Special 2: Searchable PDF Blueprint Library Page (src/pages/paper-models/blueprints.astro)
pdfs = [os.path.basename(p).replace(' ', '_') for p in glob.glob(os.path.join(PUBLIC_DIR, 'pdfs', '*.pdf'))]

blueprints_astro = f"""---
import MainLayout from '../../layouts/MainLayout.astro';

const pdfs = {json.dumps(pdfs)};
---

<MainLayout title="PDF Blueprint & Document Library">
  <div style="max-width: 1000px; margin: 0 auto;">
    <span class="badge">Download Center</span>
    <h1 style="font-size: 2.5rem; margin-bottom: 1rem;">Spacecraft PDF Blueprint Library</h1>
    <p style="color: var(--text-muted); margin-bottom: 2rem;">Searchable collection of all {len(pdfs)} recovered PDF schematics, paper model templates, and assembly instructions.</p>

    <input type="text" id="pdfSearch" placeholder="🔍 Search blueprints (e.g. periscope, panel, mercury, cnc, instruction)..." 
           style="width: 100%; padding: 0.8rem 1.25rem; font-size: 1rem; border-radius: 8px; border: 1px solid var(--border-color); background: var(--bg-card); color: #fff; margin-bottom: 2rem;" />

    <div class="grid-cards" id="pdfContainer">
      {"".join([f'<div class="card pdf-card" data-name="{pdf.lower()}"><div style="font-size:2rem; margin-bottom:0.5rem;">📄</div><h3>{pdf}</h3><p style="color:var(--text-muted); font-size:0.85rem; margin:0.5rem 0 1rem 0;">PDF Blueprint File</p><a href="/pdfs/{pdf}" target="_blank" class="btn">Download PDF</a></div>' for pdf in sorted(pdfs)])}
    </div>
  </div>

  <script>
    document.getElementById('pdfSearch')?.addEventListener('input', (e) => {{
      const query = e.target.value.toLowerCase();
      document.querySelectorAll('.pdf-card').forEach(card => {{
        const name = card.getAttribute('data-name');
        card.style.display = name.includes(query) ? 'block' : 'none';
      }});
    }});
  </script>
</MainLayout>
"""

with open(os.path.join(PAGES_DIR, 'paper-models', 'blueprints.astro'), 'w', encoding='utf-8') as f:
    f.write(blueprints_astro)
print("Created Searchable PDF Blueprint Library Page: src/pages/paper-models/blueprints.astro")
