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
    """Set up proxy rotation to avoid Google Scholar blocking.

    Returns True if proxy was set up successfully, False otherwise.
    Failures are non-fatal - the script will continue without proxy.
    """
    print("Setting up proxy rotation...")

    try:
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
        print("Proxy setup successful")
        return True

    except Exception as e:
        print(f"Warning: Proxy setup failed ({type(e).__name__}: {e})")
        print("Proceeding without proxy - may be rate limited by Google Scholar")
        return False

def fetch_with_retry(func, *args, max_retries=3, base_delay=5, **kwargs):
    """Execute a function with exponential backoff retry logic.

    Args:
        func: Function to call
        *args: Positional arguments for func
        max_retries: Maximum number of retry attempts
        base_delay: Base delay in seconds (doubles each retry)
        **kwargs: Keyword arguments for func

    Returns:
        Result of func(*args, **kwargs)

    Raises:
        Last exception if all retries fail
    """
    last_exception = None
    for attempt in range(max_retries):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            last_exception = e
            if attempt < max_retries - 1:
                delay = base_delay * (2 ** attempt)
                print(f"  Attempt {attempt + 1} failed: {e}")
                print(f"  Retrying in {delay} seconds...")
                time.sleep(delay)
            else:
                print(f"  All {max_retries} attempts failed")
    raise last_exception


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

    # Get author by ID with retry logic
    print("Fetching author profile...")
    author = fetch_with_retry(scholarly.search_author_id, SCHOLAR_ID)

    # Fill in publication list (basic info only) with retry logic
    print("Fetching publication list...")
    author = fetch_with_retry(scholarly.fill, author, sections=['publications'])

    publications = []
    new_count = 0

    for pub in author.get('publications', []):
        bib = pub.get('bib', {})
        title = bib.get('title', 'Untitled')

        # Check if we already have full details for this publication
        if title in existing_pubs and existing_pubs[title].get('authors'):
            # Use cached data but update citation count from fresh Scholar data
            cached = existing_pubs[title].copy()
            fresh_citations = pub.get('num_citations', 0)
            if fresh_citations != cached.get('citations', 0):
                print(f"  [cached, citations {cached.get('citations', 0)} → {fresh_citations}] {title[:60]}...")
            else:
                print(f"  [cached] {title[:60]}...")
            cached['citations'] = fresh_citations
            publications.append(cached)
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
    """Main entry point. Returns 0 on success, 1 on failure."""
    # Set up proxy to avoid Google Scholar blocking (non-fatal if it fails)
    proxy_ok = setup_proxy()
    if not proxy_ok:
        print("Continuing without proxy...\n")

    try:
        publications = fetch_publications()
    except Exception as e:
        print(f"\nError fetching publications: {type(e).__name__}: {e}")

        # If we have cached data, exit gracefully
        if os.path.exists(OUTPUT_FILE):
            print(f"Keeping existing {OUTPUT_FILE} (fetch failed but cached data exists)")
            return 0
        else:
            print("No cached data available - cannot recover")
            return 1

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
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main())
