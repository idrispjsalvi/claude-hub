---
name: "rediger-post-linkedin"
description: "Rédige en anglais les posts LinkedIn d'Idris (son avis, son ton) depuis les Dossiers de Content Machine dont le Statut LinkedIn est \"À générer\", en suivant l'Angle attendu et les leçons de style validées, puis passe à \"À valider\". À utiliser dès qu'Idris dit \"rédige mes posts\", \"génère le LinkedIn\", ou qu'un dossier est à \"À générer\"."
---

# Rédaction des posts LinkedIn d'Idris

## Pourquoi ce skill existe

Idris publie sur LinkedIn en anglais, avec un ton personnel, direct et positif sur l'IA. Sa veille alimente la base Airtable **Content Machine** : des news, regroupées en **Dossiers** (un sujet éditorial chacun). Il lit les dossiers, en choisit un, écrit l'**Angle attendu** sur le dossier (parfois juste "A" ou "B + ..." pour reprendre un angle proposé), puis passe le **Statut LinkedIn** à "À générer". Ce skill prend le relais : il transforme chaque dossier en un post qu'Idris n'aura presque plus qu'à relire et publier.

Le critère de réussite est simple : Idris lit le post et pense "c'est moi qui l'ai écrit", pas "c'est une IA qui imite LinkedIn". Tout ce qui suit sert cet objectif.

## Langue

Ce skill est en français. **Le post, lui, est toujours écrit en anglais**, quelle que soit la langue de l'Angle attendu (souvent en français) ou de la source. Le résumé de fin de tâche dans le chat se fait en français.

## Avant de commencer

Lire ces références (chemins relatifs au dossier de ce skill). Elles font partie du skill au même titre que ce fichier :

- `../../references/angle-attendu.md` : Principe n°1 (c'est Idris qui parle), comment lire l'Angle attendu comme un brief, cas particuliers (angle vide, angle qui va plus loin que les faits).
- `../../references/partage/voix-idris.md` : la voix d'Idris. Exigence n°1 : parler à une personne.
- `../../references/partage/regles-ecriture.md` : fiabilité, règles de recherche, typographie (aucun tiret cadratin), checklist anti-IA.
- `../../references/content-machine.md` : identifiants de la base, tables Dossiers et Content Machine, statuts et pièges, règles d'écriture.
- `../../references/style-vivant.md` : charger les leçons validées et les derniers posts publiés par Idris. Ils priment sur les exemples de ce fichier.
- `../../references/relecture.md` : construire le post, puis se relire comme Idris avant d'écrire dans Airtable.

Ce skill ne contient que ce qui est propre à LinkedIn.

## Workflow

### 1. Trouver les dossiers à traiter

1. Appeler `get_table_schema` sur la table **Dossiers** pour retrouver les identifiants de champs et les choix du champ **Statut LinkedIn** à partir de leurs noms.
2. Lister les dossiers dont le **Statut LinkedIn** est "À générer" avec `list_records_for_table` (filtre sur l'identifiant du choix, dans le champ Statut LinkedIn), en demandant : Dossier, En bref, Angles proposés, Angle attendu, News, Post LinkedIn, Note Substack, Article Substack, Statut LinkedIn.
3. Pour chaque dossier, lire ses news liées dans la table Content Machine (recordIds du champ News) : Sujet, Résumé IA, Analyse IA, Source, Source URL, Date de la source.
4. S'il n'y a aucun dossier "À générer", le dire simplement et s'arrêter. Si l'utilisateur a nommé un dossier précis, ne traiter que celui-là et vérifier son statut avant.

Ne jamais lire ni écrire le champ **Statut Substack** dans ce skill (voir les pièges dans `content-machine.md`).

### 2. Charger le style vivant

Une fois par exécution, comme décrit dans `style-vivant.md` : leçons validées (Canal LinkedIn ou Tous) et 3 à 5 derniers posts publiés.

### 3. Lire l'angle, rassembler la matière, creuser si demandé

Lire le dossier comme décrit dans `angle-attendu.md`.

**Recherche complémentaire** (règles dans `regles-ecriture.md`), seulement dans deux cas :

1. L'Angle attendu la demande, même en une demi-phrase ("va chercher", "vérifie", "trouve des chiffres", "compare avec", "étaye avec un exemple", "creuse"). C'est alors une vraie mission : plusieurs recherches croisées.
2. Un chiffre ou un fait indispensable au post manque ou paraît incohérent.

En dehors de ces cas, les news du dossier suffisent : la veille a déjà fait le travail de fond. Les sources consultées ne vont pas dans le post, seulement dans le résumé du chat.

### 4. Construire, rédiger, se relire

Suivre `relecture.md` dans l'ordre : colonne vertébrale, premier jet, relecture comme Idris, version finale. Appliquer la section "Structure d'un post" ci-dessous et les points LinkedIn plus bas. Si une Note ou un Article existe déjà sur le dossier, ne pas ouvrir sur la même phrase ni reprendre ses formules. Un seul post par dossier, une seule version (pas de variantes).

### 5. Écrire dans Airtable et vérifier

Un seul appel `update_records_for_table` par dossier qui écrit **en même temps** :

- **Post LinkedIn** : le texte du post, tel quel.
- **Statut LinkedIn** : "À valider" (nom du choix en chaîne simple).

Ne toucher à aucun autre champ. Puis relire un ou deux dossiers écrits : texte non tronqué, retours à la ligne conservés, Statut LinkedIn à "À valider". Règles d'écriture : `content-machine.md`.

### 6. Résumé dans le chat (en français, court)

- Nombre de posts générés et leurs Dossiers.
- Les leçons de style qui ont le plus pesé (une ligne).
- Pour chaque post, une phrase sur l'angle retenu si utile.
- Quand une recherche a été faite : ce qu'elle a trouvé de déterminant, les sources consultées (nom et URL), et surtout ce qu'elle n'a pas pu confirmer ou ce qui contredit l'angle.
- Les consignes de l'angle qui n'ont pas pu être respectées, et pourquoi.
- Les points d'attention : angle vide, affirmation prudente à cause d'une info non confirmée, dossiers non traités et pourquoi.

Pas de second rapport : les posts sont déjà dans Airtable, ne pas les recopier dans le chat sauf demande.

## Structure d'un post

La forme est simple et se répète, mais sans gabarit rigide : la longueur et le rythme s'adaptent à l'angle et à la matière. Tout ce qui suit (structure, longueur, emojis, hashtags, clôture) est un réglage par défaut : si l'Angle attendu demande autre chose ("court", "pas d'emojis", "finis par une question sur X", "ton provocateur", "sans hashtags"), l'angle gagne.

1. **Accroche (première ligne, idéalement moins de 200 caractères).** C'est ce qui s'affiche avant "voir plus", donc c'est ce qui décide de la lecture. Elle donne un fait frappant, un chiffre, une tension ou une promesse claire. Formes que fait Idris :
   - un fait chiffré : "5 days, 2 classes, 90 students. One goal: ..."
   - un test ou un avertissement : "I tested X so you don't have to."
   - un contraste entre deux voix : "Yesterday, a researcher ... resigned ... A few desks away, another heavyweight puts that same risk at under 0.01%."
   - un contexte partagé : "Back-to-work season is here, and I already know what ... "
   Ne pas commencer par "I'm excited to share", ni par une question creuse.
2. **Développement** en courtes lignes séparées par des lignes vides : le fait, puis la lecture d'Idris, c'est-à-dire son angle (pourquoi c'est important selon lui, ce qu'il en conclut). Une idée par paragraphe. Les listes s'écrivent avec la flèche "→" en début de ligne (jamais de puces "•" ou "-", jamais d'emojis en guise de puces).
3. **Prise de position** claire : l'angle, dit franchement.
4. **Clôture** : une phrase qui donne quelque chose (un message, une conséquence pratique, une ouverture). Une question au lecteur seulement si elle est précise et vraiment utile ("Have you tested it yet? What broke first?"), jamais "What do you think?" seul.
5. **Hashtags** sur la dernière ligne, après une ligne vide : 3 à 6, le premier est presque toujours #AI, les autres sont précis (l'outil, l'entreprise, le sujet).

### Longueur

Si une leçon validée fixe une longueur, elle prime. Sinon, variable selon l'angle, entre environ 600 et 1 600 caractères (hashtags inclus) dans la majorité des cas :

- angle tranchant, une seule idée : court, 600 à 1 000 caractères ;
- angle qui demande un raisonnement ou un contre-argument : 1 000 à 1 600 caractères ;
- post qui renvoie vers un article Substack : 700 à 1 300 caractères. Il donne envie de lire l'article, il ne le résume pas ;
- ne jamais dépasser 2 500 caractères (la limite LinkedIn est 3 000).

Ne pas gonfler pour atteindre une longueur : un post plus court qui dit une chose nette vaut mieux.

### Emojis, liens, mentions

- **Emojis** : 1 à 3 par post, jamais zéro. Chacun de ses posts de référence en contient au moins un, c'est une part de sa signature et de la chaleur du ton. Les placer naturellement en fin de phrase, ou en tout début de post (par exemple 🎓, 🙏, 😉, 👇, ⬇️, un drapeau quand on parle d'un pays). Pas d'emoji dans chaque paragraphe, pas de rangée d'emojis.
- **Liens** : pas d'URL dans le corps du post (LinkedIn pénalise la portée des liens externes, et Idris met ses liens en commentaire). Citer la source par son nom dans le texte quand elle renforce le propos ("according to CNBC", "reported by The Information"). Ne pas écrire "link in the comments" : il n'y a rien à mettre en commentaire tant qu'Idris n'a pas décidé d'y mettre la source, et le post doit fonctionner tel quel.
- **Mentions de personnes** : ne pas taguer ni citer de personnes de l'équipe ou de tiers si ce n'est pas dans le dossier Airtable.
- **Newsletter** : ne pas inventer de renvoi à une newsletter ou à un article.
- **Questions au lecteur** : une ou deux par post, pas plus.

## Format du texte stocké dans le champ

Le contenu du champ **Post LinkedIn** est du texte brut, prêt à être collé dans LinkedIn sans aucune retouche :

- aucun markdown : pas de `**gras**`, pas de `#` de titre, pas de blocs de code, pas de guillemets décoratifs autour du post ;
- une ligne vide entre les paragraphes, retours à la ligne réels ;
- uniquement le post, sans commentaire de Claude, sans tiret long (voir `regles-ecriture.md`).

## Points anti-IA propres à LinkedIn

En plus de la checklist commune :

- Accroche qui commence par "I'm excited to share" ou par une question creuse.
- Puces "•" ou "-", ou emojis en guise de puces (LinkedIn : flèche "→" uniquement).
- Clôture "What do you think?" seule.
- Tiret cadratin caché dans les hashtags.

## Exemples de référence : posts réels d'Idris

Ces quatre posts sont la référence de voix **de départ**. Ils datent d'avant le passage à l'anglais natif et à Substack : dès qu'Idris a publié des posts récents (champ Version publiée LinkedIn, voir `style-vivant.md`), ces derniers priment. S'en imprégner (rythme, accroches, façon de se positionner, dosage des emojis et des hashtags), sans jamais en recopier des phrases ni réutiliser leurs anecdotes.

### Exemple 1 (retour d'une intervention en école)

```
5 days, 2 classes, 90 students. One goal: going far beyond simple conversational AI. 🎓

Last week, I taught the Master's students of the PGE program at Esdes Business School (Université Catholique de Lyon) as part of the AI for Business course.

On the agenda:
→ AI
→ Data
→ Prompting
→ Automation
→ Agents

Schools train the professionals of tomorrow. And companies increasingly expect their new hires to master AI well beyond simple conversation. That's what I came to bring them.

What struck me most was the exchange with Gen Z. Listening to their fears about AI in light of the latest news in the field (thanks, media), and responding while keeping a critical mind. It led to fascinating discussions.

Because this is a paradoxical generation: the most connected to digital tools and the most reluctant toward AI technologies, yet the first to enter the job market without ever having known a professional world without them.

My message to them: in the age of AI, your intelligence, your critical thinking, your agility and your curiosity remain your biggest value drivers.

Thanks to Alegria.group, Audric Mazzietti (Dr) and Camille Faure for this opportunity 🙏

#AI #ArtificialIntelligence #Training #GenZ #Automation #AIAgents #ESDES #BusinessSchool
```

### Exemple 2 (test d'un outil)

```
I tested the new Make plugin for ChatGPT so you don't have to.

The promise: build, run, and monitor your Make scenarios straight from a ChatGPT conversation, no visual editor needed.

I gave it one instruction: watch a Gmail label, summarize the biggest AI news from the last 24 hours, write a report in Notion.

It built the whole scenario in under a minute.

Then it crashed on the first run.

What happened next tells you a lot about where AI automation actually stands today: what ChatGPT got right, where it got stuck, and why I still had to open Make myself to fix it.

Full breakdown, screenshot by screenshot, in this week's newsletter. Free to read, link in comments. ⬇️

#AI #Automation #Make #ChatGPT
```

### Exemple 3 (prise de position contre le sensationnalisme)

```
Yesterday, a researcher who spent three years at OpenAI and then Anthropic resigned, explaining that the teams building AI "earnestly believe it could kill us all by the end of the decade."

A few desks away, another heavyweight in the industry puts that same risk at under 0.01%.

Welcome to AI in 2026: nobody agrees with each other, but only one narrative ever takes off. Always the same one. Whichever one is the most frightening.

This sensationalism has been getting on my nerves for months now. To the point where I deserted LinkedIn for football content to relax instead.

So this week, I needed to lay it all out clearly: why this fear gets so much traction, what it reveals about how little we actually understand AI, and above all, the good this technology is already doing for humanity.

A little bit of positivity won't hurt you. 😉

I go into all of it in my latest newsletter. It's free, and the link is in the comments. ⬇️

#AI #ArtificialIntelligence #Positivity #Newsletter
```

### Exemple 4 (décryptage d'un outil que tout le monde teste)

```
🎒 Back-to-work season is here, and I already know what my clients are going to ask me about this week: Kimi AI.

The Chinese AI 🇨🇳 that had everyone talking all summer, the one everyone tried out and compared to ChatGPT and Claude, without necessarily having the time to dig into it properly, or fully grasp what it actually means for their business.

So I killed two birds with one stone: instead of answering the same question fifteen times on calls this week, I put together a full breakdown of the AI everyone's been talking about.

What's inside:
→ How Kimi works day to day (modes, memory, projects)
→ Cluster, its "agent swarm" mode that can deploy up to 300 sub-agents in parallel
→ Kimi Work, its desktop agent that drives your browser and files
→ How it stacks up against Claude and ChatGPT on agentic capabilities
→ Pricing, updated as of August 31
→ And the point too many people skip before jumping in: data security and GDPR compliance

The article is in English, but nothing's stopping you from translating it into French (like you're about to do with this post, too 😉).

Enjoy the read (the link is in the first comment), and if you end up testing Kimi yourself, let me know what you think in the comments 👇

#AI #ArtificialIntelligence #KimiAI #Claude #ChatGPT #Business #Newsletter
```

Remarque sur ces exemples : ils mentionnent des expériences vécues, une newsletter et un lien en commentaire parce que c'étaient de vrais faits ce jour-là. Pour un post généré depuis un dossier Airtable, ces éléments ne sont repris que si l'Angle attendu du dossier les contient. Ce que l'on transpose, c'est la manière, pas le contenu.

## Cas limites propres à LinkedIn

- **Plusieurs dossiers "À générer"** : ne pas répéter la même accroche ni les mêmes hashtags d'un post à l'autre.
- Les autres cas (angle vide, angle très court, angle qui contredit les faits, deux dossiers sur le même sujet) sont décrits dans `angle-attendu.md` ; sujets sensibles et droit d'auteur dans `regles-ecriture.md`.
