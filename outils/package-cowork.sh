#!/usr/bin/env bash
# Fabrique un fichier .plugin par plugin dans dist/, a installer dans Cowork.
set -euo pipefail
cd "$(dirname "$0")/.."
./outils/sync-partage.sh >/dev/null
mkdir -p dist
for plugin in plugins/*/; do
  name="$(basename "$plugin")"
  rm -f "dist/$name.plugin"
  (cd "$plugin" && zip -qr "../../dist/$name.plugin" . -x "*.DS_Store")
  echo "dist/$name.plugin"
done
