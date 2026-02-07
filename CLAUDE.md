# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**comick-merger** est une application desktop qui permet de fusionner plusieurs fichiers CBZ (Comic Book Zip) en un seul fichier. Les fichiers CBZ sont des archives ZIP contenant des images de bandes dessinées/comics.

## Environment Setup

Ce projet utilise **uv** pour la gestion des dépendances Python et **Python 3.13+**.

```bash
# Installer les dépendances
uv sync

# Activer l'environnement virtuel
# Windows
.venv\Scripts\activate
# Linux/Mac
source .venv/bin/activate

# Exécuter l'application
python main.py
```

## Architecture et Fonctionnalités Clés

### Fonctionnalités à Implémenter

L'application doit permettre :

1. **Import de fichiers CBZ**
   - Import multiple ou un par un
   - Réorganisation de l'ordre des fichiers importés

2. **Fusion des CBZ**
   - Sélection du chemin de sortie
   - Fusion des archives en un seul CBZ

3. **Gestion des Conflits de Fichiers**
   - Détection des chemins identiques entre plusieurs CBZ sources
   - Génération d'erreurs explicites en cas de risque d'écrasement
   - Options de prévention des écrasements :
     - **Par préfixes** : Ajouter un préfixe numérique (00, 01, 02...) aux images de chaque CBZ source
     - **Par dossiers** : Placer les images de chaque CBZ dans un dossier numéroté (00/, 01/, 02/...)
   - Le padding des zéros doit être calculé dynamiquement selon le nombre de CBZ à fusionner
   - **Question ouverte** : Vérifier si les lecteurs de comics supportent bien la navigation multi-dossiers dans un CBZ (préférer les dossiers si oui)

### Structure Technique

- **Format CBZ** : Archive ZIP contenant des images (généralement JPEG/PNG)
- Les fichiers CBZ peuvent potentiellement contenir plusieurs dossiers
- L'ordre des fichiers dans le CBZ fusionné doit respecter l'ordre défini par l'utilisateur

## Running Tests

```bash
# Generate test data (run once, before first test run)
python tests/setup_test_data.py

# Run all tests
pytest tests/ -v

# Run tests with coverage
pytest tests/ --cov=comick_merger --cov-report=term-missing
```

## Testing the CLI

```bash
# Create test CBZ files (run once)
python create_test_cbz.py

# Check for conflicts only
python -m comick_merger.cli test_cbz/*.cbz --check-only

# Merge with prefixes (default: 0_file.jpg, 1_file.jpg)
python -m comick_merger.cli test_cbz/*.cbz -o merged.cbz

# Merge with folders (0/file.jpg, 1/file.jpg)
python -m comick_merger.cli test_cbz/*.cbz -o merged.cbz --folders
```

## Code Structure

- `comick_merger/cbz_merger.py` - Core logic for CBZ manipulation
  - `CBZFile`: Represents a CBZ and its contents
  - `CBZMerger`: Handles conflict detection and merging
- `comick_merger/cli.py` - Command-line interface
- `comick_merger/main.py` - GUI entry point (TODO)

## Running the GUI

```bash
# Launch the GUI application
python -m comick_merger.main

# Or with uv
uv run python -m comick_merger.main
```

See `GUI_GUIDE.md` for detailed usage instructions.

## Development Status

- ✅ Core merging logic implemented
- ✅ CLI fully functional
- ✅ Conflict detection working
- ✅ Both prefix and folder modes implemented
- ✅ PyQt6 GUI implemented with drag & drop
- ✅ Unit tests with optimized test data generation
