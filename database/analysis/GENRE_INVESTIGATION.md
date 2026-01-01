# Genre Field Investigation

## Summary

The genre field **does not exist** as metadata on individual item pages. Genre is a **collection-level classification** on the vmrebetiko.gr website.

## Key Findings

### 1. Original Scraping Behavior

The database (`vmrebetiko_all_genres.db`) was scraped **without genre filtering**, capturing all 6,960 items across all collections.

**Evidence:**
- File: `vmrebetiko_db_scraper.py` lines 264-279
- Field mapping does NOT include "Μουσικό είδος" (Musical Genre)
- Only these fields were mapped:
  - Τύπος, Δημιουργός, Στιχουργός, Χρονολογία έκδοσης, etc.

### 2. How Genres Work on the Website

Genres are organized as **collections** with dedicated URLs:
```
/collection/?id=rebetiko          → Rebetiko (657 items per website)
/collection/?id=astiko_laiko      → Astiko Laiko
/collection/?id=amanes            → Amanes
... (17 total collections)
```

### 3. Search Filtering

The website supports genre filtering via search parameter:
```
/search/?fmid=p&pg=0&g=Ρεμπέτικο
```

The scraper **has this capability** (lines 145-154) but it was **not used** when creating the database.

## All Collections Found

From `genres_page.html`:
1. `rebetiko` - Ρεμπέτικο
2. `astiko_laiko` - Αστικό λαϊκό
3. `amanes` - Αμανές
4. `dimotiko` - Δημοτικό
5. `dimotikofanes` - Δημοτικοφανές
6. `elafro` - Ελαφρό
7. `epitheorisi` - Επιθεώρηση
8. `kinimatografos` - Κινηματογράφος
9. `logia_diaskeui` - Λόγια διασκευή
10. `logio` - Λόγιο
11. `opera` - Όπερα
12. `opereta` - Οπερέτα
13. `theatro_skion` - Θέατρο σκιών
14. `xena` - Ξένα
15. `xena_apo_ellhnes` - Ξένα από Έλληνες
16. `xena_ellhnikoi_stixoi` - Ξένα ελληνικοί στίχοι
17. `athinaiko_tragoudi` - Αθηναϊκό τραγούδι

## Solution Options

### Option 1: Re-scrape by Genre (Slow, Complete)

Create separate databases for each genre:
```bash
python vmrebetiko_db_scraper.py --genre "Ρεμπέτικο" --db rebetiko.db
python vmrebetiko_db_scraper.py --genre "Αστικό λαϊκό" --db astiko.db
```

**Pros:** Complete, accurate
**Cons:** Time-consuming (6,960 items × 17 genres if items overlap)

### Option 2: Scrape Genre Mappings (Fast, Efficient)

Create a script to:
1. Query search pages for each genre
2. Extract item IDs for that genre
3. Create `item_genres` mapping table

**SQL Schema:**
```sql
CREATE TABLE genres (
    id INTEGER PRIMARY KEY,
    name_en TEXT UNIQUE,
    name_el TEXT UNIQUE,
    collection_id TEXT UNIQUE
);

CREATE TABLE item_genres (
    item_id TEXT,
    genre_id INTEGER,
    PRIMARY KEY (item_id, genre_id),
    FOREIGN KEY (item_id) REFERENCES items(id),
    FOREIGN KEY (genre_id) REFERENCES genres(id)
);
```

**Pros:** Fast, allows multi-genre items
**Cons:** Requires scraping search pages only

### Option 3: Use Heuristics (Current Fallback)

Continue using year + instrument + location heuristics to identify rebetiko songs.

**Pros:** Works offline, no scraping needed
**Cons:** Imprecise (you correctly identified this issue)

## Recommended Approach

**Option 2** - Scrape genre mappings:

1. Create `tools/scrape_genre_mappings.py` script
2. For each of the 17 collections:
   - Query search pages with genre filter
   - Extract all item IDs
3. Create Alembic migration to add `genres` and `item_genres` tables
4. Populate with scraped data

This will accurately identify the **657 rebetiko songs** the website claims to have.

## Website Discrepancy Note

You mentioned the website shows "657 rebetiko entries", but my year-based filter found 2,259 songs (1920-1944 Greek recordings). This suggests:
- Many 78rpm recordings from that era are NOT classified as rebetiko by Kounadis
- Genre classification is stricter than just era + geography
- We NEED the official genre data to be accurate

## Next Steps

1. ✅ Confirm with user which option to pursue
2. ⏳ Create genre scraping script (if Option 2)
3. ⏳ Add genres table migration
4. ⏳ Update lyrics fetching to target only true rebetiko songs
