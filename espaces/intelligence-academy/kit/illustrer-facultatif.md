# Illustrer ses slides (facultatif) — recherche d'images

> **C'est un bonus.** Un deck de séance se tient sans aucune image : la charte TIA porte déjà la
> marque, et le cœur d'une séance est la pratique, pas l'illustration. Ce document sert quand une
> capture d'écran vaut mieux qu'un paragraphe — montrer l'interface d'un outil que l'élève va
> utiliser, un exemple de résultat, un schéma.
>
> **Il faut une clé Serper.** TIA n'en fournit pas : c'est un compte personnel, gratuit jusqu'à
> 2 500 recherches. ⛔ Ne demande jamais la clé de quelqu'un d'autre et ne la mets pas dans un
> fichier de travail — elle vit dans ton environnement, comme ta clé TIA.

## La clé

Crée un compte sur `serper.dev`, récupère la clé, puis :

```bash
export SERPER_API_KEY="ta-cle"
```

Sans cette variable, rien de ce qui suit ne marche — et c'est très bien : le deck se fabrique
quand même, sans images.

## Chercher

```bash
curl -s -X POST "https://google.serper.dev/images" \
  -H "X-API-KEY: $SERPER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"q": "<outil> interface screenshot 2026", "gl": "fr", "hl": "fr", "num": 20}'
```

La réponse contient un tableau `images[]` avec `imageUrl`, `title`, `source` et les dimensions.

**Deux ou trois angles valent mieux qu'une requête** : l'interface générale, l'écran précis dont tu
parles, le résultat obtenu. Une recherche en anglais (`"gl": "us", "hl": "en"`) rend souvent de
meilleures captures d'outils américains.

## Trier — l'étape qu'on saute et qu'on regrette

Télécharge les cinq ou six meilleurs candidats, puis **ouvre-les et regarde-les** (avec Claude Code :
l'outil Read affiche l'image). Rejette ce qui est flou, hors-sujet, ou montre une version de
l'interface qui n'existe plus. Une capture périmée en séance, c'est l'élève qui cherche un bouton
qui n'est plus là.

```bash
mkdir -p images
curl -s -o images/claude-projets.png "<imageUrl>"
```

Nomme les fichiers par ce qu'ils montrent (`claude-projets.png`), pas par leur origine
(`image1.png`). Convertis les `.webp` en `.png` avec Pillow si besoin — python-pptx ne lit pas
le webp.

## Le meilleur réflexe : ta propre capture

Quand tu veux montrer l'écran d'un outil, ouvre-le et fais la capture toi-même. C'est plus rapide
qu'une recherche, ça montre la version d'aujourd'hui, et c'est exactement ce que l'élève verra.

La recherche sert au reste : un schéma, une illustration de concept, une interface que tu n'as pas
sous la main.

## Poser l'image sur une slide

La librairie du kit ne fournit pas de fabrique « texte + image » : le modèle est dans
`generate_claude_fondamentaux.py` (helper `add_screenshot` + `slide_feature`), qui applique des
coins arrondis et conserve le ratio. Le principe tient en quelques lignes :

```python
from PIL import Image as PILImage
from pptx.util import Inches

def poser_image(slide, chemin, x, y, largeur_max, hauteur_max):
    """Pose une image en respectant son ratio. Retourne False si le fichier manque."""
    import os
    if not os.path.exists(chemin):
        return False                      # ⛔ pas de plantage, mais pas de silence non plus :
    pil = PILImage.open(chemin)           #    l'appelant DOIT tester ce retour et le dire.
    ratio = pil.width / pil.height
    if ratio >= largeur_max / hauteur_max:
        w = largeur_max; h = largeur_max / ratio
    else:
        h = hauteur_max; w = hauteur_max * ratio
    slide.shapes.add_picture(chemin, x, y + (hauteur_max - h) / 2, w, h)
    return True
```

⛔ **Le piège** : `add_picture` sur un fichier absent lève, alors on le garde par un
`os.path.exists` — et l'image disparaît sans un mot. C'est exactement ce qui a fait sortir nos
propres decks sans logo pendant des mois. Si `poser_image` rend `False`, **écris-le** dans la
console au lieu de continuer comme si de rien n'était.

## En une phrase à ton agent

> « Illustre la slide sur les projets Claude : cherche une capture d'interface avec Serper,
> montre-moi les candidates, et pose la meilleure à droite du texte. »
