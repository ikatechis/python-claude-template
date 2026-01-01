#!/usr/bin/env python3
"""Fetch missing lyrics from rebet.gr JSON and import into database.

This script matches database songs with lyrics from lyrics_rebet.json
(scraped from rebet.gr) and allows selective import. Focuses on Greek
rebetiko songs (containing Greek letters).

Usage:
    python tools/fetch_lyrics_online.py                # Interactive mode
    python tools/fetch_lyrics_online.py --confirm-all  # Auto-import matches
    python tools/fetch_lyrics_online.py --limit 20     # Process 20 songs
"""

import json
import sqlite3
import sys
from pathlib import Path


def get_db_path() -> Path:
    """Get database path."""
    return Path(__file__).parent.parent / "database" / "vmrebetiko_all_genres.db"


def get_lyrics_json_path() -> Path:
    """Get lyrics JSON file path."""
    return Path(__file__).parent.parent / "database" / "lyrics_rebet.json"


def load_lyrics_json() -> dict[str, dict]:
    """Load lyrics from JSON file."""
    json_path = get_lyrics_json_path()
    if not json_path.exists():
        print(f"Error: {json_path} not found")
        sys.exit(1)
    with open(json_path, encoding="utf-8") as f:
        return json.load(f)


def get_greek_songs(db_path: Path, limit: int = 50) -> list[dict]:
    """Get Greek-titled songs without lyrics."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute(
        "SELECT id, title, creator_composer FROM items WHERE lyrics IS NULL LIMIT ?",
        (limit * 3,),
    )
    rows = [dict(row) for row in cur.fetchall()]
    conn.close()
    # Filter for Greek letters
    return [r for r in rows if any(ord(c) > 128 for c in r["title"])][:limit]


def clean_lyrics(text: str) -> str:
    """Remove markup from lyrics."""
    return text.replace("]]", "").replace("[\n", "").strip()


def find_match(title: str, lyrics_data: dict) -> tuple[str, str] | None:
    """Find matching lyrics by title. Returns (json_key, lyrics) or None."""
    title_lower = title.lower().strip()
    first_word = title_lower.split()[0] if title_lower else ""

    # Exact match
    for key in lyrics_data:
        if key.lower() == title_lower:
            return (key, clean_lyrics(lyrics_data[key]["lyrics"]))

    # Substring match (key in title)
    for key in lyrics_data:
        key_lower = key.lower()
        if len(key_lower) > 3 and key_lower in title_lower:
            return (key, clean_lyrics(lyrics_data[key]["lyrics"]))

    # First word match
    if len(first_word) > 3:
        for key in lyrics_data:
            if key.lower().split()[0] == first_word:
                return (key, clean_lyrics(lyrics_data[key]["lyrics"]))

    return None


def show_match(title: str, creator: str | None, lyrics: str, limit: int = 100):
    """Display song match to user."""
    preview = lyrics[:limit].replace("\n", " ")
    print(f"\n  Title:   {title}")
    if creator:
        print(f"  Creator: {creator.replace(chr(10), ' ').strip()[:50]}")
    print(f"  Preview: {preview}...")


def confirm(title: str, creator: str | None, lyrics: str) -> str:
    """Confirm import. Returns: 'y'=import, 'n'=skip, 'a'=auto, 's'=skip rest."""
    show_match(title, creator, lyrics)
    resp = input("\nImport? (y/n/a=auto/s=skip rest): ").strip().lower()
    return resp if resp in "ynas" else confirm(title, creator, lyrics)


def update_db(db_path: Path, song_id: str, lyrics: str) -> bool:
    """Update lyrics in database."""
    try:
        conn = sqlite3.connect(db_path)
        conn.cursor().execute("UPDATE items SET lyrics = ? WHERE id = ?", (lyrics, song_id))
        conn.commit()
        conn.close()
        return True
    except sqlite3.Error as e:
        print(f"DB error: {e}")
        return False


def main():
    """Main function."""
    # Parse args
    auto_confirm = "--confirm-all" in sys.argv
    limit = 50
    for arg in sys.argv[1:]:
        if arg.startswith("--limit"):
            limit = int(arg.split("=")[1]) if "=" in arg else 50

    db_path = get_db_path()
    if not db_path.exists():
        print(f"Error: {db_path} not found")
        sys.exit(1)

    print("Loading lyrics...")
    lyrics_data = load_lyrics_json()
    print(f"Loaded {len(lyrics_data)} songs\n")

    print("Fetching Greek-titled songs without lyrics...")
    songs = get_greek_songs(db_path, limit)
    print(f"Found {len(songs)} songs to process\n")

    stats = {"found": 0, "imported": 0, "skipped": 0}
    skip_rest = False

    for song in songs:
        if skip_rest:
            break

        match = find_match(song["title"], lyrics_data)
        if not match:
            continue

        stats["found"] += 1
        key, lyrics = match

        if auto_confirm:
            show_match(song["title"], song.get("creator_composer"), lyrics)
            print("Importing...")
        else:
            print("=" * 70)
            resp = confirm(song["title"], song.get("creator_composer"), lyrics)

            if resp == "s":
                skip_rest = True
                continue
            if resp == "a":
                auto_confirm = True
            elif resp != "y":
                stats["skipped"] += 1
                continue

        if update_db(db_path, song["id"], lyrics):
            stats["imported"] += 1
            print("✓ Imported\n")
        else:
            stats["skipped"] += 1

    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"Found:    {stats['found']}")
    print(f"Imported: {stats['imported']}")
    print(f"Skipped:  {stats['skipped']}")
    print("=" * 70)


if __name__ == "__main__":
    main()
