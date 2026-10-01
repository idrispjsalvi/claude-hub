# API Intelligence Academy — préparer mes séances

Je suis formateur chez Intelligence Academy et tu m'aides à préparer mes séances de coaching.
Ce fichier est la référence de l'API qui donne accès à mes élèves. Elle est en **lecture seule**.

Deux parties : **lire les données** (les routes ci-dessous), puis **générer le deck** avec le kit
de slides fourni par TIA (section « Générer le deck de la séance »).

---

# Lire les données

## Appeler l'API

```bash
B=https://www.the-intelligence-academy.com/api/formateur-agent
H="Authorization: Bearer $TIA_FORMATEUR_TOKEN"   # la clé est dans l'environnement, ne l'écris nulle part
curl -s -H "$H" "$B/index"
```

**Enveloppe commune.** Toute réponse porte `formateur_id`. Les collections portent en plus :

```json
{ "data": [ ... ], "count": 12, "next_cursor": "…|null", "complete": true }
```

- `complete: false` → il reste des lignes : rappelle la MÊME URL avec `?cursor=<next_cursor>`.
- `?limit=` accepte 1 à 500 (défaut 100).

**Codes.** `401` clé absente/expirée/coupée · `403` ce dossier ne m'est pas assigné · `404`
introuvable · `503` panne côté serveur — **réessaie**. Un `503` n'est jamais « rien à lire » :
quand il n'y a rien, l'API répond `200` avec `data: []`.

---

## GET /index — mes élèves

Une ligne par dossier assigné. Paginé.

```json
{
  "data": [{
    "dossier_id": "uuid",
    "nom_formation": "string|null",
    "status": "formateur_ok|planifie|en_cours|termine",
    "modalite": "string|null",
    "date_debut": "AAAA-MM-JJ|null",
    "date_fin": "AAAA-MM-JJ|null",
    "duree_heures": 32,
    "lieu": "string|null",
    "client": { "nom": "string|null", "email": "string|null", "telephone": "string|null" },
    "apprenants": [{ "id": "uuid", "prenom": "string|null", "nom": "string|null", "email": "string|null" }],
    "sessions_count": 8,
    "prochaine_session": "AAAA-MM-JJ|null",
    "heures_coaching": 16,
    "heures_elearning": 16,
    "progression_elearning": { "faits": 3, "commences": 1, "total": 6, "pct": 50 }
  }]
}
```

`progression_elearning` vaut `null` quand le programme n'a aucun module e-learning. L'unité est
la paire (apprenant × module) : `total` = modules e-learning × nombre d'apprenants.

---

## GET /dossiers/{dossier_id} — le briefing d'un élève

Non paginé. C'est la lecture principale avant une séance.

```json
{
  "dossier": {
    "id": "uuid", "nom_formation": "…", "modalite": "…",
    "date_debut": "AAAA-MM-JJ|null", "date_fin": "AAAA-MM-JJ|null",
    "duree_heures": 32, "lieu": "…|null", "status": "…",
    "objectif_professionnel": "string|null",
    "client": { "nom": "…", "email": "…", "telephone": "…" }
  },
  "contexte_client": {
    "besoins": ["…"], "pain_points": ["…"], "objectifs": ["…"], "contraintes": ["…"],
    "objectifs_concrets": ["…"], "deja_couvert_commercial": ["…"], "leviers_forces": ["…"],
    "style_apprentissage": "string|undefined",
    "personnalite": "string|undefined",
    "note_relationnelle": "string|undefined",
    "profil_apprenant": { },
    "contexte_critique": { "titre": "…", "description": "…" },
    "points_attention": [{ "titre": "…", "description": "…" }],
    "projets_concrets": [{ "nom": "…", "description": "…", "etat": "…" }],
    "objections_verbatim": [{ "citation": "…", "contexte": "…" }]
  },
  "programme": {
    "titre": "string|null", "resume": "string|null",
    "source": "is_current|derniere_version|null",
    "modules": [{
      "ordre": 1, "module_id": "uuid", "titre": "…", "description": "…",
      "objectifs": ["…"], "livrables": ["…"], "duree_heures": 2,
      "niveau": "debutant|intermediaire|avance",
      "type": "elearning|coaching|mixte",
      "cas_usage": "…"
    }],
    "parcours": [{ "type": "elearning", "module_id": "uuid" }, { "type": "session", "session_id": "uuid" }]
  },
  "apprenants": [{
    "id": "uuid", "prenom": "…", "nom": "…", "email": "…",
    "progression": [{
      "module_id": "uuid", "titre": "…",
      "status": "locked|available|in_progress|completed",
      "videos_faites": 3, "videos_total": 7,
      "guides_faits": 2, "guides_total": 5,
      "termine_le": "ISO|null"
    }]
  }],
  "sessions": [ /* même forme que /planning, voir plus bas */ ]
}
```

**`parcours` est la SÉQUENCE prévue** : elle dit quel module e-learning précède quelle séance.
Sers-t'en pour savoir ce que l'élève était censé avoir vu avant la prochaine séance.
**`programme.source`** : `is_current` = version validée (le cas normal) · `derniere_version` =
aucune version courante, on sert la plus récente, à traiter avec prudence · `null` = pas de
programme.

---

## GET /dossiers/{dossier_id}/crm — ce que l'élève a dit avant de s'inscrire

Paramètres : `?appels=N` (défaut 20) · `?messages=N` (défaut 50).

```json
{
  "contacts": [{ "contact_id": "uuid", "nom": "string|null", "email": "string|null" }],
  "appels": { "data": [{
    "call_id": "uuid",
    "date": "ISO|null",
    "direction": "inbound|outbound|null",
    "outcome": "string|null",
    "duree_secondes": 1820,
    "resume": "string|null",
    "points_cles": ["…"],
    "objections": ["…"],
    "sujets": ["…"],
    "transcript": "texte intégral|null"
  }], "count": 3, "complete": true, "next_cursor": null },
  "messages": { "data": [{
    "message_id": "uuid",
    "date": "ISO|null",
    "canal": "email|sms|whatsapp|imessage",
    "direction": "inbound|outbound|null",
    "sujet": "string|null",
    "corps": "texte, tronqué à 4000 caractères + '…[tronqué]'"
  }], "count": 12, "complete": true, "next_cursor": null }
}
```

Ces appels sont des **appels de VENTE** (le commercial et le client), pas des séances. Ils disent
le besoin d'origine, le métier, les objections. `complete: false` ici veut dire « la limite
demandée a été atteinte » : redemande avec un `appels=`/`messages=` plus grand.

---

## GET /dossiers/{dossier_id}/seances — nos séances passées

Paginé. Seules les séances ENREGISTRÉES ont un transcript (le présentiel n'en a pas) : une liste
vide ne veut pas dire « aucune séance n'a eu lieu ».

```json
{
  "data": [{
    "recording_id": "uuid",
    "session_id": "uuid|null",
    "date": "ISO|null",
    "transcript": "texte intégral de la séance|null",
    "cr_coaching": {
      "sujets_abordes": ["…"],
      "exercices_realises": ["…"],
      "niveau_progression": "…",
      "observations": "…",
      "prochaines_etapes": ["…"],
      "adaptations_faites": ["…"],
      "_cles_retenues": ["nom des champs volontairement non servis"]
    }
  }]
}
```

`cr_coaching` peut être `null` (compte-rendu pas encore produit). `_cles_retenues` liste des
NOMS de champs écartés : n'essaie pas de les obtenir, ils ne me sont pas destinés.

---

## GET /planning — mes séances

Paramètres : `?depuis=AAAA-MM-JJ` (borne au futur) · paginé.

```json
{
  "data": [{
    "session_id": "uuid",
    "dossier_id": "uuid",
    "date": "AAAA-MM-JJ|null",
    "debut": "HH:MM:SS|null",
    "fin": "HH:MM:SS|null",
    "type": "visio|presentiel|e-learning",
    "lieu": "string|null",
    "visio_link": "url|null",
    "status": "planifiee|draft|annulee",
    "non_tenue_at": "ISO|null",
    "titre": "string|null",
    "nom_formation": "string|null",
    "client": "string|null"
  }]
}
```

**`status` d'une séance** : `planifiee` = confirmée · `draft` = proposée, **pas encore confirmée** ·
`annulee` = annulée, ne la prépare pas. **`non_tenue_at`** renseigné = la séance a été déclarée
non tenue. Ne compte comme heures faites ou à venir que les séances `planifiee` sans `non_tenue_at`.

---

## GET /elearning/modules — la bibliothèque

Non paginé (~40 modules).

```json
{ "data": [{
  "module_id": "uuid", "titre": "…", "description": "string|null",
  "duree_heures": 2, "niveau": "…", "type": "elearning|mixte|coaching",
  "objectifs": ["…"], "videos_total": 7, "guides_total": 13,
  "outils": ["Airtable", "Make"]
}] }
```

## GET /elearning/modules/{module_id} — le contenu d'un module

```json
{ "module": {
  "module_id": "uuid", "titre": "…", "description": "…", "duree_heures": 2,
  "niveau": "…", "type": "…", "objectifs": ["…"],
  "videos_total": 7, "guides_total": 13, "outils": [],
  "lecons": [{
    "lecon_id": "uuid", "titre": "…", "description": "string|null",
    "type": "video|exercice", "ordre": 1, "duree_minutes": 12,
    "transcript": "le texte de la vidéo, avec des repères [MM:SS]|null"
  }],
  "guides_html": [{ "id": "…", "titre": "…", "contenu_html": "<h2>…", "ordre": 1 }]
} }
```

`transcript` est ce que l'élève a réellement ENTENDU : sers-t'en pour formuler le quiz d'ouverture
et pour ne pas ré-expliquer ce qui a déjà été dit. `guides_html` contient les exercices écrits.

---

---

# Générer le deck de la séance

Les slides ne se fabriquent pas à la main : TIA fournit un **kit** — une charte, une librairie
Python et un vérificateur — que tu récupères par l'API et que tu poses sur le disque une fois.

## Poser le kit (à faire une seule fois par dossier de travail)

```bash
curl -s -H "Authorization: Bearer $TIA_FORMATEUR_TOKEN" \
  "https://www.the-intelligence-academy.com/api/formateur-agent/kit?format=zip" -o kit.zip && unzip -o kit.zip && rm kit.zip
```

Ce que tu obtiens :

| Fichier | À quoi ça sert |
|---|---|
| `kit/skill-slides.md` | **La charte et la méthode** : palette, polices, les types de slides, les règles de rythme visuel et les limites anti-débordement. **Lis-le en entier avant d'écrire le script.** |
| `kit/lib-slides-python.py` | La librairie : canvas, palette, primitives (`new_prs`, `blank_slide`, `add_header`, `add_subtitle`, `add_textbox`, `add_rounded_rect`, `add_brand_footer`, `save`) et surtout des **slides entières prêtes à l'emploi** — `slide_cover`, `slide_section`, `slide_content`, `slide_pipeline`, `slide_recap`, `slide_questions`. Utilise-les plutôt que de dessiner à la main. |
| `kit/exemple-deck.py` | **Un deck complet, en exemple.** Le skill l'exige : lis-le AVANT d'écrire quoi que ce soit, et copie ses patterns au lieu de les réinventer. |
| `kit/verif-slides.py` | Le vérificateur de débordement — obligatoire avant de me rendre le deck. |
| `kit/illustrer-facultatif.md` | **Facultatif.** Comment illustrer une slide avec une recherche d'images, SI la variable `SERPER_API_KEY` existe. Sans elle, on fabrique le deck sans image et on ne la réclame pas. |
| `kit/deroule-seance.md` | Le déroulé de séance attendu chez TIA, en détail. |

Sans `unzip`, ou pour lire les pièces sans les écrire : `GET /kit` (sans `?format=zip`)
rend le même contenu en JSON — `{ "genere_le", "count", "complete", "pieces": [{ "id", "titre",
"chemin", "format", "contenu" }] }`. `?piece=<id>` n'en tire qu'une
(`deroule-seance`, `skill-slides`, `lib-slides-python`, `exemple-deck`,
`verif-slides`, `illustrer-facultatif`).

## Fabriquer le deck

1. Lis `kit/skill-slides.md` — la charte n'est pas négociable (police unique, palette fixe,
   canvas 13.333″ × 7.5″) — **puis `kit/exemple-deck.py`**, qui montre à quoi ressemble un deck
   fini. Copie sa structure ; ne réinvente pas les helpers.
2. Écris un script Python sur ce modèle : il importe `kit/lib-slides-python.py` et produit le
   `.pptx`. Il faut `python-pptx` (`pip install python-pptx`).
3. Lance `python3 kit/verif-slides.py "$PWD/<fichier>.pptx"` — **un chemin absolu**, sinon il
   cherche à côté de lui. Il détecte les slides qui débordent : **corrige jusqu'à ce qu'il ne
   signale plus rien.** Un texte coupé en silence se découvre en séance, pas avant.
4. Rends-moi le chemin du `.pptx` et le plan de la séance en quelques lignes.

Contenu attendu du deck, dans cet ordre : le quiz d'ouverture, les quelques slides théoriques si
elles sont nécessaires, la consigne de l'exercice pratique, les devoirs de la semaine.

---

## Comment se déroule une séance chez nous

2 heures minimum, une fois par semaine. La théorie de fond vit dans le e-learning ; la séance sert
à **mettre les mains dedans** sur le cas d'usage métier réel de l'élève. Le programme est une
**trame** : si le besoin évolue, on s'en écarte.

1. **Quiz d'ouverture** (3-5 questions) sur le e-learning vu et la séance précédente.
2. **Quelques slides théoriques, seulement là où c'est nécessaire.**
3. **La pratique** : partage d'écran, l'élève fait, je reprends la main pour montrer.
4. **Des devoirs** concrets et nommés pour la semaine.

## Ce que j'attends de toi

Quand je dis « prépare la séance de <élève> » :

1. `/index` pour trouver son `dossier_id`.
2. `/dossiers/<id>` et `/dossiers/<id>/seances`, et le module en cours via `parcours` si utile.
3. Dis-moi **où il en est** en quelques lignes : vu / coincé / prochaine étape annoncée / devoirs.
4. Propose le plan de séance selon le déroulé ci-dessus, **ancré sur SON cas d'usage** —
   `contexte_client.projets_concrets` et `contexte_client.objectifs_concrets` sont là pour ça.
5. Génère le deck (section « Générer le deck de la séance »), vérificateur passé.

⛔ N'invente jamais un fait sur l'élève : si l'information n'est pas dans une réponse, dis-le.
⛔ L'API ne fait que LIRE. Planifier, émarger, déclarer mes disponibilités se fait dans mon espace.
