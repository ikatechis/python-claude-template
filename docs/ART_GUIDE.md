---
status: draft
version: 1.0.0
last_updated: 2025-01-01
---

# Art Guide & Prompt Engineering

---

## Visual Identity

### Core Aesthetic

The game's visual style should evoke:
- **1930s Greek photography** — High contrast, grainy, documentary feel
- **Film noir** — Strong shadows, limited light sources, smoke
- **Toulouse-Lautrec** — Stylized figures, warm interiors, café culture
- **Greek shadow theater (Karagiozis)** — Flat, expressive, theatrical

We are NOT going for:
- Pixel-perfect realism
- Bright, saturated colors
- Clean, modern aesthetics
- Generic "Mediterranean" look

### Color Palette

**Primary palette:**
```
Background browns:   #3D2914, #5C4033, #8B7355
Warm ambers:         #D4A574, #C4956A, #E8C39E
Deep blues:          #1A2744, #2C3E50, #34495E
Smoke greys:         #7F8C8D, #95A5A6, #BDC3C7
Blood/wine reds:     #722F37, #8B0000, #A52A2A (sparingly)
```

**Lighting conditions:**
- **Daylight:** Harsh, washed out, high contrast
- **Oil lamp:** Warm amber, strong shadows, limited reach
- **Night exterior:** Deep blue, moonlight silver, danger
- **Smoke-filled:** Diffused, hazy, dreamlike

### Typography (If Used)

- **Greek text:** Period-appropriate fonts (Didot-style)
- **UI text:** Clean, readable, minimal
- **Signs/posters:** Hand-painted aesthetic

---

## Historical Accuracy Reference

### The Problem with AI Image Generation

AI models don't know:
- What a 1930s bouzouki looks like (they'll generate mandolins or modern bouzoukis)
- How a mangas dressed (they'll default to generic "Greek" or "Mediterranean")
- Interior details of a tekes (they'll generate Turkish hookah bars)
- The specific poverty of Piraeus (they'll generate picturesque poverty)

### Solution: Reference-Based Prompting

Always include:
1. **Positive descriptors** (what IS there)
2. **Negative descriptors** (what is NOT there)
3. **Style anchors** (artistic references)
4. **Historical anchors** (era-specific details)

---

## Instrument Reference

### Bouzouki (Trichordo) — 1930s

**CRITICAL:** The 1930s bouzouki is different from the modern instrument.

**Correct features:**
- Three courses (pairs of strings), not four
- Round, gourd-shaped body (like half a watermelon)
- Long, thin neck
- Small sound hole
- Often decorated with mother-of-pearl

**Incorrect features to EXCLUDE:**
- Four courses (modern tetrachordo)
- Flat-backed body
- Electric pickups
- Modern tuning pegs

**Prompt fragment:**
```
trichordo bouzouki, three-stringed, round gourd-shaped body,
long thin neck, wooden, mother-of-pearl inlay, 1930s Greek instrument
--no four strings, no flat back, no electric, no guitar, no mandolin
```

### Baglamas

- Tiny bouzouki (40cm total length)
- Same shape as bouzouki, just smaller
- Could be hidden in a coat
- Often homemade, crude construction

**Prompt fragment:**
```
baglamas, tiny Greek stringed instrument, miniature bouzouki,
crude wooden construction, three strings, fits in a pocket
--no full-size, no guitar
```

### Other Instruments

- **Guitar:** Spanish/classical style, nylon strings, NOT steel-string acoustic
- **Violin:** Standard, but held against chest (folk style), not under chin
- **Santuri:** Hammered dulcimer, trapezoidal, not present in most scenes

---

## Clothing Reference

### Male — Mangas (Underworld)

**1930s mangas look:**
- **Hat:** Fedora (kavouraki), tilted
- **Jacket:** Suit jacket, often worn loose (one arm out "Sultana style")
- **Shirt:** Collarless or soft collar, often open at neck
- **Trousers:** High-waisted, pleated, pegged at ankle
- **Shoes:** Polished leather shoes or barefoot
- **Accessories:** Worry beads (komboloi), cigarette

**Prompt fragment:**
```
1930s Greek mangas, fedora hat tilted, suit jacket worn loose,
collarless shirt open at neck, high-waisted trousers,
polished shoes, worry beads, cigarette, mustache
--no t-shirt, no jeans, no modern clothes, no sneakers
```

### Male — Worker (Dock/Factory)

- **Hat:** Flat cap (tragiaska)
- **Shirt:** Collarless work shirt, rolled sleeves
- **Vest:** Often worn over shirt
- **Trousers:** Worn, patched, rope belt
- **Shoes:** Worn leather or barefoot

**Prompt fragment:**
```
1930s Greek dock worker, flat cap, collarless work shirt,
rolled sleeves, vest, worn trousers with rope belt,
weathered face, calloused hands, poor but dignified
--no modern workwear, no hard hat, no safety vest
```

### Female — Poor/Refugee

- **Head:** Black headscarf (mandatory for married/older)
- **Dress:** Long, dark, simple
- **Apron:** Practical, worn
- **Shoes:** Simple leather or barefoot

### Female — Singer/Performer

- **Hair:** Uncovered, styled (scandalous for the era)
- **Dress:** More western, fitted
- **Makeup:** Visible (also scandalous)
- **Accessories:** Jewelry, cigarette holder

**Prompt fragment:**
```
1930s Greek female singer, cabaret style, western dress,
styled dark hair, red lipstick, confident pose,
cigarette holder, jewelry, performer
--no headscarf, no traditional dress
```

---

## Location Reference

### Tekes (Hash Den) Interior

**Correct features:**
- Basement or back room, hidden
- Oil lamps (gkazi), not electric
- Rush chairs or cushions on floor, not regular furniture
- Hookah (argile) with coconut or glass base, bamboo stem
- Kilim rugs, worn
- Brick or plaster walls, peeling
- Smoke haze
- Men in circle, passing pipe
- Musicians in corner

**Incorrect features:**
- Electric lights
- Modern furniture
- Turkish/ornate hookahs
- Women (rare in tekes)
- Clean/tidy appearance

**Prompt fragment:**
```
1930s Greek hashish den interior, tekes, basement room,
oil lamp lighting, rush chairs, men sitting in circle,
hookah with coconut base, smoke haze, kilim rugs on floor,
peeling plaster walls, bouzouki player in corner,
amber and brown tones, noir lighting
--no electric lights, no ornate furniture, no turkish style,
--no bright colors, no clean surfaces, no modern elements
```

### Refugee Camp (1922)

**Correct features:**
- White canvas tents in rows
- Muddy ground
- Cooking fires
- Makeshift shelters with tin/wood
- Red Cross tent
- Masses of people
- Laundry hanging
- Sea visible in background

**Prompt fragment:**
```
1922 Greek refugee camp, Smyrna catastrophe, white tents in rows,
muddy ground, cooking fires, desperate people, overcrowded,
Red Cross tent, laundry hanging, Piraeus harbor in background,
documentary photography style, black and white tinted sepia
--no modern tents, no clean conditions, no tourists
```

### Port of Piraeus

**Correct features:**
- Large cargo ships
- Wooden crates, ropes, barrels
- Stone quay
- Workers in period clothing
- Tavernas with outdoor seating
- Fish market stalls
- Donkey carts
- Industrial smoke

**Prompt fragment:**
```
1930s Piraeus port Greece, cargo ships, wooden crates,
dock workers in flat caps, stone quay, industrial,
busy crowded scene, fish market stalls, taverna,
muted colors, documentary style, working class
--no modern ships, no containers, no cars, no tourists
```

---

## Prompt Templates

### Character Portrait

```
[CHARACTER DESCRIPTION], 1930s Greece, portrait,
[CLOTHING DETAILS], [EXPRESSION],
painted style, muted palette, amber lighting,
period accurate, Toulouse-Lautrec influence
--no modern elements, no bright colors, no photorealistic
```

**Example:**
```
Greek male musician age 20, thin face, dark eyes,
slight mustache, 1930s Greece, portrait,
fedora hat, collarless shirt, jacket on shoulders,
contemplative expression, holding bouzouki,
painted style, muted palette, amber lighting,
period accurate, Toulouse-Lautrec influence
--no modern elements, no bright colors, no photorealistic
```

### Location Background

```
[LOCATION], 1930s Piraeus Greece, interior/exterior,
[LIGHTING], [ATMOSPHERE], [KEY DETAILS],
painted style, wide shot, point and click game background,
muted palette, [MOOD]
--no modern elements, no tourists, no bright colors
```

**Example:**
```
Greek tekes hashish den, 1930s Piraeus Greece, interior,
oil lamp lighting, smoky atmosphere,
men sitting on floor cushions, hookah, musicians corner,
painted style, wide shot, point and click game background,
muted palette, noir mood, amber and brown tones
--no modern elements, no electric lights, no bright colors
```

### Scene Illustration

```
[SCENE DESCRIPTION], 1930s Piraeus Greece,
[CHARACTERS], [ACTION], [LOCATION],
cinematic composition, strong shadows,
painted illustration style, muted palette
--no modern elements, no bright colors
```

---

## Grok-Specific Tips

Based on working experience with Grok:

### What Works
- Detailed, specific prompts
- Historical era specification ("1930s Greece")
- Style anchors ("painted style," "documentary photography")
- Negative prompts ("--no modern elements")
- Reference images uploaded with "in this style"

### What Doesn't Work
- Vague descriptions
- Just saying "bouzouki" (gets mandolins)
- Expecting it to know Greek-specific terms
- Bright/colorful palette requests

### Iterative Refinement Process

1. Generate with basic prompt
2. Identify errors (wrong instrument, wrong clothing, etc.)
3. Add specific corrections to negative prompt
4. Add more detail to positive prompt
5. Regenerate
6. Repeat until acceptable
7. Document working prompt in `/art_pipeline/prompts/`

---

## ComfyUI Integration (Future)

### Planned Workflow

1. **Concept Phase (Current):** Grok for exploration
2. **Style Lock:** Choose 5-10 best images as style reference
3. **LoRA Training:** Train custom LoRA on reference images
4. **Production Pipeline:**
   - Base generation with custom LoRA
   - ControlNet for pose consistency
   - Img2img for variants
   - Batch generation for efficiency

### ControlNet Uses
- **Pose:** Character consistency across expressions
- **Depth:** Background perspective consistency
- **Canny:** Maintaining composition from sketches

### Image Size Standards
- **Backgrounds:** 1920x1080 (16:9)
- **Portraits:** 512x768 (2:3)
- **Items:** 256x256 (1:1)
- **UI elements:** Variable

---

## File Naming Convention

```
[category]_[location/character]_[variant]_[version].png

backgrounds/tekes_main_night_v2.png
characters/dimitris_portrait_happy_v1.png
items/bouzouki_panagis_v1.png
ui/button_choice_default.png
```

---

## Quality Checklist

Before finalizing any art asset:

- [ ] Period-appropriate clothing?
- [ ] Correct instruments (if any)?
- [ ] Correct lighting for setting?
- [ ] No modern elements visible?
- [ ] Consistent with established palette?
- [ ] Correct file format and size?
- [ ] Documented prompt in `/art_pipeline/prompts/`?

---

## Reference Image Sources

Build reference library from:
- Kounadis Archive photographs
- Greek National Film Archive
- Benaki Museum Digital Collections
- ELIA (Hellenic Literary and Historical Archive)
- Personal research photographs

Store in `/art_pipeline/references/` organized by category.
