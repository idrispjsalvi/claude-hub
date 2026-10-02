---
name: veille-ia
description: Veille IA analytique, deux fois par jour (matin pour les news de la nuit, fin de journée pour les news de la journée). Utilise la recherche web et le mode Recherche pour sourcer, recouper et analyser les news IA les plus chaudes (France, États-Unis, Chine, international), sur l'impact de l'IA en entreprise et dans la société, les géants du secteur et les États, puis écrit les news dans la base Airtable Content Machine et les regroupe en Dossiers (un sujet éditorial, une priorité, des angles proposés) pour qu'Idris lise peu et choisisse vite. Ce skill est rédigé en français mais tout le travail de Claude (recherches, analyse, contenu écrit dans Airtable, synthèse) se fait en anglais. À utiliser dès que l'utilisateur parle de veille IA, de news IA du jour, de "passage du matin" ou "passage du soir", d'alimenter Content Machine, de chercher ce qui se passe dans l'IA en ce moment, ou de préparer de la matière pour LinkedIn, Substack, un podcast ou une formation, même s'il ne dit pas explicitement "veille".
---

# Veille IA analytique

## Pourquoi ce skill existe

Idris transforme cette veille en contenu (posts LinkedIn, Notes et articles Substack, futur podcast) et l'utilise dans ses activités de formateur, coach et consultant IA auprès d'entreprises et de particuliers.

Idris a peu de temps pour lire. Il ne lit plus les news une par une : il lit les **Dossiers** (dans l'interface "Content Machine : ma veille", page "À lire"). Un passage réussi lui donne 3 à 6 dossiers clairs, classés par priorité, avec des angles prêts à choisir. Il doit pouvoir décider en 5 minutes de quoi il parle aujourd'hui.

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
- `../../references/content-machine.md` : identifiants de la base, tables Dossiers et Content Machine, champs, règles d'écriture dans Airtable.
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

## Étape 2 : sélectionner 6 à 10 news

Garder 6 à 10 news, pas plus. Idris ne peut pas tout lire et une news de plus coûte du temps de lecture.

La sélection sert le but du contenu d'Idris (voir "Pour qui et pourquoi" dans `regard-editorial.md`) : aider des professionnels et des entreprises à s'y retrouver dans le flux, à prendre des décisions éclairées, et montrer l'expertise d'Idris pour qu'ils fassent appel à lui. Une news n'est donc pas retenue parce qu'elle est "chaude", mais parce qu'elle passe ce filtre :

**La question centrale : est-ce qu'un dirigeant, un manager ou un professionnel devrait penser, décider ou agir autrement à cause de cette news ?** Adopter ou abandonner un outil, revoir un budget, former une équipe, se protéger d'un risque, se mettre en conformité, revoir une stratégie, ou simplement ne pas céder à un emballement ou à une peur.

Noter chaque news candidate sur trois critères, de 0 à 2 :

| Critère | 0 | 1 | 2 |
|---|---|---|---|
| **Décision** : ce que ça change pour un professionnel ou une entreprise | Rien de concret (politique, people, drame entre labos, levée de fonds sans effet sur l'usage) | Un contexte utile pour comprendre ou anticiper | Une décision ou une action à prendre maintenant (outil, budget, risque, conformité, compétences) |
| **Expertise** : Idris est-il légitime pour l'expliquer ? | Hors de ses domaines | Lien indirect | Au cœur de ce qu'il vend : adoption de l'IA en entreprise, automatisation (n8n, Make), agents, outils du quotidien (Claude, ChatGPT, Gemini, Copilot), formation et montée en compétences, cadre européen et français vu par les entreprises |
| **Timing** | Reprise d'une histoire connue | Nouveau, mais sans urgence | Ça bouge maintenant, ou ça prolonge un dossier qu'Idris a retenu ou publié |

Retenir en priorité les news à 4 et plus. Une news à 0 en Décision n'est retenue que si elle prépare clairement une décision à venir (par exemple une régulation en cours de vote) ; le dire dans l'Analyse.

Ce que ce filtre écarte en général, même quand c'est très repris : la géopolitique pure, les déclarations de dirigeants sans effet concret, les querelles entre labos, les levées de fonds de startups sans produit utilisable, les records de benchmark sans usage. Si une de ces news a quand même une traduction business, c'est cette traduction qui est le sujet.

Équilibre visé : au moins 1 news France ou Europe quand la fenêtre le permet, et au moins 1 news "terrain" (une entreprise qui déploie, un chiffre d'usage, un retour d'expérience), parce que c'est ce qui parle le plus au public d'Idris. Ne jamais remplir avec des news faibles pour atteindre 6 : mieux vaut 4 bonnes que 8 dont 4 médiocres, et le signaler dans la synthèse. Une news qui ne mérite ni un dossier ni un ajout à un dossier existant n'est pas écrite.

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
7. **L'exploitable** : quelle décision ou quelle action concrète pour une entreprise ou un professionnel, et que peut en dire Idris dans ses contenus, ses formations ou ses missions de conseil ?

Une affirmation spectaculaire (résolution d'un problème scientifique majeur, performance record, chiffre d'impact énorme) exige un recoupement renforcé. Tant qu'elle n'est pas confirmée par une source indépendante ou un tiers compétent, elle est classée comme annonce non vérifiée, et l'analyse explique ce qui manque pour la valider.

Une accusation (vol, plagiat, violation de règles) est traitée comme une accusation : présenter les deux versions, les preuves de chacune, et ne pas trancher sans élément solide.

## Étape 4 : rédiger les champs

Écrire en anglais (voir la section sur la langue de travail), ton direct, sans jargon inutile, sans tiret cadratin. Chaque champ a un rôle précis. Les intitulés entre guillemets ci-dessous sont à écrire tels quels en anglais dans les champs.

| Champ Airtable | Contenu |
|---|---|
| **Sujet** | Titre informatif, une ligne, qui dit ce qui s'est passé (pas un titre racoleur). |
| **Résumé IA** | 3 à 5 phrases : les faits établis, sans opinion. Ce qui s'est passé, qui, quand, chiffres clés. |
| **Analyse IA** | Le cœur de la valeur. 6 à 12 lignes structurées selon les questions de l'étape 3 : ce qui est prouvé, les intérêts en jeu, le non-dit, les conséquences. Commence par une ligne "Reliability: Confirmed / Partially confirmed / Unverified / Disputed" suivie d'une courte justification. Termine par une phrase "Key takeaway:". |
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

## Étape 5 : ranger les news en Dossiers

C'est l'étape qui fait gagner du temps à Idris. Un dossier est un **sujet éditorial**, pas une catégorie : "les agents IA qui font des bêtises en entreprise", pas "Sécurité". Idris doit pouvoir en tirer un post ou un article.

1. **Lire les dossiers ouverts** : table Dossiers, État différent de "Ignoré" et "Clos", Dernière news dans les 14 derniers jours. Lire leur titre, leur En bref et la liste de leurs news.
2. **Pour chaque news retenue**, décider :
   - elle **prolonge un dossier ouvert** (même acteurs, même enjeu, même débat) : la rattacher à ce dossier ;
   - elle **forme un sujet avec d'autres news du passage** : créer un dossier qui les regroupe ;
   - elle **tient seule** et vaut un contenu à elle seule : créer un dossier d'une seule news.
   Regrouper quand deux news se répondent (une annonce et sa critique, deux labos qui font la même chose, une tendance qui se confirme), pas seulement parce qu'elles parlent du même acteur. Une news ne va que dans un seul dossier.
3. **Remplir ou mettre à jour le dossier** (en anglais) :
   - **Dossier** : un titre qui dit la tension ou le fil ("Consumer AI agents: everyone launches, nobody has cracked it"), pas une liste.
   - **En bref** : 3 à 5 phrases qui relient les news, avec les faits et chiffres clés et ce qui est nouveau depuis la dernière mise à jour. Écrire pour Idris ("you", direct). Si le dossier prolonge un contenu qu'il a déjà publié, le dire ("Follow-up to your Instinct piece").
   - **Angles proposés** : 2 ou 3 angles, numérotés A, B, C, une ou deux lignes chacun. Chaque angle dit une position **et** le lecteur visé (dirigeant de PME, équipe ops, RH, formateur...). Les construire sur ces trois rôles, qui sont les trois façons dont le contenu d'Idris crée de la valeur :
     - **Décider** : ce que le lecteur devrait faire, vérifier ou éviter, concrètement.
     - **Décrypter** : séparer le signal du bruit (ce qui est prouvé, les intérêts, le non-dit, l'emballement ou la peur à calmer).
     - **Montrer le terrain** : ce qu'Idris voit en formation ou en mission, un test qu'il pourrait faire, une méthode qu'il peut partager. C'est l'angle qui montre son expertise et donne envie de faire appel à lui. Ne jamais inventer de vécu : formuler comme une proposition ("You could test X with...", "Share how you handle Y in your trainings").
     Ils suivent le regard éditorial d'Idris (`regard-editorial.md`), mais ce sont des propositions : Idris choisit.
   - **Priorité** : reprendre les notes de l'étape 2, au niveau du dossier (la meilleure news du dossier, plus 1 en Timing si le dossier prolonge un sujet retenu ou publié, plafonné à 2). Total de 5 ou 6 : **Haute**. 3 ou 4 : **Moyenne**. 2 ou moins : **Basse**. Au plus 3 dossiers en Haute par passage : si plus, garder ceux qui ont le meilleur score en Décision.
   - **Dernière ligne de En bref** : le score, pour qu'Idris voie pourquoi, sous la forme "Score: Decision 2/2, Expertise 2/2, Timing 1/2." 
   - **Dernière news** : date de la news la plus récente du dossier.
   - **État** : "Nouveau" pour un dossier créé. Pour un dossier existant qui reçoit une news : "Mis à jour" seulement s'il était "Nouveau" ou "Mis à jour". S'il était "Retenu", ne pas changer l'État : ajouter la news, mettre à jour En bref, et signaler la nouveauté dans la synthèse (Idris est peut-être en train d'écrire dessus).
4. Ne jamais toucher à Angle attendu, aux statuts de rédaction ni aux textes d'un dossier.

## Étape 6 : écrire dans Airtable

Identifiants et règles générales : voir `../../references/content-machine.md`.

1. Appeler `list_tables_for_base` pour récupérer les identifiants de champs à jour, à partir de leur nom, pour les tables Content Machine et Dossiers.
2. Si un champ attendu manque (Analyse IA, Date de la source, ou un champ de la table Dossiers), ne pas le créer de son propre chef et ne pas écrire de lignes à moitié remplies : le signaler à l'utilisateur et s'arrêter là.
3. Créer les news avec `create_records_for_table` dans la table Content Machine, par lots de 10 au maximum. Ne remplir que Sujet, Résumé IA, Analyse IA, Source, Source URL, Date de la source.
4. Créer les nouveaux dossiers et mettre à jour les dossiers existants dans la table Dossiers, en liant les news par leurs identifiants. Pour un dossier existant, le champ News reçoit la liste complète (anciennes news **et** nouvelles), sinon les anciennes seraient détachées.
5. Relire quelques lignes créées pour vérifier que les champs longs n'ont pas été tronqués et que les liens sont en place.

## Étape 7 : retour dans le chat

Terminer par une synthèse courte en anglais, pas un second rapport :

- Le passage traité (matin ou soir) et la fenêtre couverte.
- Le nombre de news écrites, de dossiers créés et de dossiers mis à jour.
- Les dossiers en priorité Haute, une phrase chacun.
- Les dossiers "Retenu" qui ont reçu une news nouvelle (Idris travaille peut-être dessus).
- Les points d'attention : news non vérifiées, controverses à suivre, sources qui n'ont pas pu être ouvertes, éventuelle fenêtre pauvre en bonnes news.

## Règles de qualité

- Ne jamais inventer une source, une URL, une citation ou un chiffre. Une info non retrouvée est signalée comme telle.
- Respecter le droit d'auteur : paraphraser, ne jamais recopier de longs passages des articles sources.
- Distinguer explicitement fait, allégation et interprétation.
- Rester politiquement neutre dans le ton : analyser les intérêts et les arguments de chaque camp sans prendre parti.
- Ne pas répéter une news déjà traitée sans développement nouveau.
- Si la recherche web échoue ou si la fenêtre est vide, le dire clairement plutôt que d'écrire des lignes faibles.

