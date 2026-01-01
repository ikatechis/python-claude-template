---
status: draft
version: 1.0.0
last_updated: 2025-01-01
---

# Storylet Format Specification

---

## Overview

Storylets are the atomic unit of narrative content. Each storylet is a self-contained scene with conditions, content, choices, and effects.

---

## JSON Schema

```json
{
  "id": "string (unique identifier)",
  "title": "string (for editor display, not shown to player)",
  "location": "string (location_id where this can trigger)",
  "time": ["array of valid time phases"],

  "conditions": {
    "min_day": "integer (optional)",
    "max_day": "integer (optional)",
    "date_after": "string YYYY-MM-DD (optional)",
    "date_before": "string YYYY-MM-DD (optional)",
    "flags": { "flag_name": true/false },
    "flags_any": ["flag1", "flag2"],
    "relationships": { "npc_id": { "min": 0, "max": 100 } },
    "reputation": { "faction_id": { "min": 0, "max": 100 } },
    "resources": { "resource_name": { "min": 0, "max": 100 } },
    "items": ["required_item_ids"],
    "skills": { "skill_name": { "min": 0 } },
    "track_affinity": { "track_name": { "min": 0 } }
  },

  "content": {
    "type": "simple | sequence",
    "text": "string (if simple)",
    "sequence": ["array of content blocks (if sequence)"]
  },

  "choices": [
    {
      "id": "string (unique within storylet)",
      "text": "string (shown to player)",
      "requires": { "same structure as conditions" },
      "effects": { "effect object" },
      "next": "string (storylet_id to chain, optional)"
    }
  ],

  "effects": { "effects applied when storylet completes" },
  "sets": { "flags to set when storylet completes" },

  "tags": ["array of tags for filtering/searching"],
  "priority": "integer 1-10 (higher = more likely to trigger)",
  "cooldown": "integer (days before can trigger again, 0 = no cooldown)",
  "one_time": "boolean (if true, can only trigger once ever)"
}
```

---

## Field Details

### id
- **Format:** `location_category_descriptor`
- **Examples:** `tekes_ambient_smoking`, `port_work_first_day`, `dimitris_friendship_betrayal`
- **Rules:** Lowercase, underscores, unique across all storylets

### location
- **Values:** Must match a location_id in the locations database
- **Special value:** `"any"` for storylets that can trigger anywhere

### time
- **Values:** `["proi", "apogeyma", "vrady", "nychta"]`
- **proi:** Morning (6:00-12:00)
- **apogeyma:** Afternoon (12:00-18:00)
- **vrady:** Evening (18:00-22:00)
- **nychta:** Night (22:00-6:00)
- **Empty array:** Can trigger at any time

### conditions

All conditions are optional. If specified, ALL must be true (AND logic).

```json
{
  "min_day": 5,                          // Game day >= 5
  "max_day": 10,                         // Game day <= 10
  "date_after": "1934-03-15",            // After this date
  "date_before": "1936-08-04",           // Before Metaxas

  "flags": {
    "met_panagis": true,                 // Flag must be true
    "panagis_dead": false                // Flag must be false
  },

  "flags_any": ["has_bouzouki", "has_baglamas"],  // At least one true

  "relationships": {
    "dimitris": { "min": 30 },           // Relationship >= 30
    "thomas": { "min": 20, "max": 50 }   // Between 20-50
  },

  "reputation": {
    "manges": { "min": 40 }              // Faction rep >= 40
  },

  "resources": {
    "money": { "min": 50 },              // At least 50 drachmas
    "psychi": { "max": 30 },             // Psychi is low
    "heat": { "min": 60 }                // High police attention
  },

  "items": ["knife", "photograph"],      // Must have these items

  "skills": {
    "bouzouki": { "min": 20 }            // Skill level >= 20
  },

  "track_affinity": {
    "music": { "min": 30 }               // Leaning musician
  }
}
```

### content

**Simple format:**
```json
{
  "type": "simple",
  "text": "The tekes is quiet tonight. Only three men sit in the corner, passing the hookah in silence."
}
```

**Sequence format:**
```json
{
  "type": "sequence",
  "sequence": [
    {
      "type": "narration",
      "text": "The tekes is quiet tonight."
    },
    {
      "type": "narration",
      "text": "Only three men sit in the corner, passing the hookah in silence."
    },
    {
      "type": "dialogue",
      "speaker": "kyra_sofia",
      "text": "You're early. The music doesn't start until the moon rises."
    },
    {
      "type": "action",
      "text": "She gestures to an empty cushion by the wall."
    }
  ]
}
```

**Content block types:**
- `narration` — Descriptive text, no speaker
- `dialogue` — Character speech, requires `speaker` (npc_id)
- `action` — Stage direction, character action
- `thought` — Player character's internal thought
- `memory` — Flashback or memory fragment

### choices

```json
{
  "choices": [
    {
      "id": "sit_and_wait",
      "text": "Sit down and wait for the music.",
      "effects": {
        "time": 60,
        "psychi": 5
      }
    },
    {
      "id": "ask_about_markos",
      "text": "\"Is Markos playing tonight?\"",
      "requires": {
        "flags": { "knows_markos": true }
      },
      "effects": {
        "relationships": { "kyra_sofia": 5 }
      },
      "next": "tekes_markos_inquiry"
    },
    {
      "id": "leave",
      "text": "Leave. This isn't the night.",
      "effects": {
        "psychi": -5
      }
    }
  ]
}
```

**Choice fields:**
- `id` — Unique within storylet, used for tracking
- `text` — Shown to player, can include dialogue in quotes
- `requires` — Optional conditions to show this choice
- `effects` — Changes to game state
- `next` — Optional storylet to chain to

### effects

Effects modify game state. Applied when storylet completes or when choice is made.

```json
{
  "effects": {
    "time": 30,                          // Advance 30 minutes
    "time_phase": "nychta",              // Skip to phase

    "money": 50,                         // Add 50 (use negative to subtract)
    "hunger": -20,                       // Reduce hunger (eating)
    "health": -10,                       // Lose health
    "psychi": 15,                        // Gain spirit
    "heat": 5,                           // Increase police attention

    "relationships": {
      "dimitris": 10,                    // Improve relationship
      "thomas": -5                       // Damage relationship
    },

    "reputation": {
      "manges": 10,
      "astynomia": 5                     // Being noticed by police
    },

    "flags": {
      "first_smoke": true,
      "owes_thomas": true
    },

    "items_add": ["knife"],
    "items_remove": ["money_pouch"],

    "skills": {
      "bouzouki": 5                      // Skill improvement
    },

    "track_affinity": {
      "crime": 10                        // Lean toward crime track
    },

    "location": "back_streets",          // Force move to location

    "trigger_storylet": "police_raid"    // Immediately trigger another
  }
}
```

### sets

Shorthand for setting flags when storylet completes:

```json
{
  "sets": {
    "visited_tekes": true,
    "met_kyra_sofia": true
  }
}
```

### tags

Used for filtering, searching, and AI content generation:

```json
{
  "tags": [
    "ambient",        // Category
    "tekes",          // Location
    "smoking",        // Theme
    "quiet",          // Mood
    "kyra_sofia"      // NPCs involved
  ]
}
```

**Standard tag categories:**
- **Category:** ambient, event, character, quest, tutorial
- **Mood:** quiet, tense, joyful, melancholy, dangerous
- **Theme:** music, crime, survival, love, death, friendship
- **Track:** music_path, crime_path, sea_path, work_path

### priority

1-10 scale. When multiple storylets are available, higher priority storylets are more likely to be selected.

- **1-3:** Rare events, low importance
- **4-6:** Standard content
- **7-8:** Important story beats
- **9-10:** Critical/unmissable content

### cooldown

Days before storylet can trigger again.

- **0:** Can trigger every time conditions are met
- **1:** Once per day
- **7:** Once per week
- **-1:** Special value meaning "once per location visit"

### one_time

If true, storylet can only ever trigger once per playthrough, regardless of cooldown.

---

## Complete Example

```json
{
  "id": "tekes_parangelia_fight",
  "title": "The Interrupted Dance",

  "location": "tekes",
  "time": ["nychta"],

  "conditions": {
    "min_day": 10,
    "flags": {
      "witnessed_zeibekiko": true,
      "parangelia_fight_seen": false
    },
    "resources": {
      "heat": { "max": 50 }
    },
    "reputation": {
      "manges": { "min": 20 }
    }
  },

  "content": {
    "type": "sequence",
    "sequence": [
      {
        "type": "narration",
        "text": "Nikos rises to dance. He slaps a fifty-drachma note on the bouzouki and points at the floor. The musicians begin."
      },
      {
        "type": "narration",
        "text": "The Zeibekiko. His Zeibekiko. No one else moves."
      },
      {
        "type": "narration",
        "text": "Then the sailor stands. Drunk, swaying, trying to join the dance."
      },
      {
        "type": "dialogue",
        "speaker": "nikos",
        "text": "..."
      },
      {
        "type": "narration",
        "text": "Nikos stops. The music falters. Every eye in the tekes turns to the sailor."
      }
    ]
  },

  "choices": [
    {
      "id": "keep_playing",
      "text": "Keep playing. Let it unfold.",
      "effects": {
        "relationships": { "nikos": 5 },
        "heat": 10,
        "flags": { "witnessed_tekes_stabbing": true }
      },
      "next": "tekes_parangelia_blood"
    },
    {
      "id": "stop_music",
      "text": "Stop the music. Break the tension.",
      "requires": {
        "skills": { "bouzouki": { "min": 10 } }
      },
      "effects": {
        "relationships": { "nikos": -15 },
        "psychi": -5,
        "reputation": { "manges": -5 }
      }
    },
    {
      "id": "warn_sailor",
      "text": "Shout a warning to the sailor.",
      "requires": {
        "reputation": { "manges": { "min": 40 } }
      },
      "effects": {
        "relationships": { "nikos": -5 },
        "flags": { "saved_sailor": true },
        "reputation": { "koinotita": 5 }
      }
    },
    {
      "id": "slip_out",
      "text": "Slip out before this gets ugly.",
      "effects": {
        "location": "street",
        "heat": -5
      }
    }
  ],

  "sets": {
    "parangelia_fight_seen": true
  },

  "tags": ["event", "tekes", "violence", "nikos", "zeibekiko", "tense"],
  "priority": 8,
  "cooldown": 0,
  "one_time": true
}
```

---

## File Organization

Storylets are organized by location:

```
data/storylets/
├── camp/
│   ├── ambient.json
│   ├── dimitris.json
│   ├── old_musician.json
│   └── events.json
├── tekes/
│   ├── ambient.json
│   ├── kyra_sofia.json
│   ├── performances.json
│   └── events.json
├── port/
│   └── ...
└── global/
    ├── random_encounters.json
    └── time_events.json
```

Each file contains an array of storylets:

```json
{
  "storylets": [
    { ... },
    { ... }
  ]
}
```

---

## Validation Rules

1. All `id` values must be unique across the entire game
2. All `location` values must exist in locations database
3. All `speaker` values must exist in NPCs database
4. All `flag` references must be documented in flags database
5. All `next` references must point to existing storylet ids
6. Choices must have at least one option with no requirements (fallback)

---

## Engine Behavior

1. **Load:** All storylets loaded at game start
2. **Filter:** Current location, time, and conditions checked
3. **Weight:** Available storylets weighted by priority
4. **Select:** Random selection from weighted pool
5. **Display:** Content rendered with typing effect
6. **Choice:** Player selects from available choices
7. **Apply:** Effects applied to game state
8. **Chain:** If `next` specified, immediately load that storylet
9. **Cooldown:** Mark storylet with trigger timestamp
