-- Rebetiko Game Database Schema
-- Version 1.0

-- ============================================================
-- CORE GAME CONTENT
-- ============================================================

-- Locations
CREATE TABLE locations (
    id TEXT PRIMARY KEY,
    name_el TEXT NOT NULL,           -- Greek name
    name_en TEXT NOT NULL,           -- English name
    description TEXT,
    parent_location TEXT,            -- For sub-locations
    available_from_day INTEGER DEFAULT 1,
    unlock_conditions TEXT,          -- JSON conditions
    travel_time_from_camp INTEGER,   -- Minutes
    danger_level INTEGER DEFAULT 0,  -- 0-10
    FOREIGN KEY (parent_location) REFERENCES locations(id)
);

-- NPCs
CREATE TABLE npcs (
    id TEXT PRIMARY KEY,
    name_display TEXT NOT NULL,      -- What player sees
    name_full TEXT,                  -- Full name if known
    name_greek TEXT,                 -- Greek spelling
    archetype TEXT,                  -- "mentor", "rival", "friend", etc.
    description TEXT,
    backstory TEXT,
    age INTEGER,
    origin TEXT,                     -- "smyrna", "piraeus", etc.
    primary_location TEXT,
    schedule TEXT,                   -- JSON: when they're where
    initial_relationship INTEGER DEFAULT 0,
    faction_affiliations TEXT,       -- JSON: faction -> affinity
    portrait_base TEXT,              -- Asset filename
    is_historical BOOLEAN DEFAULT FALSE,
    historical_inspiration TEXT,     -- Real person inspired by
    FOREIGN KEY (primary_location) REFERENCES locations(id)
);

-- NPC Dialogue Patterns (for AI generation)
CREATE TABLE npc_speech_patterns (
    npc_id TEXT,
    pattern_type TEXT,               -- "greeting", "farewell", "angry", etc.
    example TEXT,
    notes TEXT,
    FOREIGN KEY (npc_id) REFERENCES npcs(id)
);

-- Factions
CREATE TABLE factions (
    id TEXT PRIMARY KEY,
    name_el TEXT NOT NULL,
    name_en TEXT NOT NULL,
    description TEXT,
    reputation_thresholds TEXT       -- JSON: level -> effects
);

-- Items
CREATE TABLE items (
    id TEXT PRIMARY KEY,
    name_el TEXT NOT NULL,
    name_en TEXT NOT NULL,
    description TEXT,
    category TEXT,                   -- "keepsake", "weapon", "instrument", etc.
    value_drachmas INTEGER DEFAULT 0,
    is_unique BOOLEAN DEFAULT FALSE,
    effects TEXT                     -- JSON effects when used
);

-- Songs
CREATE TABLE songs (
    id TEXT PRIMARY KEY,
    title_el TEXT NOT NULL,
    title_en TEXT,
    dromos TEXT,                     -- "rast", "hitzaz", "sabah", etc.
    mood_tags TEXT,                  -- JSON array
    theme_tags TEXT,                 -- JSON array
    tempo TEXT,                      -- "slow", "medium", "fast"
    era TEXT,                        -- "1920s", "1930s", etc.
    lyrics_sample TEXT,              -- First verse or excerpt
    taught_by TEXT,                  -- NPC id who teaches it
    learning_conditions TEXT,        -- JSON conditions
    performance_effects TEXT,        -- JSON: what happens when played
    historical_recording TEXT,       -- Link to Kounadis if exists
    FOREIGN KEY (taught_by) REFERENCES npcs(id)
);

-- Skills
CREATE TABLE skills (
    id TEXT PRIMARY KEY,
    name_el TEXT NOT NULL,
    name_en TEXT NOT NULL,
    category TEXT,                   -- "music", "combat", "trade"
    description TEXT,
    max_level INTEGER DEFAULT 100,
    thresholds TEXT                  -- JSON: level -> abilities
);

-- Flags (documentation of all flags used)
CREATE TABLE flags (
    id TEXT PRIMARY KEY,
    description TEXT NOT NULL,
    category TEXT,                   -- "story", "met", "choice", etc.
    set_by TEXT,                     -- Storylet or event that sets it
    checked_by TEXT                  -- Storylets that check it
);

-- ============================================================
-- STORYLET STORAGE
-- ============================================================

CREATE TABLE storylets (
    id TEXT PRIMARY KEY,
    title TEXT,
    location TEXT,
    time_phases TEXT,                -- JSON array
    conditions TEXT,                 -- JSON
    content TEXT,                    -- JSON (the full content)
    choices TEXT,                    -- JSON
    effects TEXT,                    -- JSON
    sets_flags TEXT,                 -- JSON
    tags TEXT,                       -- JSON array
    priority INTEGER DEFAULT 5,
    cooldown INTEGER DEFAULT 0,
    one_time BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status TEXT DEFAULT 'draft',     -- "draft", "review", "final"
    FOREIGN KEY (location) REFERENCES locations(id)
);

-- Storylet search index (for FTS5)
CREATE VIRTUAL TABLE storylets_fts USING fts5(
    id,
    title,
    content,
    tags,
    content='storylets',
    content_rowid='rowid'
);

-- ============================================================
-- KOUNADIS ARCHIVE INTEGRATION
-- ============================================================

-- This mirrors your existing Kounadis database structure
-- Adjust field names to match your actual schema

CREATE TABLE kounadis_songs (
    id INTEGER PRIMARY KEY,
    title TEXT,
    artist TEXT,
    composer TEXT,
    lyricist TEXT,
    year INTEGER,
    label TEXT,
    catalog_number TEXT,
    dromos TEXT,
    rhythm TEXT,
    lyrics TEXT,
    themes TEXT,                     -- JSON array
    notes TEXT,
    audio_file TEXT,
    -- Add your actual Kounadis fields here
    UNIQUE(catalog_number)
);

-- Kounadis full-text search
CREATE VIRTUAL TABLE kounadis_fts USING fts5(
    title,
    artist,
    lyrics,
    themes,
    notes,
    content='kounadis_songs',
    content_rowid='id'
);

-- ============================================================
-- RESEARCH & REFERENCE
-- ============================================================

CREATE TABLE research_entries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    topic TEXT NOT NULL,
    era TEXT,
    source TEXT,
    content TEXT NOT NULL,
    key_facts TEXT,                  -- JSON array of extracted facts
    game_use_potential TEXT,         -- How this could be used
    tags TEXT,                       -- JSON array
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE VIRTUAL TABLE research_fts USING fts5(
    topic,
    content,
    key_facts,
    tags,
    content='research_entries',
    content_rowid='id'
);

-- Slang/terminology glossary
CREATE TABLE slang (
    term TEXT PRIMARY KEY,
    meaning TEXT NOT NULL,
    usage_context TEXT,
    era TEXT,
    example_sentence TEXT,
    source TEXT
);

-- Historical events (for calendar integration)
CREATE TABLE historical_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,                       -- YYYY-MM-DD or YYYY-MM or YYYY
    event TEXT NOT NULL,
    description TEXT,
    game_impact TEXT,                -- How this affects gameplay
    triggers_storylet TEXT           -- Storylet to trigger
);

-- ============================================================
-- EMBEDDINGS (for future semantic search)
-- ============================================================

-- Store embeddings for semantic search
-- This is used when we add ChromaDB or similar
CREATE TABLE embeddings (
    id TEXT PRIMARY KEY,
    source_table TEXT,               -- "storylets", "research", "kounadis"
    source_id TEXT,                  -- ID in source table
    text_content TEXT,               -- Original text
    embedding_model TEXT,            -- Model used
    embedding BLOB,                  -- Vector as blob (or store in ChromaDB)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================
-- INDEXES
-- ============================================================

CREATE INDEX idx_storylets_location ON storylets(location);
CREATE INDEX idx_storylets_status ON storylets(status);
CREATE INDEX idx_npcs_location ON npcs(primary_location);
CREATE INDEX idx_songs_dromos ON songs(dromos);
CREATE INDEX idx_research_topic ON research_entries(topic);

-- ============================================================
-- VIEWS
-- ============================================================

-- All available storylets for a location
CREATE VIEW v_storylets_by_location AS
SELECT
    s.id,
    s.title,
    s.location,
    l.name_en as location_name,
    s.priority,
    s.status
FROM storylets s
JOIN locations l ON s.location = l.id
ORDER BY s.location, s.priority DESC;

-- NPCs with their locations
CREATE VIEW v_npcs_locations AS
SELECT
    n.id,
    n.name_display,
    n.archetype,
    n.primary_location,
    l.name_en as location_name
FROM npcs n
LEFT JOIN locations l ON n.primary_location = l.id;

-- ============================================================
-- SEED DATA
-- ============================================================

-- Factions
INSERT INTO factions (id, name_el, name_en, description) VALUES
('manges', 'Μάγκες', 'Underworld', 'The criminal underworld of Piraeus'),
('mousikokosmos', 'Μουσικόκοσμος', 'Musical Community', 'Musicians, singers, venue owners'),
('koinotita', 'Κοινότητα', 'Community', 'The refugee neighborhood, ordinary people'),
('astynomia', 'Αστυνομία', 'Police', 'State authority, surveillance');

-- Core locations
INSERT INTO locations (id, name_el, name_en, description, travel_time_from_camp) VALUES
('camp', 'Καταυλισμός', 'Refugee Camp', 'The sprawling tent city at Drapetsona', 0),
('port', 'Λιμάνι', 'The Port', 'The commercial docks of Piraeus', 30),
('shore', 'Ακτή', 'The Shore', 'Rocky coastline west of the camp', 15),
('back_streets', 'Σοκάκια', 'Back Streets', 'The narrow alleys between port and city', 20),
('tekes', 'Τεκές', 'The Tekes', 'Underground hashish den with music', 25),
('cafe', 'Καφέ-Αμάν', 'The Cafe', 'Legal music venue in Drapetsona', 45),
('neighborhood', 'Γειτονιά', 'The Neighborhood', 'Refugee quarter where you live', 10);

-- Core skills
INSERT INTO skills (id, name_el, name_en, category, description) VALUES
('bouzouki', 'Μπουζούκι', 'Bouzouki', 'music', 'Skill with the three-stringed bouzouki'),
('baglamas', 'Μπαγλαμάς', 'Baglamas', 'music', 'Skill with the tiny baglamas'),
('singing', 'Τραγούδι', 'Singing', 'music', 'Vocal ability and song knowledge'),
('fighting', 'Μαχητικότητα', 'Fighting', 'combat', 'Knife fighting and brawling'),
('thievery', 'Κλεψιά', 'Thievery', 'crime', 'Pickpocketing and burglary'),
('fishing', 'Ψάρεμα', 'Fishing', 'trade', 'Fishing skill'),
('sailing', 'Ναυτοσύνη', 'Sailing', 'trade', 'Ship work and seamanship');

-- Sample items
INSERT INTO items (id, name_el, name_en, category, description, is_unique) VALUES
('photograph', 'Φωτογραφία', 'Photograph', 'keepsake', 'A faded photograph of faces you are forgetting', TRUE),
('coin', 'Νόμισμα', 'Coin', 'keepsake', 'Your father pressed it into your palm', TRUE),
('key', 'Κλειδί', 'Key', 'keepsake', 'To a door that no longer exists', TRUE),
('knife', 'Μαχαίρι', 'Knife', 'weapon', 'A simple folding knife', FALSE),
('blanket', 'Κουβέρτα', 'Blanket', 'survival', 'A rough wool blanket', FALSE);
