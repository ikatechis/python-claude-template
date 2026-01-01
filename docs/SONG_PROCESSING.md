---
status: draft
version: 1.0.0
last_updated: 2026-01-01
dependencies: RAG_SETUP.md, DATABASE_MIGRATIONS.md
dependents: storylet generation, MUSIC_SYSTEM.md
note: References 'items' table (not 'kounadis_songs')
---

# Song Database Processing Guide

## Overview

The Kounadis database contains rebetiko songs with Greek lyrics. This guide describes how to batch-process the database to:

1. **Tag each song** with consistent themes from a fixed vocabulary
2. **Translate lyrics** to English (meaning, not literal)
3. **Extract story summaries** (what happens in the song)
4. **Pull usable fragments** (lines that could appear in-game)
5. **Generate storylet ideas** (situations inspired by the song)

---

## Fixed Vocabulary

All tags must come from these predefined pools. The model cannot invent new tags.

### Theme Tags

```python
THEME_TAGS = [
    # Love & Relationships
    "love",
    "heartbreak",
    "longing",
    "jealousy",
    "separation",

    # Crime & Law
    "prison",
    "police",
    "arrest",
    "injustice",
    "betrayal",
    "informer",
    "revenge",
    "violence",
    "knife",

    # Survival
    "poverty",
    "hunger",
    "work",
    "survival",

    # Substances
    "hashish",
    "alcohol",
    "addiction",

    # Death & Loss
    "death",
    "grief",
    "loss",
    "memory",

    # Identity & Place
    "exile",
    "refugee",
    "homeland",
    "sea",
    "journey",
    "piraeus",
    "smyrna",

    # Family
    "mother",
    "family",
    "children",

    # Music & Life
    "music",
    "bouzouki",
    "tekes",
    "performance",
    "kefi",
    "derti",

    # Attitude
    "defiance",
    "resignation",
    "fate",
    "honor",
    "pride"
]
```

### Mood Options

```python
MOOD_OPTIONS = [
    "defiant",
    "mournful",
    "joyful",
    "bitter",
    "nostalgic",
    "angry",
    "resigned",
    "romantic",
    "dark",
    "playful"
]
```

---

## Database Schema Updates

Add these columns to your Kounadis table before processing:

```sql
ALTER TABLE kounadis_songs ADD COLUMN themes TEXT;           -- JSON array
ALTER TABLE kounadis_songs ADD COLUMN translation_en TEXT;   -- Full English meaning
ALTER TABLE kounadis_songs ADD COLUMN story_summary TEXT;    -- What happens
ALTER TABLE kounadis_songs ADD COLUMN mood TEXT;             -- Single value from MOOD_OPTIONS
ALTER TABLE kounadis_songs ADD COLUMN usable_fragments TEXT; -- JSON array
ALTER TABLE kounadis_songs ADD COLUMN storylet_idea TEXT;    -- Single idea
ALTER TABLE kounadis_songs ADD COLUMN processed_at TEXT;     -- ISO timestamp
```

---

## The Prompt Template

Use this exact prompt for consistency:

```
You are helping tag a rebetiko song database for a narrative game.

<allowed_themes>
love, heartbreak, longing, jealousy, separation,
prison, police, arrest, injustice, betrayal, informer, revenge, violence, knife,
poverty, hunger, work, survival,
hashish, alcohol, addiction,
death, grief, loss, memory,
exile, refugee, homeland, sea, journey, piraeus, smyrna,
mother, family, children,
music, bouzouki, tekes, performance, kefi, derti,
defiance, resignation, fate, honor, pride
</allowed_themes>

<allowed_moods>
defiant, mournful, joyful, bitter, nostalgic, angry, resigned, romantic, dark, playful
</allowed_moods>

<song>
Title: {title}
Artist: {artist}
Year: {year}
Lyrics:
{lyrics}
</song>

Return ONLY valid JSON with these fields:

{
  "themes": ["tag1", "tag2"],
  "mood": "mood_value",
  "translation": "English meaning of lyrics...",
  "story_summary": "2-3 sentences: who, what, situation",
  "usable_fragments": [
    {"el": "Greek phrase", "en": "English meaning"},
    {"el": "Greek phrase", "en": "English meaning"}
  ],
  "storylet_idea": "One sentence storylet inspiration"
}

Rules:
- themes: Pick 2-5 tags from <allowed_themes> ONLY. Do not invent new tags.
- mood: Pick exactly ONE from <allowed_moods> ONLY.
- translation: Convey meaning and feeling, not word-for-word. Keep Greek terms that have no English equivalent (ντέρτι, μάγκας, κέφι, αργιλές, etc.) untranslated. The result should read as English poetry.
- story_summary: Who is speaking? To whom? What situation? What emotion?
- usable_fragments: 2-3 short phrases (under 8 words) that could work as NPC dialogue, player thoughts, or environmental text. Include Greek and English meaning.
- storylet_idea: A game situation inspired by this song. NOT "player hears the song" — instead, the underlying situation (e.g., "The player's friend is arrested; they must decide whether to visit him in prison").

Return ONLY the JSON object. No preamble, no explanation, no markdown.
```

---

## Example Output

Input song: "Σύννεφα" (Clouds) by Vamvakaris

```json
{
  "themes": ["exile", "mother", "homeland", "grief", "longing"],
  "mood": "mournful",
  "translation": "Clouds passing by, where are you going?\nUp to the mountains, down to the sea?\nIf you pass over my village\ntell my mother I'm alive.\n\nTell her not to wait for me.\nThe road back is closed.\nTell her I think of her\nevery night when I can't sleep.\n\nClouds, you travel free.\nI'm trapped here in this city.\nMy mother's hands that held me—\nI'll never feel them again.",
  "story_summary": "A refugee speaks to the clouds, asking them to carry a message to his mother in his lost homeland. He knows he will never return. The tone is quiet grief, not dramatic — just the weight of permanent separation.",
  "usable_fragments": [
    {"el": "Πες της να μη με περιμένει", "en": "Tell her not to wait for me"},
    {"el": "Ο δρόμος πίσω έκλεισε", "en": "The road back is closed"},
    {"el": "Σύννεφα που περνάτε", "en": "Clouds passing by"}
  ],
  "storylet_idea": "The player learns their mother died in a refugee camp before they could send money home. A quiet scene on a rooftop at dusk, watching clouds move toward the east."
}
```

---

## Model Choice

**Use Claude Haiku.** This is structured extraction, not complex reasoning.

| Model | Input/M | Output/M | 500 songs |
|-------|---------|----------|-----------|
| Sonnet | $3.00 | $15.00 | ~$4.00 |
| Haiku | $0.25 | $1.25 | ~$0.50 |

The entire database can be processed for under $1.

---

## Processing Script Structure

```python
import sqlite3
import json
import time
from datetime import datetime
from anthropic import Anthropic

# Configuration
DB_PATH = "database/kounadis.db"
MODEL = "claude-haiku-4-20250514"
BATCH_SIZE = 50
RATE_LIMIT_DELAY = 0.5  # seconds between requests

# Fixed vocabulary
THEME_TAGS = [
    "love", "heartbreak", "longing", "jealousy", "separation",
    "prison", "police", "arrest", "injustice", "betrayal",
    "informer", "revenge", "violence", "knife",
    "poverty", "hunger", "work", "survival",
    "hashish", "alcohol", "addiction",
    "death", "grief", "loss", "memory",
    "exile", "refugee", "homeland", "sea", "journey", "piraeus", "smyrna",
    "mother", "family", "children",
    "music", "bouzouki", "tekes", "performance", "kefi", "derti",
    "defiance", "resignation", "fate", "honor", "pride"
]

MOOD_OPTIONS = [
    "defiant", "mournful", "joyful", "bitter", "nostalgic",
    "angry", "resigned", "romantic", "dark", "playful"
]

client = Anthropic()

def build_prompt(song):
    """Build the analysis prompt for a song."""
    return f"""You are helping tag a rebetiko song database for a narrative game.

<allowed_themes>
{", ".join(THEME_TAGS)}
</allowed_themes>

<allowed_moods>
{", ".join(MOOD_OPTIONS)}
</allowed_moods>

<song>
Title: {song['title']}
Artist: {song['artist'] or 'Unknown'}
Year: {song['year'] or 'Unknown'}
Lyrics:
{song['lyrics']}
</song>

Return ONLY valid JSON with these fields:

{{
  "themes": ["tag1", "tag2"],
  "mood": "mood_value",
  "translation": "English meaning of lyrics...",
  "story_summary": "2-3 sentences: who, what, situation",
  "usable_fragments": [
    {{"el": "Greek phrase", "en": "English meaning"}}
  ],
  "storylet_idea": "One sentence storylet inspiration"
}}

Rules:
- themes: Pick 2-5 tags from <allowed_themes> ONLY
- mood: Pick exactly ONE from <allowed_moods> ONLY
- translation: Meaning, not literal. Keep untranslatable Greek terms.
- usable_fragments: 2-3 short phrases under 8 words each
- storylet_idea: A situation inspired by the song, not "player hears song"

Return ONLY the JSON. No explanation."""


def validate_analysis(analysis):
    """Validate and clean the analysis."""

    # Filter invalid themes
    valid_themes = [t for t in analysis.get('themes', []) if t in THEME_TAGS]
    if not valid_themes:
        valid_themes = ['unknown']
    analysis['themes'] = valid_themes

    # Validate mood
    if analysis.get('mood') not in MOOD_OPTIONS:
        analysis['mood'] = 'unknown'

    return analysis


def process_song(song):
    """Send song to Claude, get structured analysis."""

    prompt = build_prompt(song)

    response = client.messages.create(
        model=MODEL,
        max_tokens=1500,
        messages=[{"role": "user", "content": prompt}]
    )

    text = response.content[0].text.strip()

    # Handle potential markdown wrapping
    if text.startswith("```"):
        text = text.split("```")[1]
        if text.startswith("json"):
            text = text[4:]

    analysis = json.loads(text)
    return validate_analysis(analysis)


def update_database(cursor, song_id, analysis):
    """Write analysis back to database."""

    cursor.execute("""
        UPDATE kounadis_songs SET
            themes = ?,
            translation_en = ?,
            story_summary = ?,
            mood = ?,
            usable_fragments = ?,
            storylet_idea = ?,
            processed_at = ?
        WHERE id = ?
    """, (
        json.dumps(analysis['themes']),
        analysis['translation'],
        analysis['story_summary'],
        analysis['mood'],
        json.dumps(analysis['usable_fragments']),
        analysis['storylet_idea'],
        datetime.now().isoformat(),
        song_id
    ))


def main():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Get unprocessed songs
    songs = cursor.execute("""
        SELECT * FROM kounadis_songs
        WHERE processed_at IS NULL
        AND lyrics IS NOT NULL
        AND lyrics != ''
    """).fetchall()

    total = len(songs)
    print(f"Processing {total} songs...")

    success = 0
    failed = []

    for i, song in enumerate(songs):
        print(f"[{i+1}/{total}] {song['title'][:50]}...")

        try:
            analysis = process_song(dict(song))
            update_database(cursor, song['id'], analysis)
            conn.commit()
            success += 1
        except json.JSONDecodeError as e:
            print(f"  JSON error: {e}")
            failed.append((song['id'], song['title'], str(e)))
        except Exception as e:
            print(f"  Error: {e}")
            failed.append((song['id'], song['title'], str(e)))

        # Rate limiting
        time.sleep(RATE_LIMIT_DELAY)

        # Checkpoint every batch
        if (i + 1) % BATCH_SIZE == 0:
            print(f"  Checkpoint: {success} successful, {len(failed)} failed")

    print(f"\nComplete: {success} successful, {len(failed)} failed")

    if failed:
        print("\nFailed songs:")
        for song_id, title, error in failed:
            print(f"  [{song_id}] {title}: {error}")

    conn.close()


if __name__ == "__main__":
    main()
```

---

## Running the Script

```bash
# Activate environment
cd rebetiko-game
source venv/bin/activate

# First, add the new columns
sqlite3 database/kounadis.db < tools/add_song_columns.sql

# Run processing
python tools/process_songs.py

# Check results
sqlite3 database/kounadis.db "SELECT COUNT(*) FROM kounadis_songs WHERE processed_at IS NOT NULL"
```

---

## Querying the Processed Database

After processing, you can query by theme:

```sql
-- Find all prison songs
SELECT title, story_summary, mood
FROM kounadis_songs
WHERE themes LIKE '%"prison"%';

-- Find mournful songs about mothers
SELECT title, translation_en
FROM kounadis_songs
WHERE themes LIKE '%"mother"%'
AND mood = 'mournful';

-- Find usable fragments about betrayal
SELECT title, usable_fragments
FROM kounadis_songs
WHERE themes LIKE '%"betrayal"%'
OR themes LIKE '%"informer"%';

-- Get storylet ideas for police scenes
SELECT title, storylet_idea
FROM kounadis_songs
WHERE themes LIKE '%"police"%'
OR themes LIKE '%"arrest"%';

-- Find defiant songs for performance scenes
SELECT title, mood, themes
FROM kounadis_songs
WHERE mood = 'defiant';
```

---

## Quality Control

After processing:

1. **Spot check 20-30 songs** — Are translations good? Are themes accurate?
2. **Check for unknowns** — `SELECT * FROM kounadis_songs WHERE mood = 'unknown'`
3. **Review fragments** — Do they read naturally as dialogue?
4. **Validate JSON** — Ensure all JSON columns parse correctly

```sql
-- Find songs that might need review
SELECT title, themes, mood
FROM kounadis_songs
WHERE mood = 'unknown'
   OR themes = '["unknown"]'
   OR themes = '[]';
```

---

## Embedding for RAG

After processing, embed the enriched data in ChromaDB:

```python
# Combine fields for richer embeddings
doc_text = f"""
Title: {song['title']}
Themes: {', '.join(json.loads(song['themes']))}
Mood: {song['mood']}
Story: {song['story_summary']}
Translation: {song['translation_en'][:500]}
"""

collection.add(
    documents=[doc_text],
    metadatas=[{
        "title": song['title'],
        "artist": song['artist'],
        "themes": song['themes'],
        "mood": song['mood']
    }],
    ids=[f"song_{song['id']}"]
)
```

Now semantic queries like "song about missing home" will find songs tagged with `exile`, `homeland`, `longing` even without exact word matches.

---

## Open Questions

- [ ] Should instrumental songs (no lyrics) be tagged differently?
- [ ] How to handle songs with unclear or corrupted lyrics?
- [ ] Should we store multiple storylet ideas per song?
- [ ] Do we need a "confidence" score for the analysis?
