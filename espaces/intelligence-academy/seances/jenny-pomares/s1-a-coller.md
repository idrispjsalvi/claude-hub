# Séance 1 · Jenny POMARÈS · Textes à coller

À envoyer dans le chat de la visio au moment de chaque exercice.

---

## Pratique 1 · L'interview pour tes instructions

Dans une nouvelle conversation, hors de tout projet.

```
Je veux rédiger mes Instructions pour Claude : le texte que tu liras dans toutes mes conversations.

Pose-moi tes questions une par une, en attendant ma réponse avant la suivante : qui je suis et mon rôle, mon entreprise et son métier, mes clients, ma façon d'écrire (ton, tutoiement ou vouvoiement, signature), et les règles que tu dois toujours respecter.

Ensuite, propose un texte de 10 à 15 lignes maximum, avec seulement ce qui vaut pour TOUTES mes conversations.

Ajoute ces deux règles :
- Ne jamais inventer un chiffre, un prix, une référence ou un nom.
- Signaler clairement ce que tu déduis ou supposes.
```

## Pratique 1 · Le test

Nouvelle conversation, sans rien expliquer :

```
Présente-moi en deux lignes.
```

---

## Pratique 2 · L'interview pour les instructions du projet

Dans le projet « Contrôle factures fournisseurs », nouvelle conversation, grille déjà ajoutée aux fichiers du projet.

```
Je veux rédiger les instructions de ce projet : « Contrôle factures fournisseurs ». Tu les liras dans toutes les conversations du projet, où je joindrai chaque mois une facture fournisseur à comparer à la grille de prix négociée qui est dans les fichiers du projet.

Pose-moi tes questions une par une, en attendant ma réponse avant la suivante : qui fait ce contrôle aujourd'hui et comment, ce que contient la grille, ce qu'il faut comparer (prix, quantités, autre chose), ce qu'on considère comme un écart, le format du résultat que je veux, et ce que j'en fais ensuite.

Ensuite, propose des instructions courtes, avec seulement ce qui vaut pour ce projet (pas ce qui est déjà dans mes Instructions pour Claude).

Ces trois règles doivent y figurer :
- Un article absent de la grille : écrire « hors grille », sans inventer de prix.
- Toujours citer la ligne de la grille utilisée.
- Ne rien inventer ; signaler une ligne illisible.
```

Une fois le texte validé : le coller dans les instructions du projet, puis ouvrir une NOUVELLE conversation dans le projet pour joindre la facture.

## Pratique 2 · Consigne de secours

Si l'interview prend trop de temps, ou pour comparer avec ce qu'elle a obtenu.

```
Tu contrôles les factures fournisseurs de Pomarès TP.

Pour chaque ligne de la facture jointe, retrouve l'article dans la grille de prix du projet, puis compare la quantité et le prix unitaire.

Rends un tableau avec ces colonnes : article, quantité, prix facturé, prix grille, écart unitaire, écart total.
Sous le tableau, donne le total des écarts à réclamer au fournisseur.

Règles :
- Un article absent de la grille : écris « hors grille », sans inventer de prix.
- Cite toujours la ligne de la grille que tu as utilisée.
- N'invente rien. Si une ligne de la facture est illisible, dis-le.
```

## Pratique 2 · Données fictives (si elle n'a pas les siennes)

Situation inventée pour l'exercice : fournisseur, chantier et prix fictifs. Colonnes séparées par des tabulations : copier le bloc et le coller en A1 d'un Google Sheet, chaque valeur tombe dans sa cellule. Mêmes données dans `donnees-fictives/` (fichiers .tsv).

Pour le projet : depuis le Google Sheet, Fichier › Télécharger › CSV (ou PDF), puis ajouter le fichier aux fichiers du projet. La facture se joint dans la conversation de la même façon.

**Onglet « Grille »** : Matériaux du Littoral, chantier « Réseau EU, rue des Oliviers », valable du 01/09 au 30/11/2026

```
Ligne	Article	Unité	Prix HT (€)
G1	Tube PVC CR8 Ø200	ml	13,20
G2	Tube PVC CR8 Ø160	ml	9,10
G3	Regard béton 1000x1000	u	312,00
G4	Tampon fonte D400	u	168,00
G5	Grave 0/31,5	t	21,80
G6	Sable 0/4	t	19,50
G7	Grillage avertisseur marron (rouleau)	u	38,00
```

**Onglet « Facture F-2026-1047 »** : Matériaux du Littoral, facture du 31/10/2026

```
Article	Qté	Unité	PU HT (€)	Total HT (€)
Tube PVC CR8 Ø200	120	ml	14,90	1788,00
Tube PVC CR8 Ø160	60	ml	9,10	546,00
Regard béton 1000x1000	4	u	312,00	1248,00
Tampon fonte D400	4	u	168,00	672,00
Grave 0/31,5	85	t	24,50	2082,50
Sable 0/4	30	t	19,50	585,00
Manchon de raccordement Ø200	6	u	8,40	50,40
			Total HT	6971,90
```

Écarts cachés, pour vérifier le tableau de Claude :
- Tube Ø200 : 14,90 € au lieu de 13,20 €, soit 1,70 € x 120 = 204,00 €.
- Grave 0/31,5 : 24,50 € au lieu de 21,80 €, soit 2,70 € x 85 = 229,50 €.
- Manchon : hors grille, aucun prix à comparer.
- Total à réclamer : 433,50 € HT.

---

## Pratique 3 · Le prompt de création du skill

Dans une nouvelle conversation. Joindre un mail commercial déjà envoyé s'il y en a un.

```
Je veux créer un skill : « mail commercial Pomarès TP ».

Il rédige un mail commercial à un client actuel, à un ancien client ou à un prospect, pour proposer nos services de travaux publics.

Pose-moi tes questions une par une, en attendant ma réponse avant la suivante : les cibles, les métiers et chantiers à mettre en avant, le ton, la longueur, l'appel à l'action, les pièges à éviter.

Règles à inscrire dans le skill :
- Seulement des chantiers, des références et des chiffres réels, que je t'ai donnés.
- Signale par [À vérifier] tout ce que tu supposes.
- Une seule demande claire à la fin du mail.
- Tu rédiges un brouillon : tu n'envoies jamais rien.
```

## Pratique 3 · Le test

```
Un mail pour proposer nos services à <client>.
```

---

## Pratique 4 · Avec le connecteur messagerie

```
Retrouve nos derniers échanges avec <client>, et résume-les en trois lignes.
```

```
Avec mon skill « mail commercial Pomarès TP », prépare-lui un mail commercial qui s'appuie sur ces échanges.
```

## Pratique 4 · Client fictif (si le connecteur ne passe pas)

Situation inventée pour l'exercice. À coller dans la conversation à la place des échanges réels.

```
Client : mairie de Saint-Exemple (83), service technique.
Dernier chantier avec nous : reprise du réseau d'eaux pluviales, avenue des Pins, livré en juin 2026.
Dernier échange (septembre 2026) : le responsable technique a parlé d'un programme de réfection de trottoirs et de branchements d'assainissement en 2027.
```
