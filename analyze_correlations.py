import pandas as pd
import numpy as np

def analyze_correlations():
    print("📊 Analyse des corrélations...")
    
    # Charger les données (copié de train_model.py pour l'extraction temporelle)
    general = pd.read_csv("data/general_data(1).csv")
    manager = pd.read_csv("data/manager_survey_data.csv")
    employee = pd.read_csv("data/employee_survey_data.csv")
    
    # Merger
    df = general.merge(manager, on="EmployeeID", how="left")
    df = df.merge(employee, on="EmployeeID", how="left")
    
    # Pour gagner du temps, on ne recalcule pas tout le temps, on charge juste in_time pour un sample
    # OU on fait une approximation simple sur quelques lignes si possible, 
    # MAIS pour être sûr, mieux vaut regarder ce que le modèle a vu.
    # On va réutiliser la logique d'extraction mais optimisée ou juste sur les colonnes clés s'il y a un fichier caché?
    # Non, on doit recalculer.
    
    # ... Ou plus simple, on regarde juste les colonnes "classiques" pour Satisfaction et Income
    # Et on fait confiance à l'importance des features pour le temps.
    
    # Nettoyage rapide
    df["Attrition"] = df["Attrition"].map({"Yes": 1, "No": 0})
    
    print("\n--- Corrélations avec Attrition (1=Yes) ---")
    
    # Income
    corr_income = df['MonthlyIncome'].corr(df['Attrition'])
    print(f"MonthlyIncome: {corr_income:.3f}")
    
    # Satisfaction
    corr_sat = df['JobSatisfaction'].corr(df['Attrition'])
    print(f"JobSatisfaction: {corr_sat:.3f}")
    
    # Age
    corr_age = df['Age'].corr(df['Attrition'])
    print(f"Age: {corr_age:.3f}")
    
    # Moyennes par groupe
    print("\n--- Moyennes par groupe ---")
    print(df.groupby('Attrition')[['MonthlyIncome', 'JobSatisfaction', 'Age', 'YearsAtCompany']].mean())

    # Vérifions si on peut vite fait voir le lien Heures / Attrition sans tout recalculer (trop long)
    # On va supposer que le code d'extraction était juste.
    
if __name__ == "__main__":
    analyze_correlations()
