---
name: apprendre-de-mes-corrections
description: "Compare les textes écrits par Claude (Post LinkedIn, Note et Article Substack) aux versions qu'Idris a réellement publiées dans Content Machine, en tire des Leçons de style concrètes à valider, et repère les leçons qui devraient remonter dans le guide de voix. À lancer chaque semaine (tâche planifiée) ou quand Idris dit \"apprends de mes corrections\", \"regarde ce que j'ai changé\", \"pourquoi je réécris toujours les posts\"."
---

# Apprendre des corrections d'Idris

## Pourquoi ce skill existe

Idris passe trop de temps à relire et réécrire ce que Claude produit. Chaque correction qu'il fait dit exactement ce qu'il attend : ce qu'il coupe, ce qu'il ajoute, ce qu'il reformule. Jusqu'ici ces corrections restaient sur LinkedIn ou Substack et Claude refaisait les mêmes écarts la fois suivante.

Ce skill ferme la boucle. Il compare la version de Claude et la version publiée, en tire des **leçons** courtes et vérifiables, et les propose à Idris dans la table **Leçons de style**. Une fois validées, elles s'appliquent automatiquement à chaque rédaction (`style-vivant.md`).

Critère de réussite : au fil des semaines, l'écart entre la version de Claude et la version publiée diminue, et Idris valide des leçons qui le font penser "oui, c'est exactement ça que je corrige".

## Langue

Ce skill est en français. Les leçons peuvent être écrites en français (Idris les lit), mais les extraits avant/après restent dans leur langue d'origine (anglais). Résumé final en français.

## Avant de commencer

Lire ces références (chemins relatifs au dossier de ce skill) :

- `../../references/content-machine.md` : tables Dossiers et Leçons de style, dossiers historiques.
- `../../references/style-vivant.md` : comment les leçons sont utilisées par les skills de rédaction.
- `../../references/partage/voix-idris.md` et `../../references/partage/regles-ecriture.md` : ce qui est déjà écrit, pour ne pas proposer une leçon qui existe déjà.

## Workflow

### 1. Trouver les dossiers à analyser

Table Dossiers : dossiers dont **Appris** n'est pas coché et dont au moins un champ **Version publiée** (LinkedIn, Note, Article) est rempli.

Pour chaque dossier, la **version Claude** est dans Post LinkedIn, Note Substack, Article Substack du dossier. Pour les trois dossiers historiques (voir `content-machine.md`), elle est dans les mêmes champs de la news liée.

S'il n'y a rien à analyser, le dire en une phrase et s'arrêter. Si des dossiers sont "Publié" sans Version publiée, les lister dans le résumé pour rappeler à Idris de coller ses textes (page "Publiés : coller la version finale" de l'interface).

### 2. Comparer, texte par texte

Pour chaque paire (version Claude, version publiée) :

1. Si les deux textes sont identiques ou presque (corrections de quelques mots), le noter : c'est un succès, et ça compte aussi.
2. Sinon, relever les écarts **significatifs**, en les classant :
   - **Accroche** : Idris a changé la première ligne. Comment (plus court, plus personnel, un chiffre, une question) ?
   - **Structure** : ordre des idées changé, paragraphes déplacés, fin réécrite.
   - **Coupes** : ce qu'il a supprimé (paragraphes entiers, précautions, explications, conseils, formules). Mesurer : longueur avant et après.
   - **Ajouts** : ce qu'il a ajouté (anecdote, avis, humour, précision, appel à l'action).
   - **Ton** : mots ou tournures remplacés. Relever les paires concrètes ("X" devient "Y").
   - **Fond** : avis de Claude qu'il a retiré ou corrigé, position adoucie ou durcie.
   - **Format** : emojis, hashtags, mise en forme, liens.
3. Ne relever que ce qu'on voit dans les textes. Ne pas deviner une intention qu'aucun écart ne montre.

### 3. Transformer les écarts en leçons

Une leçon est une **consigne positive, concrète et vérifiable**, qu'un skill de rédaction peut appliquer telle quelle :

- Bien : "Open LinkedIn posts with the concrete fact or number, not with a statement about the industry."
- Bien : "Cut the closing advice paragraph: end on the tension or the question."
- Trop vague : "Be more natural." "Sound more like Idris."

Pour chaque écart significatif :

1. Chercher dans la table Leçons de style une leçon existante qui couvre déjà cet écart (quel que soit son statut).
   - Elle existe et est **Proposée** ou **Validée** : ajouter 1 à **Occurrences**, ajouter le dossier dans **Dossiers source**, compléter **Avant / après** si l'exemple est plus parlant. Ne pas créer de doublon.
   - Elle existe et est **Rejetée** : ne rien faire (Idris a déjà tranché), sauf si l'écart revient au moins 3 fois ; alors la mentionner dans le résumé, sans changer son statut.
   - Elle n'existe pas : créer une leçon **Proposée** avec Leçon, Canal, Type, Avant / après (extraits courts, 1 à 3 phrases de chaque côté), Occurrences = 1, Dossiers source.
2. Un écart vu une seule fois peut être un choix du jour. Le proposer quand même s'il est net, mais le résumé dit qu'il n'a été vu qu'une fois.
3. Au maximum 5 nouvelles leçons par exécution, les plus nettes et les plus fréquentes d'abord. Idris doit pouvoir les valider en 2 minutes.

### 4. Repérer ce qui doit remonter dans le guide de voix

Une leçon **Validée** avec **Occurrences** de 3 ou plus est une règle stable. La lister dans le résumé comme candidate à intégrer dans `partage/voix-idris.md` ou dans le skill du canal (repo claude-hub), pour qu'Idris décide de la faire remonter. Ne pas modifier le repo depuis ce skill.

### 5. Marquer et conclure

1. Cocher **Appris** sur chaque dossier analysé. Ce skill n'écrit aucun autre champ de la table Dossiers.
2. Résumé en français, court :
   - Nombre de textes comparés, et combien Idris a publiés quasiment tels quels.
   - Les nouvelles leçons proposées (une ligne chacune), et celles dont les occurrences ont augmenté.
   - Les leçons candidates à remonter dans le guide de voix.
   - Les dossiers publiés sans Version publiée.
   - Rappel : les leçons se valident dans la page "Leçons de style à valider" de l'interface.

## Cas limites

- **Version publiée beaucoup plus longue ou sur un autre sujet** : Idris a réécrit de zéro. Ne pas en tirer de leçons de détail ; noter seulement ce qui ressort (structure, longueur) et le signaler.
- **Texte de Claude absent** (dossier rédigé à la main) : rien à comparer. La version publiée sert quand même d'exemple de style (`style-vivant.md`). Cocher Appris.
- **Écart dû à un fait corrigé** (chiffre faux, date) : ce n'est pas une leçon de style. Le signaler dans le résumé comme problème de fiabilité.
- Ne jamais modifier une leçon Validée ou Rejetée autrement que par Occurrences, Dossiers source et Avant / après.
