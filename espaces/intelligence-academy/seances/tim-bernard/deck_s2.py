#!/usr/bin/env python3
"""Timothé BERNARD, séance 2 (mer. 21 oct. 2026, 13h30-15h30) : préparer l'appel du prospect plombier,
puis construire la veille concurrentielle de sa fiche de poste, avec n8n et avec Claude. Charte TIA.

Sources : débrief S1 du 9/10 (mail et Granola), mails de Tim du 12/10 (fiche de poste en PDF),
16/10 (choix de la veille) et 18/10 (fiche du prospect plombier), dossier TIA.
Non reçus avant la séance : ses workflows (annoncés le 16/10). Non vérifiés : API d'Interfast,
ligne téléphonique du plombier, clé API Anthropic de Tim.
"""
import importlib.util
import os

HERE = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.join(HERE, "..", "..", "kit")
_spec = importlib.util.spec_from_file_location("tia", os.path.join(KIT, "lib-slides-python.py"))
tia = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(tia)

OUTPUT_PATH = os.path.join(HERE, "tim-bernard-s2-plombier-veille.pptx")
KICKER = "SÉANCE 2 / 4 · TIMOTHÉ BERNARD"
I = tia.Inches

# _draw_blocks_on_slide pose chaque ligne dans une boîte de 0.45" : une ligne qui passe à la ligne
# chevauche la suivante sans que verif-slides le voie. On borne la longueur et la hauteur ici.
MAX_CHARS = 78
N_QUIZ = 4


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
    header = f"Quiz · Question {num} / {N_QUIZ}"
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


prs = tia.new_prs()

# ── Ouverture ────────────────────────────────────────────────────────────────
tia.slide_cover(prs, KICKER, "Un prospect, une veille",
                "Préparer l'appel du plombier, construire ta veille défense",
                "Mercredi 21 octobre 2026 · 13h30-15h30 · Idris Salvi")

content("Depuis le 9 octobre", None, [
    "> j'ai un client potentiel qui veut que je le rappelle !",
    "",
    "**12/10 : tu m'envoies ta fiche de poste dans la défense.",
    "**16/10 : tu choisis la veille concurrentielle comme exercice.",
    "**18/10 : un plombier-chauffagiste attend ton appel.",
    "",
    "Aujourd'hui : ton travail d'abord, puis le plombier, puis ta veille.",
    "La veille, deux fois : avec n8n, puis avec Claude.",
])

tableau("Le déroulé", ["Horaire", "Bloc", "Tu repars avec"], [1.6, 4.3, 6.0], [
    ("13h30", "Quiz", "Les réflexes de la séance 1"),
    ("13h40", "Ce que tu as construit", "Tes workflows revus et améliorés"),
    ("14h20", "Le prospect plombier", "Ta trame d'appel et ton offre"),
    ("14h50", "Veille avec n8n", "Un workflow qui tourne chaque lundi"),
    ("15h10", "Veille avec Claude", "Un skill comparé au workflow"),
    ("15h25", "Devoirs", "Ta semaine, et la date de la séance 3"),
])

# ── 1. Quiz ──────────────────────────────────────────────────────────────────
tia.slide_section(prs, "1", "Quiz d'ouverture", "Quatre questions sur la séance 1")

notes(quiz(1, "Pourquoi Tally écrit-il directement dans Airtable, sans passer par n8n ?", [
    "A.  C'est plus rapide pour le client",
    "B.  Si n8n plante, aucune demande n'est perdue",
    "C.  Tally ne sait pas appeler un webhook",
], [
    "Réponse B : la demande est en sécurité dans Airtable.",
    "n8n travaille ensuite à partir de la base, pas à partir du formulaire.",
]), "Décision de la S1. Si C est choisi : Tally sait appeler un webhook, on l'a vu au quiz de la S1.")

quiz(2, "Aucune règle de ton Switch ne correspond à la demande. Que devient-elle ?", [
    "A.  n8n affiche une erreur",
    "B.  Elle est abandonnée, sans aucun message",
    "C.  Elle part dans la première sortie",
], [
    "Réponse B : d'où le « Fallback Output », une sortie de secours.",
    "Sans lui, tu ne sauras jamais qu'une demande a disparu.",
])

notes(quiz(3, "Ta relance J+3 plante à 9h. Comment es-tu prévenu ?", [
    "A.  n8n t'écrit automatiquement",
    "B.  Par ton workflow « Erreurs », choisi dans les Settings de J+3",
    "C.  Le client te le dit",
], [
    "Réponse B : Error Trigger, puis le message sur ton bot Telegram.",
    "Sans lui, l'échec n'apparaît que dans l'onglet Executions.",
]), "C'est le premier workflow qu'il montrera juste après : on vérifiera sa réponse en direct.")

quiz(4, "Claude doit créer des tables dans ton Airtable. Tu passes par...", [
    "A.  L'extension Chrome de Claude, qui clique pour toi",
    "B.  Le connecteur Airtable de Claude",
], [
    "Réponse B : il appelle l'API directement.",
    "C'est plus rapide, et ça consomme beaucoup moins de tokens.",
])

# ── 2. Ce que tu as construit ────────────────────────────────────────────────
tia.slide_section(prs, "2", "Ce que tu as construit", "Tu montres, on améliore et on continue ensemble")

notes(content("Ce que tu apportes", "Partage d'écran : fais-les tourner", [
    "**1.  Le workflow « Erreurs » et ton bot Telegram.",
    "**2.  Les relances J+3 et J+7, branchées sur « Erreurs ».",
    "**3.  La base que tu prépares pour le plombier.",
    "**4.  Ce que tu as essayé avec Claude Code.",
    "",
    "Pour chaque pièce : tu la lances, on la passe à la grille, on l'améliore.",
]), "Ses workflows ne sont pas arrivés par mail (annoncés le 16/10). Le 18/10, il écrit préparer "
    "« une base » pour le plombier et avancer sur Claude Code : contenu inconnu. Commence par lui "
    "demander ce qu'il veut montrer en premier. À 14h20, on passe au plombier : ce qui n'est pas "
    "fini part dans les devoirs. Si sa base plombier est avancée, elle peut servir de support au bloc suivant.")

tableau("La grille de revue", ["La question", "Ce qu'on vérifie"], [5.0, 6.9], [
    ("Il tourne seul ?", "Activé, en production, pas en mode test"),
    ("Que se passe-t-il si ça casse ?", "« Erreurs » choisi dans les Settings"),
    ("Et si aucune règle ne correspond ?", "Un Fallback Output sur chaque Switch"),
    ("Tu le lis sans l'ouvrir ?", "Nœuds renommés, une note par bloc"),
    ("Testé avec une vraie donnée ?", "Pas seulement des données épinglées"),
    ("Les accès sont propres ?", "Credentials n8n, aucune clé en clair"),
], note="La même grille servira pour chaque workflow que tu livreras à un client.")

# ── 3. Le prospect plombier ──────────────────────────────────────────────────
tia.slide_section(prs, "3", "Le prospect plombier", "Préparer un appel de 10 minutes")

content("Ce qu'il t'a dit", "Plombier-chauffagiste, il travaille seul", [
    "**4 à 7 h d'administratif par semaine, gêne de 8/10 le soir et le week-end.",
    "**Ses clients l'appellent, ou viennent par le bouche-à-oreille.",
    "**Il fait ses devis sur Interfast, en 2 à 3 jours.",
    "",
    "**Il a déjà une secrétaire indépendante.",
    "**Son budget : 100 à 150 € par mois.",
])

notes(tableau("Ses 6 demandes, ce que tu as déjà", ["Sa demande", "Tu as déjà", "Difficulté"],
              [4.6, 4.5, 2.8], [
    ("1. SMS sur appel manqué", "Rien : dépend de sa ligne", "À vérifier"),
    ("2. Un seul tableau", "Tally → Airtable", "Prêt"),
    ("3. Brouillon de devis", "Rien : il devise sur Interfast", "À vérifier"),
    ("4. Relance des devis", "Les relances J+3 et J+7", "Prêt"),
    ("5. Rappel des RDV la veille", "Le modèle des relances", "Moyen"),
    ("6. Demande d'avis Google", "Un mail en fin de chantier", "Facile"),
], note="Ses clients appellent : le SMS doit les renvoyer vers ton formulaire Tally."),
    "Non vérifié : Interfast a-t-il une API ou des exports ? Le SMS sur appel manqué demande une ligne "
    "qui sait déclencher un webhook (téléphonie en ligne type Ringover, Aircall, Twilio). Avec un "
    "simple mobile, c'est plus compliqué. Ce sont les deux premières questions de son appel.")

content("Le calcul qu'il n'a pas fait", "Avec ses propres chiffres", [
    "**2 à 3 clients perdus par mois, selon lui, à 1 000 à 5 000 € le chantier.",
    "**Soit 2 000 à 15 000 € de chiffre d'affaires qui part chaque mois.",
    "",
    "Son budget : 100 à 150 € par mois.",
    "Un seul chantier récupéré par mois paie l'outil plusieurs fois.",
    "",
    "**Fais-le-lui calculer au téléphone. Ne lui récite pas.",
])

pipeline("Le lot 1 à lui proposer", "Ce qui se passe quand il rate un appel", [
    "Appel manqué\nsur sa ligne pro",
    "SMS automatique\nlien vers Tally",
    "Airtable\nle tableau unique",
    "Relance du devis\nJ+3 et J+7",
], "Les boîtes 3 et 4 existent déjà. La 2 dépend de sa ligne : 1re question de l'appel.")

deux_colonnes("La secrétaire : obstacle ou alliée ?", None,
              ("Ce que tu dois savoir", [
                  "Que fait-elle chaque semaine ?",
                  "Combien lui coûte-t-elle ?",
                  "Pourquoi 2 à 3 jours par devis ?",
                  "Qui relance les devis aujourd'hui ?",
              ]),
              ("Ce que tu proposes", [
                  "Elle saisit moins : tout arrive trié",
                  "Les relances partent sans elle",
                  "Elle garde la relation client",
                  "Tu ne remplaces personne",
              ]),
              note="Présente l'outil comme son assistant à elle, pas comme son remplaçant.")

notes(enonce("Exercice · Ton appel de 10 minutes", [
    ("OBJECTIF", "Savoir quoi demander, quoi proposer, à quel prix"),
    ("LIVRABLE", "Une trame : 5 questions, ton lot 1, ton prix, la suite"),
    ("DURÉE", "15 min"),
], [
    "Donne à Claude sa fiche et la liste de ce que tu as déjà construit.",
    "Fais-lui écrire 5 questions : sa ligne, Interfast, sa secrétaire...",
    "Choisis ton lot 1 : deux automatisations livrables en deux semaines.",
    "Fixe ton prix : une mise en place, puis un abonnement dans son budget.",
    "On joue l'appel : je suis le plombier, tu as 10 minutes.",
]), "Le prix avait été reporté de la S1 (il pensait à 250 € une fois plus un abonnement, et sous-évaluer "
    "le récurrent). Son budget annoncé (100 à 150 €/mois) donne le cadre. Jeu de rôle : objection "
    "« j'ai déjà ma secrétaire », puis « je ne sais pas combien de temps ça me ferait gagner ».")

# ── 4. Veille avec n8n ───────────────────────────────────────────────────────
tia.slide_section(prs, "4", "Ta veille concurrentielle", "Version 1 : un workflow n8n")

content("Pourquoi cette veille", "Ta fiche de poste, mission par mission", [
    "> Mise en place de flux de veille sur les autres acteurs du secteur",
    "",
    "**40 % du poste porte sur l'automatisation, dont cette veille.",
    "**5 acteurs cités : Harmattan, Anduril, Helsing, DroneShield, Dedrone.",
    "",
    "Tu arrives en entretien avec l'outil qui tourne, pas avec une intention.",
])

notes(pipeline("Le workflow « Veille »", "Chaque lundi matin, sans toi", [
    "Schedule\nlundi 8h",
    "5 RSS Read\nun par acteur",
    "Merge\nles 5 listes",
    "Filter\n7 derniers jours",
    "Remove Duplicates\npar lien",
    "Aggregate\nun seul paquet",
    "Claude\nla synthèse",
    "Telegram\nton bot",
], "Le bot Telegram de tes devoirs sert deux fois : erreurs et veille."),
    "Aggregate : sans lui, Claude est appelé une fois par article au lieu d'une fois pour la semaine. "
    "Remove Duplicates : l'option qui écarte les items déjà vus aux exécutions précédentes évite de "
    "renvoyer la même news deux lundis de suite.")

notes(content("Théorie · Les sources", "Google News : un flux RSS par acteur", [
    "` news.google.com/rss/search?q=Helsing&hl=en-US&gl=US&ceid=US:en",
    "**Un nœud RSS Read par acteur : seul q= change dans l'URL.",
    "` q=%22Harmattan+AI%22  q=Anduril  q=Helsing  q=DroneShield  q=Dedrone",
    "**%22 = guillemets. Sans eux, « Harmattan » remonte aussi un éditeur.",
    "",
    "**Claude résume des titres, pas les articles : il cite le lien, rien de plus.",
]), "Cinq nœuds côte à côte plutôt qu'une liste d'URL découpée (Edit Fields puis Split Out) : "
    "c'est plus lisible à l'écran et ça suffit pour 5 acteurs. Merge : régler « Number of Inputs » "
    "sur 5, mode Append. Évolution possible en devoir : passer à la liste d'URL quand il ajoutera "
    "des acteurs.")

notes(content("Théorie · Claude dans n8n", "Le prompt de la synthèse", [
    "` Tu es analyste veille pour une startup de la défense.",
    "` Voici les articles de la semaine : titre, source, date, lien.",
    "` Classe-les par concurrent, puis par type : levée, contrat,",
    "` produit, publication. Une phrase par fait, avec son lien.",
    "` Un fait sans lien est supprimé. Termine par 3 signaux à suivre.",
    "**Il faut une clé API Anthropic, payée à l'usage, distincte de ton abonnement.",
]), "Vérifier avant la séance si Tim a une clé API Anthropic. Sinon, prévoir une clé de démo pour la "
    "séance et lui laisser le choix du modèle ensuite.")

enonce("Exercice · Construire la veille n8n", [
    ("OBJECTIF", "Une synthèse de la semaine reçue sur Telegram"),
    ("LIVRABLE", "Le workflow « Veille », testé sur les 5 concurrents"),
    ("DURÉE", "20 min"),
], [
    "5 nœuds RSS Read, un par acteur : seul q= change dans l'URL.",
    "Merge : 5 entrées, mode Append. Puis Filter sur 7 jours (isoDate).",
    "Remove Duplicates par lien, puis Aggregate en un seul paquet.",
    "Basic LLM Chain avec le modèle Claude et le prompt de la synthèse.",
    "Telegram : envoie le résultat à ton bot. Puis le Schedule du lundi.",
])

# ── 5. Veille avec Claude ────────────────────────────────────────────────────
tia.slide_section(prs, "5", "La même veille avec Claude", "Version 2 : un skill qui cherche sur le web")

deux_colonnes("n8n ou Claude ?", "Deux outils de ton parcours, deux logiques",
              ("Le workflow n8n", [
                  "Sources fixes : tes 5 flux RSS",
                  "Tourne seul sur ton serveur",
                  "Même format chaque lundi",
                  "Ne voit que ce que les flux donnent",
              ]),
              ("Le skill Claude", [
                  "Cherche sur tout le web",
                  "Relie les faits entre eux",
                  "Format qui peut varier",
                  "Sources à vérifier une par une",
              ]),
              note="Le meilleur des deux : n8n collecte, Claude synthétise. C'est ton workflow.")

notes(enonce("Exercice · Le skill « veille-concurrents »", [
    ("OBJECTIF", "La même synthèse, produite par Claude seul"),
    ("LIVRABLE", "Un skill dans Claude Code et son premier rapport"),
    ("DURÉE", "15 min"),
], [
    "Dans Claude Code, demande-lui de créer le skill « veille-concurrents ».",
    "Donne les 5 concurrents, les 4 types de faits et le format du rapport.",
    "Exige un lien et une date par fait, sur les 7 derniers jours.",
    "Lance-le et compare avec n8n : ce qu'il trouve en plus, ce qui est faux.",
    "Planifie-le chaque lundi, si ton abonnement Claude le permet.",
]), "Lien avec sa fiche : « Développement d'outils via Claude Code ». Il a commencé le module "
    "Fondamentaux Cursor & Claude Code (2 vidéos sur 6). Pour la planification : tâches planifiées, "
    "à vérifier selon son abonnement.")

tia.slide_recap(prs, "Séance 2 : un prospect, une veille", [
    "1.  Plombier : ses chiffres font le calcul, sa secrétaire reste dans le jeu.",
    "2.  Ses clients appellent : le SMS les renvoie vers ton Tally.",
    "3.  Veille n8n : sources fixes, même format, tourne seul.",
    "4.  Veille Claude : cherche partout, à vérifier lien par lien.",
    "5.  Le meilleur des deux : n8n collecte, Claude synthétise.",
])

# ── 6. Devoirs ───────────────────────────────────────────────────────────────
notes(content("Devoirs · avant la séance 3", None, [
    "**1.  Appeler le plombier avec ta trame, et m'envoyer ses réponses.",
    "**2.  Lundi, comparer la synthèse n8n et le rapport du skill Claude.",
    "**3.  Archiver chaque synthèse dans Airtable : une ligne par semaine.",
    "",
    "**4.  Finir le workflow « Erreurs » s'il n'est pas branché sur J+3 et J+7.",
    "**5.  E-learning : les 3 vidéos n8n, puis les Fondamentaux Claude Code.",
]), "Caler les séances 3 et 4 avant de raccrocher : aucune n'est planifiée et la formation se "
    "termine le 12/11.")

tia.slide_questions(prs)
tia.save(prs, OUTPUT_PATH)
