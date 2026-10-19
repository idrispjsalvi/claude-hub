#!/usr/bin/env python3
"""Céline LAFITTE, séance 2 (lun. 19 oct. 2026, 10h-12h) : ranger son Claude, créer son premier skill. Charte TIA.

Fonctionnalités vérifiées le 19/10/2026 sur le centre d'aide Claude (support.claude.com) :
fusion Chat/Cowork du 16/09/2026, Instructions pour Claude, mémoire par sujets et par projet,
skills dans Personnaliser › Compétences et dans les compléments Office.
"""
import importlib.util
import os

HERE = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.join(HERE, "..", "..", "kit")
_spec = importlib.util.spec_from_file_location("tia", os.path.join(KIT, "lib-slides-python.py"))
tia = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(tia)

OUTPUT_PATH = os.path.join(HERE, "celine-lafitte-s2-organisation-skills.pptx")
KICKER = "SÉANCE 2 / 4 · CÉLINE LAFITTE"
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


def quiz(num, question, options, reponse):
    """Deux slides : la question et ses choix en cartes grises, puis la même avec la réponse."""
    header = f"Quiz · Question {num} / 5"
    assert len(question) <= 80, f"Question trop longue ({len(question)}) : {question}"
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
    """Grille 3 × 2 de cartes grises : numéro et nom en teal, le rôle, puis un exemple pour Céline."""
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


def arborescence(header, instructions, projets, skills, connecteurs):
    """L'organisation proposée, de haut en bas : instructions (partout), projets (par activité),
    skills (par livrable), connecteurs (ce qui bouge)."""
    check_titles(header, None)
    assert len(projets) == 4 and len(skills) == 4
    slide = tia.blank_slide(prs)
    tia.add_header(slide, header)
    # Étage 1 : les instructions pour Claude, lues partout.
    tia.add_rounded_rect(slide, I(0.7), I(1.55), I(11.9), I(0.7), fill_color=tia.C_DARK_BLUE)
    assert len(instructions) <= 80
    text(slide, 0.95, 1.67, 11.4, 0.45, instructions, 18, bold=True, color=tia.C_WHITE)
    w, gap = 2.8, (11.9 - 4 * 2.8) / 3
    # Étage 2 : un projet par activité.
    text(slide, 0.7, 2.4, 11.9, 0.35, "PROJETS · un par activité, avec ses instructions et ses fichiers",
         15, bold=True, color=tia.C_GOLD)
    for n, (nom, contenu) in enumerate(projets):
        assert len(nom) <= 16 and len(contenu) <= 26, f"Projet trop long : {nom} / {contenu}"
        x = 0.7 + n * (w + gap)
        tia.add_rounded_rect(slide, I(x), I(2.8), I(w), I(1.15), fill_color=tia.C_TEAL if n % 2 == 0 else tia.C_HEADER_RIGHT)
        text(slide, x + 0.15, 2.88, w - 0.3, 0.4, nom, 17, bold=True, color=tia.C_WHITE)
        text(slide, x + 0.15, 3.28, w - 0.3, 0.6, contenu, 15, color=tia.C_WHITE)
    # Étage 3 : un skill par façon de faire.
    text(slide, 0.7, 4.1, 11.9, 0.35, "SKILLS · un par livrable, utilisables dans tous tes projets",
         15, bold=True, color=tia.C_GOLD)
    for n, nom in enumerate(skills):
        assert len(nom) <= 44, f"Skill trop long : {nom}"
        x = 0.7 + n * (w + gap)
        tia.add_rounded_rect(slide, I(x), I(4.5), I(w), I(0.72), fill_color=None, border_color=tia.C_TEAL)
        text(slide, x + 0.12, 4.56, w - 0.24, 0.6, nom, 16, bold=True, color=tia.C_TEAL, align=tia.PP_ALIGN.CENTER)
    # Étage 4 : les connecteurs.
    assert len(connecteurs) <= 90
    text(slide, 0.7, 5.42, 11.9, 0.45, connecteurs, 17, bold=True, color=tia.C_TEAL_LIGHT)
    return slide


prs = tia.new_prs()

# ── Ouverture ────────────────────────────────────────────────────────────────
tia.slide_cover(prs, KICKER, "Ton Claude, bien rangé",
                "Où va chaque chose, puis ton premier skill de coach",
                "Lundi 19 octobre 2026 · 10h-12h · Idris Salvi")

pipeline("Ton parcours", "4 séances, un fil rouge : ton bilan de compétences", [
    "S1 · 8 oct.\nComprendre ✓", "S2 · 19 oct.\nRanger + 1er skill",
    "S3 · 22 oct.\nLire une séance", "S4 · 28 oct.\nCartographie",
], "Aujourd'hui : ton organisation décidée, et un skill qui travaille comme toi.")

notes(deux_colonnes("Ce que tu m'as écrit", "Ton point d'avancement du 16 octobre",
    ("Ce que tu as avancé", [
        "Claude Pro, l'application ordinateur",
        "Claude dans PowerPoint, Excel et Word",
        "Une formation, sur un masque d'organisme",
        "Gmail et OneDrive connectés",
        "Instructions et mémoire : faites",
    ]),
    ("Ce qui coince", [
        "Décider ton organisation générale",
        "Projet ou skill : où ranger quoi ?",
        "Des skills qui ne te satisfont pas",
    ]),
), "Reprise fidèle de son mail du 16/10. Elle a aussi fini les e-learnings Claude le 17/10 "
   "(fondamentaux, Cowork, Chrome, Excel). Deux devoirs de la S1 ne sont pas confirmés dans son mail : "
   "la base de contexte finalisée et le retour écrit à TIA sur les e-learnings. Lui demander.")

content("Le déroulé de ce matin", None, [
    "**1.  Tour d'horizon : ce que tu as construit (10 min)",
    "**2.  Quiz sur les e-learnings Claude (10 min)",
    "**3.  Où ranger quoi dans Claude (20 min)",
    "",
    "**4.  Pratique 1 : ton organisation, décidée (25 min)",
    "**5.  Pratique 2 : ton skill « synthèse de séance » (40 min)",
    "**6.  Bonus si on avance vite : le questionnaire de valeurs",
    "**7.  Les devoirs (10 min)",
])

# ── 1. Tour d'horizon ────────────────────────────────────────────────────────
tia.slide_section(prs, "1", "Ce que tu as construit", "Partage d'écran : tu me montres")

notes(content("Tour d'horizon : tu me montres", None, [
    "**1.  Ta formation créée dans Claude, sur le masque de l'organisme",
    "**2.  Ton OneDrive réorganisé : comment tu t'y es prise",
    "",
    "**3.  Tes projets et tes skills actuels : ce qui ne te plaît pas",
    "**4.  Tes instructions et ta base de contexte : où elles sont",
]), "On part de ce qu'elle a construit. Repérer pendant le tour : ce qui est rangé au mauvais endroit "
    "(une consigne de tâche dans les instructions générales, une procédure dans un projet). On s'en sert "
    "en Pratique 1. OneDrive : lui demander COMMENT elle l'a connecté. Le connecteur Microsoft 365 existe sur "
    "tous les forfaits mais exige un compte Microsoft pro ou école, avec l'accord d'un administrateur Entra ; "
    "les comptes personnels (outlook.com, hotmail.com, live.com) ne sont pas acceptés (doc Claude, Microsoft "
    "365 connector). Avec son adresse outlook.fr, c'est sans doute le dossier OneDrive synchronisé sur son "
    "ordinateur, ouvert à Claude Code.")

notes(content("Claude sur tes fichiers", "Trois réflexes avant de lui confier un dossier", [
    "**1.  Une copie d'abord, avant toute réorganisation.",
    "**2.  Un dossier précis, jamais tout ton OneDrive.",
    "",
    "**3.  Mode Manuel : Claude te demande avant chaque action.",
    "Il demande aussi avant de supprimer un fichier pour de bon.",
]), "Elle a réorganisé des fichiers avec Claude Code : c'est l'outil qui agit le plus sur l'ordinateur "
    "(l'e-learning le dit). Dans la nouvelle expérience Claude, le réglage de permission du champ de "
    "message propose Auto ou Manuel (Manuel par défaut), et Claude demande avant toute suppression "
    "définitive (centre d'aide, « Claude Cowork and chat are one Claude », 16/09/2026).")

# ── 2. Quiz ──────────────────────────────────────────────────────────────────
tia.slide_section(prs, "2", "Quiz d'ouverture", "Cinq questions : la séance 1 et tes e-learnings Claude")

notes(quiz(1, "Séance 1 : « Le projet donne le contexte, le skill donne… »", [
    "A.  …la mémoire",
    "B.  …la façon de faire",
    "C.  …les fichiers",
], [
    "B. Le projet dit QUOI (ton activité), le skill dit COMMENT (ta méthode).",
    "C'est la clé de tout ce qu'on range aujourd'hui.",
]), "Formule de la S1 (récap du 8/10). Anthropic dit la même chose : les projets portent un contexte "
    "toujours chargé, les skills des procédures chargées seulement quand elles servent.")

notes(quiz(2, "Dans un projet, tes Instructions pour Claude et celles du projet…", [
    "A.  Celles du projet remplacent les tiennes",
    "B.  Elles s'additionnent",
    "C.  Claude ne lit que celles de ton compte",
], [
    "B. Les deux sont lues. D'où la règle : jamais la même consigne aux deux endroits,",
    "sinon elles finissent par se contredire.",
]), "E-learning « Claude, les fondamentaux », vidéo Projects : « les deux s'additionnent ». Vidéo "
    "Paramètres : l'auteur raconte une règle oubliée dans ses préférences qui gâchait des réponses deux mois plus tard.")

notes(quiz(3, "Un document change chaque semaine : comment l'ajouter ?", [
    "A.  Le téléverser à nouveau chaque lundi",
    "B.  L'ajouter depuis Google Drive : il se met à jour tout seul",
    "C.  Le recopier dans les instructions du projet",
], [
    "B. Un fichier téléversé est une photo figée ; un Google Doc relié reste à jour.",
    "PDF : texte et images lus jusqu'à 100 pages ; au-delà, le texte seul.",
]), "PDF, centre d'aide (« Upload files to Claude », 23/07/2026) : Claude analyse texte ET éléments visuels "
    "des PDF de 100 pages ou moins ; de 101 à 1 000 pages, le texte seul. Un PDF scanné de plus de 100 pages "
    "n'a donc rien à lire ; en dessous, il passe par la vision, moins fiable qu'un vrai texte (préférer le PDF "
    "exporté de Word). Fichiers de projet : 30 Mo maximum chacun. La vidéo dit « jamais de PDF scanné » : "
    "c'est plus nuancé. La vidéo Projects and Knowledge Base classe « les données qui changent chaque semaine » parmi les "
    "mauvais candidats : vrai pour un fichier TÉLÉVERSÉ, qui reste figé. Mais le centre d'aide (« Use Google "
    "Workspace connectors ») précise qu'un Google Doc ajouté aux fichiers d'un projet depuis Drive (+ › Drive) "
    "reste synchronisé avec sa dernière version ; option réservée aux projets privés. OneDrive : le connecteur "
    "Microsoft 365 exige un compte pro ou école (les comptes outlook.com, hotmail.com, live.com ne sont pas "
    "acceptés) ; avec son adresse outlook.fr, Céline passera plutôt par Google Drive ou par le téléversement.")

notes(quiz(4, "Tu veux que Claude range un dossier de ton ordinateur. Il te faut…", [
    "A.  Rien : Claude sur le web suffit",
    "B.  L'application Claude ouverte, et l'accès à ce dossier",
    "C.  Le forfait Max",
], [
    "B. Et depuis le 16 septembre, plus besoin de choisir « Cowork » :",
    "tu le demandes dans n'importe quelle conversation.",
]), "Centre d'aide, « Claude Cowork and chat are one Claude » (16/09/2026) : fusion en déploiement "
    "progressif sur Pro et Max. Si son champ de message affiche encore « Chat » et « Cowork », elle a "
    "l'ancienne version, qui marche comme dans la vidéo. L'accès aux fichiers locaux exige Claude Desktop ouvert.")

notes(quiz(5, "Où vois-tu ce que Claude a retenu de toi ?", [
    "A.  Nulle part : c'est automatique",
    "B.  Paramètres › Mémoire : chaque sujet se lit, se corrige, se supprime",
    "C.  Dans les instructions de tes projets",
], [
    "B. Santé, croyances, politique : jamais retenus, sauf si tu l'actives.",
    "La vidéo montre l'ancien emplacement (Confidentialité) : il a changé en août.",
]), "Centre d'aide, mémoire (mise à jour d'octobre 2026) : la mémoire est une liste de sujets dans "
    "Paramètres › Mémoire ; activée par défaut en Free, Pro et Max ; les sujets sensibles sont exclus sauf "
    "option « Include sensitive topics in memory ». Changement annoncé le 25/08/2026.")

# ── 3. Où ranger quoi ────────────────────────────────────────────────────────
tia.slide_section(prs, "3", "Où ranger quoi dans Claude", "Six rangements, un test en quatre questions")

notes(tableau("Depuis les vidéos, ce qui a bougé", ["Dans la vidéo", "Ce que tu vois en octobre 2026"],
    [5.2, 6.7], [
    ["Trois modes : Chat, Cowork, Code", "Chat et Cowork fusionnés, Code à part"],
    ["Préférences personnelles", "Paramètres › Instructions pour Claude"],
    ["Mémoire dans Confidentialité", "Paramètres › Mémoire, par sujets"],
    ["Compétences dans les paramètres", "Personnaliser › Compétences (tes skills)"],
    ["Cowork : fichiers à télécharger", "Claude crée directement dans ton dossier"],
], "Fusion en cours de déploiement : si tu vois encore « Chat » et « Cowork », rien ne presse."),
    "Sources, centre d'aide Claude : « Claude Cowork and chat are one Claude » (16/09/2026), « Understanding "
    "Claude's personalization features » (16/09/2026), « Use skills in Claude », article mémoire (octobre 2026). "
    "Les anciennes « Global instructions » de Cowork sont passées dans Instructions pour Claude : lui faire "
    "vérifier qu'elles n'y sont pas en double.")

notes(pipeline("Ce que Claude a sous les yeux", "Quand tu écris dans un projet, tout s'additionne", [
    "Instructions\npour Claude", "Instructions\ndu projet", "Fichiers\ndu projet", "Mémoire\ndu projet",
    "Tes skills,\ns'ils servent", "Ta demande\net tes connecteurs",
], "Chaque couche a un rôle. Une règle écrite à deux endroits finit par se contredire."),
    "Anthropic : les projets fournissent un contexte toujours chargé ; les skills se chargent seulement "
    "quand elles sont utiles (« progressive disclosure ») ; les connecteurs (MCP) donnent l'accès aux "
    "outils et aux données. Sur un forfait payant, quand les fichiers d'un projet approchent la limite, "
    "Claude passe en mode RAG : il va chercher les passages utiles.")

notes(cartes("Six rangements, six rôles", "Du plus large au plus précis", [
    ("Instructions pour Claude", "Qui tu es, ton style, tes règles valables partout", "Ex. : jamais de nom réel"),
    ("Mémoire", "Ce que Claude retient seul, au fil des échanges", "Ex. : tes outils préférés"),
    ("Projet : instructions", "Le rôle et les règles de Claude pour UNE activité", "Ex. : vouvoiement en bilan"),
    ("Projet : fichiers", "Ses documents : figés si téléversés, à jour si reliés", "Ex. : la trame d'organisme"),
    ("Skill", "Une façon de faire qui produit un livrable, partout", "Ex. : synthèse de séance"),
    ("Connecteurs", "Les données qui bougent, lues à la source", "Ex. : Gmail, ton agenda"),
]), "La mémoire est le seul rangement qu'elle ne remplit pas elle-même : elle le relit et le corrige. "
    "Tout le reste, c'est elle qui décide. Insister sur la colonne de droite : chaque exemple vient de son métier.")

notes(decision("Le test en quatre questions", [
    ("Ça vaut pour TOUT ce que tu fais ?", "Instructions pour Claude"),
    ("Ça vaut pour UNE activité (tes bilans) ?", "Projet"),
    ("C'est une façon de faire, que tu refais ?", "Skill"),
    ("Ça change chaque semaine ?", "Doc relié ou connecteur"),
], "Dans le doute : le plus précis gagne. Une règle de bilan va dans le projet Bilans."),
    "C'est l'outil de décision de la Pratique 1 : on le passe sur chacune de ses tâches. « Doc relié ou "
    "connecteur » : un document qui évolue s'ajoute au projet depuis Google Drive et reste à jour ; une "
    "info qui vit dans un outil (mails, agenda) se lit par un connecteur ; une info du jour se donne "
    "simplement dans la conversation.")

notes(deux_colonnes("Les deux niveaux d'instructions", "Elles s'additionnent, elles ne se remplacent pas",
    ("Instructions pour Claude", [
        "Paramètres › Instructions pour Claude",
        "Lues dans TOUTES tes conversations",
        "Qui tu es, ton style, tes règles fixes",
        "Ex. : « Jamais de nom de bénéficiaire »",
    ]),
    ("Instructions du projet", [
        "Page du projet › Instructions",
        "Lues seulement dans CE projet",
        "Rôle, ton et format pour cette activité",
        "Ex. : « Vouvoiement, [À vérifier] »",
    ]),
    "Une règle, un seul endroit : partout, c'est ton compte ; sinon, c'est le projet."),
    "Centre d'aide (16/09/2026) : Instructions pour Claude = réglage du compte, appliqué à toutes les "
    "conversations ; instructions du projet = contexte, rôle et règles d'un projet, appliqués à ses seules "
    "conversations. Les instructions du projet sont réservées aux forfaits payants : elle est en Pro.")

notes(deux_colonnes("Projet ou skill ?", "Le QUOI d'un côté, le COMMENT de l'autre",
    ("Le projet : le contexte", [
        "Une activité : tes bilans, tes formations",
        "Toujours chargé dans ses conversations",
        "Instructions, fichiers, mémoire",
        "Ex. : « Bilans de compétences »",
    ]),
    ("Le skill : la façon de faire", [
        "Une procédure qui produit un livrable",
        "Chargé seulement quand il sert",
        "Utilisable partout, même dans PowerPoint",
        "Ex. : « Synthèse de séance »",
    ]),
    "Un skill par livrable : plusieurs petits valent mieux qu'un gros."),
    "« What are skills? » (centre d'aide) : skills vs projets, skills vs instructions. Bonne pratique "
    "officielle : « Organize by purpose », un skill par workflow. Une des raisons probables de son malaise "
    "avec ses skills actuels : trop larges, ou du contexte mis à la place d'une méthode.")

notes(content("La mémoire et tes bilans", "Activée par défaut : à régler une fois", [
    "**Claude retient seul ton rôle, tes projets, les personnes de ton travail.",
    "Tu vois et corriges tout dans Paramètres › Mémoire.",
    "",
    "**La mémoire d'un projet peut ressortir dans tes autres conversations.",
    "**Projet Bilans : coupe l'option « mémoire du compte » pour l'isoler.",
]), "Centre d'aide : chaque projet a sa mémoire ; ce qui y est appris peut servir hors projet si la "
    "mémoire est active. Pour isoler : « Use account memory » à désactiver sous Memory, sur la page du "
    "projet (libellé anglais de l'aide, à repérer avec elle dans son interface). Une conversation seule : "
    "« + » › Mémoire, avant le premier message.")

notes(content("Tes données dans Claude Pro", "Ce que tu confies, et comment le protéger", [
    "**Paramètres › Confidentialité : l'option d'amélioration des modèles.",
    "Activée : tes conversations peuvent servir à entraîner Claude.",
    "",
    "**Conversation sensible : « + » › Mémoire coupée, avant le 1er message.",
    "**Et la règle de la S1 : anonymiser AVANT de coller.",
]), "Centre de confidentialité Anthropic (« Is my data used for model training? », 16/03/2026) : sur les "
    "forfaits grand public (Free, Pro, Max), les conversations servent à l'entraînement si l'utilisateur "
    "l'accepte ; les chats incognito n'y servent jamais. Le contenu brut des connecteurs n'est pas utilisé. "
    "Les chats incognito s'ouvrent dans l'ancienne expérience : pas de création de fichiers.")

notes(arborescence("Ton organisation : un point de départ",
    "INSTRUCTIONS POUR CLAUDE · qui tu es, ton style, l'anonymat : lues partout",
    [("Bilans", "Trames, base de contexte"),
     ("Formations", "Masques, supports"),
     ("Coaching", "Managers, tes méthodes"),
     ("Check-up de soi", "Questionnaire, restitution")],
    ["Synthèse de séance", "Synthèse finale de bilan", "Questionnaire de valeurs", "Prompts par poste"],
    "CONNECTEURS · Gmail, OneDrive : les données qui bougent, lues à la source"),
    "Proposition construite sur ses activités connues (RDV d'intro et dossier TIA) : bilans, formations "
    "(attachés de direction, demandeurs d'emploi), coaching managérial, check-up de soi. À ajuster avec elle "
    "en Pratique 1 : c'est elle qui décide. Les skills listés reprennent les livrables du programme "
    "(module 2) ; seule la première est construite aujourd'hui.")

tia.slide_recap(prs, "Où ranger quoi", [
    "1.  Instructions pour Claude : ce qui vaut partout. Court.",
    "2.  Projet : une activité, avec ses instructions et ses fichiers stables.",
    "3.  Skill : une façon de faire, un livrable. Il te suit partout.",
    "4.  Connecteurs : ce qui bouge, lu à la source.",
    "5.  Une règle à un seul endroit, jamais en double.",
])

# ── 4. Pratique 1 ────────────────────────────────────────────────────────────
tia.slide_section(prs, "4", "Pratique 1 : ton organisation", "Tu décides, je challenge")

notes(enonce("Pratique 1 · L'énoncé", [
    ("OBJECTIF", "Décider où va chaque chose, pour ne plus hésiter."),
    ("LIVRABLE", "Ton organisation validée : projets, skills, instructions relues."),
    ("DURÉE", "25 minutes"),
], [
    "Lister tes 8 à 10 tâches récurrentes avec Claude (on les écrit ensemble).",
    "Passer chacune au test des quatre questions, vu en théorie.",
    "Valider tes projets : un par activité, pas un par tâche.",
    "Faire relire tes Instructions pour Claude avec le prompt dédié.",
    "Ranger le reste : dans le bon projet, ou sur ta liste de skills.",
]), "Le prompt de relecture est dans la fiche s2-a-coller.md, à coller dans le chat de la visio. "
    "Si elle hésite sur une tâche, revenir au test : le plus précis gagne.")

notes(tableau("Pratique 1 · Ta grille de tri", ["Ta tâche", "Où la ranger", "Pourquoi"],
    [4.6, 3.3, 4.0], [
    ["Ta synthèse après chaque séance", "Skill", "Même méthode à chaque fois"],
    ["La trame d'un organisme", "Projet : fichiers", "Document stable"],
    ["Vouvoiement dans les bilans", "Projet : instructions", "Propre à cette activité"],
    ["Jamais de nom de bénéficiaire", "Instructions pour Claude", "Vaut partout"],
    ["Tes échanges avec un organisme", "Connecteur Gmail", "Ça bouge chaque semaine"],
], "À toi : tes tâches, une par ligne. On remplit ensemble, en partage d'écran."),
    "Cinq exemples pour lancer la grille, puis ses tâches à elle. Ouvrir un document partagé ou un "
    "artifact pour remplir la grille en direct.")

notes(content("Pratique 1 · Relire tes instructions", None, [
    "Nouvelle conversation, hors projet :",
    "` Voici mes Instructions pour Claude, puis la liste de mes projets.",
    "` Classe chaque phrase : partout, propre à un projet, ou méthode.",
    "` Propose une version courte, sans rien ajouter ni inventer.",
    "",
    "**Ce qui est propre à un projet part dans ses instructions.",
    "**Ce qui est une méthode rejoint ta liste de skills.",
]), "Elle colle ses Instructions pour Claude actuelles sous le prompt. Elle a écrit qu'elles sont "
    "« certainement à revoir » : c'est le moment. Vérifier aussi qu'elles ne doublent pas d'anciennes "
    "« Global instructions » de Cowork, fusionnées dans le même champ.")

# ── 5. Pratique 2 ────────────────────────────────────────────────────────────
tia.slide_section(prs, "5", "Pratique 2 : ton premier skill", "La synthèse de séance, à ta façon")

notes(content("Ce que contient un bon skill", "Ce que Claude va construire avec toi", [
    "**Un nom et une description : c'est elle qui dit QUAND l'utiliser.",
    "200 caractères maximum. Claude choisit ses skills en la lisant.",
    "",
    "**Ta méthode, étape par étape, et un exemple réussi.",
    "**Tes modèles en fichiers joints : la trame de l'organisme.",
]), "Centre d'aide, « How to create custom skills » : description de 200 caractères maximum, décisive "
    "pour le déclenchement ; une tâche répétable par skill ; des exemples ; des fichiers de référence "
    "possibles. Le skill est un dossier avec un fichier SKILL.md : elle n'a pas à l'écrire elle-même.")

notes(pipeline("Créer un skill en conversation", "Pas une ligne de code à écrire", [
    "1. Tu décris\nta méthode", "2. Claude te pose\nses questions",
    "3. Claude construit\nle skill", "4. Tu testes\net tu corriges",
], "Claude s'appuie sur son propre skill de création pour bien le structurer."),
    "Claude Academy, « How to create a skill with Claude through conversation » : on décrit, on joint ses "
    "modèles, on répond aux questions, Claude lit son skill « skill-creator » et livre le skill. Autre voie "
    "réservée au Mac : « Record a skill » (on s'enregistre en train de faire). Pas pour aujourd'hui.")

notes(enonce("Pratique 2 · L'énoncé", [
    ("OBJECTIF", "Un skill qui rédige tes synthèses de séance, à ta façon."),
    ("LIVRABLE", "Le skill « synthèse de séance », testé sur les notes de Mme R."),
    ("DURÉE", "40 minutes"),
], [
    "Vérifier : Paramètres › Capacités › exécution de code activée.",
    "Nouvelle conversation : coller le prompt de création (slide suivante).",
    "Joindre ta trame de synthèse et un exemple réussi, anonymisés.",
    "Répondre aux questions de Claude, puis enregistrer le skill proposé.",
    "Tester dans le projet Bilans : « Synthèse de ces notes » + Mme R.",
]), "Prérequis officiel : les skills exigent « Code execution and file creation » dans Paramètres › "
    "Capacités. Après l'enregistrement, le skill apparaît dans Personnaliser › Compétences, où il "
    "s'active ou se désactive. Si elle n'a pas d'exemple anonymisé sous la main : partir de la trame seule "
    "et de la synthèse de Mme R. faite en S1. Les notes de Mme R. sont dans la fiche (situation inventée).")

notes(content("Pratique 2 · Le prompt de création", None, [
    "` Je veux créer un skill : « synthèse de séance de bilan ».",
    "` Il part de mes notes brutes et rédige la synthèse de séance.",
    "` Pose-moi tes questions une par une : étapes, format, ton, pièges.",
    "` Appuie-toi sur ma trame et mon exemple joints (anonymisés).",
    "",
    "` Règles : rien d'inventé, [À vérifier] sur chaque déduction,",
    "` et une liste finale des points que je relis avant envoi.",
]), "Texte complet dans s2-a-coller.md. Les deux règles de la fin reprennent celles de la S1 : elles "
    "vivent maintenant DANS le skill, plus besoin de les répéter à chaque demande.")

notes(content("Pratique 2 · Le test", None, [
    "**1.  A-t-il servi ? Claude l'indique dans son raisonnement.",
    "**2.  Fidélité : rien d'inventé, chaque déduction en [À vérifier] ?",
    "**3.  Format : ta trame, dans l'ordre, au bon ton ?",
    "**4.  Prête à l'emploi : combien de minutes de retouche ?",
    "",
    "> Un défaut ? Fais corriger le skill, pas seulement la synthèse",
]), "Si le skill ne se déclenche pas : vérifier qu'il est activé (Personnaliser › Compétences), "
    "rendre la description plus précise, ou le demander par son nom. Pour corriger : « Modifie mon skill "
    "synthèse de séance pour que… ». Les fichiers du skill s'ouvrent à côté de la conversation et se "
    "modifient avec « Edit with Claude ».")

notes(content("Ton skill te suit partout", "Une fois activé, dans tous tes outils Claude", [
    "**Dans toutes tes conversations, avec ou sans projet.",
    "**Dans PowerPoint, Excel et Word : tape / et choisis-le.",
    "",
    "**Avec la trame d'un organisme en modèle, Claude la reprend",
    "**à l'identique dans PowerPoint et Excel.",
]), "Centre d'aide, « Use skills in Claude » : les skills activés sont disponibles dans les compléments "
    "Excel, PowerPoint, Word et Outlook (« / » pour les lister). Un skill construit avec un modèle Excel "
    "ou PowerPoint précis : Claude for Excel et PowerPoint charge ce modèle à l'identique. Lien direct avec "
    "sa formation créée sur le masque d'un organisme, et avec le fil rouge (synthèse au format de chaque organisme).")

# ── 6. Bonus ─────────────────────────────────────────────────────────────────
tia.slide_section(prs, "6", "Bonus : le questionnaire de valeurs", "Si on a de l'avance")

notes(enonce("Bonus · Le questionnaire de valeurs", [
    ("OBJECTIF", "Un premier outil pour tes coachés : valeurs, talents, compétences."),
    ("LIVRABLE", "Un questionnaire en Word, prêt à remettre à un coaché."),
    ("DURÉE", "20 minutes"),
], [
    "Dans le projet Bilans : nouvelle conversation, coller le prompt.",
    "Préciser le public : attachés de direction, ou recherche d'emploi.",
    "Relire comme un coaché : clair, sans jargon, faisable en 20 minutes ?",
    "Faire corriger, puis demander le fichier Word final.",
    "Tu le referas souvent ? Ce sera ton 2e skill (devoir).",
]), "Objectif du module 2 du programme : « Créer un premier outil pour vos coachés : le questionnaire de "
    "valeurs, de talents et de compétences techniques ». Si le temps manque, il passe en devoir (déjà prévu).")

notes(content("Bonus · Le prompt", None, [
    "` Crée un questionnaire pour mes coachés, en trois parties :",
    "` mes valeurs, mes talents, mes compétences techniques.",
    "` Public : [attachés de direction / recherche d'emploi].",
    "` Questions ouvertes et échelles de 1 à 5, sans jargon RH.",
    "",
    "` 20 minutes maximum à remplir. Livre-le en fichier Word.",
]), "Le projet Bilans fournit déjà le contexte (base de contexte, ton) : le prompt reste court. "
    "C'est la démonstration concrète de « le projet donne le contexte ».")

# ── 7. Les devoirs ───────────────────────────────────────────────────────────
tia.slide_section(prs, "7", "Les devoirs", "Pour la séance 3, jeudi 22 octobre")

notes(content("Devoirs · avant le 22 octobre", None, [
    "**1.  Mettre en place ton organisation : projets, instructions, skills",
    "**2.  Utiliser ton skill sur 2 vraies séances anonymisées, et le corriger",
    "**3.  Créer seule ton 2e skill : le questionnaire de valeurs",
    "",
    "**4.  Pour la S3 : un transcript de séance anonymisé, accord du coaché",
    "**5.  E-learning « Focus Midjourney & Nano Banana », et ton point le 21",
]), "Trois jours seulement avant la S3 : devoirs courts. Si le bonus a été fait en séance, remplacer le 3 "
    "par « les prompts par poste (attaché de direction, office manager, recherche d'emploi) », autre "
    "objectif du module 2. Le transcript sert la S3 (agents de lecture de séance). Attention : dans l'API, "
    "l'e-learning « Focus Midjourney & Nano Banana » est encore verrouillé (status locked) : le débloquer.")

tia.slide_recap(prs, "Ce que tu as fait aujourd'hui", [
    "1.  Tu sais où ranger chaque chose : le test des quatre questions.",
    "2.  Ton organisation est décidée : un projet par activité, un skill par livrable.",
    "3.  Ton premier skill est testé : tu corriges le skill, pas le résultat.",
    "4.  Tes bilans restent anonymes, jusque dans la mémoire de Claude.",
])

tia.slide_questions(prs)
tia.save(prs, OUTPUT_PATH)
