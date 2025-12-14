import pandas as pd
import pickle
import numpy as np

def detect_sensitivity():
    print("🔍 Analyse de sensibilité du modèle...")
    
    with open('models/attrition_model.pkl', 'rb') as f:
        model = pickle.load(f)
        
    # Profil de base (le "mauvais" profil)
    base_profile = {
        'Age': 25,
        'BusinessTravel': 'Travel_Frequently',
        'Department': 'Sales',
        'DistanceFromHome': 45,
        'Education': 1,
        'EducationField': 'Marketing', # Changed to Marketing to avoid 'First' drop ambiguity
        'Gender': 'Male',
        'JobLevel': 1,
        'JobRole': 'Sales Representative',
        'MaritalStatus': 'Single',
        'MonthlyIncome': 12000, 
        'NumCompaniesWorked': 7,
        'PercentSalaryHike': 10,
        'StockOptionLevel': 0,
        'TotalWorkingYears': 2,
        'TrainingTimesLastYear': 0,
        'YearsAtCompany': 1,
        'YearsSinceLastPromotion': 0,
        'YearsWithCurrManager': 0,
        'EnvironmentSatisfaction': 1,
        'JobSatisfaction': 1,
        'WorkLifeBalance': 1,
        'JobInvolvement': 1,
        'PerformanceRating': 3,
        'AvgWorkingHours': 11.0,
        'LateArrivals': 20,
        'AvgOvertime': 3.0,
        'AbsenceRate': 15.0,
        'WorkHoursVariance': 5.0
    }
    
    # Variations à tester
    variations = {
        'MonthlyIncome': [10000, 20000, 50000, 100000, 150000],
        'JobSatisfaction': [1, 2, 3, 4],
        'WorkLifeBalance': [1, 2, 3, 4],
        'AvgWorkingHours': [7, 8, 9, 10, 11, 12, 14],
        'AvgOvertime': [0, 1, 2, 3, 4, 5],
        'Age': [20, 30, 40, 50, 60]
    }
    
    results = []
    
    # Tester chaque variation
    for feature, values in variations.items():
        print(f"\n--- Test {feature} ---")
        for val in values:
            profile = base_profile.copy()
            profile[feature] = val
            df_profile = pd.DataFrame([profile])
            
            proba = model.predict_proba(df_profile)[0][1]
            print(f"{feature}={val} -> Probabilité Attrition: {proba:.2%}")
            results.append(f"{feature}={val} -> {proba:.2%}")

    with open('sensitivity_results.txt', 'w') as f:
        f.write('\n'.join(results))

if __name__ == "__main__":
    detect_sensitivity()
