# Comick Merger

Application desktop pour fusionner plusieurs fichiers CBZ (Comic Book Zip) en un seul fichier, avec gestion automatique des conflits de noms.

## Fonctionnalites

### Interface graphique (PyQt6)

- Import de fichiers CBZ par drag & drop ou via le bouton "Add Files..."
- Reorganisation de l'ordre des fichiers par glisser-deposer dans la liste
- Affichage intelligent des noms (ajout du dossier parent en cas de doublons)
- Choix du fichier de sortie
- Selection de la methode de resolution des conflits (prefixes ou dossiers)
- Barre de progression et journal d'operations en temps reel
- Fusion en arriere-plan (worker thread) pour garder l'interface reactive

### Interface en ligne de commande (CLI)

- Fusion rapide en une commande
- Verification des conflits sans fusion (`--check-only`)
- Support des deux methodes de resolution (prefixes par defaut, dossiers avec `--folders`)

### Gestion des conflits

Quand plusieurs CBZ contiennent des fichiers avec le meme chemin, deux methodes de resolution sont disponibles :

- **Prefixes** (par defaut) : chaque fichier est renomme avec un prefixe numerique (`0_cover.jpg`, `1_cover.jpg`)
- **Dossiers** : chaque CBZ source est place dans un dossier numerote (`0/cover.jpg`, `1/cover.jpg`)

Le padding des numeros est calcule automatiquement selon le nombre de CBZ a fusionner (ex: `00`, `01` pour 10+, `000`, `001` pour 100+, etc.).

### Distribution

L'application peut etre packagee en executable Windows autonome via PyInstaller. Le resultat est un dossier contenant `ComickMerger.exe` et ses dependances, distribuable sous forme de .zip.

## Installation

### Depuis les sources

Necessite Python 3.13+ et [uv](https://docs.astral.sh/uv/).

```bash
git clone <url>
cd comick-merger
uv sync
```

### Executable Windows

Telecharger le .zip depuis les releases, l'extraire, et lancer `ComickMerger.exe`.

## Utilisation

### Interface graphique

```bash
python -m comick_merger.main
```

1. Ajouter des fichiers CBZ (drag & drop ou bouton "Add Files...")
2. Reorganiser l'ordre si necessaire
3. Choisir le fichier de sortie via "Browse..."
4. Selectionner la methode de resolution des conflits
5. Cliquer sur "Merge CBZ Files"

Voir [GUI_GUIDE.md](GUI_GUIDE.md) pour le guide detaille.

### Ligne de commande

```bash
# Fusionner avec prefixes (par defaut)
python -m comick_merger.cli chapter1.cbz chapter2.cbz -o complete.cbz

# Fusionner avec dossiers
python -m comick_merger.cli *.cbz -o complete.cbz --folders

# Verifier les conflits sans fusionner
python -m comick_merger.cli *.cbz --check-only
```

## Build de l'executable

```bash
# Installer les dependances de dev
uv sync --extra dev

# Lancer le build PyInstaller
uv run pyinstaller comick_merger.spec --noconfirm

# Le resultat est dans dist/ComickMerger/
```

Voir [BUILD.md](BUILD.md) pour plus de details.

## Developpement

```bash
# Generer les donnees de test (une seule fois)
python tests/setup_test_data.py

# Lancer les tests
pytest tests/ -v

# Tests avec couverture
pytest tests/ --cov=comick_merger --cov-report=term-missing
```

Voir [DEVELOPMENT.md](DEVELOPMENT.md) pour l'architecture et les details techniques.

## Structure du projet

```
comick_merger/
  cbz_merger.py   # Logique de fusion (CBZFile, CBZMerger)
  cli.py           # Interface en ligne de commande
  gui.py           # Interface graphique PyQt6
  main.py          # Point d'entree GUI
comick_merger.spec # Configuration PyInstaller
tests/             # Tests unitaires
```

## Licence

MIT
