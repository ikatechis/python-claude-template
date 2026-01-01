# Art Guide

> **Version:** 2.0 | **Status:** Draft | **Updated:** 2025-01-15
> **Depends on:** DESIGN.md
> **Dependents:** All visual assets

---

## Overview

The game uses **high-detail 16-bit pixel art** in the style of modern point-and-click adventures like *Norco*, *Signalis*, and the reference image (Grok-generated tekes scene). The aesthetic combines 1930s Greek atmosphere with pixel art's capacity for atmospheric dithering, limited palettes, and nostalgic warmth.

**Key references:**
- 1930s Greek documentary photography
- Film noir lighting
- Toulouse-Lautrec's café scenes (composition, intimacy)
- *Norco*, *Signalis*, *VA-11 Hall-A* (pixel art mood)

---

## Visual Principles

### 1. Atmospheric Over Detailed

Smoke, shadow, and light matter more than sharp detail. Dithering creates atmosphere. Let the eye fill in what the pixels suggest.

### 2. Warm Interiors, Cool Exteriors

- Interiors (tekes, koutouki, shacks): amber, brown, cream
- Exteriors day: muted earth tones, grey-blue sky
- Exteriors night: deep blue, amber lamp pools, noir shadows

### 3. No People in Background Art

Generate locations empty. Characters are separate sprite layers composited in Godot. This allows:
- Reuse of backgrounds
- Character animation independence
- State changes (same room, different time)

### 4. Evidence of Life

Empty doesn't mean sterile. Show recent presence:
- Half-drunk wine glass
- Smoldering cigarette
- Instrument leaning on chair
- Warm coals in narghile
- Unmade bed, worn path, abandoned cart

### 5. Period Accuracy

Critical details that AI often gets wrong:
- **Bouzouki:** Round body (not modern teardrop), three double strings (trichordo), mother-of-pearl inlay
- **Baglamas:** Small bouzouki, often handmade, simple
- **Clothing:** Flat caps for workers, fedoras for manges, no modern cuts
- **Lighting:** Oil lamps, kerosene, early electric (large bulbs, visible filament)
- **No modern elements:** No plastic, no neon, no cars (rare, period-appropriate only)

---

## Color Palettes

### Master Palette

All location palettes are subsets of this master palette to ensure visual consistency across the game.

#### Warm Tones (Interiors, Night, Lamps)
| Name | Hex | Use |
|------|-----|-----|
| Deep Shadow | #1A1410 | Darkest interior shadows |
| Dark Brown | #3D2817 | Wood, dark areas |
| Warm Brown | #5C3D2E | Furniture, walls |
| Medium Brown | #8B5A2B | Skin shadow, wood grain |
| Amber | #D4A559 | Lamp light, warm glow |
| Gold | #E8C872 | Highlights, brass |
| Warm Cream | #F5DEB3 | Light areas, smoke |
| Hot Ember | #B84C28 | Narghile coal, fire |

#### Cool Tones (Exteriors, Day, Sea)
| Name | Hex | Use |
|------|-----|-----|
| Night Black | #0D1117 | Night sky, deep shadow |
| Deep Blue | #1E3A5F | Night sky, sea (night) |
| Slate Blue | #4A5568 | Overcast sky, stone |
| Cool Grey | #6B7280 | Concrete, cloudy day |
| Sea Grey | #8BA5B5 | Harbor water, morning |
| Pale Blue | #B8D4E8 | Dawn sky, reflections |
| Fog White | #E8EEF2 | Mist, overcast light |

#### Earth Tones (Exteriors, Poverty, Dust)
| Name | Hex | Use |
|------|-----|-----|
| Mud Black | #1C1612 | Deep earth shadow |
| Earth Brown | #4A3728 | Mud, dirt |
| Dust Brown | #7D6449 | Dry earth, paths |
| Rust | #A65D3F | Corroded tin, old iron |
| Ochre | #C9A66B | Sunlit stone, sand |
| Pale Dust | #D9CDBF | Dusty surfaces, haze |

#### Accent Tones (Fabric, Details)
| Name | Hex | Use |
|------|-----|-----|
| Deep Red | #6B2D3A | Curtains, wine, blood |
| Faded Red | #8B4C5A | Old fabric, worn rugs |
| Olive Green | #4A5A3C | Military, vegetation |
| Faded Green | #6B7D5A | Old paint, plants |
| Ink Blue | #2C3E5A | Dark fabric, night cloth |
| White (Dirty) | #D8D4CB | Shirts, tablecloths |

---

## Location-Specific Palettes

### Tekes (Underground Hashish Den)

**Mood:** Intimate, illicit, warm, smoky, sacred

**Primary palette:**
- Deep Shadow (#1A1410)
- Dark Brown (#3D2817)
- Warm Brown (#5C3D2E)
- Amber (#D4A559)
- Warm Cream (#F5DEB3)
- Hot Ember (#B84C28) — for narghile coals

**Lighting:** Single or few oil lamps, warm amber glow, heavy shadows, upper half of room lost in smoke

**Key elements:**
- Cracked plaster walls with damp stains
- Rush-seated wooden chairs
- Low brass tables
- Narghile (water pipe)
- Oriental rugs (faded reds, worn)
- Hanging oil lamps
- No windows (underground)

---

### Refugee Camp (1922)

**Mood:** Desolate, grey, melancholy, resilient, makeshift

**Primary palette:**
- Mud Black (#1C1612)
- Earth Brown (#4A3728)
- Dust Brown (#7D6449)
- Rust (#A65D3F)
- Cool Grey (#6B7280)
- Fog White (#E8EEF2)
- Pale Dust (#D9CDBF)

**Lighting:** Overcast, flat grey light, occasional cooking fire warmth

**Key elements:**
- Shacks of scrap wood, flattened kerosene tins, canvas
- Muddy paths with wooden planks
- Laundry lines
- Cooking fires, smoke rising
- Children's abandoned toys
- Distant harbor/ships
- Church dome silhouette

---

### Piraeus Port

**Mood:** Industrial, maritime, dawn hope, night danger

**Dawn palette:**
- Night Black (#0D1117) — fading
- Deep Blue (#1E3A5F) — sky
- Pale Blue (#B8D4E8) — horizon
- Sea Grey (#8BA5B5) — water
- Amber (#D4A559) — distant lamps
- Cool Grey (#6B7280) — stone quay

**Day palette:**
- Slate Blue (#4A5568) — sky
- Sea Grey (#8BA5B5) — water
- Ochre (#C9A66B) — sunlit stone
- Warm Brown (#5C3D2E) — crates, wood
- Rust (#A65D3F) — metal, cranes

**Night palette:**
- Night Black (#0D1117)
- Deep Blue (#1E3A5F)
- Amber (#D4A559) — lamp pools
- Warm Brown (#5C3D2E) — crates in light
- Deep Shadow (#1A1410) — noir shadows

**Key elements:**
- Stone quay, iron bollards
- Coiled ropes, wooden crates (Greek lettering)
- Cargo ships, masts, rigging
- Warehouses
- Cranes (period-appropriate)
- Wet cobblestones (reflections)
- Handcarts, cargo nets

---

### Piraeus Streets & Neighborhoods

**Mood:** Varied — lively markets, dangerous alleys, working-class residential

**Market/Day palette:**
- Ochre (#C9A66B) — sunlit walls
- Warm Cream (#F5DEB3) — awnings, light
- Faded Red (#8B4C5A) — awnings, fabric
- Olive Green (#4A5A3C) — vegetables, shutters
- Warm Brown (#5C3D2E) — wood, carts
- Dust Brown (#7D6449) — street

**Alley/Night palette:**
- Night Black (#0D1117)
- Deep Shadow (#1A1410)
- Deep Blue (#1E3A5F) — sky sliver
- Amber (#D4A559) — single lamp
- Warm Brown (#5C3D2E) — walls in light

**Key elements:**
- Narrow streets, high buildings
- Balconies with laundry
- Market stalls, awnings
- Vendor carts
- Doorways recessed in shadow
- Streetlamps (gas or early electric)
- Stray cats
- Greek signage

---

### Café-Aman (Legal Music Venue)

**Mood:** More respectable than tekes, still smoky, performance space, Smyrna elegance faded

**Primary palette:**
- Dark Brown (#3D2817)
- Warm Brown (#5C3D2E)
- Amber (#D4A559)
- Warm Cream (#F5DEB3)
- Deep Red (#6B2D3A) — curtains
- Faded Red (#8B4C5A) — upholstery
- Gold (#E8C872) — mirror frames, details

**Lighting:** Electric lights (still dim), warmer than modern, spotlight on stage

**Key elements:**
- Small round tables, white tablecloths
- Bentwood chairs
- Small stage with curtain
- Mirrors on walls
- Bar with bottles
- 1930s microphone on stand
- More formal than tekes, less intimate

---

### Koutouki (Basement Tavern)

**Mood:** Working-class, rough, cheap wine, simpler than tekes

**Primary palette:**
- Deep Shadow (#1A1410)
- Earth Brown (#4A3728)
- Warm Brown (#5C3D2E)
- Amber (#D4A559) — single lamp
- Pale Dust (#D9CDBF) — whitewash

**Lighting:** Dim, single oil lamp, stone walls absorb light

**Key elements:**
- Low ceiling, exposed beams
- Stone walls, whitewashed but stained
- Simple wooden tables and benches
- Wine barrels along wall
- Crude bar (plank on barrels)
- Tin cups, chalked price sign
- Steep narrow stairs down

---

### Vourla District (Brothel Area)

**Mood:** Danger, exploitation, red light, noir, moral ambiguity

**Primary palette:**
- Night Black (#0D1117)
- Deep Shadow (#1A1410)
- Deep Red (#6B2D3A) — key accent
- Faded Red (#8B4C5A) — fabric, curtains
- Amber (#D4A559) — lamps, windows
- Ink Blue (#2C3E5A) — night cloth, shadows

**Lighting:** Pools of red and amber from windows, deep shadows between

**Key elements:**
- Narrow streets
- Lit windows with curtains
- Doorways with women's silhouettes (implied, not explicit)
- Drunk sailors
- Police presence (sometimes)
- Cheap hotels, signs
- Danger in shadows

---

### Athens — Wealthy Neighborhoods (Kolonaki, Plaka)

**Mood:** Another world — clean, neoclassical, the establishment, contrast to Piraeus

**Primary palette:**
- Fog White (#E8EEF2) — neoclassical buildings
- Pale Blue (#B8D4E8) — sky
- Ochre (#C9A66B) — sunlit stone
- Olive Green (#4A5A3C) — shutters, trees
- Faded Green (#6B7D5A) — patina on bronze
- Ink Blue (#2C3E5A) — formal clothing
- Gold (#E8C872) — details, wealth

**Lighting:** Cleaner, brighter, daylight scenes, gas lamps at night

**Key elements:**
- Neoclassical buildings, columns
- Wide streets, sidewalks
- Cafés with outdoor seating
- Well-dressed people (implied through objects)
- Acropolis visible in distance
- Clean cobblestones
- Ornate lampposts
- Contrast: the player doesn't belong here

---

### Athens — Working-Class Neighborhoods (Metaxourgeio, Kerameikos)

**Mood:** Urban poverty, factories, closer to Piraeus feel, transitional

**Primary palette:**
- Earth Brown (#4A3728)
- Dust Brown (#7D6449)
- Rust (#A65D3F)
- Cool Grey (#6B7280)
- Slate Blue (#4A5568)
- Pale Dust (#D9CDBF)

**Lighting:** Industrial, overcast, factory smoke, less warmth than Piraeus

**Key elements:**
- Factory buildings, chimneys with smoke
- Workers' housing, cramped
- Fewer trees, more concrete
- Railway lines
- Small workshops
- Political posters on walls
- Different feel than Piraeus — industrial vs. maritime

---

### Averoff Prison

**Mood:** Institutional, oppressive, cold, grey, despair with small human touches

**Primary palette:**
- Cool Grey (#6B7280) — dominant
- Slate Blue (#4A5568) — walls
- Night Black (#0D1117) — shadows
- Fog White (#E8EEF2) — harsh light
- Faded Green (#6B7D5A) — institutional paint
- Rust (#A65D3F) — bars, old metal

**Lighting:** Harsh, flat, institutional, no warmth

**Key elements:**
- High stone walls
- Barred windows
- Guard towers
- Heavy iron gates
- Visiting room with wire mesh divider
- Cells with scratched walls, counting marks
- Human touches: photograph, book, scratched name

---

### Rooftops

**Mood:** Solitude, contemplation, urban poetry, where songs are born

**Night palette:**
- Night Black (#0D1117)
- Deep Blue (#1E3A5F) — sky
- Amber (#D4A559) — windows below
- Warm Brown (#5C3D2E) — rooftop surfaces
- Pale Blue (#B8D4E8) — stars, moonlight

**Key elements:**
- Flat roofs (Mediterranean style)
- Water tanks
- Laundry lines
- Chimneys
- City lights below (scattered amber)
- Harbor and ship lights in distance
- Stars visible (less light pollution)
- The sea on the horizon

---

## Shot Types Per Location

Each location needs multiple shots:

| Shot Type | Purpose | Example |
|-----------|---------|---------|
| **Wide/Master** | Establishing, main gameplay | Full tekes interior |
| **Detail** | Hotspots, interactions | The narghile table |
| **Transition** | Entering/exiting | Stairs down to koutouki |
| **Variant - Time** | Different atmosphere | Port at dawn vs. night |
| **Variant - State** | Story changes | Tekes after police raid |

Minimum for vertical slice: 3-5 shots per major location.

---

## Standard Prompt Structure

Use this prefix for all prompts to maintain consistency:

```
Pixel art, 16-bit style, detailed dithering, point-and-click adventure game. 1930s Greece. No people. [LOCATION AND SCENE DESCRIPTION]. [PALETTE GUIDANCE]. [MOOD]. Point-and-click adventure game style.
```

### Example:

```
Pixel art, 16-bit style, detailed dithering, point-and-click adventure game. 1930s Greece. No people. Interior of underground tekes, low vaulted ceiling, cracked plaster walls. Wooden chairs with rush seats arranged in circle. Hanging oil lamps casting amber glow. Narghile on brass table, coal glowing. Oriental rug on stone floor. Thick smoke in upper half of room. Warm palette: dark browns, amber, cream. Atmospheric, intimate, sacred. Point-and-click adventure game style.
```

---

## Consistency Techniques

### 1. Session Batching
Generate all shots for one location in a single session. AI maintains some consistency within a session.

### 2. Reference Image Input
Use your best output as reference for subsequent generations (Grok supports this).

### 3. Locked Prompt Prefix
Never change the style prefix. Only change scene description.

### 4. Post-Processing
- Adjust all images to match the defined hex palettes
- Use a palette-matching tool or do manually in Aseprite/Photoshop
- Apply same dithering pattern if AI varies

### 5. Color Correction Script
Consider a Python script that maps AI output colors to nearest palette color for perfect consistency.

---

## Animation Approach

### Backgrounds
Static images with subtle ambient animation:
- Smoke particles (Godot GPUParticles2D)
- Lamp flicker (light energy variation)
- Gentle parallax on layers (foreground/midground/background)

### Characters
Separate sprite sheets, not part of backgrounds:
- Idle: 4 frames
- Walk: 6 frames
- Talk: 4 frames
- Special actions: as needed

### Minimal Viable Animation
For vertical slice, acceptable to have:
- Static backgrounds + particles
- Characters appear/disappear (no walk animation)
- 2-3 expression variants per portrait

---

## Asset Naming Convention

```
[location]_[shot]_[variant]_[version].png

Examples:
tekes_wide_night_v1.png
tekes_wide_raid_v1.png
tekes_detail_narghile_v1.png
port_wide_dawn_v2.png
camp_interior_shack_v1.png
```

---

## File Organization

```
art_pipeline/
├── prompts/
│   ├── tekes_prompts.md
│   ├── port_prompts.md
│   └── ...
├── references/
│   ├── historical/          # 1930s photos
│   ├── style/               # Pixel art references
│   └── best_outputs/        # Best AI outputs to reuse
├── outputs/
│   ├── raw/                 # Direct from AI
│   └── processed/           # Color-corrected, final
└── sprites/
    ├── characters/
    └── ui/
```

---

## Historical Reference Sources

- **Kounadis Archive** — Photos of musicians, venues
- **Benaki Museum** — 1920s-30s Greek photography
- **ELIA Archives** — Refugee camp documentation
- **Petropoulos books** — Rebetiko culture photography
- **Greek Film Archive** — 1930s Greek cinema stills

---

## Quality Checklist

Before finalizing any asset:

- [ ] Colors match defined palette (or close)
- [ ] No modern elements (plastic, neon, wrong clothing)
- [ ] Bouzouki is correct (round body, three strings)
- [ ] Lighting is consistent with location type
- [ ] Dithering style matches other assets
- [ ] No people in background (unless intentional crowd silhouette)
- [ ] Mood matches location description
- [ ] Named correctly and in right folder
