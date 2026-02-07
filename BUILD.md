# Build : Générer un .exe distribuable pour comick-merger

## Approche : PyInstaller en mode `--onedir`

PyInstaller est l'outil standard pour packager des applications PyQt6 en .exe Windows. Le mode `--onedir` crée un dossier avec l'exe + les DLLs, qu'on zippe ensuite pour distribution.

## Étapes

1. **Ajouter PyInstaller aux dépendances dev** dans `pyproject.toml`
2. **Installer avec `uv sync`**
3. **Créer un fichier `comick_merger.spec`** configuré pour :
   - Point d'entrée : `comick_merger/main.py`
   - Mode `--onedir` (dossier)
   - Nom de l'exe : `ComickMerger.exe`
   - Mode `--windowed` (pas de console)
   - Exclusion des modules inutiles (tests, pytest, etc.)
4. **Lancer le build** via `uv run pyinstaller comick_merger.spec`
5. **Zipper le dossier** `dist/ComickMerger/` pour distribution

## Commandes rapides

```bash
# Installer les dépendances (dont pyinstaller)
uv sync

# Lancer le build
uv run pyinstaller comick_merger.spec

# Le résultat est dans dist/ComickMerger/
# Zipper ce dossier pour l'envoyer
```

## Vérification

- Lancer `dist/ComickMerger/ComickMerger.exe` pour vérifier que l'application se lance
- Vérifier que le .zip contient tout le nécessaire
