# Travailler dans claude-hub

Ce repo contient le savoir-faire Claude d'Idris (IPJS Consulting). Il est installé comme marketplace de plugins dans Claude Code et packagé en `.plugin` pour Cowork. Lire `README.md` et `CONVENTIONS.md` avant toute modification de structure.

## Règles

- `partage/` est la source unique de ce qui est commun. Ne jamais modifier `plugins/*/references/partage/` : ce sont des copies. Après toute modification de `partage/`, lancer `outils/sync-partage.sh`.
- Un skill pointe vers les références, il ne les recopie pas.
- Un skill ne contient aucune donnée client ; un espace ne contient aucune méthode réutilisable.
- Les espaces livrés par un organisme (par exemple `espaces/intelligence-academy`) ne sont pas modifiés sans demande explicite d'Idris.
- Aucun secret dans git : les clés vivent dans `espaces/<x>/.claude/settings.local.json`, ignoré par `.gitignore`.
- Aucun tiret cadratin ni demi-cadratin dans les fichiers.

## Quand Idris demande d'ajouter un cas d'usage

1. Décider avec la table de `CONVENTIONS.md` : `partage/`, skill dans un plugin existant, nouveau plugin, ou nouvel espace. Annoncer le choix en une phrase avant d'écrire.
2. Partir des gabarits de `modeles/`.
3. Mettre à jour `.claude-plugin/marketplace.json` (nouveau plugin), `CATALOGUE.md`, et la `version` du plugin.
4. Lancer `outils/verifier.sh` et corriger jusqu'à ce qu'il affiche OK.
5. Proposer le commit ; ne pousser que si Idris le demande.

## Quand Idris corrige un résultat ("le post sonne IA", "trop long", "mauvais champ")

Trouver la référence ou le skill à l'origine du comportement et le corriger là, puis le dire en une phrase. Ne pas se contenter de corriger le texte produit.
