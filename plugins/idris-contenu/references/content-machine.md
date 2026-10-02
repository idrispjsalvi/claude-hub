# Base Airtable Content Machine

Référence unique de la base pour tous les skills du plugin `idris-contenu`. Si la base change (champ renommé, nouveau statut), on modifie ce fichier et rien d'autre.

## Comment la base fonctionne (depuis le 2026-10-02)

- La **veille** écrit des **news** (table Content Machine), puis les range dans des **Dossiers** : un dossier est un sujet éditorial qui regroupe une ou plusieurs news.
- **Idris lit les Dossiers, pas les news.** Il le fait dans l'interface "Content Machine : ma veille", page "À lire". Il choisit un dossier, écrit l'**Angle attendu** sur le dossier (seul, ou avec le skill `affiner-angle` qui le challenge pour affiner sa position), puis passe un statut à "À générer".
- Les **skills de rédaction** travaillent sur un **dossier**. La matière vient de toutes les news liées, et le texte est écrit sur le dossier.
- Quand Idris publie, il colle son texte final dans les champs **Version publiée**. Le skill `apprendre-de-mes-corrections` compare ce texte à celui de Claude et propose des **Leçons de style**, qu'Idris valide. Les skills de rédaction lisent les leçons validées à chaque exécution (voir `style-vivant.md`).

## Identifiants

- Base **Content Machine** : `app7aTWK9J6nO1Kcm`
- Table **Dossiers** : `tblT7Fj1NpnxVJRvj` (un sujet éditorial, l'unité de travail d'Idris)
- Table **Content Machine** : `tblvEaTY3FtMohjhL` (une ligne par news : la matière)
- Table **Leçons de style** : `tbl04sKTcEi9xuQ1f`
- Table **Sources** : `tbl0F38Ff1NPc6b7o` (sources suivies par la veille ; lecture seule sauf demande d'Idris)
- Interface **Content Machine : ma veille** : `pbdyTPB5MZ0cU5nEb` (pages "À lire", "À relire et publier", "Publiés : coller la version finale", "Leçons de style à valider")

Ne jamais coder en dur les identifiants de **champs** ni de **choix** : les retrouver à partir de leur nom avec `get_table_schema` (ou `list_tables_for_base`) au début de chaque exécution. Ils peuvent changer.

## Table Dossiers

| Champ | Rempli par | Contenu |
|---|---|---|
| Dossier | veille-ia, creer-ligne-content-machine | Titre du sujet, en anglais, une ligne, qui dit la tension ou le fil (pas la liste des news) |
| Priorité | veille-ia | Haute, Moyenne, Basse : potentiel de contenu pour Idris (voir `veille-ia`) |
| État | veille-ia (Nouveau, Mis à jour) ; Idris (Retenu, Ignoré, Clos) ; affiner-angle (Retenu) | La veille ne rattache plus rien à un dossier Ignoré ou Clos |
| En bref | veille-ia | 3 à 5 phrases en anglais qui relient les news. Réécrit à chaque mise à jour |
| Angles proposés | veille-ia | 2 ou 3 angles, lettres A, B, C. Ce sont des propositions, pas l'avis d'Idris |
| News | veille-ia, creer-ligne-content-machine | Lien vers les news de la table Content Machine |
| Dernière news | veille-ia | Date de la news la plus récente du dossier |
| Angle attendu | Idris ; affiner-angle et creer-ligne-content-machine, seulement à partir de ce qu'Idris a dit et après sa validation | Le brief d'Idris, voir `angle-attendu.md` |
| Statut LinkedIn / Statut Substack | Idris ; skills de rédaction | Choix, voir plus bas |
| Post LinkedIn | rediger-post-linkedin | Texte brut prêt à coller |
| Note Substack | rediger-substack | Texte brut prêt à coller |
| Article Substack | rediger-substack | Markdown, commence par `Title:` puis `Subtitle:` |
| Version publiée LinkedIn / Note / Article | Idris | Le texte qu'il a réellement publié. Aucun skill n'y écrit |
| Date de publi prévue, Lien du post | Idris | Aucun skill n'y touche |
| Appris | apprendre-de-mes-corrections | Coché une fois l'écart analysé |

**Dossiers historiques** : les trois dossiers créés le 2026-10-02 pour les contenus publiés avant la table Dossiers ont leur Angle attendu et les textes de Claude sur la **news liée** (anciens champs Angle attendu, Post LinkedIn, Note Substack, Article Substack de la table Content Machine). C'est le seul cas où on lit ces anciens champs.

## Table Content Machine (news)

| Champ | Rempli par | Contenu |
|---|---|---|
| Sujet | veille-ia, creer-ligne-content-machine | Titre informatif, une ligne |
| Résumé IA | veille-ia, creer-ligne-content-machine | 3 à 5 phrases factuelles, en anglais |
| Analyse IA | veille-ia, creer-ligne-content-machine | Commence par "Reliability: ...", finit par "Key takeaway: ..." |
| Source | veille-ia, creer-ligne-content-machine | Nom de la source principale |
| Source URL | veille-ia, creer-ligne-content-machine | URL réellement consultée, jamais reconstruite |
| Date de la source | veille-ia, creer-ligne-content-machine | Date, format AAAA-MM-JJ |
| Dossiers | lien inverse, rempli automatiquement quand on lie la news depuis un dossier | |

Les anciens champs de production de cette table (Angle attendu, Statut LinkedIn, Post LinkedIn, Statut Substack, Note Substack, Article Substack, dates, Lien du post, Image) ne sont plus utilisés : aucun skill n'y écrit. Ils restent pour l'historique.

## Table Leçons de style

| Champ | Rempli par | Contenu |
|---|---|---|
| Leçon | apprendre-de-mes-corrections | Une consigne positive et concrète, en anglais ou en français |
| Canal | apprendre-de-mes-corrections | Tous, LinkedIn, Note, Article |
| Type | apprendre-de-mes-corrections | Ton, Structure, Accroche, Fond, Longueur, Format |
| Avant / après | apprendre-de-mes-corrections | L'exemple réel : ce que Claude avait écrit, ce qu'Idris a publié |
| Statut | apprendre-de-mes-corrections (Proposée) ; Idris (Validée, Rejetée) | Seules les leçons Validées s'appliquent |
| Occurrences | apprendre-de-mes-corrections | Nombre de fois où l'écart a été observé |
| Dossiers source | apprendre-de-mes-corrections | Les dossiers où l'écart a été observé |

## Statuts de rédaction (table Dossiers)

**Statut LinkedIn** et **Statut Substack** ont les mêmes choix :

- vide : rien de demandé
- "À générer" : Idris demande une rédaction (il écrit parfois "À généré" par erreur : c'est bien "À générer")
- "À valider" : texte écrit par Claude, en attente de relecture
- "Validé", "Publié" : posés par Idris

Pièges :

- Ne jamais confondre les deux champs : filtrer avec l'identifiant du champ du canal concerné, jamais celui de l'autre.
- Les choix ont des identifiants différents dans la table Dossiers et dans l'ancienne table Content Machine : toujours les relire avec `get_table_schema` sur la table **Dossiers**.
- Si un champ ou un choix attendu est introuvable, ne pas deviner, ne rien créer : le signaler à Idris et s'arrêter.

## Écriture

- Le texte produit et le passage du statut à "À valider" s'écrivent **dans le même appel** `update_records_for_table`. Une ligne n'est ainsi jamais "À valider" sans texte, ni avec un texte mais toujours "À générer" (ce qui la ferait retraiter en boucle). Si l'écriture échoue, ne pas changer le statut et le signaler.
- Si le champ de texte contenait déjà quelque chose, il est remplacé : Idris a volontairement remis le dossier en "À générer".
- Au maximum 10 lignes par appel en création, 50 en mise à jour.
- Après écriture, relire une ou deux lignes (`list_records_for_table` avec recordIds) : texte non tronqué, retours à la ligne conservés, statut correct.
- Avant de créer une news, chercher (sur Sujet et Source URL) si elle existe déjà. Avant de créer un dossier, chercher parmi les dossiers récents (État différent de Clos et Ignoré) s'il en existe un sur le même sujet.
- Si un champ nécessaire n'existe pas, ne pas le créer de son propre chef et ne pas écrire de ligne à moitié remplie : le signaler et s'arrêter.
