# Genre Scraping Fix - Investigation Report

## Problem Summary

The original script `/root/projects/rebetiko-game/tools/scrape_genre_mappings.py` was returning ALL 6,960 items for every genre instead of filtering by genre.

## Root Cause

**Wrong URL pattern was being used:**
- ❌ Original: `https://vmrebetiko.gr/search/?g=GENRE_NAME` (e.g., `?g=Ρεμπέτικο`)
- ✓ Correct: `https://vmrebetiko.gr/collection/?id=GENRE_ID` (e.g., `?id=rebetiko`)

The `/search/?g=` parameter does NOT filter results - it returns all items regardless of the genre parameter value.

## Investigation Process

### 1. Examined HTML Structure

Checked the saved HTML files:
- `/root/projects/data-scraper-rebetiko/genres_page.html`
- `/root/projects/data-scraper-rebetiko/item_page.html`

Found that the musical genres page contains links with pattern: `/collection/?id=GENRE_ID`

### 2. Tested Collection URLs

Created test script to verify the correct URLs:
```bash
# Rebetiko collection
https://vmrebetiko.gr/collection/?id=rebetiko

# Amanes collection
https://vmrebetiko.gr/collection/?id=amanes
```

Results:
- ✓ Each collection returns DIFFERENT items
- ✓ No overlap in the first 10 items between collections
- ✓ Items are correctly filtered by genre

### 3. Discovered Collection IDs

Found 17 collections on the musical genres page:

| Collection ID | Greek Name | English Name |
|---------------|------------|--------------|
| rebetiko | Ρεμπέτικο | Rebetiko |
| astiko_laiko | Αστικό λαϊκό | Urban Laiko |
| amanes | Αμανές | Amanes |
| dimotiko | Δημοτικό | Folk |
| dimotikofanes | Δημοτικοφανές | Folk-like |
| elafro | Ελαφρό | Light |
| epitheorisi | Επιθεώρηση | Revue |
| kinimatografos | Κινηματογράφος | Cinema |
| logia_diaskeui | Λόγια διασκευή | Art Song Arrangement |
| logio | Λόγιο | Art Music |
| opera | Όπερα | Opera |
| opereta | Οπερέτα | Operetta |
| theatro_skion | Θέατρο σκιών | Shadow Theater |
| xena | Ξένα | Foreign |
| xena_apo_ellhnes | Ξένα από Έλληνες | Foreign by Greeks |
| xena_ellhnikoi_stixoi | Ξένα ελληνικοί στίχοι | Foreign with Greek Lyrics |
| athinaiko_tragoudi | Αθηναϊκό τραγούδι | Athenian Song |

## Solution

Created fixed scraper: `/root/projects/rebetiko-game/tools/scrape_genre_mappings_fixed.py`

### Key Features:
1. ✓ Uses correct `/collection/?id=GENRE_ID` URLs
2. ✓ Paginates through all pages (40 items per page)
3. ✓ Saves incrementally (can resume if interrupted)
4. ✓ Deduplicates items within each collection
5. ✓ Skips already-scraped collections

### Usage:

```bash
# Run the fixed scraper
uv run python tools/scrape_genre_mappings_fixed.py

# Output will be saved to:
# database/analysis/genre_mappings.json
```

### Expected Output Format:

```json
{
  "rebetiko": {
    "name_en": "Rebetiko",
    "name_el": "Ρεμπέτικο",
    "items": ["2584", "2585", "2586", ...],
    "count": 10000
  },
  "amanes": {
    "name_en": "Amanes",
    "name_el": "Αμανές",
    "items": ["10804", "10808", ...],
    "count": 250
  },
  ...
}
```

## Performance Notes

- **Rebetiko collection** is very large (10,000+ items)
- Scraping all 17 collections will take approximately 30-60 minutes
- Script saves incrementally, so it can be stopped and resumed
- Politeness delay: 0.5 seconds between page requests

## Database Integration

Once genre mappings are scraped, they can be:
1. Added to the SQLite database as a new `genres` table
2. Linked to items via a junction table `item_genres`
3. Used for filtering and categorization in the game

Suggested schema:
```sql
CREATE TABLE genres (
    id TEXT PRIMARY KEY,
    name_en TEXT NOT NULL,
    name_el TEXT NOT NULL
);

CREATE TABLE item_genres (
    item_id TEXT NOT NULL,
    genre_id TEXT NOT NULL,
    PRIMARY KEY (item_id, genre_id),
    FOREIGN KEY (item_id) REFERENCES items(id),
    FOREIGN KEY (genre_id) REFERENCES genres(id)
);
```

## Verification

To verify the fix worked, check that:
1. Different collections have different items (no 100% overlap)
2. Total unique items < sum of all collection counts (proves overlap exists)
3. Rebetiko collection has ~10,000 items (largest collection)
4. Smaller collections like opera, operetta have <100 items

## Files

- ✓ Fixed scraper: `tools/scrape_genre_mappings_fixed.py`
- ✓ Test script: `tools/test_collection_filtering.py`
- ❌ Old broken script: `tools/scrape_genre_mappings.py` (DO NOT USE)
