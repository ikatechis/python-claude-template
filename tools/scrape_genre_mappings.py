#!/usr/bin/env python3
"""Scrape genre/collection mappings from vmrebetiko.gr.

Queries search pages for each genre to build item-to-genre mappings.
"""

import json
import sys
import time
from pathlib import Path

import requests
import urllib3
from bs4 import BeautifulSoup

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Collection IDs found on the musicalgenres page
COLLECTIONS = {
    "rebetiko": "Ρεμπέτικο",
    "astiko_laiko": "Αστικό λαϊκό",
    "amanes": "Αμανές",
    "dimotiko": "Δημοτικό",
    "dimotikofanes": "Δημοτικοφανές",
    "elafro": "Ελαφρό",
    "epitheorisi": "Επιθεώρηση",
    "kinimatografos": "Κινηματογράφος",
    "logia_diaskeui": "Λόγια διασκευή",
    "logio": "Λόγιο",
    "opera": "Όπερα",
    "opereta": "Οπερέτα",
    "theatro_skion": "Θέατρο σκιών",
    "xena": "Ξένα",
    "xena_apo_ellhnes": "Ξένα από Έλληνες",
    "xena_ellhnikoi_stixoi": "Ξένα ελληνικοί στίχοι",
    "athinaiko_tragoudi": "Αθηναϊκό τραγούδι",
}


def get_page(url: str, params: dict | None = None) -> BeautifulSoup | None:
    """Fetch and parse a webpage."""
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "el-GR,el;q=0.9,en;q=0.8",
        }
        response = requests.get(url, params=params, headers=headers, verify=False, timeout=30)
        response.raise_for_status()
        response.encoding = response.apparent_encoding
        return BeautifulSoup(response.text, "lxml")
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}", file=sys.stderr)
        return None


def get_search_page_items(page_num: int, genre: str) -> list[str]:
    """Get all item IDs from a search results page for a specific genre."""
    url = "https://vmrebetiko.gr/search/"
    params = {
        "fmid": "p",
        "pg": str(page_num),
        "g": genre,
    }

    soup = get_page(url, params)
    if not soup:
        return []

    item_ids = []
    gallery_items = soup.find_all("div", class_="eael-filterable-gallery-item-wrap")

    for item in gallery_items:
        link = item.find("a", href=lambda x: x and "/item?id=" in x)
        if link:
            href = link.get("href")
            if "?id=" in href:
                item_id = href.split("?id=")[-1]
                item_ids.append(item_id)

    return item_ids


def scrape_genre(genre_id: str, genre_name: str) -> list[str]:
    """Scrape all item IDs for a given genre.

    Returns:
        List of item IDs belonging to this genre
    """
    print(f"\n{'=' * 60}")
    print(f"Scraping: {genre_name} ({genre_id})")
    print(f"{'=' * 60}")

    all_item_ids = []
    page_num = 0
    max_empty_pages = 3  # Stop after 3 consecutive empty pages

    empty_page_count = 0

    while True:
        print(f"  Page {page_num}...", end=" ", flush=True)
        item_ids = get_search_page_items(page_num, genre_name)

        if not item_ids:
            empty_page_count += 1
            print(f"(empty - {empty_page_count}/{max_empty_pages})")
            if empty_page_count >= max_empty_pages:
                print(f"  Stopping after {max_empty_pages} empty pages")
                break
        else:
            empty_page_count = 0  # Reset counter
            all_item_ids.extend(item_ids)
            print(f"✓ {len(item_ids)} items (total: {len(all_item_ids)})")

        page_num += 1
        time.sleep(0.5)  # Be nice to the server

    # Deduplicate
    unique_ids = list(dict.fromkeys(all_item_ids))
    print(f"\n  Total unique items: {len(unique_ids)}")

    return unique_ids


def main() -> None:
    """Main scraping logic."""
    output_file = Path(__file__).parent.parent / "database" / "analysis" / "genre_mappings.json"

    print("VMRebetiko.gr Genre Mapping Scraper")
    print("=" * 60)
    print(f"Collections to scrape: {len(COLLECTIONS)}")
    print(f"Output file: {output_file}")
    print("=" * 60)

    genre_mappings = {}

    for genre_id, genre_name in COLLECTIONS.items():
        item_ids = scrape_genre(genre_id, genre_name)
        genre_mappings[genre_id] = {
            "name_en": genre_id.replace("_", " ").title(),
            "name_el": genre_name,
            "items": item_ids,
            "count": len(item_ids),
        }

        # Save incrementally in case of crash
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(genre_mappings, f, ensure_ascii=False, indent=2)

    # Print summary
    print("\n" + "=" * 60)
    print("SCRAPING COMPLETE")
    print("=" * 60)
    total_items = sum(g["count"] for g in genre_mappings.values())
    print(f"Total collections: {len(genre_mappings)}")
    print(f"Total item-genre mappings: {total_items}")
    print("\nBreakdown by genre:")
    for genre_id, data in sorted(genre_mappings.items(), key=lambda x: x[1]["count"], reverse=True):
        print(f"  {data['name_el']:30s} {data['count']:5d} items")
    print(f"\nSaved to: {output_file}")
    print("=" * 60)


if __name__ == "__main__":
    main()
