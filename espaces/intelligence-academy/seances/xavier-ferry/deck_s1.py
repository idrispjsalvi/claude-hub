#!/usr/bin/env python3
"""Xavier FERRY, séance 1 (lun. 19 oct. 2026, 16h30-18h30) : n8n prêt, outil d'analyse FEC fiabilisé,
rapport cartographié. Charte TIA.

Sources : mail de Xavier du 16/10/2026, RDV d'intro du 30/09/2026 (Granola), dossier TIA, son application
d'analyse FEC (v3.0-dev) testée le 19/10 sur les FEC fictifs de fec-fictif/.
Fonctionnalités vérifiées le 19/10/2026 : n8n.io/pricing et docs.n8n.io (essai Cloud, export/import),
hostinger.com/fr/hebergement-n8n (offres VPS), support.claude.com (Claude for Excel), API BODACC (opendatasoft).

⚠️ France Travail : aucun support ne parle de création d'entreprise. On dit « votre outil d'analyse FEC »,
« vos missions », jamais le nom du cabinet.
"""
import importlib.util
import os

HERE = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.join(HERE, "..", "..", "kit")
_spec = importlib.util.spec_from_file_location("tia", os.path.join(KIT, "lib-slides-python.py"))
tia = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(tia)

OUTPUT_PATH = os.path.join(HERE, "xavier-ferry-s1-fiabiliser-automatiser.pptx")
KICKER = "SÉANCE 1 / 4 · XAVIER FERRY"
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
    # La note native de slide_pipeline tombe à 6.4" : on la pose sous les boîtes.
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


def tableau(header, colonnes, largeurs, rows, note=None, subtitle=None):
    """Tableau : en-têtes teal, lignes grises une sur deux."""
    check_titles(header, subtitle)
    assert abs(sum(largeurs) - 11.9) < 0.01 and len(rows) <= 6
    slide = tia.blank_slide(prs)
    tia.add_header(slide, header)
    y = 1.6
    if subtitle:
        tia.add_subtitle(slide, subtitle)
        y = 2.45
    xs = [0.7]
    for w in largeurs[:-1]:
        xs.append(xs[-1] + w)
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
        assert y + 0.75 <= 6.6, f"Tableau trop plein : {header}"
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


def niveaux(header, subtitle, items, note):
    """Trois cartes côte à côte (titre teal, définition, exemple), filet or à gauche."""
    check_titles(header, subtitle)
    assert len(items) == 3 and len(note) <= 95
    slide = tia.blank_slide(prs)
    tia.add_header(slide, header)
    tia.add_subtitle(slide, subtitle)
    w, h, gap = 3.75, 2.55, 0.325
    for n, (nom, role, ex1, ex2) in enumerate(items):
        assert len(nom) <= 22, f"Nom trop long ({len(nom)}) : {nom}"
        assert len(role) <= 60, f"Rôle trop long ({len(role)}) : {role}"    # 2 lignes à 17pt sur 3.4"
        for e in (ex1, ex2):
            assert len(e) <= 30, f"Exemple trop long ({len(e)}) : {e}"
        x = 0.7 + n * (w + gap)
        tia.add_rounded_rect(slide, I(x), I(2.5), I(w), I(h), fill_color=tia.C_GRAY_BG)
        tia.add_rect(slide, I(x), I(2.65), I(0.06), I(h - 0.3), tia.C_GOLD)
        text(slide, x + 0.25, 2.6, w - 0.4, 0.45, nom, 20, bold=True, color=tia.C_TEAL)
        text(slide, x + 0.25, 3.1, w - 0.4, 0.8, role, 17, color=tia.C_TITLE)
        text(slide, x + 0.25, 4.05, w - 0.4, 0.4, ex1, 16, color=tia.C_TEAL_LIGHT)
        text(slide, x + 0.25, 4.45, w - 0.4, 0.4, ex2, 16, color=tia.C_TEAL_LIGHT)
    text(slide, 0.7, 5.35, 11.9, 0.45, note, 18, bold=True, color=tia.C_TEAL)
    return slide


prs = tia.new_prs()

# ── Ouverture ────────────────────────────────────────────────────────────────
tia.slide_cover(prs, KICKER, "Fiabiliser, puis automatiser",
                "Votre outil d'analyse testé, n8n prêt, votre rapport cartographié",
                "Lundi 19 octobre 2026 · 16h30-18h30 · Idris Salvi")

notes(pipeline("Votre parcours", "4 séances, un fil rouge : la pré-analyse d'un IBR", [
    "S1 · 19 oct.\nFiabiliser, outiller", "S2 · 28 oct.\nPré-analyse IBR",
    "S3 · 6 nov.\nBODACC ou reporting", "S4 · à caler\nMise en production",
], "Le programme est une trame : on l'ajuste à vos priorités à chaque séance."),
    "Fil rouge recalé sur le RDV d'intro du 30/09 : la prospection de masse est abandonnée (son modèle "
    "passe par les apporteurs d'affaires et l'appel direct). Priorité : la pré-analyse financière des "
    "IBR (30 à 45 jours aujourd'hui, beaucoup de travail junior répétitif). S3 : signaux BODACC pour une "
    "liste d'appels, ou reporting, à trancher avec lui. S4 : après mon retour le 23/11, ou avant le 11/11. "
    "Point admin : la date de fin du dossier TIA est le 31/10 alors que S3 est le 6/11 ; le dossier est "
    "affiché « terminé » dans l'API. À vérifier côté TIA.")

notes(deux_colonnes("Ce que vous m'avez écrit", "Votre mail du 16 octobre, et où vous en êtes",
    ("Vos trois sujets", [
        "n8n sur votre propre serveur",
        "Votre fichier d'analyse : erreurs Excel",
        "Actualiser un rapport d'activité",
    ]),
    ("Où vous en êtes", [
        "4 modules e-learning terminés",
        "n8n : vidéos vues, exercices en attente",
        "Un outil d'analyse FEC déjà construit",
        "Objectif : accélérer la pré-analyse IBR",
    ]),
    "Aujourd'hui, on traite vos trois sujets, dans cet ordre."),
    "Reprise fidèle de son mail du 16/10 et de l'API TIA : modules terminés (IA sans jargon, Claude "
    "fondamentaux, Cowork, Claude pour Excel), n8n en cours (6 vidéos sur 6, exercices non faits faute "
    "d'instance). Son outil : application HTML locale v3.0-dev qui lit FEC, liasses et relevés et produit "
    "trois classeurs Excel à formules vivantes. Commencer par le féliciter : c'est un travail sérieux.")

content("Le déroulé de la séance", None, [
    "**1.  Quiz d'ouverture (10 min)",
    "**2.  n8n : débloquer vos exercices (20 min)",
    "",
    "**3.  Fiabiliser votre outil d'analyse FEC (45 min)",
    "**4.  Votre rapport : ce qui s'automatise (25 min)",
    "",
    "**5.  Les devoirs pour le 28 octobre (10 min)",
])

# ── 1. Quiz ──────────────────────────────────────────────────────────────────
tia.slide_section(prs, "1", "Quiz d'ouverture", "Cinq questions sur vos quatre modules terminés")

notes(quiz(1, "Commenter le BFR d'un dossier : où Claude risque-t-il le moins d'inventer ?", [
    "A.  Lui demander les ratios moyens du secteur, de mémoire",
    "B.  Lui donner vos chiffres calculés et lui demander de les commenter",
    "C.  Lui demander les textes de loi applicables, avec leurs références",
], [
    "B. Commenter des données fournies : risque très faible.",
    "Chiffres de mémoire, références citées : risque élevé, à vérifier une à une.",
]), "Module « Comprendre l'IA sans jargon », guide sur les hallucinations : tableau des risques (citation "
    "de sources : très élevé ; chiffres précis : élevé ; reformulation d'un texte fourni : très faible). "
    "C'est le principe de la séquence 4 : Claude rédige à partir des chiffres de son outil, il ne les "
    "produit jamais lui-même.")

notes(quiz(2, "Après 40 échanges, Claude oublie vos consignes du début. Pourquoi ?", [
    "A.  Vous avez atteint votre limite d'utilisation de la semaine",
    "B.  Toute la conversation est relue à chaque message : le contexte sature",
    "C.  Claude efface les consignes au bout d'une heure",
], [
    "B. La fenêtre de contexte a une taille finie, pièces jointes comprises.",
    "Une conversation = un sujet. Faites résumer, puis repartez à neuf.",
]), "Module « Comprendre l'IA sans jargon », guide sur la fenêtre de contexte : symptômes de saturation "
    "(oubli des consignes, contradictions) et 5 règles (une conversation par sujet, résumer après 10-15 "
    "échanges, consignes critiques en début de conversation). Utile pour la séquence 3 : un écart par "
    "conversation quand il fait corriger son code.")

notes(quiz(3, "Votre trame de rapport évolue chaque semaine. Comment la donner à un projet ?", [
    "A.  La téléverser à nouveau à chaque nouvelle version",
    "B.  L'ajouter depuis Google Drive : Claude relit toujours la dernière version",
    "C.  La recopier dans les instructions du projet",
], [
    "B. Un fichier téléversé est une copie figée ; un document relié reste à jour.",
    "Pour ce qui vit dans un outil (mails, agenda), c'est un connecteur.",
]), "Centre d'aide Claude (« Use Google Workspace connectors », vérifié le 19/10) : un Google Doc ajouté "
    "aux fichiers d'un projet depuis Drive (+ › Drive) reste synchronisé avec sa dernière version ; option "
    "réservée aux projets privés. Le connecteur Microsoft 365 (OneDrive, SharePoint) exige un compte "
    "Microsoft pro ou école. L'e-learning (synthèse Projects) classe « les données qui changent chaque "
    "semaine » parmi les mauvais candidats : c'est vrai d'un fichier téléversé, pas d'un document relié. "
    "Si la question des PDF vient : un PDF de 100 pages ou moins est lu en entier, texte et visuels ; de "
    "101 à 1 000 pages, le texte seul (centre d'aide « Upload files to Claude », 23/07/2026). Un long PDF "
    "texte se lit donc ; un long PDF scanné (image, sans texte) n'a rien à lire au-delà de 100 pages.")

notes(quiz(4, "Pour que Claude lise les FEC d'un dossier sur votre ordinateur, il vous faut…", [
    "A.  Les téléverser un par un dans Claude sur le web",
    "B.  L'application Claude ouverte, avec accès au dossier concerné",
    "C.  Obligatoirement Claude Code et le terminal",
], [
    "B. Claude ne voit que les dossiers que vous lui ouvrez.",
    "Depuis le 16/09, Chat et Cowork ne font qu'un : demandez-le dans le chat.",
]), "Module « Claude Cowork » : accès aux fichiers locaux via Claude Desktop, seulement aux dossiers "
    "autorisés. Centre d'aide (« Claude Cowork and chat are one Claude », 16/09/2026) : fusion en "
    "déploiement progressif sur Pro et Max ; s'il voit encore « Chat » et « Cowork » séparés, il a "
    "l'ancienne version, qui marche comme dans la vidéo. Données clients : Paramètres › Confidentialité, "
    "option d'amélioration des modèles ; sur les forfaits Free, Pro et Max, les conversations servent à "
    "l'entraînement si elle est acceptée (centre de confidentialité Anthropic, 16/03/2026). Avec des FEC "
    "clients : la vérifier avec lui, ou anonymiser. Son outil d'analyse est 100 % local par conception : "
    "il a déjà ce réflexe.")

notes(quiz(5, "Une formule de votre classeur renvoie une erreur. Le bon réflexe ?", [
    "A.  Abandonner et écrire la formule à la main",
    "B.  Sélectionner la cellule et demander la cause à Claude pour Excel",
    "C.  Recopier tout le classeur dans une conversation Claude",
], [
    "B. Il remonte à la cause de l'erreur, en citant les cellules concernées.",
    "Attention : il modifie le classeur ouvert. Travaillez sur une copie.",
]), "Vidéo « Claude pour Excel » : « sélectionnez la cellule et dites-lui : qu'est-ce qui s'est passé ici ». "
    "Le formateur y conseille aussi de dupliquer l'Excel avant d'autoriser Claude à tout faire. Doc Claude "
    "(claude.com/docs/office-agents/excel, lue le 19/10) : « Identify and resolve errors and their root "
    "causes », citations cliquables au niveau de la cellule. "
    "Transition directe vers la séquence 3.")

# ── 2. n8n ───────────────────────────────────────────────────────────────────
tia.slide_section(prs, "2", "n8n : débloquer vos exercices", "Le Cloud ce soir, votre serveur ensuite")

notes(deux_colonnes("Cloud maintenant, serveur ensuite", "Vous ne perdez rien en commençant sur le Cloud",
    ("n8n Cloud : essai gratuit", [
        "Prêt en 2 minutes, sans carte bancaire",
        "14 jours, 1 000 exécutions",
        "Hébergé par n8n, en Europe (Francfort)",
        "Workspace supprimé si pas d'abonnement",
    ]),
    ("Votre serveur Hostinger", [
        "n8n préinstallé, en un clic",
        "Workflows et exécutions illimités",
        "KVM 2 conseillé : 7,79 €/mois (promo)",
        "Payé d'avance, renouvelé plus cher",
    ]),
    "Vos workflows passent de l'un à l'autre en fichier JSON."),
    "n8n.io/pricing (lu le 19/10/2026) : essai Cloud sans carte bancaire, 1 000 exécutions, 5 exécutions "
    "simultanées, 180 s maximum par exécution ; données hébergées dans l'UE (Francfort). docs.n8n.io "
    "(Cloud free trial) : 14 jours ; à la fin, le workspace expire et est supprimé, 90 jours pour "
    "récupérer ses workflows ; l'essai inclut les fonctions Pro, dont l'assistant IA de n8n (800 crédits). "
    "Version du moment : n8n 2.44 (13/10/2026). Hostinger (hostinger.com/fr/hebergement-n8n, lu le 19/10) : KVM 1 à 5,49 €/mois "
    "(renouvellement 11,99 €), KVM 2 à 7,79 €/mois (renouvellement 14,99 €, badge « le plus populaire »), "
    "packs payés d'avance, la durée exacte du prix promo est à vérifier dans le tunnel de commande. Mon "
    "n8n tourne sur Hostinger : je peux montrer. Ne pas dire « illimité » sans nuance : limité par la "
    "taille du serveur. Hostinger propose aussi un « Managed n8n » (sans administration de serveur, en "
    "déploiement selon les régions, prix non affiché) : à regarder s'il ne veut rien gérer.")

notes(pipeline("Passer du Cloud à votre serveur", "Quatre gestes, le jour où vous migrez", [
    "1. Télécharger\nchaque workflow", "2. L'importer\ndans votre n8n",
    "3. Recréer\nles identifiants", "4. Tester\npuis activer",
], "Les identifiants (comptes, clés) ne voyagent pas dans le JSON : à reconnecter."),
    "docs.n8n.io « Export and import » : menu « … » du workflow › Download (JSON), puis Import from File "
    "(ou copier-coller des nœuds). Le JSON contient le nom et l'ID des identifiants, pas les secrets : "
    "il faut les recréer sur la nouvelle instance. Conseil : migrer AVANT la fin des 14 jours.")

notes(enonce("Pratique 1 · Votre n8n en 15 minutes", [
    ("OBJECTIF", "Un n8n qui marche ce soir, pour faire les exercices du module."),
    ("LIVRABLE", "Un compte n8n Cloud et un premier workflow exécuté puis exporté."),
    ("DURÉE", "15 minutes"),
], [
    "Créer votre compte d'essai sur n8n.io (Get started, sans carte).",
    "Nouveau workflow : déclencheur manuel, puis un nœud Edit Fields.",
    "Edit Fields : société = « Ateliers Lumen », exercice = 2025. Exécuter.",
    "Le télécharger : menu « … » en haut à droite › Download.",
    "Je l'importe en direct sur mon n8n Hostinger : il marche à l'identique.",
]), "Il fait, je guide. Étape 5 : démonstration de la portabilité, en partage d'écran sur mon instance "
    "Hostinger (Import from File). Si la création de compte bloque (mail de confirmation), passer à la "
    "séquence 3 et y revenir à la fin. Il pourra ensuite faire les exercices du module dès ce soir.")

notes(content("Plus tard : votre serveur Hostinger", "Une fois l'offre VPS achetée, dans hPanel", [
    "**1.  Dans hPanel : VPS › votre serveur › Gérer",
    "**2.  Système d'exploitation : choisir le modèle « n8n »",
    "**3.  Valider : Hostinger réinstalle le serveur avec n8n (10 à 15 min)",
    "",
    "**4.  Ouvrir n8n (Gérer l'application) et créer votre compte",
    "**5.  Importer vos workflows, recréer vos identifiants",
]), "Tutoriel Hostinger « How to self-host n8n on Ubuntu » (mis à jour le 29/09/2026) : VPS › Manage › "
    "OS & Panel › Operating System ; chercher n8n (il existe aussi un template « n8n (100+ workflows) ») ; "
    "Change OS ; Hostinger demande de cocher « all my files will be deleted » (le serveur est réinstallé : "
    "sans conséquence sur un VPS neuf) et de choisir le mot de passe administrateur du serveur (root) ; "
    "Confirm. Puis VPS Overview › Manage App, et création du compte propriétaire. Sauvegarde "
    "hebdomadaire automatique par défaut. Libellés traduits par moi : l'interface française peut "
    "différer, à suivre avec lui en partage d'écran le jour venu.")

# ── 3. Fiabiliser l'outil ────────────────────────────────────────────────────
tia.slide_section(prs, "3", "Fiabiliser votre outil d'analyse", "Le tester sur un dossier dont on connaît les réponses")

notes(content("Un outil se teste sur un dossier connu", None, [
    "**Sur un vrai dossier, une erreur ne se voit pas : vous ignorez la réponse.",
    "Sur un dossier fictif, chaque écart à la réponse attendue est une erreur.",
    "",
    "**Aujourd'hui : une PME fictive, deux FEC, cinq anomalies glissées.",
    "Je connais les réponses. Vous découvrez ce que votre outil en voit.",
    "",
    "> Mieux vaut trouver l'erreur ici que devant un administrateur judiciaire",
]), "Le principe du « jeu de test » : c'est ce qui manque à un outil construit avec l'IA, qui produit "
    "des formules plausibles. Les FEC fictifs sont dans fec-fictif/ (corrigé dans corrige-anomalies.md, à "
    "NE PAS montrer avant l'exercice). Société fictive : Ateliers Lumen, menuiserie, SIREN 999000111.")

notes(pipeline("Comment votre outil fabrique l'Excel", "Votre fichier HTML est un programme", [
    "1. Vous déposez\nFEC et liasses", "2. Le programme\nlit et contrôle",
    "3. Il écrit l'Excel\net ses formules", "4. Vous ouvrez\nle classeur",
], "Une formule fausse vient du programme : c'est lui qu'on corrige."),
    "Son fichier Vestis_Analyse_FEC.html contient environ 300 Ko de code JavaScript écrit pour lui : un "
    "lecteur de FEC et de liasses, des contrôles, et un générateur de classeurs .xlsx qui écrit chaque "
    "formule (environ 11 000 sur le dossier test). Corriger une formule dans le classeur produit ne sert "
    "qu'une fois : la prochaine analyse régénère la même erreur. À lui demander en ouverture : comment "
    "il a construit l'outil (avec Claude ?) et s'il sait le faire modifier. Je le suppose, rien ne le "
    "confirme. S'il ne sait pas, la correction passera par Claude avec le prompt de la fiche.")

notes(pipeline("La boucle de fiabilisation", "À refaire après chaque modification de l'outil", [
    "1. Dossier test\naux réponses connues", "2. Lancer\nvotre outil",
    "3. Comparer\nau corrigé", "4. Corriger\nl'outil",
    "5. Relancer\nle même test",
], "On corrige l'outil qui fabrique l'Excel, jamais le classeur produit."),
    "Étape 4 : corriger dans l'Excel produit, c'est refaire la correction à chaque nouveau dossier. "
    "Étape 5 : on relance le MÊME dossier test pour vérifier que la correction n'a rien cassé ailleurs "
    "(non-régression). À terme, plusieurs dossiers tests : régime simplifié, exercice décalé, affacturage.")

notes(tableau("Cinq sources d'erreur d'un Excel généré", ["Type d'erreur", "Exemple", "Où corriger"],
    [3.3, 5.6, 3.0], [
    ["Calcul faux", "Mauvaise plage ou critère dans SOMME.SI.ENS", "L'outil"],
    ["Fonction absente", "MIN.SI.ENS avant Excel 2019 : #NOM?", "L'outil, ou Excel"],
    ["Format régional", "TEXTE(date;\"yyyy\") dans un Excel en français", "L'outil"],
    ["Donnée mal lue", "Séparateur, décimale, sens débit/crédit", "Le lecteur de FEC"],
    ["Hypothèse de calcul", "Ancienneté des créances par FIFO", "Votre choix métier"],
], "Les deux dernières lignes ne sont pas des bugs Excel : ce sont des choix à documenter."),
    "Pistes repérées en lisant son code (non vérifiées dans Excel, je n'en ai pas ici) : 48 formules "
    "MINIFS dans le classeur Trésorerie (fonction apparue avec Excel 2019 / 365 ; #NOM? sur une version "
    "antérieure) ; TEXT(...,\"yyyy-mm\") dans le classeur Relevés (en Excel français, l'année s'écrit "
    "« aaaa » dans un format : risque de texte faux). Contrôle statique fait sur les classeurs produits "
    "avec les FEC fictifs : 21 + 9 onglets, environ 11 000 formules, aucune référence vers un onglet "
    "inexistant. Lui demander sa version d'Excel et la langue de son Excel.")

notes(content("Claude pour Excel, votre auditeur", "Il modifie le classeur ouvert : faites une copie", [
    "**Sélectionnez la cellule en erreur, puis demandez :",
    "` Trouve pourquoi F12 renvoie #NOM? et explique la formule pas à pas.",
    "",
    "**Il remonte jusqu'à la cause, en citant les cellules : un clic, vous y êtes.",
    "**Il corrige en gardant les liens entre formules, et prévient avant d'écraser.",
    "",
    "**Sa correction vaut pour ce seul fichier ; reportez-la dans l'outil.",
]), "Doc Claude (claude.com/docs/office-agents/excel, lue le 19/10/2026) : disponible en Pro, Max, Team, "
    "Enterprise ; « Identify and resolve errors and their root causes » (ex. « Trace why cell H15 is "
    "returning #DIV/0 ») ; citations cliquables ; modifications qui gardent les relations entre formules ; "
    "« Overwrite protection ». Ne gère pas les macros/VBA ni les tables de données. Versions : Excel web, "
    "Windows Microsoft 365, Mac 16.46+ ; PAS Excel 2016/2019 en licence perpétuelle : lui demander sa "
    "version. Données : entrées et sorties supprimées côté Anthropic sous 30 jours, historique stocké dans "
    "le navigateur. Anthropic déconseille les calculs critiques d'audit sans vérification humaine : c'est "
    "exactement notre sujet. Installation : AppSource, « Claude for Microsoft 365 », Get it now.")

notes(enonce("Pratique 2 · Tester votre outil", [
    ("OBJECTIF", "Mesurer la fiabilité de votre outil sur un dossier au corrigé connu."),
    ("LIVRABLE", "Votre grille d'écarts : ce qui manque, ce qui est faux, où corriger."),
    ("DURÉE", "30 minutes"),
], [
    "Déposer les 2 FEC fictifs reçus dans le chat : 2024 en N-1, 2025 en N.",
    "Analyser, puis noter chaque « À voir » et ce qu'il dit du dossier.",
    "Ouvrir l'Excel d'analyse : relever les cellules en erreur (#NOM?…).",
    "Sur deux erreurs : faire expliquer la formule par Claude pour Excel.",
    "Remplir la grille : type d'erreur, onglet, correction dans l'outil.",
]), "Fichiers à lui envoyer dans le chat de la visio : fec-fictif/999000111FEC20241231.txt et "
    "999000111FEC20251231.txt. Il lit le dossier comme un vrai : lui demander son diagnostic en 2 minutes "
    "(il est l'expert). Si son Excel n'affiche aucune erreur sur ce dossier : tant mieux, on passe sur "
    "un de ses vrais classeurs (anonymisé) pour l'étape 4.")

notes(tableau("Pratique 2 · Votre grille d'écarts", ["Écart constaté", "Type", "Onglet", "Correction"],
    [3.9, 2.4, 2.3, 3.3], [
    ["Ex. : #NOM? en col. F", "Fonction absente", "Tresorerie", "Remplacer MINIFS"],
    ["…", "…", "…", "…"],
    ["…", "…", "…", "…"],
    ["…", "…", "…", "…"],
], "Une ligne par écart. Cette grille devient votre liste de corrections."),
    "La première ligne est un exemple (hypothétique tant qu'on n'a pas ouvert son Excel). Remplir en "
    "direct dans un tableur partagé ou dans le classeur lui-même (nouvel onglet).")

tia.slide_section(prs, "3 bis", "Le corrigé", "Les cinq anomalies glissées dans le FEC 2025")

notes(tableau("Le corrigé : cinq anomalies", ["Anomalie glissée", "Votre outil", "Signal"],
    [5.6, 2.6, 3.7], [
    ["Écriture déséquilibrée de 150 €", "Détectée", "Débit ≠ crédit"],
    ["Facture de 48 000 € jamais réglée", "En partie", "Voir slide suivante"],
    ["3 mois d'URSSAF impayés", "Détectée", "4 mois de retard"],
    ["Facture de 96 000 € le 30/12", "Détectée", "Coupure : 5,3×"],
    ["Facture fournisseur saisie 2 fois", "Détectée", "Doublon : 12 000 €"],
], "Et le signal d'ensemble : capitaux propres sous la moitié du capital."),
    "Résultats constatés le 19/10 en lançant son application sur les deux FEC fictifs. Le dossier "
    "raconte une PME en difficulté : CA -23 % (1 983 k€ → 1 520 k€), achats 42 % → 47 % du CA, résultat "
    "+51 k€ → -218 k€, banque +111 k€ → -153 k€ malgré un apport de 80 k€ en compte courant, capitaux "
    "propres 11 k€ pour un capital de 100 k€. Détail : fec-fictif/corrige-anomalies.md.")

notes(deux_colonnes("La facture bloquée", "Quand l'hypothèse de calcul cache le problème",
    ("Ce que dit votre outil", [
        "48 000 € échus depuis plus de 90 jours",
        "25 113 € depuis plus de 180 jours",
        "Méthode FIFO : solde imputé",
        "sur les factures les plus récentes",
    ]),
    ("Ce que dit le dossier", [
        "Une facture du 14/02/2025 : 48 000 €",
        "Jamais réglée, jamais lettrée",
        "320 jours au 31 décembre",
        "Le client paie ses factures récentes",
    ]),
    "Question : croiser la FIFO avec le lettrage quand il est fiable ?"),
    "La Clinique du Parc (fictive) continue à payer ses factures récentes : l'imputation FIFO répartit les "
    "48 000 € sur des factures plus jeunes. Le lettrage du FEC (72 % du facturé lettré en 2025) montre "
    "pourtant la facture exacte. Ce n'est pas un bug : c'est une hypothèse, que son outil documente "
    "(« indépendant du lettrage »). C'est à lui de trancher : il connaît la pratique des IBR.")

notes(content("Corriger l'outil avec Claude", "Le prompt, avec le fichier HTML de l'outil joint", [
    "` Voici mon outil d'analyse FEC (fichier joint) et un écart constaté.",
    "` Dossier test : [fichier]. Attendu : [valeur]. Obtenu : [valeur].",
    "` Trouve la cause, propose le correctif minimal, sans rien réécrire",
    "` d'autre, et un contrôle qui aurait détecté cet écart.",
    "",
    "**Puis : relancer le même dossier test. Rien d'autre n'a bougé ?",
]), "Texte complet dans s1-a-coller.md. « Correctif minimal » : un outil de 300 Ko de code ne se fait pas "
    "réécrire en entier à chaque bug, sinon on perd ce qui marchait. Le « contrôle qui aurait détecté » "
    "enrichit l'onglet Controles de son outil au fil des corrections.")

tia.slide_recap(prs, "Fiabiliser votre outil", [
    "1.  Un dossier test aux réponses connues : sans lui, une erreur ne se voit pas.",
    "2.  On corrige l'outil qui fabrique l'Excel, jamais le classeur produit.",
    "3.  Claude pour Excel explique une formule ; le correctif va dans l'outil.",
    "4.  Une hypothèse de calcul est un choix métier : on l'écrit noir sur blanc.",
    "5.  Après chaque correction, on relance le même test.",
])

# ── 4. Rapport ───────────────────────────────────────────────────────────────
tia.slide_section(prs, "4", "Votre rapport : ce qui s'automatise", "Section par section, avant de construire")

notes(niveaux("Trois niveaux d'automatisation", "Pour chaque section de votre rapport", [
    ("Automatique", "La machine calcule et met en forme, sans vous.",
     "Ex. : P&L, BFR, trésorerie", "Source : FEC, relevés"),
    ("Préparé par Claude", "Claude rédige un premier jet, vous corrigez.",
     "Ex. : commentaire du CA", "Source : vos chiffres"),
    ("Humain", "Ce que vous seul pouvez écrire, et qui fait la valeur.",
     "Ex. : diagnostic, plan", "Source : vos entretiens"),
], "Objectif : le junior ne recopie plus de chiffres ; vous relisez et vous concluez."),
    "Rappel RDV d'intro : un IBR prend 30 à 45 jours, rapport de 30 à 40 pages ; le gain visé est le "
    "travail junior répétitif, la pré-rédaction. Claude rédige À PARTIR des chiffres calculés par l'outil, "
    "jamais en recalculant lui-même : c'est la condition de fiabilité.")

notes(enonce("Pratique 3 · Cartographier votre rapport", [
    ("OBJECTIF", "Savoir ce qui s'automatise dans votre rapport, section par section."),
    ("LIVRABLE", "La grille de votre rapport : le cahier des charges de la séance 2."),
    ("DURÉE", "25 minutes"),
], [
    "Lister les sections de votre rapport type, dans l'ordre.",
    "Pour chacune : d'où viennent les données (FEC, liasse, entretien…) ?",
    "La classer : automatique, préparée par Claude, ou humaine.",
    "Estimer le temps qu'elle prend aujourd'hui, en heures.",
    "Choisir les deux sections à automatiser en séance 2.",
]), "Il est l'expert du rapport : c'est lui qui liste, je pose les questions. Critère pour les deux "
    "sections de la S2 : beaucoup de temps aujourd'hui ET données déjà produites par son outil.")

notes(tableau("Pratique 3 · Un point de départ", ["Section du rapport", "Données", "Niveau"],
    [5.0, 3.6, 3.3], [
    ["Présentation de la société", "Kbis, entretiens", "Préparé par Claude"],
    ["Évolution du CA et des marges", "FEC, liasses", "Auto + commentaire"],
    ["BFR et trésorerie", "FEC, relevés", "Automatique"],
    ["Dettes sociales et fiscales", "FEC, URSSAF, impôts", "Automatique"],
    ["Causes des difficultés", "Entretiens, analyse", "Humain"],
    ["Plan de retournement", "Votre expertise", "Humain"],
], "À corriger avec vous : c'est votre rapport, pas le mien."),
    "Proposition générique d'un IBR, construite par moi : à faire corriger par Xavier, qui en a rédigé. "
    "Les quatre premières lignes s'appuient sur ce que son outil calcule déjà (onglets PnL, Bilan_synth, "
    "Tresorerie, Social_fiscal, Pieces_a_demander).")

notes(pipeline("Ce qu'on construira en séance 2", "Vos deux sections, de l'analyse au premier jet", [
    "1. Votre outil\nproduit l'Excel", "2. n8n reçoit\nles chiffres",
    "3. Claude rédige\nle premier jet", "4. Vous relisez\net concluez",
], "Les chiffres viennent de votre outil ; Claude ne fait que rédiger."),
    "Architecture à confirmer en S2 selon ses deux sections. Point technique à trancher : son outil "
    "tourne dans le navigateur (100 % local, aucune connexion réseau par conception) ; le passage vers "
    "n8n se fera par le fichier Excel produit (dépôt dans un dossier ou formulaire), pas par l'outil "
    "lui-même. Confidentialité : données clients vers Claude via n8n = API, à poser avec lui.")

# ── 5. Devoirs ───────────────────────────────────────────────────────────────
tia.slide_section(prs, "5", "Les devoirs", "Pour la séance 2, mercredi 28 octobre")

notes(content("Devoirs · avant le 28 octobre", None, [
    "**1.  n8n : l'exercice « notification email » du module",
    "**2.  n8n : interroger l'API du BODACC (consigne dans la fiche)",
    "**3.  Votre outil : finir la grille d'écarts, corriger les 2 plus graves",
    "",
    "**4.  Votre rapport : finir la grille, choisir les 2 sections",
    "**5.  M'envoyer avant le 26/10 : grille et rapport type anonymisé",
]), "Devoir 2 : HTTP Request en GET sur l'API publique du BODACC (opendatasoft, sans clé, testée le 19/10), "
    "filtrée sur les procédures collectives d'un département, puis Edit Fields (nom, ville, date, "
    "jugement). URL complète dans s1-a-coller.md. Il pratique le HTTP Request ET prépare la S3. "
    "L'exercice 2 du module (scoring de leads via Hunter.io) n'est plus dans son cas d'usage : pas exigé. "
    "Rappel : l'essai n8n Cloud dure 14 jours ; s'il veut garder ses workflows, export JSON avant la fin "
    "ou passage sur Hostinger.")

tia.slide_recap(prs, "Ce que vous avez fait aujourd'hui", [
    "1.  Votre n8n tourne, et vos workflows suivront sur votre serveur.",
    "2.  Votre outil est testé sur un dossier aux réponses connues.",
    "3.  Vous savez d'où viennent ses erreurs, et où les corriger.",
    "4.  Votre rapport est cartographié : la séance 2 a son cahier des charges.",
])

tia.slide_questions(prs)
tia.save(prs, OUTPUT_PATH)
