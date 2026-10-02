# Timothé BERNARD : séance 1

Vendredi 2 octobre 2026, 13h-15h, visio : https://meet.google.com/pvs-gaex-ghh
Formation « Améliorer l'efficacité de sa TPE à l'aide de l'IA » (21 h : 13 h e-learning + 4 séances de 2 h), du 28/09 au 12/11/2026.
Deck : `tim-bernard-s1-n8n-webhooks.pptx` (script `deck_s1.py`).

## Où il en est

- **Fil rouge** (Granola, 25/09) : offre d'automatisation pour artisans, cas « demande → formulaire → devis IA → l'artisan corrige et envoie ». Projet médical ECN mis de côté. Commercialisation visée au 1er décembre 2026. Le dossier TIA présente encore l'arbitrage artisans/ECN comme non tranché : il l'a été lors du RDV d'intro.
- **E-learning** (API) : module n8n en cours, 1 vidéo sur 6 et 3 fiches sur 15. Les modules suivants (Cursor et Claude Code, Maîtriser Claude Code, etc.) sont encore **verrouillés**.
- **Brief** : jamais envoyé.
- **Ce qu'il demande** (mail du 01/10, 16h33) : « poncer n8n un max », se faire réexpliquer ce qu'il n'a pas compris, et comprendre **sans IA à côté**.
- **Ce qu'il a tenté** (capture, mail du 01/10, 21h) : Webhook POST → Edit Fields → Switch (mode Rules) → Edit Fields1 et Edit Fields2, **tous deux branchés sur la sortie 0**. L'item part donc dans les deux branches : il n'y a aucun aiguillage. Il s'est arrêté (« plus j'avance moins je comprends »). C'est le point d'entrée de la séance.
- **Séances passées** : aucune (l'API n'en a pas, normal pour une S1).

## Le déroulé (120 min)

| Horaire | Bloc | Contenu |
|---|---|---|
| 13h00 | Cadrage (10 min) | Rappel du fil rouge, sa demande d'hier : n8n seulement, lui à la souris, pas de Claude pour construire |
| 13h10 | Quiz (10 min) | Trigger · Filter/IF/Switch · `$json` et `$('Nœud')` · item · onglet Executions |
| 13h20 | Sa capture (10 min) | Relire son workflow : pourquoi le Switch n'aiguille rien |
| 13h30 | Théorie (15 min) | Webhook (inverse du HTTP Request, URL test et production, `$json.body`), Edit Fields, Switch (règles, sorties, fallback) |
| 13h45 | Pratique (60 min) | « Demande artisan v1 » : Webhook POST → Edit Fields → Switch plomberie/électricité/fallback → Respond to Webhook ; test envoyé depuis un 2e workflow en HTTP Request (ça lui fait pratiquer les deux nœuds) |
| 14h45 | Devoirs et S2 (15 min) | Devoirs ci-dessous, fixer la date de la S2 |

Bonus si le temps le permet : un nœud IA sur la branche plomberie qui rédige un brouillon de devis (aperçu seulement, il veut d'abord comprendre sans IA).

## Devoirs annoncés

1. Vidéos n8n dans l'ordre : Variables, JSON et mapping, puis Conditions et boucles, puis HTTP Request et Webhooks.
2. Refaire « Demande artisan v1 » de zéro, seul, sans IA ni notes, avec un 3e métier.
3. Envoyer le brief artisans sur idris@the-intelligence-academy.com : 1 métier cible, les champs d'une demande, la structure d'un devis, un exemple.
4. Écrire à Antoine pour débloquer les modules Cursor et Claude Code.

## À trancher de ton côté

- **Contenu de la S2.** Le plan noté le 25/09 prévoit Claude Code et Cursor en S2. Tim demande d'approfondir n8n, et la brique suivante du fil rouge (devis IA) se construit dans n8n. Je te recommande de consacrer la S2 au nœud IA dans n8n et de décaler Claude Code et Cursor en S3. Les modules correspondants sont de toute façon verrouillés.
- **Dates S2 à S4** : rien n'est planifié dans l'API. Objectif noté le 25/09 : tout terminer avant fin octobre (la formation court jusqu'au 12/11).

## Points d'attention

- Risque de dispersion (dossier TIA) : garder le cap sur les artisans et ne pas rouvrir le sujet ECN.
- Le valoriser d'avoir arrêté plutôt que d'avoir bricolé : c'est exactement le cadrage dont il a besoin.
- Il a répondu sur ta boîte perso. Tu lui as déjà demandé de passer par idris@the-intelligence-academy.com : rappelle-le en fin de séance.
- Côté interlocuteurs : il signe « Timothé », et le dossier TIA l'appelle « Tim ».
