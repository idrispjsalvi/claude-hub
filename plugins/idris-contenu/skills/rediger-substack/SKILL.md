---
name: rediger-substack
description: "Rédige en anglais la Note et l'Article Substack d'Idris (son avis, son ton) depuis les lignes Content Machine dont le Statut Substack est \"À générer\", en suivant l'Angle attendu, puis passe à \"À valider\". À utiliser dès qu'Idris parle de Substack, de Note Substack, d'Article Substack, de générer le contenu Substack, ou qu'une ligne a son Statut Substack à \"À générer\" (ou \"À généré\"), même s'il ne cite pas le skill."
---

# Rédaction des Notes et Articles Substack d'Idris

## Pourquoi ce skill existe

Idris publie sur Substack en anglais, avec son ton personnel, direct et positif sur l'IA. Sa veille alimente la base Airtable **Content Machine** (une ligne par news). Il lit la veille, choisit les sujets qui l'intéressent, écrit lui-même l'**Angle attendu** (sa thèse, ce qu'il veut dire), puis passe le **Statut Substack** à "À générer". Ce skill prend le relais : pour chaque ligne, il produit deux contenus complémentaires, une **Note** (format court du fil Substack) et un **Article** (format long envoyé par email aux abonnés), qu'Idris n'aura presque plus qu'à relire et publier.

Le critère de réussite est simple : Idris lit le texte et pense "c'est moi qui l'ai écrit", pas "c'est une IA qui imite un blog". Et il doit pouvoir copier-coller le contenu dans Substack sans retoucher quoi que ce soit.

## Langue

Ce skill est en français. **La Note et l'Article sont toujours écrits en anglais**, quelle que soit la langue de l'Angle attendu (souvent en français) ou de la source. Le résumé de fin de tâche dans le chat se fait en français.

## Avant de commencer

Lire ces références (chemins relatifs au dossier de ce skill). Elles font partie du skill au même titre que ce fichier :

- `../../references/angle-attendu.md` : Principe n°1 (c'est Idris qui parle ; dans un article long, l'envie d'étoffer avec des opinions maison est le piège principal), comment lire l'Angle attendu comme un brief, cas particuliers.
- `../../references/partage/voix-idris.md` : la voix d'Idris. Exigence n°1 : parler à une personne, y compris dans l'Article.
- `../../references/partage/regles-ecriture.md` : fiabilité, règles de recherche, typographie (aucun tiret cadratin), checklist anti-IA.
- `../../references/content-machine.md` : identifiants de la base, champs, statuts et pièges, règles d'écriture.

Ce skill ne contient que ce qui est propre à Substack.

## Workflow

### 1. Trouver les lignes à traiter

1. Appeler `get_table_schema` sur la table Content Machine pour retrouver, à partir de leurs noms, les identifiants des champs **Statut Substack**, **Note Substack**, **Article Substack** et l'identifiant du choix "À générer" de **Statut Substack**. Filtrer avec l'identifiant du champ **Statut Substack**, jamais celui de Statut LinkedIn (mêmes choix, voir `content-machine.md`).
2. Lister les lignes dont le **Statut Substack** est "À générer" avec `list_records_for_table`, en demandant : Sujet, Résumé IA, Analyse IA, Source, Source URL, Date de la source, Angle attendu, Note Substack, Article Substack, Statut Substack.
3. S'il n'y a aucune ligne "À générer", le dire simplement et s'arrêter. Si l'utilisateur a nommé une ligne précise (par son Sujet), ne traiter que celle-là, après avoir vérifié son statut.

### 2. Lire l'angle, rassembler la matière, creuser

Lire la ligne comme décrit dans `angle-attendu.md`.

**Recherche complémentaire** (règles dans `regles-ecriture.md`). Un article de 900 à 1 400 mots ne peut pas reposer sur trois lignes de résumé : il faut de la matière.

1. **Toujours pour l'Article** : ouvrir la Source URL et, quand elle existe, la source primaire (communiqué, étude, texte officiel, page de tarifs). Chercher le contexte qui donne du corps au texte (ce qui s'est passé avant, ce que disent les concurrents ou les critiques, un chiffre de comparaison). Recouper les chiffres importants.
2. **Quand l'angle la demande**, même en une demi-phrase : c'est une vraie mission, avec plusieurs recherches croisées.

Les sources réellement consultées alimentent la section "Sources" de l'Article et le résumé du chat. Ne jamais inventer une URL.

### 3. Rédiger la Note, puis l'Article

Suivre la voix d'Idris et les sections "La Note" et "L'Article" ci-dessous, puis passer la checklist anti-IA (`regles-ecriture.md`) et les points Substack plus bas. Une seule version de chaque (pas de variantes).

Rédiger la Note et l'Article comme deux pièces qui se complètent, pas comme un résumé et sa version longue : la Note frappe avec une idée, l'Article la démontre. Ne pas recopier des phrases de l'un dans l'autre.

### 4. Écrire dans Airtable

Un seul appel `update_records_for_table` par ligne qui écrit **en même temps** :

- **Note Substack** : le texte de la Note, tel quel.
- **Article Substack** : l'Article complet, tel quel.
- **Statut Substack** : "À valider" (nom du choix en chaîne simple).

Ne toucher à aucun autre champ. Règles d'écriture et de vérification : `content-machine.md`.

### 5. Vérifier

Relire une ou deux lignes écrites : les deux textes non tronqués (surtout l'Article, long), retours à la ligne conservés, Statut Substack à "À valider".

### 6. Résumé dans le chat (en français, court)

- Nombre de lignes traitées et leurs Sujets.
- Pour chaque ligne, une phrase sur l'angle retenu si utile.
- Ce que la recherche a trouvé de déterminant, les sources consultées (nom et URL), et surtout ce qu'elle n'a pas pu confirmer ou ce qui contredit l'angle.
- Les consignes de l'angle non respectées, et pourquoi.
- Les points d'attention : angle vide, affirmation prudente à cause d'une info non confirmée, lignes non traitées et pourquoi.

Ne pas recopier les textes dans le chat sauf demande : ils sont déjà dans Airtable.

## La Note

Une Note Substack est un message court dans le fil, lu en scrollant, comme un tweet un peu plus posé. Elle doit tenir debout toute seule et donner envie de réagir.

- **Contenu** : une seule idée, la plus tranchante de l'angle. Accroche dès la première ligne (un fait frappant, un chiffre, une tension), puis la lecture d'Idris en quelques lignes courtes.
- **Longueur** : 300 à 800 caractères, jamais plus de 1 200. Pas de gonflage : une Note plus courte qui dit une chose nette vaut mieux.
- **Forme** : texte brut, lignes courtes, une ligne vide entre les blocs. Pas de markdown (Substack n'affiche pas le gras ni les titres dans une Note), pas de hashtags, pas de titre. Flèche "→" en début de ligne si une mini-liste est vraiment utile.
- **Emojis** : 0 à 2, en fin de phrase, jamais en guise de puces. Le fil Substack est un peu plus sobre que LinkedIn.
- **Clôture** : une phrase qui donne quelque chose, ou une question précise au lecteur. Pas de "What do you think?" seul.
- **Pas de renvoi à l'Article** ("link in the comments", "read the full piece"), sauf si l'angle le demande : rien ne garantit la date de publication de l'Article, et la Note doit fonctionner seule.
- **Liens** : pas d'URL dans la Note. Citer la source par son nom quand ça renforce le propos.

## L'Article

Un article Substack arrive dans la boîte mail des abonnés d'Idris et reste dans son archive. Il doit se lire d'un trait, avoir une colonne vertébrale (l'angle) et apporter de la substance que la Note n'a pas : contexte, chiffres, comparaison, raisonnement.

### Format du champ

Markdown prêt à coller dans l'éditeur Substack, avec cette structure exacte :

```
Title: <titre de l'article>
Subtitle: <sous-titre>

<corps de l'article en markdown>
```

- **Title** : 6 à 12 mots, concret, qui donne le sujet ou la tension (pas de titre clickbait, pas de "Everything you need to know about"). Le titre reprend la position d'Idris quand c'est possible.
- **Subtitle** : une phrase, qui complète le titre sans le répéter.
- **Corps** : commence directement par l'accroche, sans "Introduction", sans répéter le titre.

### Longueur

900 à 1 400 mots pour le corps, sauf consigne de l'angle (cible : environ 1 100 mots). Le plancher de 900 mots compte : un article trop court ressemble à un long post, pas à un article de newsletter. Si le premier jet est en dessous, ne pas délayer : aller chercher plus de matière (une recherche de plus sur le contexte, un précédent, un chiffre de comparaison, l'objection la plus sérieuse à l'angle) ou développer le raisonnement qui mène de l'angle à sa conséquence. Ne jamais compléter avec du remplissage, des généralités ou des avis maison.

Dans le corps, rester factuel sur ce qu'a fait la recherche : écrire "according to X" ou "no independent replication has been published" plutôt que d'attribuer à Idris des vérifications qu'il n'a pas faites lui-même.

### Structure

Sans gabarit rigide, mais le fil est toujours celui-ci :

1. **Accroche** (2 à 4 phrases) : un fait frappant, un chiffre, une tension, une scène. Elle donne envie de lire la suite, sans "In this article".
2. **Les faits** : ce qui s'est passé, avec chiffres, noms, dates, sources attribuées dans le texte. Assez pour qu'un lecteur qui n'a pas vu la news comprenne tout.
3. **La lecture d'Idris** : c'est l'angle, développé. Pourquoi ça compte, ce que ça révèle, qui y gagne quoi. Idris raisonne : il pose un fait, en tire une conséquence, teste l'objection la plus sérieuse (s'appuyer sur le contre-argument trouvé pendant la recherche), puis réaffirme sa position.
4. **Ce que ça change pour le lecteur** : une conséquence pratique, seulement si elle découle de l'angle ou des faits (voir Principe n°1, pas de conseil maison).
5. **Clôture** : une phrase qui donne quelque chose (une ouverture, un message), ou une question précise aux lecteurs. Pas de récapitulatif, pas de "In conclusion".
6. **Sources** : section finale `## Sources`, une puce par source réellement consultée : `- [Nom de la source](URL)`. Uniquement des URL réellement ouvertes pendant la recherche.

### Markdown autorisé

- Sous-titres de section en `##` (2 à 4 dans l'article), courts et concrets, pas de sous-titres génériques ("Background", "Analysis", "Conclusion"). Pas de `#` (le titre est déjà en tête) et pas de `###` sauf besoin réel.
- Gras `**...**` avec parcimonie (quelques mots-clés ou un chiffre clé, pas des phrases entières).
- Listes à puces `-` ou `→` seulement pour de vraies énumérations (3 à 6 items). Le corps reste majoritairement en prose.
- Liens `[texte](URL)` dans le corps quand ils renvoient à la source primaire (contrairement à LinkedIn, un lien dans un article est bienvenu). Pas de lien vers autre chose que des sources consultées.
- Citations en `>` seulement pour une vraie citation trouvée dans une source, courte, attribuée.
- Séparateur `---` avant la section Sources si utile.
- Emojis : 0 à 2 dans tout l'article.
- Pas de hashtags, pas de tableau, pas de HTML.

### Questions au lecteur

Une ou deux dans la Note, deux ou trois dans tout l'Article, jamais en rafale.

## Format des textes stockés dans les champs

- **Note Substack** : texte brut, sans aucun markdown.
- **Article Substack** : markdown comme décrit ci-dessus, uniquement le contenu à publier, en commençant par la ligne `Title:`.
- Aucun tiret long, nulle part, y compris dans les titres et les sources (voir `regles-ecriture.md`).
- Une ligne vide entre les paragraphes, retours à la ligne réels.
- Les deux textes en anglais.

## Points anti-IA propres à Substack

En plus de la checklist commune :

- "In this article", "Introduction", "In conclusion", récapitulatif final.
- Trop de sous-titres, ou des sous-titres génériques ("Background", "Analysis").
- Paragraphes tous de la même taille, chaque section qui finit sur une punchline.
- **Répétition entre Note et Article** : les mêmes phrases dans les deux.

## Exemple de manière (Note)

Cet exemple montre le rythme et le dosage, pas un contenu à réutiliser. Il s'inspire d'un vrai post d'Idris.

```
Yesterday, one researcher resigned saying the teams building AI "earnestly believe it could kill us all by the end of the decade."

A few desks away, another heavyweight puts that same risk at under 0.01%.

Nobody agrees with each other, yet only one story ever takes off: the scariest one. Thanks, media 😉

If you follow AI news, ask yourself who benefits from the version you're reading.
```

## Cas limites propres à Substack

- **Plusieurs lignes "À générer"** : ne pas répéter la même accroche ni la même structure d'un article à l'autre.
- **Post LinkedIn déjà généré sur la même ligne** : ne pas le lire pour le recopier ni le modifier. La Note et l'Article ont leur propre texte, plus posé que le post.
- Les autres cas (angle vide, angle très court, angle qui contredit les faits, deux lignes sur le même sujet) sont décrits dans `angle-attendu.md` ; sujets sensibles et droit d'auteur dans `regles-ecriture.md`.
