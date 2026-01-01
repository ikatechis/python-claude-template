---
status: draft
version: 1.0.0
last_updated: 2025-01-01
---

# Game State Schema

---

## Overview

The GameState is the single source of truth for all mutable game data. It is saved/loaded as JSON and passed to the storylet engine for condition evaluation.

---

## Complete Schema

```gdscript
# GDScript representation
class_name GameState

# === TEMPORAL ===
var hour: int = 8                    # 0-23
var day: int = 1                     # Day counter from game start
var date: Dictionary = {             # Calendar date
    "year": 1922,
    "month": 9,
    "day": 15
}

# === SPATIAL ===
var current_location: String = "camp"
var known_locations: Array[String] = ["camp"]
var location_states: Dictionary = {} # Location-specific flags

# === RESOURCES ===
var money: int = 0                   # Drachmas
var hunger: int = 50                 # 0-100 (0 = starving, 100 = full)
var health: int = 100                # 0-100 (0 = dead)
var psychi: int = 50                 # 0-100 (spirit/morale)
var heat: int = 0                    # 0-100 (police attention, hidden)
var addiction: int = 0               # 0-100 (hashish dependency)

# === SOCIAL ===
var reputation: Dictionary = {
    "manges": 0,                     # Underworld respect
    "mousikokosmos": 0,              # Musical community
    "koinotita": 0,                  # Neighborhood/refugee trust
    "astynomia": 0                   # Police awareness (inverse)
}

var relationships: Dictionary = {}   # npc_id -> int (0-100)

# === PROGRESS ===
var flags: Dictionary = {}           # flag_name -> bool
var storylets_seen: Dictionary = {}  # storylet_id -> timestamp
var choices_made: Array[Dictionary] = [] # History of choices

# === SKILLS ===
var skills: Dictionary = {
    "bouzouki": 0,
    "baglamas": 0,
    "guitar": 0,
    "singing": 0,
    "fighting": 0,
    "thievery": 0,
    "fishing": 0,
    "sailing": 0
}

var songs_known: Array[String] = []  # song_ids
var instruments_owned: Array[String] = []

# === INVENTORY ===
var inventory: Array[String] = []    # item_ids

# === TRACK AFFINITY ===
var track_affinity: Dictionary = {
    "music": 0,
    "crime": 0,
    "sea": 0,
    "work": 0
}

# === META ===
var player_name: String = ""
var player_origin: String = ""       # "smyrna", "aivali", etc.
var starting_keepsake: String = ""   # "photograph", "coin", "key", "nothing"
var family_status: String = ""       # "dead", "lost", "sick"
```

---

## Field Details

### Temporal

#### hour (int, 0-23)
Current hour in 24-hour format. Advances through actions and travel.

#### day (int, 1+)
Day counter from game start. Used for storylet conditions like `min_day`.

#### date (Dictionary)
Calendar date for historical events and long-term tracking.

```gdscript
func get_date_string() -> String:
    return "%d-%02d-%02d" % [date.year, date.month, date.day]

func get_phase() -> String:
    if hour >= 6 and hour < 12:
        return "proi"       # Morning
    elif hour >= 12 and hour < 18:
        return "apogeyma"   # Afternoon
    elif hour >= 18 and hour < 22:
        return "vrady"      # Evening
    else:
        return "nychta"     # Night
```

### Spatial

#### current_location (String)
ID of current location. Must match a key in locations database.

**Valid values:** `camp`, `port`, `shore`, `back_streets`, `tekes`, `cafe`, `neighborhood`, etc.

#### known_locations (Array[String])
Locations the player has discovered. Unknown locations don't appear on travel menu.

#### location_states (Dictionary)
Per-location state tracking:

```gdscript
location_states = {
    "tekes": {
        "raided_recently": true,
        "last_visit_day": 15
    },
    "port": {
        "knows_stavros": true
    }
}
```

### Resources

#### money (int)
Drachmas. Can be negative (debt).

**Reference values (1934):**
- 0-30: Desperate poverty
- 30-100: Surviving
- 100-300: Comfortable
- 300+: Relatively wealthy

#### hunger (int, 0-100)
- **0:** Starving, health damage
- **1-25:** Hungry, negative effects
- **26-75:** Normal
- **76-100:** Full, no concerns

Depletes by ~10 per day phase.

#### health (int, 0-100)
- **0:** Death
- **1-25:** Critical, many actions unavailable
- **26-50:** Injured/sick
- **51-75:** Minor issues
- **76-100:** Healthy

Affected by: work, violence, disease, starvation, weather.

#### psychi (int, 0-100)
Spirit/morale. Represents mental state.

- **0-25:** Depressed, dialogue options locked, dark thoughts
- **26-50:** Low, pessimistic
- **51-75:** Normal
- **76-100:** High spirits, creativity bonus

Affected by: music, connection, hashish (temporary), trauma, loss.

#### heat (int, 0-100)
Police attention. **Hidden from player** — they feel it through events.

- **0-25:** Safe, police ignore you
- **26-50:** On radar, random checks possible
- **51-75:** Watched, frequent stops
- **76-100:** Hunted, raids, arrests

Increases: Crime, being seen, informants
Decreases: Time, bribes, laying low

#### addiction (int, 0-100)
Hashish dependency. Emerges if player smokes frequently.

- **0:** No dependency
- **1-25:** Mild, no mechanical effect
- **26-50:** Moderate, psychi penalties without use
- **51-75:** Severe, withdrawal symptoms
- **76-100:** Destructive, health and relationship damage

### Social

#### reputation (Dictionary)
Four factions, each 0-100:

**manges (Underworld)**
- Gained: Honor code, toughness, not snitching
- Lost: Cowardice, betrayal, talking to police
- Effects: Underworld storylets, protection, danger

**mousikokosmos (Musical Community)**
- Gained: Good performances, learning, respect for tradition
- Lost: Selling out, plagiarism, disrespect
- Effects: Music storylets, teaching, recording access

**koinotita (Community)**
- Gained: Helping refugees, reliability, family
- Lost: Bringing trouble, abandonment, selfishness
- Effects: Housing, work opportunities, social support

**astynomia (Police)**
- Note: This is AWARENESS, not favor
- Gained: Any police contact, being noticed
- Lost: Time passing, bribes
- Effects: Raids, stops, arrest probability

#### relationships (Dictionary)
Per-NPC relationship values, 0-100:

```gdscript
relationships = {
    "dimitris": 45,
    "panagis": 60,
    "kyra_sofia": 30,
    "thomas": 20
}
```

**Thresholds:**
- **0-10:** Hostile/unknown
- **11-30:** Acquaintance
- **31-50:** Friendly
- **51-70:** Close
- **71-90:** Trusted
- **91-100:** Intimate/loyal

### Progress

#### flags (Dictionary)
Boolean flags for tracking events:

```gdscript
flags = {
    # Tutorial/progression
    "tutorial_complete": true,
    "left_camp": true,

    # Character knowledge
    "met_dimitris": true,
    "knows_thomas_real_name": false,

    # Story events
    "witnessed_stabbing": true,
    "panagis_dead": true,

    # Choices
    "stole_bread": true,
    "refused_thomas_job": false
}
```

#### storylets_seen (Dictionary)
Tracks when storylets were triggered for cooldown:

```gdscript
storylets_seen = {
    "tekes_ambient_quiet_night": 1697234567,  # Unix timestamp
    "dimitris_friendship_01": 1697134567
}
```

#### choices_made (Array[Dictionary])
History for analysis/debugging:

```gdscript
choices_made = [
    {
        "storylet": "camp_water_line",
        "choice": "talk_to_dimitris",
        "day": 1,
        "timestamp": 1697234567
    }
]
```

### Skills

#### skills (Dictionary)
Skill levels 0-100:

```gdscript
skills = {
    "bouzouki": 25,      # Main instrument skill
    "baglamas": 0,       # Secondary instrument
    "guitar": 0,         # Rhythm instrument
    "singing": 15,       # Vocal ability
    "fighting": 10,      # Combat
    "thievery": 20,      # Stealing, lockpicking
    "fishing": 5,        # Shore/sea path
    "sailing": 0         # Ship work
}
```

**Skill thresholds:**
- **0-10:** Novice
- **11-30:** Beginner
- **31-50:** Competent
- **51-70:** Skilled
- **71-90:** Expert
- **91-100:** Master

#### songs_known (Array[String])
Song IDs the player can perform:

```gdscript
songs_known = [
    "fragkosyriani",
    "minore_tou_teke",
    "taxim_rast"
]
```

#### instruments_owned (Array[String])
```gdscript
instruments_owned = [
    "panagis_bouzouki",  # Inherited
    "cheap_baglamas"     # Bought
]
```

### Inventory

#### inventory (Array[String])
Item IDs currently carried:

```gdscript
inventory = [
    "photograph",        # Keepsake
    "knife",            # Weapon
    "blanket"           # Survival
]
```

**Item categories:**
- **Keepsakes:** photograph, coin, key
- **Weapons:** knife, razor
- **Survival:** blanket, food_bread, water_flask
- **Instruments:** bouzouki_*, baglamas_*
- **Valuables:** jewelry, watch
- **Documents:** nansen_passport, work_permit

### Track Affinity

#### track_affinity (Dictionary)
Measures how much player has engaged with each track:

```gdscript
track_affinity = {
    "music": 45,    # Musician path
    "crime": 20,    # Underworld path
    "sea": 10,      # Sailor path
    "work": 25      # Worker path
}
```

Primary track = highest value. Affects:
- Available storylets
- NPC reactions
- Ending calculations

### Meta

#### player_name (String)
Set during tutorial or left empty for "Unknown."

#### player_origin (String)
Set in opening: `"smyrna"`, `"aivali"`, `"constantinople"`, etc.

#### starting_keepsake (String)
From opening choice: `"photograph"`, `"coin"`, `"key"`, `"nothing"`

#### family_status (String)
From opening choice: `"dead"`, `"lost"`, `"sick"`

---

## Save/Load Format

```json
{
  "version": "1.0",
  "timestamp": "2024-01-15T14:30:00Z",
  "playtime_seconds": 3600,

  "temporal": {
    "hour": 22,
    "day": 15,
    "date": { "year": 1922, "month": 10, "day": 1 }
  },

  "spatial": {
    "current_location": "tekes",
    "known_locations": ["camp", "port", "tekes", "neighborhood"],
    "location_states": {}
  },

  "resources": {
    "money": 45,
    "hunger": 60,
    "health": 85,
    "psychi": 70,
    "heat": 15,
    "addiction": 5
  },

  "social": {
    "reputation": {
      "manges": 30,
      "mousikokosmos": 45,
      "koinotita": 25,
      "astynomia": 10
    },
    "relationships": {
      "dimitris": 55,
      "kyra_sofia": 35
    }
  },

  "progress": {
    "flags": {
      "tutorial_complete": true,
      "met_dimitris": true
    },
    "storylets_seen": {},
    "choices_made": []
  },

  "skills": {
    "skills": { "bouzouki": 25, "singing": 15 },
    "songs_known": ["taxim_rast"],
    "instruments_owned": ["panagis_bouzouki"]
  },

  "inventory": ["photograph", "knife"],

  "track_affinity": {
    "music": 45,
    "crime": 10,
    "sea": 5,
    "work": 15
  },

  "meta": {
    "player_name": "Stelios",
    "player_origin": "smyrna",
    "starting_keepsake": "photograph",
    "family_status": "dead"
  }
}
```

---

## Utility Functions

```gdscript
class_name GameState

func get_phase() -> String:
    # Returns current time phase

func advance_time(minutes: int) -> void:
    # Advances time, handling day rollover

func get_primary_track() -> String:
    # Returns track with highest affinity

func check_condition(condition: Dictionary) -> bool:
    # Evaluates a storylet condition against current state

func apply_effects(effects: Dictionary) -> void:
    # Applies storylet effects to state

func get_relationship(npc_id: String) -> int:
    # Returns relationship value, defaulting to 0

func modify_relationship(npc_id: String, delta: int) -> void:
    # Safely modifies relationship within 0-100

func has_flag(flag_name: String) -> bool:
    # Returns flag value, defaulting to false

func set_flag(flag_name: String, value: bool = true) -> void:
    # Sets a flag

func has_item(item_id: String) -> bool:
    # Checks inventory

func add_item(item_id: String) -> void:
    # Adds to inventory

func remove_item(item_id: String) -> bool:
    # Removes from inventory, returns success

func save_to_json() -> String:
    # Serializes state to JSON

func load_from_json(json_string: String) -> void:
    # Deserializes state from JSON
```
