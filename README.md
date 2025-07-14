# Extraction de Métadonnées PDF avec ChatPDF

## Description

Ce projet permet d'extraire automatiquement des métadonnées secondaires à partir de fichiers PDF, en utilisant l'API ChatPDF. Il traite un ensemble de documents, pose des questions ciblées à l'API, et met à jour un fichier JSON avec les informations extraites.

## Fonctionnalités

- Téléversement automatique de PDF vers ChatPDF.
- Extraction d'un sujet secondaire pertinent pour chaque document.
- Mise à jour dynamique d'un fichier `version.json` contenant les métadonnées enrichies.
- Gestion des erreurs (fichiers manquants, erreurs d'API, etc.).
- Nettoyage des réponses pour garantir la cohérence des données.

## Prérequis

- Python 3.x
- Un compte et une clé API ChatPDF valide
- Les bibliothèques Python suivantes :
  - `requests`
  - `json`
  - `os`
  - `re`
  - `time`

## Installation

1. Clonez ce dépôt ou copiez les fichiers dans un dossier local.
2. Installez les dépendances nécessaires :
   ```powershell
   pip install requests
   ```
3. Placez vos fichiers PDF dans le dossier spécifié par la variable `PDF_FOLDER` (par défaut `D:\0_Pour_ChatPDF`).
4. Préparez un fichier `version.json` contenant les métadonnées de base de vos documents.

## Utilisation

1. Renseignez votre clé API dans la variable `API_KEY` du fichier `chatPDF_Modif.py`.
2. Exécutez le script :
   ```powershell
   python chatPDF_Modif.py
   ```
3. Le script traitera chaque document, extraira le sujet secondaire et mettra à jour le fichier `version.json`.

## Structure du projet

- `chatPDF_Modif.py` : Script principal d'extraction et de traitement.
- `version.json` : Fichier JSON contenant les métadonnées des documents (à créer/compléter).
- `csvJson.py`, `jsonTocsv.py` : Scripts utilitaires pour la conversion entre formats CSV et JSON.

## Exemple de structure du fichier `version.json`

```json
[
  {
    "Titre": "Titre du document",
    "Fichier": "nom_du_fichier.pdf",
    "Description": "Description du document",
    "Sujet": "Sujet principal",
    "Sujet 2": null
  }
]
```

## Remarques

- Si un fichier PDF n'est pas trouvé, il passe au suivant.
- Le script attend 1 seconde entre chaque requête pour éviter de surcharger l'API.

---

# PDF Metadata Extraction with ChatPDF

## Description

This project automatically extracts secondary metadata from PDF files using the ChatPDF API. It processes a set of documents, asks targeted questions to the API, and updates a JSON file with the extracted information.

## Features

- Automatic upload of PDFs to ChatPDF.
- Extraction of a relevant secondary subject for each document.
- Dynamic update of a `version.json` file containing enriched metadata.
- Error handling (missing files, API errors, etc.).
- Cleans up responses to ensure data consistency.

## Requirements

- Python 3.x
- A valid ChatPDF account and API key
- The following Python libraries:
  - `requests`
  - `json`
  - `os`
  - `re`
  - `time`

## Installation

1. Clone this repository or copy the files to a local folder.
2. Install the required dependencies:
   ```powershell
   pip install requests
   ```
3. Place your PDF files in the folder specified by the `PDF_FOLDER` variable (default is `D:\0_Pour_ChatPDF`).
4. Prepare a `version.json` file containing the basic metadata for your documents.

## Usage

1. Enter your API key in the `API_KEY` variable in `chatPDF_Modif.py`.
2. Run the script:
   ```powershell
   python chatPDF_Modif.py
   ```
3. The script will process each document, extract the secondary subject, and update the `version.json` file.

## Project Structure

- `chatPDF_Modif.py`: Main extraction and processing script.
- `version.json`: JSON file containing document metadata (to be created/completed).
- `csvJson.py`, `jsonTocsv.py`: Utility scripts for CSV/JSON conversion.

## Example `version.json` Structure

```json
[
  {
    "Titre": "Document title",
    "Fichier": "file_name.pdf",
    "Description": "Document description",
    "Sujet": "Main subject",
    "Sujet 2": null
  }
]
```

## Notes

- If a PDF file is not found, it skips to the next one.
- The script waits 1 second between each request to avoid overloading