# Séance 1 · Xavier FERRY · Textes à coller

À envoyer dans le chat de la visio au moment de chaque exercice.

---

## Pratique 1 · Votre n8n en 15 minutes

1. Créez votre compte d'essai : https://n8n.io (bouton « Get started », sans carte bancaire, 14 jours, 1 000 exécutions).
2. Nouveau workflow : un déclencheur manuel (« Trigger manually »), puis un nœud **Edit Fields**.
3. Dans Edit Fields, ajoutez deux champs :
   - `societe` = `Ateliers Lumen`
   - `exercice` = `2025`
4. Exécutez, puis téléchargez le workflow : menu « … » en haut à droite › **Download**.
5. Envoyez-moi le fichier JSON dans le chat : je l'importe sur mon n8n.

---

## Pratique 2 · Tester votre outil

**Fichiers joints** (FEC fictifs, société inventée) :
- `999000111FEC20241231.txt` : à déposer dans « Exercice N-1 »
- `999000111FEC20251231.txt` : à déposer dans « Exercice N (dernier clos) »

**Dans Claude pour Excel**, sur une copie du classeur, sélectionnez la cellule en erreur puis :

```
Trouve pourquoi cette cellule renvoie une erreur et remonte jusqu'à la cause.
Explique la formule pas à pas, en citant les cellules utilisées.
Ne modifie rien : je veux d'abord comprendre.
```

**Votre grille d'écarts** (une ligne par écart) :

| Écart constaté | Type d'erreur | Onglet | Correction à faire dans le code |
|---|---|---|---|
| | | | |

Types d'erreur : calcul faux · fonction absente de votre Excel · format régional · donnée mal lue · hypothèse de calcul.

---

## Corriger l'outil avec Claude

Dans une nouvelle conversation. Joignez votre outil (le fichier HTML) et décrivez un écart à la fois.

```
Voici mon outil d'analyse FEC (fichier HTML joint) et un écart constaté sur un dossier test.

Dossier test : [nom du fichier FEC]
Onglet et cellule : [où l'écart apparaît]
Valeur attendue : [ce que le dossier contient vraiment]
Valeur obtenue : [ce que l'outil affiche]

1. Trouve la cause dans le code et explique-la en deux phrases.
2. Propose le correctif minimal : ne réécris rien d'autre, ne change ni la structure ni les noms.
3. Propose un contrôle à ajouter à l'onglet Controles qui aurait détecté cet écart.

Si la cause est une hypothèse de calcul et non un bug, dis-le et décris les options, sans trancher à ma place.
```

Après chaque correction : relancez l'outil sur les mêmes FEC et vérifiez que rien d'autre n'a bougé.

---

## Pratique 3 · Cartographier votre rapport

Dans une nouvelle conversation. Joignez le plan de votre rapport type (anonymisé).

```
Voici le plan d'un rapport que je rédige lors d'un diagnostic financier d'entreprise.

Pour chaque section, remplis un tableau avec ces colonnes :
- Section
- Données nécessaires et leur source (FEC, liasse, relevés, entretiens, documents juridiques…)
- Niveau d'automatisation : « automatique » (calcul et mise en forme), « préparé par Claude » (premier jet à partir de chiffres fournis), ou « humain » (jugement, entretiens, recommandations)
- Ce qui rend l'automatisation risquée, s'il y a un risque

Ne déduis rien que le plan ne dit pas : si une section est ambiguë, pose-moi la question.
```

---

## Devoir 2 · Interroger l'API du BODACC dans n8n

API publique, sans clé. Le but : pratiquer le nœud HTTP Request et préparer la séance 3.

1. Nouveau workflow : déclencheur manuel, puis un nœud **HTTP Request**.
2. Méthode : `GET`. URL (procédures collectives publiées à Paris, les 20 plus récentes) :

```
https://bodacc-datadila.opendatasoft.com/api/explore/v2.1/catalog/datasets/annonces-commerciales/records?where=familleavis%3D%22collective%22%20AND%20numerodepartement%3D%2275%22&order_by=dateparution%20desc&limit=20
```

3. Exécutez : la réponse contient une liste `results`. Ajoutez un nœud **Split Out** sur le champ `results` pour obtenir une annonce par item.
4. Ajoutez un **Edit Fields** avec ces champs :
   - `date` = `{{ $json.dateparution }}`
   - `societe` = `{{ $json.commercant }}`
   - `ville` = `{{ $json.ville }}`
   - `jugement` = `{{ JSON.parse($json.jugement).nature }}`
5. Changez de département : remplacez `75` dans l'URL par le vôtre.

Bonus : n'afficher que les jugements d'ouverture de redressement judiciaire (nœud **Filter** sur `jugement`).
