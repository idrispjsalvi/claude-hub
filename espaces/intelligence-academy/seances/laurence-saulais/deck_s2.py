#!/usr/bin/env python3
"""Laurence SAULAIS, séance 2 (mar. 13 oct. 2026, 9h-11h) : Les visuels, générer et retoucher. Charte TIA."""
import importlib.util
import os

HERE = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.join(HERE, "..", "..", "kit")
_spec = importlib.util.spec_from_file_location("tia", os.path.join(KIT, "lib-slides-python.py"))
tia = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(tia)

OUTPUT_PATH = os.path.join(HERE, "laurence-saulais-s2-visuels.pptx")
KICKER = "SÉANCE 2 / 4 · LAURENCE SAULAIS"

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


prs = tia.new_prs()

# ── Ouverture ────────────────────────────────────────────────────────────────
tia.slide_cover(prs, KICKER, "Les visuels, sans repartir de zéro",
                "Générer, retoucher, poser le texte, décliner",
                "Mardi 13 octobre 2026 · 9h-11h · Idris Salvi")

pipeline("Le parcours", "Quatre séances, on est à la deuxième", [
    "S1 · 2 oct.\nFondamentaux ✓", "S2 · 13 oct.\nVisuels",
    "S3 · 20 oct.\nÉcrits, tableaux, CR", "S4 · 29 oct.\nProjet de bout en bout",
], "Le livrable d'aujourd'hui : votre affiche, retouchée et déclinée en publication.")

content("Le déroulé de ce matin", None, [
    "**1.  Quiz (10 min)",
    "**2.  Vos exercices : trois points (25 min)",
    "**3.  Votre compte Claude (10 min)",
    "",
    "**4.  Les visuels, l'essentiel (15 min)",
    "**5.  La pratique : votre affiche, puis votre flyer piano (45 min)",
    "**6.  Les devoirs (10 min)",
])

# ── 1. Quiz ──────────────────────────────────────────────────────────────────
tia.slide_section(prs, "1", "Quiz d'ouverture", "Quatre questions, tirées de vos propres questions")

notes(quiz(1, "Trois mécanismes distincts : reliez chacun à sa définition.", [
    "A.  Retient vos préférences d'une conversation à l'autre",
    "B.  Réutilise vos échanges pour améliorer les futurs modèles",
    "C.  Prend le temps de raisonner avant de répondre",
], [
    "A = la mémoire  ·  B = l'entraînement  ·  C = le mode Thinking",
    "Votre reformulation par mail était juste : trois réglages, trois effets.",
]), "Laurence a demandé par mail de valider sa compréhension de ces trois notions : elle était "
    "correcte. Le dire franchement, c'est une réponse à son besoin de réassurance.")

notes(quiz(2, "Une question sur la santé de votre mère : « Instant » ou « Temporaire » ?", [
    "A.  Instant : la conversation n'est pas conservée",
    "B.  Temporaire : hors historique, hors entraînement, effacée après 30 jours",
    "C.  Les deux reviennent au même",
], [
    "B. « Instant » est un modèle rapide (GPT-5.5 Instant), comme « Thinking » :",
    "il ne change rien à la confidentialité. Le bouton à utiliser : Temporaire.",
]), "Point important : dans son fichier, Laurence écrit qu'elle pose désormais ses questions de "
    "santé « en mode Instant ». Instant est le modèle par défaut de ChatGPT depuis mai 2026, ce "
    "n'est pas le chat temporaire. Lui faire montrer à l'écran où elle clique. Depuis fin août 2026, "
    "un chat temporaire peut être ajouté à l'historique après coup, et on peut choisir au départ s'il "
    "utilise la mémoire et les instructions : cela répond à sa question sur la conversion. Il reste "
    "conservé 30 jours côté OpenAI pour la sécurité.")

notes(quiz(3, "Vos infos sont déjà dans la mémoire. Faut-il les répéter dans les instructions ?", [
    "A.  Non, la mémoire suffit",
    "B.  Oui : l'essentiel stable va dans les instructions, la mémoire complète",
    "C.  Oui, tout doit être écrit deux fois",
], [
    "B. Les instructions : ce que VOUS décidez, lu à chaque échange.",
    "La mémoire : ce que l'outil a retenu. Il s'en sert ou non, et peut se tromper.",
]), "Elle pose aussi la question de la phrase « Ces instructions s'appliquent à toutes mes "
    "conversations » : inutile, c'est la définition même des instructions personnalisées. Les 1 500 "
    "caractères gagnés servent mieux ailleurs.")

notes(quiz(4, "Synthèse, puis courrier, sur le même dossier : un projet ou deux ?", [
    "A.  Deux projets : un par type de document",
    "B.  Un projet, et une conversation par tâche",
    "C.  Une seule conversation pour tout",
], [
    "B. Le projet porte le contexte commun : sources, ton, destinataires.",
    "Chaque conversation porte une tâche. C'est la clé de vos questions.",
]), "C'est la question qui l'a bloquée toute la semaine (« Coordination : synthèses et courriers »). "
    "En séance 1, la formule « un projet par tâche » était trop stricte : la reformuler ici.")

# ── 2. Vos exercices ─────────────────────────────────────────────────────────
tia.slide_section(prs, "2", "Vos exercices", "Trois points en séance, le reste par écrit")

notes(deux_colonnes("Les projets : la règle simple", "Ce qui va dans le projet, ce qui va dans le chat",
    ("Le projet = le contexte commun", [
        "Les instructions (ton, méthode)",
        "Les sources (vos exemples réussis)",
        "Les destinataires habituels",
        "Ce qui ne change pas d'une fois à l'autre",
    ]),
    ("La conversation = une tâche", [
        "« Rédige le courrier au CCAS »",
        "« Fais l'affiche du 14 novembre »",
        "« Adapte ma candidature à cette annonce »",
        "Une conversation neuve à chaque tâche",
    ]),
    "Si deux tâches partagent le même contexte, elles vont dans le même projet."),
    "Partir de son mail du 8/10 : affiches, flyers piano, candidatures spontanées, réponses aux "
    "annonces. La règle tranche toutes ses hésitations sans « usine à gaz ».")

notes(content("Vos projets, simplifiés", "Ma recommandation : trois projets, pas plus", [
    "**1.  Créations graphiques : affiches, flyers, carte de positionnement.",
    "     Dans les sources, un exemple réussi par support, bien nommé.",
    "",
    "**2.  Recherche d'emploi : candidatures spontanées et réponses aux annonces.",
    "     CV et carte en sources. Vous collez l'annonce : pas besoin d'agent.",
    "",
    "**3.  Formation IA : vos exercices et vos questions. Bonne idée.",
]), "Sa conclusion était « un projet par support ». Contre-argument : elle se perd déjà dans "
    "l'arborescence. Un projet par support ne se justifie que si ce support revient souvent et a "
    "beaucoup d'exemples propres. Les instructions graphiques actuelles sont trop longues : 10 lignes "
    "suffisent (direction artistique, méthode, validation). Réponse à sa question : oui, ChatGPT "
    "rédige un mail personnalisé à partir de l'annonce collée, un agent n'apporte rien ici.")

notes(content("Le prompt des trois livrables", "Ce qui marche, ce qu'on enlève, ce qu'on garde", [
    "**✅  Contexte, trois livrables, un ton par destinataire, une vérification.",
    "",
    "**✂️  L'étape « mots-clés et prédiction » : inutile pour produire.",
    "C'était un exercice pour comprendre l'IA, pas une étape de travail.",
    "",
    "**➕  Votre ajout « Informations manquantes à vérifier » : à garder",
    "dans toutes vos trames. Il évite que l'IA comble les trous en inventant.",
]), "Elle demande si l'analyse des mots-clés était nécessaire : non, elle vient de la consigne "
    "d'un exercice de l'e-learning sur la prédiction de mots, et elle consomme du contexte. Valoriser "
    "sa trouvaille « Informations manquantes » : c'est exactement le réflexe de vérification.")

notes(content("Votre cadre de confidentialité", "Votre version courte est la bonne", [
    "**✅  Vos quatre questions, écrites sans l'IA : courtes, à vous, applicables.",
    "**⚠️  Remplacer « mode Instant » par « chat Temporaire » partout.",
    "**⚠️  Le chat Temporaire ne rend pas acceptable une donnée nominative.",
    "",
    "**Votre question de fond : que continue-t-on à faire soi-même ?",
    "> L'IA prépare. Vous décidez, vous validez, vous signez.",
]), "Deux minutes de discussion sur sa question de fond, elle y tient (et le programme prévoit "
    "« fixer ses propres limites d'usage »). Sa version rédigée par l'IA est juste sur le fond mais "
    "trop longue pour être appliquée au quotidien.")

content("Vos autres questions", "Réponse écrite après la séance, promis", [
    "**•  Le schéma qui montre le fonctionnement de l'IA",
    "**•  Garder une trace de ce qu'on a validé, et quand",
    "**•  Votre dilemme sur l'entraînement : votre conclusion tient",
    "",
    "**•  Passer à un forfait supérieur pour tester les agents",
    "**•  La limite de 1 500 caractères des instructions",
])

# ── 3. Le compte Claude ──────────────────────────────────────────────────────
tia.slide_section(prs, "3", "Votre compte Claude", "Créé ensemble, réglé avant le premier message")

notes(enonce("Votre compte Claude, en quatre étapes", [
    ("OBJECTIF", "Un compte gratuit, réglé pour protéger vos données"),
    ("LIVRABLE", "Compte créé, entraînement désactivé, préférences écrites"),
    ("DURÉE", "10 min"),
], [
    "Sur claude.ai : « Continuer avec Google » ou avec votre e-mail.",
    "Paramètres › Confidentialité : désactivez « Aider à améliorer Claude ».",
    "Paramètres › Profil : collez l'essentiel de vos instructions ChatGPT.",
    "Test : votre prompt des trois livrables, comparé à la réponse de ChatGPT.",
]), "Depuis fin 2025, pour les comptes personnels (Free, Pro, Max), l'utilisation des conversations "
    "pour l'entraînement est activée par défaut : la désactiver en premier, c'est sa priorité déclarée. "
    "Désactivé, la conservation est de 30 jours. Les libellés exacts des menus peuvent varier : "
    "suivre l'écran. Gemini : même logique, en option pour une photo de fond avec Nano Banana.")

# ── 4. Les visuels, l'essentiel ──────────────────────────────────────────────
tia.slide_section(prs, "4", "Les visuels, l'essentiel", "Ce qu'il faut savoir avant de cliquer")

notes(tableau("Trois générateurs, comparés", ["", "ChatGPT", "Nano Banana", "Midjourney"],
    [2.6, 3.1, 3.1, 3.1], [
    ["Version", "Images 2.5 (sept. 26)", "Nano Banana 2", "V8 (2026)"],
    ["Où", "Dans ChatGPT", "Appli Gemini", "midjourney.com"],
    ["Prix", "Inclus, tous forfaits", "Gratuit, quota/jour", "Payant, sans essai"],
    ["Point fort", "Retouche en dialogue", "Retoucher vos photos", "Esthétique, styles"],
    ["Pour vous", "Votre affiche", "Photo de fond (option)", "Vu en e-learning"],
], "Midjourney : dès 10 $ par mois. On s'en passe : ChatGPT et Gemini suffisent pour vos supports."),
    "ChatGPT Images 2.5 est sorti le 8 septembre 2026 pour tous les utilisateurs : retouches plus "
    "précises, modèles prêts (« Affiche »), retouche par commentaire sur l'image, croquis (@Sketch). "
    "Nano Banana 2 est le générateur d'images de Google dans l'appli Gemini : gratuit avec un quota "
    "quotidien, téléchargement en 1K sans abonnement, très bon pour modifier une photo existante. "
    "Midjourney V8 : le plus esthétique, moodboards pour un style constant, mais aucun essai gratuit "
    "sur le site (seulement l'appli niji · journey, au style manga). Basic à 10 $ par mois, 8 $ en annuel.")

notes(pipeline("Écrire un prompt d'image", "Cinq ingrédients, dans cet ordre", [
    "1. Sujet\nquoi, qui", "2. Style\nphoto, aquarelle…", "3. Composition\ncadrage, place libre",
    "4. Ambiance\nlumière, couleurs", "5. Format\nA4, carré 1:1",
], "Le même réflexe que contexte, consigne, format : décrire ce qu'on voit."),
    "C'est la méthode de prompt de la séance 1 appliquée à l'image. Un prompt d'image décrit une "
    "scène, pas une intention : « une affiche qui donne envie » ne dit rien, « des fauteuils en arc "
    "de cercle autour d'un piano » dit tout. Laurence connaît le vocabulaire de la direction "
    "artistique : l'inviter à l'utiliser.")

notes(content("Un prompt d'image complet, en exemple", None, [
    "` Affiche A4 portrait pour un après-midi musical en résidence seniors.",
    "` Style : illustration aquarelle douce, tons crème et bleu nuit.",
    "` Composition : un piano à gauche, des fauteuils en arc de cercle.",
    "` Ambiance : lumière chaude d'après-midi, atmosphère conviviale.",
    "` Laisser le tiers supérieur vide pour le titre. Aucun texte.",
    "",
    "**« Aucun texte » : le texte, on le pose ensuite dans Canva.",
]), "Exemple fictif, à adapter à son événement réel. La place laissée vide pour le titre "
    "prépare l'étape Canva.")

notes(deux_colonnes("Générer ou retoucher ?", "Deux gestes différents",
    ("Générer", [
        "Vous partez d'une description",
        "Tout peut changer d'un essai à l'autre",
        "Pour trouver une idée, un style",
    ]),
    ("Retoucher", [
        "Vous partez d'une image existante",
        "Un seul élément change",
        "Pour améliorer sans repartir de zéro",
    ]),
    "Pour retoucher : dites ce qui change ET ce qui ne doit pas bouger."),
    "La confusion classique : demander une correction dans un nouveau message de génération, et "
    "obtenir une image entièrement différente. Retoucher, c'est partir de l'image et la nommer.")

notes(content("La retouche ciblée dans ChatGPT", "Quatre gestes", [
    "**1.  Cliquez sur l'image pour l'ouvrir en grand.",
    "**2.  Sélectionnez la zone (pinceau), ou posez un commentaire dessus.",
    "**3.  Décrivez le changement, puis ce qui reste identique.",
    "",
    "**4.  Vérifiez HORS de la zone : visages, texte, bords.",
    "L'outil régénère l'image entière : le reste peut bouger un peu.",
]), "Ce n'est pas une retouche au pixel comme dans Photoshop : ChatGPT recrée l'image en gardant "
    "le plus possible l'original. Images 2.5 a nettement amélioré ce point, mais il faut toujours "
    "contrôler. Si ça dérive : revenir à la version précédente dans la conversation, une seule "
    "retouche par message, et formuler ce qui ne doit pas bouger.")

notes(content("Image plate ou design en calques ?", None, [
    "**ChatGPT, Gemini : une image « plate », le texte fait partie du dessin.",
    "Fautes possibles, et rien n'est modifiable après coup.",
    "",
    "**Canva AI, plugin Canva : un design en calques, le texte reste du texte.",
    "Titre, date, lieu : modifiables à la main, à tout moment.",
    "",
    "**Donc : le visuel où vous voulez, le texte toujours dans Canva.",
]), "Ses propres instructions graphiques parlaient déjà de « fidélité des textes » : c'est la "
    "réponse. Une image générée par ChatGPT ou Gemini est un fichier image unique : pour corriger "
    "une date, il faut regénérer. Dans Canva, chaque texte est un calque qu'on corrige au clavier.")

notes(deux_colonnes("Canva : deux façons d'utiliser l'IA", None,
    ("Canva AI, dans Canva", [
        "Bouton « Canva AI » dans l'éditeur",
        "Décrivez l'affiche : il la compose",
        "Textes et images en calques séparés",
        "« Change le titre » : seul le titre bouge",
        "Gratuit : nombre d'usages IA limité",
    ]),
    ("Le plugin Canva, dans ChatGPT", [
        "Connecté une fois à votre compte Canva",
        "« Canva, crée un flyer A5 pour… »",
        "Un vrai design Canva, dans le chat",
        "Textes modifiés en dialoguant",
        "« Ouvrir dans Canva » pour exporter",
    ]),
    "Dans les deux cas, le texte reste du vrai texte : on le corrige à la main."),
    "Canva AI 2.0 a été lancé le 16 avril 2026 (Canva Create), d'abord en aperçu : il s'appuie sur "
    "le « Canva Design Model » et produit des designs en calques, pas une image figée. Quand on lui "
    "demande une modification, seul l'élément visé change. Sur le forfait gratuit, le nombre "
    "d'utilisations de l'IA est limité (les chiffres publiés varient) : vérifier le forfait de "
    "Laurence. Le plugin Canva dans ChatGPT : création, aperçu et modification de designs Canva "
    "dans la conversation (annonce Canva du 3 juin 2026) ; il suffit d'écrire « Canva » dans le "
    "prompt. Disponible en France (vérifié par Idris). C'est la réponse à sa question « comment "
    "connecter GPT à Canva ». Dans Canva, Gomme magique et Modification magique retouchent aussi "
    "une zone d'image.")

notes(pipeline("La chaîne complète", "De l'idée au support prêt à diffuser", [
    "1. Brief\nmessage, public", "2. Générer\nsans texte", "3. Retoucher\nune zone à la fois",
    "4. Canva\ntexte en calques", "5. Décliner\nA4, carré, story", "6. Vérifier\nvos critères",
], "Chaque étape se valide avant la suivante."),
    "C'est aussi la trame de la séance 4 (projet de bout en bout) : la poser maintenant.")

tia.slide_recap(prs, "Les visuels", [
    "1.  Un prompt d'image décrit une scène : sujet, style, composition, ambiance, format.",
    "2.  Retoucher, ce n'est pas regénérer : dire ce qui change et ce qui reste.",
    "3.  Après chaque retouche, on vérifie hors de la zone.",
    "4.  Le visuel dans ChatGPT ou Gemini, le texte dans Canva, en calques.",
    "5.  Canva AI et le plugin Canva composent un design modifiable.",
    "6.  Pas besoin de Midjourney pour vos supports.",
])

# ── 5. La pratique ───────────────────────────────────────────────────────────
tia.slide_section(prs, "5", "La pratique", "Partage d'écran : vous faites, je montre")

notes(enonce("Exercice 1 · Partie A : retoucher", [
    ("OBJECTIF", "Améliorer votre affiche du week-end sans repartir de zéro"),
    ("LIVRABLE", "Une version retouchée, validée sur vos critères"),
    ("DURÉE", "20 min"),
], [
    "Partagez l'écran : l'affiche, et ce qui vous gêne encore (3 points max).",
    "Projet Créations graphiques › nouvelle conversation › importez l'affiche.",
    "Point 1 : sélectionnez la zone, décrivez le changement et ce qui reste.",
    "Vérifiez hors de la zone. Puis point 2, puis point 3 : un par message.",
    "Gardez la meilleure version : téléchargez-la.",
]), "Laisser Laurence faire. Reprendre la main seulement pour montrer la sélection la première "
    "fois. Si l'affiche contient beaucoup de texte généré, on passera vite à la partie B.")

notes(content("Les phrases à adapter", None, [
    "` Dans la zone sélectionnée, [le changement]. Ne modifie rien",
    "` d'autre : ni les couleurs, ni le cadrage, ni le texte.",
    "",
    "` Recrée exactement ce visuel sans aucun texte, en gardant",
    "` le haut de l'image dégagé pour le titre.",
    "",
    "` Décline ce visuel au format carré 1:1 pour une publication :",
    "` même style, même palette, aucun texte.",
]), "Ces phrases sont des trames : les crochets se remplacent par sa demande. Elle peut les "
    "enregistrer dans les instructions du projet Créations graphiques.")

notes(enonce("Exercice 1 · Partie B : texte et formats", [
    ("OBJECTIF", "Un support propre, texte fiable, en deux formats"),
    ("LIVRABLE", "Affiche A4 et publication carrée, prêtes à diffuser"),
    ("DURÉE", "15 min"),
], [
    "Demandez à ChatGPT la version sans texte, puis téléchargez-la.",
    "Canva › nouveau design A4 › importez l'image en fond.",
    "Canva AI : « Ajoute titre, date, heure et lieu, lisibles de loin. »",
    "Vérifiez : chaque texte est un calque, corrigez à la main si besoin.",
    "Canva AI : « Décline ce design en publication carrée. »",
]), "Si son quota d'IA Canva est épuisé ou si Canva AI n'est pas disponible sur son forfait : "
    "poser le texte à la main, puis Redimensionner (Canva Pro) ou créer un format carré et y "
    "copier les éléments. Relire ensuite avec la check-list de la slide suivante.")

notes(content("Avant de valider : vos critères", "Tirés de vos propres instructions graphiques", [
    "**☐  La hiérarchie : on lit d'abord quoi, puis quand, puis où.",
    "**☐  Les textes exacts : date, heure, lieu, contact, relus un par un.",
    "**☐  Le blanc tournant : des marges, de l'air, rien de collé au bord.",
    "",
    "**☐  Pas d'élément décoratif qui n'apporte rien (pictos, effets).",
    "**☐  Lisible de loin pour l'affiche, sur un téléphone pour la publication.",
]), "Ce sont ses propres critères (instructions « CRÉATIONS GRAPHIQUES ») : les lui rendre "
    "sous forme de check-list montre qu'elle les a déjà, il suffit de les appliquer.")

notes(enonce("Bonus · Votre flyer piano, depuis ChatGPT", [
    ("OBJECTIF", "Tester le plugin Canva dans ChatGPT sur un vrai support"),
    ("LIVRABLE", "Un flyer modifiable dans Canva, prêt à finir"),
    ("DURÉE", "10 min"),
], [
    "Dans ChatGPT, connectez Canva à votre compte (une seule fois).",
    "Écrivez : « Canva, crée un flyer A5 avec ce texte : [titre, date, lieu] »",
    "Ajustez en dialoguant : « titre plus court », « date plus visible ».",
    "Ouvrez dans Canva pour finir et exporter. Comparez avec l'exercice 1.",
]), "C'est la réponse concrète à sa question « connecter GPT à Canva ». La connexion se fait sur "
    "SON compte Canva : c'est elle qui valide l'autorisation. Option si le temps le permet : une "
    "photo de fond générée avec Nano Banana dans Gemini (gratuit, quota par jour, téléchargement "
    "en 1K), importée ensuite dans le design. Rappel du cadre : pas de photo de résidents "
    "identifiables (droit à l'image).")

# ── 6. Les devoirs ───────────────────────────────────────────────────────────
tia.slide_section(prs, "6", "Les devoirs", "Pour la séance 3, mardi 20 octobre")

content("Devoirs · à produire", None, [
    "**1.  Finir l'affiche et sa version publication, avec le prompt utilisé",
    "**2.  Le flyer piano complet : visuel IA et texte posé dans Canva",
    "**3.  Ranger vos projets ChatGPT : trois, instructions de 10 lignes max",
    "",
    "**À m'envoyer d'ici le lundi 19 octobre, dans un seul fichier.",
])

content("Devoirs · e-learning et séance 3", None, [
    "**1.  « Claude : les fondamentaux » (votre compte est prêt)",
    "**2.  « Claude pour Excel » : la séance 3 parle des tableaux",
    "**3.  « Focus Midjourney & Nano Banana » : les vidéos Nano Banana",
    "",
    "**Pour la S3 : un vrai cas d'écrit (courrier, candidature) anonymisé,",
    "**et un tableau de suivi que vous tenez ou aimeriez tenir.",
    "",
    "Certification : pas encore d'information, je vous tiens au courant.",
])

tia.slide_questions(prs)
tia.save(prs, OUTPUT_PATH)
