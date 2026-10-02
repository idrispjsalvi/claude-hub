#!/usr/bin/env python3
"""Timothé BERNARD : séance 1 (ven. 2 oct. 2026, 13h-15h) : n8n et webhooks, sur le cas artisans. Charte TIA."""
import importlib.util
import os

HERE = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.join(HERE, "..", "..", "kit")
_spec = importlib.util.spec_from_file_location("tia", os.path.join(KIT, "lib-slides-python.py"))
tia = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(tia)

OUTPUT_PATH = os.path.join(HERE, "tim-bernard-s1-n8n-webhooks.pptx")
KICKER = "SÉANCE 1 / 4 · TIMOTHÉ BERNARD"

# _draw_blocks_on_slide pose chaque ligne dans une boîte de 0.45" : une ligne qui passe à la ligne
# chevauche la suivante sans que verif-slides le voie. On borne la longueur et la hauteur ici.
MAX_CHARS = 78


def pipeline(header, subtitle, steps, note):
    # La note native de slide_pipeline tombe à 6.4" : verif-slides la signale. On la pose sous les
    # boîtes, plus bas quand le diagramme passe sur deux lignes.
    slide = tia.slide_pipeline(prs, header, subtitle, steps)
    y = 4.5 if len(steps) <= 4 else 6.05
    tia.add_textbox(slide, tia.Inches(0.7), tia.Inches(y), tia.Inches(12.0), tia.Inches(0.7),
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
tia.slide_cover(prs, KICKER, "n8n et les webhooks, compris pour de bon",
                "Ta première demande d'artisan, reçue et triée",
                "Vendredi 2 octobre 2026 · 13h-15h · Idris Salvi")

content("Ce qu'on a fixé le 25 septembre", None, [
    "**Le fil rouge : une offre d'automatisation pour artisans, puis TPE/PME.",
    "**Le cas d'usage : demande reçue → formulaire → devis IA → l'artisan valide.",
    "",
    "**Le projet médical (ECN) reste de côté pendant la formation.",
    "**Objectif de commercialisation : 1er décembre 2026.",
])

content("Ce que tu m'as demandé hier", None, [
    "> je veux vraiment poncer n8n un max",
    "> ce que j'aimerai c'est vraiment comprendre moi meme sans IA à coté",
    "",
    "**Donc aujourd'hui : n8n uniquement, et c'est toi qui tiens la souris.",
    "**Pas de Claude pour construire. Tu comprends chaque nœud avant le suivant.",
])

content("Le déroulé de cet après-midi", None, [
    "**1.  Quiz (10 min) sur la vidéo et les fiches que tu as vues",
    "**2.  Ton workflow d'hier soir, relu ensemble (10 min)",
    "**3.  Webhook, Edit Fields, Switch : les 3 nœuds qui t'ont perdu (15 min)",
    "",
    "**4.  La pratique (60 min) : ton premier workflow « demande artisan »",
    "**5.  Les devoirs et la date de la séance 2 (15 min)",
])

# ── 1. Quiz ──────────────────────────────────────────────────────────────────
tia.slide_section(prs, "1", "Quiz d'ouverture", "Cinq questions sur la découverte de n8n")

content("Quiz · Question 1", "Par quoi commence toujours un workflow ?", [
    "A.  Une action (envoyer un mail, écrire dans une base)",
    "B.  Un trigger, le déclencheur, repéré par le petit éclair",
    "C.  Une condition IF",
    "",
    "**Réponse B : manuel, planifié, webhook, formulaire... il en faut un.",
])

content("Quiz · Question 2", "Filter, IF ou Switch ?", [
    "Une demande peut concerner la plomberie, l'électricité ou autre chose.",
    "Quel nœud pour envoyer chaque cas sur son propre chemin ?",
    "",
    "**Switch : un IF à plusieurs branches.",
    "**IF : deux branches (vrai / faux). Filter : on continue ou on s'arrête.",
])

content("Quiz · Question 3", "Deux façons d'aller chercher une donnée", [
    "` {{ $json.prenom }}",
    "` {{ $('Params').item.json.prenom }}",
    "",
    "**La 1re lit le nœud juste avant, quel qu'il soit.",
    "**La 2e lit un nœud précis, par son nom : plus sûr quand le workflow grandit.",
])

content("Quiz · Question 4", "Un « item », c'est quoi ?", [
    "A.  Un nœud du workflow",
    "B.  Un objet JSON, entre accolades : une personne, une demande, une ligne",
    "C.  Une exécution",
    "",
    "**Réponse B : 3 demandes reçues = 3 items, chaque nœud traite chacun.",
])

content("Quiz · Question 5", "Ton workflow a planté cette nuit", [
    "Où vas-tu voir ce qui s'est passé ?",
    "",
    "**L'onglet Executions : les exécutions en erreur sont en rouge.",
    "**Tu cliques dessus et tu vois, nœud par nœud, les données entrées et sorties.",
])

# ── 2. Ton workflow d'hier soir ──────────────────────────────────────────────
tia.slide_section(prs, "2", "Ton workflow d'hier soir", "Tu as bien fait de t'arrêter là")

pipeline("Ce que montre ta capture", "Webhook POST → Edit Fields → Switch → deux Edit Fields", [
    "Webhook\nPOST, 1 item reçu",
    "Edit Fields\n1 item",
    "Switch\nmode Rules",
    "Edit Fields1 et 2\ntous deux sur « 0 »",
], "Les deux branches partent de la même sortie : l'item va dans les deux.")

content("Pourquoi ça t'a perdu", "Le Switch n'aiguille rien s'il n'a qu'une sortie", [
    "**Chaque règle du Switch crée une sortie : 0, 1, 2...",
    "**Brancher deux nœuds sur la sortie 0 = les deux reçoivent la même donnée.",
    "",
    "Pour trier, il faut une règle par cas, et un nœud par sortie.",
    "On le reconstruit proprement tout à l'heure, toi aux commandes.",
])

# ── 3. Les trois nœuds ───────────────────────────────────────────────────────
tia.slide_section(prs, "3", "Les trois nœuds clés", "Webhook, Edit Fields, Switch")

pipeline("Le chemin d'une demande d'artisan", "Ce qu'on construit aujourd'hui", [
    "Le client\nremplit un formulaire",
    "Webhook\nn8n reçoit la demande",
    "Edit Fields\non garde l'utile",
    "Switch\non trie par métier",
    "Respond\n« demande reçue »",
], "Plus tard : un nœud IA rédige le brouillon de devis, l'artisan valide.")

content("Le Webhook", "L'inverse du HTTP Request", [
    "**HTTP Request : n8n appelle un autre service.",
    "**Webhook : un autre service (site, formulaire) appelle n8n.",
    "",
    "**URL de test : elle n'écoute que pendant que tu cliques sur « écouter ».",
    "**URL de production : elle tourne seule, une fois le workflow activé.",
])

content("Le Webhook", "Où arrive la donnée ?", [
    "En POST, la demande arrive dans le « body » de l'item.",
    "` {{ $json.body.type_travaux }}",
    "",
    "**À côté : headers, query, params. Tu peux les ignorer pour l'instant.",
    "**Réflexe : regarde toujours l'onglet OUTPUT avant de mapper.",
])

content("Edit Fields (Set)", "Le nœud qui fait le ménage", [
    "**Il ne garde que les champs utiles et leur donne un nom clair.",
    "**Exemple : body.type_travaux devient simplement « metier ».",
    "",
    "Les nœuds suivants lisent des champs propres, pas tout le webhook.",
    "Tu peux aussi y écrire des valeurs fixes : un tarif, un message.",
])

content("Le Switch", "Une règle = une sortie", [
    "**Règle 0 : metier = plomberie → sortie 0",
    "**Règle 1 : metier = électricité → sortie 1",
    "**Fallback output : aucune règle vraie → une sortie « à qualifier »",
    "",
    "Par défaut, l'item sort par la première règle vraie.",
    "Renomme les sorties : tu liras ton workflow sans l'ouvrir.",
])

tia.slide_recap(prs, "Les trois nœuds clés", [
    "1.  Webhook : un service extérieur appelle n8n. Test d'abord, production ensuite.",
    "2.  En POST, la donnée est dans $json.body.",
    "3.  Edit Fields : on garde l'utile, on renomme clairement.",
    "4.  Switch : une règle par cas, un nœud par sortie, un fallback.",
    "5.  Avant de mapper, on lit l'OUTPUT du nœud précédent.",
])

# ── 4. La pratique ───────────────────────────────────────────────────────────
tia.slide_section(prs, "4", "La pratique", "Partage d'écran : tu fais, je reprends la main si besoin")

content("Exercice · La demande de test", "Ce qu'envoie le formulaire d'un client", [
    "` {",
    "`   \"nom\": \"Mme Durand\",",
    "`   \"type_travaux\": \"plomberie\",",
    "`   \"description\": \"Fuite sous l'évier de la cuisine\",",
    "`   \"code_postal\": \"69007\"",
    "` }",
])

content("Exercice · Étapes 1 à 3", "Recevoir la demande", [
    "**1.  Nouveau workflow « Demande artisan v1 », trigger Webhook en POST.",
    "**2.  Clique sur écouter, puis envoie la demande de test depuis un",
    "**     second workflow : HTTP Request, POST, URL de test, body JSON.",
    "",
    "**3.  Lis l'OUTPUT du Webhook : où se trouve « type_travaux » ?",
])

content("Exercice · Étapes 4 à 6", "Nettoyer et trier", [
    "**4.  Edit Fields : nom, metier, description, code_postal. Rien d'autre.",
    "**5.  Switch : plomberie (0), électricité (1), fallback « à qualifier ».",
    "**6.  Un Edit Fields par sortie : le message à renvoyer au client.",
    "",
    "Teste les 3 cas en changeant « type_travaux » dans ta demande de test.",
])

content("Exercice · Étapes 7 et 8", "Répondre et passer en production", [
    "**7.  Respond to Webhook : « Merci, votre demande est bien reçue ».",
    "**     (dans le Webhook : réponse via le nœud Respond to Webhook)",
    "",
    "**8.  Active le workflow, remplace l'URL de test par celle de production.",
    "Regarde le résultat dans l'onglet Executions, comme dans le quiz.",
])

content("Si on a le temps", "Un aperçu de la suite", [
    "**Ajouter un nœud IA sur la branche plomberie :",
    "**« Rédige un brouillon de devis à partir de cette description. »",
    "",
    "C'est la brique « devis IA » de ton offre. On la creuse ensuite.",
])

# ── 5. Les devoirs ───────────────────────────────────────────────────────────
tia.slide_section(prs, "5", "Les devoirs", "Pour la séance 2")

content("Devoirs · avant la séance 2", None, [
    "**1.  Vidéos n8n, dans cet ordre : Variables, JSON et mapping,",
    "**     puis Conditions (IF, Switch, Filter), puis HTTP Request et Webhooks",
    "**2.  Refaire « Demande artisan v1 » de zéro, seul, sans IA ni notes,",
    "**     avec un 3e métier en plus",
    "",
    "**3.  M'envoyer ton brief artisans sur idris@the-intelligence-academy.com",
    "**4.  Écrire à Antoine pour débloquer les modules Cursor et Claude Code",
])

content("Le brief artisans", "Une page, pour construire le devis IA", [
    "**1 métier d'artisan cible pour commencer (plombier, électricien...).",
    "**Les champs d'une demande : ce que le client doit remplir.",
    "",
    "**Ce que contient un devis : postes, unités, prix, TVA, mentions.",
    "**Un exemple de devis, réel ou fictif.",
])

tia.slide_questions(prs)
tia.save(prs, OUTPUT_PATH)
