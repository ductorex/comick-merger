# Tests

## Setup

Avant de lancer les tests pour la première fois, vous devez générer les fichiers CBZ de test :

```bash
python tests/setup_test_data.py
```

Cela crée environ **10 000 fichiers CBZ** dans `tests/test_data/` (~4 MB).

⚠️ **Important** : Les fichiers de test doivent être générés une seule fois. Ils sont exclus du dépôt git via `.gitignore`.

## Lancer les tests

```bash
# Tous les tests
pytest tests/ -v

# Avec couverture
pytest tests/ --cov=comick_merger --cov-report=term-missing

# Tests spécifiques
pytest tests/test_cbz_merger.py::TestCBZMergerPadding -v
```

## Structure des tests

### Fichiers de test créés

- **`test_data/simple/`** - 2 CBZ sans conflits
- **`test_data/conflict/`** - 3 CBZ avec des fichiers en conflit
- **`test_data/nested/`** - 2 CBZ avec des structures de dossiers imbriquées
- **`test_data/many/`** - 10 000+ CBZ numérotés pour tester le padding
  - Inclut les fichiers spécifiques : `chap1.cbz`, `chap2.cbz`, `chap3.cbz`, `chap9.cbz`, `chap10.cbz`, `chap11.cbz`, `chap1000.cbz`, `chap10000.cbz`
  - Fichiers numérotés : `chapter00000.cbz` à `chapter09999.cbz`
- **`test_data/special/`** - CBZ avec des entrées de répertoires
- **`test_data/invalid/`** - Fichiers invalides pour tester la gestion d'erreurs

### Catégories de tests

1. **`TestCBZFile`** - Chargement et validation des fichiers CBZ
2. **`TestCBZMergerConflictDetection`** - Détection des conflits
3. **`TestCBZMergerPadding`** - Calcul du padding pour 2, 10, 11, 100, 1000, 10000 fichiers
4. **`TestCBZMergerWithSpecificNames`** - Tests avec les noms spécifiques demandés
5. **`TestCBZMergerMerging`** - Fusion réelle avec préfixes et dossiers

## Performance

Les tests utilisent des **fixtures avec scope="session"** pour charger les fichiers une seule fois, ce qui réduit considérablement le temps d'exécution :

- Temps d'exécution : ~30 secondes (au lieu de 3+ minutes si les fichiers étaient créés à chaque test)
- Les tests sélectionnent seulement les fichiers nécessaires depuis `test_data/many/` (par exemple, les 100 premiers pour un test, les 1000 premiers pour un autre)

## Régénérer les données de test

Si vous modifiez `setup_test_data.py` ou si les fichiers sont corrompus :

```bash
python tests/setup_test_data.py
```

Le script supprime automatiquement `tests/test_data/` avant de recréer tous les fichiers.
