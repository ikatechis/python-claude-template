---
status: stable
version: 1.0.0
last_updated: 2026-01-01
---

# Ο Δρόμος του Μάγκα
### A Rebetiko Story Game

Narrative-driven point-and-click game set in 1922-1940 Piraeus. Experience the world that created rebetiko music — not as a tourist, but as someone fighting to survive within it.

**Language:** English with Greek elements (see `docs/LANGUAGE_GUIDE.md`)
**Status:** Phase 0 - Foundation & Infrastructure

---

## Overview

You are a refugee. You arrived in Piraeus from Smyrna in 1922, after the catastrophe. You have nothing — no family, no money, no future. Just survival.

But there is music. In the hash dens and basement taverns, in the smoke and the cheap wine, men play the bouzouki and sing of pain, of longing, of defiance. This is rebetiko. This is where you might find something worth living for.

### Core Pillars

1. **Historical Authenticity** — Grounded in the Kounadis Archive and primary research
2. **Emergent Narrative** — Systems create stories, not scripted branches
3. **Musical Identity** — Songs as tools, performance as gameplay
4. **Meaningful Choices** — Every decision has weight in a zero-sum economy

---

## Project Structure

```
rebetiko-game/
├── CLAUDE.md                 # Claude Code context file
├── README.md                 # This file
├── .gitignore
├── .claude/                  # Claude Code settings
│   └── settings.json
├── docs/                     # Design documentation
│   ├── DESIGN.md             # Game Design Document
│   ├── STORYLET_FORMAT.md    # Storylet JSON specification
│   ├── GAME_STATE.md         # Game state schema
│   ├── ART_GUIDE.md          # Visual style & prompts
│   └── RAG_SETUP.md          # RAG pipeline guide
├── database/                 # SQLite databases
│   └── schema.sql            # Database schema
├── research/                 # Historical materials
│   ├── IDEAS.md              # Brainstorming pool
│   └── slang_glossary.md     # Period terminology
├── art_pipeline/             # Image generation
│   ├── prompts/              # Working prompts
│   ├── references/           # Historical photos
│   └── outputs/              # Generated images
├── tools/                    # Python utilities (to be created)
└── godot/                    # Godot project (to be created)
```

---

## Tech Stack

| Component | Tool | Notes |
|-----------|------|-------|
| Game Engine | Godot 4.x | GDScript |
| Narrative | Custom JSON Storylets | Not Ink — systemic, not branching |
| Database | SQLite | Game content + Kounadis archive |
| Vector Search | ChromaDB | For RAG semantic search |
| LLM | Claude API | Content generation |
| Image Gen | Grok → ComfyUI | Concepts → Production |
| Project Mgmt | GitHub Projects & Issues | Via GitHub MCP |

---

## Getting Started

### Prerequisites

- **Python 3.12** (managed via pyenv)
- **uv** (fast Python package manager)
- **Node.js** (for MCP servers: GitHub, SQLite)

### Quick Start

```bash
# 1. Clone the repo
git clone <your-repo>
cd rebetiko-game

# 2. Install Python dependencies
uv sync

# 3. Review database analysis
cat database/analysis/ANALYSIS_SUMMARY.md
```

### Current Status

✅ **Completed:**
- Python environment (Python 3.12 + uv)
- Comprehensive database analysis (6,960 items, 1,689 rebetiko songs)
- MCP configuration (GitHub + SQLite servers)
- Documentation structure

⏳ **Next Steps:**
1. Set up GitHub Projects for task tracking
2. Begin lyrics matching and RAG pipeline setup
3. Design initial storylet system
4. Create art pipeline for character concepts

📊 **See `PROGRESS_SUMMARY.md` for detailed status**

### Key Documentation

**Start here:**
1. **`PROGRESS_SUMMARY.md`** — Current status and next steps
2. **`CLAUDE.md`** — Project overview and Claude Code context
3. **`docs/DESIGN.md`** — Full game design document

**Database Analysis:**
- `database/analysis/ANALYSIS_SUMMARY.md` — Comprehensive findings
- `database/analysis/rebetiko_era_songs.json` — 1,689 songs for processing

**Guides:**
- `docs/LANGUAGE_GUIDE.md` — Language approach (English with Greek)
- `docs/RAG_SETUP.md` — RAG pipeline documentation
- `docs/STORYLET_FORMAT.md` — How storylets work

---

## Development Phases

| Phase | Focus | Duration | Status |
|-------|-------|----------|--------|
| **0: Foundation** | Tools, docs, pipeline | 2-3 weeks | **Current** |
| 1: PoC | Tekes only, 5 NPCs, 3 days | 2-3 months | Planned |
| 2: Vertical Slice | 4 locations, 15 NPCs, demo | 3-4 months | Planned |
| 3: Production | Full game | 8-12 months | Planned |

---

## The Four Tracks

Players can pursue four paths (not mutually exclusive):

- **Ο Μουσικός** — The Musician. Learn bouzouki, perform, record.
- **Ο Μάγκας** — The Underworld. Crime, protection, the knife.
- **Ο Ναύτης** — The Sailor. Ships, escape, exile.
- **Ο Εργάτης** — The Worker. The docks, honest labor.

The player isn't locked into a path — they accumulate *affinity* based on choices.

---

## Historical Era

- **1922:** Arrival from Smyrna, refugee camps
- **1922-1926:** Learning years, establishing in Piraeus
- **1926-1936:** Golden era of rebetiko
- **1936-1940:** Metaxas dictatorship, censorship

---

## License

TBD

---

## Acknowledgments

- Kounadis Archive
- The rebetes who lived this history
- Η μνήμη τους να είναι αιώνια
