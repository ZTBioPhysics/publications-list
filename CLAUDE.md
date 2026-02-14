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
- Smart caching: only fetches full details for new publications
- Citation counts refreshed on every run from basic Scholar data (no extra API calls)
- Proxy rotation via ScraperAPI (preferred) or free proxies (fallback)

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
- `SCRAPER_API_KEY` env var (recommended): Set as GitHub Actions repository secret for reliable ScraperAPI proxy access
- Without it, falls back to free proxies (unreliable)

## Running Locally
```bash
pip install -r requirements.txt
python fetch_pubs.py
```

## Current Status
**Project is stable and fully operational.** GitHub Actions workflow runs daily at 2 AM UTC using ScraperAPI for reliable Google Scholar access. Citation counts are refreshed on every run.

Last updated: 2026-02-14

## Known Issues
- `scholarly` library is unmaintained; httpx must stay pinned to <0.28.0
- ScraperAPI free tier has 5,000 requests/month limit (more than sufficient for daily runs)

## Conda Environment
- Name: `berndsen-lab-website`
- Python: 3.11

## Future Ideas
- Team/People page (photo grid with Scholar/ORCID links)
- Research Projects page (visual cards per research area)
- Software & Tools page (lab computational tools/pipelines)
- Photo gallery (lab photos, cryo-EM micrographs, conference presentations)
- Lab News/Blog (papers, grants, student achievements)
