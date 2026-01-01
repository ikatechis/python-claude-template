#!/usr/bin/env python3
"""Match lyrics from lyrics_rebet.json to database items by title.

Uses fuzzy matching to handle title variations, URL slugs, and accent differences.
Produces a JSON report with match confidence scores.
"""

import json
import re
import sqlite3
import unicodedata
from difflib import SequenceMatcher
from pathlib import Path

# Common filler words to ignore in fuzzy matching
COMMON_WORDS = {"και", "αν", "για", "να", "με", "στο", "της", "του", "η", "ο"}


def normalize_text(text: str) -> str:
    """Normalize Greek text for matching (remove accents, lowercase)."""
    if not text:
        return ""
    nfd = unicodedata.normalize("NFD", text)
    text = "".join(c for c in nfd if unicodedata.category(c) != "Mn")
    return text.lower().strip()


def extract_title_parts(title: str) -> list[str]:
    """Split title by parentheses to handle 'Main(Subtitle)' format.

    Example: 'Καλόγερος(Βαρέθηκα τις γκόμενες)' -> ['Καλόγερος', 'Βαρέθηκα τις γκόμενες']
    """
    if "(" not in title:
        return [title]
    match = re.match(r"^([^()]+)\(([^()]+)\)$", title)
    if match:
        return [match.group(1), match.group(2)]
    return [title]


def extract_title_from_slug(slug: str) -> str:
    """Extract title from URL slug."""
    parts = slug.split("--")
    title = parts[0].replace("-", " ")
    return title.title()


def has_meaningful_overlap(text1: str, text2: str) -> bool:
    """Check if texts share meaningful content (not just common words).

    Requires at least 3-4 char overlap on short titles.
    """
    words1 = set(text1.split()) - COMMON_WORDS
    words2 = set(text2.split()) - COMMON_WORDS

    if not words1 or not words2:
        return False

    common = words1 & words2
    if not common:
        return False

    # For short titles, require character-level overlap too
    if min(len(text1), len(text2)) < 15:
        common_chars = sum(len(w) for w in common)
        return common_chars >= 3

    return True


def similarity_score(a: str, b: str) -> float:
    """Calculate similarity with meaningful word overlap check."""
    # Quick rejection: only common words overlap
    if not has_meaningful_overlap(a, b):
        return 0.0

    matcher = SequenceMatcher(None, a, b)
    return matcher.ratio()


def match_title(
    lyrics_title: str, url_slug: str, db_titles: list[str]
) -> tuple[str | None, float, str]:
    """Match a lyrics title against database titles.

    Returns: (best_match_title, confidence_score, match_reason)
    """
    # Extract main and subtitle parts from lyrics title
    lyric_parts = extract_title_parts(lyrics_title)
    slug_title = extract_title_from_slug(url_slug)

    candidates = [
        (lyric_parts[0], "main"),
        (slug_title, "slug"),
    ]
    if len(lyric_parts) > 1:
        candidates.append((lyric_parts[1], "subtitle"))

    best_match = None
    best_score = 0.0
    best_reason = ""

    for candidate, source in candidates:
        norm_candidate = normalize_text(candidate)

        for db_title in db_titles:
            norm_db = normalize_text(db_title)
            score = similarity_score(norm_candidate, norm_db)

            if score > best_score:
                best_score = score
                best_match = db_title
                best_reason = source

    return best_match, best_score, best_reason


def main() -> None:
    """Match lyrics to database and generate report."""
    lyrics_file = Path("database/lyrics_rebet.json")
    db_file = Path("database/vmrebetiko_all_genres.db")

    # Load lyrics
    with open(lyrics_file) as f:
        lyrics_data = json.load(f)

    # Load database titles
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute("SELECT id, title FROM items ORDER BY title")
    db_items = cursor.fetchall()
    db_titles = [item[1] for item in db_items]
    db_title_to_id = {item[1]: item[0] for item in db_items}
    conn.close()

    # Match each lyric
    certain = []
    uncertain = []
    wrong = []

    for lyric_title, lyric_data in lyrics_data.items():
        url_slug = lyric_data["url"].split("/songs/")[-1]
        best_match, confidence, reason = match_title(lyric_title, url_slug, db_titles)

        result = {
            "lyric_title": lyric_title,
            "url_slug": url_slug,
            "matched_db_title": best_match,
            "confidence": round(confidence, 3),
            "match_source": reason,
            "song_id": db_title_to_id.get(best_match) if best_match else None,
        }

        if confidence >= 0.85:
            certain.append(result)
        elif confidence >= 0.70:
            uncertain.append(result)
        else:
            wrong.append(result)

    # Generate report
    report = {
        "metadata": {
            "total_lyrics": len(lyrics_data),
            "certain": len(certain),
            "uncertain": len(uncertain),
            "likely_wrong": len(wrong),
        },
        "certain": sorted(certain, key=lambda x: x["confidence"], reverse=True),
        "uncertain": sorted(uncertain, key=lambda x: x["confidence"], reverse=True),
        "likely_wrong": sorted(wrong, key=lambda x: x["confidence"], reverse=True),
    }

    # Write report
    with open("database/analysis/lyrics_match_report.json", "w") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    print("Match Report:")
    print(f"  Total lyrics: {report['metadata']['total_lyrics']}")
    print(f"  Certain (>=0.85): {report['metadata']['certain']}")
    print(f"  Uncertain (0.70-0.84): {report['metadata']['uncertain']}")
    print(f"  Likely wrong (<0.70): {report['metadata']['likely_wrong']}")
    print("\nReport saved to: database/analysis/lyrics_match_report.json")


if __name__ == "__main__":
    main()
