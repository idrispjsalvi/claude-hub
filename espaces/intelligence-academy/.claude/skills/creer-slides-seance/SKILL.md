---
name: creer-slides-seance
description: Génère le deck de slides (.pptx) d'une séance de coaching Intelligence Academy à partir du kit officiel TIA (charte graphique, librairie Python, vérificateur anti-débordement). Utilise ce skill dès que l'utilisateur demande de créer, générer ou préparer les slides, le deck ou le support d'une séance de coaching — même s'il ne dit pas explicitement "kit" ou "pptx", par exemple "prépare le deck pour la séance de [élève]" ou "fais-moi les slides de la prochaine séance".
---

# Créer les slides d'une séance

Génère un `.pptx` conforme à la charte TIA pour une séance de coaching, en repartant du kit
officiel plutôt qu'en dessinant des slides à la main.

## 1. Récupérer le kit

Si le dossier `kit/` n'existe pas déjà dans le répertoire de travail (ou s'il est potentiellement
périmé), télécharge-le :

```bash
curl -s -H "Authorization: Bearer $TIA_FORMATEUR_TOKEN" \
  "https://www.the-intelligence-academy.com/api/formateur-agent/kit?format=zip" -o kit.zip && unzip -o kit.zip && rm kit.zip
```

`$TIA_FORMATEUR_TOKEN` doit être défini dans l'environnement (voir le `CLAUDE.md` du projet). Si
la commande échoue en `401`, la clé est absente/expirée — dis-le à l'utilisateur plutôt que de
réessayer en boucle.

Le kit contient :

| Fichier | Rôle |
|---|---|
| `kit/skill-slides.md` | La charte et la méthode (palette, polices, types de slides, règles anti-débordement). **À lire en entier avant d'écrire le script.** |
| `kit/lib-slides-python.py` | La librairie : canvas, palette, primitives (`new_prs`, `blank_slide`, `add_header`, `add_subtitle`, `add_textbox`, `add_rounded_rect`, `add_brand_footer`, `save`) et des slides prêtes à l'emploi (`slide_cover`, `slide_section`, `slide_content`, `slide_pipeline`, `slide_recap`, `slide_questions`). |
| `kit/exemple-deck.py` | Un deck complet en exemple. **À lire avant d'écrire quoi que ce soit** — copie ses patterns au lieu de les réinventer. |
| `kit/verif-slides.py` | Le vérificateur de débordement — obligatoire avant de rendre le deck. |
| `kit/illustrer-facultatif.md` | Facultatif : comment illustrer une slide si `SERPER_API_KEY` existe. Sans cette variable, on fabrique le deck sans image, sans la réclamer. |
| `kit/deroule-seance.md` | Le déroulé de séance détaillé attendu chez TIA. |

## 2. Rassembler le contenu de la séance

Avant d'écrire une seule slide, sache pour QUI et POUR QUOI ce deck est fait : l'élève, son cas
d'usage métier, le module e-learning en cours, ce qui a été vu à la séance précédente. Si ces
informations n'ont pas déjà été rassemblées dans la conversation, va les chercher via l'API
décrite dans `CLAUDE.md` (`/dossiers/{id}`, `/dossiers/{id}/seances`) avant de continuer — un deck
générique sans ancrage sur le cas réel de l'élève ne sert à rien.

Le contenu du deck suit toujours cet ordre :
1. Quiz d'ouverture (3-5 questions) sur le e-learning vu et la séance précédente.
2. Quelques slides théoriques, seulement là où c'est nécessaire.
3. La consigne de l'exercice pratique, ancrée sur le cas d'usage réel de l'élève.
4. Les devoirs de la semaine, concrets et nommés.

## 3. Écrire le script du deck

1. Lis `kit/skill-slides.md` — la charte n'est pas négociable (police unique, palette fixe, canvas
   13.333″ × 7.5″).
2. Lis `kit/exemple-deck.py` et calque la structure de ton script dessus.
3. Écris un script Python qui importe `kit/lib-slides-python.py` et produit le `.pptx` avec les
   helpers de haut niveau (`slide_cover`, `slide_section`, `slide_content`, `slide_pipeline`,
   `slide_recap`, `slide_questions`) plutôt que de manipuler `python-pptx` directement.
   Dépendance requise : `pip install python-pptx`.

## 4. Vérifier avant de rendre

```bash
python3 kit/verif-slides.py "$PWD/<fichier>.pptx"
```

Utilise un **chemin absolu** — sinon le vérificateur cherche le fichier à côté de lui. Corrige le
script et relance tant que le vérificateur signale un débordement : un texte coupé se découvre en
séance, pas avant.

## 5. Rendre la main

Donne à l'utilisateur :
- le chemin du `.pptx` généré,
- un résumé du plan de séance en quelques lignes (quiz → théorie → pratique → devoirs).
