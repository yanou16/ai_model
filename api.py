"""
🚀 API REST pour la Prédiction d'Attrition des Employés
Utilisation: python api.py
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import pickle
import os

app = Flask(__name__)
CORS(app)  # Permet les requêtes depuis le frontend

# Charger le modèle au démarrage
MODEL_PATH = 'models/attrition_model.pkl'
model = None

def load_model():
    """Charge le modèle entraîné"""
    global model
    if not os.path.exists(MODEL_PATH):
        print(f"❌ Erreur: Le modèle n'existe pas à {MODEL_PATH}")
        print("💡 Lancez d'abord: python train_model.py")
        return False
    
    with open(MODEL_PATH, 'rb') as f:
        model = pickle.load(f)
    
    print(f"✅ Modèle chargé avec succès!")
    return True

@app.route('/health', methods=['GET'])
def health_check():
    """Endpoint pour vérifier que l'API fonctionne"""
    return jsonify({
        'status': 'ok',
        'message': 'API de prédiction d\'attrition opérationnelle',
        'model_loaded': model is not None
    })

@app.route('/predict', methods=['POST'])
def predict():
    """
    Endpoint principal pour prédire l'attrition
    
    Exemple de requête JSON:
    {
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
    """
    
    if model is None:
        return jsonify({
            'error': 'Modèle non chargé',
            'message': 'Le modèle n\'a pas pu être chargé au démarrage'
        }), 500
    
    try:
        # Récupérer les données JSON
        data = request.get_json()
        
        if not data:
            return jsonify({
                'error': 'Données manquantes',
                'message': 'Veuillez fournir les données de l\'employé en JSON'
            }), 400
        
        # Valider les champs requis
        required_fields = [
            'Age', 'Gender', 'MaritalStatus', 'DistanceFromHome', 'Education',
            'EducationField', 'Department', 'JobRole', 'JobLevel', 'MonthlyIncome',
            'TotalWorkingYears', 'YearsAtCompany', 'YearsWithCurrManager',
            'YearsSinceLastPromotion', 'NumCompaniesWorked', 'BusinessTravel',
            'PercentSalaryHike', 'StockOptionLevel', 'TrainingTimesLastYear',
            'EnvironmentSatisfaction', 'JobSatisfaction', 'WorkLifeBalance',
            'JobInvolvement', 'PerformanceRating'
        ]
        
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return jsonify({
                'error': 'Champs manquants',
                'missing_fields': missing_fields
            }), 400
        
        # Ajouter les features temporelles optionnelles avec valeurs par défaut
        # Ces valeurs sont les médianes calculées sur le dataset d'entraînement
        optional_time_features = {
            'AvgWorkingHours': 8.5,
            'LateArrivals': 10,
            'AvgOvertime': 0.5,
            'AbsenceRate': 5.0,
            'WorkHoursVariance': 1.0
        }
        
        for feature, default_value in optional_time_features.items():
            if feature not in data:
                data[feature] = default_value
        
        # Créer un DataFrame avec les données
        employee_df = pd.DataFrame([data])
        
        # Faire la prédiction
        prediction = model.predict(employee_df)[0]
        proba = model.predict_proba(employee_df)[0]
        
        # Probabilités
        proba_no = float(proba[0] * 100)
        proba_yes = float(proba[1] * 100)
        
        # Déterminer le niveau de risque
        risk_level = 'low'
        if prediction == 1:
            if proba_yes > 70:
                risk_level = 'high'
            elif proba_yes > 50:
                risk_level = 'medium'
        
        # Recommandations
        recommendations = []
        if prediction == 1:
            recommendations = [
                "Organiser un entretien individuel",
                "Évaluer les opportunités de promotion",
                "Améliorer l'équilibre vie pro/perso",
                "Proposer des formations supplémentaires"
            ]
        else:
            recommendations = ["Employé satisfait - Continuer le bon travail!"]
        
        # Réponse
        response = {
            'prediction': {
                'will_leave': bool(prediction == 1),
                'label': 'Oui' if prediction == 1 else 'Non'
            },
            'probabilities': {
                'stay': round(proba_no, 2),
                'leave': round(proba_yes, 2)
            },
            'risk_level': risk_level,
            'recommendations': recommendations,
            'employee_data': data
        }
        
        return jsonify(response), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Erreur lors de la prédiction',
            'message': str(e)
        }), 500

@app.route('/fields', methods=['GET'])
def get_fields():
    """Retourne la liste des champs requis et leurs valeurs possibles"""
    return jsonify({
        'required_fields': {
            'Age': {'type': 'integer', 'description': 'Âge de l\'employé'},
            'Gender': {'type': 'string', 'options': ['Male', 'Female']},
            'MaritalStatus': {'type': 'string', 'options': ['Single', 'Married', 'Divorced']},
            'DistanceFromHome': {'type': 'integer', 'description': 'Distance du domicile en km'},
            'Education': {'type': 'integer', 'min': 1, 'max': 5, 'description': '1=Below College, 2=College, 3=Bachelor, 4=Master, 5=Doctor'},
            'EducationField': {'type': 'string', 'options': ['Life Sciences', 'Medical', 'Marketing', 'Technical Degree', 'Other']},
            'Department': {'type': 'string', 'options': ['Sales', 'Research & Development', 'Human Resources']},
            'JobRole': {'type': 'string', 'description': 'Poste de l\'employé'},
            'JobLevel': {'type': 'integer', 'min': 1, 'max': 5},
            'MonthlyIncome': {'type': 'integer', 'description': 'Revenu mensuel en $'},
            'TotalWorkingYears': {'type': 'integer', 'description': 'Années d\'expérience totales'},
            'YearsAtCompany': {'type': 'integer', 'description': 'Années dans l\'entreprise'},
            'YearsWithCurrManager': {'type': 'integer', 'description': 'Années avec le manager actuel'},
            'YearsSinceLastPromotion': {'type': 'integer', 'description': 'Années depuis dernière promotion'},
            'NumCompaniesWorked': {'type': 'integer', 'description': 'Nombre d\'entreprises précédentes'},
            'BusinessTravel': {'type': 'string', 'options': ['Non-Travel', 'Travel_Rarely', 'Travel_Frequently']},
            'PercentSalaryHike': {'type': 'integer', 'description': 'Augmentation salariale (%) dernière année'},
            'StockOptionLevel': {'type': 'integer', 'min': 0, 'max': 3},
            'TrainingTimesLastYear': {'type': 'integer', 'description': 'Formations suivies l\'année dernière'},
            'EnvironmentSatisfaction': {'type': 'integer', 'min': 1, 'max': 4},
            'JobSatisfaction': {'type': 'integer', 'min': 1, 'max': 4},
            'WorkLifeBalance': {'type': 'integer', 'min': 1, 'max': 4},
            'JobInvolvement': {'type': 'integer', 'min': 1, 'max': 4},
            'PerformanceRating': {'type': 'integer', 'min': 3, 'max': 4}
        },
        'optional_fields': {
            'AvgWorkingHours': {'type': 'float', 'description': 'Heures moyennes travaillées par jour', 'default': 8.5},
            'LateArrivals': {'type': 'integer', 'description': 'Nombre de retards (arrivées après 9h)', 'default': 10},
            'AvgOvertime': {'type': 'float', 'description': 'Heures supplémentaires moyennes par jour', 'default': 0.5},
            'AbsenceRate': {'type': 'float', 'description': 'Taux d\'absence en %', 'default': 5.0},
            'WorkHoursVariance': {'type': 'float', 'description': 'Variance des heures de travail (régularité)', 'default': 1.0}
        }
    })

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🚀 API DE PRÉDICTION D'ATTRITION DES EMPLOYÉS")
    print("="*60 + "\n")
    
    # Charger le modèle
    if not load_model():
        print("\n⚠️  L'API va démarrer mais les prédictions ne fonctionneront pas.")
        print("   Entraînez d'abord le modèle avec: python train_model.py\n")
    
    print("\n📡 Endpoints disponibles:")
    print("   GET  /health  - Vérifier le statut de l'API")
    print("   GET  /fields  - Liste des champs requis")
    print("   POST /predict - Prédire l'attrition d'un employé")
    
    print("\n🌐 L'API démarre sur http://localhost:5000")
    print("="*60 + "\n")
    
    # Démarrer l'API
    app.run(debug=True, host='0.0.0.0', port=5000)
