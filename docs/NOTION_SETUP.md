---
status: draft
version: 0.1.0
last_updated: 2025-01-01
---

# Notion Workspace Specification

This document specifies the Notion workspace structure for the Rebetiko game project. Use this as a guide when setting up Notion manually, or let Claude Code create it via the Notion MCP server.

---

## MCP Server Setup

### Prerequisites
1. Notion account with a workspace
2. Notion API integration key

### Getting the API Key
1. Go to https://www.notion.so/my-integrations
2. Click "New integration"
3. Name it "Rebetiko Game Dev"
4. Select your workspace
5. Copy the "Internal Integration Token"

### Claude Code Configuration

Add to your Claude Code MCP settings:

```json
{
  "mcpServers": {
    "notion": {
      "command": "npx",
      "args": ["-y", "@notionhq/notion-mcp-server"],
      "env": {
        "NOTION_API_KEY": "secret_your_key_here"
      }
    }
  }
}
```

### Share Pages with Integration
In Notion, you must explicitly share pages with the integration:
1. Open the page/database
2. Click "..." menu → "Add connections"
3. Select your integration

---

## Workspace Structure

```
📁 Ο Δρόμος του Μάγκα
├── 📄 Dashboard (Home)
├── 📁 Design
│   ├── 📄 Game Design Document
│   ├── 📄 Narrative Bible
│   ├── 📄 Systems Design
│   └── 📄 Art Bible
├── 📁 Content
│   ├── 🗃️ Storylets Database
│   ├── 🗃️ NPCs Database
│   ├── 🗃️ Locations Database
│   ├── 🗃️ Songs Database
│   └── 🗃️ Flags Database
├── 📁 Production
│   ├── 🗃️ Tasks Database
│   ├── 🗃️ Sprints Database
│   ├── 📄 Current Sprint
│   └── 📄 Roadmap
├── 📁 Assets
│   ├── 🗃️ Backgrounds Tracker
│   ├── 🗃️ Portraits Tracker
│   └── 🗃️ Audio Tracker
├── 📁 Research
│   ├── 🗃️ Historical Research
│   ├── 📄 Slang Glossary
│   └── 📄 Timeline
└── 📄 Ideas & Brainstorming
```

---

## Database Specifications

### Tasks Database

**Properties:**

| Property | Type | Options/Notes |
|----------|------|---------------|
| Task | Title | Task name |
| Status | Select | Backlog, Todo, In Progress, Review, Done, Blocked |
| Phase | Select | 0: Foundation, 1: PoC, 2: Vertical Slice, 3: Production |
| Category | Select | Code, Art, Writing, Design, Audio, Research, PM |
| Priority | Select | P0 (Critical), P1 (High), P2 (Medium), P3 (Low) |
| Estimated Hours | Number | |
| Actual Hours | Number | |
| Assignee | Person | (for future team expansion) |
| Due Date | Date | |
| Sprint | Relation | → Sprints Database |
| Blocked By | Relation | → Tasks (self-reference) |
| Notes | Text | |

**Views:**
- Kanban by Status
- Table by Phase
- Calendar
- This Week filter
- My Tasks filter

---

### Storylets Database

**Properties:**

| Property | Type | Options/Notes |
|----------|------|---------------|
| ID | Title | e.g., "tekes_ambient_01" |
| Title (Display) | Text | Human-readable title |
| Location | Relation | → Locations Database |
| Time Phases | Multi-select | Πρωί, Απόγευμα, Βράδυ, Νύχτα |
| Status | Select | Idea, Draft, Written, Implemented, Tested |
| Priority | Number | 1-10 |
| One-Time | Checkbox | |
| Tags | Multi-select | ambient, event, character, quest, tutorial, etc. |
| NPCs Involved | Relation | → NPCs Database |
| Flags Required | Relation | → Flags Database |
| Flags Set | Relation | → Flags Database |
| Content Preview | Text | First 200 chars |
| Full JSON | Text | Complete storylet JSON |
| Notes | Text | Design notes |
| Created | Created time | |
| Updated | Last edited time | |

**Views:**
- By Location (Board grouped by Location)
- By Status (Kanban)
- Unimplemented (Status != Implemented, Tested)
- All (Table)

---

### NPCs Database

**Properties:**

| Property | Type | Options/Notes |
|----------|------|---------------|
| Name | Title | Display name |
| Greek Name | Text | Ελληνικό όνομα |
| ID | Text | e.g., "kyra_sofia" |
| Archetype | Select | Mentor, Rival, Friend, Authority, Victim, etc. |
| Track | Multi-select | Music, Crime, Sea, Work, Neutral |
| Primary Location | Relation | → Locations Database |
| Age | Number | |
| Origin | Select | Σμύρνη, Πειραιάς, Αϊβαλί, Κωνσταντινούπολη, etc. |
| Description | Text | Short description |
| Backstory | Text | Full backstory |
| Personality | Text | How they talk, behave |
| Schedule | Text | When they're where |
| Initial Relationship | Number | Starting relationship value |
| Historical Inspiration | Text | Real person if any |
| Portrait Status | Select | Needed, In Progress, Done |
| Implementation Status | Select | Not Started, Partial, Complete |
| Related Storylets | Relation | → Storylets Database |
| Notes | Text | |

**Views:**
- By Location
- By Track
- Needs Portrait (Portrait Status = Needed)
- All NPCs (Table)

---

### Locations Database

**Properties:**

| Property | Type | Options/Notes |
|----------|------|---------------|
| Name | Title | English name |
| Greek Name | Text | Ελληνικό όνομα |
| ID | Text | e.g., "tekes" |
| Type | Select | Hub, Path-Specific, Sub-location |
| Parent Location | Relation | → Locations (self-reference) |
| Available From | Text | Conditions or day number |
| Travel Time | Number | Minutes from camp |
| Danger Level | Number | 0-10 |
| Description | Text | |
| Hotspots | Text | List of interactive hotspots |
| Art Status | Select | Needed, Concept, In Progress, Final |
| Variants Needed | Multi-select | Day, Night, Dawn, Rain, etc. |
| Related NPCs | Relation | → NPCs Database |
| Related Storylets | Relation | → Storylets Database |
| Notes | Text | |

**Views:**
- By Type
- Art Pipeline (grouped by Art Status)
- All Locations

---

### Songs Database

**Properties:**

| Property | Type | Options/Notes |
|----------|------|---------------|
| Title | Title | Greek title |
| Title (Latin) | Text | Transliteration |
| ID | Text | e.g., "fragkosyriani" |
| Dromos | Select | Ραστ, Χιτζάζ, Σαμπάχ, Χουζάμ, Νιαβέντ, etc. |
| Tempo | Select | Αργό, Μέτριο, Γρήγορο |
| Mood Tags | Multi-select | Χαρά, Λύπη, Ντέρτι, Νοσταλγία, etc. |
| Theme Tags | Multi-select | Αγάπη, Ξενιτιά, Φυλακή, Χασίς, Θάνατος, etc. |
| Era | Select | 1920s, 1930s, 1940s |
| Taught By | Relation | → NPCs Database |
| Learning Conditions | Text | JSON or description |
| Performance Effects | Text | What happens when played |
| Lyrics (Sample) | Text | First verse |
| Kounadis ID | Text | Reference to Kounadis DB |
| Audio Link | URL | |
| Implementation Status | Select | Not Started, Implemented, Tested |
| Notes | Text | |

**Views:**
- By Dromos
- By Theme
- Learnable Songs
- All Songs

---

### Flags Database

**Properties:**

| Property | Type | Options/Notes |
|----------|------|---------------|
| Flag Name | Title | e.g., "met_dimitris" |
| Description | Text | What this flag means |
| Category | Select | Story, Met, Choice, Item, Quest, System |
| Default Value | Checkbox | Usually false |
| Set By | Relation | → Storylets Database |
| Checked By | Relation | → Storylets Database |
| Notes | Text | |

**Views:**
- By Category
- All Flags

---

### Historical Research Database

**Properties:**

| Property | Type | Options/Notes |
|----------|------|---------------|
| Topic | Title | |
| Era | Multi-select | 1920s, 1930s, 1940s |
| Category | Select | Economy, Society, Music, Crime, Daily Life, Politics |
| Source | Text | Where this info came from |
| Content | Text | The research content |
| Key Facts | Text | Bullet points |
| Game Use | Text | How this could be used |
| Tags | Multi-select | |
| Related NPCs | Relation | → NPCs Database |
| Related Locations | Relation | → Locations Database |
| Used In | Relation | → Storylets Database |

**Views:**
- By Category
- By Era
- Unused Research

---

### Asset Trackers (Backgrounds, Portraits, Audio)

**Common Properties:**

| Property | Type | Options/Notes |
|----------|------|---------------|
| Name | Title | |
| Status | Select | Needed, In Progress, Review, Done |
| Priority | Select | P0, P1, P2, P3 |
| Related To | Relation | → Locations or NPCs |
| Variants | Multi-select | |
| File Link | URL | Link to file |
| Prompt Used | Text | For AI-generated art |
| Notes | Text | |

---

## Dashboard Template

The main dashboard should include:

### Header
- Project title and one-line description
- Current phase indicator
- Key metrics (storylets written, NPCs defined, etc.)

### This Week
- Embedded view of current sprint tasks
- Focus areas

### Quick Links
- Link to each major database
- Link to design docs

### Progress Tracker
- Phase 0 checklist
- Phase 1 checklist (collapsed)
- etc.

### Recent Activity
- Recently edited storylets
- Recently added NPCs
- Recent research

---

## Templates

### Storylet Template
When creating a new storylet entry:
```
ID: [location]_[category]_[descriptor]
Title:
Location:
Time Phases:
Priority: 5
Tags:

Content Preview:


Full JSON:
{
  "id": "",
  "location": "",
  "time": [],
  "conditions": {},
  "content": {
    "type": "simple",
    "text": ""
  },
  "choices": [],
  "tags": [],
  "priority": 5,
  "one_time": false
}

Notes:
```

### NPC Template
```
Name:
Greek:
ID:

Archetype:
Track:
Location:
Age:
Origin:

Description (1-2 sentences):


Backstory:


Personality & Speech:


Schedule:


Historical Inspiration:


Notes:
```

### Weekly Sprint Template
```
# Week of [Date]

## Focus
-

## Goals
- [ ]
- [ ]
- [ ]

## Tasks
[Embedded filtered view from Tasks database]

## Blockers
-

## Notes


## Retrospective (end of week)
### What went well

### What didn't

### Learnings

```

---

## Usage with Claude Code

Once the MCP server is configured and pages are shared, you can use commands like:

```
"Show me all storylets for the tekes location"

"Create a new NPC entry for a dock worker named Leonidas"

"Update the status of storylet tekes_ambient_01 to 'Written'"

"What tasks are in the current sprint?"

"Add a new research entry about hashish den rituals"
```

Claude Code will use the Notion MCP to execute these operations directly.
