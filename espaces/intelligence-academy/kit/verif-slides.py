#!/usr/bin/env python3
"""
Vérifie les slides PPTX pour détecter les overflows de contenu.
Exporte chaque slide en image via Keynote pour vérification visuelle.

Usage :
  python3 verify_slides.py claude-chrome.pptx
  python3 verify_slides.py  # vérifie tous les PPTX du dossier slides/
"""

import sys
import os
import subprocess
import tempfile
import time
from pptx import Presentation
from pptx.util import Inches, Emu

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SLIDES_DIR = os.path.dirname(SCRIPT_DIR)
EXPORT_DIR = os.path.join(SLIDES_DIR, "verify")

# Slide bounds
SLIDE_W = Inches(13.333)
SLIDE_H = Inches(7.5)
SAFE_BOTTOM = Inches(6.5)  # max_y used in _draw_blocks_on_slide
LINE_H = Inches(0.45)
LINE_GAP = Inches(0.12)
BLOCK_GAP = Inches(0.3)
CONTENT_TOP_WITH_SUB = Inches(2.6)
CONTENT_TOP_NO_SUB = Inches(1.8)


def check_overflow(pptx_path):
    """Analyse chaque slide pour détecter les éléments qui débordent ou sont tronqués."""
    prs = Presentation(pptx_path)
    name = os.path.basename(pptx_path)
    issues = []

    for i, slide in enumerate(prs.slides, 1):
        # Collect all textboxes on this slide
        textboxes = []
        has_header = False
        has_subtitle = False
        last_textbox_bottom = 0

        for shape in slide.shapes:
            if not shape.has_text_frame:
                continue

            bottom = shape.top + shape.height
            textboxes.append({
                'text': shape.text,
                'top': shape.top,
                'bottom': bottom,
                'left': shape.left,
                'width': shape.width,
                'height': shape.height,
            })

            # Detect header (gradient bar area, top 1.25")
            if shape.top < Inches(0.5) and shape.height < Inches(1.2):
                has_header = True

            # Detect subtitle (area around 1.6")
            if Inches(1.4) < shape.top < Inches(1.9):
                has_subtitle = True

            # Track last content position
            if bottom > last_textbox_bottom and shape.top > Inches(1.5):
                last_textbox_bottom = bottom

        # Check for content slides that end abruptly near max_y
        # (sign of truncation: last textbox is near 6.5" but slide has lots of empty space below title)
        if has_header and last_textbox_bottom > 0:
            content_zone_start = CONTENT_TOP_WITH_SUB if has_subtitle else CONTENT_TOP_NO_SUB

            # Count actual content textboxes (below subtitle area)
            content_boxes = [tb for tb in textboxes if tb['top'] >= content_zone_start - Inches(0.1)]

            # If the last content box ends right at or near max_y (6.3-6.6"),
            # AND there aren't many content boxes, it's likely truncated
            if content_boxes:
                last_bottom_inches = Emu(last_textbox_bottom).inches
                # Content that stops between 6.0-6.6" is suspicious
                if 6.0 < last_bottom_inches < 6.6:
                    # Check if content is dense (many boxes packed together)
                    content_count = len(content_boxes)
                    available_height = SAFE_BOTTOM - content_zone_start
                    used_height = last_textbox_bottom - content_zone_start
                    fill_ratio = Emu(used_height).inches / Emu(available_height).inches if available_height > 0 else 0

                    if fill_ratio > 0.85:
                        # Slide is >85% full — likely at capacity, content may be truncated
                        first_text = content_boxes[0]['text'][:30] if content_boxes else '?'
                        last_text = content_boxes[-1]['text'][:30] if content_boxes else '?'
                        issues.append(
                            f"  Slide {i}: remplissage {fill_ratio:.0%} — contenu potentiellement tronqué "
                            f"(dernière ligne à {last_bottom_inches:.1f}\", max={Emu(SAFE_BOTTOM).inches:.1f}\")"
                            f"\n           Début: '{first_text}...' → Fin: '{last_text}...'"
                        )

    if issues:
        print(f"\n⚠️  {name} — {len(issues)} slide(s) avec contenu potentiellement tronqué :")
        for issue in issues:
            print(issue)
    else:
        print(f"\n✅  {name} — aucun overflow détecté ({len(prs.slides)} slides)")

    return issues


def export_to_images(pptx_path):
    """Exporte les slides en images via Keynote (macOS)."""
    name = os.path.splitext(os.path.basename(pptx_path))[0]
    out_dir = os.path.join(EXPORT_DIR, name)
    os.makedirs(out_dir, exist_ok=True)

    abs_path = os.path.abspath(pptx_path)
    abs_out = os.path.abspath(out_dir)

    script = f'''
    tell application "Keynote"
        set theDoc to open POSIX file "{abs_path}"
        delay 2
        export theDoc to POSIX file "{abs_out}" as slide images with properties {{image format:PNG}}
        close theDoc saving no
    end tell
    '''

    try:
        result = subprocess.run(
            ['osascript', '-e', script],
            capture_output=True, text=True, timeout=30
        )
        if result.returncode == 0:
            images = sorted([f for f in os.listdir(out_dir) if f.endswith('.png')])
            print(f"  📸 Exporté {len(images)} slides → {out_dir}/")
            return [os.path.join(out_dir, img) for img in images]
        else:
            print(f"  ❌ Export Keynote échoué : {result.stderr.strip()}")
            return []
    except subprocess.TimeoutExpired:
        print(f"  ❌ Export Keynote timeout (30s)")
        return []
    except Exception as e:
        print(f"  ❌ Export Keynote erreur : {e}")
        return []


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    if args:
        files = [os.path.join(SLIDES_DIR, f) if not os.path.isabs(f) else f
                 for f in args]
    else:
        files = sorted([
            os.path.join(SLIDES_DIR, f)
            for f in os.listdir(SLIDES_DIR)
            if f.endswith('.pptx') and not f.startswith('~')
        ])

    if not files:
        print("Aucun fichier PPTX trouvé.")
        return

    print(f"Vérification de {len(files)} fichier(s) PPTX...\n")

    all_issues = []
    for pptx_path in files:
        if not os.path.exists(pptx_path):
            print(f"❌ Fichier introuvable : {pptx_path}")
            continue
        issues = check_overflow(pptx_path)
        all_issues.extend(issues)

    print(f"\n{'='*60}")
    if all_issues:
        print(f"⚠️  Total : {len(all_issues)} problème(s) à corriger")
    else:
        print(f"✅ Tous les PPTX sont clean !")

    # Demander export images ?
    if '--export' in sys.argv:
        print(f"\nExport des slides en images (via Keynote)...")
        os.makedirs(EXPORT_DIR, exist_ok=True)
        for pptx_path in files:
            if os.path.exists(pptx_path):
                export_to_images(pptx_path)


if __name__ == "__main__":
    main()
