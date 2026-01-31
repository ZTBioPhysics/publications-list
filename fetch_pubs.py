#!/usr/bin/env python3
"""
Fetch publications from Google Scholar and save to JSON.
Only fetches full details for new publications to avoid rate limiting.
"""

from scholarly import scholarly, ProxyGenerator
import json
import os
import time
from datetime import datetime, timezone

SCHOLAR_ID = "u9i3_ywAAAAJ"
OUTPUT_FILE = "publications.json"

def setup_proxy():
    """Set up proxy rotation to avoid Google Scholar blocking."""
    print("Setting up proxy rotation...")
    pg = ProxyGenerator()

    # Try ScraperAPI first if available (more reliable)
    scraper_api_key = os.environ.get('SCRAPER_API_KEY')
    if scraper_api_key:
        print("Using ScraperAPI proxy")
        pg.ScraperAPI(scraper_api_key)
    else:
        # Fall back to free proxies
        print("Using free proxy rotation")
        success = pg.FreeProxies()
        if not success:
            print("Warning: Could not set up free proxies, proceeding without")
            return False

    scholarly.use_proxy(pg)
    return True

def load_existing_publications():
    """Load existing publications from JSON file if it exists."""
    if not os.path.exists(OUTPUT_FILE):
        return {}

    try:
        with open(OUTPUT_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            # Create a lookup by title for quick matching
            return {pub['title']: pub for pub in data.get('publications', [])}
    except (json.JSONDecodeError, KeyError):
        return {}

def fetch_publications():
    """Fetch all publications, only getting full details for new ones."""
    print(f"Fetching publications for Scholar ID: {SCHOLAR_ID}")

    # Load existing data to avoid re-fetching
    existing_pubs = load_existing_publications()
    print(f"Found {len(existing_pubs)} existing publications in cache")

    # Get author by ID
    author = scholarly.search_author_id(SCHOLAR_ID)

    # Fill in publication list (basic info only)
    author = scholarly.fill(author, sections=['publications'])

    publications = []
    new_count = 0

    for pub in author.get('publications', []):
        bib = pub.get('bib', {})
        title = bib.get('title', 'Untitled')

        # Check if we already have full details for this publication
        if title in existing_pubs and existing_pubs[title].get('authors'):
            # Use cached data
            print(f"  [cached] {title[:60]}...")
            publications.append(existing_pubs[title])
        else:
            # New publication - fetch full details
            print(f"  [fetching] {title[:60]}...")
            new_count += 1

            # Add delay between requests to avoid rate limiting
            if new_count > 1:
                time.sleep(2)

            try:
                # Fill in full publication details (includes authors)
                full_pub = scholarly.fill(pub)
                full_bib = full_pub.get('bib', {})

                # Format authors
                authors = full_bib.get('author', '')
                if isinstance(authors, list):
                    authors = ', '.join(authors)

                pub_data = {
                    'title': title,
                    'authors': authors,
                    'year': full_bib.get('pub_year', bib.get('pub_year', '')),
                    'venue': full_bib.get('citation', bib.get('citation', '')),
                    'citations': full_pub.get('num_citations', pub.get('num_citations', 0)),
                    'url': full_pub.get('pub_url', pub.get('pub_url', '')),
                    'scholar_url': f"https://scholar.google.com/citations?view_op=view_citation&hl=en&user={SCHOLAR_ID}&citation_for_view={pub.get('author_pub_id', '')}"
                }
                publications.append(pub_data)

            except Exception as e:
                print(f"    Warning: Could not fetch details for '{title}': {e}")
                # Fall back to basic info
                pub_data = {
                    'title': title,
                    'authors': '',
                    'year': bib.get('pub_year', ''),
                    'venue': bib.get('citation', ''),
                    'citations': pub.get('num_citations', 0),
                    'url': pub.get('pub_url', ''),
                    'scholar_url': f"https://scholar.google.com/citations?view_op=view_citation&hl=en&user={SCHOLAR_ID}&citation_for_view={pub.get('author_pub_id', '')}"
                }
                publications.append(pub_data)

    print(f"\nFetched details for {new_count} new publication(s)")

    # Sort by year (newest first), then by citations
    publications.sort(key=lambda x: (-(int(x['year']) if str(x['year']).isdigit() else 0), -x['citations']))

    return publications

def main():
    # Set up proxy to avoid Google Scholar blocking
    setup_proxy()

    publications = fetch_publications()

    # Create output data with metadata
    output = {
        'last_updated': datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'),
        'scholar_id': SCHOLAR_ID,
        'total_publications': len(publications),
        'publications': publications
    }

    # Write to JSON file
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"\nSuccessfully saved {len(publications)} publications to {OUTPUT_FILE}")
    print(f"Last updated: {output['last_updated']}")

if __name__ == '__main__':
    main()
