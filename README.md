# Ο Δρόμος του Μάγκα
### A Rebetiko Story Game

Narrative-driven point-and-click game set in 1922-1940 Piraeus. Experience the world that created rebetiko music — not as a tourist, but as someone fighting to survive within it.

**Language:** Ελληνικά (Greek)

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
│   ├── RAG_SETUP.md          # RAG pipeline guide
│   └── NOTION_SETUP.md       # Project management setup
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
| Project Mgmt | Notion | Via MCP server |

---

## Getting Started

### Prerequisites

- Python 3.10+
- Godot 4.x
- Node.js (for Notion MCP)
- Your Kounadis database

### Setup

```bash
# 1. Clone the repo
git clone <your-repo>
cd rebetiko-game

# 2. Create Python environment
python -m venv venv
source venv/bin/activate

# 3. Install dependencies
pip install chromadb anthropic sqlite-utils pandas sentence-transformers

# 4. Initialize ChromaDB (see docs/RAG_SETUP.md)
# 5. Embed your Kounadis data
# 6. Set up Notion MCP (see docs/NOTION_SETUP.md)
```

### Key Documentation

Start here:
1. `CLAUDE.md` — Project overview and context
2. `docs/DESIGN.md` — Full game design document
3. `docs/STORYLET_FORMAT.md` — How storylets work
4. `docs/RAG_SETUP.md` — Setting up the RAG pipeline

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
