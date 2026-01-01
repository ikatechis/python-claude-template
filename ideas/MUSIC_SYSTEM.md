# Music System Design

> **Version:** 1.0 | **Status:** Draft | **Updated:** 2025-01-15
> **Depends on:** DESIGN.md, STORYLET_FORMAT.md
> **Dependents:** storylets (performance chains), schema.sql

---

## Overview

Music is not a minigame. Music is what you *become* through living.

The player doesn't compose songs through mechanics — they earn songs through experience. The player doesn't perform through rhythm games — they make strategic choices about what to play for whom, and deal with the consequences.

Two interconnected systems:
1. **Song Acquisition** — How you learn and create songs
2. **Performance** — How you use songs and what happens when you do

---

## Part 1: Song Acquisition

### Song Types

| Type | How Acquired | Significance |
|------|--------------|--------------|
| **Learned** | Taught by NPCs, heard at venues | Your repertoire, shows your training |
| **Mastered** | Practice + high skill | Better performance effects |
| **Original** | Created through lived experience | Defines your identity, highest impact |

### Learning Songs (from others)

Songs are learned through:
- **Direct teaching** — An NPC teaches you (relationship + time)
- **Observation** — You hear it enough times, you pick it up (passive)
- **Collaboration** — Playing with someone who knows it

Each learned song:
- Increases relevant skill (bouzouki, singing, specific dromos)
- Expands repertoire (more choices during performance)
- Connects you to the person who taught it (they hear you play it? they react)

**Example Storylet: Learning a Song**

```json
{
  "id": "panagis_teaches_minore",
  "conditions": {
    "relationships": { "panagis": { "min": 40 } },
    "flags": { "asked_panagis_to_teach": true },
    "skills": { "bouzouki": { "min": 15 } }
  },
  "content": {
    "type": "sequence",
    "sequence": [
      { "type": "narration", "text": "Panagis takes your hands and positions your fingers on the neck. 'No, not there. Here. Feel the distance.'" },
      { "type": "narration", "text": "For an hour, you play the same phrase. Your fingertips burn. He doesn't say if you're doing it right." },
      { "type": "dialogue", "speaker": "panagis", "text": "'Again.'" },
      { "type": "narration", "text": "And then, near the end, something shifts. The phrase stops being notes and becomes... something else." },
      { "type": "dialogue", "speaker": "panagis", "text": "'You hear it now. This is 'Minore tis Avgis.' It belonged to a man in Smyrna. Now it belongs to you. Don't waste it.'" }
    ]
  },
  "effects": {
    "skills": { "bouzouki": 5 },
    "flags": { "knows_song_minore_avgis": true }
  },
  "sets": { "learned_song_from_panagis": true }
}
```

### Creating Original Songs

Original songs emerge from **lived experience + musical skill + emotional state**.

**Required conditions (example: prison song):**
```json
{
  "conditions": {
    "flags": { "served_prison_time": true },
    "skills": { "bouzouki": { "min": 35 } },
    "resources": { "psychi": { "max": 50 } }
  }
}
```

The player doesn't *choose* to write a song. The game triggers a "song emerges" storylet when conditions align — often at night, alone, or in a reflective moment.

**Player Agency in Creation:**

The storylet offers limited choices that shape the song's character:

```json
{
  "id": "song_creation_prison",
  "content": {
    "type": "sequence",
    "sequence": [
      { "type": "narration", "text": "You can't sleep. The bouzouki is in your hands before you realize you've picked it up." },
      { "type": "narration", "text": "Something is coming. You feel it in your chest before your fingers find it." },
      { "type": "narration", "text": "It's about the cell. The walls. What you became inside them." }
    ]
  },
  "choices": [
    {
      "id": "defiant",
      "text": "They didn't break you. The song will say that.",
      "effects": {
        "flags": {
          "has_original_prison_song": true,
          "prison_song_mood": "defiant"
        }
      }
    },
    {
      "id": "broken",
      "text": "They broke something. The song will say that too.",
      "effects": {
        "flags": {
          "has_original_prison_song": true,
          "prison_song_mood": "mournful"
        }
      }
    },
    {
      "id": "revenge",
      "text": "It's about the one who put you there.",
      "effects": {
        "flags": {
          "has_original_prison_song": true,
          "prison_song_mood": "vengeful",
          "prison_song_about_informer": true
        }
      }
    }
  ]
}
```

Same experience (prison), different songs. The mood affects future performance reactions.

### Original Song Categories

| Experience Required | Song Theme | Example Trigger |
|--------------------|------------|-----------------|
| Prison time served | Imprisonment, freedom, betrayal | Night after release |
| Lost a loved one | Death, grief, memory | Alone after funeral |
| Failed romance | Love, loss, regret | After breakup storylet |
| Survived violence | Pain, toughness, scars | Recovering from injury |
| Police persecution | Defiance, injustice, survival | After raid/beating |
| Deep poverty | Hunger, dignity, struggle | Lowest money + psychi |
| Found community | Belonging, loyalty, friendship | High relationships milestone |
| Exile/travel (sailor) | Longing, distance, return | While away from Piraeus |

Each category has 2-3 mood variants based on player choice during creation.

---

## Part 2: Performance System

### Performance as Storylet Chain

A performance is a sequence of connected storylets:

```
[ENTER VENUE] → room setup, who's here tonight
      ↓
[SONG CHOICE 1] → pick from repertoire, see immediate reaction
      ↓
[SONG CHOICE 2] → accumulated mood affects options and reactions
      ↓
[SONG CHOICE 3 or INTERRUPT] → tension may trigger events (parangelia, fight, raid)
      ↓
[PERFORMANCE END] → resolution based on accumulated state
```

### Room State Variables

Set at performance start, modified by each song:

| Variable | Range | Description |
|----------|-------|-------------|
| `perf_mood` | string | "neutral", "melancholy", "defiant", "joyful", "tense" |
| `perf_tension` | 0-100 | Likelihood of conflict |
| `perf_kefi` | 0-100 | Crowd energy and enjoyment |
| `perf_cop_attention` | 0-100 | Police suspicion (if cops present) |
| `perf_romance_chance` | 0-100 | If target present, likelihood of connection |

### Crowd Composition Flags

Set at performance start based on location + time + random factors:

```json
{
  "perf_manges_present": true,
  "perf_manges_count": 2,
  "perf_workers_present": true,
  "perf_woman_alone": true,
  "perf_woman_id": "maria",
  "perf_cop_undercover": true,
  "perf_famous_musician": false,
  "perf_your_enemy_present": false
}
```

Some flags are hidden (undercover cop). Player reads the room but doesn't have perfect information.

### Song Effects

Each song has defined effects on room state:

```json
{
  "song_id": "tis_fylakis",
  "title": "Της Φυλακής",
  "title_en": "The Prison Song",
  "dromos": "hitzaz",
  "mood": "defiant",
  "effects": {
    "perf_mood": "defiant",
    "perf_tension": 15,
    "perf_kefi": 10,
    "perf_cop_attention": 25
  },
  "special_reactions": {
    "manges_present": { "reputation.manges": 5 },
    "cop_present": { "perf_cop_attention": 20 }
  }
}
```

### The Song Choice Storylet

```json
{
  "id": "tekes_performance_song_choice",
  "content": {
    "type": "simple",
    "text": "The crowd waits. What do you play?"
  },
  "choices": [
    {
      "id": "play_fragkosyriani",
      "text": "[Fragkosyriani — a love song, safe]",
      "requires": { "flags": { "knows_song_fragkosyriani": true } },
      "effects": { "perf_mood": "romantic", "perf_kefi": 15 },
      "next": "tekes_performance_reaction_love"
    },
    {
      "id": "play_tis_fylakis",
      "text": "[Tis Fylakis — defiant, risky if cops are here]",
      "requires": { "flags": { "knows_song_tis_fylakis": true } },
      "effects": { "perf_mood": "defiant", "perf_tension": 15, "perf_cop_attention": 25 },
      "next": "tekes_performance_reaction_defiant"
    },
    {
      "id": "play_original_prison",
      "text": "[Your prison song — only you can sing this]",
      "requires": { "flags": { "has_original_prison_song": true } },
      "effects": { "perf_mood": "defiant", "perf_tension": 20, "perf_kefi": 25 },
      "next": "tekes_performance_reaction_original"
    },
    {
      "id": "stop_playing",
      "text": "[Put down the bouzouki]",
      "next": "tekes_performance_end_early"
    }
  ]
}
```

### Event Triggers

After each song (or at performance end), check for triggered events:

**Parangelia (Paid Request):**
```json
{
  "conditions": {
    "flags": { "perf_manges_present": true },
    "resources": { "perf_kefi": { "min": 40 } }
  }
}
→ Mangas stands up, demands his Zeibekiko
```

**Knife Fight:**
```json
{
  "conditions": {
    "flags": { "perf_manges_present": true },
    "resources": {
      "perf_tension": { "min": 70 },
      "perf_alcohol": { "min": 50 }
    }
  }
}
→ Violence erupts
```

**Police Raid:**
```json
{
  "conditions": {
    "flags": { "perf_cop_undercover": true },
    "resources": { "perf_cop_attention": { "min": 60 } }
  }
}
→ Whistles outside, everyone runs
```

**Romance Spark:**
```json
{
  "conditions": {
    "flags": { "perf_woman_alone": true },
    "resources": {
      "perf_romance_chance": { "min": 50 },
      "perf_mood": "romantic"
    }
  }
}
→ She's still there after the show. She's looking at you.
```

**Famous Musician Notices:**
```json
{
  "conditions": {
    "flags": { "perf_famous_musician": true },
    "resources": { "perf_kefi": { "min": 70 } },
    "skills": { "bouzouki": { "min": 50 } }
  }
}
→ After the set, he approaches. "Where did you learn that?"
```

### The Parangelia Chain

When a mangas stands to dance, the performance is interrupted:

```json
{
  "id": "tekes_parangelia_start",
  "content": {
    "type": "sequence",
    "sequence": [
      { "type": "narration", "text": "Nikos rises. The room goes quiet." },
      { "type": "narration", "text": "He walks to you slowly — the mangas walk, each step deliberate — and slaps a fifty-drachma note on the body of your bouzouki." },
      { "type": "narration", "text": "He points at the floor. His floor, now. His dance." },
      { "type": "narration", "text": "Everyone knows the rules. You play until he's done. No one else moves. No one else breathes." }
    ]
  },
  "effects": {
    "money": 50,
    "flags": { "in_parangelia": true, "parangelia_dancer": "nikos" }
  },
  "choices": [
    {
      "id": "play_his_dance",
      "text": "[Begin the Zeibekiko]",
      "next": "tekes_parangelia_dance"
    },
    {
      "id": "refuse",
      "text": "[Shake your head. No.]",
      "requires": { "reputation": { "manges": { "min": 60 } } },
      "effects": { "relationships": { "nikos": -40 }, "reputation": { "manges": -15 } },
      "next": "tekes_parangelia_refused"
    }
  ]
}
```

Then, mid-dance:

```json
{
  "id": "tekes_parangelia_interruption",
  "conditions": {
    "flags": { "in_parangelia": true },
    "random_chance": 0.3
  },
  "content": {
    "type": "sequence",
    "sequence": [
      { "type": "narration", "text": "Nikos turns, slow, arms wide." },
      { "type": "narration", "text": "A drunk sailor at the edge of the room stands up. He's grinning. He doesn't know." },
      { "type": "narration", "text": "He takes a step toward the dance floor." },
      { "type": "narration", "text": "Nikos's hand moves to his belt." }
    ]
  },
  "choices": [
    {
      "id": "keep_playing",
      "text": "[Keep playing. It's not your business.]",
      "effects": { "perf_tension": 40 },
      "next": "tekes_parangelia_violence"
    },
    {
      "id": "stop_music",
      "text": "[Stop the music. Break the spell.]",
      "effects": { "relationships": { "nikos": -30 }, "reputation": { "manges": -10 } },
      "next": "tekes_parangelia_broken"
    },
    {
      "id": "signal_sailor",
      "text": "[Catch the sailor's eye. Shake your head: don't.]",
      "requires": { "reputation": { "manges": { "min": 30 } } },
      "effects": { "flags": { "saved_drunk_sailor": true } },
      "next": "tekes_parangelia_sailor_sits"
    }
  ]
}
```

### Songs Coming Back

Later in the game, the player's songs should echo:

```json
{
  "id": "thessaloniki_hears_your_song",
  "location": "thessaloniki_taverna",
  "conditions": {
    "flags": { "has_original_prison_song": true },
    "resources": { "day": { "min": 200 } }
  },
  "content": {
    "type": "sequence",
    "sequence": [
      { "type": "narration", "text": "You don't recognize the singer. A young man, thin, bad teeth." },
      { "type": "narration", "text": "But you recognize the song." },
      { "type": "narration", "text": "It's yours. The one that came to you in the dark, after they let you out. About the walls. About what you became." },
      { "type": "narration", "text": "He's singing it wrong — the third verse is different, the words changed somewhere along the way." },
      { "type": "narration", "text": "But it's yours. Somehow, it traveled. Somehow, it lived." }
    ]
  },
  "choices": [
    {
      "id": "approach_him",
      "text": "[Wait until he finishes. Then introduce yourself.]",
      "next": "thessaloniki_your_song_revealed"
    },
    {
      "id": "say_nothing",
      "text": "[Say nothing. Drink your wine. Let it belong to everyone now.]",
      "effects": { "psychi": 15 }
    },
    {
      "id": "correct_him",
      "text": "[Stand up. Sing the real third verse.]",
      "effects": { "reputation": { "mousikokosmos": 10 } },
      "next": "thessaloniki_you_sang_your_song"
    }
  ]
}
```

---

## Part 3: Song Database Schema

```sql
CREATE TABLE songs (
    id TEXT PRIMARY KEY,
    title_el TEXT NOT NULL,
    title_en TEXT,
    type TEXT NOT NULL,             -- "traditional", "learned", "original"
    dromos TEXT,                     -- "rast", "hitzaz", "sabah", etc.
    mood TEXT,                       -- "defiant", "mournful", "joyful", "romantic"
    tempo TEXT,                      -- "slow", "medium", "fast"

    -- For learned songs
    taught_by TEXT,                  -- NPC id
    origin_location TEXT,            -- Where it comes from

    -- For original songs
    creation_experience TEXT,        -- "prison", "loss", "love", "poverty", etc.
    creation_storylet TEXT,          -- Storylet that creates it

    -- Lyrics
    lyrics_fragment_el TEXT,         -- First verse in Greek
    lyrics_fragment_en TEXT,         -- English meaning (not translation)

    -- Performance effects (JSON)
    base_effects TEXT,               -- Always applied
    conditional_effects TEXT,        -- Based on crowd/context

    -- Meta
    historical_inspiration TEXT,     -- Real song if based on one
    notes TEXT
);
```

---

## Part 4: Design Principles

### Music as Consequence, Not Action

The player doesn't "do music." They live, and music happens. This keeps the tone serious and the songs meaningful.

### Limited Repertoire Creates Strategy

The player can't play any song — only the ones they know. This makes learning songs valuable and performance choices meaningful.

### Original Songs as Character Signature

By late game, your original songs define who you are. A player with a prison song, a betrayal song, and a love-lost song has a different musical identity than one with sea songs and work songs.

### Hidden Information Creates Drama

The player doesn't know if there's an undercover cop. They don't know if the mangas in the corner is about to snap. They play based on what they see, and sometimes they're wrong.

### Consequences Ripple

The song you play tonight might come back years later. The informer you wrote a song about might hear it. The woman you serenaded might remember when you meet again.

---

## Open Questions

- [ ] How many songs should exist at launch? (Target: 30 traditional, 15 learnable, 10 original templates)
- [ ] Should the player hear actual audio, or is this text-only?
- [ ] How do we handle the dromos system — is it mechanical or just flavor?
- [ ] Can songs be "forgotten" if not played for a long time?
