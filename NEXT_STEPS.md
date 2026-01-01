---
status: active
version: 1.0.0
last_updated: 2026-01-01
---

# Next Steps - Rebetiko Game Project

## Current Status Summary

### ✅ Completed (Phase 0 - Foundation)

**Database Infrastructure:**
- ✅ Alembic migrations set up (6 migrations)
- ✅ Metadata extracted into columns (lyrics, dates, rhythms, places)
- ✅ FTS5 full-text search on lyrics
- ✅ Normalized rhythm types (1,005 items) and recording places (3,092 items)

**Lyrics Processing:**
- ✅ Fuzzy matched 649 lyrics from lyrics_rebet.json
- ✅ Imported 135 certain matches (≥0.85 confidence)
- ✅ Database now has 672 songs with lyrics (was 537)
- ✅ Created review spreadsheet for 89 uncertain matches

**Genre Mapping:**
- 🔄 **IN PROGRESS** - Genre scraper running in background
- ✅ Fixed scraping approach (fmid=f instead of fmid=p)
- ✅ Documented 17 genre collections

**Documentation:**
- ✅ All .md files standardized with YAML frontmatter
- ✅ Comprehensive guides created (migrations, genre investigation, etc.)

---

## 🎯 Immediate Next Steps

### 1. Complete Lyrics Review (PRIORITY)
**File:** `database/analysis/uncertain_lyrics_REVIEW.csv`
**Action:** Manual review of 89 uncertain matches
**Columns to fill:**
- `decision`: YES/NO/SKIP
- `notes`: Any comments

**After review:**
```bash
# Import accepted matches
uv run python tools/import_lyrics.py --uncertain-only
```

### 2. Verify Genre Scraping Results
**When scraper completes:**
```bash
# Check results
cat database/analysis/genre_mappings.json | python3 -c "
import sys, json
data = json.load(sys.stdin)
for genre, info in sorted(data.items(), key=lambda x: x[1]['count'], reverse=True):
    print(f'{genre:25s} {info[\"count\"]:5d} items - {info[\"name_el\"]}')"
```

**Expected:**
- Rebetiko: ~719 items (website shows 657-719 depending on search)
- Other genres: Various counts

**If counts look wrong:** Re-investigate search parameters

### 3. Create Genre Migration
**Once genre mappings are verified:**

```bash
# Create migration
alembic revision -m "add_genre_tables"
```

**Migration should:**
1. Create `genres` table (id, name_en, name_el, collection_id)
2. Create `item_genres` table (item_id, genre_id) - many-to-many
3. Populate from genre_mappings.json

### 4. Fetch Remaining Lyrics
**Target:** ~2,000 rebetiko songs without lyrics

**Approach:**
1. Use genre mapping to identify true rebetiko songs
2. Google search: "{title} {artist} στίχοι"
3. Parse Greek lyrics websites
4. Import with fuzzy matching

**Script to create:**
```bash
tools/fetch_lyrics_for_genre.py --genre rebetiko --limit 100
```

---

## 📋 Phase 1 Planning - Proof of Concept

### Core Requirements (from ROADMAP.md)
- **Scope:** Tekes only (single location)
- **Duration:** 3 in-game days
- **NPCs:** 5 characters
- **Mechanics:** Minimal viable systems

### Systems to Implement

#### 1. Storylet Engine (Godot)
**Priority: HIGH**
**Files to create:**
- `godot/scripts/storylet_engine.gd`
- `godot/data/storylets/` (JSON files)

**Features:**
- Load storylets from JSON
- Check requirements (stats, flags, location, time)
- Present available storylets
- Execute outcomes

**First storylet to implement:**
- `tekes_arrival.json` - Player enters tekes for first time

#### 2. Game State System
**Priority: HIGH**
**Files:**
- `godot/scripts/game_state.gd`
- Save/load functionality

**State to track:**
- Stats: psychi, hunger, money, reputation
- Location, time of day
- Flags/variables
- Relationship values

#### 3. Song Database Integration
**Priority: MEDIUM**
**Files:**
- `godot/scripts/song_database.gd`
- Copy SQLite DB to `godot/assets/data/`

**Features:**
- Query songs by genre, era, mood
- Get song metadata for storylets
- Track "known songs" by player

#### 4. Simple UI
**Priority: MEDIUM**
**Scenes:**
- `godot/scenes/ui/storylet_choice.tscn`
- `godot/scenes/ui/stat_display.tscn`

**Style:** Text-based, minimal graphics (Phase 1)

---

## 🔄 Recurring Tasks

### Weekly
- [ ] Review lyrics matching progress
- [ ] Test storylet engine with new content
- [ ] Document new systems in `/docs`

### As Needed
- [ ] Add database migrations when schema changes
- [ ] Update ROADMAP.md with progress
- [ ] Commit regularly with conventional commits

---

## 🚀 Long-Term Goals (Phase 2+)

### RAG Pipeline Setup
**When:** After core storylet engine works
**Purpose:** Generate contextually appropriate storylets
**Tools:** ChromaDB + Claude API

### Art Pipeline
**When:** After Phase 1 PoC
**Purpose:** Character portraits, location art
**Tools:** Grok/Midjourney → ComfyUI

### Full Game Scope
**Timeline:** 8-12 months (Phase 3)
**Features:** 4 locations, 15+ NPCs, 30+ days, all 4 tracks

---

## 📊 Success Metrics

### Phase 0 (Foundation) - ✅ COMPLETE
- [x] Database normalized and queryable
- [x] 500+ songs with lyrics
- [x] Genre mappings complete
- [x] Documentation standardized

### Phase 1 (PoC) - Target: 2-3 months
- [ ] Storylet engine functional
- [ ] 10+ storylets implemented
- [ ] 5 NPCs with dialogue
- [ ] 3 playable days
- [ ] Save/load works

### Phase 2 (Vertical Slice) - Target: 3-4 months
- [ ] 4 locations playable
- [ ] 50+ storylets
- [ ] 15+ NPCs
- [ ] Basic music integration
- [ ] Demo-ready (15-20 mins gameplay)

---

## ⚠️ Blockers / Questions

1. **Genre scraping count discrepancy:**
   - Website shows 657 rebetiko entries
   - Our scraper finding 3000+ (still running)
   - Need to verify if filtering is correct

2. **Lyrics sources:**
   - Need reliable Greek lyrics websites
   - May need to handle multiple sources
   - Copyright considerations

3. **Godot 4.x learning curve:**
   - GDScript 2.0 syntax
   - New scene structure
   - Resource management

---

## 📁 Key Files Reference

**Database:**
- `database/vmrebetiko_all_genres.db` - Main database (93MB)
- `database/lyrics_rebet.json` - 649 songs with lyrics (719KB)
- `alembic/versions/` - Database migrations

**Analysis:**
- `database/analysis/genre_mappings.json` - Genre-to-item mappings
- `database/analysis/uncertain_lyrics_REVIEW.csv` - **NEEDS MANUAL REVIEW**

**Documentation:**
- `docs/DESIGN.md` - Full game design
- `docs/ROADMAP.md` - Development phases
- `docs/STORYLET_FORMAT.md` - JSON specification
- `docs/DATABASE_MIGRATIONS.md` - Alembic guide

**Tools:**
- `tools/scrape_genre_mappings_correct.py` - Genre scraper (RUNNING)
- `tools/import_lyrics.py` - Import matched lyrics
- `tools/match_lyrics.py` - Fuzzy match lyrics to DB
- `tools/query_db.py` - Quick DB queries

---

**Last Updated:** 2026-01-01
**Current Phase:** 0 → 1 Transition
**Next Milestone:** Phase 1 PoC (Tekes only)
