---
status: draft
version: 0.1.0
last_updated: 2025-01-01
---

# RAG Pipeline Setup Guide

**Purpose:** Enable Claude to generate historically authentic content by conditioning on the Kounadis database, research materials, and reference documents.

---

## Why RAG is Essential

Without RAG, Claude knows general information about rebetiko. With RAG, Claude can:

1. **Find thematically related songs** — "Give me a song about longing for Smyrna" finds actual songs with that theme, even if "Smyrna" isn't in the title
2. **Pull specific historical details** — Economic data, slang usage, event dates
3. **Generate authentic dialogue** — Based on actual speech patterns from research
4. **Create consistent storylets** — Grounded in the established world

**Example without RAG:**
> Claude invents a song called "The Tears of Piraeus" that sounds generically Greek

**Example with RAG:**
> Claude finds "Μινόρε της Αυγής" in Kounadis, sees its themes (dawn, loneliness, port life), and references it naturally or creates something that fits alongside it

---

## Architecture Overview

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│  Source Data    │────▶│  Embedding       │────▶│   ChromaDB      │
│  - Kounadis DB  │     │  Generation      │     │   (Vectors)     │
│  - Research     │     │  (Claude/OpenAI) │     │                 │
│  - Dossiers     │     └──────────────────┘     └────────┬────────┘
│  - Slang        │                                       │
└─────────────────┘                                       │
                                                          ▼
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│  Generation     │◀────│  Retrieved       │◀────│  Query          │
│  Request        │     │  Context         │     │  "sad exile     │
│  (Claude)       │     │  (Top K docs)    │     │   song"         │
└─────────────────┘     └──────────────────┘     └─────────────────┘
```

---

## Setup Instructions

### 1. Install Dependencies

```bash
# Create virtual environment
cd rebetiko-game
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install packages
pip install chromadb
pip install anthropic  # For Claude API
pip install sqlite-utils  # For easier SQLite handling
pip install pandas  # For data manipulation
```

### 2. Initialize ChromaDB

```python
# tools/init_chromadb.py
import chromadb
from chromadb.config import Settings

# Create persistent ChromaDB instance
client = chromadb.PersistentClient(path="./database/chromadb")

# Create collections for different content types
collections = {
    "songs": client.get_or_create_collection(
        name="kounadis_songs",
        metadata={"description": "Songs from Kounadis archive"}
    ),
    "research": client.get_or_create_collection(
        name="research_entries",
        metadata={"description": "Historical research and dossiers"}
    ),
    "storylets": client.get_or_create_collection(
        name="storylets",
        metadata={"description": "Game storylets for reference"}
    ),
    "slang": client.get_or_create_collection(
        name="slang_glossary",
        metadata={"description": "Period slang and terminology"}
    )
}

print("ChromaDB initialized with collections:", list(collections.keys()))
```

### 3. Embed Kounadis Data

```python
# tools/embed_kounadis.py
import chromadb
import sqlite3
from anthropic import Anthropic

# Initialize
client = chromadb.PersistentClient(path="./database/chromadb")
collection = client.get_collection("kounadis_songs")
anthropic = Anthropic()

# Connect to Kounadis SQLite
conn = sqlite3.connect("./database/kounadis.db")
cursor = conn.cursor()

# Fetch songs (adjust query to your actual schema)
cursor.execute("""
    SELECT id, title, artist, lyrics, themes, notes
    FROM songs
    WHERE lyrics IS NOT NULL
""")

songs = cursor.fetchall()

# Process in batches
batch_size = 50
for i in range(0, len(songs), batch_size):
    batch = songs[i:i+batch_size]

    documents = []
    metadatas = []
    ids = []

    for song in batch:
        song_id, title, artist, lyrics, themes, notes = song

        # Create rich document for embedding
        doc_text = f"""
        Τίτλος: {title}
        Καλλιτέχνης: {artist}
        Στίχοι: {lyrics[:500] if lyrics else 'N/A'}
        Θέματα: {themes or 'N/A'}
        Σημειώσεις: {notes or 'N/A'}
        """

        documents.append(doc_text)
        metadatas.append({
            "title": title,
            "artist": artist or "",
            "themes": themes or "",
            "source": "kounadis"
        })
        ids.append(f"song_{song_id}")

    # Add to ChromaDB (it handles embedding automatically with default model)
    collection.add(
        documents=documents,
        metadatas=metadatas,
        ids=ids
    )

    print(f"Embedded {i + len(batch)} / {len(songs)} songs")

conn.close()
print("Kounadis embedding complete!")
```

### 4. Embed Research Materials

```python
# tools/embed_research.py
import chromadb
import os
from pathlib import Path

client = chromadb.PersistentClient(path="./database/chromadb")
collection = client.get_collection("research_entries")

# Process markdown files in research folder
research_dir = Path("./research")

for md_file in research_dir.glob("*.md"):
    if md_file.name == "IDEAS.md":
        continue  # Skip the ideas dump

    content = md_file.read_text(encoding="utf-8")

    # Split into chunks (by section or by size)
    # Simple approach: split by ## headers
    sections = content.split("\n## ")

    for i, section in enumerate(sections):
        if len(section.strip()) < 100:
            continue

        section_title = section.split("\n")[0] if section else f"Section {i}"

        collection.add(
            documents=[section],
            metadatas=[{
                "source_file": md_file.name,
                "section": section_title,
                "type": "research"
            }],
            ids=[f"{md_file.stem}_{i}"]
        )

print("Research embedding complete!")
```

### 5. Query Function

```python
# tools/rag_query.py
import chromadb
from anthropic import Anthropic

client = chromadb.PersistentClient(path="./database/chromadb")
anthropic = Anthropic()

def query_context(query: str, collections: list = None, n_results: int = 5) -> str:
    """
    Query ChromaDB and return formatted context for Claude.

    Args:
        query: Natural language query (can be in Greek)
        collections: List of collection names to search, or None for all
        n_results: Number of results per collection

    Returns:
        Formatted context string to include in Claude prompt
    """
    if collections is None:
        collections = ["kounadis_songs", "research_entries", "slang_glossary"]

    all_results = []

    for coll_name in collections:
        try:
            coll = client.get_collection(coll_name)
            results = coll.query(
                query_texts=[query],
                n_results=n_results
            )

            for doc, metadata in zip(results['documents'][0], results['metadatas'][0]):
                all_results.append({
                    "collection": coll_name,
                    "content": doc,
                    "metadata": metadata
                })
        except Exception as e:
            print(f"Error querying {coll_name}: {e}")

    # Format for Claude
    context = "<retrieved_context>\n"
    for r in all_results:
        context += f"\n<document source=\"{r['collection']}\">\n"
        context += f"Metadata: {r['metadata']}\n"
        context += f"Content: {r['content'][:1000]}\n"
        context += "</document>\n"
    context += "</retrieved_context>"

    return context


def generate_with_context(prompt: str, query: str = None) -> str:
    """
    Generate content with RAG context.

    Args:
        prompt: The generation prompt
        query: Optional specific query for context (defaults to prompt)

    Returns:
        Claude's response
    """
    context = query_context(query or prompt)

    full_prompt = f"""
{context}

Use the above context to inform your response. Your response should be in English prose with Greek terms integrated naturally where appropriate (see LANGUAGE_GUIDE.md for guidelines). The content must be historically accurate based on the retrieved context.

{prompt}
"""

    response = anthropic.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=2000,
        messages=[{"role": "user", "content": full_prompt}]
    )

    return response.content[0].text


# Example usage
if __name__ == "__main__":
    # Test query
    result = query_context("songs about exile and loneliness")
    print(result)

    # Test generation
    storylet = generate_with_context(
        "Write a storylet for the tekes where the player hears live rebetiko for the first time."
    )
    print(storylet)
```

---

## Integration with Claude Code

When using Claude Code for content generation, the workflow is:

1. **Before generating content**, run a RAG query to pull relevant context
2. **Include context in the prompt** to Claude
3. **Generate** storylets, dialogue, etc. grounded in real data

### Example: Generating a Storylet

```python
# tools/generate_storylet.py
from rag_query import generate_with_context

storylet_prompt = """
Create a storylet in JSON format for the location "tekes".

Requirements:
- The player is new to the tekes
- Describe the atmosphere (smoke, music, lamplight)
- Include dialogue with Kyra Sofia (the owner)
- At least 3 choices for the player
- Use authentic period slang, integrated naturally (see LANGUAGE_GUIDE.md)
- Write in English prose with Greek terms where appropriate

Follow the format from STORYLET_FORMAT.md
"""

result = generate_with_context(
    storylet_prompt,
    query="tekes hashish music atmosphere rebetiko"
)

print(result)
```

---

## File Structure After Setup

```
rebetiko-game/
├── database/
│   ├── kounadis.db          # Your existing Kounadis data
│   ├── game.db              # Game content (schema.sql)
│   └── chromadb/            # Vector database (created by ChromaDB)
│       ├── chroma.sqlite3
│       └── ...
├── tools/
│   ├── init_chromadb.py
│   ├── embed_kounadis.py
│   ├── embed_research.py
│   ├── rag_query.py
│   └── generate_storylet.py
└── venv/                    # Python virtual environment
```

---

## Testing the Pipeline

```bash
# Activate environment
source venv/bin/activate

# Initialize ChromaDB
python tools/init_chromadb.py

# Embed your data (run after adding kounadis.db)
python tools/embed_kounadis.py
python tools/embed_research.py

# Test query
python -c "from tools.rag_query import query_context; print(query_context('ρεμπέτικο Σμύρνη'))"
```

---

## Notes on Embedding Models

ChromaDB uses a default embedding model (all-MiniLM-L6-v2). For better Greek language support, consider:

1. **Multilingual models:** `paraphrase-multilingual-MiniLM-L12-v2`
2. **OpenAI embeddings:** Better quality, costs money
3. **Claude embeddings:** When available via API

To change the embedding model:

```python
from chromadb.utils import embedding_functions

# Use multilingual model
ef = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="paraphrase-multilingual-MiniLM-L12-v2"
)

collection = client.get_or_create_collection(
    name="kounadis_songs",
    embedding_function=ef
)
```
