# Conventions : faire grandir claude-hub

Le repo doit pouvoir accueillir n'importe quel nouveau cas d'usage (prospection, formation pour un nouvel organisme, conseil, administratif) sans devenir un fourre-tout. Ce fichier dit où chaque chose va.

## La question à se poser

| Ce que j'ajoute | Où ça va | Exemple |
|---|---|---|
| Une règle vraie pour tout ce que je fais | `partage/` | "Toujours tutoyer les apprenants", nouvelle règle d'écriture |
| Une méthode réutilisable chez plusieurs clients | Un skill dans un plugin de domaine | Préparer une séance de coaching, qualifier un prospect |
| Ce qui est propre à un client ou organisme | `espaces/<client>/CLAUDE.md` | Charte DataBird, programme ILIA, kit TIA |
| Des données (apprenants, prospects, decks produits) | `espaces/<client>/` | Dossiers par apprenant |
| Un secret (clé d'API, token) | `espaces/<client>/.claude/settings.local.json` | Jamais ailleurs, jamais dans git |

Règle d'or : **un skill ne contient jamais de données client, un espace ne contient jamais de méthode réutilisable.** Le skill dit comment faire ; l'espace dit pour qui et avec quoi.

## Plugins = domaines d'activité

Un plugin regroupe les skills d'un même métier. Plugins actuels et prévus :

| Plugin | Domaine | Statut |
|---|---|---|
| `idris-contenu` | Veille, LinkedIn, Substack, futur podcast | Actif |
| `idris-formation` | Préparer, animer, débriefer des séances et formations, quel que soit l'organisme | À créer quand un 2e organisme en a besoin |
| `idris-prospection` | Cibler, qualifier, écrire aux prospects, suivre le pipe | À créer |
| `idris-conseil` | Audits, propositions commerciales, livrables de mission | À créer |

Créer un nouveau plugin plutôt que d'agrandir un plugin existant quand le domaine est différent : chaque plugin s'installe, se met à jour et peut se partager séparément (par exemple pour une formation).

## Nommage

- Plugins : `idris-<domaine>` en minuscules et tirets.
- Skills : `<verbe>-<objet>` en français, minuscules et tirets (`rediger-post-linkedin`, `preparer-seance`, `qualifier-prospect`). Dans Cowork et Claude Code, ils apparaissent sous la forme `idris-<domaine>:<skill>`.
- Espaces : `espaces/<organisme-ou-client>` en minuscules et tirets (`intelligence-academy`, `databird`).
- Références : un fichier par sujet, nom explicite (`content-machine.md`, `angle-attendu.md`).

## Ajouter un cas d'usage, pas à pas

1. **Nouveau domaine ?** Copier `modeles/plugin/` vers `plugins/idris-<domaine>/`, renseigner `plugin.json`, l'ajouter dans `.claude-plugin/marketplace.json`.
2. **Nouveau skill** : copier `modeles/plugin/skills/nom-du-skill/` dans le plugin, l'écrire. Ce qui est commun à plusieurs skills du plugin va dans `plugins/<plugin>/references/`. Ce qui est commun à plusieurs plugins va dans `partage/`.
3. **Nouveau client ou organisme** : copier `modeles/espace/` vers `espaces/<nom>/`, remplir son `CLAUDE.md` (contexte, contraintes, où sont les données, quels skills utiliser).
4. **Lancer `outils/verifier.sh`**, augmenter la version du plugin, mettre à jour `CATALOGUE.md`, commit, push.
5. **Installer** : `/plugin marketplace update claude-hub` dans Claude Code ; re-packager pour Cowork.

Le plus simple : ouvrir Claude Code à la racine du repo et lui dire "ajoute un cas d'usage : ..." ; le `CLAUDE.md` du repo lui donne cette procédure.

## Écrire un bon skill

- Le `description` du frontmatter décide quand le skill se déclenche : y mettre les mots qu'Idris emploie vraiment.
- Le skill commence par une section "Avant de commencer" qui liste les références à lire, en chemins relatifs au dossier du skill (`../../references/...`, `../../references/partage/...`).
- Il ne recopie jamais une référence : il pointe vers elle et ne garde que ce qui lui est propre.
- Il dit quoi faire quand une information manque (s'arrêter et signaler, plutôt que deviner).

## Versions

- Chaque modification d'un plugin augmente sa `version` dans `plugin.json` (1.0.0 vers 1.0.1 pour une correction, 1.1.0 pour un nouveau skill).
- Les espaces fournis par un organisme (comme Intelligence Academy) restent tels quels : on ne modifie pas ce qu'ils ont livré ; on ajoute à côté si besoin.
