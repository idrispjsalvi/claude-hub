# claude-hub

Le savoir-faire Claude d'IPJS Consulting, au même endroit pour Cowork et Claude Code.

Un principe : **ce que Claude sait faire** (skills, voix, règles) vit ici, une seule fois. **Où Claude le fait** (Cowork ou Claude Code) dépend seulement de ce dont la tâche a besoin.

## Ce qu'il y a dedans

```
claude-hub/
├── README.md               vous êtes ici
├── CONVENTIONS.md          comment ajouter un cas d'usage (prospection, nouvel organisme...)
├── CATALOGUE.md            tous les skills : domaine, où les lancer, comment les déclencher
├── CLAUDE.md               consignes pour Claude quand il travaille DANS ce repo
├── partage/                ce qui sert partout (profil, voix, règles d'écriture) : source unique
├── plugins/                un plugin par domaine d'activité
│   └── idris-contenu/      veille IA + LinkedIn + Substack (Airtable Content Machine)
├── espaces/                un dossier de travail par client ou organisme (contexte + données)
│   └── intelligence-academy/
├── modeles/                gabarits pour créer un nouveau plugin ou un nouvel espace
├── global/CLAUDE.md        à brancher dans ~/.claude/CLAUDE.md (Claude Code)
└── outils/                 sync-partage.sh, verifier.sh, package-cowork.sh
```

Trois briques, trois rôles :

| Brique | Contient | Exemple | Règle |
|---|---|---|---|
| `partage/` | Ce qui est vrai pour tout ce que tu fais | Ta voix, pas de tiret cadratin | Modifié ici, copié dans chaque plugin par `outils/sync-partage.sh` |
| `plugins/<domaine>/` | Un savoir-faire réutilisable, sans données client | Rédiger un post LinkedIn | Installé dans Cowork et Claude Code |
| `espaces/<client>/` | Le contexte et les données d'un client ou organisme | Programme, apprenants, kit fourni | Ouvert dans Claude Code, ou connecté comme dossier dans Cowork |

## Où lancer quoi

Une question suffit : **la tâche a-t-elle besoin de fichiers locaux, de scripts ou d'une clé d'API privée ?** Oui : Claude Code. Non : Cowork.

| Tâche | Où | Pourquoi |
|---|---|---|
| Tâches à heure fixe (veille 8h et 19h) | Cowork, tâche planifiée | Tourne dans le cloud, ordinateur éteint |
| Contenu : posts, Substack, lignes Content Machine | Cowork | Connecteur Airtable, lancement en un clic, mobile |
| Mails, agenda, Drive, propositions, docs à partager | Cowork | Connecteurs Gmail, Calendar, Drive, Docs |
| Séances Intelligence Academy (API TIA, decks .pptx) | Claude Code dans `espaces/intelligence-academy` | Clé API, python-pptx, vérificateur |
| Supports de formation construits par scripts | Claude Code dans `espaces/<organisme>` | Fichiers, scripts, versions |
| Dev : n8n, VPS, firstcrm | Claude Code | Terminal, git, SSH |

## Installation

### Claude Code (sur ton Mac)

```bash
# 1. Récupérer le repo (une fois)
cd ~/Documents && git clone https://github.com/idrispjsalvi/claude-hub.git

# 2. Brancher le CLAUDE.md global (une fois)
mkdir -p ~/.claude && echo '@~/Documents/claude-hub/global/CLAUDE.md' >> ~/.claude/CLAUDE.md

# 3. Installer les plugins (une fois), dans Claude Code :
/plugin marketplace add ~/Documents/claude-hub
/plugin install idris-contenu@claude-hub
```

Après chaque `git pull`, lancer `/plugin marketplace update claude-hub` dans Claude Code pour récupérer les nouvelles versions.

**Espace Intelligence Academy** : la clé TIA n'est pas dans GitHub. Après le clone, recopier une fois ton fichier `.claude/settings.local.json` depuis l'ancien dossier `~/Documents/Intelligence Academy/` vers `~/Documents/claude-hub/espaces/intelligence-academy/.claude/`. Ensuite, ouvrir Claude Code dans `espaces/intelligence-academy`.

### Cowork

1. Dans une conversation Cowork, demander à Claude de packager le plugin depuis le repo (il lance `outils/package-cowork.sh`, qui produit `dist/<plugin>.plugin`) et de t'envoyer le fichier.
2. Le fichier s'affiche dans la conversation avec un bouton pour l'installer.
3. Les skills s'appellent alors `idris-contenu:veille-ia`, `idris-contenu:rediger-post-linkedin`, etc. Repointer les tâches planifiées dessus, tester, puis désactiver les anciens skills de compte.

## Au quotidien

- **Corriger un comportement** : modifier la référence concernée (voix, règles, base Airtable) plutôt que de le redire en conversation. Le correctif profite à tous les skills et aux deux outils.
- **Avant de pousser** : `outils/verifier.sh` (synchronise `partage/`, cherche les tirets cadratins et les secrets, valide les plugins), puis augmenter la `version` du plugin modifié dans son `plugin.json`.
- **Ajouter un cas d'usage** : suivre `CONVENTIONS.md`.
