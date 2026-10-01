#!/usr/bin/env python3
"""Formation CC - MODULE 1 : Fondations (repo, secrets, source de vérité). Charte TIA."""
import os
from _cc_slides_lib import (new_prs, slide_cover, slide_section, slide_content,
                            slide_recap, slide_questions, save, SLIDES_DIR)

OUTPUT_PATH = os.path.join(SLIDES_DIR, "formation-cc-m1-fondations.pptx")
KICKER = "PILOTER CLAUDE CODE COMME UN POWER-USER"


def build():
    prs = new_prs()
    slide_cover(prs, KICKER, "Module 1 : Fondations",
                "Préparer le terrain pour qu'un agent soit efficace",
                "Repo, source de vérité, tout par API, secrets, mémoire")

    slide_section(prs, "1", "Le CLAUDE.md", "Le contrat de travail de l'agent")
    slide_content(prs, "Séquence 1 : Le CLAUDE.md", "Ce qu'un bon CLAUDE.md contient",
        [
            "Stack, architecture, commandes essentielles.",
            "Conventions de code, règles de travail (commit, push, jamais de PR).",
            "Les gotchas du projet (ce qui casse silencieusement).",
            "",
            "**Un CLAUDE.md riche = un agent qui ne se trompe pas de chemin.",
            "> j'aimerais que tu regardes tous les claude md de mes projets pour réutiliser des archi que j'aime",
        ])

    slide_section(prs, "2", "Source de vérité", "Une seule donnée canonique, le reste en dérive")
    slide_content(prs, "Séquence 2 : Source de vérité", "Le concept central",
        [
            "Pour chaque donnée : UNE source canonique. Tout le reste en dérive.",
            "",
            "Exemples : le dossier fait foi, tout s'écrit dans la base, le legacy est ignoré.",
            "",
            "**Anti-pattern : la même donnée éclatée en 3 endroits.",
            "C'est la racine n°1 des corruptions silencieuses.",
        ])

    slide_section(prs, "3", "Tout piloter par API", "Zéro clic manuel")
    slide_content(prs, "Séquence 3 : Tout par API", "Pourquoi tout par API",
        [
            "On pilote Vercel, Supabase, Cloudflare par API/curl, pas par dashboard.",
            "",
            "**Raison : un agent cloud doit être autonome, sans humain devant un écran.",
            "",
            "> connecté en direct aux apis de vercel supabase notamment pour les agents plus tard",
        ])

    slide_section(prs, "4", "Les secrets dans un vault", "Jamais en clair, jamais versionné")
    slide_content(prs, "Séquence 4 : Secrets", "La règle absolue",
        [
            "Bitwarden CLI : créer / lire les clés par commande.",
            "",
            "**Jamais de secret en clair dans un fichier versionné ou un fichier mémoire.",
            "(les mémoires sont auto-poussées sur GitHub : un secret y finirait public)",
            "",
            "On référence par le nom de l'item, jamais par la valeur.",
            "> teste et si ca marche tu peux le mettre dans bitwarden",
        ])

    slide_section(prs, "5", "Mémoire & docs", "La mémoire long-terme du projet")
    slide_content(prs, "Séquence 5 : Mémoire & docs", "Capitaliser en continu",
        [
            "Fichiers mémoire project_*.md + index, mis à jour au fil de l'eau.",
            "Plans dans docs/plans/, synchronisés avec le code.",
            "",
            "**« note tout » comme réflexe de fin de tâche.",
            "La doc synchronisée = ce qui survit quand le contexte se perd.",
        ])

    slide_recap(prs, "Module 1 : Fondations", [
        "1.  Un CLAUDE.md riche : stack, conventions, gotchas, commandes.",
        "2.  Une source de vérité par donnée ; le reste en dérive.",
        "3.  Tout par API pour rendre l'agent autonome.",
        "4.  Secrets dans un vault, jamais en clair ni versionnés.",
        "5.  Mémoire et docs : un livrable de premier ordre.",
    ])
    slide_questions(prs)
    save(prs, OUTPUT_PATH)


if __name__ == "__main__":
    build()
