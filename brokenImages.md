# Broken Images Report: SpacecraftReplicas.com

This document contains the complete audit of broken image references across all subpages of **SpacecraftReplicas.com** (`https://opulent-spoon-r4xj95r6w5f5pw4-4321.app.github.dev/`).

---

## 📊 Summary Statistics
- **Total Pages Audited**: 21
- **Total `<img>` Tags Inspected**: 70
- **Total Valid Images Loaded**: 44
- **Total Broken Image References**: 26

---

## ❌ Broken Images by Page Route

### Page: `/about`
**URL**: `https://opulent-spoon-r4xj95r6w5f5pw4-4321.app.github.dev/about`

| Image Reference | Missing Filename | Reason / Status |
| :--- | :--- | :--- |
| `/images/IMG_0203-150x112.jpg` | `IMG_0203-150x112.jpg` | Missing from archive (`public/images/`) |
| `/images/IMG_0204-150x112.jpg` | `IMG_0204-150x112.jpg` | Missing from archive (`public/images/`) |
| `/images/IMG_0205-150x112.jpg` | `IMG_0205-150x112.jpg` | Missing from archive (`public/images/`) |
| `/images/IMG_0206-150x112.jpg` | `IMG_0206-150x112.jpg` | Missing from archive (`public/images/`) |
| `/images/IMG_0207-150x112.jpg` | `IMG_0207-150x112.jpg` | Missing from archive (`public/images/`) |
| `/images/IMG_0208-150x112.jpg` | `IMG_0208-150x112.jpg` | Missing from archive (`public/images/`) |
| `/images/IMG_0209-150x112.jpg` | `IMG_0209-150x112.jpg` | Missing from archive (`public/images/`) |
| `/images/IMG_0210-150x112.jpg` | `IMG_0210-150x112.jpg` | Missing from archive (`public/images/`) |

---

### Page: `/community/collectspace`
**URL**: `https://opulent-spoon-r4xj95r6w5f5pw4-4321.app.github.dev/community/collectspace`

| Image Reference | Missing Filename | Reason / Status |
| :--- | :--- | :--- |
| `/images/IMG_5322-113x150.jpg` | `IMG_5322-113x150.jpg` | Missing from archive (`public/images/`) |

---

### Page: `/community/homebuilts`
**URL**: `https://opulent-spoon-r4xj95r6w5f5pw4-4321.app.github.dev/community/homebuilts`

| Image Reference | Missing Filename | Reason / Status |
| :--- | :--- | :--- |
| `/images/N42BP%20in%20LV%20RM_small.jpg` | `N42BP in LV RM_small.jpg` | Missing from archive (`public/images/`) |
| `/images/Cockpit1_small.jpg` | `Cockpit1_small.jpg` | Missing from archive (`public/images/`) |
| `/images/Front2_small.jpg` | `Front2_small.jpg` | Missing from archive (`public/images/`) |
| `/images/560A0061_small.JPG` | `560A0061_small.JPG` | Missing from archive (`public/images/`) |

---

### Page: `/mercury/aft-bulkhead`
**URL**: `https://opulent-spoon-r4xj95r6w5f5pw4-4321.app.github.dev/mercury/aft-bulkhead`

| Image Reference | Missing Filename | Reason / Status |
| :--- | :--- | :--- |
| `/images/IMG_0122-300x225.jpg` | `IMG_0122-300x225.jpg` | Missing from archive (`public/images/`) |

---

### Page: `/mercury/antenna-fairing`
**URL**: `https://opulent-spoon-r4xj95r6w5f5pw4-4321.app.github.dev/mercury/antenna-fairing`

| Image Reference | Missing Filename | Reason / Status |
| :--- | :--- | :--- |
| `/images/IMG_1159-300x225.jpg` | `IMG_1159-300x225.jpg` | Missing from archive (`public/images/`) |

---

### Page: `/mercury/hallmark`
**URL**: `https://opulent-spoon-r4xj95r6w5f5pw4-4321.app.github.dev/mercury/hallmark`

| Image Reference | Missing Filename | Reason / Status |
| :--- | :--- | :--- |
| `/images/image003_small.jpg` | `image003_small.jpg` | Missing from archive (`public/images/`) |
| `/images/image005_small.jpg` | `image005_small.jpg` | Missing from archive (`public/images/`) |
| `/images/image007_small.jpg` | `image007_small.jpg` | Missing from archive (`public/images/`) |
| `/images/image009_small.jpg` | `image009_small.jpg` | Missing from archive (`public/images/`) |
| `/images/image011_small.jpg` | `image011_small.jpg` | Missing from archive (`public/images/`) |
| `/images/image014_small.jpg` | `image014_small.jpg` | Missing from archive (`public/images/`) |
| `/images/image015_small.jpg` | `image015_small.jpg` | Missing from archive (`public/images/`) |

---

### Page: `/mercury/periscope`
**URL**: `https://opulent-spoon-r4xj95r6w5f5pw4-4321.app.github.dev/mercury/periscope`

| Image Reference | Missing Filename | Reason / Status |
| :--- | :--- | :--- |
| `/images/IMG_2188-300x225.jpg` | `IMG_2188-300x225.jpg` | Missing from archive (`public/images/`) |
| `/images/periscope_PDF-300x269.jpg` | `periscope_PDF-300x269.jpg` | Missing from archive (`public/images/`) |

---

### Page: `/shuttle/x-37-x-40`
**URL**: `https://opulent-spoon-r4xj95r6w5f5pw4-4321.app.github.dev/shuttle/x-37-x-40`

| Image Reference | Missing Filename | Reason / Status |
| :--- | :--- | :--- |
| `/images/Z` | `Z` | Missing from archive (`public/images/`) |
| `/images/2Q==` | `2Q==` | Missing from archive (`public/images/`) |

---


## 💡 Recommendations & Next Steps
1. **Fallback Image Placeholder**: Implement a clean CSS/SVG placeholder for missing archive photos (`onerror="this.src='/images/placeholder.svg'"`).
2. **Snapshot Search**: Search secondary Wayback Machine capture dates for missing thumbnail files (`-150x112.jpg`, `_small.jpg`).
