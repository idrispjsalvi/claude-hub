#!/usr/bin/env python3
"""Jenny POMARÈS, séance 1 (lun. 26 oct. 2026, 14h30-16h30) : son Claude en 4 briques. Charte TIA.

Fonctionnalités reprises des vérifications du 19/10/2026 sur le centre d'aide Claude (deck S2 de
Céline) : Instructions pour Claude, instructions et fichiers de projet, skills (Personnaliser ›
Compétences, exécution de code requise), connecteur Microsoft 365. Quiz calé sur le module
« Comprendre l'IA sans jargon » (leçons LLM, system prompt, hallucinations, fenêtre de contexte).
"""
import importlib.util
import os

HERE = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.join(HERE, "..", "..", "kit")
_spec = importlib.util.spec_from_file_location("tia", os.path.join(KIT, "lib-slides-python.py"))
tia = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(tia)

OUTPUT_PATH = os.path.join(HERE, "jenny-pomares-s1-claude-4-briques.pptx")
KICKER = "SÉANCE 1 / 4 · JENNY POMARÈS"
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


def briques(header, subtitle, items):
    """Les 4 briques en cartes côte à côte : numéro or, nom teal, rôle, puis le cas de Jenny."""
    check_titles(header, subtitle)
    assert len(items) == 4
    slide = tia.blank_slide(prs)
    tia.add_header(slide, header)
    tia.add_subtitle(slide, subtitle)
    w, h = 2.8, 3.2
    for n, (nom, role, cas) in enumerate(items):
        assert len(nom) <= 14, f"Nom trop long ({len(nom)}) : {nom}"
        assert len(role) <= 60, f"Rôle trop long ({len(role)}) : {role}"  # 3 lignes à 16pt sur 2.5"
        assert len(cas) <= 40, f"Cas trop long ({len(cas)}) : {cas}"  # 2 lignes
        x = 0.7 + n * (w + 0.233)
        y = 2.5
        tia.add_rounded_rect(slide, I(x), I(y), I(w), I(h), fill_color=tia.C_GRAY_BG)
        tia.add_rect(slide, I(x), I(y), I(w), I(0.08), tia.C_GOLD)
        text(slide, x + 0.2, y + 0.2, w - 0.4, 0.45, str(n + 1), 26, bold=True, color=tia.C_GOLD)
        text(slide, x + 0.2, y + 0.75, w - 0.4, 0.45, nom, 20, bold=True, color=tia.C_TEAL)
        text(slide, x + 0.2, y + 1.25, w - 0.4, 1.1, role, 16, color=tia.C_TITLE)
        text(slide, x + 0.2, y + 2.4, w - 0.4, 0.7, cas, 15, color=tia.C_TEAL_LIGHT)
    return slide


prs = tia.new_prs()

# ── Ouverture ────────────────────────────────────────────────────────────────
tia.slide_cover(prs, KICKER, "Ton Claude, en 4 briques",
                "Instructions, projet, skill, connecteur : sur tes vrais dossiers",
                "Lundi 26 octobre 2026 · 14h30-16h30 · Idris Salvi")

notes(pipeline("Ton parcours", "4 séances, à valider ensemble en fin de séance", [
    "S1 · 26 oct.\nClaude, 4 briques", "S2\nTri des mails",
    "S3\nRegistre échéances", "S4\nDevis et suivi",
], "Aujourd'hui : un Claude qui connaît Pomarès TP, et 4 outils en place."),
    "Arc proposé à partir de l'intro du 16/10 et de ses mails du 16/10 et du 23/10. Les mails "
    "commerciaux (23/10) et le contrôle des factures n'ont pas de séance dédiée : le projet factures "
    "est fait aujourd'hui, l'envoi régulier des mails commerciaux est à placer avec elle. Le programme "
    "TIA prévoyait bilan par chantier et veille AO : elle ne les a pas cités à l'intro.")

notes(content("Le déroulé de cet après-midi", None, [
    "**1.  Quiz : les bases de l'IA (15 min)",
    "**2.  Les 4 briques de Claude, et où vont tes sujets (10 min)",
    "**3.  Brique 1 · Instructions : théorie, puis pratique (15 min)",
    "**4.  Brique 2 · Projet : théorie, puis pratique (30 min)",
    "**5.  Brique 3 · Skill : théorie, puis pratique (20 min)",
    "**6.  Brique 4 · Connecteur : théorie, puis pratique (15 min)",
    "",
    "**7.  Devoirs et suite du parcours (5 min)",
]), "Avant de lancer : son par le téléphone, partage d'écran, application Claude ouverte, forfait "
    "vérifié. Lui dire que son e-learning est sans doute verrouillé jusqu'au début officiel de la "
    "formation (02/11 dans le dossier TIA), à confirmer par TIA ; elle pense qu'on l'a oubliée.")

notes(content("Avant de commencer", "Trois vérifications, deux minutes", [
    "**1.  Le son passe par ton téléphone, l'écran par ton ordinateur.",
    "**2.  L'application Claude est ouverte et connectée.",
    "**3.  Ton forfait : Paramètres › Facturation. Gratuit ou Pro ?",
    "",
    "Pro est nécessaire pour les instructions de projet et les skills.",
]), "Centre d'aide (vérifié pour Céline le 19/10) : les instructions de projet sont réservées aux "
    "forfaits payants ; les skills exigent l'exécution de code (Paramètres › Capacités). Si elle est en "
    "gratuit : lui montrer sur ton écran, et lui conseiller Pro avant la S2. Ne pas citer de prix de "
    "mémoire : Léo lui a parlé d'« autour de 20 euros », à vérifier sur la page de tarifs.")

# ── 1. Quiz ──────────────────────────────────────────────────────────────────
tia.slide_section(prs, "1", "Quiz : les bases de l'IA", "Cinq questions, avant même l'e-learning")

notes(quiz(1, "Un modèle comme Claude ou ChatGPT, c'est…", [
    "A.  Une base de données qui retrouve la bonne réponse",
    "B.  Un modèle qui prédit le mot suivant le plus probable",
    "C.  Un moteur de recherche, comme Google",
], [
    "B. Il écrit mot après mot ce qui est le plus probable, selon le contexte.",
    "Il ne « sait » rien : il peut donc se tromper avec beaucoup d'aplomb.",
]), "Module « IA sans jargon », leçon « Comment fonctionne ChatGPT (les LLM) » : l'image de l'autocomplete "
    "très avancé, plus le mécanisme d'attention qui garde le contexte. Elle verra cette vidéo après le 02/11.")

notes(quiz(2, "Claude t'annonce un prix de tuyau absent de ta grille. Que s'est-il passé ?", [
    "A.  Il a trouvé un tarif plus récent que le tien",
    "B.  Il a écrit un chiffre plausible : une hallucination",
    "C.  Ta grille de prix est forcément fausse",
], [
    "B. La parade : lui faire citer la ligne exacte de la grille, puis vérifier.",
    "C'est la règle qu'on mettra dans ton projet factures tout à l'heure.",
]), "Leçon « Les hallucinations des LLM » : le modèle ne ment pas, il propose toujours une suite, même "
    "fausse ; vérifier les faits importants, demander ses sources. Ne pas reprendre le chiffre de la vidéo "
    "(« moins de 5 % ») : il n'est pas sourcé.")

notes(quiz(3, "La fenêtre de contexte de Claude contient…", [
    "A.  Seulement ta dernière question",
    "B.  Toute la conversation : tes messages, ses réponses, tes fichiers",
    "C.  Tout ce que tu lui as écrit depuis ton inscription",
], [
    "B. À chaque message, Claude relit toute la conversation.",
    "Plus elle s'allonge, plus elle se remplit : elle a une limite.",
]), "Leçon « La fenêtre de contexte » : prompts, historique, pièces jointes et réponses du modèle comptent "
    "tous. Une image pèse environ 1 000 tokens selon la vidéo. Ne pas donner de tailles par forfait : la "
    "vidéo cite des chiffres qui ont pu changer.")

notes(quiz(4, "Dix factures plus tard, les réponses se dégradent. Tu fais quoi ?", [
    "A.  Tu insistes dans la même conversation",
    "B.  Tu repars d'une nouvelle conversation, dans un projet",
    "C.  Tu changes de forfait",
], [
    "B. La conversation trop longue fait oublier le début à Claude.",
    "Dans un projet, ta grille et tes consignes restent là à chaque fois.",
]), "Leçon « La fenêtre de contexte » : quand la conversation déborde, le modèle oublie le début (souvent "
    "les pièces jointes et la consigne principale) sans le signaler. Conseil de la vidéo : rouvrir une "
    "conversation. C'est l'argument du projet : une conversation par facture, la grille toujours chargée.")

notes(quiz(5, "Avant même ta question, Claude a déjà reçu…", [
    "A.  Rien du tout",
    "B.  Les consignes d'Anthropic, puis les tiennes si tu en as écrit",
    "C.  Ton historique ChatGPT",
], [
    "B. C'est le « system prompt ». Tes Instructions pour Claude s'y ajoutent.",
    "D'où la brique 1 : écrire une fois qui tu es, pour toutes tes conversations.",
]), "Leçon « La notion de system prompt » : l'éditeur place ses instructions avant celles de l'utilisateur. "
    "Transition directe vers la partie suivante.")

# ── 2. Les 4 briques ─────────────────────────────────────────────────────────
tia.slide_section(prs, "2", "Ton Claude en 4 briques", "Ce qu'on construit aujourd'hui, sur Pomarès TP")

notes(briques("Les 4 briques", "Du plus large au plus précis", [
    ("Instructions", "Qui tu es et tes règles. Lues dans TOUTES tes conversations.",
     "Pomarès TP, tes clients, ton ton"),
    ("Projet", "Un dossier de travail : ses consignes et ses fichiers.",
     "Contrôle des factures fournisseurs"),
    ("Skill", "Une façon de faire réutilisable, qui produit un livrable.",
     "Tes mails commerciaux"),
    ("Connecteur", "Claude lit tes outils à la source : mails, fichiers, agenda.",
     "Ta messagerie"),
]), "Le fil rouge, à répéter : le projet donne le contexte (QUOI), le skill donne la façon de faire "
    "(COMMENT). Les instructions valent partout, le connecteur apporte ce qui bouge.")

notes(pipeline("Ce que Claude a sous les yeux", "Quand tu écris dans un projet, tout s'additionne", [
    "Instructions\npour Claude", "Instructions\ndu projet", "Fichiers\ndu projet",
    "Tes skills,\ns'ils servent", "Ta demande", "Tes\nconnecteurs",
], "Une règle à un seul endroit : écrite deux fois, elle finit par se contredire."),
    "Centre d'aide (16/09/2026, vérifié le 19/10) : les instructions du compte et du projet s'additionnent ; "
    "les skills ne se chargent que quand ils servent ; les connecteurs donnent accès aux outils. Le tout "
    "occupe la fenêtre de contexte vue au quiz.")

notes(tableau("Tes sujets : où ils vont", ["Ton sujet", "Avec quoi", "Quand"], [5.4, 3.9, 2.6], [
    ["Factures contre grille du chantier", "Projet Claude", "Aujourd'hui"],
    ["Mails commerciaux clients, prospects", "Skill + connecteur", "Aujourd'hui"],
    ["Tri des mails : devis, AO, CV", "Make ou n8n", "Séance 2"],
    ["Échéances : CT, Veritas, visites, EPI", "Registre + rappels", "Séance 3"],
    ["Devis dictés, TVA, suivi des devis", "Selon Batappli", "Séance 4"],
    ["Heures intérimaires, fioul, AdBlue", "À placer", "À décider"],
], "Ta liste du 16 octobre est entièrement rangée : on valide l'ordre en fin de séance."),
    "Reprise de l'intro (16/10) et de ses mails des 16/10 et 23/10. Le relevé d'heures des intérimaires "
    "(chaque lundi) et les commandes de fioul et d'AdBlue n'ont pas encore de séance : les échéances "
    "fournisseurs et les commandes rejoignent naturellement le registre de la S3. L'envoi régulier des "
    "mails commerciaux est aussi à placer.")

# ── 3. Brique 1 : instructions ───────────────────────────────────────────────
tia.slide_section(prs, "3", "Brique 1 : tes instructions", "Écrire une fois qui tu es")

notes(deux_colonnes("Les deux niveaux d'instructions", "Elles s'additionnent, elles ne se remplacent pas",
    ("Instructions pour Claude", [
        "Paramètres › Instructions pour Claude",
        "Lues dans TOUTES tes conversations",
        "Qui tu es, l'entreprise, tes règles fixes",
        "Ex. : « Jamais de prix inventé »",
    ]),
    ("Instructions d'un projet", [
        "Page du projet › Instructions",
        "Lues seulement dans CE projet",
        "Le rôle et le format pour une activité",
        "Ex. : « Tableau des écarts en sortie »",
    ]),
    "Ce qui vaut partout va dans ton compte ; le reste, dans le projet."),
    "Centre d'aide « Understanding Claude's personalization features » (16/09/2026) : Instructions pour "
    "Claude = réglage du compte ; instructions du projet = contexte et règles d'un projet. La mémoire "
    "(Paramètres › Mémoire) existe aussi : Claude y retient seul des sujets, qu'on peut relire et corriger. "
    "On n'y touche pas aujourd'hui.")

notes(content("Ce qu'on met dans tes instructions", "Court, stable, vrai partout", [
    "✅  Qui tu es : DAF de Pomarès TP (Var), grands comptes et particuliers.",
    "✅  Ta façon d'écrire : ton, vouvoiement des clients, signature.",
    "✅  Tes règles : jamais de chiffre inventé, signaler ce qui est déduit.",
    "",
    "❌  Une consigne pour une seule tâche : elle ira dans un projet.",
    "❌  Une méthode que tu répètes : elle deviendra un skill.",
]), "Exemples tirés de l'intro (entreprise familiale, 40 ans, avec son frère ; Veolia, Lyonnaise des Eaux, "
    "mairies ; relance des particuliers). Le vouvoiement des clients est une supposition : la laisser "
    "trancher.")

notes(enonce("Pratique 1 · Tes instructions", [
    ("OBJECTIF", "Que Claude sache qui tu es, sans le lui redire."),
    ("LIVRABLE", "Tes Instructions pour Claude enregistrées, 10 à 15 lignes."),
    ("DURÉE", "10 minutes"),
], [
    "Ouvrir une nouvelle conversation, hors de tout projet.",
    "Coller le prompt d'interview (je te l'envoie dans le chat de la visio).",
    "Répondre aux questions de Claude, une par une.",
    "Relire le texte proposé : enlever ce qui ne vaut pas partout.",
    "Le coller dans Paramètres › Instructions pour Claude, puis enregistrer.",
]), "Prompt complet dans s1-a-coller.md. Test rapide après enregistrement : nouvelle conversation, "
    "« Présente-moi en deux lignes » ; Claude doit citer Pomarès TP sans qu'on le lui dise.")

# ── 4. Brique 2 : projet ─────────────────────────────────────────────────────
tia.slide_section(prs, "4", "Brique 2 : le projet", "Le contrôle des factures fournisseurs")

notes(content("Un projet, c'est quoi ?", "Un dossier de travail pour une activité", [
    "**Des instructions : le rôle de Claude et le format attendu.",
    "**Des fichiers : tes documents de référence, toujours chargés.",
    "**Des conversations : une par facture, la grille déjà là.",
    "",
    "Un fichier téléversé reste figé ; un PDF exporté se lit mieux qu'un scan.",
]), "Centre d'aide « Upload files to Claude » (23/07/2026, vérifié le 19/10) : PDF de 100 pages ou moins lus "
    "avec texte et visuels ; au-delà, texte seul ; 30 Mo maximum par fichier de projet. Un scan passe par "
    "la vision, moins fiable. Un Google Doc ajouté depuis Drive reste synchronisé (projets privés) : "
    "seulement si elle est sous Google.")

notes(pipeline("Le contrôle, étape par étape", "Claude prépare, toi tu décides", [
    "1. La grille\ndu chantier", "2. La facture\ndu mois",
    "3. Claude compare\nligne à ligne", "4. Le tableau\ndes écarts", "5. Tu vérifies\net tu réclames",
], "Les lignes conformes ne t'occupent plus : tu ne regardes que les écarts."),
    "C'est l'usage que la secrétaire fait à la main chaque mois sur des factures de 10 pages, avec des "
    "avoirs tous les mois (intro du 16/10). La grille est négociée par chantier et vaut environ 3 mois.")

notes(enonce("Pratique 2 · Le projet factures", [
    ("OBJECTIF", "Repérer en minutes les écarts entre facture et prix négociés."),
    ("LIVRABLE", "Le projet « Contrôle factures fournisseurs » et un 1er tableau juste."),
    ("DURÉE", "25 minutes"),
], [
    "Projets › Nouveau projet : « Contrôle factures fournisseurs ».",
    "Fichiers du projet : ajouter la grille de prix du chantier.",
    "Dans le projet : coller le prompt d'interview, répondre à Claude.",
    "Coller le texte validé dans les instructions du projet.",
    "Nouvelle conversation : joindre la facture, vérifier 3 lignes.",
]), "Même méthode que la Pratique 1 : elle rédige ses instructions en se faisant interviewer. Si elle n'a "
    "pas sa grille et sa facture : données fictives de s1-a-coller.md, au format tableur (Google Sheet, puis "
    "Fichier › Télécharger › CSV pour l'ajouter au projet). Trois écarts cachés, 433,50 € HT à réclamer. "
    "Étape 5 essentielle : c'est le réflexe du quiz 2. Si l'interview traîne : consigne de secours dans la fiche.")

notes(content("Pratique 2 · L'interview du projet", None, [
    "` Je veux rédiger les instructions de ce projet. Chaque mois, je",
    "` joindrai une facture à comparer à la grille du projet.",
    "` Pose-moi tes questions une par une : qui contrôle, quoi comparer,",
    "` ce qu'est un écart, le format du résultat, ce que j'en fais.",
    "",
    "` Règles : « hors grille » sans prix, toujours citer la ligne",
    "` de la grille, ne rien inventer, signaler une ligne illisible.",
]), "Texte complet dans s1-a-coller.md. Les trois règles sont imposées dans le prompt : la dernière "
    "reprend la parade du quiz 2. L'interview se fait DANS le projet (Claude voit la grille), puis le texte "
    "validé va dans les instructions du projet, et la facture se joint dans une nouvelle conversation. Si "
    "elle veut aussi les quantités contre les bons de livraison : les joindre dans la conversation, pas dans "
    "le projet (ils changent à chaque facture).")

notes(tableau("Pratique 2 · Le résultat attendu", ["Article", "Facturé", "Grille", "Écart"],
    [5.3, 2.2, 2.2, 2.2], [
    ["Tube PVC CR8 Ø200 (ml)", "14,90 €", "13,20 €", "+ 1,70 €"],
    ["Regard béton 1000x1000", "312,00 €", "312,00 €", "conforme"],
    ["Grave 0/31,5 (t)", "24,50 €", "21,80 €", "+ 2,70 €"],
    ["Manchon de raccordement", "8,40 €", "hors grille", "à vérifier"],
], "Exemple sur les données fictives. Toi : tu vérifies chaque écart avant de réclamer."),
    "Chiffres inventés pour l'exercice, cohérents avec la facture fictive de s1-a-coller.md. Ce sont des "
    "ordres de grandeur plausibles, pas des prix de marché.")

# ── 5. Brique 3 : skill ──────────────────────────────────────────────────────
tia.slide_section(prs, "5", "Brique 3 : le skill", "Tes mails commerciaux, à ta façon")

notes(deux_colonnes("Projet ou skill ?", "Le QUOI d'un côté, le COMMENT de l'autre",
    ("Le projet : le contexte", [
        "Une activité : tes factures",
        "Toujours chargé dans ses conversations",
        "Ses instructions et ses fichiers",
        "Ex. : « Contrôle factures »",
    ]),
    ("Le skill : la façon de faire", [
        "Une méthode qui produit un livrable",
        "Chargé seulement quand il sert",
        "Utilisable dans toutes tes conversations",
        "Ex. : « Mail commercial Pomarès TP »",
    ]),
    "Un skill par livrable : plusieurs petits valent mieux qu'un gros."),
    "Centre d'aide « What are skills? » : skills et projets, skills et instructions. Bonne pratique officielle : "
    "un skill par workflow. Claude choisit ses skills en lisant leur description (200 caractères maximum).")

notes(pipeline("Créer un skill en conversation", "Pas une ligne de code à écrire", [
    "1. Tu décris\nta méthode", "2. Claude te pose\nses questions",
    "3. Claude construit\nle skill", "4. Tu testes\net tu corriges",
], "Ton skill apparaît ensuite dans Personnaliser › Compétences."),
    "Claude Academy, « How to create a skill with Claude through conversation » (vérifié le 19/10) : on décrit, "
    "on joint des exemples, on répond aux questions, Claude s'appuie sur son skill « skill-creator ». "
    "Prérequis : exécution de code et création de fichiers activées dans Paramètres › Capacités.")

notes(enonce("Pratique 3 · Ton skill commercial", [
    ("OBJECTIF", "Écrire un mail commercial juste et à ton ton, en 2 minutes."),
    ("LIVRABLE", "Le skill « Mail commercial Pomarès TP », testé sur un client."),
    ("DURÉE", "15 minutes"),
], [
    "Vérifier : Paramètres › Capacités › exécution de code activée.",
    "Nouvelle conversation : coller le prompt de création (slide suivante).",
    "Joindre un mail commercial déjà envoyé, s'il y en a un.",
    "Répondre aux questions de Claude, puis enregistrer le skill.",
    "Tester : « Un mail pour proposer nos services à <client> ».",
]), "Le skill écrit, il n'envoie rien : l'envoi régulier relève d'un outil d'envoi ou de Make / n8n, plus "
    "tard. Tester sur un client existant (pro). Prospection de particuliers : règles CNIL à sourcer avant "
    "d'en parler, ne pas improviser.")

notes(content("Pratique 3 · Le prompt de création", None, [
    "` Je veux créer un skill : « mail commercial Pomarès TP ».",
    "` Il rédige un mail commercial à un client ou à un prospect.",
    "` Pose-moi tes questions une par une : cibles, métiers à mettre",
    "` en avant, ton, longueur, appel à l'action, pièges à éviter.",
    "",
    "` Règles : seulement des chantiers et des références réels,",
    "` signale ce que tu supposes, et une seule demande claire à la fin.",
]), "Texte complet dans s1-a-coller.md. Les règles reprennent celles de ses instructions : dans le skill, "
    "elles s'appliquent même si elle l'utilise hors de son compte habituel.")

# ── 6. Brique 4 : connecteur ─────────────────────────────────────────────────
tia.slide_section(prs, "6", "Brique 4 : le connecteur", "Claude lit ta messagerie, tu gardes la main")

notes(content("Un connecteur, c'est quoi ?", "Claude va chercher l'information à la source", [
    "**Tu relies une fois ton outil : messagerie, agenda, fichiers.",
    "**Claude y lit ce qu'il faut, seulement quand tu le demandes.",
    "**Tu choisis ce qu'il peut faire, outil par outil.",
    "",
    "Aujourd'hui : il lit et il prépare. C'est toi qui envoies.",
    "Microsoft 365 : compte pro, et l'accord de l'administrateur.",
]), "Centre d'aide (vérifié pour Céline le 19/10) : le connecteur Microsoft 365 existe sur tous les forfaits "
    "mais exige un compte pro ou école et l'accord d'un administrateur Entra ; outlook.com et hotmail refusés. "
    "Gmail passe par les connecteurs Google Workspace. Si pomarestp.fr n'est ni chez Microsoft 365 ni chez "
    "Google : pas de connecteur direct, montrer sur ton écran. Emplacement exact (Paramètres › Connecteurs "
    "ou « + » dans la conversation) : à repérer en direct dans son interface.")

notes(enonce("Pratique 4 · Ta messagerie", [
    ("OBJECTIF", "Un mail commercial qui s'appuie sur vos vrais échanges."),
    ("LIVRABLE", "Ta messagerie reliée et un brouillon pour un vrai client."),
    ("DURÉE", "10 minutes"),
], [
    "Relier ta messagerie dans les connecteurs de Claude.",
    "Choisir un client existant à qui proposer un service.",
    "Demander : « Retrouve nos derniers échanges avec <client> ».",
    "Puis : « Avec mon skill, prépare-lui un mail commercial ».",
    "Relire le brouillon, le corriger, l'envoyer toi-même si tu veux.",
]), "En partage d'écran, ses mails clients sont visibles : lui proposer de filtrer avant d'afficher. Si le "
    "connecteur ne passe pas : client fictif de s1-a-coller.md, collé dans la conversation.")

tia.slide_recap(prs, "Tes 4 briques", [
    "1.  Instructions : qui tu es, lu partout. Court et stable.",
    "2.  Projet : une activité, ses consignes, ses fichiers de référence.",
    "3.  Skill : une méthode qui produit un livrable, utilisable partout.",
    "4.  Connecteur : Claude lit tes outils ; tu gardes la main sur l'envoi.",
    "5.  Toujours : faire citer la source, et vérifier les chiffres.",
])

# ── 7. Devoirs ───────────────────────────────────────────────────────────────
tia.slide_section(prs, "7", "Tes devoirs", "D'ici la séance 2")

notes(content("Tes devoirs", "D'ici la séance 2", [
    "**1.  Passer 3 factures du mois dans le projet, avec ta secrétaire.",
    "Noter ce qui est faux ou manquant dans le tableau.",
    "**2.  Préparer 3 mails avec ton skill : client, ancien client, prospect.",
    "Noter ce que tu corriges : on améliorera le skill.",
    "**3.  Dès l'ouverture de l'e-learning : « IA sans jargon », « Claude ».",
    "**4.  Pour la S2 : 5 à 10 mails types reçus (devis, AO, CV).",
]), "Devoir 3 : a priori à partir du 02/11, à confirmer par TIA, comme le remplacement de Claude for Chrome "
    "par un module Make / n8n (toujours sans réponse de Léo). Devoir 4 : demander aussi quelle messagerie "
    "et qui l'administre, si ce n'est pas réglé en séance. Valider l'ordre des séances 2 à 4.")

tia.slide_questions(prs)
tia.save(prs, OUTPUT_PATH)
