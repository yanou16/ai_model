import pandas as pd
import json

# Charger les données
df = pd.read_csv("data/general_data(1).csv")
emp = pd.read_csv("data/employee_survey_data.csv")
mgr = pd.read_csv("data/manager_survey_data.csv")

# Fusionner
df = pd.merge(df, emp, on='EmployeeID', how='left')
df = pd.merge(df, mgr, on='EmployeeID', how='left')

# Récupérer l'employé #28 (index 28 = EmployeeID 29 probablement, vérifier)
# On cherche par index pour être sûr c'est celui du find_high_risk.py
row = df.iloc[28]

# Convertir en dict et gérer les types numpy
data = row.to_dict()
for k, v in data.items():
    if pd.isna(v):
        data[k] = None
    else:
        data[k] = str(v)

with open('profile_28.json', 'w') as f:
    json.dump(data, f, indent=4)
print("Profil sauvegardé dans profile_28.json")
