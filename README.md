# Berndsen Lab Website

Dynamic web pages for the [Berndsen Lab](https://sites.google.com/view/berndsenlab) at the University of Missouri, hosted on GitHub Pages and embedded via iframes into Google Sites.

## Pages

- **[Publications](https://ztbiophysics.github.io/Berndsen-Lab-Website/index.html)** — Auto-updated from Google Scholar (daily). Sortable by date or citation count.
- **[Press & Media](https://ztbiophysics.github.io/Berndsen-Lab-Website/press.html)** — News coverage and embedded videos.
- **[3D Structures](https://ztbiophysics.github.io/Berndsen-Lab-Website/structures.html)** — Interactive Mol* viewer for PDB protein structures.

## How It Works

A GitHub Actions workflow runs daily at 2 AM UTC:
1. `fetch_pubs.py` fetches publications from Google Scholar via the `scholarly` library
2. Citation counts are refreshed on every run; full details are only fetched for new publications
3. Uses [ScraperAPI](https://www.scraperapi.com/) for reliable proxy access (falls back to free proxies)
4. Updated `publications.json` is committed and deployed to GitHub Pages

## Setup

```bash
# Create conda environment
conda create -n berndsen-lab-website python=3.11
conda activate berndsen-lab-website

# Install dependencies
pip install -r requirements.txt

# Run locally (optional: set SCRAPER_API_KEY for proxy support)
export SCRAPER_API_KEY=your_key_here
python fetch_pubs.py
```

## GitHub Actions Configuration

Add `SCRAPER_API_KEY` as a repository secret (**Settings > Secrets and variables > Actions**) for reliable daily updates.

## Adding Press Articles & Videos

Edit `press.json` and add entries to the `"articles"` array:

**Article:**
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
To find image URLs: right-click the main image on an article and select "Copy Image Address".

**YouTube video:**
```json
{
  "title": "Video Title",
  "source": "YouTube",
  "youtube_id": "VIDEO_ID_HERE",
  "description": "Description"
}
```

**Facebook video:**
```json
{
  "title": "Video Title",
  "source": "Facebook",
  "facebook_url": "https://www.facebook.com/watch/?v=VIDEO_ID",
  "description": "Description"
}
```

## 3D Structure Viewer

Structures are auto-fetched from RCSB PDB using `audit_author.name = "Berndsen, Z.T."` and categorized by keywords. New PDB deposits appear automatically once released.

To add new categories, edit the `categories` object in `structures.html`:
```javascript
const categories = {
  'HIV/SIV Envelope Glycoproteins': ['HIV', 'SIV', 'Envelope', 'SOSIP', 'ApexGT'],
  'Lipoproteins': ['ApoB', 'LDL', 'Lipoprotein', 'Low-Density'],
  'Bacterial Proteins': ['Escherichia', 'E. coli', 'EtpA', 'adhesin', 'Bacterial']
};
```

## Troubleshooting

- **Publications not updating**: Check the Actions tab on GitHub. Verify `SCRAPER_API_KEY` secret is set. ScraperAPI free tier allows 5,000 requests/month.
- **Images not loading on press page**: Ensure the URL is publicly accessible. Some sites block hotlinking.
- **Embed not showing in Google Sites**: Check iframe height is sufficient. Try Ctrl+Shift+R to clear Google Sites cache.

## Tech Stack

- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Backend**: Python 3.11 (`scholarly`)
- **Hosting**: GitHub Pages
- **APIs**: Google Scholar, RCSB PDB Search/Data API
- **3D Viewer**: Mol* (molstar.org)
- **CI/CD**: GitHub Actions