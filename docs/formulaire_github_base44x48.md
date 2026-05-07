# Formulaires + commandes GitHub (base28 ➜ base44x48 ➜ base64)

Ce document te donne des **formulaires prêts à copier-coller** pour organiser ton dépôt GitHub et le retravailler avec IA vers un jeu d’exploration, en progression **base28 puis base64**.

## 1) Formulaire “ajout de commandes GitHub”

### A. Informations dépôt
- **Nom du repo** :
- **Branche principale** : `main`
- **Branche de travail** : `feature/exploration-base28-base64`
- **Objectif** : Transformer le projet en jeu d’exploration avec montée par paliers: **28 ➜ 44x48 ➜ 64**.

### B. Checklist commandes Git (opérationnel)
```bash
git checkout -b feature/exploration-base28-base64
git add .
git commit -m "feat: progression base28 vers base64"
git push -u origin feature/exploration-base28-base64
```

### C. Checklist GitHub (PR)
- [ ] Ouvrir une Pull Request vers `main`
- [ ] Titre PR : `feat: exploration game progression base28 to base64`
- [ ] Ajouter captures/vidéo de la navigation
- [ ] Lier les issues (`Closes #...`)
- [ ] Demander review (IA + humain)

## 2) Formulaire “retravail IA” (prompt prêt à l’emploi)

Copie ce prompt dans ton assistant IA :

```text
Tu es un ingénieur gameplay. Reprends mon dépôt GitHub et transforme-le en jeu d’exploration.
Contraintes:
1) Déployer en 3 paliers: base28, puis 44x48, puis base64.
2) Générer ou compléter les lignes manquantes de code (found and/or built lines).
3) Architecture modulaire: engine, map, player, events, ui.
4) Ajouter boucle de jeu, collisions, inventaire de base, points d’intérêt.
5) Produire commits atomiques + messages clairs, un commit par palier.
6) Ajouter tests minimaux (chargement carte, déplacement, collisions) pour chaque palier.
7) Fournir un CHANGELOG des ajouts et migrations.
Sortie attendue:
- plan d’implémentation,
- fichiers créés/modifiés,
- commandes Git à exécuter,
- résumé PR prêt à publier.
```

## 3) Spécification technique des paliers

### Palier A — base28
- **Largeur (X)**: 28
- **Hauteur (Y)**: 28
- **Indexation**: `(x: 0..27, y: 0..27)`
- **Stockage map**: `map[28][28]`

### Palier B — base44x48
- **Largeur (X)**: 44
- **Hauteur (Y)**: 48
- **Indexation**: `(x: 0..43, y: 0..47)`
- **Stockage map**: `map[48][44]`

### Palier C — base64
- **Largeur (X)**: 64
- **Hauteur (Y)**: 64
- **Indexation**: `(x: 0..63, y: 0..63)`
- **Stockage map**: `map[64][64]`

### Tuiles standard (tous paliers)
- **Tuile vide**: `.`
- **Mur/obstacle**: `#`
- **Spawn joueur**: `S`
- **Objectif/point d’intérêt**: `O`

Exemple logique de validation:
```pseudo
assert width in [28, 44, 64]
assert height in [28, 48, 64]
assert 0 <= player.x < width
assert 0 <= player.y < height
```

## 4) Formulaire de “lignes trouvées/construites”

Utilise ce tableau dans chaque PR:

| Palier | Type | Fichier | Lignes | Description |
|---|---|---|---:|---|
| base28 | Found | src/map.* | 120-180 | Fonction de chargement existante détectée |
| base28 | Built | src/player.* | 1-90 | Déplacement joueur initial |
| 44x48 | Built | src/collision.* | 1-70 | Limites et obstacles 44x48 |
| base64 | Found+Built | src/game_loop.* | 40-220 | Boucle complétée pour grande carte |

## 5) Modèle PR (français)

```markdown
## Objectif
Transformer le projet en jeu d’exploration avec progression base28 ➜ 44x48 ➜ base64.

## Changements
- palier base28 implémenté
- migration carte vers 44x48
- extension finale vers base64
- complétion des lignes manquantes (found/built)

## Vérifications
- lancement local OK
- tests carte/déplacement/collisions OK sur les 3 paliers

## Notes
- architecture prête pour quêtes, fog-of-war et sauvegarde.
```

## 6) Commandes de suivi recommandées

```bash
git status
git log --oneline -n 15
git diff main...feature/exploration-base28-base64
```

---
Si tu veux, je peux aussi te générer la **version automatisée** (script) qui crée ces templates directement dans `.github/` (issue templates + PR template + workflow CI) avec variantes base28/44x48/64.
