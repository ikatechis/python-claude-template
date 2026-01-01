#!/usr/bin/env python3
"""
Analyze genre (Μουσικό είδος) classification for vmrebetiko database items.

Uses heuristics and existing metadata to classify items as Ρεμπέτικο (rebetiko)
based on attributes like creator, recording place, era, and musical characteristics.

Usage:
    uv run python tools/fetch_genres.py [--limit 100] [--sample] [--db DATABASE]
"""

import argparse
import json
import sqlite3
from pathlib import Path

from tqdm import tqdm


def classify_as_rebetiko(item_id: str, metadata: str | None) -> bool:
    """
    Classify item as rebetiko based on metadata heuristics.

    Rebetiko criteria:
    - Recording from Piraeus, Athens, or other port cities (1920-1940)
    - Creator names associated with rebetiko tradition
    - Keywords in title or metadata

    Args:
        item_id: Database item ID (for logging)
        metadata: JSON metadata string

    Returns:
        True if likely rebetiko, False otherwise
    """
    if not metadata:
        return False

    try:
        data = json.loads(metadata)
    except json.JSONDecodeError:
        return False

    # Known rebetiko composers and singers
    rebetiko_artists = {
        "Βολής",
        "Παπαΐωάννου",
        "Καράμπατη",
        "Τσιτσάνης",
        "Νταγιαν",
        "Βαμβακάρης",
        "Πολυδόρου",
        "Λόγος",
        "Ζάττας",
        "Κόκκοτας",
        "Βουγιουκλάκης",
        "Λυραντωνής",
        "Σαντούρια",
        "Ραμόνα",
        "Κατερίνα",
    }

    # Check creators
    creator = data.get("Δημιουργός (Συνθέτης)", "").lower()
    for artist in rebetiko_artists:
        if artist.lower() in creator.lower():
            return True

    # Check recording places (major rebetiko centers)
    recording_place = data.get("Τόπος ηχογράφησης", "").lower()
    rebetiko_places = {"πειραιάς", "πειραιευς", "αθήνα", "νέα υόρκη"}
    if any(place in recording_place for place in rebetiko_places):
        # Check era (rebetiko: 1920-1940)
        rec_date = data.get("Χρονολογία ηχογράφησης", "")
        if rec_date and "19" in rec_date:
            try:
                year = int(rec_date[:4])
                if 1900 <= year <= 1960:
                    return True
            except (ValueError, IndexError):
                pass

    # Check item type
    item_type = data.get("Τύπος", "").lower()
    if "δίσκος" in item_type or "δίσκο" in item_type:
        # 78 RPM records are likely rebetiko if from right era
        pub_date = data.get("Χρονολογία έκδοσης", "")
        if pub_date and "19" in pub_date:
            try:
                year = int(pub_date[:4])
                if 1920 <= year <= 1950:
                    return True
            except (ValueError, IndexError):
                pass

    return False


def analyze_genres(
    db_path: Path, limit: int | None = None, sample: bool = False
) -> dict[str, list[str]]:
    """
    Analyze genres for items in database.

    Args:
        db_path: Path to SQLite database
        limit: Limit items to analyze (for testing)
        sample: Only analyze 10 examples

    Returns:
        Dictionary mapping classification to lists of item IDs
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    query = "SELECT id, metadata_json FROM items WHERE metadata_json IS NOT NULL"
    if limit:
        query += f" LIMIT {limit}"

    cursor.execute(query)
    items = cursor.fetchall()
    conn.close()

    if sample:
        print("Sample mode: analyzing first 10 items")
        items = items[:10]

    classifications: dict[str, list[str]] = {
        "rebetiko": [],
        "other": [],
    }

    print(f"Analyzing {len(items)} items...")

    for item_id, metadata in tqdm(items, desc="Classifying"):
        if classify_as_rebetiko(item_id, metadata):
            classifications["rebetiko"].append(item_id)
        else:
            classifications["other"].append(item_id)

    return classifications


def generate_report(classifications: dict[str, list[str]]) -> None:
    """
    Generate and print classification report.

    Args:
        classifications: Dictionary mapping genre to item IDs
    """
    print("\n" + "=" * 70)
    print("GENRE ANALYSIS REPORT")
    print("=" * 70)

    rebetiko_count = len(classifications["rebetiko"])
    other_count = len(classifications["other"])
    total = rebetiko_count + other_count

    print(f"\nTotal items analyzed: {total}")
    print(f"Ρεμπέτικο items: {rebetiko_count} ({rebetiko_count / total * 100:.1f}%)")
    print(f"Other items: {other_count} ({other_count / total * 100:.1f}%)")

    if rebetiko_count > 0:
        print("\nExample Ρεμπέτικο items (first 10):")
        for item_id in classifications["rebetiko"][:10]:
            print(f"  - {item_id}")

    print("\n" + "=" * 70)


def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Analyze genre classification for vmrebetiko database items"
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=100,
        help="Limit number of items to analyze (default: 100 for testing)",
    )
    parser.add_argument("--sample", action="store_true", help="Analyze only 10 items as sample")
    parser.add_argument(
        "--db",
        type=Path,
        default=Path("/root/projects/rebetiko-game/database/vmrebetiko_all_genres.db"),
        help="Path to database file",
    )

    args = parser.parse_args()

    print(f"Database: {args.db}")
    print(f"Limit: {args.limit}")

    classifications = analyze_genres(args.db, limit=args.limit, sample=args.sample)
    generate_report(classifications)


if __name__ == "__main__":
    main()
