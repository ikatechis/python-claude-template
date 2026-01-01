---
status: draft
version: 0.1.0
last_updated: 2025-01-01
---

# Development Roadmap

**Goal:** Build Ο Δρόμος του Μάγκα in achievable phases, from proof of concept to full game.

---

## Phase 0: Foundation (Current) — 2-3 weeks

**Goal:** Set up all tools, pipelines, and documentation needed for production.

### Infrastructure
- [x] Project structure created
- [x] Core documentation written (DESIGN, STORYLET_FORMAT, GAME_STATE, LANGUAGE_GUIDE, ART_GUIDE)
- [ ] Python environment with uv
- [ ] SQLite schema designed and created
- [ ] ChromaDB initialized for RAG
- [ ] Notion workspace set up (or alternative project management)

### Data & Content Pipeline
- [ ] Kounadis database ingested (if available)
- [ ] Research materials embedded in ChromaDB
- [ ] RAG query tools working
- [ ] Slang glossary compiled (30-50 essential terms)
- [ ] First 20 glossary entries written

### Godot Setup
- [ ] Godot 4.x project initialized
- [ ] Folder structure set up (scenes, scripts, assets, data)
- [ ] Git LFS configured for assets
- [ ] Basic project settings (resolution, rendering, etc.)

### Art Pipeline
- [ ] Art style references collected
- [ ] Color palettes defined (master + location-specific)
- [ ] First test background generated (tekes)
- [ ] ComfyUI workflow documented (if using)
- [ ] Naming conventions established

**Deliverable:** All tools working, first test art generated, ready to build.

---

## Phase 1: Proof of Concept — 4-6 weeks

**Goal:** One playable location with core systems functional. Prove the game loop works.

### Core Systems (GDScript)
- [ ] GameState class fully implemented
  - [ ] Temporal (time, date, phase)
  - [ ] Spatial (location, known_locations)
  - [ ] Resources (money, hunger, health, psychi, heat)
  - [ ] Social (reputation, relationships)
  - [ ] Progress (flags, storylets_seen)
  - [ ] Skills, inventory, track_affinity
- [ ] Time system
  - [ ] Advance time (minutes → hours → days)
  - [ ] Time phase calculation (proi/apogeyma/vrady/nychta)
  - [ ] Daily resource depletion (hunger)
- [ ] Storylet engine
  - [ ] Load storylets from JSON files
  - [ ] Filter by conditions (location, time, flags, resources, etc.)
  - [ ] Weighted selection (by priority)
  - [ ] Display content (text rendering)
  - [ ] Handle player choices
  - [ ] Apply effects to GameState
  - [ ] Cooldown tracking
- [ ] Save/Load system
  - [ ] Serialize GameState to JSON
  - [ ] Save to file (multiple slots)
  - [ ] Load from file

### UI (Godot)
- [ ] Basic game window layout
- [ ] Location view (background image display)
- [ ] Narrative text box with typewriter effect
- [ ] Choice buttons (dynamic, based on storylet)
- [ ] Status panel (basic stats: money, hunger, health, psychi)
- [ ] Time/date display
- [ ] Main menu (New Game, Load, Quit)
- [ ] Save/Load menu

### Content — Camp Location (Act 0)
- [ ] Camp background art (wide shot, at least 2 variants)
- [ ] 5 NPCs defined with full data:
  - [ ] Dimitris (first friend)
  - [ ] Panagis (old musician, dies in camp)
  - [ ] Aid Worker (neutral)
  - [ ] Sick Woman (flavor NPC)
  - [ ] Camp Guard (authority figure)
- [ ] 10-15 storylets written:
  - [ ] Tutorial/intro (arriving at camp)
  - [ ] Meeting Dimitris (friendship start)
  - [ ] Meeting Panagis (music intro)
  - [ ] Hunger/survival situations (3-4)
  - [ ] Music learning scene (Panagis teaches)
  - [ ] Panagis death scene
  - [ ] Decision to leave camp
  - [ ] Ambient/filler storylets (2-3)

### Content — Tekes Location (First Real Location)
- [ ] Tekes background art (night, smoky, intimate)
- [ ] 3 additional NPCs:
  - [ ] Kyra Sofia (tekes owner)
  - [ ] Markos (bouzouki player)
  - [ ] Regular Patron (ambient NPC)
- [ ] 10-15 storylets written:
  - [ ] First entry to tekes (discovery)
  - [ ] Music performances (2-3)
  - [ ] Smoking hashish (choice, consequence)
  - [ ] Learning from Markos
  - [ ] Relationship building with Sofia
  - [ ] Ambient/atmosphere storylets (3-4)
  - [ ] Small conflict/choice moment

### Glossary System
- [ ] Glossary data structure in GameState
- [ ] Glossary UI panel (browsable list, categories)
- [ ] Auto-add terms on first encounter
- [ ] Inline term highlighting (optional hover/click for definition)
- [ ] 30 glossary entries written (cover common terms in PoC)

### Testing & Polish
- [ ] Playtest: Camp → Tekes over 3 in-game days
- [ ] Check all systems work (time, resources, choices, flags)
- [ ] Verify storylets trigger correctly based on conditions
- [ ] Balance resource economy (can you survive?)
- [ ] Fix critical bugs

**Deliverable:** A playable 30-minute experience showing core game loop.

---

## Phase 2: Vertical Slice — 8-12 weeks

**Goal:** Expand to 4 locations, 15 NPCs, 150+ storylets. Demo-ready build covering Act 1.

### New Locations
- [ ] Port (day/dawn/night variants)
  - [ ] Background art
  - [ ] 15-20 storylets (work, sailing, characters)
- [ ] Neighborhood Streets (day/night)
  - [ ] Background art
  - [ ] 15-20 storylets (housing, market, community)
- [ ] Koutouki (tavern)
  - [ ] Background art
  - [ ] 10-15 storylets (drinking, music, gossip)

### New Systems
- [ ] Music system (basic implementation)
  - [ ] Songs database (10 songs defined)
  - [ ] Learn song mechanics
  - [ ] Performance mechanic (simple: choose song → check skill → outcome)
  - [ ] Hartoura (tips) based on performance
- [ ] Relationship depth
  - [ ] NPC schedules (who's where, when)
  - [ ] Deeper relationship storylets (trust thresholds)
  - [ ] Betrayal/loyalty mechanics
- [ ] Crime system (if pursuing mangas path)
  - [ ] Small jobs (theft, delivery)
  - [ ] Heat mechanics (police attention)
  - [ ] Arrest/consequences

### NPCs (10 additional, 15 total)
- [ ] Track-specific mentors and rivals
- [ ] At least 5 with portraits
- [ ] Full backstories and schedules

### Content Scale
- [ ] 150+ total storylets across all locations
- [ ] Multiple storylets per NPC (relationship arcs)
- [ ] Path-specific content (musician vs. crime vs. work)
- [ ] Historical events (flavor, optional)

### Art Assets
- [ ] 4 locations with variants (12-16 backgrounds total)
- [ ] 5-8 character portraits (3 expressions each)
- [ ] Basic UI graphics (menus, buttons, icons)

### Music & Audio (Optional for Vertical Slice)
- [ ] Ambient soundscapes per location
- [ ] 2-3 rebetiko tracks (from Kounadis or original)
- [ ] Basic SFX (footsteps, door, coins)

### Polish
- [ ] Improved UI (better fonts, layout, polish)
- [ ] Transitions between locations
- [ ] Save slot management
- [ ] Settings menu (volume, text speed)
- [ ] Playtest with external testers
- [ ] Demo trailer (if needed for pitch/funding)

**Deliverable:** A 2-3 hour demo covering Act 1, ready to show publicly.

---

## Phase 3: Full Production — 6-12 months

**Goal:** Complete game with all three acts, all locations, all systems.

### Scope
- [ ] All locations (15-20 total, including Athens, prison, rooftops)
- [ ] All NPCs (30-40, with full arcs)
- [ ] 400+ storylets covering entire game
- [ ] All four tracks fully fleshed out
- [ ] Music system expanded (dromos mechanics, recording studio)
- [ ] Full endings (7+ based on accumulated state)

### New Act Content
- [ ] Act 2 (1926-1936): Golden era, peak content
- [ ] Act 3 (1936-1940): Metaxas dictatorship, censorship, survival

### Systems Completion
- [ ] Advanced music mechanics (dromos, improvisation)
- [ ] Addiction system (if keeping it)
- [ ] Long-term consequences (prison time, exile)
- [ ] Historical events integrated
- [ ] Recording studio mechanics

### Art Completion
- [ ] All locations with full variants (50+ backgrounds)
- [ ] All NPC portraits (30+ characters, multiple expressions)
- [ ] Cutscene art (if using)
- [ ] UI polish and cohesion

### Audio Completion
- [ ] Full ambient soundscapes for all locations
- [ ] 10-20 rebetiko tracks
- [ ] Complete SFX library
- [ ] Voice acting (optional, Phase 3b)

### Writing & Localization
- [ ] All storylets written and tested
- [ ] Full glossary (100+ terms)
- [ ] Proofreading and editing pass
- [ ] Greek localization (director's cut, optional)

### Testing & Release Prep
- [ ] Extensive playtesting (all paths, all endings)
- [ ] Balance pass (economy, difficulty, pacing)
- [ ] Bug fixing and polish
- [ ] Achievements/Steam integration (if PC)
- [ ] Trailer, screenshots, press kit
- [ ] Store page setup (Steam, itch.io, etc.)

**Deliverable:** Complete game, ready for release.

---

## Immediate Next Steps (This Week)

If starting now, here's the priority order:

1. **Database schema** — Create `database/schema.sql` with all tables
2. **Initialize Godot project** — Basic folder structure, test scene
3. **GameState class** — Implement in GDScript, test save/load
4. **First storylet** — Write one complete storylet, manually load it, display it
5. **First background** — Generate tekes art, import to Godot
6. **Time system** — Get time advancing, days passing

**Goal for Week 1:** See a storylet display on screen in Godot, with a choice that advances time.

---

## Dependencies & Risks

### Critical Path
- Godot learning curve (if new to it)
- Art generation consistency (pixel art pipeline)
- Storylet writing velocity (need 400+ eventually)
- Historical research availability (Kounadis access?)

### Mitigation
- Use simpler art style if pixel art is too slow
- Build content generation tools (RAG prompts that work)
- Consider collaborators for writing or art
- Scope ruthlessly: minimum viable content per phase

---

## Success Metrics Per Phase

**Phase 0:** All tools installed and working, first test art generated.

**Phase 1:** 30-minute playable loop that feels good.

**Phase 2:** 2-3 hour demo that external playtesters want to finish.

**Phase 3:** Complete game that honors the subject matter and is worth playing.

---

**Remember:** This is ambitious. Stay disciplined about scope. Cut features before cutting quality. The core experience (storylets, choices, atmosphere, language) is what matters. Everything else is secondary.
