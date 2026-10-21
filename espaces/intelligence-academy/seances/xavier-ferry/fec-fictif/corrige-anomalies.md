# FEC fictif : corrigé (pour Idris, ne pas montrer avant l'exercice)

Société entièrement fictive : **Ateliers Lumen**, menuiserie sur mesure, SIREN fictif 999000111, capital 100 000 €.
Deux exercices civils : 2024 (sain) et 2025 (dégradé, avec anomalies glissées volontairement).

| Fichier | Exercice | Lignes |
|---|---|---|
| `999000111FEC20241231.txt` | 2024 (à déposer en « Exercice N-1 ») | 906 |
| `999000111FEC20251231.txt` | 2025 (à déposer en « Exercice N ») | 932 |

Format : 18 colonnes réglementaires, tabulation, décimale virgule, UTF-8. Pas de liasse ni de relevés bancaires (facultatifs dans son appli).
Régénération : `python3 gen_fec.py <dossier>` (tirage aléatoire figé, mêmes fichiers à chaque fois).

## L'histoire que racontent les chiffres

| | 2024 | 2025 |
|---|---|---|
| Chiffre d'affaires HT | 1 983 k€ | 1 520 k€ (-23 %) |
| Taux d'achats de matières | 42 % | 47 % |
| EBITDA | positif | fortement négatif |
| Résultat net | +51 k€ | -218 k€ |
| Banque à la clôture | +111 k€ | -153 k€ (découvert) |
| Capitaux propres | 229 k€ | 11 k€ (< moitié du capital) |

En juin 2025, l'associé apporte 80 k€ en compte courant pour tenir la trésorerie.

## Les anomalies glissées en 2025, et ce que l'appli de Xavier en dit (testé le 19/10/2026)

| # | Anomalie | Où | Détectée ? |
|---|---|---|---|
| A1 | Écriture déséquilibrée de 150 € (débit 1 250, crédit 1 100) | OD du 30/09/2025, « Regularisation frais de deplacement » | Oui : « Total débit = total crédit : 150 » et « Écritures déséquilibrées : 1 » |
| A2 | Facture client de 48 000 € TTC jamais réglée | VT du 14/02/2025, FA2025-0900, Clinique du Parc (C006) | **En partie** : voir plus bas |
| A3 | Cotisations URSSAF de septembre, octobre et novembre non payées | Journal SA, aucun règlement BQ | Oui : « URSSAF 128 297, 4,0 mois de retard » |
| A4 | Grosse facture de 96 000 € TTC le 30/12 (coupure suspecte) | VT du 30/12/2025, FA2025-0901, Agence Mobilis | Oui : « ventes des 5 derniers jours : 5,3× la moyenne » |
| A5 | Facture fournisseur saisie deux fois (14 400 € TTC) | AC du 22/05/2025, F003-2291, Vernis et Finitions | Oui : « 1 écriture en double, impact résultat (12 000) » |
| (signal) | Capitaux propres inférieurs à la moitié du capital | conséquence de la perte | Oui : « 11 340 / 50 000 À voir » |

### A2, le point intéressant pour la séance

L'appli calcule l'ancienneté des créances en imputant le solde de chaque client sur ses factures **les plus récentes** (méthode FIFO, indépendante du lettrage). La Clinique du Parc continue à payer ses factures récentes. Les 48 000 € bloqués depuis février sont donc répartis sur des factures plus récentes. Résultat affiché : « échu > 90 j : 48 000 / > 180 j : 25 113 ».

Il aurait fallu lire 48 000 € échus depuis plus de 180 jours (320 jours au 31/12). Le lettrage du FEC le montre pourtant : cette facture est la seule de 2025 non lettrée chez ce client avant octobre.
Question à poser à Xavier : faut-il croiser l'ancienneté FIFO avec le lettrage quand le lettrage est fiable (ici 72 % du facturé lettré) ?

## Ce que je n'ai pas pu vérifier

- **Les erreurs de calcul dans l'Excel** : je n'ai pas Excel ici, donc les formules n'ont pas été recalculées. Contrôle statique des deux classeurs (`sorties-appli-xavier/`) : 21 et 9 onglets, environ 11 000 formules, aucune référence vers un onglet inexistant.
- **Pistes à tester en ouvrant les classeurs dans Excel** :
  - `MINIFS` (48 formules dans le classeur Trésorerie) n'existe qu'à partir d'Excel 2019 ou 365. Sur une version plus ancienne, on obtient `#NOM?`.
  - Le classeur « relevés » utilise `TEXT(...;"yyyy-mm")`. Un Excel en français attend « aaaa » pour l'année, d'où un risque de texte faux. Je ne l'ai pas généré, faute de relevés bancaires.
