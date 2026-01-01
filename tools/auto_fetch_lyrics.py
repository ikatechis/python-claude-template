#!/usr/bin/env python3
"""Automated lyrics finder using local JSON + optional WebSearch.

For 1920-1944 era rebetiko songs without lyrics:
1. Query DB for songs
2. Try matching against lyrics_rebet.json (scraped from rebet.gr)
3. If not found, optionally fetch via manual entry/WebSearch
4. Show preview and confirm before updating DB

Usage:
    python tools/auto_fetch_lyrics.py                # Interactive mode
    python tools/auto_fetch_lyrics.py --limit 10    # Process 10 songs
    python tools/auto_fetch_lyrics.py --auto        # Auto-import all
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


def load_lyrics_json() -> dict:
    """Load lyrics from JSON file."""
    json_path = get_lyrics_json_path()
    if not json_path.exists():
        return {}
    try:
        with open(json_path, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError):
        return {}


def get_songs_without_lyrics(db_path: Path, limit: int = 10) -> list[dict]:
    """Get Greek-titled songs from 1920-1944 without lyrics."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    cur.execute(
        """
        SELECT id, title, creator_composer, recording_date FROM items
        WHERE lyrics IS NULL AND recording_date IS NOT NULL
        AND substr(recording_date, 1, 4) BETWEEN '1920' AND '1944'
        ORDER BY recording_date ASC LIMIT ?
    """,
        (limit * 2,),
    )

    rows = [dict(row) for row in cur.fetchall()]
    conn.close()
    # Filter for Greek titles (unicode > 127)
    return [r for r in rows if any(ord(c) > 127 for c in r["title"])][:limit]


def build_search_query(title: str, artist: str | None) -> str:
    """Build search query: '{title} {artist} στίχοι'."""
    artist_part = f" {artist.split()[0]}" if artist else ""
    return f"{title}{artist_part} στίχοι"


def find_lyrics_in_json(title: str, lyrics_data: dict) -> str | None:
    """Find matching lyrics in JSON (exact, substring, or first-word match)."""
    title_lower = title.lower().strip()
    first_word = title_lower.split()[0] if title_lower else ""

    for key in lyrics_data:
        key_lower = key.lower()
        # Try exact match
        if key_lower == title_lower:
            lyrics = lyrics_data[key].get("lyrics", "")
            if lyrics:
                return lyrics.replace("]]", "").replace("[\n", "").strip()
        # Try substring match
        if len(key_lower) > 3 and key_lower in title_lower:
            lyrics = lyrics_data[key].get("lyrics", "")
            if lyrics:
                return lyrics.replace("]]", "").replace("[\n", "").strip()
        # Try first word match
        if len(first_word) > 3 and key_lower.split()[0] == first_word:
            lyrics = lyrics_data[key].get("lyrics", "")
            if lyrics:
                return lyrics.replace("]]", "").replace("[\n", "").strip()

    return None


def show_song(
    title: str, artist: str | None, query: str, lyrics: str = "", status: str = ""
) -> None:
    """Display song info, query, and optional preview."""
    print(f"\n  Title:      {title}")
    if artist:
        print(f"  Artist:     {artist.replace(chr(10), ' ').strip()[:50]}")
    print(f"  Search:     {query}")
    if status:
        print(f"  Status:     {status}")
    if lyrics:
        preview = lyrics[:150].replace("\n", " ").strip()
        if len(lyrics) > 150:
            preview += "..."
        print(f"  Preview:    {preview}")


def confirm(title: str, artist: str | None, lyrics: str) -> str:
    """Ask confirmation (y/n/s). Returns user's choice."""
    show_song(title, artist, build_search_query(title, artist), lyrics)
    resp = input("\nImport lyrics? (y/n/s=skip rest): ").strip().lower()
    return resp if resp in "yns" else confirm(title, artist, lyrics)


def update_db(db_path: Path, song_id: str, lyrics: str) -> bool:
    """Update lyrics in database."""
    try:
        conn = sqlite3.connect(db_path)
        conn.cursor().execute("UPDATE items SET lyrics = ? WHERE id = ?", (lyrics, song_id))
        conn.commit()
        conn.close()
        return True
    except sqlite3.Error as e:
        print(f"  DB error: {e}")
        return False


def get_lyrics_manual() -> str:
    """Get lyrics from user input (Ctrl+D or END to finish)."""
    print("  Paste lyrics (Ctrl+D or END on new line to finish):")
    lines = []
    try:
        while True:
            line = input("  > ")
            if line.strip().upper() == "END":
                break
            lines.append(line)
    except EOFError:
        pass
    return "\n".join(lines).strip()


def main() -> None:
    """Main function."""
    # Parse arguments
    auto_mode = "--auto" in sys.argv
    limit = 10
    for arg in sys.argv[1:]:
        if arg.startswith("--limit"):
            limit = int(arg.split("=")[1]) if "=" in arg else 10

    db_path = get_db_path()
    if not db_path.exists():
        print(f"Error: {db_path} not found")
        sys.exit(1)

    print("Loading lyrics from lyrics_rebet.json...")
    lyrics_data = load_lyrics_json()
    print(f"Loaded {len(lyrics_data)} songs\n" if lyrics_data else "Warning: JSON file not found\n")

    print("Fetching songs from 1920-1944 without lyrics...")
    songs = get_songs_without_lyrics(db_path, limit)
    print(f"Found {len(songs)} songs\n")

    if not songs:
        print("No songs found!")
        sys.exit(0)

    stats = {"searched": 0, "found": 0, "imported": 0, "skipped": 0}
    skip_rest = False

    for song in songs:
        if skip_rest:
            break

        stats["searched"] += 1
        print("=" * 70)
        print(f"[{stats['searched']}/{len(songs)}] Searching...")

        # Try to find lyrics in JSON
        lyrics = find_lyrics_in_json(song["title"], lyrics_data)

        # If not found, ask for manual input
        if not lyrics:
            if not auto_mode:
                show_song(
                    song["title"],
                    song.get("creator_composer"),
                    build_search_query(song["title"], song.get("creator_composer")),
                    status="Not found in lyrics_rebet.json",
                )
                resp = input("\nSearch online? (y/n/s=skip rest): ").strip().lower()
                if resp == "s":
                    skip_rest = True
                    stats["skipped"] += 1
                    continue
                if resp != "y":
                    stats["skipped"] += 1
                    continue

            lyrics = get_lyrics_manual()

        if not lyrics:
            stats["skipped"] += 1
            continue

        stats["found"] += 1

        # Confirm import
        if auto_mode:
            show_song(
                song["title"],
                song.get("creator_composer"),
                build_search_query(song["title"], song.get("creator_composer")),
                lyrics,
            )
            print("[AUTO MODE] Importing...")
        else:
            resp = confirm(song["title"], song.get("creator_composer"), lyrics)

            if resp == "s":
                skip_rest = True
                stats["skipped"] += 1
                continue
            if resp != "y":
                stats["skipped"] += 1
                continue

        # Update database
        if update_db(db_path, song["id"], lyrics):
            stats["imported"] += 1
            print("✓ Imported")
        else:
            stats["skipped"] += 1

    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"Searched:  {stats['searched']}")
    print(f"Found:     {stats['found']}")
    print(f"Imported:  {stats['imported']}")
    print(f"Skipped:   {stats['skipped']}")
    print("=" * 70)


if __name__ == "__main__":
    main()
