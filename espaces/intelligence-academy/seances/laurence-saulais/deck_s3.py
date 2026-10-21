#!/usr/bin/env python3
"""Laurence SAULAIS, séance 3 (mar. 20 oct. 2026, 9h-11h) : écrits, tableaux et CV avec Claude. Charte TIA.

Fonctionnalités vérifiées le 19/10/2026 :
- Claude for Excel : claude.com/docs/office-agents/excel (Pro, Max, Team, Enterprise ; Excel sur le web,
  Windows avec Microsoft 365, Mac ; pas Excel 2016/2019 en licence perpétuelle).
- Création de fichiers .xlsx dans le chat : support.claude.com, « Create and edit files with Claude » (06/08/2026).
- Limites Pro : support.claude.com, « What is the Pro plan? » et « How do usage and length limits work? ».
- Connecteurs : support.claude.com, « Use connectors to extend Claude's capabilities » (Personnaliser › Connecteurs).
- Cowork : « Claude Cowork and chat are one Claude » (16/09/2026), « Get started with Claude Cowork ».
- Prospection B2B : cnil.fr, « La prospection commerciale par courrier électronique » (10/06/2026).
"""
import importlib.util
import os

HERE = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.join(HERE, "..", "..", "kit")
_spec = importlib.util.spec_from_file_location("tia", os.path.join(KIT, "lib-slides-python.py"))
tia = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(tia)

OUTPUT_PATH = os.path.join(HERE, "laurence-saulais-s3-ecrits-tableaux.pptx")
KICKER = "SÉANCE 3 / 4 · LAURENCE SAULAIS"

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
    tia.add_textbox(slide, tia.Inches(0.7), tia.Inches(y), tia.Inches(12.0), tia.Inches(0.45),
                    note, font_size=18, bold=True, color=tia.C_TEAL)
    return slide


def content(header, subtitle, bullets):
    check_titles(header, subtitle)
    for line in bullets:
        # Consolas est plus large : 70 caractères tiennent sur une ligne.
        assert not line.startswith("` ") or len(line) <= 72, f"Ligne de code trop longue : {line}"
        assert len(line.lstrip("*")) <= MAX_CHARS, f"Ligne trop longue ({len(line)}) : {line}"
    blocks = tia._split_into_blocks(bullets)
    n_lines = sum(len(b) for b in blocks)
    top = 2.55 if subtitle else 1.7
    bottom = top + n_lines * 0.57 - 0.12 + (len(blocks) - 1) * 0.26
    assert bottom <= 6.0, f"Slide « {subtitle or header} » trop pleine (bas à {bottom:.2f}\")"
    return tia.slide_content(prs, header, subtitle, bullets)


def quiz(num, question, options, reponse):
    """Deux slides : la question et ses choix en cartes grises, puis la même avec la réponse."""
    header = f"Quiz · Question {num} / 4"
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
        tia.add_textbox(slide, tia.Inches(0.7), tia.Inches(1.55), tia.Inches(11.9), tia.Inches(0.8),
                        question, font_size=24, bold=True, color=tia.C_TITLE)
        y = 2.5
        for o in options:
            tia.add_rounded_rect(slide, tia.Inches(0.7), tia.Inches(y), tia.Inches(11.9), tia.Inches(0.58),
                                 fill_color=tia.C_GRAY_BG)
            tia.add_textbox(slide, tia.Inches(0.95), tia.Inches(y + 0.08), tia.Inches(11.5), tia.Inches(0.42),
                            o, font_size=19, color=tia.C_BODY)
            y += 0.7
        if with_answer:
            tia.add_rounded_rect(slide, tia.Inches(0.7), tia.Inches(4.75), tia.Inches(11.9), tia.Inches(1.15),
                                 fill_color=tia.C_TEAL)
            yy = 4.85
            for r in reponse:
                tia.add_textbox(slide, tia.Inches(0.95), tia.Inches(yy), tia.Inches(11.5), tia.Inches(0.42),
                                r, font_size=18, bold=True, color=tia.C_WHITE)
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
        tia.add_textbox(slide, tia.Inches(x + 0.15), tia.Inches(y), tia.Inches(w - 0.2), tia.Inches(0.4),
                        titre, font_size=18, bold=True, color=tia.C_TEAL)
    tia.add_rect(slide, tia.Inches(0.7), tia.Inches(y + 0.45), tia.Inches(11.9), tia.Inches(0.03), tia.C_GOLD)
    y += 0.55
    for n, row in enumerate(rows):
        if n % 2 == 0:
            tia.add_rect(slide, tia.Inches(0.7), tia.Inches(y), tia.Inches(11.9), tia.Inches(0.5), tia.C_GRAY_BG)
        for i, (x, w, texte) in enumerate(zip(xs, largeurs, row)):
            assert len(texte) <= int((w - 0.3) * 8.5), f"Cellule trop longue ({len(texte)}) : {texte}"
            tia.add_textbox(slide, tia.Inches(x + 0.15), tia.Inches(y + 0.06), tia.Inches(w - 0.2), tia.Inches(0.38),
                            texte, font_size=16, bold=(i == 0), color=tia.C_TITLE if i == 0 else tia.C_BODY)
        y += 0.5
    if note:
        assert len(note) <= 95, f"Note trop longue ({len(note)}) : {note}"
        tia.add_textbox(slide, tia.Inches(0.7), tia.Inches(y + 0.25), tia.Inches(11.9), tia.Inches(0.5),
                        note, font_size=17, bold=True, color=tia.C_TEAL)
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
    tia.add_rect(slide, tia.Inches(6.45), tia.Inches(top), tia.Inches(0.03), tia.Inches(0.6 + n_max * 0.52), tia.C_GOLD)
    for x, (titre, lignes) in ((0.7, gauche), (6.75, droite)):
        assert len(lignes) <= 5
        assert len(titre) <= 34, f"Titre de colonne trop long ({len(titre)}) : {titre}"
        tia.add_textbox(slide, tia.Inches(x), tia.Inches(top), tia.Inches(5.5), tia.Inches(0.45),
                        titre, font_size=21, bold=True, color=tia.C_TEAL)
        y = top + 0.65
        for l in lignes:
            assert len(l) <= 44, f"Ligne de colonne trop longue ({len(l)}) : {l}"
            tia.add_textbox(slide, tia.Inches(x), tia.Inches(y), tia.Inches(5.6), tia.Inches(0.42),
                            l, font_size=18, color=tia.C_BODY)
            y += 0.52
    if note:
        assert len(note) <= 95, f"Note trop longue ({len(note)}) : {note}"
        assert top + 0.8 + n_max * 0.52 + 0.45 <= 6.0, f"Colonnes trop pleines : {header}"
        tia.add_textbox(slide, tia.Inches(0.7), tia.Inches(top + 0.8 + n_max * 0.52), tia.Inches(11.9), tia.Inches(0.45),
                        note, font_size=18, bold=True, color=tia.C_GOLD)
    return slide


def enonce(header, cadre, steps):
    """Slide d'exercice (type 10 de la charte) : un bandeau gris Objectif / Livrable / Durée,
    puis les étapes numérotées (numéro teal en gras, texte foncé)."""
    check_titles(header, None)
    assert len(cadre) == 3 and len(steps) <= 5
    slide = tia.blank_slide(prs)
    tia.add_header(slide, header)
    tia.add_rounded_rect(slide, tia.Inches(0.7), tia.Inches(1.55), tia.Inches(11.9), tia.Inches(1.25),
                         fill_color=tia.C_GRAY_BG)
    col_w = [4.6, 5.0, 1.9]
    x = 0.95
    for (label, texte), w in zip(cadre, col_w):
        assert len(texte) <= 2 * (w - 0.2) * 8, f"Cadre trop long ({len(texte)}) : {texte}"  # 2 lignes à 16pt
        tia.add_textbox(slide, tia.Inches(x), tia.Inches(1.65), tia.Inches(w - 0.2), tia.Inches(0.35),
                        label, font_size=14, bold=True, color=tia.C_GOLD)
        tia.add_textbox(slide, tia.Inches(x), tia.Inches(1.98), tia.Inches(w - 0.2), tia.Inches(0.75),
                        texte, font_size=16, color=tia.C_TITLE)
        x += w
    y = 3.1
    for n, step in enumerate(steps, 1):
        assert len(step) <= 74, f"Étape trop longue ({len(step)}) : {step}"
        tb = slide.shapes.add_textbox(tia.Inches(0.7), tia.Inches(y), tia.Inches(11.9), tia.Inches(0.45))
        tf = tb.text_frame; tf.word_wrap = True
        p = tf.paragraphs[0]
        r = p.add_run(); r.text = f"{n}.  "
        r.font.name = tia.FONT; r.font.size = tia.Pt(19); r.font.bold = True; r.font.color.rgb = tia.C_TEAL
        r = p.add_run(); r.text = step
        r.font.name = tia.FONT; r.font.size = tia.Pt(19); r.font.color.rgb = tia.C_BODY
        y += 0.57
    return slide


def decision(header, rows, note):
    """Questions à plat : une question par ligne, une flèche or, la réponse en pastille teal."""
    check_titles(header, None)
    assert len(rows) <= 4 and len(note) <= 95
    slide = tia.blank_slide(prs)
    tia.add_header(slide, header)
    y = 1.6
    for question, reponse in rows:
        assert len(question) <= 56, f"Question trop longue ({len(question)}) : {question}"
        assert len(reponse) <= 26, f"Réponse trop longue ({len(reponse)}) : {reponse}"
        tia.add_rounded_rect(slide, tia.Inches(0.7), tia.Inches(y), tia.Inches(7.7), tia.Inches(0.78), fill_color=tia.C_GRAY_BG)
        tia.add_textbox(slide, tia.Inches(0.95), tia.Inches(y + 0.17), tia.Inches(7.3), tia.Inches(0.45),
                        question, font_size=19, color=tia.C_TITLE)
        tia.add_textbox(slide, tia.Inches(8.45), tia.Inches(y + 0.12), tia.Inches(0.5), tia.Inches(0.5),
                        "→", font_size=26, bold=True, color=tia.C_GOLD, align=tia.PP_ALIGN.CENTER)
        tia.add_rounded_rect(slide, tia.Inches(9.0), tia.Inches(y), tia.Inches(3.6), tia.Inches(0.78), fill_color=tia.C_TEAL)
        tia.add_textbox(slide, tia.Inches(9.1), tia.Inches(y + 0.18), tia.Inches(3.4), tia.Inches(0.45),
                        reponse, font_size=18, bold=True, color=tia.C_WHITE, align=tia.PP_ALIGN.CENTER)
        y += 0.95
    tia.add_textbox(slide, tia.Inches(0.7), tia.Inches(y + 0.15), tia.Inches(11.9), tia.Inches(0.45),
                    note, font_size=18, bold=True, color=tia.C_TEAL)
    return slide


prs = tia.new_prs()

# ── Ouverture ────────────────────────────────────────────────────────────────
tia.slide_cover(prs, KICKER, "Écrits, tableaux et CV",
                "Un tableau de suivi, un CV adapté à une offre",
                "Mardi 20 octobre 2026 · 9h-11h · Idris Salvi")

notes(pipeline("Le parcours", "Quatre séances, on est à la troisième", [
    "S1 · 2 oct.\nFondamentaux ✓", "S2 · 13 oct.\nVisuels ✓",
    "S3 · 20 oct.\nÉcrits, tableaux", "S4 · 29 oct.\nProjet complet",
], "Aujourd'hui : Claude au travail sur vos deux dossiers réels."),
    "Module 3 du programme : les écrits, les tableaux, les comptes-rendus. Ancré sur ses deux "
    "demandes du 19/10 : sa liste d'établissements (Word et Excel) et son CV à adapter à une offre.")

content("Le déroulé de ce matin", None, [
    "**1.  Quiz (5 min)",
    "**2.  Vos retours d'exercices (10 min)",
    "**3.  Claude Pro : vos questions (15 min)",
    "",
    "**4.  Pratique 1 : du Word au tableau de suivi (40 min)",
    "**5.  Pratique 2 : votre CV adapté à une offre (35 min)",
    "**6.  Bonus : un compte-rendu de réunion (10 min)",
    "**7.  Les devoirs (5 min)",
])

# ── 1. Quiz ──────────────────────────────────────────────────────────────────
tia.slide_section(prs, "1", "Quiz d'ouverture", "Quatre questions : votre semaine et l'e-learning")

notes(quiz(1, "Votre bandeau en PNG, envoyé à @Canva : pourquoi ça bloque ?", [
    "A.  Il faut un abonnement Canva payant",
    "B.  Le connecteur modifie un design Canva, pas une image",
    "C.  Le fichier est trop lourd",
], [
    "B. Un PNG n'a pas de calques : il faut d'abord en faire un design Canva.",
    "Votre solution, la conversion en éléments modifiables, est la bonne.",
]), "Son docx, exercice 2 : la réponse de ChatGPT (« le fichier joint est une image, pas le design "
    "Canva modifiable ») l'a laissée perplexe. C'est l'explication. Elle a trouvé seule la parade.")

notes(quiz(2, "Gemini : vous coupez « Conserver l'activité ». Que perdez-vous ?", [
    "A.  Rien : seul l'entraînement s'arrête",
    "B.  L'historique de vos discussions",
    "C.  La génération d'images",
], [
    "B. Un seul réglage pour l'historique et l'entraînement. Coupé, Google garde 72 h.",
    "Votre lecture était juste. Gemini : des images, jamais de donnée personnelle.",
]), "Source : sa propre capture de Paramètres › Activité dans les applications Gemini (19/10) : "
    "« En conservant votre activité, vous pouvez reprendre vos discussions […] et contribuer à "
    "l'amélioration des services Google ». Désactivé, Google conserve 72 h. Sa déduction est juste.")

notes(quiz(3, "Pourquoi garder ChatGPT à côté de Claude Pro ?", [
    "A.  Claude rédige moins bien",
    "B.  Claude ne génère pas d'images",
    "C.  ChatGPT retient mieux le contexte",
], [
    "B. Vidéo 1 de l'e-learning Claude : pas de génération d'images chez Claude.",
    "Votre choix d'hier est le bon : Claude pour écrire, ChatGPT pour les images.",
]), "E-learning « Claude : les fondamentaux », vidéo 1 (Claude vs ChatGPT vs Gemini) : génération "
    "d'images, mode vocal avancé et analyse vidéo ne sont pas les points forts de Claude ; l'écriture "
    "et l'analyse, si. Elle a pris Claude Pro le 19/10 et garde ChatGPT Go pour les images.")

notes(quiz(4, "Limite atteinte en 5 heures : qu'est-ce qui consomme le plus ?", [
    "A.  Les longues conversations avec un modèle puissant",
    "B.  Le nombre de projets créés",
    "C.  Les instructions personnalisées",
], [
    "A. Plus le modèle est puissant et l'échange long, plus vous consommez.",
    "On voit tout à l'heure comment faire durer votre forfait Pro.",
]), "Vidéo 1 de l'e-learning : « plus le modèle est puissant, plus il va consommer des tokens ». "
    "Elle a atteint la limite du forfait gratuit le 19/10 après-midi (mail « Décision : souscription "
    "abonnement pro CLAUDE »).")

# ── 2. Vos retours ───────────────────────────────────────────────────────────
tia.slide_section(prs, "2", "Vos retours d'exercices", "Ce que vous avez trouvé, ce qui a coincé")

notes(deux_colonnes("Votre semaine de pratique", "Votre document du 19 octobre",
    ("Ce qui marche", [
        "Un projet, une conversation par tâche",
        "« Modifier » : corrections à la lettre",
        "Le texte rendu modifiable dans Canva",
        "Vos prompts gardés pour la suite",
    ]),
    ("Ce qui a coincé", [
        "@Canva bloqué sur une image PNG",
        "Web et appli : deux historiques",
        "Télécharger un fichier depuis Work",
        "Le flyer de Gemini, raté",
    ]),
    "Votre méthode tient. Il reste à choisir un seul endroit où travailler."),
    "Son projet ChatGPT « MAILINGS RENCONTRE PIANO » : conversation 1 stratégie et brief, "
    "conversation 2 le flyer, conversation 3 le bandeau. Exactement la logique vue en S2. "
    "Le flyer est sorti juste du premier coup grâce à un brief préparé en amont.")

notes(pipeline("Corriger un visuel de ChatGPT", "Votre méthode, à garder telle quelle", [
    "1. ChatGPT\ncrée le visuel", "2. Canva\nle rend modifiable",
    "3. Corriger\nun seul élément", "4. Vérifier\ndans l'éditeur",
], "Gardez l'image intacte : ne rendez modifiable que ce qui doit changer."),
    "C'est sa conclusion, reformulée : la conversion complète en calques peut dégrader la "
    "typographie ; mieux vaut ne rendre modifiables que les éléments qui changent. Elle nuance ce "
    "qu'on disait en S2 (« image plate, rien de modifiable ») : le reconnaître. Nom exact de la "
    "fonction Canva non vérifié (aide Canva inaccessible le 19/10) : reprendre ses mots, « conversion "
    "en éléments modifiables ». Elle note qu'il faut un abonnement pour les corrections par l'IA de Canva.")

notes(deux_colonnes("Qui fait quoi, désormais", None,
    ("Claude Pro, appli ordinateur", [
        "Rédiger : mails, courriers, CV",
        "Analyser : offres, documents",
        "Tableaux : Excel, avec l'add-in",
        "Canva : par le connecteur",
        "Projets, skills et Cowork",
    ]),
    ("ChatGPT Go, appli ordinateur", [
        "Générer un visuel",
        "Le retoucher avec « Modifier »",
        "L'enregistrer : clic droit sur l'image",
        "Rester en mode Chat pour les images",
    ]),
    "Un outil par usage, une interface par outil : vous ne cherchez plus."),
    "Choix d'Idris : l'appli ordinateur en priorité pour les deux, pour les skills et les "
    "fonctions en plus. Ses difficultés venaient du va-et-vient web / appli : conversations Work "
    "invisibles sur le web, téléchargements compliqués dans Work. Sa question « à quoi sert Work ? » : "
    "faire agir ChatGPT sur des fichiers de l'ordinateur, comme Cowork chez Claude. Avec Claude Pro, "
    "c'est Claude qui jouera ce rôle. « Luna 6 » dans Work : non vérifié, à regarder sur son écran. "
    "Ses instructions personnalisées « invisibles » dans l'appli : vérifier en mode Chat.")

notes(content("Gemini : vos deux questions", None, [
    "**Activité coupée = plus d'historique : vous avez bien lu.",
    "Un seul réglage couvre l'historique et l'entraînement.",
    "",
    "**« Validation de Mon activité » : un mot de passe en plus",
    "pour consulter votre historique. Rien à voir avec l'entraînement.",
    "",
    "**Donc : Gemini pour des images, jamais pour une donnée personnelle.",
]), "Ses deux captures (docx du 19/10). Le second réglage protège l'accès à « Mon activité » "
    "(validation supplémentaire), utile si quelqu'un utilise son ordinateur : facultatif. Gemini "
    "propose aussi un chat temporaire. Son flyer Gemini, « à pleurer » : confirme le choix de ChatGPT "
    "pour ses supports.")

# ── 3. Claude Pro ────────────────────────────────────────────────────────────
tia.slide_section(prs, "3", "Claude Pro : vos questions", "Vos réglages, votre liste du 19 octobre, vos limites")

notes(content("Trois réglages à vérifier", "Dans les paramètres de Claude, cinq minutes", [
    "**☐  Confidentialité : l'aide à l'amélioration des modèles, désactivée.",
    "Vous l'aviez coupée sur le compte gratuit : on vérifie qu'elle l'est encore.",
    "",
    "**☐  Capacités : « Exécution de code et création de fichiers », activée.",
    "C'est ce qui permet à Claude de vous rendre un vrai fichier Excel.",
    "",
    "**☐  Le bon compte : l'appli ordinateur affiche bien « Pro ».",
]), "Paramètres › Confidentialité (option d'amélioration des modèles) et Paramètres › Capacités. "
    "Centre d'aide, « Create and edit files with Claude » (06/08/2026) : création de fichiers .xlsx, "
    ".docx, .pptx, .pdf sur tous les forfaits, activée par défaut en Free, Pro et Max ; 30 Mo par "
    "fichier. Elle a créé son compte en S2 avec l'entraînement désactivé : le passage au Pro ne "
    "devrait rien changer, mais on regarde.")

notes(deux_colonnes("Les limites du forfait Pro", "Visibles dans Paramètres › Utilisation",
    ("Deux compteurs", [
        "Session : remise à zéro toutes les 5 h",
        "Semaine : tous modèles confondus",
        "Web, appli, Excel : même compteur",
    ]),
    ("Pour faire durer", [
        "Une conversation par tâche",
        "Une nouvelle quand ça s'allonge",
        "Vos documents dans un projet",
        "Opus pour le difficile, sinon Sonnet",
    ]),
    "Un document rangé dans un projet compte moins que s'il est recollé."),
    "Centre d'aide (mis à jour la semaine du 19/10/2026) : « What is the Pro plan? » : limite par "
    "session remise à zéro toutes les cinq heures, plus une limite hebdomadaire sur tous les "
    "modèles ; le suivi est dans Paramètres › Utilisation. « How do usage and length limits work? » : "
    "claude.ai, Claude Desktop et Claude Code comptent dans la même limite ; conseils : projets, "
    "instructions courtes, désactiver la réflexion étendue et les connecteurs inutiles, nouvelle "
    "conversation quand l'échange s'allonge. « Usage limit best practices » : le contenu d'un projet "
    "mis en cache compte moins. Le choix du modèle vient de l'e-learning (vidéo 1).")

notes(decision("Vos questions sur le module", [
    ("Pas de « Recherche web » dans le menu « + » ?", "Elle est automatique"),
    ("L'icône Cowork ne fait rien ?", "Demandez, simplement"),
    ("Excel et PowerPoint : introuvables ?", "Chercher le bon nom"),
    ("Importer la mémoire de ChatGPT ?", "Oui, en triant avant"),
], "Le point commun : vous avez la nouvelle version de Claude, sans modes."),
    "Son mail du 19/10 au soir (« CLAUDE LES FONDAMENTAUX : questions pour demain en séance »). Elle a "
    "demandé de ne pas répondre par écrit : tout se traite ici, en partage d'écran. Les vidéos de "
    "l'e-learning montrent l'ancienne interface, d'où ses écarts.")

notes(content("La nouvelle version de Claude", None, [
    "**Depuis le 16 septembre, Chat et Cowork ne font plus qu'un.",
    "Plus de mode à choisir : décrivez la tâche dans la conversation.",
    "**La recherche web aussi est automatique : plus de bouton dans « + ».",
    "",
    "**L'icône Cowork ne répond pas ? Mettez l'appli à jour.",
    "claude.com/download, puis redémarrez l'appli.",
    "**Windows Pro ? Rien de tel chez Anthropic : Windows 10 ou plus.",
]), "Centre d'aide : « Claude Cowork and chat are one Claude » (16/09/2026), déploiement progressif "
    "en commençant par Pro et Max ; signe qu'on l'a : le champ de message n'affiche plus « Chat » et "
    "« Cowork ». « Use Claude Cowork on web, desktop and mobile » : « there's no Cowork option to "
    "select » ; « If you don't see the Cowork option in the message box, update the app ». « Get "
    "started with Claude Cowork » : Cowork exige la dernière version de Claude pour Windows "
    "(claude.com/download). « Enable and use web search » : « If you have the new Claude experience, "
    "there's no web search toggle » ; Claude cherche quand c'est utile. Windows : « Installing Claude "
    "Desktop » demande Windows 10 ou plus ; depuis le 6/10, les nouvelles tâches Cowork Pro et Max "
    "tournent dans le cloud. Dossiers autorisés : Paramètres › Dossiers de confiance. Faire vérifier "
    "en direct : si son champ de message affiche encore « Cowork », elle a l'ancienne version.")

notes(content("Votre mémoire Claude", None, [
    "**Générer la mémoire à partir des conversations : bon choix.",
    "Claude retient des sujets ; vous les relisez dans Paramètres › Mémoire.",
    "Santé, religion, politique : jamais retenus, sauf si vous l'activez.",
    "",
    "**Importer la mémoire de ChatGPT : oui, en trois temps.",
    "1. Paramètres › Mémoire › Importer : copiez le prompt dans ChatGPT.",
    "2. Ajoutez-y : « sans rien sur ma santé ni sur ma famille ».",
    "3. Collez la réponse dans Claude, puis relisez les sujets créés.",
]), "Centre d'aide, « Use Claude's chat search and memory » (mis à jour la semaine du 19/10) : "
    "réglage « Generate memory from chats » dans Paramètres › Mémoire, activé par défaut en Free, Pro "
    "et Max ; mémoire en sujets (Topics) modifiables ou supprimables ; sujets sensibles (santé, "
    "religion, politique…) exclus par défaut, sauf « Include sensitive topics in memory ». « Import and "
    "export your memory from Claude » : Paramètres › Mémoire › « Start import », prompt fourni à coller "
    "dans ChatGPT, qu'on peut personnaliser pour exclure le sensible, puis « Add to memory » ; pas de "
    "relecture avant l'enregistrement, on relit après dans le panneau Mémoire. Fonction expérimentale ; "
    "Claude peut ne pas garder les détails personnels sans lien avec le travail. Pourquoi trier : elle a "
    "posé dans ChatGPT des questions de santé concernant sa mère (S2). Ses instructions sont déjà "
    "recopiées depuis la S2 : l'import complète, il ne remplace pas.")

tia.slide_recap(prs, "Claude Pro, vos questions", [
    "1.  Claude pour écrire et analyser, ChatGPT pour les images.",
    "2.  L'appli ordinateur, pour chaque outil : un seul historique.",
    "3.  Plus de mode à choisir : demandez, Claude cherche et agit.",
    "4.  La mémoire : importée triée, relue dans Paramètres › Mémoire.",
    "5.  Une conversation par tâche, vos documents dans un projet.",
])

# ── 4. Pratique 1 ────────────────────────────────────────────────────────────
tia.slide_section(prs, "4", "Pratique 1 : du Word au tableau de suivi",
                  "Votre liste d'établissements, prête pour les relances")

notes(tableau("Excel : dans le chat ou dans Excel ?", ["", "Dans le chat Claude", "L'add-in dans Excel"],
    [2.6, 4.65, 4.65], [
    ["Où", "Dans Claude, fichier joint", "Un panneau Claude dans Excel"],
    ["Ce qu'il rend", "Un nouveau fichier à télécharger", "Le classeur ouvert, modifié"],
    ["L'original", "Jamais touché", "Modifié, il prévient avant"],
    ["Idéal pour", "Convertir, créer, nettoyer", "Faire vivre un tableau existant"],
    ["Aujourd'hui", "A : le Word devient Excel", "B : le tableau de suivi"],
], "Les deux sont inclus dans votre forfait Pro et puisent dans le même compteur."),
    "Chat : création de fichiers sur tous les forfaits, l'original n'est jamais modifié, on "
    "télécharge un nouveau fichier. Add-in (claude.com/docs/office-agents/excel) : Pro, Max, Team, "
    "Enterprise ; Claude lit et modifie le classeur ouvert, sur plusieurs onglets ; tri, filtres, "
    "mise en forme conditionnelle, listes déroulantes ; « Claude warns you before overwriting existing "
    "data ». Pas de macros ni VBA. Même limite d'usage que le compte. L'e-learning le résume : avant, "
    "« il fallait retélécharger le Excel derrière ».")

notes(content("Vos contacts : ce que vous confiez", "Trois minutes avant d'ouvrir le fichier", [
    "**contact@, accueil@ : adresses d'établissement, sans souci.",
    "**Nom et mail direct d'une personne : donnée personnelle.",
    "Ne confiez que les colonnes utiles, entraînement désactivé.",
    "",
    "**Démarcher un professionnel par mail : possible sans accord préalable,",
    "si le message concerne son métier et propose de se désinscrire.",
]), "Sa question du 19/10 : « données non anonymisées puisqu'il s'agit d'un fichier de contacts ». "
    "CNIL, « La prospection commerciale par courrier électronique » (10/06/2026) : entre "
    "professionnels, pas de consentement préalable si le message est « en rapport avec la profession "
    "de la personne démarchée », avec information et opposition simple et gratuite (lien de "
    "désinscription) ; les adresses génériques (contact@, info@) ne sont pas soumises à ces règles. "
    "Pour ses prochains mailings : un lien ou une phrase pour se désinscrire.")

notes(enonce("Pratique 1 · A : du Word à l'Excel", [
    ("OBJECTIF", "Votre liste d'établissements dans un vrai tableau"),
    ("LIVRABLE", "Un fichier .xlsx propre, une ligne par établissement"),
    ("DURÉE", "15 min"),
], [
    "Nouvelle conversation Claude, hors projet : joignez votre fichier Word.",
    "Collez le prompt de conversion (je l'envoie dans le chat de la visio).",
    "Vérifiez l'aperçu : une ligne par établissement, rien d'inventé.",
    "Lisez la liste des établissements sans mail ni téléphone.",
    "Téléchargez le fichier .xlsx et ouvrez-le dans Excel.",
]), "On suppose que « convertir » veut dire passer du Word à l'Excel : le lui faire confirmer en "
    "ouvrant l'exercice. Si elle a aussi un Excel, le prompt prévoit la fusion et les doublons. "
    "Prompt complet dans s3-a-coller.md.")

notes(content("Pratique 1 · A : le prompt", None, [
    "` Voici la liste des établissements que je démarche (fichier joint).",
    "` Transforme-la en fichier Excel, une ligne par établissement.",
    "` Garde chaque information dans sa colonne. N'invente rien :",
    "` une information absente reste vide.",
    "` Si je joins deux fichiers, fusionne-les et signale les doublons.",
    "` À la fin, liste les établissements sans mail ni téléphone.",
]), "Version courte du prompt de la fiche. La règle « n'invente rien » et la liste des manques "
    "reprennent son réflexe « Informations manquantes à vérifier » de la S1.")

notes(pipeline("Installer Claude dans Excel", "Un seul complément, aussi pour PowerPoint", [
    "1. Marketplace\nMicrosoft", "2. Chercher « Claude\nfor Microsoft 365 »",
    "3. « Obtenir\nmaintenant »", "4. Excel › Accueil\n› Compléments", "5. Connexion\navec votre compte",
], "Pas « Claude by Anthropic » : le complément s'appelle « Claude for Microsoft 365 »."),
    "Son mail du 19/10 : échec de l'installation Excel et PowerPoint, alors qu'elle a Claude Pro et "
    "Microsoft 365. Elle cherchait « Claude by Anthropic » (consigne donnée par Claude lui-même). "
    "claude.com/docs/office-agents (Excel et PowerPoint) : une seule fiche, « Claude for Microsoft 365 » "
    "sur Microsoft Marketplace (AppSource, WA200010725), qui couvre Excel, PowerPoint, Word et Outlook ; "
    "« Get it now » (Obtenir maintenant), puis ouvrir Excel, activer le complément (Accueil › "
    "Compléments sous Windows) et se connecter avec son compte Claude. Prérequis : Windows avec "
    "abonnement Microsoft 365, build 16.0.13127.20296 ou plus ; sinon Excel sur le web. La doc ne "
    "couvre pas le dépannage côté particulier : si ça bloque encore, essayer Excel sur le web. "
    "Méfiance : prendre le complément publié par Anthropic.")

notes(enonce("Pratique 1 · B : le tableau de suivi", [
    ("OBJECTIF", "Savoir chaque semaine qui relancer, sans chercher"),
    ("LIVRABLE", "Le tableau de suivi de votre mailing de Noël"),
    ("DURÉE", "25 min"),
], [
    "Installez l'add-in, puis ouvrez Claude dans votre fichier Excel.",
    "Collez le prompt du tableau de suivi (dans le chat de la visio).",
    "Contrôlez : vos données d'origine n'ont pas bougé.",
    "Saisissez deux ou trois dates d'envoi, puis sélectionnez ces lignes.",
    "Demandez : « Quels établissements dois-je relancer cette semaine ? »",
]), "C'est le livrable « tableau de suivi » du module 3, sur son vrai mailing de Noël envoyé le "
    "19/10. Sélectionner une plage avant de poser la question : Claude sait de quelles lignes on "
    "parle (astuce de l'e-learning). Laisser l'autorisation des actions sur « demander » au début.")

notes(content("Pratique 1 · B : le prompt", None, [
    "` Ce classeur est ma liste d'établissements pour mon mailing de Noël.",
    "` Ajoute quatre colonnes : Date d'envoi, Relance prévue, Réponse,",
    "` Prochaine action. Relance prévue : date d'envoi + 10 jours.",
    "` Réponse : liste déroulante (En attente, Intéressé, Devis envoyé,",
    "` Pas intéressé), avec une couleur par réponse.",
    "` Ne modifie aucune donnée existante.",
]), "Listes déroulantes (validation des données) et mise en forme conditionnelle font partie de ce "
    "que l'add-in sait faire (doc Claude for Excel). Si elle préfère un autre délai de relance, "
    "elle change le chiffre.")

# ── 5. Pratique 2 ────────────────────────────────────────────────────────────
tia.slide_section(prs, "5", "Pratique 2 : votre CV adapté à une offre", "Tout dans Claude, jusqu'à Canva")

notes(pipeline("Une candidature, de l'offre au CV", "Six étapes, votre validation au milieu", [
    "1. L'offre\nlien ou texte", "2. L'analyse\nattentes clés",
    "3. Propositions\navant / après", "4. Votre « go »\nrien avant",
    "5. Canva\nla copie du CV", "6. Relecture\npuis export PDF",
], "Claude propose, vous décidez : aucune modification avant votre « go »."),
    "Le même déroulé qu'en S2 pour le projet Candidatures de ChatGPT, transposé dans Claude, que "
    "Laurence juge plus pertinent pour sa recherche d'emploi (mail du 19/10).")

notes(deux_colonnes("Le projet « Recherche d'emploi »", "Ce qui reste, ce qui change à chaque offre",
    ("Le projet : ce qui reste", [
        "Instructions : votre démarche",
        "Fichiers : CV, carte de positionnement",
        "Vos candidatures réussies, en exemple",
        "La règle : rien d'inventé",
    ]),
    ("La conversation : chaque offre", [
        "Le lien ou le texte de l'offre",
        "Spontanée ou réponse à une annonce",
        "Vos remarques sur le poste",
        "Une conversation par offre",
    ]),
    "Vous n'apportez que la nouveauté : le projet connaît déjà votre parcours."),
    "Instructions de projet : réservées aux forfaits payants, elle est en Pro. Elles s'ajoutent aux "
    "Instructions pour Claude du compte (Paramètres) : ne pas répéter la même règle aux deux endroits. "
    "Si elle a déjà un projet Candidatures dans ChatGPT, elle peut en recopier les instructions.")

notes(enonce("Pratique 2 · L'énoncé", [
    ("OBJECTIF", "Un CV adapté à une offre réelle, sans rien inventer"),
    ("LIVRABLE", "La copie de votre CV modifiée dans Canva, en PDF"),
    ("DURÉE", "35 min"),
], [
    "Personnaliser › Connecteurs › « + » › Canva › Connecter.",
    "Créez le projet : vos instructions, votre CV et votre carte en fichiers.",
    "Nouvelle conversation : l'offre, puis votre prompt préparé.",
    "Validez les propositions une par une, puis dites « go ».",
    "Claude modifie la COPIE dans Canva : relisez-la dans l'éditeur.",
]), "Centre d'aide, « Use connectors to extend Claude's capabilities » : Personnaliser › Connecteurs "
    "› « + » › parcourir › Canva › Connecter, puis se connecter à Canva. Dans une conversation : "
    "« + » › Connecteurs pour l'activer. Canva est un connecteur interactif (« Create and edit "
    "designs ») : le design s'affiche dans la conversation. Fonctionne avec un compte Canva gratuit "
    "(testé par Idris). C'est elle qui donne l'autorisation sur son compte Canva. Elle a préparé son "
    "prompt et la copie du CV : partir des siens ; le modèle de la fiche sert de secours.")

notes(content("Pratique 2 · Le modèle d'instructions", None, [
    "` Pour chaque offre : 1. Résume ses attentes (missions, mots-clés).",
    "` 2. Compare avec mon CV : ce qui correspond, ce qui manque.",
    "` 3. Propose les modifications une par une, avec avant / après.",
    "` 4. Attends mon « go » avant toute modification dans Canva.",
    "` 5. Ne modifie que la copie du CV que je t'indique.",
    "` Règles : n'invente aucune expérience. Signale ce qui est à vérifier.",
]), "À comparer avec ses propres instructions : garder ce qu'elle a écrit, compléter si une étape "
    "manque (surtout 4 et 5). Version complète dans s3-a-coller.md.")

notes(content("Avant d'envoyer : votre relecture", "Quatre contrôles, à chaque candidature", [
    "**☐  Chaque ligne du CV est vraie : rien n'a été ajouté par Claude.",
    "**☐  Les mots-clés de l'offre apparaissent, sans forcer.",
    "",
    "**☐  La mise en page a tenu : rien ne déborde dans Canva.",
    "**☐  L'original est intact, la copie porte le nom de l'offre.",
]), "Le contrôle 1 est le plus important : un CV « optimisé » par l'IA peut glisser une compétence "
    "ou une formulation qu'elle n'a pas. Nommer la copie avec la date et l'offre (sa règle de "
    "nommage de la S2).")

# ── 6. Bonus ─────────────────────────────────────────────────────────────────
tia.slide_section(prs, "6", "Bonus : le compte-rendu", "Si le temps le permet, sinon en devoir")

notes(pipeline("Un compte-rendu instruit", "Vos règles, écrites une fois", [
    "1. Notes brutes\nfictives ici", "2. Vos règles\nformat et ton",
    "3. Le CR\npar Claude", "4. Relecture\npoints sensibles",
], "Points sensibles : des faits, aucun nom de résident, aucun détail médical."),
    "Troisième production du module 3 : « un compte-rendu instruit selon ses règles », avec une "
    "« formulation maîtrisée des points sensibles ». Les notes sont fictives (résidence Les Tilleuls "
    "inventée) : aucune donnée réelle.")

notes(enonce("Bonus · L'énoncé", [
    ("OBJECTIF", "Un compte-rendu prêt à envoyer, rédigé selon vos règles"),
    ("LIVRABLE", "Le CR d'une réunion fictive de préparation"),
    ("DURÉE", "10 min"),
], [
    "Nouvelle conversation Claude : collez les notes fictives.",
    "Ajoutez le prompt et ses règles (dans le chat de la visio).",
    "Relisez les points sensibles : la chute, l'unité protégée, les photos.",
    "Gardez le prompt : il resservira à chacune de vos réunions.",
]), "Notes et prompt dans s3-a-coller.md. Ce qu'on regarde : la chute d'une résidente formulée sans "
    "nom ni détail médical, l'unité protégée, la règle sur les photos (accord écrit), les actions "
    "avec un responsable et une date. Si on manque de temps : en devoir.")

tia.slide_recap(prs, "Ce matin", [
    "1.  Excel : le chat pour convertir, l'add-in pour faire vivre le tableau.",
    "2.  Vos contacts : seulement les colonnes utiles, et un lien pour se désinscrire.",
    "3.  Le projet garde ce qui reste, la conversation apporte la nouveauté.",
    "4.  Claude propose, vous validez : rien ne change avant votre « go ».",
    "5.  Un CV adapté reste un CV vrai : chaque ligne se relit.",
])

# ── 7. Les devoirs ───────────────────────────────────────────────────────────
tia.slide_section(prs, "7", "Les devoirs", "Pour la séance 4, jeudi 29 octobre")

content("Devoirs · à produire", None, [
    "**1.  Votre tableau de suivi à jour : envois et relances notés",
    "**2.  Une vraie candidature, avec le projet « Recherche d'emploi »",
    "**3.  Le compte-rendu, s'il n'a pas été fait en séance",
    "",
    "**À m'envoyer d'ici le mardi 27 octobre, dans un seul fichier.",
])

notes(content("Devoirs · e-learning et séance 4", None, [
    "**1.  « Claude : les fondamentaux » : les vidéos restantes",
    "**2.  « Claude pour Excel », puis « Claude Cowork »",
    "",
    "**Pour la S4 : choisissez un NOUVEAU projet et écrivez son brief.",
    "Piste 1 : votre offre musicale du printemps 2027.",
    "Piste 2 : une animation, dans votre futur poste médico-social.",
    "Votre kit de Noël sert de modèle : on verra ce qui se réutilise.",
]), "Module 4 : « un kit de communication complet et documenté sur un projet réel » et « ce qui se "
    "réutilise d'un projet à l'autre ». Refaire Noël serait redondant : elle l'a déjà produit et "
    "documenté. Les deux pistes sont des propositions : c'est elle qui choisit. Progression "
    "e-learning au 19/10 : « Claude : les fondamentaux » 2 vidéos sur 8.")

tia.slide_questions(prs)
tia.save(prs, OUTPUT_PATH)
