---
status: draft
version: 0.1.0
last_updated: 2025-01-01
---

# Lyrics Coverage Analysis

**Database:** vmrebetiko_all_genres.db + lyrics_rebet.json

---

## ✅ Current Status

### Lyrics Available:
- **189 songs** with lyrics in database (Στίχοι field in metadata_json)
- **101 songs** matched with lyrics_rebet.json
- **Total: 290 songs with lyrics (17% of 1,689 rebetiko-era recordings)**

### Still Needed:
- **1,399 songs** (83%) need lyrics from external sources

---

## 📊 Coverage by Source

| Source | Count | Quality |
|--------|-------|---------|
| Kounadis Database (Στίχοι field) | 189 | High - direct from archive |
| lyrics_rebet.json | 101 | High - verified matches |
| **Total Available** | **290** | |
| External sources needed | 1,399 | TBD |

---

## 🎯 Strategy

### Phase 1: Merge Existing Data (This Week)
1. **Create unified database:**
   ```sql
   CREATE TABLE songs_rebetiko (
       kounadis_id TEXT PRIMARY KEY,
       title TEXT,
       composer TEXT,
       lyricist TEXT,
       year INTEGER,
       lyrics_greek TEXT,
       lyrics_source TEXT,  -- 'kounadis', 'rebet_json', 'external', 'manual'
       -- Processing fields
       themes TEXT,
       mood TEXT,
       translation_en TEXT,
       story_summary TEXT,
       usable_fragments TEXT,
       storylet_idea TEXT,
       processed_at TEXT
   );
   ```

2. **Import Kounadis lyrics (189 songs):**
   - Extract from metadata_json Στίχοι field
   - Mark as source='kounadis'

3. **Import lyrics_rebet.json (101 songs):**
   - Match by normalized title
   - Mark as source='rebet_json'

4. **Result: 290 songs ready to process**

### Phase 2: External Lyrics (Next Week)
For the remaining 1,399 songs, prioritize by:

**Priority Tier 1 (Top 100):**
- Famous composers: Vamvakaris, Tsitsanis, Papaioannou, Mitsakis
- Peak years: 1927-1931
- Songs mentioned in interviews or research

**Sources to try:**
1. **stixoi.info** - Large Greek lyrics database
2. **lyricstranslate.com** - Often has rebetiko with translations
3. **YouTube video descriptions** - Many rebetiko uploads include lyrics
4. **Historical books** - Petropoulos collections
5. **Manual transcription** - For critically important songs

**Approach:**
- Build scraper for stixoi.info (respect robots.txt)
- Search by song title + composer
- Verify lyrics match (check first line against audio if available)
- Manual search for top 20-30 most important songs

### Phase 3: Processing (Week 3)
Once we have 300-500 songs with lyrics:
1. Apply SONG_PROCESSING.md workflow
2. Use Claude Haiku for:
   - Theme tagging (from fixed vocabulary)
   - Mood classification
   - English translation (meaning, not literal)
   - Story summary
   - Usable fragments (dialogue-ready lines)
   - Storylet ideas

Cost: ~$0.01 per song × 500 = ~$5

---

## 🔍 Sample Matched Songs

Perfect matches from lyrics_rebet.json:

| Year | Database Title | JSON Title | Match |
|------|----------------|------------|-------|
| 1934 | Αγιοθοδωρίτισσα | Αγιοθοδωρίτισσα | 100% |
| 1931 | Αδυνάτισα ο καημένος | Αδυνάτισα ο καημένος | 100% |
| 1930 | Αλανιάρα μερακλού | Αλανιάρα μερακλού | 100% |
| 1928 | Αλατσατιανή | Αλατσατιανή | 100% |
| 1936 | Αλεξανδριανή φελάχα | Αλεξανδριανή φελάχα | 100% |

Fuzzy matches (variant titles):

| Year | Database Title | JSON Title | Match |
|------|----------------|------------|-------|
| 1936 | Αλανιάρα | Αλανιάρης | 82% |
| 1927 | Αυτά τα μαύρα μάτια | Γι' αυτά τα μαύρα μάτια σου | 83% |

---

## 📋 Sample Songs Needing Lyrics

From the 1,399 without lyrics:

| Year | Title | Composer | Priority |
|------|-------|----------|----------|
| 1929 | Arap sabah taksim | Άγνωστος | Medium |
| 1927 | Α! Κακούργα Έλλη | Άγνωστος | Low |
| 1933 | Αγαπησιάρης | Τούντας Παναγιώτης | **HIGH** |
| 1933 | Αγαπώ μια παντρεμένη | Άγνωστος | Low |

---

## 🎮 Game Implications

### With 290 Songs (Current):
- **Sufficient for vertical slice** (need ~30-50 for demo)
- Can select best songs by theme/mood
- Good variety across years and composers

### With 500+ Songs (Goal):
- **Comprehensive coverage** for full game
- RAG can find songs for any narrative context
- Multiple songs per theme/mood combination
- Historical breadth across entire era

### Minimum Viable:
- **50 carefully selected songs** would be enough for Phase 1
- Choose songs that cover:
  - All major themes (exile, prison, love, hashish, etc.)
  - All moods (mournful, defiant, joyful, etc.)
  - Famous composers and titles
  - Historical significance

---

## 🚀 Immediate Next Steps

1. **Build merge script** (Python):
   ```python
   # Merge Kounadis database + lyrics_rebet.json
   # Create songs_rebetiko.db with unified schema
   # Import 290 songs with lyrics
   ```

2. **Identify top 50-100 priority songs** needing lyrics:
   - Famous titles
   - Important composers
   - Referenced in research

3. **Search stixoi.info** for priority songs:
   - Build simple scraper
   - Match by title/composer
   - Add to database

4. **Process first batch** (50 songs):
   - Run through SONG_PROCESSING.md
   - Validate quality
   - Iterate on prompts

5. **Set up RAG** with processed songs:
   - Embed in ChromaDB
   - Test semantic queries
   - Validate for storylet generation

---

## 📊 Realistic Timeline

- **Week 1:** Merge existing data (290 songs) ✅
- **Week 2:** Find 100-200 more lyrics from external sources
- **Week 3:** Process 300-500 songs with Claude
- **Week 4:** RAG setup and testing

**By end of month:** 300-500 fully processed songs ready for game development

---

## ✨ Success Metrics

- [ ] 290 songs imported and verified
- [ ] 100+ additional lyrics found and matched
- [ ] 300+ songs processed with themes/translations
- [ ] RAG semantic search working ("sad exile song" → relevant results)
- [ ] 10 sample storylets generated using RAG context
