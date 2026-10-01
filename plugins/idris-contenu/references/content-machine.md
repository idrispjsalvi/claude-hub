# Base Airtable Content Machine

Référence unique de la base pour tous les skills du plugin `idris-contenu`. Si la base change (champ renommé, nouveau statut), on modifie ce fichier et rien d'autre.

## Identifiants

- Base **Content Machine** : `app7aTWK9J6nO1Kcm`
- Table **Content Machine** : `tblvEaTY3FtMohjhL` (une ligne par sujet)
- Table **Sources** : `tbl0F38Ff1NPc6b7o` (sources suivies par la veille ; lecture seule sauf demande d'Idris)

Ne jamais coder en dur les identifiants de **champs** ni de **choix** : les retrouver à partir de leur nom avec `get_table_schema` (ou `list_tables_for_base`) au début de chaque exécution. Ils peuvent changer.

## Champs et qui les remplit

| Champ | Rempli par | Contenu |
|---|---|---|
| Sujet | veille-ia, creer-ligne-content-machine | Titre informatif, une ligne |
| Résumé IA | veille-ia, creer-ligne-content-machine | 3 à 5 phrases factuelles, en anglais |
| Analyse IA | veille-ia, creer-ligne-content-machine | Commence par "Reliability: ...", finit par "Key takeaway: ..." |
| Source | veille-ia, creer-ligne-content-machine | Nom de la source principale |
| Source URL | veille-ia, creer-ligne-content-machine | URL réellement consultée, jamais reconstruite |
| Date de la source | veille-ia, creer-ligne-content-machine | Date, format AAAA-MM-JJ |
| Angle attendu | Idris (à la main) ; creer-ligne-content-machine seulement à partir de ce qu'Idris a dit | Le brief d'Idris, voir `angle-attendu.md` |
| Statut LinkedIn | Idris ; rediger-post-linkedin ; creer-ligne-content-machine sur demande | Choix, voir plus bas |
| Post LinkedIn | rediger-post-linkedin | Texte brut prêt à coller |
| Statut Substack | Idris ; rediger-substack | Choix, voir plus bas |
| Note Substack | rediger-substack | Texte brut prêt à coller |
| Article Substack | rediger-substack | Markdown, commence par `Title:` puis `Subtitle:` |
| Image Post LinkedIn, dates de publication, Lien du post | Idris | Aucun skill n'y touche |

Règle générale : un skill ne touche **que** les champs qui lui sont attribués dans ce tableau.

## Statuts

**Statut LinkedIn** et **Statut Substack** ont exactement les mêmes choix (mêmes noms, parfois mêmes identifiants de choix) :

- vide : rien de demandé
- "À générer" : Idris demande une rédaction (il écrit parfois "À généré" par erreur : c'est bien "À générer")
- "À valider" : texte écrit par Claude, en attente de relecture

Pièges :

- Ne jamais confondre les deux champs : filtrer avec l'identifiant du champ du canal concerné, jamais celui de l'autre.
- Le champ **Statut LinkedIn** s'appelait "Statut" avant le 25/09/2026. Si un champ attendu est introuvable (renommé encore), ne pas deviner en prenant un autre champ aux mêmes choix : le signaler à Idris et s'arrêter.
- Si le choix "À générer" ou "À valider" n'existe pas, ne rien créer et ne rien écrire : le signaler et s'arrêter.

## Écriture

- Le texte produit et le passage du statut à "À valider" s'écrivent **dans le même appel** `update_records_for_table`. Une ligne n'est ainsi jamais "À valider" sans texte, ni avec un texte mais toujours "À générer" (ce qui la ferait retraiter en boucle). Si l'écriture échoue, ne pas changer le statut et le signaler.
- Si le champ de texte contenait déjà quelque chose, il est remplacé : Idris a volontairement remis la ligne en "À générer".
- Au maximum 10 lignes par appel en création, 50 en mise à jour.
- Après écriture, relire une ou deux lignes (`list_records_for_table` avec recordIds) : texte non tronqué, retours à la ligne conservés, statut correct.
- Avant de créer une ligne, chercher (sur Sujet et Source URL) si le sujet existe déjà, pour ne pas créer de doublon.
- Si un champ nécessaire n'existe pas, ne pas le créer de son propre chef et ne pas écrire de ligne à moitié remplie : le signaler et s'arrêter.
