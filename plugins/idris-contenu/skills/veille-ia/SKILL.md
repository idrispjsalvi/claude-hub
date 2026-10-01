---
name: veille-ia
description: Veille IA analytique, deux fois par jour (matin pour les news de la nuit, fin de journée pour les news de la journée). Utilise la recherche web et le mode Recherche pour sourcer, recouper et analyser les news IA les plus chaudes (France, États-Unis, Chine, international), sur l'impact de l'IA en entreprise et dans la société, les géants du secteur et les États, puis écrit une ligne par news dans la base Airtable Content Machine. Ce skill est rédigé en français mais tout le travail de Claude (recherches, analyse, contenu écrit dans Airtable, synthèse) se fait en anglais. À utiliser dès que l'utilisateur parle de veille IA, de news IA du jour, de "passage du matin" ou "passage du soir", d'alimenter Content Machine, de chercher ce qui se passe dans l'IA en ce moment, ou de préparer de la matière pour LinkedIn, Substack, un podcast ou une formation, même s'il ne dit pas explicitement "veille".
---

# Veille IA analytique

## Pourquoi ce skill existe

Idris transforme cette veille en contenu (posts LinkedIn, Notes et articles Substack, futur podcast) et l'utilise dans ses activités de formateur, coach et consultant IA auprès d'entreprises et de particuliers.

Un simple résumé n'a aucune valeur pour lui : tout le monde peut en lire un. La valeur vient de l'analyse : comprendre ce qui se joue derrière l'annonce, ce qui est prouvé et ce qui ne l'est pas, et ce que ça change pour un dirigeant, un salarié ou un citoyen. Chaque ligne écrite doit donner à Idris un angle qu'il ne trouverait pas en lisant les titres.

## Langue de travail : tout en anglais

Ce skill est rédigé en français pour qu'Idris puisse le relire, le corriger et l'adapter facilement. En revanche, Claude fait tout son travail en anglais, parce qu'Idris publie son contenu en anglais (LinkedIn, Substack, podcast) même s'il travaille aussi beaucoup en français.

- **Tout ce que Claude écrit est en anglais** : les valeurs de tous les champs Airtable (Sujet, Résumé IA, Analyse IA, Source), la synthèse finale dans le chat, et tout message adressé à l'utilisateur pendant le passage. Les noms des champs Airtable restent tels quels (Résumé IA, Analyse IA, etc.).
- **Les recherches sont bilingues quand c'est utile.** Chercher en anglais par défaut, mais chercher aussi en français (et dans d'autres langues si pertinent) pour trouver les sources françaises, européennes ou chinoises qui n'existent pas en anglais. Ne pas se priver d'une bonne source parce qu'elle est en français.
- **Traduire et paraphraser.** Une source en français ou dans une autre langue est résumée et analysée en anglais. Ne pas laisser de passages non traduits, et rester fidèle au sens. Le nom de la source (par exemple "Les Echos") et l'URL restent inchangés.
- **Les noms propres, titres officiels et termes techniques** gardent leur forme d'origine. Quand un terme français n'a pas d'équivalent courant en anglais, le garder et l'expliquer brièvement la première fois.
- **Style** : anglais clair, direct et naturel, sans jargon inutile, sans tiret cadratin. Éviter le style traduit mot à mot ou trop académique : Idris réutilise ces textes comme matière de contenu.

## Avant de commencer

Lire ces références (chemins relatifs au dossier de ce skill) :

- `../../references/regard-editorial.md` : le regard éditorial d'Idris, qui oriente toute l'analyse.
- `../../references/content-machine.md` : identifiants de la base, champs, règles d'écriture dans Airtable.
- `../../references/partage/regles-ecriture.md` : fiabilité, recherche, typographie (aucun tiret cadratin).

Le regard éditorial oriente l'analyse, mais ne doit jamais la fausser.

## Étape 0 : déterminer le passage et la fenêtre

Fuseau : Europe/Paris. Déduire le passage de l'heure actuelle ou de la demande de l'utilisateur.

- **Matin** : news publiées depuis la veille 18h jusqu'à maintenant. Ce sont les news de la nuit, dont beaucoup viennent des États-Unis et d'Asie.
- **Soir** : news publiées depuis 8h le jour même jusqu'à maintenant.

Fenêtre stricte. Une news publiée en dehors de la fenêtre n'est retenue que si un développement nouveau majeur est survenu dans la fenêtre (réaction officielle, démenti, chiffre nouveau), et dans ce cas le développement nouveau est le sujet.

## Étape 1 : ratisser large avec la recherche web

Objectif : constituer une liste brute d'une trentaine de candidates.

1. Lire la table **Sources** de la base Content Machine (liste de sources suivies par Idris) et vérifier ce qu'elles ont publié dans la fenêtre. La liste est un point de départ, pas une limite.
2. Lancer des recherches web par catégorie, avec la date du jour dans les requêtes ("aujourd'hui", date explicite) pour forcer la fraîcheur :
   - **Secteur IA** : annonces des géants (OpenAI, Anthropic, Google DeepMind, Meta, Microsoft, Nvidia, Mistral, xAI), levées de fonds, acquisitions, départs et arrivées clés, résultats de recherche.
   - **News Français** : écosystème français et européen, régulation (AI Act, CNIL, gouvernement), entreprises françaises qui déploient l'IA.
   - **News Américaine** : politique américaine de l'IA, Big Tech, décisions de justice, controverses.
   - **News Mondial** : Chine (DeepSeek, Alibaba, Baidu, Moonshot, etc.), Europe, Moyen-Orient, Inde, ONU, G7, régulations et rivalités entre États.
   - **Outils** : nouveaux outils et fonctionnalités que des entreprises ou des particuliers peuvent utiliser.
   - **Impact entreprise et société** : emploi, productivité, cas d'usage réels en entreprise, études chiffrées, éthique, désinformation, éducation.
3. Vérifier la date de publication de chaque résultat avant de le garder. Les moteurs remontent souvent du contenu ancien qui semble récent. Si la date est introuvable, ouvrir la page.
4. Privilégier les sources primaires (communiqué officiel, blog de l'entreprise, décision de justice, texte de loi, article scientifique) aux articles qui les commentent.

## Étape 2 : sélectionner 10 à 15 news

Garder 10 à 15 news. Une news est "chaude" quand elle cumule plusieurs de ces critères :

- Elle change quelque chose de concret pour des entreprises, des salariés ou l'action publique.
- Elle implique un géant du secteur ou un État.
- Elle est nouvelle, pas la énième reprise d'une histoire connue.
- Elle est controversée, ou contient une tension, une contradiction ou un enjeu de pouvoir.
- Idris peut en tirer un contenu, un exemple de formation ou un conseil concret pour des entreprises ou des particuliers.

Équilibre visé : chaque catégorie couverte quand la fenêtre le permet, avec au moins 2 news France et au moins 2 hors États-Unis. Ne jamais remplir avec des news faibles pour atteindre 10 : mieux vaut 10 bonnes que 15 dont 5 médiocres, et le signaler dans la synthèse.

Dédoublonnage : avant de retenir une news, chercher dans la table Content Machine (recherche sur Sujet et Source URL) si elle a déjà été traitée. Si oui, ne la recréer que s'il y a un développement nouveau.

## Étape 3 : investiguer chaque news retenue

Pour chaque news retenue, lancer une investigation approfondie avec le mode Recherche. Si le mode Recherche n'est pas disponible dans le contexte d'exécution (par exemple une tâche planifiée), le remplacer par au moins 3 recherches web croisées par news : la source primaire, une source indépendante, et une source qui contredit ou nuance.

L'investigation répond à ces questions :

1. **Le fait** : qu'est-ce qui est réellement établi ? Qui l'affirme, avec quelles preuves ?
2. **Le recoupement** : d'autres sources indépendantes confirment-elles ? Y a-t-il des démentis, des réserves d'experts, une contre-expertise ?
3. **Les intérêts** : à qui profite l'annonce ? Qui parle, et pourquoi maintenant (levée de fonds, procès, lobbying, concurrence, calendrier politique) ?
4. **Le non-dit** : qu'est-ce que la news omet, minimise ou contourne ? Quelles conditions, limites ou coûts sont cachés ?
5. **Les conséquences** : ce que ça change à 3 mois et à 3 ans pour les entreprises, les salariés, les particuliers, les États.
6. **Les liens** : quelle tendance de fond ou quelle autre news récente cela éclaire-t-il ?
7. **L'exploitable** : que peut en faire concrètement une entreprise ou un particulier, et que peut en dire Idris dans ses contenus ou ses formations ?

Une affirmation spectaculaire (résolution d'un problème scientifique majeur, performance record, chiffre d'impact énorme) exige un recoupement renforcé. Tant qu'elle n'est pas confirmée par une source indépendante ou un tiers compétent, elle est classée comme annonce non vérifiée, et l'analyse explique ce qui manque pour la valider.

Une accusation (vol, plagiat, violation de règles) est traitée comme une accusation : présenter les deux versions, les preuves de chacune, et ne pas trancher sans élément solide.

## Étape 4 : rédiger les champs

Écrire en anglais (voir la section sur la langue de travail), ton direct, sans jargon inutile, sans tiret cadratin. Chaque champ a un rôle précis. Les intitulés entre guillemets ci-dessous sont à écrire tels quels en anglais dans les champs.

| Champ Airtable | Contenu |
|---|---|
| **Sujet** | Titre informatif, une ligne, qui dit ce qui s'est passé (pas un titre racoleur). |
| **Résumé IA** | 3 à 5 phrases : les faits établis, sans opinion. Ce qui s'est passé, qui, quand, chiffres clés. |
| **Analyse IA** | Le cœur de la valeur. 8 à 15 lignes structurées selon les questions de l'étape 3 : ce qui est prouvé, les intérêts en jeu, le non-dit, les conséquences. Commence par une ligne "Reliability: Confirmed / Partially confirmed / Unverified / Disputed" suivie d'une courte justification. Termine par une phrase "Key takeaway:". |
| **Source** | Nom de la source principale (par exemple "Reuters", "Blog OpenAI"). |
| **Source URL** | URL exacte de la source principale. Toujours une source réellement consultée, jamais reconstruite de mémoire. |
| **Date de la source** | Date de publication de la source principale (champ de type date, format AAAA-MM-JJ, sans heure). |

Ne remplir aucun autre champ de la table. En particulier **Angle attendu** reste vide : Idris le remplit lui-même à la main après avoir lu la veille, c'est son choix éditorial. Les champs Post LinkedIn, Note Substack, Article Substack, Statut LinkedIn, Statut Substack, dates de publication et Lien du post relèvent de la production de contenu ultérieure et restent vides aussi.

La catégorie (Secteur IA, News Français, News Américaine, News Mondial, Outils) sert uniquement à équilibrer la sélection à l'étape 2. Elle n'est pas stockée dans un champ.

### Ce qui sépare une bonne analyse d'un résumé déguisé

Exemple d'illustration (hypothétique) : une entreprise annonce qu'un de ses modèles a "résolu" un problème mathématique célèbre.

- **Résumé déguisé** : "L'entreprise X annonce que son modèle a résolu le problème Y, une avancée majeure pour la science."
- **Analyse** : ce qui est réellement publié (preuve complète, prépublication, simple communiqué ?), qui a vérifié, ce que disent les spécialistes du domaine, le calendrier de l'annonce par rapport à la levée de fonds ou aux concurrents, ce que la preuve (si elle existe) change vraiment pour l'industrie, et ce que ça dit de la manière dont on doit lire les annonces de performance des labos.

La règle : si la phrase pourrait être écrite sans avoir fait aucune recherche au-delà de l'article, elle n'a pas sa place dans l'Analyse IA.

## Étape 5 : écrire dans Airtable

Identifiants et règles générales : voir `../../references/content-machine.md`. Ce skill écrit dans la table **Content Machine** et lit la table **Sources**.

Procédure :

1. Appeler `list_tables_for_base` pour récupérer les identifiants de champs à jour, à partir de leur nom.
2. Si le champ **Analyse IA** ou **Date de la source** n'existe pas, ne pas le créer de son propre chef et ne pas écrire de lignes à moitié remplies : le signaler à l'utilisateur et s'arrêter là.
3. Ne toucher à aucun champ de statut ni de production (Statut LinkedIn, Statut Substack, Angle attendu, etc.) : Idris les gère lui-même.
4. Créer les lignes avec `create_records_for_table`, par lots de 10 au maximum.
5. Relire quelques lignes créées pour vérifier que les champs longs (Analyse IA) n'ont pas été tronqués.

## Étape 6 : retour dans le chat

Terminer par une synthèse courte en anglais, pas un second rapport :

- Le passage traité (matin ou soir) et la fenêtre couverte.
- Le nombre de news écrites dans la base.
- Les 3 news les plus chaudes en une phrase chacune, avec ce qui les rend exploitables pour du contenu.
- Les points d'attention : news non vérifiées, controverses à suivre, sources qui n'ont pas pu être ouvertes, éventuelle fenêtre pauvre en bonnes news.

## Règles de qualité

- Ne jamais inventer une source, une URL, une citation ou un chiffre. Une info non retrouvée est signalée comme telle.
- Respecter le droit d'auteur : paraphraser, ne jamais recopier de longs passages des articles sources.
- Distinguer explicitement fait, allégation et interprétation.
- Rester politiquement neutre dans le ton : analyser les intérêts et les arguments de chaque camp sans prendre parti.
- Ne pas répéter une news déjà traitée sans développement nouveau.
- Si la recherche web échoue ou si la fenêtre est vide, le dire clairement plutôt que d'écrire des lignes faibles.

