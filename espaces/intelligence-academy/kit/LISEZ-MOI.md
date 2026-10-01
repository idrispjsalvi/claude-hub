# Kit slides — Intelligence Academy (version du 2026-09-02)

À poser à la racine de ton dossier de travail, puis ouvrir Claude Code dedans.

- `deroule-seance.md` — Comment on veut que les séances se passent
- `skill-slides.md` — Le skill de génération des slides (charte TIA)
- `lib-slides-python.py` — La librairie Python partagée des decks (palette, helpers, types de slides)
- `verif-slides.py` — Le vérificateur de débordement des slides
- `exemple-deck.py` — Un deck COMPLET en exemple — le modèle à copier
- `illustrer-facultatif.md` — BONUS — illustrer ses slides (nécessite une clé Serper personnelle)
- `logos/` — 10 logos (dont `ia-round.png`, posé au pied de chaque slide).
  ⛔ Ne pas les déplacer : la librairie les cherche à cet endroit précis, et un logo
  introuvable est SAUTÉ en silence — le deck sort sans marque sans que rien ne le dise.

Ordre de lecture pour l'agent : la charte (`skill-slides`), puis le deck d'exemple
(`exemple-deck`), puis écrire le script en important `lib-slides-python`. Avant de rendre
un deck : `python3 kit/verif-slides.py "$PWD/<fichier>.pptx"` — il attrape les slides dont
le texte déborde.

Il faut Python et `python-pptx` (`pip install python-pptx`).