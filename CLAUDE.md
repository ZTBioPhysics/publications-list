# Berndsen Lab Website - Project Context

## Overview
This is the **Berndsen Lab publication and media management system** for the University of Missouri. It provides dynamically updated web pages embedded into the lab's Google Sites website via iframes, maintaining a professional online presence for research publications, press coverage, and interactive 3D protein structure visualization.

**Repository:** `ZTBioPhysics/Berndsen-Lab-Website`
**GitHub Pages:** `https://ztbiophysics.github.io/Berndsen-Lab-Website/`

## Components

### 1. Publications Page (`index.html`)
- Displays Dr. Zachary T. Berndsen's Google Scholar publications
- Sortable by date or citation count
- Shows stats: total publications and citations
- Data source: `publications.json` (auto-generated daily)

### 2. Press & Media Page (`press.html`)
- News coverage and articles about lab research
- Supports embedded videos (YouTube, Facebook)
- Data source: `press.json` (manually edited)

### 3. 3D Structure Viewer (`structures.html`)
- Interactive Mol* viewer for PDB protein structures
- Auto-fetches from RCSB PDB using author search
- Collapsible sidebar, categorized by research focus

### 4. Publication Fetcher (`fetch_pubs.py`)
- Python script scraping Google Scholar via `scholarly` library
- Smart caching: only fetches new publications
- Proxy rotation via ScraperAPI or free proxies

## Technology Stack
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Backend**: Python 3.11 (`scholarly` library)
- **Hosting**: GitHub Pages (static)
- **APIs**: RCSB Search/Data API, Google Scholar
- **3D Viewer**: Mol* (molstar.org)
- **CI/CD**: GitHub Actions (daily updates at 2 AM UTC)

## Key Files
| File | Purpose |
|------|---------|
| `fetch_pubs.py` | Google Scholar scraper |
| `index.html` | Publications page |
| `press.html` | Press coverage page |
| `structures.html` | 3D protein viewer |
| `style.css` | Shared styles |
| `publications.json` | Auto-generated publication data |
| `press.json` | Manual press article data |
| `.github/workflows/update-publications.yml` | CI/CD automation |

## Design Decisions
- **Mizzou Gold (#F1B82D)** as primary accent color
- Static hosting with client-side JSON fetching
- Smart caching to minimize API calls and respect rate limits
- Responsive design optimized for iframe embedding

## Configuration
- `SCRAPER_API_KEY` env var (optional): For proxy rotation
- Without it, falls back to free proxies

## Running Locally
```bash
pip install -r requirements.txt
python fetch_pubs.py
```

## Current Status
Project is stable. Pending commit with httpx fix for GitHub Actions.

**Uncommitted changes:**
- `requirements.txt` - Added `httpx<0.28.0` pin (fixes scholarly compatibility)
- `fetch_pubs.py` - Improved error handling, retry logic, graceful degradation

## Known Issues
- `scholarly` library is unmaintained; httpx must stay pinned to <0.28.0
- Free proxies are unreliable; consider ScraperAPI if blocking becomes frequent

## Pending/Future Work
- Commit and push the httpx fix
- Trigger GitHub Action manually to verify
- Update Google Sites iframe embed codes to new URL:
  - `https://ztbiophysics.github.io/Berndsen-Lab-Website/index.html`
  - `https://ztbiophysics.github.io/Berndsen-Lab-Website/press.html`
  - `https://ztbiophysics.github.io/Berndsen-Lab-Website/structures.html`
