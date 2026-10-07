#!/usr/bin/env python3
"""Céline LAFITTE, séance 1 (jeu. 8 oct. 2026, 9h-11h) : comprendre l'IA et prendre en main ChatGPT. Charte TIA."""
import importlib.util
import os

HERE = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.join(HERE, "..", "..", "kit")
_spec = importlib.util.spec_from_file_location("tia", os.path.join(KIT, "lib-slides-python.py"))
tia = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(tia)

OUTPUT_PATH = os.path.join(HERE, "celine-lafitte-s1-ia-chatgpt.pptx")
KICKER = "SÉANCE 1 / 4 · CÉLINE LAFITTE"

# _draw_blocks_on_slide pose chaque ligne dans une boîte de 0.45" : une ligne qui passe à la ligne
# chevauche la suivante sans que verif-slides le voie. On borne la longueur et la hauteur ici.
MAX_CHARS = 78


def check_titles(header, subtitle):
    # Titre 34pt et sous-titre 26pt sur 11.5" : au-delà, ils passent sur deux lignes et chevauchent.
    assert len(header) <= 42, f"Titre trop long ({len(header)}) : {header}"
    assert subtitle is None or len(subtitle) <= 50, f"Sous-titre trop long ({len(subtitle)}) : {subtitle}"


def pipeline(header, subtitle, steps, note):
    check_titles(header, subtitle)
    for s in steps:
        for part in s.split("\n"):
            assert len(part) <= 22, f"Boîte de schéma trop longue ({len(part)}) : {part}"
    # La note native de slide_pipeline tombe à 6.4" : verif-slides la signale. On la pose sous les
    # boîtes, plus bas quand le diagramme passe sur deux lignes.
    slide = tia.slide_pipeline(prs, header, subtitle, steps)
    y = 4.5 if len(steps) <= 4 else 6.05
    tia.add_textbox(slide, tia.Inches(0.7), tia.Inches(y), tia.Inches(12.0), tia.Inches(0.7),
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


def enonce(header, cadre, steps):
    """Slide d'exercice (type 10 de la charte) : un bandeau gris Objectif / Livrable / Durée,
    puis les étapes numérotées (numéro teal en gras, texte foncé)."""
    check_titles(header, None)
    assert len(cadre) == 3 and len(steps) <= 5
    slide = tia.blank_slide(prs)
    tia.add_header(slide, header)
    tia.add_rounded_rect(slide, tia.Inches(0.7), tia.Inches(1.55), tia.Inches(11.9), tia.Inches(1.25),
                         fill_color=tia.C_GRAY_BG)
    col_w = [4.3, 5.2, 2.0]
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


def scpic_lettres(header, subtitle, rows):
    """Une ligne par lettre : la lettre en pastille teal, son nom et sa question, puis l'exemple."""
    check_titles(header, subtitle)
    assert len(rows) == 5
    slide = tia.blank_slide(prs)
    tia.add_header(slide, header)
    tia.add_subtitle(slide, subtitle)
    y = 2.45
    for lettre, nom, question, exemple in rows:
        assert len(exemple) <= 80, f"Exemple trop long ({len(exemple)}) : {exemple}"  # 2 lignes à 17pt
        tia.add_rounded_rect(slide, tia.Inches(0.7), tia.Inches(y), tia.Inches(0.62), tia.Inches(0.62),
                             fill_color=tia.C_TEAL)
        tia.add_textbox(slide, tia.Inches(0.7), tia.Inches(y + 0.06), tia.Inches(0.62), tia.Inches(0.5),
                        lettre, font_size=24, bold=True, color=tia.C_WHITE, align=tia.PP_ALIGN.CENTER)
        tia.add_textbox(slide, tia.Inches(1.5), tia.Inches(y - 0.04), tia.Inches(3.0), tia.Inches(0.35),
                        nom, font_size=18, bold=True, color=tia.C_TITLE)
        tia.add_textbox(slide, tia.Inches(1.5), tia.Inches(y + 0.3), tia.Inches(3.0), tia.Inches(0.35),
                        question, font_size=15, color=tia.C_TEAL_LIGHT)
        tia.add_textbox(slide, tia.Inches(4.6), tia.Inches(y + 0.02), tia.Inches(8.0), tia.Inches(0.65),
                        exemple, font_size=17, color=tia.C_BODY)
        y += 0.72
    return slide


def comparatif(header, colonnes, rows):
    """Tableau à trois colonnes (critère, offre A, offre B), lignes grises une sur deux."""
    check_titles(header, None)
    assert len(rows) <= 8
    slide = tia.blank_slide(prs)
    tia.add_header(slide, header)
    xs, ws = [0.7, 4.3, 7.9], [3.6, 3.6, 4.7]
    y = 1.55
    for x, w, titre in zip(xs, ws, colonnes):
        tia.add_textbox(slide, tia.Inches(x + 0.15), tia.Inches(y), tia.Inches(w - 0.2), tia.Inches(0.4),
                        titre, font_size=18, bold=True, color=tia.C_TEAL)
    tia.add_rect(slide, tia.Inches(0.7), tia.Inches(y + 0.45), tia.Inches(11.9), tia.Inches(0.03), tia.C_GOLD)
    y += 0.52
    for n, row in enumerate(rows):
        if n % 2 == 0:
            tia.add_rect(slide, tia.Inches(0.7), tia.Inches(y), tia.Inches(11.9), tia.Inches(0.46), tia.C_GRAY_BG)
        for i, (x, w, texte) in enumerate(zip(xs, ws, row)):
            assert len(texte) <= int((w - 0.3) * 8.5), f"Cellule trop longue ({len(texte)}) : {texte}"
            tia.add_textbox(slide, tia.Inches(x + 0.15), tia.Inches(y + 0.04), tia.Inches(w - 0.2), tia.Inches(0.36),
                            texte, font_size=16, bold=(i == 0), color=tia.C_TITLE if i == 0 else tia.C_BODY)
        y += 0.46
    return slide


prs = tia.new_prs()

# ── Ouverture ────────────────────────────────────────────────────────────────
tia.slide_cover(prs, KICKER, "L'IA comprise, ChatGPT en main",
                "Ta méthode de prompt et ta base de contexte de coach",
                "Jeudi 8 octobre 2026 · 9h-11h · Idris Salvi")

content("Ce que tu veux en sortir", "Tes mots, lors de notre RDV d'intro", [
    "**1.  Comprendre vraiment comment ça fonctionne,",
    "**     pour encadrer les personnes que tu accompagnes sur l'IA.",
    "",
    "**2.  Arrêter de t'éparpiller : peu d'outils, bien maîtrisés.",
    "",
    "**3.  Des outils réutilisables, au rendu professionnel.",
])

pipeline("Ton parcours", "4 séances, un fil rouge : ton bilan de compétences", [
    "S1 · 8 oct.\nComprendre + méthode", "S2 · 19 oct.\nTes écrits de coach",
    "S3 · 22 oct.\nLire une séance", "S4 · 28 oct.\nCartographie",
], "Aujourd'hui : les bases solides, sur lesquelles tout le reste s'appuie.")

content("Le déroulé de ce matin", None, [
    "**1.  Quiz sur le e-learning (10 min)",
    "**2.  Comment ça marche, ChatGPT Free ou Plus en octobre 2026 (35 min)",
    "",
    "**3.  Exercice 1 : la méthode SCPIC sur un bilan fictif (30 min)",
    "**4.  Exercice 2 : ta base de contexte de coach (30 min)",
    "",
    "**5.  Démo : Granola branché à ChatGPT (5 min)",
    "**6.  Les devoirs (10 min)",
])

# ── 1. Quiz ──────────────────────────────────────────────────────────────────
tia.slide_section(prs, "1", "Quiz d'ouverture", "Cinq questions sur « Comprendre l'IA sans jargon »")

content("Quiz · Question 1", "Un LLM comme ChatGPT, au fond, ça fait quoi ?", [
    "A.  Il cherche la bonne réponse dans une base de données",
    "B.  Il prédit la suite de texte la plus probable, mot après mot",
    "C.  Il comprend le sens comme un humain",
    "",
    "**Réponse B. Il ne « sait » rien : il produit ce qui est plausible.",
])

content("Quiz · Question 2", "Comment ChatGPT a-t-il appris ?", [
    "Remets dans l'ordre :",
    "A.  Des humains notent ses réponses     B.  Il lit des milliards de textes",
    "",
    "**B puis A. Le pré-entraînement lui apprend la langue,",
    "**le retour humain (RLHF) lui apprend à être utile et poli.",
])

content("Quiz · Question 3", "Le system prompt", [
    "Quand tu écris à ChatGPT, qu'est-ce que le modèle lit en premier ?",
    "",
    "**Des consignes invisibles d'OpenAI, puis les tiennes, puis ta demande.",
    "**C'est exactement là qu'on va glisser ta base de contexte.",
])

content("Quiz · Question 4", "Les hallucinations", [
    "Vrai ou faux : si ChatGPT répond avec assurance, c'est que c'est juste.",
    "",
    "**Faux. Il produit toujours une suite, vraie ou non, avec le même aplomb.",
    "**Dans un bilan : une compétence que la personne n'a jamais citée.",
])

content("Quiz · Question 5", "La fenêtre de contexte", [
    "Ta conversation dure depuis 2 heures. Que risque-t-il de se passer ?",
    "A.  Rien      B.  Il oublie le début      C.  Il devient plus précis",
    "",
    "**Réponse B. Sa mémoire de travail est limitée : au-delà, le début glisse.",
    "**Le réflexe : un nouveau chat par tâche, et le contexte dans un projet.",
])

# ── 2. Comment ça marche ─────────────────────────────────────────────────────
tia.slide_section(prs, "2", "Comment ça marche", "Ce que tu pourras expliquer à tes apprenants")

pipeline("Ce que ChatGPT lit vraiment", "À chaque message, il relit tout ceci", [
    "1. Consignes\nd'OpenAI (invisibles)", "2. Tes instructions\n(compte ou projet)",
    "3. Fichiers\net historique du chat", "4. Ta demande\ndu jour",
], "Tout tient dans la fenêtre de contexte : c'est TOUT ce qu'il sait de toi.")

content("Ce que ChatGPT lit vraiment", "La conséquence pour ton travail", [
    "**Il ne te connaît pas. Il ne connaît pas tes organismes, ni ton métier.",
    "Sans contexte, il comble les vides avec du générique.",
    "",
    "**La qualité de la réponse dépend de ce que tu lui donnes à lire.",
    "D'où deux outils : une méthode pour la demande (SCPIC),",
    "et une base de contexte écrite une fois, relue à chaque échange.",
])

content("La fenêtre de contexte, en chiffres", "ChatGPT Free, en mode rapide", [
    "**27 000 jetons au total. Un jeton, c'est un morceau de mot.",
    "**Dont environ 12 pages pour ton texte à toi.",
    "",
    "Le reste est déjà pris : consignes d'OpenAI, tes instructions,",
    "la mémoire, le raisonnement et la réponse elle-même.",
    "",
    "**Pour un bilan de 15 séances : une synthèse par séance, pas tout d'un coup.",
])

content("Le modèle ou ton forfait ?", "Deux chiffres à ne pas confondre", [
    "**GPT-5.6 Sol peut lire 1 050 000 jetons : c'est sa capacité,",
    "**accessible aux développeurs, par l'API.",
    "",
    "**Dans ChatGPT, c'est ton forfait qui fixe la limite :",
    "Free 27K en mode rapide · Plus 54K, et 256K en raisonnement.",
    "",
    "**Tu lis « 1 million de jetons » ? Demande : dans quel outil, quel forfait ?",
])

content("Le mode Think", "Quand le faire réfléchir avant de répondre", [
    "**Think : le modèle raisonne par étapes avant de répondre.",
    "Plus lent, plus fiable sur ce qui demande d'analyser ou de croiser.",
    "",
    "**Oui : analyser des notes de bilan, comparer des pistes d'évolution.",
    "**Inutile : reformuler un mail, corriger l'orthographe.",
])

content("Les hallucinations", "Les parades, à appliquer et à transmettre", [
    "**Dans la demande : « N'ajoute rien qui ne soit pas dans mes notes. »",
    "**Marquer les déductions : « Signale par [À vérifier] ce que tu déduis. »",
    "",
    "**Faire relire : « Qu'est-ce qui, dans ta réponse, pourrait être faux ? »",
    "**Toujours : c'est toi qui valides avant que ça parte au bénéficiaire.",
])

content("ChatGPT Free en octobre 2026", "Ce que tu as, sans payer", [
    "**Modèle GPT-5.6 Luna, avec le mode Think.",
    "**Recherche web, dépôt de fichiers et d'images, création d'images.",
    "",
    "**Projets : des instructions + 5 fichiers, partageables à 5 personnes.",
    "**Instructions personnalisées : 1 500 caractères maximum.",
    "",
    "**Il lit environ 12 pages d'un coup. Limites sur fichiers et images.",
])

content("Web ou application ordinateur ?", "Les deux sont gratuites, elles ne font pas pareil", [
    "**Web et mobile : Chat, avec tes projets et tes instructions.",
    "**ChatGPT Work n'y est ouvert qu'aux forfaits payants.",
    "",
    "**Application ordinateur (Mac, Windows) : Chat, Work, Codex et Skills.",
    "**En Free, Work et Codex y sont limités en usage.",
    "",
    "**Mon conseil : installe l'application. Tes projets s'y retrouvent.",
])

content("À quoi sert ChatGPT Work ?", "Chat répond, Work exécute", [
    "**Chat : répondre, reformuler, réfléchir avec toi. Rapide.",
    "**Work : un agent. Tu donnes un objectif, il découpe et exécute.",
    "",
    "**Il livre un document, un tableur, des diapositives, un rapport.",
    "**Tu suis l'avancement, tu réponds à ses questions, tu valides.",
    "",
    "**Pour toi, plus tard : tes notes, mises au format Word d'un organisme.",
])

content("Les Skills, comme dans Claude", "Dans l'application ordinateur, en bêta", [
    "**Une procédure réutilisable : instructions, exemples, parfois du code.",
    "**ChatGPT l'utilise tout seul quand la tâche s'y prête.",
    "",
    "**Où : Plugins, dans la barre latérale, puis l'onglet Skills.",
    "**Pour en créer une : demande-le en conversation, il t'accompagne.",
    "",
    "**Le projet donne le contexte. La skill donne la façon de faire.",
])

comparatif("Free ou Plus ?", ["", "Free · 0 €", "Plus · 23 € par mois"], [
    ["Modèles", "GPT-5.6 Luna", "+ GPT-6 et GPT-5.6 Sol (limités)"],
    ["Fenêtre de contexte", "27K, dont ~12 pages à toi", "54K, dont ~40 pages à toi"],
    ["Fichiers par projet", "5", "25"],
    ["Instructions perso", "1 500 caractères", "5 000 caractères"],
    ["Recherche approfondie", "limitée", "oui"],
    ["ChatGPT Work (agent)", "limité, appli ordinateur", "ordinateur, web et mobile"],
    ["Tâches planifiées", "non", "oui"],
    ["Extensions Word, Excel", "limitées", "oui"],
])

content("Plus vaut le coup si…", None, [
    "**Tes notes de bilan dépassent 12 pages à faire lire d'un coup.",
    "**Tu veux plus de 5 documents de référence par projet.",
    "",
    "**Tu veux confier des tâches longues à ChatGPT Work, sur le web.",
    "**Tu prépares des formations avec la recherche approfondie.",
    "",
    "**Free ou Plus : entraînement sur tes données par défaut, refus possible.",
    "Il existe aussi Go (8 €) et Pro (dès 103 €). Prix France, octobre 2026.",
])

content("Ce qui a changé depuis la vidéo", "Les GPT personnalisés", [
    "Le e-learning montre comment créer ton propre GPT.",
    "",
    "**En Free, la création de GPT n'est pas disponible.",
    "**Tu peux utiliser les GPT existants, pas en créer.",
    "",
    "**L'équivalent en Free : le projet (instructions + fichiers).",
])

content("Où ranger ton contexte", "Trois niveaux, du plus large au plus précis", [
    "**Instructions personnalisées : qui tu es, ton style.",
    "Valent pour toutes les conversations. 1 500 caractères en Free.",
    "",
    "**Projet : un usage précis (ex. « Bilans de compétences »).",
    "Instructions + fichiers. Prioritaires sur les instructions générales.",
    "",
    "**Le prompt : la tâche du jour, structurée avec SCPIC.",
])

pipeline("La méthode SCPIC", "Cinq briques, vues dans le e-learning", [
    "S · Système\nqui doit être l'IA ?", "C · Contexte\nquelles infos donner ?",
    "P · Public\nà qui c'est destiné ?", "I · Instruction\nque doit-elle faire ?",
    "C · Contraintes\nformat et limites",
], "La méthode que tu transmettras ensuite à tes coachés.")

scpic_lettres("SCPIC, lettre par lettre", "Exemple inventé : préparer une séance de coaching", [
    ("S", "Système", "le rôle de l'IA",
     "« Tu es une coach professionnelle certifiée, spécialiste du management. »"),
    ("C", "Contexte", "ce qu'elle doit savoir",
     "« Mon coaché, manager depuis 6 mois, a du mal à déléguer. Séance 4 sur 8. »"),
    ("P", "Public", "pour qui est le résultat",
     "« Le plan est pour moi : je m'en sers pendant la séance. »"),
    ("I", "Instruction", "la tâche, avec un verbe",
     "« Propose un déroulé en 3 temps, avec 2 questions ouvertes par temps. »"),
    ("C", "Contraintes", "format, longueur, limites",
     "« Une demi-page, en puces, sans jargon RH. »"),
])

content("SCPIC : la synthèse d'une séance", None, [
    "**S :  Tu es une consultante en bilan de compétences expérimentée.",
    "**C :  Voici mes notes brutes de la séance 3 sur 15.",
    "**P :  La synthèse est pour la bénéficiaire ; je la relis avant envoi.",
    "",
    "**I :  Rédige une synthèse en 4 parties : travaillé, valeurs,",
    "**      compétences transférables, travail pour la prochaine séance.",
    "**C :  Une page, vouvoiement, rien d'inventé, [À vérifier] si tu déduis.",
])

content("Tes données", "Ce que tu confies à ChatGPT Free", [
    "**Paramètres › Contrôles des données › « Améliorer le modèle pour tous ».",
    "Activé : tes nouvelles conversations peuvent servir à entraîner les modèles.",
    "",
    "**Chat éphémère : ni historique, ni mémoire, ni entraînement.",
    "**Piège : un pouce levé ou baissé peut verser la conversation à l'entraînement.",
])

content("Tes données", "Dans un bilan de compétences", [
    "**Le bilan est confidentiel : ce qui entre dans l'outil doit l'être aussi.",
    "",
    "**Jamais : nom, employeur nommé, ville, détail qui permette de reconnaître.",
    "**Toujours : prénom fictif ou initiale, entreprise décrite (« PME, 80 pers. »).",
    "",
    "**La règle, que tu transmettras : anonymiser AVANT de coller.",
])

tia.slide_recap(prs, "Trois phrases pour tes apprenants", [
    "1.  Il prédit, il ne sait pas : on vérifie ce qui compte.",
    "2.  Il ne sait de toi que ce que tu lui donnes : on écrit son contexte.",
    "3.  Ce que tu lui donnes peut servir ailleurs : on anonymise avant.",
    "4.  Une demande claire suit SCPIC : système, contexte, public,",
    "     instruction, contraintes.",
])

# ── 3. Exercice 1 ────────────────────────────────────────────────────────────
tia.slide_section(prs, "3", "Exercice 1 : SCPIC sur un bilan", "Partage d'écran : tu fais, je montre")

enonce("Exercice 1 · L'énoncé", [
    ("OBJECTIF", "Voir de tes yeux ce que SCPIC change à une synthèse de bilan."),
    ("LIVRABLE", "Ton projet « Bilans de compétences » et une synthèse de séance que tu signerais."),
    ("DURÉE", "30 minutes"),
], [
    "Régler tes données : Paramètres › Contrôles des données.",
    "Créer le projet « Bilans de compétences » (Nouveau projet, à gauche).",
    "Dans le projet : coller les notes fictives + « Fais une synthèse ».",
    "Nouveau chat dans le projet : mêmes notes, demande écrite en SCPIC.",
    "Comparer les deux réponses avec la grille (slide suivante).",
])

content("Exercice 1 · Les notes fictives à coller", None, [
    "Séance 3/15 · « Mme R. », 44 ans, assistante de direction depuis 12 ans.",
    "PME industrielle (80 pers.). Veut évoluer : office manager ? RH ?",
    "Peur de « repartir de zéro ». Fierté : a piloté le déménagement du siège.",
    "Aime organiser, être le point de contact. Évite les conflits frontaux.",
    "Valeurs citées : fiabilité, reconnaissance, équilibre (2 enfants).",
    "Outils : Excel avancé, Sage. Organise les réunions du CSE.",
    "**Situation inventée : aucune personne réelle. Texte complet dans le chat.",
])

content("Exercice 1 · La grille de comparaison", "Pour chaque réponse, quatre questions", [
    "**1.  Fidélité : a-t-il inventé quelque chose qui n'est pas dans les notes ?",
    "**2.  Structure : retrouves-tu tes 4 parties, dans l'ordre ?",
    "",
    "**3.  Ton : est-ce écrit pour Mme R. ou pour un rapport ?",
    "**4.  Prête à l'emploi : combien de minutes de retouche avant envoi ?",
    "",
    "> Ce qui a changé entre les deux, c'est ce que tu lui as donné à lire",
])

# ── 4. Exercice 2 ────────────────────────────────────────────────────────────
tia.slide_section(prs, "4", "Exercice 2 : ta base de contexte", "Écrite une fois, relue à chaque échange")

content("Ta base de contexte de coach", "Ce qu'elle contient : une page, huit rubriques", [
    "**1.  Qui je suis          2.  Mes publics",
    "**3.  Mes accompagnements (bilan, coaching, formation)",
    "",
    "**4.  Mes méthodes et outils          5.  Mes livrables et leurs formats",
    "**6.  Mon ton          7.  Ce que je ne veux jamais",
    "",
    "**8.  Mes règles de confidentialité",
])

enonce("Exercice 2 · L'énoncé", [
    ("OBJECTIF", "Que ChatGPT connaisse ton métier sans que tu le répètes."),
    ("LIVRABLE", "Ta base de contexte : en résumé dans ton compte, en entier dans ton projet."),
    ("DURÉE", "30 minutes"),
], [
    "Coller le prompt d'interview : ChatGPT te pose 10 questions, une à une.",
    "Il rédige ta base. Tu relis et tu corriges tout ce qui sonne faux.",
    "L'ajouter aux fichiers du projet, puis coller les instructions du projet.",
    "La faire résumer en 1 500 caractères pour tes instructions personnalisées.",
    "Test : nouveau chat, « Synthèse de ces notes » + les notes fictives.",
])

content("Exercice 2 · Les instructions du projet", "Paramètres du projet › Instructions", [
    "` Tu es l'assistant de Céline, coach professionnelle.",
    "` Appuie-toi toujours sur le fichier « Base de contexte de coach ».",
    "",
    "` 1. Données anonymisées seulement : signale tout détail identifiant.",
    "` 2. N'invente rien : marque [À vérifier] ce que tu déduis.",
    "` 3. Termine par les points que je dois relire avant envoi.",
])

content("Exercice 2 · Le résumé pour ton compte", "Paramètres › Personnalisation", [
    "` Résume ma base de contexte en moins de 1 500 caractères :",
    "` qui je suis, mes publics, mon ton, mes règles de confidentialité.",
    "` Garde seulement ce qui vaut pour toutes mes conversations.",
    "",
    "**Le résumé, dans tes instructions personnalisées : lu partout.",
    "**La base complète, dans chaque projet qui en a besoin.",
])

content("Bonus · La même base dans Claude", "Ton contexte n'est pas prisonnier d'un outil", [
    "**Claude › Projets › ton projet de bilan existant.",
    "**Instructions du projet : les mêmes, collées telles quelles.",
    "",
    "**Connaissances du projet : le même document de base de contexte.",
    "Un seul texte, deux outils : c'est ça, arrêter de s'éparpiller.",
])

# ── 5. Démo ──────────────────────────────────────────────────────────────────
tia.slide_section(prs, "5", "Démo : Granola + ChatGPT", "Tes notes de réunion, directement dans la conversation")

pipeline("Granola branché à ChatGPT", "Ce que je te montre", [
    "1. Granola\nprend les notes du RDV", "2. Dans ChatGPT\nchercher Granola",
    "3. On connecte\nGranola", "4. On demande\n« le mail de suivi »",
], "Exemple : notre RDV d'intro, transformé en mail de récap en une demande.")

# ── 6. Les devoirs ───────────────────────────────────────────────────────────
tia.slide_section(prs, "6", "Les devoirs", "Pour la séance 2, lundi 19 octobre")

content("Devoirs · avant le 19 octobre", None, [
    "**1.  Finir « Découvrir et utiliser ChatGPT »",
    "**2.  Suivre « Claude : les fondamentaux »",
    "**3.  Installer ChatGPT pour ordinateur et y retrouver ton projet",
    "**     puis tester ta base de contexte sur 3 vraies tâches anonymisées",
    "",
    "**4.  M'envoyer d'ici le 16 octobre : une note de séance anonymisée",
    "**     et les trames de synthèse de tes deux organismes",
    "**5.  Penser au coaché de la S3 et lui parler de l'enregistrement",
])

tia.slide_questions(prs)
tia.save(prs, OUTPUT_PATH)
