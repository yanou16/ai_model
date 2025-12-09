# Test de l'API avec les nouvelles features temporelles

import requests
import json

API_URL = "http://localhost:5000"

# Test 1: Requête SANS les nouvelles features (compatibilité backward)
print("=" * 60)
print("TEST 1: Requête sans features temporelles (backward compatibility)")
print("=" * 60)

employee_data_basic = {
    "Age": 35,
    "Gender": "Male",
    "MaritalStatus": "Married",
    "DistanceFromHome": 10,
    "Education": 3,
    "EducationField": "Life Sciences",
    "Department": "Research & Development",
    "JobRole": "Research Scientist",
    "JobLevel": 2,
    "MonthlyIncome": 5000,
    "TotalWorkingYears": 10,
    "YearsAtCompany": 5,
    "YearsWithCurrManager": 3,
    "YearsSinceLastPromotion": 1,
    "NumCompaniesWorked": 2,
    "BusinessTravel": "Travel_Rarely",
    "PercentSalaryHike": 15,
    "StockOptionLevel": 1,
    "TrainingTimesLastYear": 3,
    "EnvironmentSatisfaction": 3,
    "JobSatisfaction": 4,
    "WorkLifeBalance": 3,
    "JobInvolvement": 3,
    "PerformanceRating": 3
}

try:
    response = requests.post(f"{API_URL}/predict", json=employee_data_basic)
    if response.status_code == 200:
        result = response.json()
        print("✅ Succès!")
        print(f"   Prédiction: {result['prediction']['label']}")
        print(f"   Probabilité de partir: {result['probabilities']['leave']}%")
        print(f"   Niveau de risque: {result['risk_level']}")
    else:
        print(f"❌ Erreur: {response.status_code}")
        print(response.json())
except Exception as e:
    print(f"❌ Erreur de connexion: {e}")
    print("   Assurez-vous que l'API est démarrée (python api.py)")

# Test 2: Requête AVEC les nouvelles features
print("\n" + "=" * 60)
print("TEST 2: Requête avec features temporelles")
print("=" * 60)

employee_data_with_time = employee_data_basic.copy()
employee_data_with_time.update({
    "AvgWorkingHours": 9.5,  # Travaille beaucoup
    "LateArrivals": 25,       # Beaucoup de retards
    "AvgOvertime": 1.5,       # Heures sup importantes
    "AbsenceRate": 2.0,       # Peu d'absences
    "WorkHoursVariance": 2.5  # Horaires irréguliers
})

try:
    response = requests.post(f"{API_URL}/predict", json=employee_data_with_time)
    if response.status_code == 200:
        result = response.json()
        print("✅ Succès!")
        print(f"   Prédiction: {result['prediction']['label']}")
        print(f"   Probabilité de partir: {result['probabilities']['leave']}%")
        print(f"   Niveau de risque: {result['risk_level']}")
        print(f"   Recommandations: {result['recommendations']}")
    else:
        print(f"❌ Erreur: {response.status_code}")
        print(response.json())
except Exception as e:
    print(f"❌ Erreur de connexion: {e}")

# Test 3: Vérifier l'endpoint /fields
print("\n" + "=" * 60)
print("TEST 3: Vérification de l'endpoint /fields")
print("=" * 60)

try:
    response = requests.get(f"{API_URL}/fields")
    if response.status_code == 200:
        fields = response.json()
        print("✅ Succès!")
        print(f"   Champs requis: {len(fields.get('required_fields', {}))} champs")
        print(f"   Champs optionnels: {len(fields.get('optional_fields', {}))} champs")
        
        if 'optional_fields' in fields:
            print("\n   📋 Features temporelles optionnelles:")
            for field, info in fields['optional_fields'].items():
                print(f"      • {field}: {info['description']} (défaut: {info['default']})")
    else:
        print(f"❌ Erreur: {response.status_code}")
except Exception as e:
    print(f"❌ Erreur de connexion: {e}")

print("\n" + "=" * 60)
print("✅ Tests terminés!")
print("=" * 60)
