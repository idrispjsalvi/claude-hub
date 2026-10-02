---
name: "creer-ligne-content-machine"
description: "Crée dans Airtable Content Machine une news et son Dossier à partir d'un sujet perso (test d'outil, retour d'expérience, idée) qu'Idris raconte en conversation, prête pour rediger-post-linkedin ou rediger-substack."
---

# Créer une ligne Content Machine depuis une conversation

## Pourquoi ce skill existe

La veille (skill `veille-ia`) alimente la base Content Machine avec des news trouvées par Claude. Mais Idris a aussi des sujets qui ne viennent pas de la veille : un outil qu'il a testé, une formation qu'il a donnée, une discussion avec un client, une idée. Ce skill transforme ce qu'il raconte en une news Airtable complète, au même format que celles de la veille, et en un **Dossier** qui la porte (c'est sur le dossier que vivent l'Angle attendu, les statuts et les textes). `rediger-post-linkedin` et `rediger-substack` peuvent ensuite écrire.

La différence clé avec la veille : ici, la matière vient d'Idris, pas du web. Claude structure et complète, il n'invente rien.

## Langue

Ce skill est en français. Les valeurs écrites dans Airtable (Sujet, Résumé IA, Analyse IA, Source, titre du Dossier, En bref, Angle attendu) sont en **anglais**, comme pour la veille, parce qu'Idris publie en anglais. Les échanges dans le chat se font en français (ou dans la langue d'Idris).

## Avant de commencer

Lire ces références (chemins relatifs au dossier de ce skill) :

- `../../references/content-machine.md` : identifiants de la base, champs, statuts et pièges, règles d'écriture.
- `../../references/angle-attendu.md` : ce qu'un skill de rédaction attend d'un Angle attendu (pour en écrire un qu'il comprendra).
- `../../references/partage/regles-ecriture.md` : fiabilité, recherche, typographie (aucun tiret cadratin), données personnelles.

## Déclenchement

Utiliser ce skill quand Idris dit qu'il veut créer une ligne Content Machine, ajouter un sujet perso, transformer un test, une expérience ou une idée en contenu, ou qu'il raconte un test d'outil en disant qu'il veut en faire un post, une note ou un article. Aussi quand un autre skill (par exemple un débrief de séance ou de mission) propose un sujet tiré du terrain : dans ce cas le sujet doit déjà être anonymisé, et on vérifie qu'aucun nom d'apprenant, de client ou d'entreprise n'entre dans la ligne sans accord explicite d'Idris.

## Principe n°1 : ne rien inventer

Tout ce qui concerne le vécu d'Idris (ce qu'il a testé, combien de temps, ce qui a marché ou planté, ses chiffres, son avis) vient uniquement de ce qu'il a dit dans la conversation. Ne jamais combler un trou avec une supposition. Si une information manque, la demander ou la laisser de côté. Les faits sur l'outil ou le sujet lui-même (ce que c'est, prix, éditeur) peuvent être vérifiés par recherche web, avec une source réellement consultée.

## Workflow

### 1. Recueillir la matière

Laisser Idris raconter, en vrac si besoin. Puis compléter avec **quelques questions courtes, une à trois à la fois**, seulement sur ce qui manque. Ne pas dérouler un questionnaire. Ce qu'il faut avoir à la fin :

- **Le sujet** : de quoi s'agit-il (outil, événement, expérience, idée) et son nom exact.
- **Ce qu'il a fait ou vécu** : le contexte du test ou de l'expérience (durée, cas d'usage, conditions).
- **Ce qu'il a constaté** : ce qui a bien marché, ce qui a coincé, les chiffres ou exemples concrets.
- **Son avis** : sa position, ce qu'il veut faire passer.
- **Consignes de contenu** (optionnel) : ton, longueur, question finale, chiffres à aller chercher, comparaison à faire, point à vérifier.
- **Une source à citer** (optionnel) : URL du site de l'outil, de l'article ou de la page concernée.

Si Idris a déjà tout dit dans son premier message, ne rien redemander : passer directement à l'étape 2.

### 2. Recherche complémentaire (seulement si utile)

Faire une recherche web uniquement si :

- Idris le demande ("vérifie", "va chercher", "compare avec"), ou
- il manque un fait de base sur l'outil (ce que c'est, éditeur, prix, date de sortie) que l'Analyse IA doit contenir, ou
- l'URL officielle est manquante et utile comme Source URL.

Privilégier les sources primaires (site officiel, page de tarifs, documentation). Vérifier les dates. Ne jamais inventer un chiffre, une source ou une URL. Garder la liste des sources réellement consultées pour le résumé du chat.

### 3. Rédiger les champs (en anglais)

News (table Content Machine) :

| Champ | Contenu |
|---|---|
| **Sujet** | Titre informatif, une ligne, qui dit de quoi il s'agit (par exemple "Idris tested X: what worked and what broke"). Pas de titre racoleur. |
| **Résumé IA** | 3 à 5 phrases factuelles : ce qu'est le sujet (outil, événement) et ce qu'Idris a fait avec. Sans opinion. |
| **Analyse IA** | Commence par une ligne "Reliability: Confirmed (first-hand test by Idris)" quand c'est un test ou un vécu direct, ou la fiabilité réelle pour un fait externe non vérifié par Idris. Puis 6 à 12 lignes : ce qu'il a constaté (résultats, limites, chiffres), ce que ça montre, les points faibles ou risques mentionnés, ce qui est exploitable pour des entreprises ou des particuliers. S'appuyer sur ce qu'il a dit, pas sur des suppositions. Termine par "Key takeaway:". |
| **Source** | "Personal test" (test perso), "Personal experience", ou le nom de la source externe si c'est le sujet principal. |
| **Source URL** | URL réellement consultée (site officiel de l'outil, article). Laisser vide s'il n'y en a pas, ne jamais en reconstruire une de mémoire. |
| **Date de la source** | Champ date, format AAAA-MM-JJ : la date du jour pour un test ou une expérience récente, sinon la date réelle de la source. |
| **Angle attendu** (sur le Dossier) | La position d'Idris, écrite comme un brief pour les skills de rédaction (`rediger-post-linkedin`, `rediger-substack`, voir `angle-attendu.md`) : son avis, l'expérience vécue à mentionner explicitement ("I tested it for X days on Y", sinon le skill de rédaction n'écrira pas de vécu), les consignes de fond (recherches à faire) et de forme (ton, longueur, question finale) qu'il a données. Reprendre ses mots et l'intensité de son avis, sans l'adoucir ni le durcir. Le champ est en anglais, sauf mots qu'il veut garder en français. |

Dossier (table Dossiers) : **Dossier** (titre du sujet), **En bref** (2 ou 3 phrases), **News** (la news créée, plus des news existantes si Idris relie son test à une actualité de la base), **Dernière news** (Date de la source), **État** "Retenu", **Angle attendu** comme décrit dans le tableau. Laisser **Angles proposés** et **Priorité** vides : c'est le rôle de la veille, et ici l'angle vient d'Idris.

La différence avec la veille : ici Claude remplit **Angle attendu**, parce que c'est Idris qui vient de dire son avis en conversation. Ce n'est pas un angle inventé par Claude.

### 4. Faire valider avant d'écrire

Montrer à Idris un aperçu court de la ligne (Sujet, angle, points clés de l'Analyse) dans le chat et demander confirmation, sauf s'il a dit d'écrire directement. C'est sa voix et son vécu qui partent dans la base : mieux vaut qu'il corrige avant. Poser aussi la question des statuts LinkedIn et Substack (voir plus bas) dans le même message.

### 5. Écrire dans Airtable

1. Appeler `get_table_schema` sur les tables Content Machine et Dossiers pour retrouver les identifiants de champs et les choix des champs **Statut LinkedIn**, **Statut Substack** et **État** (table Dossiers) à partir de leurs noms.
2. Avant de créer, chercher (recherche sur Sujet dans Content Machine, et sur le titre parmi les dossiers récents) si le sujet existe déjà. Si oui, le dire à Idris et demander s'il veut compléter l'existant ou créer du neuf.
3. Créer la news avec `create_records_for_table` dans la table Content Machine. Remplir seulement Sujet, Résumé IA, Analyse IA, Source, Source URL, Date de la source.
4. Créer le dossier dans la table Dossiers, lié à la news.
5. **Statuts** (sur le dossier) : mettre **Statut LinkedIn** et/ou **Statut Substack** à "À générer" seulement si Idris veut le contenu correspondant tout de suite (ou l'a demandé). Sinon les laisser vides.
6. Ne remplir aucun autre champ (Post LinkedIn, Note Substack, Article Substack, Versions publiées, dates de publication, Lien du post). Les autres règles (champ manquant, choix manquant) sont dans `content-machine.md`.

### 6. Vérifier et conclure

Relire la news et le dossier créés pour vérifier que les champs longs ne sont pas tronqués et que les retours à la ligne sont conservés. Puis répondre en français, court :

- Titre du dossier créé et statuts appliqués.
- Ce qui a été complété par recherche (avec les sources consultées) et ce qui n'a pas pu être vérifié.
- Si un statut est "À générer" : rappeler qu'il peut lancer la rédaction correspondante (LinkedIn ou Substack).
- Ce qui manquait et qu'il pourrait ajouter dans Airtable (par exemple une capture, une URL).

Ne pas recopier toute la ligne dans le chat sauf demande.

## Règles de qualité

- Ne jamais inventer d'expérience, de chiffre, de citation, de client ou de source. Ce qu'Idris n'a pas dit n'entre pas dans les champs de vécu.
- L'Analyse IA reste une matière de travail : on distingue fait, constat d'Idris et interprétation.
- Respecter le droit d'auteur : paraphraser, ne pas recopier de longs passages.
- Une seule ligne par sujet, sauf si Idris demande explicitement de couper en plusieurs angles.
- Plusieurs sujets dans la même conversation : les traiter un par un, chacun avec sa validation.
