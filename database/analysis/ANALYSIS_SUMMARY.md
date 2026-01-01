---
status: stable
version: 1.0.0
last_updated: 2025-01-01
---

# Kounadis Archive Database - Comprehensive Analysis

**Database:** vmrebetiko_all_genres.db
**Analysis Date:** 2025-01-01
**Total Items:** 6,960

## Executive Summary

The Kounadis archive database contains **6,960 historical items** spanning multiple media types (78rpm records, sheet music, interviews, biographies). For the rebetiko game, we have identified **1,689 songs from the 1920-1944 era**, of which **189 have complete lyrics** (11.2%).

### Key Findings

- ✅ **All files downloaded:** 6,570 audio + 4,644 PDFs + 5,257 images
- ✅ **48 metadata fields discovered** with varying fill rates
- ✅ **537 items total with Στίχοι (lyrics) field** across all types
- ⚠️ **1,500 rebetiko songs need lyrics** from external sources
- ✅ **Rich metadata:** Composer (77%), Lyricist (77%), Publisher (83%)

## Item Type Breakdown

| Type | Count | Percentage |
|------|-------|------------|
| Δίσκος 78 Στροφών (78rpm records) | 3,096 | 44.5% |
| Έντυπη Παρτιτούρα (Sheet music) | 2,296 | 33.0% |
| Βιογραφικό (Biographies) | 381 | 5.5% |
| Φωτογραφία (Photographs) | 170 | 2.4% |
| Συνέντευξη (Interviews) | 52 | 0.7% |
| Ταχυδρομική κάρτα (Postcards) | 149 | 2.1% |
| Σημειώσεις (Notes) | 374 | 5.4% |
| Other types | 442 | 6.4% |

## Rebetiko Era Songs (1920-1944)

**Total:** 1,689 Greek 78rpm recordings

### By Decade

| Decade | Count | With Lyrics | Lyrics % |
|--------|-------|-------------|----------|
| 1920-1929 | 489 | 47 | 9.6% |
| 1930-1939 | 1,089 | 131 | 12.0% |
| 1940-1944 | 111 | 11 | 9.9% |

### Top Composers (in rebetiko era songs)

1. **Τσιτσάνης Βασίλης** - 89 songs
2. **Βάμβακος Μάρκος** - 87 songs
3. **Τούντας Γιάννης** - 76 songs
4. **Παγιατάκης Βαγγέλης** - 54 songs
5. **Σκαρβέλης Στρατός** - 51 songs

### Language Distribution (all items)

| Language | Count | Percentage |
|----------|-------|------------|
| Ελληνικά (Greek) | 5,328 | 93.3% |
| Ελληνικά-Αγγλικά | 117 | 2.0% |
| Αγγλικά (English) | 73 | 1.3% |
| Ελληνικά-Γαλλικά | 42 | 0.7% |
| Other combinations | 151 | 2.6% |

## Metadata Field Analysis

### High Fill Rate (>80%)

| Field | Fill Rate | Unique Values | Notes |
|-------|-----------|---------------|-------|
| Προέλευση (Provenance) | 94.4% | 39 | Mostly "Αρχείο Κουνάδη" |
| Αναγνωριστικό (Identifier) | 94.5% | 6,577 | Nearly unique IDs |
| Άδεια χρήσης (License) | 94.3% | 4 | Mostly "cc" |
| Φυσική περιγραφή | 91.9% | 1,455 | Physical condition |
| Εκδότης (Publisher) | 83.3% | 776 | Record labels, publishers |
| Γλώσσα/ες (Languages) | 82.1% | 77 | Language combinations |

### Medium Fill Rate (40-80%)

| Field | Fill Rate | Unique Values | Notes |
|-------|-----------|---------------|-------|
| Δημιουργός (Συνθέτης) | 77.1% | 1,007 | Composers |
| Στιχουργός (Lyricist) | 76.7% | 1,315 | Lyricists |
| Τραγουδιστές (Singers) | 44.4% | - | Vocalists |
| Ορχήστρα-Εκτελεστές | 38.5% | - | Orchestra/performers |
| Τόπος έκδοσης | 40.1% | 115 | Publication place |

### Critical Low Fill Rate (<40%)

| Field | Fill Rate | Unique Values | Impact |
|-------|-----------|---------------|--------|
| **Στίχοι (Lyrics)** | **7.7%** | - | ⚠️ CRITICAL for game |
| Πρώτες λέξεις | 31.4% | 2,024 | First words/incipit |
| Χρονολογία έκδοσης | 26.0% | 149 | Publication date |
| Χορός / Ρυθμός | 15.0% | - | Dance/rhythm type |
| Διεύθυνση Ορχήστρας | 9.2% | - | Conductor |

## Lyrics Coverage Analysis

### Current Status

- **Items with Στίχοι field:** 537 (7.7% of all items)
- **Rebetiko songs with lyrics:** 189 (11.2% of 1,689)
- **Songs without lyrics:** 1,500 (88.8%)

### Lyrics Sources

1. **In database (Στίχοι):** 189 songs
2. **lyrics_rebet.json:** 649 songs total
   - Cross-reference needed for exact matches
   - Estimated ~100-150 additional matches
3. **External sources needed:** ~1,350-1,400 songs
   - stixoi.info
   - rebetiko.gr
   - Manual transcription from sheet music/audio

### Lyrics Field Content

Items with lyrics contain:
- Full Greek lyrics (Στίχοι field in metadata_json)
- Average length: 200-800 characters
- Some include translations (Ελληνικά-Αγγλικά items)
- Some truncated with "..." indicating more verses

## Historical Research Material

### Interviews (Συνέντευξη)

- **Count:** 52 interviews
- **Content:** Audio recordings with interviewees from rebetiko era
- **Fill rate for Συνεντευξιαζόμενος:** 0.7%
- **Use case:** RAG context for authentic voices, historical details

### Biographies (Βιογραφικό)

- **Count:** 381 artist biographies
- **Content:** Life stories of musicians, composers, lyricists
- **Fields:** Birth/death dates, birthplace, profession (Ιδιότητα)
- **Use case:** NPC characterization, historical accuracy

### Photographs & Postcards

- **Φωτογραφία:** 170 images
- **Ταχυδρομική κάρτα:** 149 postcards
- **Content:** Historical Piraeus, Athens, musicians, venues
- **Use case:** Visual reference for ComfyUI art generation

## Recording Details (78rpm Records)

For items with recording metadata:

- **Χρονολογία ηχογράφησης:** 44.2% fill rate
- **Τόπος ηχογράφησης:** 44.5% fill rate
  - Primary locations: Βερολίνο, Κωνσταντινούπολη, Αθήνα
- **Αριθμός καταλόγου:** 44.5% fill rate (catalog numbers)
- **Αριθμός μήτρας:** 43.8% fill rate (matrix numbers)
- **Διάρκεια:** 45.2% fill rate (2:00-3:30 average)

## Files Downloaded Status

| File Type | Count | Status |
|-----------|-------|--------|
| Audio files | 6,570 | ✅ All downloaded |
| PDF documents | 4,644 | ✅ All downloaded |
| Images | 5,257 | ✅ All downloaded |

**Total files:** 241,449 files across all items

## Data Quality Assessment

### Strengths

- ✅ **Complete provenance:** 94%+ items traced to Κουνάδη archive
- ✅ **High composer/lyricist attribution:** 77%
- ✅ **Consistent identifiers:** Nearly unique IDs
- ✅ **Rich publisher data:** 83% with publisher info
- ✅ **All files present:** Audio, PDFs, images downloaded

### Gaps

- ⚠️ **Low lyrics coverage:** Only 11% of rebetiko songs
- ⚠️ **Missing publication dates:** 74% without date
- ⚠️ **Limited dance/rhythm tags:** Only 15%
- ⚠️ **Sparse conductor info:** Only 9%
- ⚠️ **Inconsistent metadata formatting:** Needs normalization

### Data Normalization Needed

1. **Composer names:** Inconsistent formatting
   - "Τούντας Γιάννης" vs "Γιάννης Τούντας"
   - "[Χατζηαποστόλου Νίκος]" (brackets indicate uncertainty)
2. **Dates:** Multiple formats
   - "1933" vs "[Πρώτη έκδοση: 1876]" vs "7/4/1922"
3. **Languages:** Need standardization
   - "Ελληνικά-Αγγλικά" vs "Ελληνικά - Αγγλικά"

## Priority Actions

### Immediate

1. ✅ **Export analysis to JSON** - DONE
2. ⏳ **Set up Notion workspace** - IN PROGRESS
3. ⏳ **Import 1,689 songs to Notion** - PENDING
4. ⏳ **Cross-reference lyrics_rebet.json** - PENDING

### Short-term

1. Normalize composer/lyricist names
2. Extract and categorize all tags from historical descriptions
3. Match songs with external lyrics sources (stixoi.info)
4. Create embeddings for all songs with metadata

### Medium-term

1. Transcribe sheet music lyrics (for items with PDFs)
2. Process interview audio for RAG context
3. Extract musician biographies for NPC inspiration
4. Create genre/mood taxonomy from metadata

## Files Generated

**Location:** `database/analysis/`

1. **field_statistics.json**
   - Fill rates for all 17 standard fields
   - Unique value counts

2. **metadata_fields.json**
   - All 48 metadata fields discovered
   - Counts and examples for each

3. **items_with_lyrics.json**
   - 537 items with Στίχοι field
   - Includes item type, language, lyrics length

4. **rebetiko_era_songs.json**
   - 1,689 songs (1920-1944)
   - Ready for Notion import
   - Fields: id, title, composer, year, has_lyrics

## Recommendations

### For RAG Pipeline

1. **Embed all song metadata** (title, composer, year, description)
2. **Embed lyrics separately** with song reference
3. **Embed interview transcripts** for contextual authenticity
4. **Embed biographies** for NPC character depth

### For Notion Workflow

1. **Import all 1,689 songs** to Songs Database
2. **Mark priority songs** (1927-1931 golden era)
3. **Manual review UI** for lyrics matching
4. **Track processing status** (lyrics, tags, embeddings)

### For Content Generation

1. **Use songs WITH lyrics first** for storylet prototypes
2. **Reference interviews** for authentic dialogue patterns
3. **Use biographies** for NPC background generation
4. **Use photographs** for visual style references

---

**Next Steps:** See `docs/MCP_QUICK_START.md` for Notion setup and `docs/RAG_SETUP.md` for embedding pipeline.
