# Guide d'Utilisation du GUI

## Lancer l'application

```bash
# Avec l'environnement virtuel activé
python -m comick_merger.main

# Ou avec uv (recommandé)
uv run python -m comick_merger.main
```

## Interface

L'interface principale comporte les sections suivantes :

### 1. Liste des fichiers CBZ

- **Ajouter des fichiers** :
  - Cliquez sur "Add Files..." et sélectionnez vos fichiers CBZ
  - Ou faites un **drag & drop** directement sur la liste

- **Réorganiser** :
  - Glissez-déposez les fichiers dans la liste pour changer l'ordre
  - L'ordre dans la liste détermine l'ordre dans le CBZ fusionné

- **Supprimer** :
  - Sélectionnez les fichiers et cliquez sur "Remove Selected"
  - Ou "Clear All" pour tout effacer

### 2. Fichier de sortie

- Cliquez sur "Browse..." pour choisir où sauvegarder le CBZ fusionné
- Par défaut : `merged.cbz`

### 3. Méthode de résolution des conflits

Deux options disponibles :

- **Prefixes (0_file.jpg)** - Par défaut ✓
  - Ajoute un préfixe numérique aux noms de fichiers
  - Plus compatible avec tous les lecteurs de comics
  - Exemple : `0_cover.jpg`, `1_cover.jpg`, `2_cover.jpg`

- **Folders (0/file.jpg)**
  - Place chaque CBZ dans un dossier numéroté
  - Plus organisé visuellement
  - Exemple : `0/cover.jpg`, `1/cover.jpg`, `2/cover.jpg`
  - Note : Certains lecteurs peuvent nécessiter navigation manuelle

### 4. Journal (Log)

- Affiche les opérations en cours
- Messages d'ajout/suppression de fichiers
- Progression de la fusion
- Erreurs éventuelles

### 5. Bouton de fusion

- Le bouton "Merge CBZ Files" devient actif quand :
  - Au moins 2 fichiers CBZ sont ajoutés
  - Un fichier de sortie est sélectionné

- Pendant la fusion :
  - Une barre de progression apparaît
  - L'interface est temporairement désactivée
  - Les messages de progression s'affichent dans le log

- En cas de succès :
  - Message de confirmation
  - Le fichier CBZ fusionné est créé à l'emplacement choisi

## Workflow typique

1. **Lancez l'application**
   ```bash
   python -m comick_merger.main
   ```

2. **Ajoutez vos fichiers CBZ**
   - Par drag & drop ou bouton "Add Files..."
   - Les fichiers apparaissent dans la liste

3. **Réorganisez si nécessaire**
   - Glissez-déposez pour changer l'ordre

4. **Choisissez le fichier de sortie**
   - Cliquez sur "Browse..."
   - Sélectionnez l'emplacement et le nom

5. **Choisissez la méthode de résolution**
   - Préfixes (recommandé) ou Dossiers

6. **Cliquez sur "Merge CBZ Files"**
   - Attendez la fin de la fusion
   - Un message de confirmation apparaît

7. **Votre CBZ fusionné est prêt !**

## Gestion des conflits

Si plusieurs CBZ contiennent des fichiers avec le même nom :

- **Avec préfixes** : Les fichiers sont renommés `0_nom.jpg`, `1_nom.jpg`, etc.
- **Avec dossiers** : Les fichiers sont placés dans `0/nom.jpg`, `1/nom.jpg`, etc.

Le nombre de zéros est calculé automatiquement selon le nombre de CBZ :
- 2-9 fichiers : `0`, `1`, ..., `9`
- 10-99 fichiers : `00`, `01`, ..., `99`
- 100-999 fichiers : `000`, `001`, ..., `999`
- Etc.

## Astuces

- **Ordre alphabétique** : Les lecteurs de comics lisent généralement les fichiers par ordre alphabétique
- **Test rapide** : Commencez avec 2-3 fichiers pour tester
- **Prévisualisation** : Ouvrez le CBZ fusionné avec votre lecteur préféré pour vérifier le résultat
- **Logs** : Consultez le journal pour suivre la progression et diagnostiquer les problèmes

## Raccourcis clavier

- **Ctrl+O** : Ajouter des fichiers (à implémenter)
- **Delete** : Supprimer les fichiers sélectionnés (à implémenter)
- **Ctrl+S** : Lancer la fusion (à implémenter)

## Dépannage

### L'application ne se lance pas

```bash
# Vérifiez que PyQt6 est installé
uv sync

# Essayez de lancer directement
.venv/Scripts/python.exe -m comick_merger.main
```

### Le bouton "Merge" est désactivé

- Vérifiez qu'au moins 2 fichiers CBZ sont ajoutés
- Vérifiez qu'un fichier de sortie est sélectionné

### Erreur lors de la fusion

- Vérifiez que les fichiers CBZ sont valides (archives ZIP)
- Vérifiez que vous avez les permissions d'écriture sur le dossier de sortie
- Consultez le journal pour plus de détails
