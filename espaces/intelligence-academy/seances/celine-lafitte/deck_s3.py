#!/usr/bin/env python3
"""Céline LAFITTE, séance 3 (mer. 28 oct. 2026, 13h-15h) : son outil d'autocoaching en service,
et le chemin de l'artefact à la plateforme. Charte TIA.

Fonctionnalités vérifiées le 27/10/2026 sur le centre d'aide Claude (support.claude.com) :
« Share artifacts » (23/09/2026), « What are artifacts and how do I use them » (mis à jour cette
semaine), « Use Google Workspace connectors » (mis à jour cette semaine), « Connect to Microsoft 365 ».
Demande de Céline : son mail du 27/10/2026 (images hors priorité, autocoaching et plateforme).
"""
import importlib.util
import os

HERE = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.join(HERE, "..", "..", "kit")
_spec = importlib.util.spec_from_file_location("tia", os.path.join(KIT, "lib-slides-python.py"))
tia = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(tia)

OUTPUT_PATH = os.path.join(HERE, "celine-lafitte-s3-autocoaching-plateforme.pptx")
KICKER = "SÉANCE 3 / 4 · CÉLINE LAFITTE"
I = tia.Inches

# _draw_blocks_on_slide pose chaque ligne dans une boîte de 0.45" : une ligne qui passe à la ligne
# chevauche la suivante sans que verif-slides le voie. On borne la longueur et la hauteur ici.
MAX_CHARS = 78


def check_titles(header, subtitle):
    # Titre 34pt et sous-titre 26pt sur 11.5" : au-delà, ils passent sur deux lignes et chevauchent.
    assert len(header) <= 42, f"Titre trop long ({len(header)}) : {header}"
    assert subtitle is None or len(subtitle) <= 50, f"Sous-titre trop long ({len(subtitle)}) : {subtitle}"


def notes(slides, text):
    """Notes orateur pour Idris, posées sur chaque slide d'une même séquence."""
    for s in slides if isinstance(slides, list) else [slides]:
        s.notes_slide.notes_text_frame.text = text
    return slides


def text(slide, x, y, w, h, s, size, bold=False, color=None, align=None):
    tia.add_textbox(slide, I(x), I(y), I(w), I(h), s, font_size=size, bold=bold,
                    color=color or tia.C_BODY, align=align or tia.PP_ALIGN.LEFT)


def pipeline(header, subtitle, steps, note):
    check_titles(header, subtitle)
    for s in steps:
        for part in s.split("\n"):
            assert len(part) <= 22, f"Boîte de schéma trop longue ({len(part)}) : {part}"
    assert len(note) <= 95, f"Note trop longue ({len(note)}) : {note}"
    # La note native de slide_pipeline tombe à 6.4" : verif-slides la signale. On la pose sous les
    # boîtes, plus bas quand le diagramme passe sur deux lignes.
    slide = tia.slide_pipeline(prs, header, subtitle, steps)
    y = 4.5 if len(steps) <= 4 else 5.5
    text(slide, 0.7, y, 12.0, 0.45, note, 18, bold=True, color=tia.C_TEAL)
    return slide


def content(header, subtitle, bullets):
    check_titles(header, subtitle)
    for line in bullets:
        # Consolas est plus large : 70 caractères tiennent sur une ligne.
        assert not line.startswith("` ") or len(line) <= 72, f"Ligne de code trop longue ({len(line)}) : {line}"
        assert len(line.lstrip("*")) <= MAX_CHARS, f"Ligne trop longue ({len(line)}) : {line}"
    blocks = tia._split_into_blocks(bullets)
    n_lines = sum(len(b) for b in blocks)
    top = 2.55 if subtitle else 1.7
    bottom = top + n_lines * 0.57 - 0.12 + (len(blocks) - 1) * 0.26
    assert bottom <= 6.0, f"Slide « {subtitle or header} » trop pleine (bas à {bottom:.2f}\")"
    return tia.slide_content(prs, header, subtitle, bullets)


def quiz(num, total, question, options, reponse):
    """Deux slides : la question et ses choix en cartes grises, puis la même avec la réponse."""
    header = f"Quiz · Question {num} / {total}"
    assert len(question) <= 62, f"Question trop longue ({len(question)}) : {question}"
    assert len(options) <= 3 and len(reponse) <= 2
    for o in options:
        assert len(o) <= 80, f"Choix trop long ({len(o)}) : {o}"
    for r in reponse:
        assert len(r) <= 82, f"Réponse trop longue ({len(r)}) : {r}"
    out = []
    for with_answer in (False, True):
        slide = tia.blank_slide(prs)
        tia.add_header(slide, header)
        text(slide, 0.7, 1.55, 11.9, 0.8, question, 24, bold=True, color=tia.C_TITLE)
        y = 2.5
        for o in options:
            tia.add_rounded_rect(slide, I(0.7), I(y), I(11.9), I(0.58), fill_color=tia.C_GRAY_BG)
            text(slide, 0.95, y + 0.08, 11.5, 0.42, o, 19)
            y += 0.7
        if with_answer:
            tia.add_rounded_rect(slide, I(0.7), I(4.75), I(11.9), I(1.15), fill_color=tia.C_TEAL)
            yy = 4.85
            for r in reponse:
                text(slide, 0.95, yy, 11.5, 0.42, r, 18, bold=True, color=tia.C_WHITE)
                yy += 0.47
        out.append(slide)
    return out


def tableau(header, colonnes, largeurs, rows, note=None):
    """Tableau comparatif : en-têtes teal, lignes grises une sur deux."""
    check_titles(header, None)
    assert abs(sum(largeurs) - 11.9) < 0.01 and len(rows) <= 6
    slide = tia.blank_slide(prs)
    tia.add_header(slide, header)
    xs = [0.7]
    for w in largeurs[:-1]:
        xs.append(xs[-1] + w)
    y = 1.6
    for x, w, titre in zip(xs, largeurs, colonnes):
        assert len(titre) <= int((w - 0.3) * 7.5), f"En-tête trop long ({len(titre)}) : {titre}"
        text(slide, x + 0.15, y, w - 0.2, 0.4, titre, 18, bold=True, color=tia.C_TEAL)
    tia.add_rect(slide, I(0.7), I(y + 0.45), I(11.9), I(0.03), tia.C_GOLD)
    y += 0.55
    for n, row in enumerate(rows):
        if n % 2 == 0:
            tia.add_rect(slide, I(0.7), I(y), I(11.9), I(0.5), tia.C_GRAY_BG)
        for i, (x, w, t) in enumerate(zip(xs, largeurs, row)):
            assert len(t) <= int((w - 0.3) * 8.5), f"Cellule trop longue ({len(t)}) : {t}"
            text(slide, x + 0.15, y + 0.06, w - 0.2, 0.38, t, 16, bold=(i == 0),
                 color=tia.C_TITLE if i == 0 else tia.C_BODY)
        y += 0.5
    if note:
        assert len(note) <= 95, f"Note trop longue ({len(note)}) : {note}"
        text(slide, 0.7, y + 0.25, 11.9, 0.5, note, 17, bold=True, color=tia.C_TEAL)
    return slide


def deux_colonnes(header, subtitle, gauche, droite, note=None):
    """Deux colonnes séparées par un filet or : (titre, lignes) de chaque côté."""
    check_titles(header, subtitle)
    slide = tia.blank_slide(prs)
    tia.add_header(slide, header)
    if subtitle:
        tia.add_subtitle(slide, subtitle)
    top = 2.5 if subtitle else 1.7
    n_max = max(len(gauche[1]), len(droite[1]))
    tia.add_rect(slide, I(6.45), I(top), I(0.03), I(0.6 + n_max * 0.52), tia.C_GOLD)
    for x, (titre, lignes) in ((0.7, gauche), (6.75, droite)):
        assert len(lignes) <= 5 and len(titre) <= 40
        text(slide, x, top, 5.5, 0.45, titre, 21, bold=True, color=tia.C_TEAL)
        y = top + 0.65
        for l in lignes:
            assert len(l) <= 44, f"Ligne de colonne trop longue ({len(l)}) : {l}"
            text(slide, x, y, 5.6, 0.42, l, 18)
            y += 0.52
    if note:
        assert len(note) <= 95, f"Note trop longue ({len(note)}) : {note}"
        assert top + 0.8 + n_max * 0.52 + 0.45 <= 6.0, f"Colonnes trop pleines : {header}"
        text(slide, 0.7, top + 0.8 + n_max * 0.52, 11.9, 0.45, note, 18, bold=True, color=tia.C_GOLD)
    return slide


def enonce(header, cadre, steps):
    """Slide d'exercice (type 10 de la charte) : un bandeau gris Objectif / Livrable / Durée,
    puis les étapes numérotées (numéro teal en gras, texte foncé)."""
    check_titles(header, None)
    assert len(cadre) == 3 and len(steps) <= 5
    slide = tia.blank_slide(prs)
    tia.add_header(slide, header)
    tia.add_rounded_rect(slide, I(0.7), I(1.55), I(11.9), I(1.25), fill_color=tia.C_GRAY_BG)
    col_w = [4.6, 5.0, 1.9]
    x = 0.95
    for (label, t), w in zip(cadre, col_w):
        assert len(t) <= 2 * (w - 0.2) * 8, f"Cadre trop long ({len(t)}) : {t}"  # 2 lignes à 16pt
        text(slide, x, 1.65, w - 0.2, 0.35, label, 14, bold=True, color=tia.C_GOLD)
        text(slide, x, 1.98, w - 0.2, 0.75, t, 16, color=tia.C_TITLE)
        x += w
    y = 3.1
    for n, step in enumerate(steps, 1):
        assert len(step) <= 74, f"Étape trop longue ({len(step)}) : {step}"
        tb = slide.shapes.add_textbox(I(0.7), I(y), I(11.9), I(0.45))
        tf = tb.text_frame; tf.word_wrap = True
        p = tf.paragraphs[0]
        r = p.add_run(); r.text = f"{n}.  "
        r.font.name = tia.FONT; r.font.size = tia.Pt(19); r.font.bold = True; r.font.color.rgb = tia.C_TEAL
        r = p.add_run(); r.text = step
        r.font.name = tia.FONT; r.font.size = tia.Pt(19); r.font.color.rgb = tia.C_BODY
        y += 0.57
    return slide


def cartes(header, subtitle, items):
    """Grille 3 × 2 de cartes grises : nom en teal, le rôle, puis un exemple pour Céline."""
    check_titles(header, subtitle)
    assert len(items) == 6
    slide = tia.blank_slide(prs)
    tia.add_header(slide, header)
    tia.add_subtitle(slide, subtitle)
    w, h = 3.8, 1.6
    for n, (nom, role, exemple) in enumerate(items):
        assert len(nom) <= 28, f"Nom de carte trop long ({len(nom)}) : {nom}"
        assert len(role) <= 54, f"Rôle trop long ({len(role)}) : {role}"   # 2 lignes à 16pt sur 3.5"
        assert len(exemple) <= 28, f"Exemple trop long ({len(exemple)}) : {exemple}"  # 1 ligne
        x = 0.7 + (n % 3) * (w + 0.25)
        y = 2.4 + (n // 3) * (h + 0.2)
        tia.add_rounded_rect(slide, I(x), I(y), I(w), I(h), fill_color=tia.C_GRAY_BG)
        tia.add_rect(slide, I(x), I(y + 0.15), I(0.06), I(h - 0.3), tia.C_GOLD)
        text(slide, x + 0.22, y + 0.08, w - 0.35, 0.4, nom, 17, bold=True, color=tia.C_TEAL)
        text(slide, x + 0.22, y + 0.48, w - 0.35, 0.6, role, 16, color=tia.C_TITLE)
        text(slide, x + 0.22, y + 1.08, w - 0.35, 0.4, exemple, 16, color=tia.C_TEAL_LIGHT)
    return slide


def decision(header, rows, note):
    """Arbre de décision à plat : une question par ligne, une flèche or, la réponse en pastille teal."""
    check_titles(header, None)
    assert len(rows) <= 4 and len(note) <= 95
    slide = tia.blank_slide(prs)
    tia.add_header(slide, header)
    y = 1.6
    for question, reponse in rows:
        assert len(question) <= 56, f"Question trop longue ({len(question)}) : {question}"
        assert len(reponse) <= 26, f"Réponse trop longue ({len(reponse)}) : {reponse}"
        tia.add_rounded_rect(slide, I(0.7), I(y), I(7.7), I(0.78), fill_color=tia.C_GRAY_BG)
        text(slide, 0.95, y + 0.17, 7.3, 0.45, question, 19, color=tia.C_TITLE)
        text(slide, 8.45, y + 0.12, 0.5, 0.5, "→", 26, bold=True, color=tia.C_GOLD, align=tia.PP_ALIGN.CENTER)
        tia.add_rounded_rect(slide, I(9.0), I(y), I(3.6), I(0.78), fill_color=tia.C_TEAL)
        text(slide, 9.1, y + 0.18, 3.4, 0.45, reponse, 18, bold=True, color=tia.C_WHITE, align=tia.PP_ALIGN.CENTER)
        y += 0.95
    text(slide, 0.7, y + 0.15, 11.9, 0.45, note, 18, bold=True, color=tia.C_TEAL)
    return slide


def echelle(header, marches, note):
    """Un escalier de quatre marches, de la plus simple (en bas) à la plus complète (en haut) :
    numéro et nom en gras, une ligne d'explication dessous."""
    check_titles(header, None)
    assert len(marches) == 4 and len(note) <= 95
    slide = tia.blank_slide(prs)
    tia.add_header(slide, header)
    w, h = 7.4, 0.86
    for n, (nom, ligne) in enumerate(marches):
        assert len(nom) <= 30, f"Nom de marche trop long ({len(nom)}) : {nom}"
        assert len(ligne) <= 62, f"Ligne de marche trop longue ({len(ligne)}) : {ligne}"
        x = 0.7 + n * 1.5
        y = 4.55 - n * 0.98
        tia.add_rounded_rect(slide, I(x), I(y), I(w), I(h),
                             fill_color=tia.C_TEAL if n % 2 == 0 else tia.C_HEADER_RIGHT)
        text(slide, x + 0.2, y + 0.04, w - 0.4, 0.4, f"{n + 1}.  {nom}", 18, bold=True, color=tia.C_WHITE)
        text(slide, x + 0.2, y + 0.42, w - 0.4, 0.4, ligne, 15, color=tia.C_WHITE)
    text(slide, 0.7, 1.65, 2.9, 0.4, "↑  PLUS COMPLET", 16, bold=True, color=tia.C_GOLD)
    text(slide, 0.7, 2.05, 2.9, 0.7, "plus de travail, plus de coût", 15, color=tia.C_TEAL_LIGHT)
    text(slide, 0.7, 5.5, 11.9, 0.45, note, 18, bold=True, color=tia.C_TEAL)
    return slide


prs = tia.new_prs()

# ── Ouverture ────────────────────────────────────────────────────────────────
tia.slide_cover(prs, KICKER, "Ton outil, en service",
                "De l'artefact à la plateforme : le bon chemin pour tes clients",
                "Mercredi 28 octobre 2026 · 13h-15h · Idris Salvi")

pipeline("Ton parcours", "4 séances, un fil rouge : tes outils de coach", [
    "S1 · 8 oct.\nComprendre ✓", "S2 · 19 oct.\nRanger + skills ✓",
    "S3 · 28 oct.\nTon outil en ligne", "S4 · 5 nov.\nTa chaîne complète",
], "Aujourd'hui : ton check-up rempli par un coaché, et ta route vers ta plateforme.")

notes(deux_colonnes("Ce que tu m'as écrit", "Ton point d'avancement du 27 octobre",
    ("Ce que tu as avancé", [
        "Ton organisation : claire dans ta tête",
        "Instructions créées, Claude et ChatGPT",
        "Ton skill de synthèse : « nickel »",
        "Un 2e skill : préparation et compte rendu",
        "Tout l'e-learning disponible : terminé",
    ]),
    ("Ce que tu veux aujourd'hui", [
        "Partager ton outil d'autocoaching",
        "Récupérer les réponses de tes coachés",
        "Interface ou plateforme : la différence ?",
        "Les images : pas ta priorité",
    ]),
), "Reprise fidèle de son mail du 27/10 (réponse à mon mail du jour). L'API confirme : les 8 modules "
   "e-learning sont terminés, Midjourney & Nano Banana compris. Ce qu'elle n'a pas fini : formaliser "
   "toute son organisation dans Claude, et peaufiner ses instructions. Les images sortent de la séance à "
   "sa demande. Sa question « interface ou plateforme » rejoint le projet de plateforme collaborative "
   "évoqué par Antoine à l'appel de vente.")

content("Le déroulé de cet après-midi", None, [
    "**1.  Quiz : tes e-learnings et la séance 2 (10 min)",
    "**2.  Tes devoirs : tu me montres (15 min)",
    "**3.  Théorie : de l'artefact à la plateforme (20 min)",
    "",
    "**4.  Pratique 1 : ton check-up en service (40 min)",
    "**5.  Pratique 2 : ta feuille de route (25 min)",
    "**6.  Les devoirs (10 min)",
])

# ── 1. Quiz ──────────────────────────────────────────────────────────────────
tia.slide_section(prs, "1", "Quiz d'ouverture", "Quatre questions : tes e-learnings et la séance 2")

notes(quiz(1, 4, "Les instructions personnalisées de ChatGPT s'appliquent…", [
    "A.  Seulement au GPT personnalisé que tu as créé",
    "B.  À toutes tes conversations, sauf tes GPT personnalisés",
    "C.  Seulement à la conversation en cours",
], [
    "B. C'est l'équivalent de tes Instructions pour Claude :",
    "ce qui vaut partout, court, sans règle de tâche.",
]), "E-learning « Fonctionnalités avancées de ChatGPT », vidéo 1 : « ça s'appliquera tout le temps, "
    "sauf aux GPT personnalisés ». Pont avec la S2 : elle a créé des instructions des deux côtés, "
    "même règle de tri (partout / projet / méthode).")

notes(quiz(2, 4, "Deep Research, par rapport à une recherche web classique…", [
    "A.  Va plus vite, sur moins de pages",
    "B.  Agit comme un agent : des centaines de pages, il clique, il creuse",
    "C.  Ne cite pas ses sources",
], [
    "B. Idéal pour des données objectives : un marché, des chiffres, des dispositifs.",
    "Pour ton métier : un panorama des financements d'un bilan, par exemple.",
]), "E-learning, vidéo « Réaliser une recherche approfondie sur un sujet » : jusqu'à 200 pages, "
    "un vrai agent qui peut cliquer (FAQ dépliables), intérêt « principalement sur des données objectives ».")

notes(quiz(3, 4, "Midjourney : garder le même style sur 20 visuels, avec…", [
    "A.  Le même prompt, copié à chaque fois",
    "B.  Un moodboard : quelques images de référence de ton style",
    "C.  Le nom d'un artiste dans le prompt",
], [
    "B. Le moodboard porte la direction artistique : tes prompts restent courts.",
    "Le nom d'un artiste : souvent bloqué, et pas ton style à toi.",
]), "E-learning « Focus Midjourney & Nano Banana », vidéo Moodboard. Le module ChatGPT avancé dit aussi "
    "qu'on ne peut pas (ou difficilement) citer un artiste dans un prompt d'image. Question courte : "
    "les images ne sont pas sa priorité, on ne s'y attarde pas.")

notes(quiz(4, 4, "Séance 2 : un fichier vivant, tu le donnes à Claude…", [
    "A.  En le téléversant à nouveau chaque lundi",
    "B.  En le laissant dans Drive : Claude le lit à la source",
    "C.  En le recopiant dans les instructions du projet",
], [
    "B. Et c'est exactement le cas des réponses de tes coachés :",
    "elles arrivent dans un tableur, Claude va les lire là où elles sont.",
]), "Pont direct vers la Pratique 1. Centre d'aide « Use Google Workspace connectors » : le connecteur "
    "Google Drive lit les Sheets (texte seulement). La synchronisation automatique dans les fichiers d'un "
    "projet n'est confirmée que pour les Google Docs : pour un Sheets, on demande la lecture dans la "
    "conversation, qui lit la version du moment.")

# ── 2. Retour sur les devoirs ────────────────────────────────────────────────
tia.slide_section(prs, "2", "Tes devoirs", "Partage d'écran : tu me montres")

notes(content("Tes devoirs : tu me montres", None, [
    "**1.  Ton organisation : ce qui est en place, ce qui reste à faire",
    "**2.  Tes instructions, Claude et ChatGPT : on les relit ensemble",
    "",
    "**3.  Ton 2e skill, préparation et compte rendu : un test en direct",
    "**4.  Ton outil d'autocoaching, tel qu'il est aujourd'hui",
]), "Point 1 : 5 minutes maximum, juste débloquer ce qui l'empêche de finir (souvent : où ranger un "
    "cas limite). Point 3 : lui faire lancer le skill sur des notes fictives, vérifier qu'il se "
    "déclenche seul. Point 4 : c'est le pont vers la théorie. Regarder si son artefact affiche « Publish » "
    "(artefact legacy, créé dans un chat avant le 16/09/2026 : publié, il s'ouvre SANS compte Claude) ou "
    "« Share » (artefact récent : compte Claude obligatoire). Regarder aussi s'il appelle Claude pour "
    "produire la cartographie : dans ce cas, l'IA consomme le forfait de la personne qui le remplit.")

# ── 3. Théorie ───────────────────────────────────────────────────────────────
tia.slide_section(prs, "3", "De l'artefact à la plateforme", "Quatre marches, une question : jusqu'où monter ?")

notes(deux_colonnes("Interface ou plateforme ?", "Ta question, la réponse en une slide",
    ("Une interface", [
        "Une porte d'entrée : une page, un lien",
        "Le coaché remplit, tu reçois",
        "Pas de compte, pas d'historique",
        "Ex. : ton check-up en ligne",
    ]),
    ("Une plateforme", [
        "Des comptes : chacun se connecte",
        "Un espace par coaché, à lui seul",
        "Son historique : réponses, synthèses",
        "Ex. : ton espace de suivi de coaching",
    ]),
    "Une plateforme = des interfaces + des comptes + une mémoire par coaché."),
    "Réponse directe à son mail : « une interface pour mes clients, ou une plateforme, je ne sais pas si "
    "c'est différent ». Oui : la différence tient aux comptes et à la durée. Une interface sert un usage "
    "ponctuel ; une plateforme suit une personne dans le temps.")

notes(pipeline("Ton outil, en quatre temps", "Ce que fait ton check-up, quel que soit l'outil", [
    "1. Le coaché\nrépond", "2. Ses réponses\nsont rangées", "3. L'IA\nanalyse", "4. Tu relis,\ntu restitues",
], "Chaque marche de l'échelle fait ces quatre temps, mais pas au même endroit."),
    "Grille de lecture pour la suite : pour chaque solution, se demander où se passe chaque temps. "
    "Le temps 4 ne change jamais : rien ne part au coaché sans sa relecture (c'est aussi son "
    "positionnement de coach face à l'IA).")

notes(echelle("De l'artefact à la plateforme", [
    ("Artefact Claude", "Le coaché ouvre ton lien avec son propre compte Claude"),
    ("Formulaire + tableur", "Lien ouvert à tous, réponses rangées dans un Google Sheets"),
    ("Interface hébergée", "Ton outil à ton image, en ligne, sans compte à créer"),
    ("Plateforme", "Des comptes, un espace et un historique par coaché"),
], "On monte d'une marche seulement quand la précédente ne suffit plus."),
    "Marche 3 : une petite application construite avec Claude Code et mise en ligne chez un hébergeur "
    "(compter quelques euros par mois, ordre de grandeur donné en S2). Marche 4 : un outil de portail "
    "client no-code (par exemple Softr sur une base Airtable) ou un développement sur mesure.")

notes(content("Marche 1 : ton artefact aujourd'hui", "Ce que dit l'aide Claude, à jour d'octobre", [
    "**Partager : bouton Share › « Only you » ou « Anyone with the link ».",
    "Le coaché doit avoir un compte Claude, même gratuit, même avec le lien.",
    "",
    "**S'il appelle Claude, l'IA tourne sur le forfait de la personne.",
    "**Stockage : 20 Mo de texte, personnel ou partagé avec tous.",
    "",
    "> Récupérer les réponses de tous : rien de prévu dans l'aide Claude",
]), "Sources, centre d'aide Claude : « Share artifacts » (23/09/2026) : « Everyone needs a Claude account. "
    "People without one can't open a shared artifact, even with the link. The only exception is a legacy "
    "artifact published from a chat. » « What are artifacts » (mis à jour cette semaine) : stockage sur "
    "Pro, Max, Team, Enterprise, 20 Mo par artefact, texte seulement ; personnel ou partagé ; l'usage de "
    "Claude « counts against each person's own plan limits ». Aucune page ne décrit la collecte des "
    "réponses de plusieurs visiteurs ni leur export par le créateur : le présenter comme non documenté, "
    "pas comme impossible. Point non tranché entre deux pages : « Share artifacts » dit qu'un artefact qui "
    "utilise Claude ne peut pas être en « Anyone with the link ». À tester en direct sur le sien.")

notes(tableau("Les 4 marches, côte à côte",
    ["", "1. Artefact", "2. Formulaire", "3. Interface", "4. Plateforme"],
    [2.7, 2.3, 2.3, 2.3, 2.3], [
    ["Compte du coaché", "Claude", "Aucun", "Aucun", "Créé chez toi"],
    ["Ses réponses", "Dans l'artefact", "Google Sheets", "Ta base", "Ta base"],
    ["L'IA tourne sur", "Son forfait", "Ton Claude", "Une clé API", "Une clé API"],
    ["Coût pour toi", "Inclus (Pro)", "Gratuit", "~5 €/mois", "Abonnement"],
    ["Qui le construit", "Toi + Claude", "Toi, 20 min", "Claude Code", "Outil no-code"],
], "Aujourd'hui : la marche 2. La 3 et la 4 se décident en Pratique 2."),
    "Marche 2 : Google Forms est gratuit avec un compte Google, et le répondant n'a besoin d'aucun compte "
    "tant qu'on ne coche pas « Limiter à 1 réponse » (qui impose la connexion Google). « Ton Claude » : "
    "c'est elle qui lance l'analyse dans son Claude Pro, avec le connecteur Google Drive. Marches 3 et 4 : "
    "une IA intégrée à une application passe par l'API Claude, payée à l'usage. Pourquoi Google et pas "
    "Microsoft : le connecteur Microsoft 365 de Claude refuse les comptes personnels (outlook.com, hotmail, "
    "live), il exige un compte pro ou école (centre d'aide « Connect to Microsoft 365 »). Avec son adresse "
    "outlook.fr, c'est bloqué ; elle a déjà connecté Gmail, donc un compte Google.")

notes(content("Les données de tes coachés", "L'usage responsable, avant la technique", [
    "**Dis ce que tu collectes et pourquoi : une phrase en tête du formulaire.",
    "**Demande l'accord : c'est la première question, obligatoire.",
    "",
    "**Ne demande que le nécessaire : pas de santé, pas de nom complet.",
    "**Avant Claude, un code à la place du nom : « C-01 », « C-02 ».",
    "",
    "> Rien ne part au coaché sans ta relecture",
]), "Ses check-ups touchent à la personne (valeurs, objectifs, parfois la santé ou la vie privée) : ce "
    "sont des données personnelles au sens du RGPD. Rappel S2 : Paramètres › Confidentialité, option "
    "d'amélioration des modèles à désactiver. Sur un artefact en stockage partagé, ce qu'un coaché saisit "
    "peut être vu par les autres : c'est l'avertissement de l'aide Claude.")

tia.slide_recap(prs, "De l'artefact à la plateforme", [
    "1.  Interface = une porte d'entrée. Plateforme = des comptes et un suivi.",
    "2.  Ton artefact : idéal pour toi, pas pour collecter chez des coachés.",
    "3.  Formulaire + tableur : le bon outil pour ton check-up, dès aujourd'hui.",
    "4.  On monte d'une marche seulement quand la précédente ne suffit plus.",
    "5.  Les données d'abord : accord, minimum, code à la place du nom.",
])

# ── 4. Pratique 1 ────────────────────────────────────────────────────────────
tia.slide_section(prs, "4", "Pratique 1 : ton check-up en service", "Deux parties : le formulaire, puis la cartographie")

notes(pipeline("Pratique 1 · Le circuit", "Ce que tu auras construit dans 40 minutes", [
    "Google Forms\nle coaché répond", "Google Sheets\nune ligne par coaché",
    "Claude + Drive\nlit la ligne", "Skill Cartographie\nrédige",
    "Toi\ntu relis, tu envoies",
], "Partie A (20 min) : les deux premières boîtes. Partie B (20 min) : les trois suivantes."),
    "Le circuit complet sous les yeux avant de commencer, pour qu'elle sache à chaque étape où elle en est.")

notes(enonce("Pratique 1 · Partie A : le formulaire", [
    ("OBJECTIF", "Ton check-up rempli sans compte, les réponses rangées."),
    ("LIVRABLE", "Un Google Form relié à un Google Sheets, testé une fois."),
    ("DURÉE", "20 minutes"),
], [
    "Dans la conversation de ton artefact : coller le prompt A (chat).",
    "Google Forms › Formulaire vierge : titre, puis l'intro de Claude.",
    "Créer chaque question listée par Claude, avec le type proposé.",
    "Onglet Réponses › Lier à Sheets : une ligne par réponse.",
    "Remplir toi-même en coaché fictif C-01, vérifier la ligne dans Sheets.",
]), "Le prompt A est dans s3-a-coller.md, à coller dans le chat de la visio. Paramètres du formulaire : "
    "ne PAS cocher « Limiter à 1 réponse » (elle impose un compte Google au répondant). Collecte d'e-mails : "
    "seulement si elle en a besoin pour renvoyer la cartographie. Ajouter une question « Ton code » "
    "(C-01…) qu'elle donne au coaché : c'est ce code, pas le nom, que Claude verra.")

notes(content("Partie A · Le prompt, dans ton artefact", None, [
    "` Je veux transformer cet outil en Google Form. Liste ses",
    "` questions dans l'ordre, avec le type Google Forms de chacune :",
    "` réponse courte, paragraphe, échelle, choix multiples, cases.",
    "",
    "` Ajoute en tête « Ton code coaché » et une question d'accord.",
    "` Propose une phrase d'intro. N'invente aucune question.",
]), "Texte complet dans s3-a-coller.md, à coller dans le chat de la visio. À lancer dans la conversation "
    "où elle a créé son outil d'autocoaching : Claude y a déjà toutes les questions sous les yeux.")

notes(content("Partie A · Les types de questions", "Un type par question, pour des réponses lisibles", [
    "**Réponse courte : ton code coaché, un prénom, un poste.",
    "**Paragraphe : « Qu'est-ce qui compte le plus pour toi au travail ? »",
    "",
    "**Échelle de 1 à 5 : ton niveau d'énergie, ta satisfaction.",
    "**Choix multiples : une seule réponse possible.",
    "**Cases à cocher : plusieurs réponses, tes valeurs par exemple.",
]), "Les noms suivent l'interface française de Google Forms. Une échelle ou des cases donnent des "
    "réponses comparables d'un coaché à l'autre ; les paragraphes donnent la matière de la cartographie. "
    "Le prompt A demande justement à Claude de proposer le type de chaque question.")

notes(enonce("Pratique 1 · Partie B : la cartographie", [
    ("OBJECTIF", "Claude lit les réponses d'un coaché et rédige sa cartographie."),
    ("LIVRABLE", "Ton skill « Cartographie », testé sur la réponse fictive."),
    ("DURÉE", "20 minutes"),
], [
    "Vérifier : Paramètres › Connecteurs › Google Drive est connecté.",
    "Dans ton projet de coaching : coller le prompt B (chat), code C-01.",
    "Juger le rendu : fidèle aux réponses ? au format de ta cartographie ?",
    "« On crée un skill à partir de ce rendu » : tu valides sa structure.",
    "Le tester sur une 2e réponse fictive : tu corriges le skill, pas le texte.",
]), "Le connecteur Google Drive lit les Sheets (centre d'aide « Use Google Workspace connectors ») : texte "
    "seulement, et le fichier doit tenir dans la fenêtre de contexte. On demande la lecture dans la "
    "conversation : Claude lit la version du moment. Ne pas compter sur l'ajout du Sheets aux fichiers du "
    "projet : la synchronisation automatique n'est documentée que pour les Google Docs. Étapes 4-5 : la "
    "méthode de création de skill de la S2.")

notes(content("Partie B · Le prompt, dans ton projet", None, [
    "` Dans mon Drive, ouvre le Google Sheets « Check-up - réponses ».",
    "` Lis uniquement la ligne du code C-01.",
    "` Rédige sa cartographie selon ma trame : valeurs, talents,",
    "` motivations, freins, pistes d'évolution.",
    "",
    "` Règles : rien d'inventé, cite la réponse qui fonde chaque point,",
    "` [À vérifier] sur chaque déduction.",
]), "Texte complet dans s3-a-coller.md. Adapter le nom du Sheets et les rubriques à SA cartographie "
    "(celle que produit son artefact actuel). Les règles reprennent celles de la S1 et de son skill de "
    "synthèse : elles passeront dans le skill Cartographie.")

tia.slide_recap(prs, "Ton check-up en service", [
    "1.  Un lien que tes coachés remplissent, sans compte.",
    "2.  Une ligne par coaché, rangée seule dans ton Sheets.",
    "3.  Claude lit la ligne à la source, avec un code à la place du nom.",
    "4.  Ton skill Cartographie rédige, toi tu relis et tu restitues.",
])

# ── 5. Pratique 2 ────────────────────────────────────────────────────────────
tia.slide_section(prs, "5", "Pratique 2 : ta feuille de route", "Jusqu'où monter, pour quels clients ?")

notes(decision("Quelle marche pour quel besoin ?", [
    ("Ton coaché a Claude, et tu restes à ses côtés ?", "Marche 1 · artefact"),
    ("Un questionnaire, rempli une fois ?", "Marche 2 · formulaire"),
    ("Un outil à ton image, sans compte ?", "Marche 3 · interface"),
    ("Chaque coaché revient voir son espace ?", "Marche 4 · plateforme"),
], "Une même activité peut combiner deux marches : un formulaire, puis un espace."),
    "Outil de décision de la Pratique 2, sur le modèle du test en quatre questions de la S2. Marche 1 : "
    "cas réaliste en séance (elle partage son écran) ou pour un client équipé de Claude.")

notes(enonce("Pratique 2 · L'énoncé", [
    ("OBJECTIF", "Décider ce que tu construis, pour qui, et dans quel ordre."),
    ("LIVRABLE", "Ta feuille de route d'une page : publics, marches, étapes."),
    ("DURÉE", "25 minutes"),
], [
    "Lister tes publics : coachés, bilans, attachés de direction, organismes.",
    "Pour chacun : que remplit-il, que reçoit-il, revient-il ?",
    "Passer chacun au test : quelle marche lui suffit ?",
    "Dessiner ta plateforme cible avec les six questions (slide suivante).",
    "Choisir la première étape réaliste, à préparer pour la séance 4.",
]), "Faire l'exercice dans Claude (une conversation dans son projet de coaching, ou un document partagé) "
    "pour qu'elle reparte avec la page. Le prompt C de la fiche structure la feuille de route. Ses publics "
    "connus (dossier TIA) : managers, attachés de direction, personnes en reconversion, organismes de bilan.")

notes(cartes("Ta plateforme cible", "Six questions avant de construire quoi que ce soit", [
    ("Qui se connecte ?", "Tes coachés, et peut-être l'organisme qui finance", "Ex. : le coaché, toi"),
    ("Ce qu'il voit", "Son espace : ses réponses, ses synthèses, ses étapes", "Ex. : sa cartographie"),
    ("Ce qu'il remplit", "Check-up, questionnaire de valeurs, bilan d'étape", "Ex. : le check-up"),
    ("Ce que fait l'IA", "Analyser, synthétiser, proposer des pistes", "Ex. : la cartographie"),
    ("Ce que tu valides", "Tout ce qui part au coaché passe par toi", "Ex. : chaque restitution"),
    ("Où vivent les données", "Un outil choisi pour ça, avec l'accord du coaché", "Ex. : hébergement en UE"),
]), "Ces six réponses forment le cahier des charges de la marche 3 ou 4, que Claude Code ou un outil "
    "no-code saura construire. C'est aussi le module 4 du programme (« Poser la première version de l'espace "
    "partagé avec le coaché »), qu'on attaque en S4.")

notes(content("Pour monter aux marches 3 et 4", "Ce qu'il faut savoir avant de se lancer", [
    "**Marche 3 : Claude Code construit l'application, un hébergeur la publie.",
    "Inclus dans ton forfait Pro ; l'hébergement, quelques euros par mois.",
    "",
    "**Marche 4 : un outil de portail client no-code, ou du sur-mesure.",
    "Ex. : Softr sur une base Airtable, avec les comptes de tes coachés.",
    "",
    "**Dès qu'une application appelle l'IA : une clé API Claude, à l'usage.",
]), "Claude Code est inclus dans le forfait Pro. Ordre de grandeur de l'hébergement donné en S2 (environ "
    "5 € par mois). Softr et Airtable : exemple d'outils de portail client, pas une recommandation ferme ; "
    "le choix se fera en S4 à partir de sa feuille de route. L'API Claude est facturée à l'usage, "
    "séparément de l'abonnement Pro.")

# ── 6. Les devoirs ───────────────────────────────────────────────────────────
tia.slide_section(prs, "6", "Les devoirs", "Pour la séance 4, jeudi 5 novembre")

notes(content("Devoirs · avant le 5 novembre", None, [
    "**1.  Envoyer ton formulaire à 1 ou 2 coachés réels, avec leur accord",
    "**2.  Lancer ton skill Cartographie sur leurs réponses, le corriger",
    "**3.  Finir de mettre en place ton organisation dans Claude",
    "",
    "**4.  M'envoyer ta feuille de route d'une page avant le 3 novembre",
    "**5.  Pour la S4 : un transcript de séance anonymisé, avec accord",
    "**6.  Émarger sur ton tableau de bord",
]), "Le 1 et le 2 donnent la matière réelle de la S4. Le 4 laisse deux jours pour préparer la S4 sur "
    "sa feuille de route (marche choisie, première version de l'espace coaché). Le 5 sert le module 3 du "
    "programme (agent de lecture de séance), assemblé en S4 dans la chaîne séance, lecture, cartographie.")

tia.slide_recap(prs, "Ce que tu as fait aujourd'hui", [
    "1.  Tu sais faire la différence entre une interface et une plateforme.",
    "2.  Ton check-up est en ligne : un lien, sans compte, réponses rangées.",
    "3.  Ton skill Cartographie lit une ligne et rédige, tu relis.",
    "4.  Ta feuille de route dit jusqu'où monter, et par quoi commencer.",
])

tia.slide_questions(prs)
tia.save(prs, OUTPUT_PATH)
