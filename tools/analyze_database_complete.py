#!/usr/bin/env python3
"""
Comprehensive Kounadis Database Analysis
Exhaustively examines all fields, extracts all unique values, and documents the complete schema.
"""

import json
import sqlite3
from collections import defaultdict
from pathlib import Path

DB_PATH = "database/vmrebetiko_all_genres.db"
OUTPUT_DIR = Path("database/analysis")
OUTPUT_DIR.mkdir(exist_ok=True)


def analyze_database():
    """Comprehensive database analysis"""

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    print("=" * 80)
    print("COMPREHENSIVE KOUNADIS DATABASE ANALYSIS")
    print("=" * 80)

    # ============================================================================
    # 1. TABLE STRUCTURE
    # ============================================================================
    print("\n### 1. TABLE STRUCTURE ###\n")

    tables = cursor.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()

    for table in tables:
        table_name = table["name"]
        print(f"\nTable: {table_name}")
        print("-" * 40)

        # Get schema
        schema = cursor.execute(f"PRAGMA table_info({table_name})").fetchall()
        for col in schema:
            print(f"  {col['name']:20} {col['type']:10} {'NOT NULL' if col['notnull'] else 'NULL'}")

        # Get count
        count = cursor.execute(f"SELECT COUNT(*) FROM {table_name}").fetchone()[0]
        print(f"\n  Total rows: {count:,}")

    # ============================================================================
    # 2. ITEMS TABLE - FIELD ANALYSIS
    # ============================================================================
    print("\n\n### 2. ITEMS TABLE - FIELD-BY-FIELD ANALYSIS ###\n")

    # Get all items
    items = cursor.execute("SELECT * FROM items").fetchall()
    total_items = len(items)

    # Analyze each standard field
    fields = [
        "id",
        "url",
        "title",
        "item_type",
        "creator_composer",
        "lyricist",
        "publication_date",
        "publication_place",
        "publisher",
        "language",
        "first_words",
        "physical_description",
        "provenance",
        "identifier",
        "license",
        "reference",
        "scraped_at",
    ]

    field_stats = {}

    for field in fields:
        non_null = sum(1 for item in items if item[field])
        unique_values = len(set(item[field] for item in items if item[field]))

        field_stats[field] = {
            "total": total_items,
            "non_null": non_null,
            "null": total_items - non_null,
            "fill_rate": f"{(non_null / total_items) * 100:.1f}%",
            "unique_values": unique_values,
        }

        print(
            f"{field:25} : {non_null:5}/{total_items:5} ({field_stats[field]['fill_rate']:6}) | {unique_values:5} unique values"
        )

    # ============================================================================
    # 3. METADATA_JSON - COMPREHENSIVE FIELD EXTRACTION
    # ============================================================================
    print("\n\n### 3. METADATA_JSON - ALL FIELDS FOUND ###\n")

    all_metadata_fields = defaultdict(int)
    metadata_field_examples = defaultdict(list)

    for item in items:
        if item["metadata_json"]:
            try:
                metadata = json.loads(item["metadata_json"])
                for key, value in metadata.items():
                    all_metadata_fields[key] += 1
                    if len(metadata_field_examples[key]) < 3 and value:
                        metadata_field_examples[key].append(str(value)[:100])
            except:
                pass

    print("Metadata fields found (sorted by frequency):\n")
    for field, count in sorted(all_metadata_fields.items(), key=lambda x: x[1], reverse=True):
        fill_rate = (count / total_items) * 100
        print(f"{field:40} : {count:5}/{total_items:5} ({fill_rate:5.1f}%)")
        if metadata_field_examples[field]:
            for example in metadata_field_examples[field][:2]:
                print(f"  → {example}")

    # ============================================================================
    # 4. CRITICAL FIELD: ΣΤΙΧΟΙ (LYRICS)
    # ============================================================================
    print("\n\n### 4. LYRICS ANALYSIS (Στίχοι field) ###\n")

    items_with_lyrics = []
    for item in items:
        if item["metadata_json"]:
            try:
                metadata = json.loads(item["metadata_json"])
                if "Στίχοι" in metadata and metadata["Στίχοι"]:
                    items_with_lyrics.append(
                        {
                            "id": item["id"],
                            "title": item["title"],
                            "type": item["item_type"],
                            "language": item["language"],
                            "lyrics_length": len(metadata["Στίχοι"]),
                        }
                    )
            except:
                pass

    print(f"Total items with Στίχοι: {len(items_with_lyrics)}")

    # Breakdown by type
    lyrics_by_type = defaultdict(int)
    for item in items_with_lyrics:
        lyrics_by_type[item["type"]] += 1

    print("\nBreakdown by item type:")
    for item_type, count in sorted(lyrics_by_type.items(), key=lambda x: x[1], reverse=True):
        print(f"  {item_type:40} : {count}")

    # Breakdown by language
    lyrics_by_language = defaultdict(int)
    for item in items_with_lyrics:
        lang = item["language"] or "Unknown"
        lyrics_by_language[lang] += 1

    print("\nBreakdown by language:")
    for lang, count in sorted(lyrics_by_language.items(), key=lambda x: x[1], reverse=True):
        print(f"  {lang:40} : {count}")

    # ============================================================================
    # 5. ITEM TYPES - COMPREHENSIVE BREAKDOWN
    # ============================================================================
    print("\n\n### 5. ITEM TYPES - DETAILED BREAKDOWN ###\n")

    type_breakdown = cursor.execute("""
        SELECT item_type, COUNT(*) as count
        FROM items
        GROUP BY item_type
        ORDER BY count DESC
    """).fetchall()

    for row in type_breakdown:
        print(f"{row['item_type']:40} : {row['count']:5}")

    # ============================================================================
    # 6. LANGUAGES
    # ============================================================================
    print("\n\n### 6. LANGUAGES ###\n")

    lang_breakdown = cursor.execute("""
        SELECT language, COUNT(*) as count
        FROM items
        WHERE language IS NOT NULL
        GROUP BY language
        ORDER BY count DESC
    """).fetchall()

    for row in lang_breakdown[:20]:
        print(f"{row['language']:40} : {row['count']:5}")

    # ============================================================================
    # 7. COMPOSERS (Top 50)
    # ============================================================================
    print("\n\n### 7. TOP 50 COMPOSERS ###\n")

    composer_breakdown = cursor.execute("""
        SELECT creator_composer, COUNT(*) as count
        FROM items
        WHERE creator_composer IS NOT NULL
        GROUP BY creator_composer
        ORDER BY count DESC
        LIMIT 50
    """).fetchall()

    for row in composer_breakdown:
        print(f"{row['creator_composer']:40} : {row['count']:5}")

    # ============================================================================
    # 8. FILES ANALYSIS
    # ============================================================================
    print("\n\n### 8. FILES TABLE ANALYSIS ###\n")

    file_breakdown = cursor.execute("""
        SELECT file_type,
               COUNT(*) as total,
               SUM(CASE WHEN downloaded = 1 THEN 1 ELSE 0 END) as downloaded
        FROM files
        GROUP BY file_type
    """).fetchall()

    for row in file_breakdown:
        print(f"{row['file_type']:15} : {row['downloaded']:6}/{row['total']:6} downloaded")

    # ============================================================================
    # 9. REBETIKO ERA ANALYSIS (1920-1944)
    # ============================================================================
    print("\n\n### 9. REBETIKO ERA (1920-1944) - 78RPM GREEK RECORDINGS ###\n")

    rebetiko_songs = []
    for item in items:
        if (
            item["item_type"] == "Δίσκος 78 Στροφών"
            and item["language"]
            and "Ελληνικά" in item["language"]
        ):
            if item["metadata_json"]:
                try:
                    metadata = json.loads(item["metadata_json"])
                    rec_date = metadata.get("Χρονολογία ηχογράφησης", "")
                    year = None
                    if "/" in rec_date:
                        parts = rec_date.split("/")
                        if len(parts) == 3:
                            year = int(parts[-1])
                    elif rec_date.isdigit() and len(rec_date) == 4:
                        year = int(rec_date)

                    if year and 1920 <= year <= 1944:
                        rebetiko_songs.append(
                            {
                                "id": item["id"],
                                "title": item["title"],
                                "composer": item["creator_composer"],
                                "year": year,
                                "has_lyrics": bool(metadata.get("Στίχοι")),
                            }
                        )
                except:
                    pass

    print(f"Total Greek 78rpm recordings (1920-1944): {len(rebetiko_songs)}")
    print(f"With lyrics: {sum(1 for s in rebetiko_songs if s['has_lyrics'])}")
    print(f"Without lyrics: {sum(1 for s in rebetiko_songs if not s['has_lyrics'])}")

    # By year
    year_counts = defaultdict(int)
    for song in rebetiko_songs:
        year_counts[song["year"]] += 1

    print("\nBy year:")
    for year in sorted(year_counts.keys()):
        print(f"  {year}: {year_counts[year]:3} recordings")

    # ============================================================================
    # 10. EXPORT DATA TO JSON FILES
    # ============================================================================
    print("\n\n### 10. EXPORTING ANALYSIS TO FILES ###\n")

    # Export all metadata fields with examples
    with open(OUTPUT_DIR / "metadata_fields.json", "w", encoding="utf-8") as f:
        output = {}
        for field, count in all_metadata_fields.items():
            output[field] = {
                "count": count,
                "fill_rate": f"{(count / total_items) * 100:.1f}%",
                "examples": metadata_field_examples[field][:5],
            }
        json.dump(output, f, ensure_ascii=False, indent=2)
    print(f"✓ Metadata fields exported to {OUTPUT_DIR / 'metadata_fields.json'}")

    # Export items with lyrics
    with open(OUTPUT_DIR / "items_with_lyrics.json", "w", encoding="utf-8") as f:
        json.dump(items_with_lyrics, f, ensure_ascii=False, indent=2)
    print(f"✓ Items with lyrics exported to {OUTPUT_DIR / 'items_with_lyrics.json'}")

    # Export rebetiko songs list
    with open(OUTPUT_DIR / "rebetiko_era_songs.json", "w", encoding="utf-8") as f:
        json.dump(rebetiko_songs, f, ensure_ascii=False, indent=2)
    print(f"✓ Rebetiko era songs exported to {OUTPUT_DIR / 'rebetiko_era_songs.json'}")

    # Export field statistics
    with open(OUTPUT_DIR / "field_statistics.json", "w", encoding="utf-8") as f:
        json.dump(field_stats, f, ensure_ascii=False, indent=2)
    print(f"✓ Field statistics exported to {OUTPUT_DIR / 'field_statistics.json'}")

    # ============================================================================
    # SUMMARY REPORT
    # ============================================================================
    print("\n\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"""
Total items in database: {total_items:,}
Items with lyrics (Στίχοι): {len(items_with_lyrics)}
Greek 78rpm (1920-1944): {len(rebetiko_songs)}
  - With lyrics: {sum(1 for s in rebetiko_songs if s["has_lyrics"])}
  - Without lyrics: {sum(1 for s in rebetiko_songs if not s["has_lyrics"])}

Top item types:
  - 78rpm records: {sum(1 for item in items if item["item_type"] == "Δίσκος 78 Στροφών"):,}
  - Sheet music: {sum(1 for item in items if item["item_type"] == "Έντυπη Παρτιτούρα"):,}
  - Interviews: {sum(1 for item in items if item["item_type"] == "Συνέντευξη"):,}
  - Artist bios: {sum(1 for item in items if item["item_type"] == "Καλλιτέχνης"):,}

Files:
  - Audio files: {cursor.execute('SELECT COUNT(*) FROM files WHERE file_type = "audio"').fetchone()[0]:,}
  - PDFs: {cursor.execute('SELECT COUNT(*) FROM files WHERE file_type = "pdfs"').fetchone()[0]:,}
  - Images: {cursor.execute('SELECT COUNT(*) FROM files WHERE file_type = "images"').fetchone()[0]:,}

Analysis files created in: {OUTPUT_DIR}/
""")

    conn.close()


if __name__ == "__main__":
    analyze_database()
