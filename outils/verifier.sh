#!/usr/bin/env bash
# Controles avant commit : partage synchronise, aucun tiret cadratin, aucun secret, plugins valides.
set -uo pipefail
cd "$(dirname "$0")/.."
ok=0
./outils/sync-partage.sh >/dev/null
if grep -rIl $'—\|–' partage plugins README.md CONVENTIONS.md CATALOGUE.md CLAUDE.md global 2>/dev/null; then
  echo "ERREUR : tiret cadratin ou demi-cadratin dans les fichiers ci-dessus"; ok=1; fi
if git ls-files --cached --others --exclude-standard | grep -E 'settings\.local\.json$|\.env$' ; then
  echo "ERREUR : un fichier de secrets serait versionne"; ok=1; fi
if git ls-files --cached --others --exclude-standard -z | xargs -0 grep -IlE '(TIA_FORMATEUR_TOKEN|API_KEY)"?\s*[:=]\s*"[A-Za-z0-9_-]{16,}' 2>/dev/null; then
  echo "ERREUR : une cle semble ecrite en clair dans les fichiers ci-dessus"; ok=1; fi
if command -v claude >/dev/null; then
  for p in plugins/*/; do claude plugin validate "$p" || ok=1; done
fi
[ $ok -eq 0 ] && echo "OK : tout est propre"
exit $ok
