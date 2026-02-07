# Guide de Développement

## Installation

```bash
# Installer les dépendances
uv sync

# Activer l'environnement virtuel
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac
```

## Utilisation du CLI

### Créer des fichiers de test

```bash
python create_test_cbz.py
```

Cela crée 3 fichiers CBZ de test dans le dossier `test_cbz/` avec des conflits intentionnels.

### Commandes disponibles

```bash
# Vérifier les conflits sans fusionner
python -m comick_merger.cli test_cbz/*.cbz --check-only

# Fusionner avec préfixes (par défaut)
python -m comick_merger.cli test_cbz/chapter1.cbz test_cbz/chapter2.cbz -o merged.cbz

# Fusionner avec dossiers
python -m comick_merger.cli test_cbz/*.cbz -o merged.cbz --folders

# Spécifier un chemin de sortie
python -m comick_merger.cli *.cbz -o /path/to/output.cbz
```

## Architecture

### Modules

1. **`cbz_merger.py`** - Logique principale
   - `CBZFile`: Classe représentant un fichier CBZ
   - `CBZMerger`: Gère la détection de conflits et la fusion

2. **`cli.py`** - Interface en ligne de commande
   - Utilise `argparse` pour gérer les arguments
   - Affiche les conflits de manière lisible
   - Gère les erreurs proprement

3. **`main.py`** - Point d'entrée pour le GUI (à implémenter)

### Gestion des Conflits

Deux stratégies pour éviter l'écrasement de fichiers :

1. **Préfixes** (par défaut) : `0_page.jpg`, `1_page.jpg`
   - Plus compatible avec tous les lecteurs
   - Les fichiers restent à la racine du ZIP

2. **Dossiers** : `0/page.jpg`, `1/page.jpg`
   - Plus organisé visuellement
   - Peut nécessiter navigation manuelle dans certains lecteurs

Le padding des numéros est calculé automatiquement selon le nombre de CBZ.

## Prochaines Étapes

### GUI avec PyQt6

À implémenter dans `comick_merger/gui.py` :

- [ ] Fenêtre principale avec drag & drop
- [ ] Liste des CBZ importés (réorganisables)
- [ ] Sélection du fichier de sortie
- [ ] Choix de la méthode de prévention (préfixes/dossiers)
- [ ] Barre de progression pendant la fusion
- [ ] Affichage des conflits détectés

### Améliorations possibles

- [ ] Support du format CBR (RAR)
- [ ] Prévisualisation des images
- [ ] Option pour ne pas prévenir les conflits (écraser)
- [ ] Validation du format des images
- [ ] Compression des images avant fusion
- [ ] Tri naturel des fichiers (page_1, page_2, ..., page_10)

## Tests Manuels

```bash
# Test 1: Fusionner des CBZ sans conflits
# (créer manuellement des CBZ avec des noms différents)

# Test 2: Fusionner avec beaucoup de CBZ (>10) pour tester le padding
# Le padding devrait être 01, 02, ..., 10, 11

# Test 3: Vérifier l'ordre des fichiers dans le ZIP final
# Les lecteurs lisent généralement par ordre alphabétique
```

## Notes Techniques

- Les fichiers CBZ sont des archives ZIP standard
- Python utilise `zipfile` pour lire/écrire les ZIP
- Le module préserve l'ordre d'ajout des fichiers dans le ZIP
- Attention aux problèmes d'encodage sur Windows (éviter les caractères Unicode dans les prints)
