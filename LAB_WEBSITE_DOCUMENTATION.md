# Berndsen Lab Website Documentation

## Overview

This document describes the custom embedded pages created for the Berndsen Lab Google Sites website. These pages are hosted on GitHub Pages and embedded into Google Sites via iframes, allowing for dynamic content and custom styling that Google Sites doesn't natively support.

---

## Architecture

```
GitHub Repository (publications-list)
    │
    ├── GitHub Actions (runs daily)
    │   └── Fetches Google Scholar → updates publications.json
    │
    ├── GitHub Pages (hosts static files)
    │   ├── index.html (Publications page)
    │   ├── press.html (Press & Media page)
    │   ├── publications.json (auto-updated)
    │   └── press.json (manually updated)
    │
    └── Embedded in Google Sites via <iframe>
```

---

## Publications Page

### How It Works
1. **Python script** (`fetch_pubs.py`) scrapes Google Scholar using your Scholar ID
2. **GitHub Actions** runs this script daily at 2:00 AM UTC
3. Script saves publication data to `publications.json`
4. **HTML page** (`index.html`) loads the JSON and renders a styled list
5. **Caching**: Author details are cached - only new publications trigger full fetches

### Files
- `fetch_pubs.py` - Python script that fetches from Google Scholar
- `publications.json` - Generated data file (auto-updated)
- `index.html` - The styled publications page
- `style.css` - Shared styles
- `requirements.txt` - Python dependencies (scholarly)
- `.github/workflows/update-publications.yml` - Automation workflow

### Google Scholar ID
Your Scholar ID: `u9i3_ywAAAAJ`
(Found in your Scholar URL: `https://scholar.google.com/citations?user=u9i3_ywAAAAJ`)

### Manual Update
To force an update:
1. Go to: https://github.com/ZTBioPhysics/publications-list/actions
2. Click "Update Publications List"
3. Click "Run workflow"

### Embed Code
```html
<iframe src="https://ztbiophysics.github.io/publications-list/" width="100%" height="2500" style="border:none;"></iframe>
```

---

## Press & Media Page

### How It Works
1. You manually edit `press.json` to add/remove articles
2. **HTML page** (`press.html`) loads the JSON and renders:
   - Article cards in a responsive grid
   - Embedded videos (YouTube and Facebook supported)
3. Push changes to GitHub → automatically deployed to GitHub Pages

### Files
- `press.json` - Article and video data (manually edited)
- `press.html` - The styled press page

### Adding a New Press Article
Edit `press.json` and add a new entry in the `"articles"` array:

```json
{
  "title": "Article Title Here",
  "source": "Publication Name",
  "date": "2025-01-20",
  "url": "https://example.com/article-link",
  "image": "https://example.com/image.jpg",
  "description": "Brief description (optional)"
}
```

**Finding image URLs:** Right-click the main image on an article → "Copy Image Address"

### Adding a New Video

**YouTube:**
```json
{
  "title": "Video Title",
  "source": "YouTube",
  "youtube_id": "VIDEO_ID_HERE",
  "description": "Description"
}
```
(The video ID is the part after `v=` in YouTube URLs)

**Facebook:**
```json
{
  "title": "Video Title",
  "source": "Facebook",
  "facebook_url": "https://www.facebook.com/watch/?v=VIDEO_ID",
  "description": "Description"
}
```

### Embed Code
```html
<iframe src="https://ztbiophysics.github.io/publications-list/press.html" width="100%" height="1800" style="border:none;"></iframe>
```

---

## Updating & Pushing Changes

### Local Editing Workflow
```bash
# Navigate to the repo
cd /path/to/publications-list

# Edit files (e.g., press.json)

# Stage, commit, and push
git add .
git commit -m "Add new press article"
git push
```

### After Pushing
- Changes go live on GitHub Pages within 1-2 minutes
- Refresh your Google Sites page to see updates

---

## Repository Information

- **GitHub Repo:** https://github.com/ZTBioPhysics/publications-list
- **Publications URL:** https://ztbiophysics.github.io/publications-list/
- **Press Page URL:** https://ztbiophysics.github.io/publications-list/press.html
- **Local Path:** `/Users/ztbm97/Library/CloudStorage/OneDrive-UniversityofMissouri/Berndsen_Lab/Code/GitHub/publications-list/`

---

## Styling Notes

- **Mizzou Gold** (`#F1B82D`) is used for accent colors (underlines, source labels)
- Responsive design adapts to mobile screens
- Cards have hover effects (subtle lift and shadow)
- Images are cropped to consistent heights (180px for articles)

---

## Future Ideas for Lab Website

### 1. Interactive 3D Structure Viewer
Embed Mol* or 3Dmol.js to display your lab's PDB structures interactively. Visitors could rotate, zoom, and explore molecules like the apoB100/LDL structure.

**Could include:**
- Multiple structures in a gallery
- Preset views highlighting key features
- Links to PDB entries

### 2. Team/People Page
A styled grid of lab members with:
- Photos (consistent sizing)
- Name, title, research focus
- Links to Google Scholar, ORCID, email
- Could auto-fetch their publication counts

### 3. Research Projects Page
Visual cards for each research area:
- HIV envelope/glycan shields
- LDL/apolipoprotein structures
- Bacteriophage DNA packaging
- Influenza hemagglutinin

Each with representative images, descriptions, and key publications.

### 4. Software & Tools
If your lab has computational tools, scripts, or analysis pipelines:
- Download links or GitHub repos
- Documentation
- Example outputs

### 5. Photo Gallery
- Lab photos
- Conference presentations
- Cryo-EM micrographs
- Molecular visualizations
Displayed in a lightbox-style grid.

### 6. Teaching & Resources
- Course materials
- Protocols
- Tutorials for students
- Useful links

### 7. Social Media Feed
Embed Twitter/X or Bluesky feed to show real-time lab updates.

### 8. Lab News/Blog
Simple chronological updates about:
- New papers
- Grants awarded
- Student achievements
- Conference presentations

---

## Troubleshooting

### Images not loading
- Check that the image URL is publicly accessible
- Some sites block hotlinking - try finding a different image URL
- The page shows a gold placeholder if an image fails to load

### Publications not updating
- Check GitHub Actions: https://github.com/ZTBioPhysics/publications-list/actions
- Google Scholar may rate-limit requests; the script handles this gracefully

### Embed not showing in Google Sites
- Make sure the iframe height is sufficient
- Google Sites may cache; try refreshing with Ctrl+Shift+R

---

## Contact

For questions or updates, this system was set up with assistance from Claude (Anthropic).

Repository created: January 2026
