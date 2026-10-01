#!/usr/bin/env python3
"""Laurence SAULAIS — Séance 1 (ven. 2 oct. 2026, 9h-11h) : Les fondamentaux en profondeur. Charte TIA."""
import importlib.util
import os

HERE = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.join(HERE, "..", "..", "kit")
_spec = importlib.util.spec_from_file_location("tia", os.path.join(KIT, "lib-slides-python.py"))
tia = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(tia)

OUTPUT_PATH = os.path.join(HERE, "laurence-saulais-s1-fondamentaux.pptx")
KICKER = "SÉANCE 1 / 4 · LAURENCE SAULAIS"

# _draw_blocks_on_slide pose chaque ligne dans une boîte de 0.45" : une ligne qui passe à la ligne
# chevauche la suivante sans que verif-slides le voie. On borne la longueur et la hauteur ici.
MAX_CHARS = 78


def pipeline(header, subtitle, steps, note):
    # La note native de slide_pipeline tombe à 6.4" : verif-slides la signale. On la pose plus haut.
    slide = tia.slide_pipeline(prs, header, subtitle, steps)
    tia.add_textbox(slide, tia.Inches(0.7), tia.Inches(4.5), tia.Inches(12.0), tia.Inches(0.7),
                    note, font_size=18, bold=True, color=tia.C_TEAL)
    return slide


def content(header, subtitle, bullets):
    for line in bullets:
        assert len(line.lstrip("*")) <= MAX_CHARS, f"Ligne trop longue ({len(line)}) : {line}"
    blocks = tia._split_into_blocks(bullets)
    n_lines = sum(len(b) for b in blocks)
    top = 2.55 if subtitle else 1.7
    bottom = top + n_lines * 0.57 - 0.12 + (len(blocks) - 1) * 0.26
    assert bottom <= 6.0, f"Slide « {subtitle or header} » trop pleine (bas à {bottom:.2f}\")"
    return tia.slide_content(prs, header, subtitle, bullets)


prs = tia.new_prs()

# ── Ouverture ────────────────────────────────────────────────────────────────
tia.slide_cover(prs, KICKER, "Les fondamentaux, en profondeur",
                "Comprendre, cadrer, garder la main",
                "Vendredi 2 octobre 2026 · 9h-11h · Idris Salvi")

pipeline("Le parcours", "Quatre séances, dans l'ordre de la proposition", [
    "S1 · 2 oct.\nFondamentaux", "S2 · 13 oct.\nVisuels",
    "S3 · 16 oct.\nÉcrits, tableaux, CR", "S4 · 20 oct.\nProjet de bout en bout",
], "Avant chaque séance : le e-learning. Pendant la séance : la pratique sur votre cas.")

content("Le e-learning, remis dans l'ordre", None, [
    "**Avant S1 :  Comprendre l'IA sans jargon",
    "**Avant S2 :  Focus Midjourney & Nano Banana, puis Claude — Les fondamentaux",
    "",
    "**Avant S3 :  Claude pour Excel, puis Claude Cowork",
    "**Avant S4 :  Claude for Chrome",
    "",
    "Chaque module se trouve juste avant la séance qui en parle.",
])

content("Ce qu'on a clarifié par mail", None, [
    "**Les « jours » du programme : un regroupement automatique par heures.",
    "**ChatGPT : gardez votre version, tout modèle récent convient.",
    "",
    "**Claude : on crée et on configure votre compte ensemble, aujourd'hui.",
    "**Les exercices « Spécifiquement pour toi » : repris après le quiz.",
])

content("Le déroulé de ce matin", None, [
    "**1.  Quiz (10 min), puis vos exercices du e-learning (10 min)",
    "**2.  Les fondamentaux (35 min) : mots, outils, méthode, données, limites",
    "",
    "**3.  La pratique (50 min) : votre méthode et votre cadre, sur un support réel",
    "**4.  Les devoirs (10 min)",
])

# ── 1. Quiz ──────────────────────────────────────────────────────────────────
tia.slide_section(prs, "1", "Quiz d'ouverture", "Cinq questions sur le e-learning")

content("Quiz · Question 1", "Un LLM, au fond, ça fait quoi ?", [
    "A.  Il cherche la bonne réponse dans une base de données",
    "B.  Il prédit le mot le plus probable, en tenant compte du contexte",
    "C.  Il comprend le sens comme un humain",
    "",
    "**Réponse B : un « autocomplete très avancé », qui calcule les liens entre mots.",
])

content("Quiz · Question 2", "Le modèle apprend en devinant des mots cachés", [
    "« Le chat boit du ___ » : comment s'appelle cette phase d'entraînement ?",
    "A.  Le pre-training      B.  Le system prompt      C.  La multimodalité",
    "",
    "**Réponse A : le pré-entraînement, sur des milliards d'exemples.",
])

content("Quiz · Question 3", "Le system prompt", [
    "Quand vous écrivez à ChatGPT, qu'est-ce qui arrive au modèle en premier ?",
    "",
    "**Les instructions cachées d'OpenAI, puis votre demande à la suite.",
    "C'est l'une des raisons pour lesquelles il est toujours d'accord avec vous.",
])

content("Quiz · Question 4", "Faire mieux réfléchir l'IA", [
    "Vrai ou faux : un modèle qui raisonne répond aussi vite qu'un autre.",
    "",
    "**Faux : il « réfléchit » avant de répondre. Plus lent, plus fiable",
    "**sur les tâches complexes. Inutile pour reformuler un mail.",
])

content("Quiz · Question 5", "Bonus, si vous avez vu les dernières vidéos", [
    "La fenêtre de contexte, c'est quoi ?",
    "",
    "**Ce que le modèle peut lire d'un coup : vos prompts, l'historique,",
    "**les pièces jointes et sa réponse. Au-delà, il « oublie » le début.",
])

content("Vos exercices du e-learning", "« Spécifiquement pour toi » : on les fait ensemble", [
    "Ouvrez à l'écran l'exercice qui vous a bloquée.",
    "On lit la consigne, vous le faites, je reprends la main si besoin.",
    "",
    "**Ce qu'on en retient : comment aborder seule les suivants.",
])

# ── 2. Les fondamentaux ──────────────────────────────────────────────────────
tia.slide_section(prs, "2", "Les fondamentaux", "Ce que la séance ajoute au e-learning")

content("Les mots, avec vos exemples", "Ce qui se cache derrière le vocabulaire", [
    "**IA générative : produit du texte, des images, du son à partir d'une demande.",
    "**Modèle : le « moteur » (GPT, Claude, Gemini). L'appli n'est que la vitrine.",
    "",
    "**Agent : un modèle qui enchaîne des actions seul (chercher, trier, écrire).",
    "Ex. : veiller sur les appels à projets et vous en faire la synthèse.",
])

content("Les mots, avec vos exemples", "L'hallucination : faux, mais dit avec aplomb", [
    "Votre croisière : une réponse fausse, énoncée avec assurance.",
    "Le modèle ne ment pas. Il produit toujours une suite, vraie ou non.",
    "",
    "**Les parades : vérifier les faits importants, exiger les sources,",
    "**demander « Es-tu certain ? Qu'est-ce qui pourrait être faux ? »",
])

content("Le panorama", "Quel outil pour quel usage ?", [
    "**ChatGPT : polyvalent, ce que vous connaissez déjà.",
    "**Claude : rédaction longue, documents, projets de travail.",
    "**Gemini : écosystème Google, lecture de vidéos.",
    "",
    "**Midjourney et Nano Banana : générer et retoucher des images (S2).",
    "**Canva : mettre en page ce que l'IA a généré.",
])

pipeline("Une méthode de prompt", "Quatre temps, à écrire une fois, à réutiliser", [
    "1. Contexte\nqui je suis, pour qui",
    "2. Consigne\nce que j'attends",
    "3. Format\nlongueur, ton, structure",
    "4. Vérification\nce que je contrôle",
], "Ce que vous faites déjà d'instinct, rendu explicite et réutilisable.")

content("Le cadre de vos données", "Ce qui entre dans un outil, et ce qui n'y entre jamais", [
    "**Jamais : nom, adresse, santé, situation sociale d'une personne réelle.",
    "**Toujours : anonymiser (« Mme A., 82 ans, seule ») ou passer au fictif.",
    "",
    "**Deux réglages à maîtriser : l'entraînement et la mémoire.",
    "**Garder une trace : ce que vous avez validé, et quand.",
])

content("Le cadre de vos données", "Pourquoi c'est votre compétence, pas un détail", [
    "Dans le médico-social, c'est le cadre que vous aurez à poser",
    "dans une structure, pour une équipe.",
    "",
    "**Distinguer : une donnée publique (un appel à projets)",
    "**et une situation nominative (une personne accompagnée).",
])

content("Vos données", "L'entraînement : au cas par cas, comme vous le souhaitez", [
    "**Par défaut : vous contribuez à améliorer le modèle. C'est un choix légitime.",
    "**Dossier innovant : une conversation temporaire, exclue de l'entraînement.",
    "",
    "**Ou le réglage global : Paramètres › Contrôles des données.",
    "Coupé, il vaut pour toutes vos conversations, jusqu'à le réactiver.",
])

content("Vos données", "Ce que l'outil retient de votre quotidien", [
    "**La mémoire : ChatGPT retient des faits sur vous, d'un échange à l'autre.",
    "**Paramètres › Personnalisation : la consulter, l'effacer, la couper.",
    "",
    "**Mémoire et entraînement sont deux réglages distincts.",
    "La conversation temporaire n'utilise ni ne crée de souvenirs.",
])

content("Vos données", "En situation professionnelle : le cadre de l'établissement", [
    "**La charte informatique et le DPO de la structure fixent la règle.",
    "**Santé, situation sociale : des données sensibles au sens du RGPD.",
    "",
    "**Un compte personnel n'est pas un outil validé par l'établissement.",
    "**Offres pro (Business, Enterprise) : pas d'entraînement par défaut, contrat.",
])

pipeline("Vos données", "Avant d'envoyer, quatre questions", [
    "Nominatif ?\n→ anonymiser",
    "Dossier innovant ?\n→ temporaire",
    "Cadre pro ?\n→ outil validé",
    "Rien de tout ça ?\n→ allez-y",
], "Votre réflexe, à écrire dans votre cadre de confidentialité.")

content("Protéger vos contenus", "Votre concept original, confié à un outil grand public", [
    "**Conditions d'utilisation : relire ce que l'outil fait de vos données.",
    "**Travailler par fragments : ne pas confier le concept entier d'un coup.",
    "",
    "**Antériorité datée : garder une trace de votre version, avant l'IA.",
    "**Titularité : ce que dit chaque outil de la propriété de ce qui en sort.",
])

content("Garder la main", "Pour que l'IA reste un instrument de travail", [
    "**Repérer quand l'outil vous emmène ailleurs que là où vous alliez.",
    "**Contrer le « toujours d'accord » : demandez-lui de vous contredire.",
    "",
    "**Fixer vos limites d'usage : quand, pour quoi, combien de temps.",
    "**La relation à l'outil : il imite l'écoute, il n'est pas une relation.",
])

tia.slide_recap(prs, "Les fondamentaux", [
    "1.  Un LLM prédit, il ne sait pas : vérifiez ce qui compte.",
    "2.  Un outil par usage, pas un outil pour tout.",
    "3.  Contexte, consigne, format, vérification : votre méthode.",
    "4.  Rien de nominatif dans un outil grand public, jamais.",
    "5.  Vos limites d'usage sont écrites, pas implicites.",
])

# ── 3. La pratique ───────────────────────────────────────────────────────────
tia.slide_section(prs, "3", "La pratique", "Partage d'écran : vous faites, je montre")

content("Exercice · Étape 1", "Votre base de contexte personnelle", [
    "Un texte que vous collerez en tête de vos échanges avec l'IA :",
    "**qui vous êtes, votre métier visé, votre façon d'écrire, vos exigences.",
    "",
    "On l'écrit ensemble, puis on la teste dans ChatGPT.",
])

content("Exercice · Étape 2", "Le premier support : une réunion partenaires", [
    "Projet fictif : lutter contre l'isolement des personnes âgées à domicile.",
    "**Livrable : l'ordre du jour d'une réunion de lancement avec les partenaires.",
    "",
    "Avec la méthode : contexte, consigne, format, vérification.",
    "Puis : « Contredis-moi : qu'est-ce qui manque à cet ordre du jour ? »",
])

content("Exercice · Étape 3", "Votre cadre de confidentialité", [
    "**Une page : ce qui entre, ce qui n'entre jamais, comment anonymiser.",
    "**À l'écran : entraînement, conversation temporaire et mémoire de ChatGPT.",
    "",
    "**Bonus : votre compte Claude, avec les mêmes précautions.",
])

# ── 4. Les devoirs ───────────────────────────────────────────────────────────
tia.slide_section(prs, "4", "Les devoirs", "Pour la séance 2, lundi 13 octobre")

content("Devoirs · avant le 13 octobre", None, [
    "**1.  Finir « Comprendre l'IA sans jargon » (hallucinations, contexte)",
    "**2.  Suivre « Focus Midjourney & Nano Banana »",
    "**3.  Suivre « Claude — Les fondamentaux », compte créé en séance",
    "",
    "**4.  Utiliser votre base de contexte sur 3 situations réelles",
    "**5.  Écrire vos limites d'usage personnelles (5 lignes)",
    "**6.  M'envoyer le projet visuel, fil rouge de la S2",
])

tia.slide_questions(prs)
tia.save(prs, OUTPUT_PATH)
