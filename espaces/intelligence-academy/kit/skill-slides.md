# PPTX Design — Intelligence Academy Slide Design System

You are a PowerPoint slide design expert for Intelligence Academy training modules. When generating slides via `python-pptx`, apply this design system strictly. Slides are created **from scratch** (blank slides + shapes), NOT cloned from a template.

## Trigger

Activate this skill whenever:
- Generating PowerPoint slides with `python-pptx`
- Editing any `generate_module*.py` script in `docs/formations/slides/`
- The user asks to create, improve, or audit presentation slides

## Reference Implementation

**Always read an existing script first** before generating slides. The reference scripts are in `docs/formations/slides/generate_module*.py`. Copy the exact same helper functions and patterns — do not reinvent.

## Slide Canvas

- **Dimensions:** 13.333" × 7.5" (standard 16:9)
- **Safe margins:** 0.7" from left/right, 0.2" from top
- **Full width:** `Inches(13.333)`, full height: `Inches(7.5)`
- **Content width:** `Inches(11.5)` (from left 0.7")

```python
W = Inches(13.333)
H = Inches(7.5)
```

## Color Palette

```python
C_HEADER_LEFT  = RGBColor(0x0A, 0x25, 0x30)  # Dark blue-green (header gradient left)
C_HEADER_RIGHT = RGBColor(0x1E, 0x55, 0x65)  # Teal (header gradient right)
C_GOLD         = RGBColor(0xE8, 0xA0, 0x00)  # Gold accent — labels, lines, highlights
C_WHITE        = RGBColor(0xFF, 0xFF, 0xFF)
C_BLACK        = RGBColor(0x00, 0x00, 0x00)
C_TITLE        = RGBColor(0x1A, 0x1A, 0x1A)  # Near-black for titles
C_BODY         = RGBColor(0x33, 0x33, 0x33)  # Dark gray for body text
C_TEAL         = RGBColor(0x1B, 0x5E, 0x6B)  # Teal for numbered items, accents
C_TEAL_LIGHT   = RGBColor(0x5A, 0x8A, 0x8F)  # Light teal for subtitles, durations
C_DARK_BLUE    = RGBColor(0x0F, 0x2B, 0x3A)  # Full dark bg for recap/cover/transition slides
C_GRAY_BG      = RGBColor(0xED, 0xED, 0xED)  # Light gray for card backgrounds
```

**Usage rules:**
- `C_GOLD` = the accent. Used for: labels ("MODULE 1"), separator lines, "À retenir" titles, footer brand, step numbers, accent strips. Works because it's rare.
- `C_DARK_BLUE` = full background for cover, lesson transitions, recap, questions slides. Creates visual contrast with white-background content slides.
- `C_HEADER_LEFT` + `C_HEADER_RIGHT` = simulated gradient for the standard header bar.
- `C_TEAL` / `C_TEAL_LIGHT` = secondary accent for numbered items, durations, annotations.
- Never use pure `#083851` alone as the palette — that was the old approach. Use the full palette above.

## Typography

**Single font family:** `Bricolage Grotesque` for everything. Differentiate via size + weight + color.

| Role | Size | Weight | Color |
|------|------|--------|-------|
| Cover title | 52pt | Bold | `C_WHITE` |
| Header title | 36pt | Bold | `C_WHITE` |
| Subtitle | 28pt | Bold | `C_TITLE` |
| Body text | 18-20pt | Regular | `C_BODY` |
| Exercise steps | 17pt | Regular | `C_BODY` |
| Annotations / tips | 16pt | Regular | `C_TEAL` |
| Footer brand | 13-14pt | Bold | `C_GOLD` |

**Rules:**
- One font (`Bricolage Grotesque`) — hierarchy comes from size + weight + color, not font mixing.
- Minimum text: 14pt (footer), 16pt (annotations), 17pt (body content).
- `space_before = Pt(4-10)` between paragraphs for breathing room.

## Helper Functions (copy from reference)

Every `generate_module*.py` script MUST include these core helpers:

```python
def new_prs():
    prs = Presentation()
    prs.slide_width = W
    prs.slide_height = H
    return prs

def blank_slide(prs):
    return prs.slides.add_slide(prs.slide_layouts[6])  # completely blank

def add_rect(slide, left, top, width, height, fill_color=None):
    shape = slide.shapes.add_shape(1, left, top, width, height)
    shape.line.fill.background()  # no border
    if fill_color:
        shape.fill.solid()
        shape.fill.fore_color.rgb = fill_color
    return shape

def add_textbox(slide, left, top, width, height, text, font_name=FONT,
                font_size=18, bold=False, color=C_BODY, align=PP_ALIGN.LEFT,
                word_wrap=True):
    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf = txBox.text_frame
    tf.word_wrap = word_wrap
    p = tf.paragraphs[0]
    p.alignment = align
    run = p.add_run()
    run.text = text
    run.font.name = font_name
    run.font.size = Pt(font_size)
    run.font.bold = bold
    run.font.color.rgb = color
    return txBox, tf

def add_header(slide, title_text):
    """Standard header: gradient rect (2 halves) + gold line + white title."""
    add_rect(slide, Inches(0), Inches(0), Inches(6.7), Inches(1.25), C_HEADER_LEFT)
    add_rect(slide, Inches(6.7), Inches(0), Inches(6.633), Inches(1.25), C_HEADER_RIGHT)
    add_rect(slide, Inches(0), Inches(1.25), Inches(13.333), Inches(0.02), C_GOLD)
    add_textbox(slide, Inches(0.7), Inches(0.2), Inches(11.5), Inches(0.9),
                title_text, font_size=36, bold=True, color=C_WHITE)

def add_subtitle(slide, text):
    add_textbox(slide, Inches(0.7), Inches(1.6), Inches(11.5), Inches(0.7),
                text, font_size=28, bold=True, color=C_TITLE)

def add_content_block(slide, top_offset, lines, font_size=18, color=C_BODY):
    """Multi-line textbox with proper paragraph spacing."""
    tb = slide.shapes.add_textbox(Inches(0.7), top_offset, Inches(11.5), Inches(5.0))
    tf = tb.text_frame
    tf.word_wrap = True
    first = True
    for line in lines:
        if first:
            p = tf.paragraphs[0]
            first = False
        else:
            p = tf.add_paragraph()
        p.space_before = Pt(6)
        run = p.add_run()
        run.text = line
        run.font.name = FONT
        run.font.size = Pt(font_size)
        run.font.color.rgb = color
    return tf

def add_logo(slide, logo_name, left, top, size=Inches(0.8)):
    path = os.path.join(LOGOS_DIR, f"{logo_name}.png")
    if os.path.exists(path):
        try:
            slide.shapes.add_picture(path, left, top, size, size)
            return True
        except:
            return False
    return False
```

## Slide Types (10 types — use the right one)

### 1. Cover Slide (`slide_cover`)
Full `C_HEADER_LEFT` background + `C_HEADER_RIGHT` lower band. Gold "MODULE N" label, large white title, light teal subtitle, gold footer.

### 2. Sommaire (`slide_sommaire`)
Standard header + list of lessons with multi-run paragraphs: teal lesson number, dark title, light teal duration. One slide for the whole module overview.

### 3. Lesson Title / Transition (`slide_lesson_title`)
Full `C_DARK_BLUE` background + gold accent strip (thin vertical bar). Gold lesson number, large white title, light teal duration + format. Creates visual break between lessons.

### 4. Content (`slide_content`)
Standard header + optional subtitle + bullet list. White background. The workhorse slide — most content goes here.

### 5. Content with Logo (`slide_content_with_logo`)
Same as content but with a large logo (1.4") positioned top-right (`Inches(11.2), Inches(2.0)`). Text area narrowed to `Inches(9.8)` when logo present.

### 6. Two Columns (`slide_two_columns`)
Standard header + two text columns separated by a gold vertical line. Left column: `Inches(0.7)`, width `Inches(5.5)`. Separator at `Inches(6.4)`. Right column: `Inches(6.7)`, width `Inches(5.8)`. Great for comparisons, pros/cons, problems/solutions.

### 7. Tools Grid (`slide_tools_grid`)
3×2 grid of gray cards, each with logo + tool name + description. `cell_w = Inches(3.8)`, `cell_h = Inches(2.0)`, gap 0.35". Perfect for presenting multiple tools/concepts at once.

### 8. Workflow Diagram (`slide_workflow`)
Horizontal row of colored boxes with logos + step numbers + arrows between them. Shows a process flow visually. Annotation text below.

### 9. Recap / "À retenir" (`slide_recap`)
Full `C_DARK_BLUE` background + gold top strip. Gold "À retenir" title, white subtitle, white bullet list. Used at the end of each lesson section.

### 10. Exercise (`slide_exercise`)
Standard header + numbered steps with multi-run paragraphs: teal step number (bold), dark body text. Used for hands-on exercises.

### 11. Questions (`slide_questions`)
Full black background, centered "Des questions ?" in 64pt white, gold footer. One per module, before the closing slide.

## Visual Rhythm — Alternating Slide Types

**Never use 3+ content slides in a row.** Break monotony with:
- Lesson transition slides (dark bg) between sections
- Recap slides (dark bg) at end of each lesson
- Tools grid or workflow diagram for visual variety
- Two-column layout for comparisons
- Content-with-logo when presenting a specific tool

**Pattern per lesson:**
```
Lesson Title (dark) → Content × 2-4 → Recap (dark)
```

**Pattern per module:**
```
Cover (dark) → Sommaire → [Lesson × N] → Questions (black) → Closing (dark)
```

## Content Writing Rules

### Bullets
- **Max 8-10 lines** per slide (including empty lines for spacing)
- Empty `""` lines create visual grouping — use them between concepts
- Lead with emoji or symbol for visual anchoring: 💡, 🎯, ✅, ❌, ⚠️, 🔄, →, •
- Quoted text for impactful phrases: `"C'est la différence entre..."`
- Indented sub-bullets with 3 spaces: `"   • Sub point here"`

### Multi-run formatting
For rich formatting within a single paragraph (e.g., teal number + dark text), use multiple `p.add_run()` calls:
```python
run_num = p.add_run()
run_num.text = "1.  "
run_num.font.color.rgb = C_TEAL
run_num.font.bold = True

run_text = p.add_run()
run_text.text = "The actual content"
run_text.font.color.rgb = C_BODY
```

## File Structure

```
docs/formations/slides/
├── generate_module01.py       # Self-contained script per module
├── generate_module02.py
├── ...
├── module-01-ecosysteme.pptx  # Generated output
├── module-02-supabase.pptx
└── ...
```

Each script is **self-contained**: helpers + slide builders + data + build() function + `__main__`. Copy helpers from an existing script — do not import from a shared module.

**Logos directory:** `docs/formations/logos/` (icons as `{name}.png`)

**LOGOS_DIR path must be updated** for the local machine. The existing scripts use `/home/node/.openclaw/...` — update to match the user's local path.

## Anti-Patterns — NEVER DO

- **Clone from template** — always create from scratch with `blank_slide()` + `add_rect()` + `add_textbox()`
- **Same layout for every slide** — use at least 4-5 different slide types per module
- **Only white backgrounds** — alternate with dark blue backgrounds for transitions, recaps, cover
- **3 colors only** — use the full palette (dark blue, teal, gold, gray backgrounds)
- **Wall of text** — break content across multiple slides rather than cramming
- **Missing visual breaks** — always put a dark-bg transition slide between lesson sections
- **Inconsistent spacing** — use `space_before = Pt(4-10)` consistently, empty `""` lines for grouping
- **Logo row at bottom** — place logos contextually: top-right for tools, grid for overviews, workflow for processes
