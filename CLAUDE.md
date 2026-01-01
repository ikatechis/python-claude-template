# Ο ΔΡΟΜΟΣ ΤΟΥ ΜΑΓΚΑ (The Road of the Mangas)

A narrative-driven point-and-click game set in the rebetiko underworld of 1922-1940 Piraeus.

## Project Overview

Players experience the life of a refugee arriving from the Asia Minor catastrophe, navigating survival, music, crime, and the margins of society through emergent storytelling powered by interconnected game systems.

### Core Pillars
1. **Historical Authenticity** — Grounded in the Kounadis Archive and primary research
2. **Emergent Narrative** — Systems create stories, not scripted branches
3. **Musical Identity** — Songs as tools, performance as gameplay
4. **Meaningful Choices** — Every decision has weight in a zero-sum economy

## Tech Stack

- **Game Engine:** Godot 4.x (GDScript)
- **Narrative System:** Custom JSON storylets (not Ink)
- **Database:** SQLite (game content + Kounadis archive)
- **Vector Search:** ChromaDB for semantic search and RAG
- **LLM Integration:** Claude API for content generation
- **Image Generation:** Grok/Midjourney for concepts, ComfyUI for production
- **Project Management:** Notion (via MCP server)
- **Python:** 3.12 (pyenv) for tools and scripts
- **Package Manager:** uv
- **Testing:** pytest + coverage
- **Linting:** ruff, mypy

## Language

**The game is in Greek (Ελληνικά).** All storylets, dialogue, and UI are written in Greek. English translation is a Phase 2+ concern.

## RAG Pipeline

Content generation is **conditioned on the Kounadis database** via RAG (Retrieval-Augmented Generation). This ensures historically authentic content. See `docs/RAG_SETUP.md` for details.

## Directory Structure

```
rebetiko-game/
├── .claude/              # Claude Code settings and context
├── docs/                 # Design documents, specs, guides
├── database/             # SQLite databases
├── research/             # Historical materials, dossiers
├── art_pipeline/         # Image generation workflow
│   ├── prompts/          # Documented prompts that work
│   ├── references/       # Historical photos, style guides
│   └── outputs/          # Generated images
├── tools/                # Python scripts for DB, RAG, etc.
├── godot/                # Godot project
│   ├── assets/           # Game assets
│   ├── data/             # JSON storylets, NPCs, songs
│   ├── scenes/           # Godot scenes
│   └── scripts/          # GDScript files
└── notion/               # Notion export/templates
```

## Key Concepts

### Storylets (Not Branching Narrative)
The game uses a **storylet system**, not traditional branching dialogue. Storylets are self-contained narrative units that become available based on game state (location, time, relationships, flags, resources). The engine selects from available storylets using weighted randomness.

### The Four Tracks
Players can pursue four paths (not mutually exclusive):
- **Ο Μουσικός (Musician)** — Learning bouzouki, performing, recording
- **Ο Μάγκας (Underworld)** — Crime, protection, the knife
- **Ο Ναύτης (Sailor)** — The ships, escape, exile
- **Ο Εργάτης (Worker)** — The docks, honest labor, the grind

### Historical Era
- **Act 0 (Prologue):** 1922 — Arrival from Smyrna, refugee camps
- **Act 1:** 1922-1926 — Learning years, establishing in Piraeus
- **Act 2:** 1926-1936 — Golden era of rebetiko, the tekes, recording
- **Act 3:** 1936-1940 — Metaxas dictatorship, censorship, survival

## Working with This Codebase

### Before Making Changes
1. Check `docs/DESIGN.md` for current design decisions
2. Check `docs/STORYLET_FORMAT.md` for JSON schema
3. Check `database/schema.sql` for data structure

### Code Conventions
- GDScript: Use snake_case, document public functions
- JSON: Use lowercase_with_underscores for keys
- Python tools: Include docstrings, use type hints

### Content Guidelines
- Dialogue should feel authentic to 1930s Piraeus slang
- Reference `research/slang_glossary.md` for terminology
- Economic values should follow the research (60 Drs = docker's daily wage)

### Documentation Metadata

All documentation files (`.md`) should include YAML frontmatter with minimal, essential metadata:

```yaml
---
status: draft | review | stable
version: 0.1.0
last_updated: 2025-01-01
---
```

**Metadata Fields:**
- `status`: Document maturity (draft → review → stable)
- `version`: Semantic version for significant changes
- `last_updated`: ISO date format (YYYY-MM-DD)

**Update Protocol:**
- ✅ Update `last_updated` when modifying document content
- ✅ Suggest version bump for significant changes (user decides)
- ✅ Ask user about status transitions (draft → review → stable)
- ❌ **Never** update metadata without content changes
- ❌ **Never** batch-update all docs just for metadata

**Token Efficiency:**
- Only update metadata when you actually modify the document
- Use git for change history, not in-document changelogs
- Let hooks auto-update dates if configured

## Current Phase

**Phase 0: Foundation** — Setting up tools, pipeline, documentation.

## Key Files

- `docs/DESIGN.md` — Game design document
- `docs/STORYLET_FORMAT.md` — Storylet JSON specification
- `docs/GAME_STATE.md` — Game state schema
- `docs/ART_GUIDE.md` — Visual style and prompt engineering
- `docs/RAG_SETUP.md` — RAG pipeline documentation
- `docs/NOTION_SETUP.md` — Project management setup
- `research/IDEAS.md` — Brainstorming and idea pool
- `research/slang_glossary.md` — Period terminology reference
- `database/schema.sql` — Database schema

---

## Python Development Best Practices

### Commands

```bash
uv sync                    # Install deps
uv run python src/main.py  # Run (normal)
DEBUG=1 uv run python ...  # Run (debug)
uv run pytest              # Test
uv run ruff check .        # Lint
uv run mypy src            # Type check
```

### Verification Protocol

**Before suggesting code:**
1. Search docs with ref.tools (`ref_search_documentation` + `ref_read_url`)
2. Verify function signatures and parameters
3. Check pyproject.toml for library versions
4. State confidence: VERIFIED, OBVIOUS, or UNCERTAIN

**Verify:** External library APIs, version-specific features, unfamiliar functions
**Skip:** Basic Python syntax, standard operators, already-verified APIs

### Token Efficiency Best Practices

**Use LSP for zero-token lookups:**
- ✅ `LSP goToDefinition` - Find function definitions without reading files
- ✅ `LSP findReferences` - Find all usages across codebase
- ✅ `LSP hover` - Get type hints and documentation
- ❌ Reading entire files just to find one function

**Batch operations in parallel:**
- ✅ Multiple reads in single message: `Read file1.py`, `Read file2.py`
- ❌ Sequential reads across multiple messages

**Smart search patterns:**
- ✅ Specific Glob patterns: `**/*config*.py`
- ✅ LSP for code navigation (zero file reads)
- ❌ Task tool for simple file searches
- ❌ Speculative reading of 5+ files

**When unsure:**
- ✅ Ask user for file paths
- ❌ Read multiple files hoping to find the right one

### Logging

```python
from logger import get_logger
logger = get_logger(__name__)

logger.debug("Detailed state")     # DEBUG=1 only
logger.info("Normal operation")    # File only
logger.warning("Recoverable error") # Console + file
logger.error("Critical", exc_info=True)  # Console + file
```

**Never suppress errors silently - always log them.**

### Development Workflow

1. Verify APIs with ref.tools
2. Write code
3. Test with `uv run pytest`
4. Commit with conventional format (feat:, fix:, docs:)
