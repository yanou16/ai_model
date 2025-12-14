import pandas as pd
import pickle
import numpy as np

def find_high_risk():
    print("🔍 Recherche d'un profil à haut risque...")
    
    # Charger le modèle
    with open('models/attrition_model.pkl', 'rb') as f:
        model = pickle.load(f)
    
    # Charger les données pour avoir un exemple de base
    df = pd.read_csv("data/general_data(1).csv")
    
    # Essayer de trouver le profil avec la plus haute probabilité dans le dataset existant
    # (Note: on ne peut pas utiliser le pipeline complet sur le CSV brut car il manque les features temporelles calculées)
    # On va plutôt créer un "dummy" profil artificiel très mauvais
    
    # Colonnes attendues par le modèle (dans l'ordre approximatif)
    columns = ['Age', 'BusinessTravel', 'Department', 'DistanceFromHome', 'Education', 'EducationField',
       'Gender', 'JobLevel', 'JobRole', 'MaritalStatus', 'MonthlyIncome', 'NumCompaniesWorked',
       'PercentSalaryHike', 'StockOptionLevel', 'TotalWorkingYears', 'TrainingTimesLastYear',
       'YearsAtCompany', 'YearsSinceLastPromotion', 'YearsWithCurrManager',
       'EnvironmentSatisfaction', 'JobSatisfaction', 'WorkLifeBalance', 'JobInvolvement', 'PerformanceRating',
       'AvgWorkingHours', 'LateArrivals', 'AvgOvertime', 'AbsenceRate', 'WorkHoursVariance']
    
    # Charger les données brutes
    print("Chargement des profils réels...")
    df_gen = pd.read_csv("data/general_data(1).csv")
    df_emp = pd.read_csv("data/employee_survey_data.csv")
    df_mgr = pd.read_csv("data/manager_survey_data.csv")
    
    # Fusionner les données
    df_raw = pd.merge(df_gen, df_emp, on='EmployeeID', how='inner')
    df_raw = pd.merge(df_raw, df_mgr, on='EmployeeID', how='inner')
    
    # Filtrer ceux qui sont partis (Attrition = Yes)
    leavers = df_raw[df_raw['Attrition'] == 'Yes'].head(5)
    
    print("\n--- Test sur 5 employés qui sont VRAIMENT partis ---")
    
    # Note: On a besoin du pipeline complet. Le plus simple faire tourner predict sur le dossier data transformé
    # Mais ici on charge le csv brut. Il manque les features temporelles calculées.
    # On va faire une passe "rapide" en mettant des valeurs moyennes pour le temps
    # JUSTE pour voir si les features statiques suffisent à déclencher l'alarme
    
    time_cols = ['AvgWorkingHours', 'LateArrivals', 'AvgOvertime', 'AbsenceRate', 'WorkHoursVariance']
    
    output = []
    output.append(f"--- Test sur 5 employés qui sont VRAIMENT partis ---")

    for idx, row in leavers.iterrows():
        # Créer un dataframe pour ce profil
        profile = pd.DataFrame([row])
        
        # Ajouter features temporelles bidon (moyennes ou sévères) pour le test
        profile['AvgWorkingHours'] = 10.0
        profile['LateArrivals'] = 5
        profile['AvgOvertime'] = 2.0
        profile['AbsenceRate'] = 10.0
        profile['WorkHoursVariance'] = 3.0
        
        try:
            proba = model.predict_proba(profile)[0][1]
            decision = model.predict(profile)[0]
            
            res_str = f"Employé #{idx} (Parti): Score Modell = {proba:.2%} | Prédiction = {'OUI' if decision else 'NON'}"
            print(res_str)
            output.append(res_str)
            
            # Afficher quelques features clés pour comprendre
            output.append(f"   Age: {row['Age']}, Dept: {row['Department']}, Role: {row['JobRole']}, Income: {row['MonthlyIncome']}")
            output.append(f"   Satisfaction: {row['JobSatisfaction']}, OT: {profile['AvgOvertime'].values[0]}")
            output.append("-" * 30)

        except Exception as e:
            err = f"Erreur employé #{idx}: {e}"
            print(err)
            output.append(err)

    with open('real_leavers_output.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(output))
    
    print("Résultats sauvegardés dans real_leavers_output.txt")

if __name__ == "__main__":
    find_high_risk()
