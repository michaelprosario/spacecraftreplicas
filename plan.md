# Website Recovery & Rebuild Plan: SpacecraftReplicas.com

## Executive Summary
This plan outlines the systematic strategy to recover, harvest, clean, and rebuild **SpacecraftReplicas.com** using snapshots archived on the Internet Archive Wayback Machine (`https://web.archive.org/web/*/www.spacecraftreplicas.com*`).

The archival inventory scan has successfully retrieved **360 KB of CDX metadata** indexing over **1,000 archived URLs** with `200 OK` status codes, including spacecraft build instructions, schematics, model templates, high-resolution PDFs, image galleries, and HTML pages.

---

## 📊 Discovered Asset Inventory Overview

| Asset Category | File Extensions / Types | Discovered Quantity | Description & Notes |
| :--- | :--- | :---: | :--- |
| **PDF Documents** | `.pdf` | **~80+ Files** | Instructions (`x40-instructions.pdf`, `instruction.pdf`), schematics (`mercury61.pdf`, `boeing1.pdf`), panel templates (`panel13e.pdf`, `panel16.pdf`), CNC files (`cnc2.pdf`), periscope blueprints. |
| **Image Media** | `.jpg`, `.jpeg`, `.png`, `.gif` | **~350+ Files** | Spacecraft model photo galleries, build diagrams, logos, thumbnail maps, paper craft templates. |
| **Web Pages** | `.html`, `.htm`, WordPress routes | **~150+ Pages** | Main home page, blog entries, FAQ, contact page, model galleries (`/paper`, `/gallery`, `/hallmark`). |
| **Stylesheets & Scripts** | `.css`, `.js` | **~25+ Files** | Original CSS layout files, theme assets, navigation scripts. |

---

## 1. Archival Exploration & Asset Inventorying

### 1.1 Querying the Wayback CDX Server API
We retrieved the complete index of captured URLs:
```bash
curl -sL "https://web.archive.org/cdx/search/cdx?url=spacecraftreplicas.com/*&output=json&fl=original,timestamp,mimetype,statuscode,digest,length" -o cdx_raw.json
```

### 1.2 Identified Key Resources
- **Model Blueprints & Templates**:
  - `wp-content/uploads/2010/12/instruction.pdf`
  - `wp-content/uploads/2010/12/mercury61.pdf`
  - `wp-content/uploads/2011/11/x40-instructions.pdf`
  - `wp-content/uploads/2011/11/boeing1.pdf`
  - `wp-content/uploads/2010/12/persicope-assembly.pdf`
  - `wp-content/uploads/2011/03/cnc2.pdf`, `cnc3.pdf`, `cnc5.pdf`
- **Galleries & Photo Assets**:
  - `/gallery/img_1159_small.jpg`, `/gallery/img_2177_sm.jpg`, `/gallery/mac-12_small.jpg`
  - `/paper/cardxx_small.jpg`, `/paper/kitfox-biplane_small.jpg`

---

## 2. Automated Harvesting Strategy

### 2.1 Raw Content Extraction (`id_` Endpoint)
All requests target the raw (`id_`) Wayback URL endpoint to retrieve pure original files without Wayback Machine toolbar wrappers:
```
https://web.archive.org/web/{timestamp}id_/{original_url}
```

### 2.2 Local Directory Structure
Harvested assets are stored in the following directory layout:
```
/workspaces/spacecraftreplicas/
├── recovered_site/
│   ├── index.html
│   ├── pages/
│   ├── assets/
│   │   ├── images/
│   │   ├── pdfs/
│   │   ├── css/
│   │   └── js/
├── cdx_raw.json
├── plan.md
└── README.md
```

### 2.3 Download Script Specs (`download_assets.py`)
- **Deduplication**: Deduplicate by URL digest and clean path.
- **Resilience**: Rate-limiting (0.2s delay per request), User-Agent header, auto-retry on 503.

---

## 3. Data Cleaning & Link Normalization

### 3.1 Scraping Wayback Artifacts
Strip any residual `__wm` JavaScript objects or Archive toolbar elements.

### 3.2 Href & Image Path Fixing
- Convert legacy absolute domain links (e.g. `http://www.spacecraftreplicas.com/...`) to relative paths.
- Re-link all PDF downloads to local `/assets/pdfs/` paths.
- Re-link all image sources to local `/assets/images/` paths.

---

## 4. Website Modernization & Rebuilding

### 4.1 Modern Frontend Architecture
- Clean HTML5 semantic layout (`<header>`, `<nav>`, `<main>`, `<article>`, `<footer>`).
- Responsive CSS Grid/Flexbox with modern typography (Inter/Outfit).
- PDF viewer integration and downloadable paper model section.

### 4.2 Local Development Server
- Dev server via `python3 -m http.server 8000` or `npm run dev`.

---

## 5. Verification & Quality Assurance Checklist

- [x] **CDX Metadata Query**: Successfully indexed 360 KB JSON of archived assets.
- [ ] **Asset Harvesting**: Download 100% of discovered HTML, JPG, and PDF files.
- [ ] **Link Integrity**: Verify zero broken links across all subpages.
- [ ] **PDF & Image Validation**: Confirm all schematic PDFs open correctly.
- [ ] **Responsive Design Check**: Test layout on desktop and mobile viewports.
