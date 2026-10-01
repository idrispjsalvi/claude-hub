#!/usr/bin/env bash
# Copie partage/*.md dans plugins/*/references/partage/.
# A lancer apres toute modification de partage/ (le hook git pre-commit le fait aussi).
set -euo pipefail
cd "$(dirname "$0")/.."
for plugin in plugins/*/; do
  dest="${plugin}references/partage"
  mkdir -p "$dest"
  rm -f "$dest"/*.md
  for f in partage/*.md; do
    {
      echo "<!-- COPIE AUTOMATIQUE de partage/$(basename "$f"). Ne pas modifier ici : modifier partage/ puis lancer outils/sync-partage.sh -->"
      echo
      cat "$f"
    } > "$dest/$(basename "$f")"
  done
  echo "partage -> $dest"
done
