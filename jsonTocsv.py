import json
import csv

# Colonnes à ajouter si elles sont absentes
colonnes_a_ajouter = [
    "Droits", "Importance matérielle"
]

# Charger les données JSON
with open('version.json', 'r', encoding='utf-8') as json_file:
    data = json.load(json_file)

# Ajouter les colonnes manquantes avec des valeurs vides
for item in data:
    for colonne in colonnes_a_ajouter:
        if colonne not in item:
            item[colonne] = ""

# Liste complète des colonnes dans l'ordre souhaité
fieldnames = list(data[0].keys())

# Écriture du fichier CSV compatible Excel
with open('donnees_excel.csv', 'w', encoding='utf-8-sig', newline='') as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames, delimiter=';')
    writer.writeheader()
    writer.writerows(data)
