import os
import requests
import json
from time import sleep
import re


"""
Explication étape par étape de l'execution du script :
1. **Configuration** : 
   - Définition de la clé API, du dossier contenant les PDFs et du fichier JSON de sortie.
   - Chargement des métadonnées déjà extraites depuis le fichier JSON.
2. **Fonctions** :
    - `upload_pdf`: Upload un PDF à ChatPDF et retourne son `sourceId`.
    - `ask_question`: Pose une question à un PDF et retourne la réponse.
    - `delete_pdf`: Supprime un PDF de ChatPDF.
    - `process_pdf`: Traite un PDF unique, pose une question et retourne les métadonnées extraites.
    - `update_json`: Met à jour le fichier JSON avec les données traitées.
"""


# Configuration
API_KEY = "sec_xxxxxxxxxxx"  # Remplacez par votre clé API
PDF_FOLDER = r"D:\0_Pour_ChatPDF"  # Dossier contenant les PDFs

# Question structurée
QUESTION = (
"Indique **uniquement l'année de publication** du document intitulé."
"Si aucune date explicite n’est trouvée dans le document, réponds exactement par : s.d."
"Aucune autre information, aucun texte supplémentaire."
)

HEADERS = {
    'x-api-key': API_KEY,
    'Content-Type': 'application/json'
}

def upload_pdf(file_path):
    """Upload un PDF à ChatPDF et retourne son sourceId"""
    try:
        with open(file_path, 'rb') as file:
            files = [('file', (os.path.basename(file_path), file, 'application/pdf'))]
            headers = {'x-api-key': API_KEY}
            
            response = requests.post(
                'https://api.chatpdf.com/v1/sources/add-file',
                headers=headers,
                files=files
            )
            
            if response.status_code == 200:
                return response.json()['sourceId']
            else:
                print(f"Erreur lors de l'UPLOAD: {response.status_code} - {response.text}")
                return None
    except Exception as e:
        print(f"Exception lors de l'UPLOAD: {str(e)}")
        return None

def ask_question(source_id, question):
    """Pose une question à un PDF et retourne la réponse"""
    data = {
        "sourceId": source_id,
        "messages": [{"role": "user", "content": question}],
        "referenceSources": True
    }
    
    try:
        response = requests.post(
            'https://api.chatpdf.com/v1/chats/message',
            headers=HEADERS,
            json=data
        )
        
        if response.status_code == 200:
            return response.json()['content']
        else:
            print(f"Erreur lors de la question: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"Exception lors de la QUESTION: {str(e)}")
        return None

def delete_pdf(source_id):
    """Supprime un PDF de ChatPDF"""
    data = {"sources": [source_id]}
    
    try:
        response = requests.post(
            'https://api.chatpdf.com/v1/sources/delete',
            headers=HEADERS,
            json=data
        )
        return response.status_code == 200
    except Exception as e:
        print(f"Exception lors de la SUPPRESSION: {str(e)}")
        return False

def process_pdf(file_path, item):
    """Traite un PDF unique et retourne les métadonnées extraites"""
    file_name = os.path.basename(file_path)

    # Upload du PDF
    source_id = upload_pdf(file_path)
    if not source_id:
        return None

    # Pose la question
    response = ask_question(source_id, (
        "À partir des éléments suivants :\n"
        f"- Titre : {item['Titre']}\n"
        f"- Description : {item.get('Description', 'Aucune description fournie')}\n"
        f"- Sujet principal : {item['Sujet']}\n\n"
        "Propose un **sujet secondaire pertinent** qui pourrait également être abordé dans ce document.\n"
        "**Réponds uniquement par le sujet secondaire, sans explication ni texte supplémentaire.**"
    ))

    if not response:
        delete_pdf(source_id)
        return None
    
    # Nettoyage de la réponse
    response = response.strip()
    response = re.sub(r'\n+', '\n', response)  # Supprime les lignes vides
    response = re.sub(r'\s+', ' ', response)  # Supprime les espaces multiples
    response = response.replace("\n", " ")  # Remplace les sauts de ligne par des espaces
    response = response.replace("'", "\'")  # Échappe les apostrophes
    response = response.replace('"', '\"')  # Échappe les guillemets
    response = response.replace("“", '"').replace("”", '"')  # Remplace les guillemets typographiques par des guillemets droits
    response = response.replace("‘", "'").replace("’", "'")  # Remplace les apostrophes typographiques par des simples
    

    # Supprime le PDF de ChatPDF
    delete_pdf(source_id)

    return response
  
def update_json(data):
    """Met à jour le fichier version.json avec les données traitées"""
    with open('version.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def main():
    """
    Le but de ce script est de demander à chatpdf d'extraire seulement la description d'un item json. Le json est déjà créé version.json.
    """
    # Vérifie que le dossier existe 
    if not os.path.exists(PDF_FOLDER):
        print(f"Le dossier {PDF_FOLDER} n'existe pas.")
        return
    
    data = []
    with open('version.json', 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            print("Erreur de décodage JSON dans version.json")
            return
          
    countTraitement = [item for item in data if not item.get("Sujet 2")]
    countTraitement = len(countTraitement)
    count = 0
          
    for item in data:
        if not item.get("Sujet 2"):
            count += 1
            print(f"\n\nTraitement de l'item {count}/{countTraitement}: {item['Titre']}")

            file_name = "nouveau_" + item["Fichier"]
            pdf_file = os.path.join(PDF_FOLDER, file_name)
            if not os.path.exists(pdf_file):
                print(f"Le fichier {pdf_file} n'existe pas.")
                continue
            res = process_pdf(pdf_file, item)
            if res:
                item["Sujet 2"] = res
                print("Sujet principal :", item["Sujet"])
                print("Sujet secondaire :", res)
                print(f"Sujet EXTRAIT pour {item['Titre']}")
                update_json(data)
            else:
                print(f"AUCUN sujet extraite pour {item['Titre']}")
            sleep(1)
                
    
if __name__ == "__main__":
    main()