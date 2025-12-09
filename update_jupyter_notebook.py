"""
Script pour ajouter automatiquement les features temporelles dans data_cleaning.ipynb
Exécuter avec: python update_jupyter_notebook.py
"""

import nbformat
from nbformat.v4 import new_code_cell
import os

# Code de la cellule à ajouter
cell_code = '''# =========================================================
# Extraction des Features Temporelles
# =========================================================

import numpy as np

def extract_time_features():
    """Extrait les features temporelles depuis in_time.csv et out_time.csv"""
    print("⏰ Extraction des features temporelles...")
    
    # Charger les données temporelles
    in_time = pd.read_csv("data/in_time.csv")
    out_time = pd.read_csv("data/out_time.csv")
    
    # Identifier la colonne EmployeeID (première colonne)
    employee_id_col = in_time.columns[0]
    
    # Extraire les colonnes de dates (toutes sauf la première)
    date_columns = in_time.columns[1:]
    
    time_features = []
    
    for idx, row in in_time.iterrows():
        employee_id = row[employee_id_col]
        
        # Récupérer les heures d'arrivée et de départ
        in_times = row[date_columns]
        out_times = out_time.iloc[idx][date_columns]
        
        # Convertir en datetime
        in_times_dt = pd.to_datetime(in_times, errors='coerce')
        out_times_dt = pd.to_datetime(out_times, errors='coerce')
        
        # Calculer les heures de travail pour chaque jour
        working_hours = []
        late_count = 0
        overtime_hours = []
        
        for in_t, out_t in zip(in_times_dt, out_times_dt):
            if pd.notna(in_t) and pd.notna(out_t):
                # Heures travaillées
                hours = (out_t - in_t).total_seconds() / 3600
                working_hours.append(hours)
                
                # Retards (arrivée après 9h00)
                if in_t.hour >= 9 and in_t.minute > 0:
                    late_count += 1
                
                # Heures supplémentaires (plus de 8h)
                if hours > 8:
                    overtime_hours.append(hours - 8)
        
        # Calculer les features
        avg_working_hours = np.mean(working_hours) if working_hours else 8.0
        avg_overtime = np.mean(overtime_hours) if overtime_hours else 0.0
        absence_rate = (len(date_columns) - len(working_hours)) / len(date_columns) * 100
        work_hours_variance = np.var(working_hours) if len(working_hours) > 1 else 0.0
        
        time_features.append({
            'EmployeeID': employee_id,
            'AvgWorkingHours': round(avg_working_hours, 2),
            'LateArrivals': late_count,
            'AvgOvertime': round(avg_overtime, 2),
            'AbsenceRate': round(absence_rate, 2),
            'WorkHoursVariance': round(work_hours_variance, 2)
        })
    
    time_df = pd.DataFrame(time_features)
    print(f"✅ Features temporelles extraites pour {len(time_df)} employés")
    print(f"   Nouvelles colonnes: {list(time_df.columns[1:])}")
    
    return time_df

# Extraire les features temporelles
time_features = extract_time_features()

# Afficher les premières lignes
print("\\n📊 Aperçu des features temporelles:")
display(time_features.head())

# Statistiques descriptives
print("\\n📈 Statistiques des features temporelles:")
display(time_features.describe())

# Merger avec le DataFrame principal
print(f"\\n🔄 Avant merge: {df.shape[0]} lignes, {df.shape[1]} colonnes")
df = df.merge(time_features, on="EmployeeID", how="left")
print(f"✅ Après merge: {df.shape[0]} lignes, {df.shape[1]} colonnes")

# Vérifier qu'il n'y a pas de valeurs manquantes
print("\\n🔍 Valeurs manquantes dans les nouvelles features:")
new_features = ['AvgWorkingHours', 'LateArrivals', 'AvgOvertime', 'AbsenceRate', 'WorkHoursVariance']
for feature in new_features:
    missing = df[feature].isnull().sum()
    print(f"   {feature}: {missing} valeurs manquantes")

# =========================================================
# Visualisations des Features Temporelles
# =========================================================

fig, axes = plt.subplots(2, 3, figsize=(18, 10))
fig.suptitle('📊 Distribution des Features Temporelles', fontsize=16, fontweight='bold')

# 1. AvgWorkingHours
axes[0, 0].hist(df['AvgWorkingHours'], bins=30, color='skyblue', edgecolor='black')
axes[0, 0].set_title('Heures Moyennes Travaillées')
axes[0, 0].set_xlabel('Heures')
axes[0, 0].set_ylabel('Fréquence')
axes[0, 0].axvline(df['AvgWorkingHours'].mean(), color='red', linestyle='--', label=f'Moyenne: {df["AvgWorkingHours"].mean():.2f}h')
axes[0, 0].legend()

# 2. LateArrivals
axes[0, 1].hist(df['LateArrivals'], bins=30, color='lightcoral', edgecolor='black')
axes[0, 1].set_title('Nombre de Retards')
axes[0, 1].set_xlabel('Retards')
axes[0, 1].set_ylabel('Fréquence')
axes[0, 1].axvline(df['LateArrivals'].mean(), color='red', linestyle='--', label=f'Moyenne: {df["LateArrivals"].mean():.1f}')
axes[0, 1].legend()

# 3. AvgOvertime
axes[0, 2].hist(df['AvgOvertime'], bins=30, color='lightgreen', edgecolor='black')
axes[0, 2].set_title('Heures Supplémentaires Moyennes')
axes[0, 2].set_xlabel('Heures')
axes[0, 2].set_ylabel('Fréquence')
axes[0, 2].axvline(df['AvgOvertime'].mean(), color='red', linestyle='--', label=f'Moyenne: {df["AvgOvertime"].mean():.2f}h')
axes[0, 2].legend()

# 4. AbsenceRate
axes[1, 0].hist(df['AbsenceRate'], bins=30, color='orange', edgecolor='black')
axes[1, 0].set_title('Taux d\\'Absence (%)')
axes[1, 0].set_xlabel('Taux (%)')
axes[1, 0].set_ylabel('Fréquence')
axes[1, 0].axvline(df['AbsenceRate'].mean(), color='red', linestyle='--', label=f'Moyenne: {df["AbsenceRate"].mean():.2f}%')
axes[1, 0].legend()

# 5. WorkHoursVariance
axes[1, 1].hist(df['WorkHoursVariance'], bins=30, color='purple', edgecolor='black')
axes[1, 1].set_title('Variance des Heures de Travail')
axes[1, 1].set_xlabel('Variance')
axes[1, 1].set_ylabel('Fréquence')
axes[1, 1].axvline(df['WorkHoursVariance'].mean(), color='red', linestyle='--', label=f'Moyenne: {df["WorkHoursVariance"].mean():.2f}')
axes[1, 1].legend()

# 6. Corrélation avec Attrition
attrition_corr = df[new_features + ['Attrition']].corr()['Attrition'].drop('Attrition').sort_values()
axes[1, 2].barh(attrition_corr.index, attrition_corr.values, color='teal')
axes[1, 2].set_title('Corrélation avec Attrition')
axes[1, 2].set_xlabel('Corrélation')
axes[1, 2].axvline(0, color='black', linestyle='-', linewidth=0.5)

plt.tight_layout()
plt.show()

# =========================================================
# Analyse de l'Impact sur l'Attrition
# =========================================================

print("\\n📊 Comparaison des features temporelles par statut d'attrition:")
print("="*70)

for feature in new_features:
    print(f"\\n{feature}:")
    print(f"   Employés restants: {df[df['Attrition']==0][feature].mean():.2f}")
    print(f"   Employés partis:   {df[df['Attrition']==1][feature].mean():.2f}")
    diff = df[df['Attrition']==1][feature].mean() - df[df['Attrition']==0][feature].mean()
    print(f"   Différence:        {diff:+.2f}")

print("\\n✅ Features temporelles intégrées avec succès!")
print(f"   Le DataFrame contient maintenant {df.shape[1]} colonnes")
'''

def update_notebook():
    """Ajoute la cellule de features temporelles au notebook"""
    
    notebook_path = "data_cleaning.ipynb"
    
    if not os.path.exists(notebook_path):
        print(f"❌ Erreur: Le fichier {notebook_path} n'existe pas!")
        return
    
    print(f"📂 Lecture du notebook: {notebook_path}")
    
    # Lire le notebook
    with open(notebook_path, 'r', encoding='utf-8') as f:
        nb = nbformat.read(f, as_version=4)
    
    # Vérifier si la cellule existe déjà
    for cell in nb.cells:
        if 'extract_time_features' in cell.source:
            print("⚠️  La cellule de features temporelles existe déjà!")
            print("   Aucune modification nécessaire.")
            return
    
    # Trouver où insérer (après le merge des datasets)
    insert_index = None
    for i, cell in enumerate(nb.cells):
        if 'merge' in cell.source.lower() and 'employeeid' in cell.source.lower():
            insert_index = i + 1
            break
    
    if insert_index is None:
        # Si pas trouvé, ajouter à la fin
        insert_index = len(nb.cells)
        print("⚠️  Position d'insertion non trouvée, ajout à la fin du notebook")
    
    # Créer la nouvelle cellule
    new_cell = new_code_cell(cell_code)
    
    # Insérer la cellule
    nb.cells.insert(insert_index, new_cell)
    
    # Sauvegarder le notebook
    backup_path = notebook_path.replace('.ipynb', '_backup.ipynb')
    print(f"\n💾 Création d'une sauvegarde: {backup_path}")
    with open(backup_path, 'w', encoding='utf-8') as f:
        nbformat.write(nb, f)
    
    print(f"💾 Mise à jour du notebook: {notebook_path}")
    with open(notebook_path, 'w', encoding='utf-8') as f:
        nbformat.write(nb, f)
    
    print("\n✅ Notebook mis à jour avec succès!")
    print(f"   Cellule ajoutée à la position {insert_index}")
    print(f"   Sauvegarde créée: {backup_path}")
    print("\n📋 Prochaines étapes:")
    print("   1. Ouvrir data_cleaning.ipynb dans Jupyter")
    print("   2. Exécuter la nouvelle cellule")
    print("   3. Vérifier les visualisations et statistiques")

if __name__ == "__main__":
    print("\n" + "="*60)
    print("🚀 MISE À JOUR DU NOTEBOOK JUPYTER")
    print("="*60 + "\n")
    
    update_notebook()
    
    print("\n" + "="*60)
    print("✅ TERMINÉ!")
    print("="*60 + "\n")
