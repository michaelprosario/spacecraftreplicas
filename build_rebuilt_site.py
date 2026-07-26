import os
import glob
import json
import urllib.parse
from bs4 import BeautifulSoup

BASE_DIR = '/workspaces/spacecraftreplicas/recovered_site'

def list_harvested_assets():
    images = glob.glob(os.path.join(BASE_DIR, 'assets', 'images', '*'))
    pdfs = glob.glob(os.path.join(BASE_DIR, 'assets', 'pdfs', '*'))
    pages = glob.glob(os.path.join(BASE_DIR, 'pages', '*'))
    
    images_rel = [os.path.relpath(p, BASE_DIR) for p in images]
    pdfs_rel = [os.path.relpath(p, BASE_DIR) for p in pdfs]
    pages_rel = [os.path.relpath(p, BASE_DIR) for p in pages]
    
    return images_rel, pdfs_rel, pages_rel

def build_modern_index():
    images_rel, pdfs_rel, pages_rel = list_harvested_assets()
    
    pdf_cards_html = ""
    for pdf_path in sorted(pdfs_rel):
        fname = os.path.basename(pdf_path)
        title = fname.replace('.pdf', '').replace('_', ' ').replace('-', ' ').title()
        size_kb = round(os.path.getsize(os.path.join(BASE_DIR, pdf_path)) / 1024, 1) if os.path.exists(os.path.join(BASE_DIR, pdf_path)) else 0
        pdf_cards_html += f"""
        <div class="card pdf-card">
            <div class="card-icon">📄</div>
            <div class="card-body">
                <h3>{title}</h3>
                <p class="file-info">{fname} ({size_kb} KB)</p>
                <div class="card-actions">
                    <a href="{pdf_path}" target="_blank" class="btn btn-primary">Download PDF</a>
                </div>
            </div>
        </div>
        """
        
    img_cards_html = ""
    for img_path in sorted(images_rel)[:36]: # display top 36 images
        fname = os.path.basename(img_path)
        title = fname.replace('_', ' ').replace('-', ' ').title()
        img_cards_html += f"""
        <div class="gallery-item">
            <img src="{img_path}" alt="{title}" loading="lazy" onclick="openLightbox('{img_path}', '{title}')" />
            <div class="gallery-caption">{fname}</div>
        </div>
        """

    index_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SpacecraftReplicas.com | Rebuilt Historical Archive</title>
    <meta name="description" content="Recovered and rebuilt historical archive of SpacecraftReplicas.com featuring space scale model blueprints, instructions, paper craft, and photos.">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&family=Outfit:wght@400;600;800&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg-dark: #0a0c10;
            --bg-card: rgba(22, 27, 34, 0.75);
            --border-color: rgba(255, 255, 255, 0.1);
            --primary: #38bdf8;
            --primary-hover: #0284c7;
            --accent: #f59e0b;
            --text-main: #f3f4f6;
            --text-muted: #9ca3af;
        }}

        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }}

        body {{
            font-family: 'Inter', sans-serif;
            background-color: var(--bg-dark);
            color: var(--text-main);
            line-height: 1.6;
            background-image: 
                radial-gradient(circle at 15% 20%, rgba(56, 189, 248, 0.08) 0%, transparent 40%),
                radial-gradient(circle at 85% 80%, rgba(245, 158, 11, 0.05) 0%, transparent 40%);
            min-height: 100vh;
        }}

        header {{
            background: rgba(10, 12, 16, 0.85);
            backdrop-filter: blur(12px);
            position: sticky;
            top: 0;
            z-index: 100;
            border-bottom: 1px solid var(--border-color);
        }}

        .nav-container {{
            max-width: 1200px;
            margin: 0 auto;
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 1rem 2rem;
        }}

        .logo {{
            font-family: 'Outfit', sans-serif;
            font-size: 1.5rem;
            font-weight: 800;
            color: #fff;
            text-decoration: none;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }}

        .logo span {{
            color: var(--primary);
        }}

        .nav-links {{
            display: flex;
            gap: 1.5rem;
            list-style: none;
        }}

        .nav-links a {{
            color: var(--text-muted);
            text-decoration: none;
            font-weight: 500;
            transition: color 0.2s;
        }}

        .nav-links a:hover {{
            color: var(--primary);
        }}

        .hero {{
            max-width: 1200px;
            margin: 4rem auto 2rem auto;
            padding: 0 2rem;
            text-align: center;
        }}

        .hero h1 {{
            font-family: 'Outfit', sans-serif;
            font-size: 3rem;
            font-weight: 800;
            margin-bottom: 1rem;
            background: linear-gradient(135deg, #fff 0%, var(--primary) 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}

        .hero p {{
            font-size: 1.2rem;
            color: var(--text-muted);
            max-width: 800px;
            margin: 0 auto 2rem auto;
        }}

        .stats-banner {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1.5rem;
            max-width: 1000px;
            margin: 2rem auto;
        }}

        .stat-card {{
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            padding: 1.5rem;
            border-radius: 12px;
            text-align: center;
        }}

        .stat-number {{
            font-family: 'Outfit', sans-serif;
            font-size: 2.5rem;
            font-weight: 800;
            color: var(--primary);
        }}

        .stat-label {{
            color: var(--text-muted);
            font-size: 0.9rem;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}

        .section {{
            max-width: 1200px;
            margin: 4rem auto;
            padding: 0 2rem;
        }}

        .section-title {{
            font-family: 'Outfit', sans-serif;
            font-size: 2rem;
            font-weight: 700;
            margin-bottom: 1.5rem;
            display: flex;
            align-items: center;
            gap: 0.75rem;
        }}

        .pdf-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 1.5rem;
        }}

        .pdf-card {{
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 1.5rem;
            display: flex;
            gap: 1rem;
            transition: transform 0.2s, border-color 0.2s;
        }}

        .pdf-card:hover {{
            transform: translateY(-4px);
            border-color: var(--primary);
        }}

        .card-icon {{
            font-size: 2rem;
        }}

        .card-body h3 {{
            font-size: 1.1rem;
            margin-bottom: 0.5rem;
            color: #fff;
        }}

        .file-info {{
            font-size: 0.85rem;
            color: var(--text-muted);
            margin-bottom: 1rem;
        }}

        .btn {{
            display: inline-block;
            padding: 0.5rem 1rem;
            border-radius: 6px;
            text-decoration: none;
            font-weight: 600;
            font-size: 0.9rem;
            transition: background 0.2s;
        }}

        .btn-primary {{
            background: var(--primary);
            color: #000;
        }}

        .btn-primary:hover {{
            background: var(--primary-hover);
            color: #fff;
        }}

        .gallery-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
            gap: 1rem;
        }}

        .gallery-item {{
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            overflow: hidden;
            cursor: pointer;
            transition: transform 0.2s;
        }}

        .gallery-item:hover {{
            transform: scale(1.03);
        }}

        .gallery-item img {{
            width: 100%;
            height: 140px;
            object-fit: cover;
        }}

        .gallery-caption {{
            padding: 0.5rem;
            font-size: 0.75rem;
            color: var(--text-muted);
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
            text-align: center;
        }}

        footer {{
            border-top: 1px solid var(--border-color);
            padding: 2rem;
            text-align: center;
            color: var(--text-muted);
            margin-top: 4rem;
        }}

        /* Lightbox modal */
        .modal {{
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.9);
            z-index: 1000;
            justify-content: center;
            align-items: center;
        }}

        .modal img {{
            max-width: 90%;
            max-height: 80%;
            border-radius: 8px;
        }}
    </style>
</head>
<body>
    <header>
        <div class="nav-container">
            <a href="#" class="logo">🚀 Spacecraft<span>Replicas</span></a>
            <ul class="nav-links">
                <li><a href="#overview">Overview</a></li>
                <li><a href="#blueprints">Blueprints & PDFs</a></li>
                <li><a href="#gallery">Photo Gallery</a></li>
                <li><a href="#pages">Archived Pages</a></li>
            </ul>
        </div>
    </header>

    <div class="hero" id="overview">
        <h1>Spacecraft Replicas Historical Archive</h1>
        <p>Recovered and rebuilt from the Internet Archive Wayback Machine. Dedicated to scale spacecraft modeling, paper craft templates, blueprints, and historical spaceflight replicas.</p>

        <div class="stats-banner">
            <div class="stat-card">
                <div class="stat-number">{len(pdfs_rel)}</div>
                <div class="stat-label">PDF Blueprints & Docs</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{len(images_rel)}</div>
                <div class="stat-label">Restored Photos</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{len(pages_rel)}</div>
                <div class="stat-label">Recovered Pages</div>
            </div>
        </div>
    </div>

    <section class="section" id="blueprints">
        <div class="section-title">📄 Downloadable Spacecraft Blueprints & Instructions</div>
        <div class="pdf-grid">
            {pdf_cards_html if pdf_cards_html else '<p style="color: var(--text-muted);">PDF downloads are currently downloading from the archive...</p>'}
        </div>
    </section>

    <section class="section" id="gallery">
        <div class="section-title">🖼️ Spacecraft Model Photo Gallery</div>
        <div class="gallery-grid">
            {img_cards_html if img_cards_html else '<p style="color: var(--text-muted);">Image gallery photos downloading from the archive...</p>'}
        </div>
    </section>

    <section class="section" id="pages">
        <div class="section-title">🌐 Recovered Historical Pages</div>
        <div class="pdf-grid">
            {"".join([f'<div class="card pdf-card"><div class="card-icon">🌐</div><div class="card-body"><h3>{os.path.basename(p)}</h3><div class="card-actions"><a href="{p}" class="btn btn-primary">View Page</a></div></div></div>' for p in sorted(pages_rel)[:12]])}
        </div>
    </section>

    <footer>
        <p>SpacecraftReplicas.com Historical Restoration Project | Archived via Wayback Machine</p>
    </footer>

    <div class="modal" id="lightbox" onclick="this.style.display='none'">
        <img id="modal-img" src="" alt="" />
    </div>

    <script>
        function openLightbox(src, title) {{
            document.getElementById('modal-img').src = src;
            document.getElementById('lightbox').style.display = 'flex';
        }}
    </script>
</body>
</html>
"""
    with open(os.path.join(BASE_DIR, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(index_html)
        
    print("Built modernized index.html successfully!")

if __name__ == '__main__':
    build_modern_index()
