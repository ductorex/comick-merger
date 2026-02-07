# Comick Merger

Application desktop pour fusionner plusieurs fichiers CBZ (Comic Book Zip) en un seul.

## Fonctionnalités

✅ **Interface graphique moderne (PyQt6)**
- Import par drag & drop ou bouton
- Réorganisation des fichiers par glisser-déposer
- Choix du fichier de sortie
- Sélection de la méthode de résolution des conflits

✅ **Interface en ligne de commande (CLI)**
- Fusion rapide en une commande
- Vérification des conflits sans fusion

✅ **Gestion intelligente des conflits**
- Détection automatique des fichiers en conflit
- Deux méthodes de résolution :
  - **Préfixes** : `0_image.jpg`, `1_image.jpg` (recommandé)
  - **Dossiers** : `0/image.jpg`, `1/image.jpg`
- Padding automatique selon le nombre de fichiers (00, 000, 0000, etc.)

✅ **Robuste et testé**
- 22 tests unitaires avec pytest
- Support jusqu'à 10 000+ fichiers CBZ
- Validation des formats et gestion d'erreurs

## Installation

```bash
# Cloner le dépôt
git clone <url>
cd comick-merger

# Installer les dépendances avec uv (recommandé)
uv sync

# Ou avec pip
pip install -e .
```

## Utilisation

### Interface Graphique (GUI)

```bash
# Lancer l'application GUI
python -m comick_merger.main

# Ou utilisez les scripts de lancement
# Windows:
run_gui.bat

# Linux/Mac:
./run_gui.sh
```

Voir [GUI_GUIDE.md](GUI_GUIDE.md) pour le guide détaillé.

### Ligne de Commande (CLI)

```bash
# Fusionner avec préfixes (par défaut)
python -m comick_merger.cli chapter1.cbz chapter2.cbz chapter3.cbz -o complete.cbz

# Fusionner avec dossiers
python -m comick_merger.cli *.cbz -o complete.cbz --folders

# Vérifier les conflits sans fusionner
python -m comick_merger.cli *.cbz --check-only
```

## Développement

Voir [DEVELOPMENT.md](DEVELOPMENT.md) et [CLAUDE.md](CLAUDE.md) pour les instructions de développement.

### Tests

```bash
# Générer les données de test (une seule fois)
python tests/setup_test_data.py

# Lancer les tests
pytest tests/ -v

# Avec couverture
pytest tests/ --cov=comick_merger
```

## Résolution des Conflits

Quand plusieurs CBZ contiennent des fichiers avec le même nom, deux options :

1. **Préfixes** (recommandé) : `0_cover.jpg`, `1_cover.jpg`, `2_cover.jpg`
   - Plus compatible avec tous les lecteurs
   - Les fichiers restent à la racine

2. **Dossiers** : `0/cover.jpg`, `1/cover.jpg`, `2/cover.jpg`
   - Plus organisé visuellement
   - Peut nécessiter navigation manuelle dans certains lecteurs

Le padding est calculé automatiquement :
- 2-9 fichiers → `0`, `1`, ..., `9`
- 10-99 fichiers → `00`, `01`, ..., `99`
- 100-999 fichiers → `000`, `001`, ..., `999`
- 1000-9999 fichiers → `0000`, `0001`, ..., `9999`

## Licence

MIT
