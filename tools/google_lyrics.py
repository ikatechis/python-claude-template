#!/usr/bin/env python3
"""Find lyrics using Google search for songs without lyrics.

Focuses on 1920-1944 era rebetiko songs. For each song:
1. Build search query: "{title} {artist} στίχοι"
2. Use Google to find lyrics
3. Show preview and ask confirmation
4. Update database if confirmed

Usage:
    python tools/google_lyrics.py                # Interactive mode
    python tools/google_lyrics.py --limit 10    # Process 10 songs
    python tools/google_lyrics.py --auto        # Auto-import all
"""

import sqlite3
import sys
from pathlib import Path


def get_db_path() -> Path:
    """Get database path."""
    return Path(__file__).parent.parent / "database" / "vmrebetiko_all_genres.db"


def get_songs_without_lyrics(db_path: Path, limit: int = 20) -> list[dict]:
    """Get songs from 1920-1944 era without lyrics.

    Prioritizes songs that are likely to have lyrics available online.
    """
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    # Get songs from 1920-1944 without lyrics, ordered by date
    cur.execute(
        """
        SELECT id, title, creator_composer, date_issued
        FROM items
        WHERE lyrics IS NULL
        AND date_issued IS NOT NULL
        AND substr(date_issued, 1, 4) >= '1920'
        AND substr(date_issued, 1, 4) <= '1944'
        ORDER BY date_issued ASC
        LIMIT ?
    """,
        (limit * 2,),
    )

    rows = [dict(row) for row in cur.fetchall()]
    conn.close()

    # Filter for Greek titles (more likely to have Greek lyrics online)
    return [r for r in rows if any(ord(c) > 127 for c in r["title"])][:limit]


def build_search_query(title: str, artist: str | None) -> str:
    """Build Google search query for lyrics.

    Example: "Μινόρε της αυγής Τσιτσάνης στίχοι"
    """
    query = f"{title} στίχοι"
    if artist:
        # Clean artist name (remove newlines, take first name if multiple)
        artist_clean = artist.replace("\n", " ").strip().split()[0]
        query = f"{title} {artist_clean} στίχοι"
    return query


def show_preview(title: str, artist: str | None, query: str, limit: int = 100):
    """Display song and search query to user."""
    print(f"\n  Title:      {title}")
    if artist:
        print(f"  Artist:     {artist.replace(chr(10), ' ').strip()[:50]}")
    print(f"  Search:     {query}")
    print("  Status:     Ready to search on Google")


def confirm_search(title: str, artist: str | None, query: str) -> str:
    """Ask user to confirm search. Returns: 'y'=search, 'n'=skip, 's'=skip rest."""
    show_preview(title, artist, query)
    resp = input("\nSearch for lyrics? (y/n/s=skip rest): ").strip().lower()
    return resp if resp in "yns" else confirm_search(title, artist, query)


def get_lyrics_from_user() -> str:
    """Get lyrics from user input."""
    print("\nPaste lyrics below (Ctrl+D or type END on new line to finish):")
    lines = []
    try:
        while True:
            line = input()
            if line.strip().upper() == "END":
                break
            lines.append(line)
    except EOFError:
        pass
    return "\n".join(lines).strip()


def update_db_lyrics(db_path: Path, song_id: str, lyrics: str) -> bool:
    """Update lyrics in database."""
    try:
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute("UPDATE items SET lyrics = ? WHERE id = ?", (lyrics, song_id))
        conn.commit()
        conn.close()
        return True
    except sqlite3.Error as e:
        print(f"DB error: {e}")
        return False


def main():
    """Main function."""
    # Parse arguments
    auto_mode = "--auto" in sys.argv
    limit = 20
    for arg in sys.argv[1:]:
        if arg.startswith("--limit"):
            limit = int(arg.split("=")[1]) if "=" in arg else 20

    db_path = get_db_path()
    if not db_path.exists():
        print(f"Error: {db_path} not found")
        sys.exit(1)

    print("Fetching songs from 1920-1944 without lyrics...")
    songs = get_songs_without_lyrics(db_path, limit)
    print(f"Found {len(songs)} songs\n")

    if not songs:
        print("No songs found!")
        sys.exit(0)

    stats = {"processed": 0, "imported": 0, "skipped": 0}
    skip_rest = False

    for song in songs:
        if skip_rest:
            break

        stats["processed"] += 1
        query = build_search_query(song["title"], song.get("creator_composer"))

        print("=" * 70)

        if auto_mode:
            show_preview(song["title"], song.get("creator_composer"), query)
            print("[AUTO MODE] Visit search link and paste lyrics\n")
            resp = input("Paste lyrics? (y/n/s=skip rest): ").strip().lower()
            if resp not in "yns":
                resp = "n"
        else:
            resp = confirm_search(song["title"], song.get("creator_composer"), query)

        if resp == "s":
            skip_rest = True
            stats["skipped"] += 1
            continue

        if resp != "y":
            stats["skipped"] += 1
            continue

        # Get lyrics from user
        lyrics = get_lyrics_from_user()
        if not lyrics:
            print("No lyrics provided, skipping")
            stats["skipped"] += 1
            continue

        # Update database
        if update_db_lyrics(db_path, song["id"], lyrics):
            stats["imported"] += 1
            print("✓ Imported")
        else:
            stats["skipped"] += 1

    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"Processed: {stats['processed']}")
    print(f"Imported:  {stats['imported']}")
    print(f"Skipped:   {stats['skipped']}")
    print("=" * 70)
    print("\nTip: Use queries like: 'Μινόρε της αυγής Τσιτσάνης στίχοι'")


if __name__ == "__main__":
    main()
