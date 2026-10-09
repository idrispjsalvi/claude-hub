#!/usr/bin/env python3
"""Timothé BERNARD : séance 1, v2 (ven. 9 oct. 2026, 13h-15h) : Tally → n8n → Airtable pour Ylang Ylang. Charte TIA."""
import importlib.util
import os

HERE = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.join(HERE, "..", "..", "kit")
_spec = importlib.util.spec_from_file_location("tia", os.path.join(KIT, "lib-slides-python.py"))
tia = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(tia)

OUTPUT_PATH = os.path.join(HERE, "tim-bernard-s1-v2-tally-n8n-airtable.pptx")
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
tia.slide_cover(prs, KICKER, "Ta première démo Ylang Ylang",
                "Tally → n8n → Airtable, testé avec une vraie demande",
                "Vendredi 9 octobre 2026 · 13h-15h · Idris Salvi")

content("Ce que tu m'as écrit hier", None, [
    "> j'aimerais bien qu'on voit via Webhook et qu'on fasse marcher",
    "> une vraie automatisation",
    "",
    "**Ylang Ylang : site, hébergement et gestion des demandes pour artisans.",
    "**Leur problème : ils répondent tard et ne relancent jamais leurs devis.",
    "**Le livrable : un workflow testé avec une vraie soumission Tally.",
])

content("Aujourd'hui, et plus tard", None, [
    "**En séance : architecture, Tally, zone, Airtable, les deux mails, test réel.",
    "**En séance : on dessine la relance J+3 ensemble.",
    "",
    "**Devoirs : tu construis la relance J+3 et la gestion des erreurs.",
    "**Séance 2 : le prix, et le passage de la démo à un vrai artisan.",
    "**Hors périmètre (ton choix) : l'IA pour le prix, le site web.",
])

content("Le déroulé", "Chaque bloc : 5 min de théorie, puis tu pratiques", [
    "**1.  Quiz (10 min)  ·  2.  Architecture : 3 workflows (15 min)",
    "**3.  Tally → Webhook (20 min)  ·  4.  Le Switch zone (15 min)",
    "",
    "**5.  Airtable (15 min)  ·  6.  Les deux mails (20 min)",
    "**7.  Test réel (10 min)  ·  8.  Relance J+3 et devoirs (10 min)",
])

# ── 1. Quiz ──────────────────────────────────────────────────────────────────
tia.slide_section(prs, "1", "Quiz d'ouverture", "Quatre questions sur ce que tu as vu")

content("Quiz · Question 1", "Une demande arrive à 3h du matin", [
    "Quelle URL ton formulaire Tally doit-il appeler ?",
    "A.  L'URL de test du Webhook",
    "B.  L'URL de production du Webhook",
    "",
    "**Réponse B : l'URL de test n'écoute que quand tu cliques sur « écouter ».",
    "**La production tourne seule, une fois le workflow activé.",
])

content("Quiz · Question 2", "Ton Webhook reçoit ceci en POST", [
    "` { \"code_postal\": \"34700\" }",
    "Quelle expression lit le code postal dans le nœud suivant ?",
    "A.  {{ $json.code_postal }}        B.  {{ $json.body.code_postal }}",
    "",
    "**Réponse B : tout est rangé dans « body ». A renvoie du vide, sans erreur.",
    "**Et avec Tally ? Ce n'est pas si simple. Réponse dans 20 minutes.",
])

content("Quiz · Question 3", "Ta capture de la semaine dernière", [
    "Edit Fields1 et Edit Fields2 sont branchés sur la sortie 0 du Switch.",
    "Que reçoit chacun des deux ?",
    "",
    "**Le même item : ton Switch n'a qu'une règle, donc une seule sortie.",
    "**Pour trier, il faut une règle par cas et un nœud par sortie.",
])

content("Quiz · Question 4", "Aucune règle du Switch ne correspond", [
    "Que devient la demande ?",
    "",
    "**Par défaut : elle est abandonnée, sans erreur. Tu ne le vois pas.",
    "**Option « Fallback Output » → « Extra Output » : une sortie de secours.",
    "C'est exactement le cas « hors zone » qu'on va construire.",
])

# ── 2. Architecture ──────────────────────────────────────────────────────────
tia.slide_section(prs, "2", "L'architecture", "Un ou deux workflows ? En fait, trois")

content("Théorie · Un workflow, un déclencheur", None, [
    "**Une demande arrive : c'est un événement → Webhook.",
    "**Chaque matin, on cherche les devis à relancer : c'est une heure → Schedule.",
    "**Un workflow plante : c'est une erreur → Error Trigger.",
    "",
    "Trois déclencheurs différents = trois workflows.",
    "Tu n'as pas à choisir : la nature du déclencheur décide pour toi.",
])

pipeline("Tes trois workflows", "Ils ne se parlent pas : ils partagent la base Airtable", [
    "Demandes\nWebhook, à chaque envoi Tally",
    "Relances\nSchedule, chaque matin",
    "Erreurs\nError Trigger, à chaque plantage",
], "Aujourd'hui on construit « Demandes ». Les deux autres sont tes devoirs.")

content("Pratique · Ta base Airtable", "À vérifier avant de toucher à n8n", [
    "**Statut : nouveau, devis envoyé, relancé, gagné, perdu.",
    "**Faut-il ajouter « hors zone » ? On le décide au bloc 4.",
    "**Date de la demande : n8n la remplira.",
    "",
    "**Il manque « Date devis envoyé » : sans elle, pas de calcul J+3.",
    "Qui la remplit ? L'artisan, à la main, quand il envoie son devis.",
])

# ── 3. Tally → Webhook ───────────────────────────────────────────────────────
tia.slide_section(prs, "3", "Tally → Webhook", "Lire les vraies données avant de les mapper")

content("Théorie · Ce que Tally envoie vraiment", None, [
    "` { \"eventType\": \"FORM_RESPONSE\", \"data\": { \"fields\": [",
    "`   { \"label\": \"Code postal\", \"value\": \"34700\" },",
    "`   { \"label\": \"Type de travaux\", \"value\": [\"a1b2c3\"], \"options\": [...] }",
    "` ] } }",
    "",
    "**Les réponses sont dans un tableau, pas dans des champs nommés.",
    "**Menu déroulant : value est un identifiant. Le libellé est dans options.",
])

content("Pratique · Brancher Tally", "Partage d'écran : c'est toi qui cliques", [
    "**1.  Webhook : copie l'URL de test, clique sur « écouter ».",
    "**2.  Tally → Integrations → Webhooks : colle l'URL, envoie une réponse.",
    "**3.  Lis l'OUTPUT : où sont le code postal et le type de travaux ?",
    "",
    "**4.  Adapte ton Edit Fields : un champ propre par information.",
    "` {{ $json.body.data.fields.find(f => f.label == 'Code postal').value }}",
])

# ── 4. Le Switch zone ────────────────────────────────────────────────────────
tia.slide_section(prs, "4", "Le Switch zone", "L'artisan ne se déplace pas partout")

content("Théorie · Le Switch", "Une règle = une sortie", [
    "**Chaque règle crée sa sortie : 0, 1, 2...",
    "**L'item sort par la première règle vraie.",
    "**Fallback Output : ce qui ne correspond à rien a sa propre sortie.",
    "",
    "Renomme les sorties : tu lis le workflow sans ouvrir le nœud.",
    "Une liste de départements suffit : « commence par 34 », « 30 »...",
])

content("Pratique · Trier par zone", None, [
    "**1.  Règle « dans la zone » : le code postal commence par l'un",
    "**     des départements de l'artisan.",
    "**2.  Fallback → Extra Output, renommé « hors zone ».",
    "",
    "**3.  À décider : que reçoit un prospect hors zone ? Un refus poli, rien ?",
    "**4.  Teste les deux cas avec deux réponses Tally différentes.",
])

# ── 5. Airtable ──────────────────────────────────────────────────────────────
tia.slide_section(prs, "5", "Airtable", "Chaque demande enregistrée, avec son statut")

content("Théorie · Airtable dans n8n", None, [
    "**Accès : un Personal Access Token, limité à ta base.",
    "**Le nœud : Base → Table → opération Create, puis le mapping champ par champ.",
    "",
    "**Les pièges : une date au format ISO, un Statut qui existe déjà",
    "**dans la liste d'options (sinon Airtable refuse la ligne).",
    "` {{ $now.toISO() }}",
])

content("Pratique · Enregistrer la demande", None, [
    "**1.  Branche « dans la zone » → Airtable, Create record.",
    "**2.  Mappe les champs propres de ton Edit Fields.",
    "**3.  Statut = « nouveau », Date de la demande = maintenant.",
    "",
    "**4.  Branche « hors zone » : selon ta décision du bloc 4.",
    "**5.  Vérifie la ligne dans Airtable, pas seulement dans n8n.",
])

# ── 6. Les deux mails ────────────────────────────────────────────────────────
tia.slide_section(prs, "6", "Les deux mails", "Répondre vite, c'est ce qui fait gagner le chantier")

content("Théorie · Les expressions", "Un texte qui change selon la demande", [
    "` Bonjour {{ $json.nom }}, nous avons bien reçu votre demande.",
    "",
    "**Une phrase qui change : condition ? si vrai : si faux",
    "` {{ $json.type == 'Plomberie' ? 'Un plombier' : 'Un artisan' }}",
    "`   vous rappelle sous 24 h.",
    "",
    "**Tout le message change selon le type : un Switch, un mail par sortie.",
])

content("Pratique · Accusé de réception et notification", None, [
    "**1.  Gmail au prospect : son nom, ses travaux, le délai de rappel.",
    "**2.  Gmail à l'artisan : nom, téléphone, code postal, type, description.",
    "",
    "**3.  Relis-les : un artisan accepterait-il qu'ils partent à son nom ?",
    "Pour la démo, tout part de ton Gmail. Le vrai expéditeur : séance 2.",
])

# ── 7. Test réel ─────────────────────────────────────────────────────────────
tia.slide_section(prs, "7", "Le test réel", "On remplit le formulaire comme un vrai client")

content("Théorie · Activer le workflow", None, [
    "**Inactif : seule l'URL de test marche, et seulement quand tu écoutes.",
    "**Actif : l'URL de production tourne seule, jour et nuit.",
    "",
    "**Chaque passage laisse une trace dans l'onglet Executions.",
    "C'est là que tu iras voir si un artisan te dit « j'ai rien reçu ».",
])

content("Pratique · De bout en bout", None, [
    "**1.  Active le workflow.",
    "**2.  Dans Tally, remplace l'URL de test par celle de production.",
    "**3.  Remplis le formulaire depuis ton téléphone, comme un client.",
    "",
    "**4.  Vérifie : Executions en vert, la ligne Airtable, les deux mails.",
    "**Ta démo est prête à être montrée.",
])

tia.slide_recap(prs, "Le workflow « Demandes »", [
    "1.  Tally appelle l'URL de production du Webhook.",
    "2.  Edit Fields va chercher chaque réponse dans data.fields.",
    "3.  Le Switch trie par zone, le fallback attrape le hors zone.",
    "4.  Airtable enregistre la demande : statut « nouveau » et date.",
    "5.  Gmail répond au prospect et prévient l'artisan.",
])

# ── 8. Relance J+3 et devoirs ────────────────────────────────────────────────
tia.slide_section(prs, "8", "La relance J+3", "Le deuxième workflow, à construire seul")

pipeline("Le workflow « Relances »", "Il ne réagit à rien : il se réveille chaque matin", [
    "Schedule\nchaque matin, 9h",
    "Airtable Search\nfiltre par formule",
    "Gmail\nrelance du prospect",
    "Airtable Update\nstatut « relancé »",
], "Le statut change : la ligne sort du filtre. Pas de double relance.")

content("La formule du filtre", "Dans le champ « Filter By Formula » du nœud Airtable", [
    "` AND({Statut} = \"devis envoyé\", {Date devis envoyé},",
    "`     DATETIME_DIFF(TODAY(), {Date devis envoyé}, 'days') >= 3)",
    "",
    "**Pourquoi pas le nœud Airtable Trigger ? Il réagit à une ligne créée",
    "**ou modifiée. Le temps qui passe ne modifie aucune ligne.",
    "La ligne passe à « relancé » : elle ne sera plus relancée.",
])

content("Devoirs · avant la séance 2", None, [
    "**1.  Construire « Relances » et le tester avec une fausse ligne",
    "**     dont la date d'envoi du devis est il y a 4 jours.",
    "**2.  Créer « Erreurs » (Error Trigger → mail) et le choisir comme",
    "**     Error Workflow dans les Settings de « Demandes ».",
    "",
    "**3.  Finir le module n8n : les 3 vidéos qui restent.",
    "**4.  Relancer Antoine pour débloquer les modules verrouillés.",
])

tia.slide_questions(prs)
tia.save(prs, OUTPUT_PATH)
