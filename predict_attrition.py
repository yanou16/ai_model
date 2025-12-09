"""
🎯 Outil de Prédiction d'Attrition des Employés
Utilisation: python predict_attrition.py
"""

import pandas as pd
import numpy as np
import pickle
import os
from colorama import init, Fore, Style

# Initialiser colorama pour les couleurs dans le terminal
init(autoreset=True)

def load_model():
    """Charge le modèle entraîné"""
    model_path = 'models/attrition_model.pkl'
    
    if not os.path.exists(model_path):
        print(f"{Fore.RED}❌ Erreur: Le modèle n'existe pas!")
        print(f"{Fore.YELLOW}💡 Lancez d'abord: python train_model.py")
        return None
    
    with open(model_path, 'rb') as f:
        model = pickle.load(f)
    
    print(f"{Fore.GREEN}✅ Modèle chargé avec succès!\n")
    return model

def get_user_input():
    """Demande les informations de l'employé à l'utilisateur"""
    print(f"{Fore.CYAN}{'='*60}")
    print(f"{Fore.CYAN}🔍 PRÉDICTION D'ATTRITION - Entrez les informations de l'employé")
    print(f"{Fore.CYAN}{'='*60}\n")
    
    # Informations démographiques
    print(f"{Fore.YELLOW}📋 Informations Démographiques:")
    age = int(input("  Age: "))
    gender = input("  Genre (Male/Female): ")
    marital_status = input("  Statut marital (Single/Married/Divorced): ")
    distance_from_home = int(input("  Distance du domicile (km): "))
    
    # Éducation
    print(f"\n{Fore.YELLOW}🎓 Éducation:")
    print("  1=Below College, 2=College, 3=Bachelor, 4=Master, 5=Doctor")
    education = int(input("  Niveau d'éducation (1-5): "))
    education_field = input("  Domaine (Life Sciences/Medical/Marketing/Technical Degree/Other): ")
    
    # Travail
    print(f"\n{Fore.YELLOW}💼 Informations Professionnelles:")
    department = input("  Département (Sales/Research & Development/Human Resources): ")
    job_role = input("  Poste (ex: Sales Executive, Research Scientist, Manager): ")
    job_level = int(input("  Niveau de poste (1-5): "))
    monthly_income = int(input("  Revenu mensuel ($): "))
    
    # Expérience
    print(f"\n{Fore.YELLOW}⏱️ Expérience:")
    total_working_years = int(input("  Années d'expérience totales: "))
    years_at_company = int(input("  Années dans l'entreprise: "))
    years_with_curr_manager = int(input("  Années avec le manager actuel: "))
    years_since_last_promotion = int(input("  Années depuis dernière promotion: "))
    num_companies_worked = int(input("  Nombre d'entreprises précédentes: "))
    
    # Conditions de travail
    print(f"\n{Fore.YELLOW}🏢 Conditions de Travail:")
    business_travel = input("  Voyages d'affaires (Non-Travel/Travel_Rarely/Travel_Frequently): ")
    percent_salary_hike = int(input("  Augmentation salariale (%) dernière année: "))
    stock_option_level = int(input("  Niveau d'options d'achat d'actions (0-3): "))
    training_times_last_year = int(input("  Formations suivies l'année dernière: "))
    
    # Satisfaction (1-4)
    print(f"\n{Fore.YELLOW}😊 Satisfaction (échelle 1-4):")
    environment_satisfaction = int(input("  Satisfaction environnement: "))
    job_satisfaction = int(input("  Satisfaction du travail: "))
    work_life_balance = int(input("  Équilibre vie pro/perso: "))
    job_involvement = int(input("  Implication dans le travail: "))
    
    # Performance
    print(f"\n{Fore.YELLOW}📊 Performance:")
    performance_rating = int(input("  Évaluation de performance (3-4): "))
    
    # Créer le dictionnaire
    employee_data = {
        'Age': age,
        'Gender': gender,
        'MaritalStatus': marital_status,
        'DistanceFromHome': distance_from_home,
        'Education': education,
        'EducationField': education_field,
        'Department': department,
        'JobRole': job_role,
        'JobLevel': job_level,
        'MonthlyIncome': monthly_income,
        'TotalWorkingYears': total_working_years,
        'YearsAtCompany': years_at_company,
        'YearsWithCurrManager': years_with_curr_manager,
        'YearsSinceLastPromotion': years_since_last_promotion,
        'NumCompaniesWorked': num_companies_worked,
        'BusinessTravel': business_travel,
        'PercentSalaryHike': percent_salary_hike,
        'StockOptionLevel': stock_option_level,
        'TrainingTimesLastYear': training_times_last_year,
        'EnvironmentSatisfaction': environment_satisfaction,
        'JobSatisfaction': job_satisfaction,
        'WorkLifeBalance': work_life_balance,
        'JobInvolvement': job_involvement,
        'PerformanceRating': performance_rating
    }
    
    return pd.DataFrame([employee_data])

def predict_attrition(model, employee_df):
    """Fait la prédiction et affiche les résultats"""
    
    # Prédiction
    prediction = model.predict(employee_df)[0]
    proba = model.predict_proba(employee_df)[0]
    
    # Probabilités
    proba_no = proba[0] * 100
    proba_yes = proba[1] * 100
    
    # Affichage des résultats
    print(f"\n{Fore.CYAN}{'='*60}")
    print(f"{Fore.CYAN}📊 RÉSULTATS DE LA PRÉDICTION")
    print(f"{Fore.CYAN}{'='*60}\n")
    
    if prediction == 1:
        print(f"{Fore.RED}⚠️  RISQUE D'ATTRITION: OUI")
        print(f"{Fore.RED}   L'employé risque de quitter l'entreprise!")
    else:
        print(f"{Fore.GREEN}✅ RISQUE D'ATTRITION: NON")
        print(f"{Fore.GREEN}   L'employé devrait rester dans l'entreprise.")
    
    print(f"\n{Fore.YELLOW}📈 Probabilités:")
    print(f"   • Reste dans l'entreprise: {Fore.GREEN}{proba_no:.2f}%")
    print(f"   • Quitte l'entreprise:     {Fore.RED}{proba_yes:.2f}%")
    
    # Recommandations
    print(f"\n{Fore.CYAN}💡 Recommandations:")
    if prediction == 1:
        if proba_yes > 70:
            print(f"{Fore.RED}   🔴 RISQUE ÉLEVÉ - Action immédiate requise!")
        elif proba_yes > 50:
            print(f"{Fore.YELLOW}   🟡 RISQUE MODÉRÉ - Surveillance recommandée")
        
        print(f"{Fore.CYAN}   Suggestions:")
        print(f"   • Organiser un entretien individuel")
        print(f"   • Évaluer les opportunités de promotion")
        print(f"   • Améliorer l'équilibre vie pro/perso")
        print(f"   • Proposer des formations supplémentaires")
    else:
        print(f"{Fore.GREEN}   ✅ Employé satisfait - Continuer le bon travail!")
    
    print(f"\n{Fore.CYAN}{'='*60}\n")

def main():
    """Fonction principale"""
    print(f"\n{Fore.MAGENTA}{'='*60}")
    print(f"{Fore.MAGENTA}🎯 SYSTÈME DE PRÉDICTION D'ATTRITION DES EMPLOYÉS")
    print(f"{Fore.MAGENTA}{'='*60}\n")
    
    # Charger le modèle
    model = load_model()
    if model is None:
        return
    
    while True:
        # Obtenir les données de l'employé
        employee_df = get_user_input()
        
        # Faire la prédiction
        predict_attrition(model, employee_df)
        
        # Demander si on continue
        continue_pred = input(f"{Fore.YELLOW}Faire une autre prédiction? (o/n): ").lower()
        if continue_pred != 'o':
            print(f"\n{Fore.MAGENTA}👋 Au revoir!\n")
            break

if __name__ == "__main__":
    main()
