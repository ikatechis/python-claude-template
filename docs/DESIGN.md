---
status: draft
version: 0.1.0
last_updated: 2025-01-01
---

# Game Design Document: Ο ΔΡΟΜΟΣ ΤΟΥ ΜΑΓΚΑ

---

## 1. Vision Statement

### One-Sentence Pitch
Survive as a refugee musician in 1930s Piraeus — smoke hashish in illegal tekedes, learn songs from legends, dodge police, build reputation, and maybe record your voice before history erases you.

### Core Experience
The player experiences the world that created rebetiko music: not as a tourist, but as someone fighting to survive within it. Every choice has weight because resources are scarce, relationships are fragile, and history is indifferent to individual suffering.

### Emotional Goals
- **Authenticity over romanticism** — The poverty is real, the danger is real
- **Beauty within hardship** — Music as transcendence, not escape
- **Moral complexity** — No clear heroes or villains, just survival
- **Historical witness** — The player sees a world that was erased

---

## 2. Core Mechanics

### 2.1 The Storylet System

The game does NOT use traditional branching narrative. Instead:

1. **Storylets** are self-contained narrative units (10-50 lines of content)
2. Each storylet has **conditions** that determine availability
3. The engine **filters** storylets by current game state
4. From available storylets, one is **selected** (weighted random or priority)
5. Player **choices** within storylets modify game state
6. Modified state **unlocks new storylets**

This creates emergent narrative: the same playthrough never happens twice, but the world feels coherent because storylets respond to consistent state.

### 2.2 Game State

The game tracks:

**Temporal:**
- Current time (hour, day phase: proi/apogeyma/vrady/nychta)
- Current date (day, month, year)
- Calendar events (holidays, historical events)

**Spatial:**
- Current location
- Known locations
- Location states (is the tekes raided? is the cafe open?)

**Resources:**
- Money (Drachmas)
- Hunger (0-100, depletes over time)
- Health (0-100, affected by work, violence, disease)
- Psychi (0-100, spirit/morale, affected by music, connection, trauma)
- Heat (0-100, police attention, hidden from player)

**Social:**
- Faction reputation (Manges, Mousikokosmos, Koinotita, Astynomia)
- Individual NPC relationships (0-100 per NPC)
- Known NPCs and their current states

**Progress:**
- Flags (boolean events that have occurred)
- Skills (musical ability, instruments, songs known)
- Inventory (items carried)
- Track affinity (which path the player leans toward)

### 2.3 Time System

Time advances through:
- Traveling between locations (15-60 minutes)
- Completing storylets (variable)
- Working (hours)
- Sleeping/resting (skips to next phase)

Day phases affect:
- Which NPCs are present at locations
- Which storylets are available
- Danger levels (night is more dangerous)
- Work availability (port hires at dawn)

### 2.4 Economy

Based on historical research (1934 baseline):
- Docker's daily wage: 60 Drachmas
- Bread: 7 Drs per oka
- Wine: 10-12 Drs per oka
- Olive oil: 35 Drs per oka
- Rent (shack): 100-150 Drs per month
- Tekes session: 10 Drs
- Musician's good night: 100-200 Drs (but irregular)

The player starts with almost nothing. Survival requires constant resource management.

### 2.5 Reputation System

Four factions with 0-100 reputation:

| Faction | What It Represents | How to Gain | How to Lose |
|---------|-------------------|-------------|-------------|
| Μάγκες | Underworld respect | Honor code, violence, not snitching | Cowardice, betrayal, weakness |
| Μουσικόκοσμος | Musical community | Playing well, learning songs, respecting elders | Selling out, stealing songs, disrespect |
| Κοινότητα | Neighborhood trust | Helping refugees, being reliable, family | Bringing heat, abandoning people |
| Αστυνομία | Police awareness | Avoiding crime, informing (hated) | Any illegal activity |

High Astynomia is BAD (more raids, random stops). The other three unlock storylets and opportunities.

### 2.6 Music System (Phase 1+)

**Songs Known:** Player learns songs through NPC interactions
**Dromoi (Modes):** Each song has a dromos (Rast, Hitzaz, Sabah, etc.)
**Performance:** Player selects song based on crowd mood
**Hartoura:** Tips based on performance quality and crowd match

Music is both a skill tree and an economic system.

---

## 3. Narrative Structure

### 3.1 The Three Acts

**Prologue (Act 0): Ξεριζωμός (1922)**
- Arrival from Smyrna catastrophe
- Refugee camp survival
- First exposure to bouzouki
- Choice of primary path
- Duration: 30 minutes gameplay

**Act 1: Μαθητεία (1922-1926)**
- Learning years in Piraeus
- Building relationships, reputation
- First jobs (whatever path)
- Rising in chosen track
- Duration: 3-5 hours

**Act 2: Η Χρυσή Εποχή (1926-1936)**
- The golden era of rebetiko
- Full access to tekes, recording studios
- Peak conflict and opportunity
- Major relationship arcs resolve
- Duration: 5-8 hours

**Act 3: Λογοκρισία (1936-1940)**
- Metaxas dictatorship
- Music banned/underground
- Survival vs. integrity
- Multiple endings based on accumulated state
- Duration: 2-3 hours

### 3.2 The Four Tracks

Players are not locked into tracks. They accumulate **track affinity** based on choices. By end of Act 1, one track is primary but others remain available.

**Ο Μουσικός (The Musician)**
- Core loop: Learn songs → Perform → Build reputation → Access better venues → Record
- Key NPCs: Old Musician (Panagis), Cafe owner (Efterpi), Rival (Andreas)
- Key locations: The Wall, Cafe-Aman, Recording Studio
- Rewards: Artistic fulfillment, legacy, some money
- Risks: Poverty, irrelevance, selling out

**Ο Μάγκας (The Underworld)**
- Core loop: Small jobs → Earn trust → Bigger jobs → Territory → Power
- Key NPCs: Thomas the Fox, Soula, The Cardplayer
- Key locations: Back Streets, Kafeneio, Vourla
- Rewards: Money, fear, protection
- Risks: Violence, prison, death

**Ο Ναύτης (The Sailor)**
- Core loop: Ship work → Travel → Return changed → Ship again or stay
- Key NPCs: Captain Nikos, Barba Yorgos, Port contacts
- Key locations: Port, Shore, Foreign ports
- Rewards: Escape, perspective, foreign money
- Risks: Permanent exile, rootlessness

**Ο Εργάτης (The Worker)**
- Core loop: Daily labor → Save money → Small stability → Family?
- Key NPCs: Kyrios Stavros, Leonidas, Theia Katerina
- Key locations: Port, Factory, Neighborhood
- Rewards: Stability, dignity, quiet life
- Risks: Body breakdown, obscurity, regret

### 3.3 Endings

Endings are determined by accumulated state, not a final choice. Categories:

- **The Legend:** High musician reputation, survived to 1940, recorded
- **The Boss:** High mangas reputation, controls territory
- **The Exile:** Left Greece, lives abroad
- **The Family Man:** Worker path, has family, quiet life
- **The Prisoner:** Caught, serving time when game ends
- **The Corpse:** Dead (multiple causes possible)
- **The Forgotten:** Alive but irrelevant, the most common outcome

---

## 4. Locations

### 4.1 Hub Locations

**Ο Καταυλισμός (Refugee Camp)** — Act 0 only
- Sub-locations: Your corner, Aid tent, The Wall, Sick tents, Exits
- Function: Tutorial, origin establishment

**Η Γειτονιά (The Neighborhood)** — Acts 1-3
- Home base after leaving camp
- Sub-locations: Your room, Taverna, Street, Market

**Ο Τεκές (The Tekes)** — Acts 1-3
- Illegal hashish den with music
- Core location for music and underworld tracks
- Sub-locations: Smoking circle, Musician's corner, Back room

### 4.2 Path-Specific Locations

**Musician Path:**
- Το Καφέ-Αμάν (Cafe) — Legal music venue
- Το Στούντιο (Recording Studio) — Columbia/Odeon
- Η Μάντρα του Μπάτη (Batis's Mandra) — Historical venue

**Underworld Path:**
- Τα Σοκάκια (Back Streets) — Crime hub
- Η Βούρλα (The Brothel District) — Dangerous, profitable
- Το Κρησφύγετο (The Hideout) — Criminal base

**Sailor Path:**
- Το Λιμάνι (The Port) — Work, ships
- Η Ακτή (The Shore) — Reflection, fishing
- Foreign ports — Alexandria, Constantinople, Marseille

**Worker Path:**
- Η Αποθήκη (The Warehouse) — Indoor work
- Το Εργοστάσιο (The Factory) — Regular labor
- Η Λαϊκή (The Market) — Commerce

---

## 5. Key NPCs

### 5.1 Mentor Figures

| Name | Track | Role | Fate |
|------|-------|------|------|
| Παναγής | Music | Old Smyrna musician | Dies in camp phase |
| Κυρία Ευτέρπη | Music | Cafe owner, gatekeeper | Survives, judges you |
| Θωμάς ο Αλεπού | Crime | Introduces underworld | Variable |
| Κύριος Σταύρος | Work/Sea | Port foreman | Constant |
| Καπετάν Νίκος | Sea | Ship captain | Variable |

### 5.2 Peer Figures

| Name | Track | Role | Relationship |
|------|-------|------|--------------|
| Δημήτρης | Any | First friend from camp | Variable, can die |
| Σούλα | Crime | Rival/ally | Complex |
| Ανδρέας | Music | Rival musician | Antagonistic |
| Λεωνίδας | Work | Protector/friend | Loyal |

### 5.3 Historical Inspirations

NPCs are inspired by real figures but fictionalized:
- The Patriarch (Markos Vamvakaris archetype)
- The Doomed Youth (Anestis Delias archetype)
- The Queen (Roza Eskenazi archetype)
- The Gatekeeper (Minos Matsas archetype)

---

## 6. Visual Style

### 6.1 Art Direction

- **Style:** Stylized realism, muted palette, strong shadows
- **Inspiration:** 1930s Greek photography, film noir, Toulouse-Lautrec
- **Palette:** Browns, ambers, deep blues, smoke greys
- **Lighting:** Oil lamps, harsh sunlight, smoke haze

### 6.2 Character Art

- Portraits with 3-5 expressions per major NPC
- Consistent proportions and style across all characters
- Clothing accurate to era and class
- Instruments rendered with historical accuracy

### 6.3 Backgrounds

- Each location needs multiple variants (time of day, weather)
- Hotspots clearly indicated but not UI-breaking
- Atmospheric details: smoke, light shafts, movement

---

## 7. Audio

### 7.1 Music

- **Source material:** Kounadis archive recordings
- **Original compositions:** For performances, adaptations of period songs
- **Dromoi representation:** Authentic Greek modes

### 7.2 Ambient

- Location-specific ambience (port, tekes, street)
- Time-of-day variations
- Weather effects

### 7.3 Voice

- **Approach:** Key lines voiced, most text-only
- **Language:** English prose with authentic Greek terms and exclamations (see LANGUAGE_GUIDE.md)
- **Dialect:** Era-appropriate Piraeus slang integrated naturally

---

## 8. Scope & Milestones

### Phase 0: Foundation (Current)
- [x] Core design document
- [ ] Storylet format specification
- [ ] Database schema
- [ ] Art pipeline setup
- [ ] Godot project initialization

### Phase 1: Proof of Concept
- [ ] One location (Tekes) fully functional
- [ ] 5 NPCs with relationship tracking
- [ ] 40 storylets
- [ ] 3 in-game days playable
- [ ] Core systems working

### Phase 2: Vertical Slice
- [ ] 4 locations
- [ ] 15 NPCs
- [ ] 150+ storylets
- [ ] Full month playable
- [ ] Music system functional
- [ ] Demo-ready build

### Phase 3: Full Production
- [ ] All locations
- [ ] All NPCs
- [ ] 400+ storylets
- [ ] Full game arc
- [ ] Polish and release

---

## 9. Open Questions

- [ ] Protagonist: Fixed or player-created?
- [x] Language: Greek-first or English-first? **→ English with Greek elements (see LANGUAGE_GUIDE.md)**
- [ ] Scope of PoC: 3 days or 7 days?
- [ ] Music minigame: QTE, rhythm, or narrative only?
- [ ] Violence: How explicit?
- [ ] Addiction mechanics: How punishing?

---

## Appendix: Reference Materials

- `/research/slang_glossary.md` — Period slang and terminology
- `/research/IDEAS.md` — Brainstorming and idea pool
- `/docs/STORYLET_FORMAT.md` — Storylet JSON specification
- `/docs/GAME_STATE.md` — Game state schema
- `/docs/LANGUAGE_GUIDE.md` — Language and localization guidelines
- `/docs/RAG_SETUP.md` — RAG pipeline setup
- `/docs/ART_GUIDE.md` — Visual style guide
- `/docs/NOTION_SETUP.md` — Project management setup
- `/database/schema.sql` — Database schema
