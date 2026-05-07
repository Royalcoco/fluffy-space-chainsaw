# Formulaires + commandes GitHub (base 44x48)

Ce document te donne des **formulaires prêts à copier-coller** pour organiser ton dépôt GitHub et le retravailler avec IA vers un jeu d’exploration.

## 1) Formulaire “ajout de commandes GitHub”

### A. Informations dépôt
- **Nom du repo** :
- **Branche principale** : `main`
- **Branche de travail** : `feature/exploration-44x48`
- **Objectif** : Transformer le projet en jeu d’exploration avec grille **44x48**.

### B. Checklist commandes Git (opérationnel)
```bash
git checkout -b feature/exploration-44x48
git add .
git commit -m "feat: base exploration 44x48"
git push -u origin feature/exploration-44x48
```

### C. Checklist GitHub (PR)
- [ ] Ouvrir une Pull Request vers `main`
- [ ] Titre PR : `feat: exploration game base 44x48`
- [ ] Ajouter captures/vidéo de la navigation
- [ ] Lier les issues (`Closes #...`)
- [ ] Demander review (IA + humain)

## 2) Formulaire “retravail IA” (prompt prêt à l’emploi)

Copie ce prompt dans ton assistant IA :

```text
Tu es un ingénieur gameplay. Reprends mon dépôt GitHub et transforme-le en jeu d’exploration.
Contraintes:
1) Monde en grille 44 colonnes x 48 lignes.
2) Générer ou compléter les lignes manquantes de code (found and/or built lines).
3) Architecture modulaire: engine, map, player, events, ui.
4) Ajouter boucle de jeu, collisions, inventaire de base, points d’intérêt.
5) Produire commits atomiques + messages clairs.
6) Ajouter tests minimaux (chargement carte, déplacement, collisions).
7) Fournir un CHANGELOG des ajouts.
Sortie attendue:
- plan d’implémentation,
- fichiers créés/modifiés,
- commandes Git à exécuter,
- résumé PR prêt à publier.
```

## 3) Spécification technique “base 44x48”

- **Largeur (X)**: 44
- **Hauteur (Y)**: 48
- **Indexation recommandée**: `(x: 0..43, y: 0..47)`
- **Stockage map**: tableau 2D `map[48][44]`
- **Tuile vide**: `.`
- **Mur/obstacle**: `#`
- **Spawn joueur**: `S`
- **Objectif/point d’intérêt**: `O`

Exemple logique de validation:
```pseudo
assert width == 44
assert height == 48
assert 0 <= player.x < 44
assert 0 <= player.y < 48
```

## 4) Formulaire de “lignes trouvées/construites”

Utilise ce tableau dans chaque PR:

| Type | Fichier | Lignes | Description |
|---|---|---:|---|
| Found | src/map.* | 120-180 | Fonction de chargement existante détectée |
| Built | src/player.* | 1-90 | Nouveau module déplacement joueur |
| Built | src/collision.* | 1-70 | Détection obstacles + limites 44x48 |
| Found+Built | src/game_loop.* | 40-160 | Boucle existante complétée pour exploration |

## 5) Modèle PR (français)

```markdown
## Objectif
Transformer le projet en jeu d’exploration sur base 44x48.

## Changements
- ajout moteur déplacement
- ajout contraintes carte 44x48
- ajout collisions + POI
- complétion des lignes manquantes (found/built)

## Vérifications
- lancement local OK
- tests carte/déplacement/collisions OK

## Notes
- architecture prête pour quêtes, fog-of-war et sauvegarde.
```

## 6) Commandes de suivi recommandées

```bash
git status
git log --oneline -n 10
git diff main...feature/exploration-44x48
```

---
Si tu veux, je peux aussi te générer la **version automatisée** (script) qui crée ces templates directement dans `.github/` (issue templates + PR template + workflow CI).
