---
status: draft
version: 1.0.0
last_updated: 2026-01-01
dependencies: DESIGN.md
dependents: All storylet content, UI text
---

# Language & Localization Guide

## Overview

The game is written in **English** with Greek elements preserved for authenticity. The goal is accessibility without tourism — the player should feel immersed in a Greek world, not lectured about it.

---

## Core Principles

### 1. Naturalized Foreignness

Greek terms are introduced *in context*, not translated or footnoted. The prose teaches meaning through usage.

**Bad:**
> The *mangas* (Greek: tough guy/street-smart man) walked into the *tekes* (Greek: hashish den).

**Good:**
> The mangas walked into the tekes like he owned it. Men like him — the *magkes*, they called themselves — usually did own places like this. Or thought they did.

By the second mention, the player understands. By the fifth, they're thinking in these terms.

### 2. What Stays in Greek

| Category | Examples | Reason |
|----------|----------|--------|
| **Untranslatable concepts** | μάγκας, ντέρτι, κέφι, ψυχή | No English equivalent captures the meaning |
| **Song titles** | Φραγκοσυριανή, Μινόρε της Αυγής | Authenticity, recognizable to those who know |
| **Musical terms** | ταξίμι, δρόμος, αμανές, παραγγελία | Technical vocabulary of the world |
| **Exclamations** | Γεια σου!, Ώπα!, Άντε ρε | Flavor, rhythm, authenticity |
| **Place names** | Πειραιάς (first use), then Piraeus | Grounding, then accessibility |
| **Terms of address** | ρε, μωρέ, κυρά, μπάρμπα | Social texture |

### 3. What's Written in English

- All narrative prose
- All dialogue (with Greek terms mixed in naturally)
- All UI elements
- All system text
- Descriptions and stage directions

### 4. How Greek Terms Are Introduced

**First use:** Contextual definition woven into prose

> He was a *mangas* — you could see it in the way he walked, slow and deliberate, like every step was a statement. The other men made room for him without being asked.

**Subsequent uses:** No explanation needed

> The mangas nodded at you. That was something.

**Player glossary:** Terms are added to an in-game journal/glossary as they're encountered (see below).

---

## The Glossary System

### How It Works

1. When a Greek term appears for the first time, it's flagged in the storylet
2. The term is added to the player's "Λέξεις" (Words) journal section
3. Player can check the glossary anytime but doesn't need to
4. Glossary entries are written *in character* — as if the protagonist is noting down new vocabulary

### Glossary Entry Format

```json
{
  "term": "μάγκας",
  "transliteration": "mangas",
  "short": "A man who lives by the code of the streets. Tough, proud, dangerous.",
  "long": "The magkes are the men who run the margins — the tekes, the card games, the knife fights. They have their own rules. Respect is everything. Weakness is death. I don't know if I want to become one. But I need to understand them to survive here.",
  "first_encountered": "storylet_id",
  "category": "people"
}
```

### Glossary Categories

- **Άνθρωποι (People)** — mangas, rebetis, teketzis, karfi, etc.
- **Τόποι (Places)** — tekes, koutouki, piatsa, mandra, etc.
- **Μουσική (Music)** — taximi, dromos, amanes, parangelia, hartoura, etc.
- **Ζωή (Life)** — derti, kefi, psychi, filotimo, etc.

### Implementation

In storylet JSON:

```json
{
  "content": {
    "type": "simple",
    "text": "The {mangas}(glossary:mangas) at the corner table hasn't moved in an hour."
  }
}
```

The engine:
1. Renders "mangas" in styled text (italics or slight highlight)
2. Checks if `glossary_mangas` flag is set
3. If not, adds to glossary and sets flag
4. If player clicks/hovers (optional), shows short definition

---

## Greek Text Display

### Song Lyrics

When original song lyrics are shown, display Greek with English meaning below:

```
Πέρασα φυλακές και πέρασα βουνά
Μα σαν εσένα βάσανο, κανένα

---
I passed through prisons and I passed through mountains
But a torment like you — never.
```

The English is *meaning*, not literal translation. It should read as poetry.

### Signs and Environmental Text

In-world Greek text (shop signs, posters, newspapers) stays in Greek but is:
- Readable if the player knows Greek
- Conveyed through context if they don't
- Occasionally translated by NPCs ("That sign says they're hiring")

### Character Names

Characters are introduced with Greek names, spelled in Latin alphabet after first use:

> "I'm Παναγιώτης. But everyone calls me Panagis."

From then on, the game uses "Panagis."

---

## Dialogue Style

### Register and Formality

Characters speak differently based on class, education, and relationship:

**Mangas (street):**
> "Άντε ρε, what are you looking at? You got a problem?"

**Educated/upper class:**
> "I wouldn't recommend lingering here after dark. This isn't Kolonaki."

**Older refugee:**
> "Back in Smyrna... but what's the use. Smyrna is ash."

**Player character (internal):**
> Thoughtful, observant, somewhere between — they're educated enough to narrate, street enough to survive.

### Slang Integration

Slang is used sparingly but consistently:

- **Authentic:** Used by characters who would use it
- **Not translated:** Context makes meaning clear
- **Not overused:** A few terms per scene, not every sentence

**Overwritten:**
> "Ρε μάγκα, we got κέφι tonight, eh? Πάμε to the τεκέ for some μαύρο and ντέρτι!"

**Natural:**
> "You coming or not? There's kefi tonight. Real music."

---

## Style Guide for Writers

### Do:

- Use Greek terms when English truly can't capture the meaning
- Introduce terms through context, not explanation
- Let characters teach vocabulary naturally ("That's called a parangelia — when someone pays for their dance")
- Use transliteration after establishing the Greek (Παναγής → Panagis)
- Keep Greek exclamations short and impactful
- Write English that has the *rhythm* of Greek speech (shorter sentences, more pauses, direct address)

### Don't:

- Translate everything (loses texture)
- Leave everything in Greek (loses accessibility)
- Use footnotes or parenthetical translations
- Overload any single passage with Greek terms
- Make non-Greek speakers feel they're missing crucial information
- Make Greek speakers feel it's been flattened for tourists

### The Balance Test

Read your passage aloud. A player who knows no Greek should:
- Understand what's happening
- Feel the foreignness as texture, not barrier
- Learn 1-2 new terms naturally

A player who knows Greek should:
- Feel the authenticity
- Appreciate the untranslated elements
- Not cringe at misuse or errors

---

## Localization Notes (Future)

### Greek Version ("Director's Cut")

If a Greek localization is made:
- All English prose → Greek
- Greek terms remain (no longer italicized)
- Deeper slang integration possible
- Some explanatory context can be removed (Greek players know what a tekes is)
- Song lyrics shown only in Greek (no translation line)
- Glossary becomes optional/hidden

### Other Languages

For other languages (German, French, etc.):
- Same principle: target language prose + Greek preserved terms
- Glossary essential
- May need slightly more contextual explanation

---

## File Structure for Text

```
godot/data/
├── storylets/
│   └── *.json          # English prose, Greek terms marked
├── glossary/
│   └── terms.json      # All glossary entries
├── songs/
│   └── lyrics.json     # Greek + English meaning
└── ui/
    └── strings.json    # UI text (English)
```

---

## Sample Passage

Here's how a scene reads with these principles applied:

---

The tekes was below street level — you had to know the stairs were there, hidden behind the coal seller's shop. Inside, the air was thick enough to chew. Smoke from the narghile curled toward a ceiling you couldn't see.

Three men sat in a circle, passing the pipe. They didn't look up when you entered. That was a test, or maybe just indifference. Hard to tell with magkes.

"Νέος," one of them said. *New one.* It wasn't a question.

The bouzouki player in the corner kept playing — a taximi, slow and winding, searching for something it hadn't found yet. He was old. His fingers moved like they remembered being young.

"Κάτσε," the first man said. *Sit.*

You sat.

"You play?" He gestured at the old man. "Like him?"

"I'm learning."

"Everybody's learning." He took a long pull from the pipe. The coal glowed red. "Some people learn too slow. They die stupid."

He passed you the kalami — the reed stem, still warm from his lips.

"Welcome to Piraeus."

---

## Glossary Entry: τεκές (tekes)

*Added to glossary when player first enters*

**Short:** An illegal hashish den, usually with music. The heart of rebetiko culture.

**Long:** The tekedes are where the real music lives — not the cleaned-up café songs for tourists, but the raw stuff. Smoke and wine and men who've seen the inside of Averoff Prison. The police raid them sometimes, but they always come back. They're part of Piraeus like the sea is.

---

## Open Questions

- [ ] Voice acting: If implemented, should it be in Greek with English subtitles?
- [ ] How much Greek text is shown in-world (signs, newspapers)?
- [ ] Should the glossary be diegetic (the character's notebook) or meta (game menu)?
- [ ] How do we handle the Turkish/Armenian vocabulary some refugees would use?
