# Catalogue des skills

Mettre ce tableau à jour à chaque skill ajouté, renommé ou retiré.

| Skill | Plugin ou espace | Où le lancer | Comment le déclencher | Lit / écrit |
|---|---|---|---|---|
| `veille-ia` | idris-contenu | Cowork, tâches planifiées 8h et 19h | "passage du matin", "fais la veille" | Écrit des lignes dans Content Machine |
| `creer-ligne-content-machine` | idris-contenu | Cowork ou chat | "j'ai testé X, fais-en une ligne", "ajoute ce sujet" | Écrit une ligne dans Content Machine |
| `rediger-post-linkedin` | idris-contenu | Cowork (tâche à lancer en un clic) | Statut LinkedIn = "À générer", "rédige mes posts" | Écrit Post LinkedIn, Statut LinkedIn |
| `rediger-substack` | idris-contenu | Cowork (tâche à lancer en un clic) | Statut Substack = "À générer", "génère le Substack" | Écrit Note et Article Substack, Statut Substack |
| `affiner-angle` | idris-contenu | Cowork ou chat | "aide-moi à trouver mon angle", "challenge-moi sur ce dossier" | Écrit l'Angle attendu d'un Dossier après validation |
| `apprendre-de-mes-corrections` | idris-contenu | Cowork, tâche planifiée le vendredi 17h49 | "apprends de mes corrections" | Compare textes de Claude et versions publiées, propose des Leçons de style |
| `creer-slides-seance` | espaces/intelligence-academy (skill de projet, fourni par TIA) | Claude Code ouvert dans `espaces/intelligence-academy` | "prépare la séance de X", "fais les slides" | API TIA en lecture, écrit un .pptx dans `seances/` |

## Références partagées

| Fichier | Utilisé par |
|---|---|
| `partage/profil-idris.md` | Tous (via `global/CLAUDE.md` côté Claude Code) |
| `partage/voix-idris.md` | rediger-post-linkedin, rediger-substack, futurs skills d'écriture (prospection, e-mails) |
| `partage/regles-ecriture.md` | Tous les skills |
| `plugins/idris-contenu/references/content-machine.md` | Les 4 skills de contenu |
| `plugins/idris-contenu/references/angle-attendu.md` | rediger-post-linkedin, rediger-substack, creer-ligne-content-machine |
| `plugins/idris-contenu/references/style-vivant.md` | Skills de rédaction (leçons de style validées) |
| `plugins/idris-contenu/references/relecture.md` | Skills de rédaction (passe de relecture) |
| `plugins/idris-contenu/references/regard-editorial.md` | veille-ia, et le ton des skills de rédaction |
