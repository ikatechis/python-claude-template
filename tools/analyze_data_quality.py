#!/usr/bin/env python3
"""
Data Quality Analysis for Kounadis Database

Analyzes dance_rhythm and recording_place fields to identify variations
that need normalization. Outputs JSON report for lookup table creation.
"""

import json
import sqlite3
from collections import defaultdict
from pathlib import Path

DB_PATH = "database/vmrebetiko_all_genres.db"
OUTPUT_DIR = Path("database/analysis")
OUTPUT_DIR.mkdir(exist_ok=True)


def analyze_dance_rhythm(conn):
    """Analyze all dance_rhythm values and their variations."""
    cursor = conn.cursor()

    # Get all non-null dance_rhythm values
    rhythms = cursor.execute(
        "SELECT dance_rhythm, COUNT(*) as count FROM items WHERE dance_rhythm IS NOT NULL GROUP BY dance_rhythm ORDER BY count DESC"
    ).fetchall()

    print(f"\n{'=' * 80}")
    print("DANCE_RHYTHM ANALYSIS")
    print(f"{'=' * 80}\n")

    print(f"Total unique values: {len(rhythms)}")
    print(f"Total items with rhythm: {sum(r[1] for r in rhythms)}\n")

    # Group by patterns
    patterns = defaultdict(list)

    for rhythm, count in rhythms:
        # Identify patterns
        has_brackets = "[" in rhythm or "]" in rhythm
        has_parens = "(" in rhythm or ")" in rhythm
        has_question = "?" in rhythm
        is_compound = (
            " - " in rhythm
            or ", " in rhythm
            or " / " in rhythm
            or (has_brackets and not rhythm.startswith("["))
        )

        key = "compound" if is_compound else "simple"
        if has_brackets:
            key = "bracketed"
        if has_question:
            key = "uncertain"

        patterns[key].append((rhythm, count))

    print("Patterns found:")
    for pattern_type, items in patterns.items():
        print(f"\n{pattern_type.upper()} ({len(items)} variations):")
        for rhythm, count in sorted(items, key=lambda x: x[1], reverse=True)[:10]:
            print(f"  {count:4} | {rhythm}")

    # Find base forms (most common variations)
    base_forms = {}
    for rhythm, count in rhythms:
        # Strip brackets and normalize
        clean = rhythm.strip("[]()").strip()
        if clean in base_forms:
            base_forms[clean].append((rhythm, count))
        else:
            base_forms[clean] = [(rhythm, count)]

    print("\n\nBASE FORMS (with variations):")
    for base, variations in sorted(
        base_forms.items(), key=lambda x: sum(v[1] for v in x[1]), reverse=True
    )[:20]:
        total = sum(v[1] for v in variations)
        print(f"\n{base} (total: {total})")
        for variant, count in sorted(variations, key=lambda x: x[1], reverse=True):
            if variant != base:
                print(f"    {count:4} | {variant}")

    return {
        "total_unique": len(rhythms),
        "total_items": sum(r[1] for r in rhythms),
        "top_20": [{"rhythm": r[0], "count": r[1]} for r in rhythms[:20]],
        "all_values": [{"rhythm": r[0], "count": r[1]} for r in rhythms],
        "base_forms": {
            base: [{"variant": v[0], "count": v[1]} for v in variations]
            for base, variations in base_forms.items()
        },
    }


def analyze_recording_place(conn):
    """Analyze all recording_place values and their variations."""
    cursor = conn.cursor()

    places = cursor.execute(
        "SELECT recording_place, COUNT(*) as count FROM items WHERE recording_place IS NOT NULL GROUP BY recording_place ORDER BY count DESC"
    ).fetchall()

    print(f"\n\n{'=' * 80}")
    print("RECORDING_PLACE ANALYSIS")
    print(f"{'=' * 80}\n")

    print(f"Total unique values: {len(places)}")
    print(f"Total items with place: {sum(p[1] for p in places)}\n")

    # Categorize
    uncertain = []
    compound = []
    clean = []

    for place, count in places:
        if "?" in place or ";" in place:
            uncertain.append((place, count))
        elif " ή " in place or ", " in place or " / " in place:
            compound.append((place, count))
        else:
            clean.append((place, count))

    print(f"UNCERTAIN PLACES ({len(uncertain)}):")
    for place, count in sorted(uncertain, key=lambda x: x[1], reverse=True)[:15]:
        print(f"  {count:4} | {place}")

    print(f"\nCOMPOUND PLACES ({len(compound)}):")
    for place, count in sorted(compound, key=lambda x: x[1], reverse=True)[:15]:
        print(f"  {count:4} | {place}")

    print(f"\nCLEAN PLACES ({len(clean)}) - Top 20:")
    for place, count in sorted(clean, key=lambda x: x[1], reverse=True)[:20]:
        print(f"  {count:4} | {place}")

    # Find base forms (strip uncertainty markers)
    base_forms = {}
    for place, count in places:
        # Strip question marks, parentheses, semicolons
        clean_place = (
            place.replace("(?)", "")
            .replace("(", "")
            .replace(")", "")
            .replace(";", "")
            .replace("?", "")
            .strip()
        )

        if clean_place in base_forms:
            base_forms[clean_place].append((place, count))
        else:
            base_forms[clean_place] = [(place, count)]

    print("\n\nBASE FORMS (with variations):")
    for base, variations in sorted(
        base_forms.items(), key=lambda x: sum(v[1] for v in x[1]), reverse=True
    )[:15]:
        if len(variations) > 1:  # Only show bases with variations
            total = sum(v[1] for v in variations)
            print(f"\n{base} (total: {total})")
            for variant, count in sorted(variations, key=lambda x: x[1], reverse=True):
                if variant != base:
                    print(f"    {count:4} | {variant}")

    return {
        "total_unique": len(places),
        "total_items": sum(p[1] for p in places),
        "uncertain_count": len(uncertain),
        "compound_count": len(compound),
        "clean_count": len(clean),
        "top_20": [{"place": p[0], "count": p[1]} for p in places[:20]],
        "all_values": [{"place": p[0], "count": p[1]} for p in places],
        "uncertain": [{"place": p[0], "count": p[1]} for p in uncertain],
        "compound": [{"place": p[0], "count": p[1]} for p in compound],
        "base_forms": {
            base: [{"variant": v[0], "count": v[1]} for v in variations]
            for base, variations in base_forms.items()
        },
    }


def main():
    """Run analysis and output JSON report."""
    conn = sqlite3.connect(DB_PATH)

    rhythm_analysis = analyze_dance_rhythm(conn)
    place_analysis = analyze_recording_place(conn)

    # Save report
    report = {
        "generated_at": "2026-01-01",
        "database": DB_PATH,
        "dance_rhythm": rhythm_analysis,
        "recording_place": place_analysis,
    }

    output_file = OUTPUT_DIR / "data_quality_report.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    print(f"\n\n{'=' * 80}")
    print("REPORT SAVED")
    print(f"{'=' * 80}\n")
    print(f"Report saved to: {output_file}")

    conn.close()


if __name__ == "__main__":
    main()
