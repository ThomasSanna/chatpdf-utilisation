import csv
import json

"""
Json voulu : [
  {
    "Titre": "120 Randonnées et Balades au Coeur du PNRC",
    "Titre alternatif": "",
    "Description": "La collection de guides la plus complète pour visiter et parcourir la Corse. Elle offre un choix de balades et de randonnées — familiales ou sportives — pour découvrir les micro-régions de l'île et les sites de montagne de manière inédite.",
    "Table des matières": "Avant-propos, Introduction, Carte d'identité, Historique et présentation, Charte et mission, Carte et randonnées, Biotopes et végétation, Faune, Géologie, la randonnée, Recommandations",
    "Sujet": "Etudes de l'environnement Géographie Paysages",
    "Sujet 1": "Géographie",
    "Sujet 2": "Randonnées$Nature",
    "Type": "Textes imprimés",
    "Identifiant": "ISBN 2-905124-55-5",
    "Créateur": "Gauthier, Alain",
    "Éditeur": "Éditions Albiana",
    "Contributeur": "Parc Naturel Régional de Corse",
    "Contributeur 2": "Sanna, Thomas",
    "Langue": "Français",
    "Date": "2003",
    "Format": "Imprimé",
    ... ETC...
    
    Le CSV a pour première ligne les noms des colonnes, et les lignes suivantes contiennent les données.
"""

def csv_to_json(csv_file_path, json_file_path):
  with open(csv_file_path, encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile, delimiter=';')
    data = list(reader)

  with open(json_file_path, 'w', encoding='utf-8') as jsonfile:
    json.dump(data, jsonfile, ensure_ascii=False, indent=2)
        
csv_to_json('1800PDF24-06.csv', 'version.json')