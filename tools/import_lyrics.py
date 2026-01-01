#!/usr/bin/env python3
"""Import lyrics from lyrics_rebet.json into the database.

Handles three confidence levels:
- >= 0.85 (certain): Direct import
- 0.70-0.84 (uncertain): Ask user for confirmation
- < 0.70 (wrong): Skip
"""

import json
import shutil
import sqlite3
from pathlib import Path
from typing import Any


def clean_lyrics(lyrics: str) -> str:
    """Remove ]] markers from lyrics text."""
    return lyrics.replace("]]", "").replace("[\n", "").strip()


def load_songs_data() -> dict[str, dict[str, Any]]:
    """Load lyrics from JSON file."""
    json_path = Path(__file__).parent.parent / "database" / "lyrics_rebet.json"
    with open(json_path) as f:
        return json.load(f)


def load_match_report() -> dict[str, Any]:
    """Load match report with confidence scores."""
    report_path = (
        Path(__file__).parent.parent / "database" / "analysis" / "lyrics_match_report.json"
    )
    with open(report_path) as f:
        return json.load(f)


def get_db_lyrics(db_path: Path, song_id: str) -> str | None:
    """Get existing lyrics from database, if any."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT lyrics FROM items WHERE id = ?", (song_id,))
    row = cur.fetchone()
    conn.close()
    return row["lyrics"] if row else None


def update_db_lyrics(db_path: Path, song_id: str, lyrics: str) -> None:
    """Update lyrics in database."""
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("UPDATE items SET lyrics = ? WHERE id = ?", (lyrics, song_id))
    conn.commit()
    conn.close()


def confirm_match(lyric_title: str, db_title: str) -> str:
    """Ask user to confirm an uncertain match.

    Returns: 'y' (confirm), 'n' (reject), 's' (skip rest)
    """
    print(f"\n  Lyrics file: '{lyric_title}'")
    print(f"  Database:    '{db_title}'")
    response = input("  Confirm match? (y/n/s to skip rest): ").strip().lower()
    return response if response in ["y", "n", "s"] else confirm_match(lyric_title, db_title)


def main() -> None:
    """Main import logic."""
    db_path = Path(__file__).parent.parent / "database" / "vmrebetiko_all_genres.db"

    # Create backup
    backup_path = db_path.with_stem(f"{db_path.stem}_backup")
    shutil.copy2(db_path, backup_path)
    print(f"Backup created: {backup_path}")

    # Load data
    songs_data = load_songs_data()
    report = load_match_report()

    stats = {"imported": 0, "skipped": 0, "already_had": 0, "rejected": 0}
    skip_rest = False

    # Process certain matches (confidence >= 0.85)
    print("\nProcessing certain matches (confidence >= 0.85)...")
    for match in report["certain"]:
        song_id = match["song_id"]
        lyric_title = match["lyric_title"]

        if lyric_title not in songs_data:
            continue

        if get_db_lyrics(db_path, song_id):
            stats["already_had"] += 1
            continue

        lyrics = clean_lyrics(songs_data[lyric_title]["lyrics"])
        update_db_lyrics(db_path, song_id, lyrics)
        stats["imported"] += 1

    print(f"  Imported {stats['imported']} certain matches")

    # Process uncertain matches (0.70 <= confidence < 0.85)
    if not skip_rest:
        print("\nProcessing uncertain matches (0.70 <= confidence < 0.85)...")
        for match in report["uncertain"]:
            if skip_rest:
                break

            song_id = match["song_id"]
            lyric_title = match["lyric_title"]

            if lyric_title not in songs_data:
                stats["skipped"] += 1
                continue

            if get_db_lyrics(db_path, song_id):
                stats["already_had"] += 1
                continue

            response = confirm_match(lyric_title, match["matched_db_title"])
            if response == "s":
                skip_rest = True
                stats["skipped"] += 1
            elif response == "y":
                lyrics = clean_lyrics(songs_data[lyric_title]["lyrics"])
                update_db_lyrics(db_path, song_id, lyrics)
                stats["imported"] += 1
            else:  # 'n'
                stats["rejected"] += 1

    # Summary
    print("\n" + "=" * 50)
    print("IMPORT SUMMARY")
    print("=" * 50)
    print(f"Imported:      {stats['imported']}")
    print(f"Skipped:       {stats['skipped']}")
    print(f"Rejected:      {stats['rejected']}")
    print(f"Already had:   {stats['already_had']}")
    print(f"Total:         {sum(stats.values())}")
    print("=" * 50)


if __name__ == "__main__":
    main()
