"""
🚀 API REST pour la Prédiction d'Attrition des Employés
Utilisation: python api.py
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import pickle
import os
import google.generativeai as genai
from groq import Groq
from dotenv import load_dotenv
import shap
import numpy as np

# Charger les variables d'environnement (.env)
load_dotenv()

# Configurer Gemini
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    try:
        genai.configure(api_key=GEMINI_API_KEY)
    except Exception as e:
        print(f"⚠️ Erreur config Gemini: {e}")
else:
    print("⚠️ Attention: GEMINI_API_KEY non trouvé dans les variables d'environnement.")

# Configurer Groq
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
groq_client = None
if GROQ_API_KEY:
    try:
        groq_client = Groq(api_key=GROQ_API_KEY)
    except Exception as e:
        print(f"⚠️ Erreur config Groq: {e}")
else:
    print("⚠️ Attention: GROQ_API_KEY non trouvé dans les variables d'environnement.")

app = Flask(__name__)
CORS(app)  # Permet les requêtes depuis le frontend

# Charger le modèle au démarrage
MODEL_PATH = 'models/attrition_model.pkl'
model = None
explainer = None
preprocessor = None
classifier = None

def load_model():
    """Charge le modèle entraîné"""
    global model, explainer, preprocessor, classifier
    if not os.path.exists(MODEL_PATH):
        print(f"❌ Erreur: Le modèle n'existe pas à {MODEL_PATH}")
        print("💡 Lancez d'abord: python train_model.py")
        return False
    
    with open(MODEL_PATH, 'rb') as f:
        model = pickle.load(f)

    # Initialiser SHAP Explainer
    try:
        print("🤔 Initialisation de SHAP Explainer...")
        # Check if model is a Pipeline
        if hasattr(model, 'named_steps'):
            preprocessor = model.named_steps['preprocessor']
            classifier = model.named_steps['classifier']
            explainer = shap.TreeExplainer(classifier)
            print(f"✅ SHAP Explainer prêt (sur Pipeline: {type(classifier).__name__}).")
        else:
            # Fallback for raw model
            explainer = shap.TreeExplainer(model)
            print("✅ SHAP Explainer prêt (sur Modèle brut).")
            
    except Exception as e:
        print(f"⚠️ Erreur init SHAP: {e}")
        explainer = None
    
    import time
    mod_time = os.path.getmtime(MODEL_PATH)
    time_str = time.ctime(mod_time)
    print(f"✅ Modèle chargé avec succès!")
    print(f"📅 Timestamp du modèle: {time_str}")
    print(f"☢️  VERSION: NUCLEAR (GradientBoosting)")
    return True

@app.route('/health', methods=['GET'])
def health_check():
    """Endpoint pour vérifier que l'API fonctionne"""
    return jsonify({
        'status': 'ok',
        'message': 'API de prédiction d\'attrition opérationnelle',
        'model_loaded': model is not None
    })

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

@app.route('/predict', methods=['POST'])
def predict():
    """Endpoint principal pour prédire l'attrition"""
    if model is None:
        return jsonify({
            'error': 'Modèle non chargé',
            'message': 'Le modèle n\'a pas pu être chargé au démarrage'
        }), 500
    
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Données manquantes', 'message': 'Veuillez fournir les données de l\'employé en JSON'}), 400
        
        # Ajouter les features temporelles optionnelles par défaut si manquantes
        optional_time_features = {
            'AvgWorkingHours': 8.5, 'LateArrivals': 10, 'AvgOvertime': 0.5,
            'AbsenceRate': 5.0, 'WorkHoursVariance': 1.0
        }
        for feature, default_value in optional_time_features.items():
            if feature not in data:
                data[feature] = default_value
        
        employee_df = pd.DataFrame([data])
        
        prediction = model.predict(employee_df)[0]
        proba = model.predict_proba(employee_df)[0]
        
        proba_no = float(proba[0] * 100)
        proba_yes = float(proba[1] * 100)
        
        risk_level = 'low'
        if prediction == 1:
            if proba_yes > 70: risk_level = 'high'
            elif proba_yes > 50: risk_level = 'medium'
        
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

        # 4. SHAP Explanation
        explanation_data = None
        if explainer and preprocessor is not None:
            try:
                # 1. Transform input data using the pipeline's preprocessor
                # SHAP needs the transformed numeric matrix that the model actually sees
                X_transformed = preprocessor.transform(employee_df)
                
                # 2. Variable names (need to retrieve feature names from OneHotEncoder)
                feature_names = []
                
                # Retrieve feature names from ColumnTransformer
                try:
                    feature_names = preprocessor.get_feature_names_out()
                except:
                    # Fallback
                    feature_names = [f"Feature {i}" for i in range(X_transformed.shape[1])]

                # 3. Calculate SHAP
                shap_valores = explainer.shap_values(X_transformed)
                
                # Handle binary classification
                vals = shap_valores
                if isinstance(shap_valores, list):
                    vals = shap_valores[1] # Class 1 = Yes
                elif len(np.array(shap_valores).shape) == 3: 
                    vals = np.array(shap_valores)[:,:,1]
                
                feature_values = vals[0] # Single sample
                
                # 4. Map back to JSON
                features_map = []
                for i, impact in enumerate(feature_values):
                    # Clean feature name
                    feat_name = str(feature_names[i])
                    features_map.append({
                        "feature": feat_name,
                        "impact": float(impact),
                        "value": "N/A"
                    })
                
                # Top Risk Factors
                risk_factors = sorted([f for f in features_map if f['impact'] > 0], key=lambda x: x['impact'], reverse=True)[:5]
                
                # Top Protective Factors
                protective_factors = sorted([f for f in features_map if f['impact'] < 0], key=lambda x: x['impact'])[:5]
                
                explanation_data = {
                    "risk_factors": risk_factors,
                    "protective_factors": protective_factors
                }
            except Exception as e:
                print(f"⚠️ SHAP Error during calculation: {e}")
                explanation_data = None
        
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
            'employee_data': data,
            'explainability': explanation_data
        }
        
        return jsonify(response), 200
        
    except Exception as e:
        return jsonify({'error': 'Erreur lors de la prédiction', 'message': str(e)}), 500

@app.route('/chat', methods=['POST'])
def chat():
    """Endpoint pour le chatbot (Gemini ou Groq)"""
    data = request.get_json()
    user_message = data.get('message', '')
    provider = data.get('provider', 'gemini') # 'gemini' or 'groq'
    
    if not user_message:
        return jsonify({'reply': "Je n'ai pas compris votre message."}), 400

    employee_context = ""
    employee_data = data.get('employee_data')
    prediction_result = data.get('prediction_result')

    if employee_data:
        employee_context += f"""
    CONTEXTE PROFIL EMPLOYÉ (Données du formulaire) :
    {employee_data}
    """

    if prediction_result:
        probabilities = prediction_result.get('probabilities', {})
        risk_level = prediction_result.get('risk_level', 'inconnu')
        employee_context += f"""
    RÉSULTAT DE LA PRÉDICTION ACTUELLE :
    - Risque d'Attrition : {risk_level.upper()}
    - Probabilité de Départ : {probabilities.get('leave', 0)}%
    
    Utilise ces pourcentages pour justifier tes conseils.
    """

    context = f"""
    Tu es un Expert RH Analytique intégré dans un Dashboard de Prédiction d'Attrition.
    Ton rôle est d'aider l'utilisateur à comprendre pourquoi un employé part, et à simuler des scénarios.

    Données du Modèle d'Attrition (Random Forest + SMOTE) :
    - Facteurs clés : TotalWorkingYears, Age, MonthlyIncome, YearsAtCompany, DistanceFromHome.

    {employee_context}

    Consignes :
    - Si une donnée contextuelle existe, utilise-la.
    - Sois concis, professionnel et direct.
    - Réponds en Français.
    """
    
    try:
        reply = ""
        
        if provider == 'groq':
            if not groq_client:
                 return jsonify({'reply': "⚠️ API Key Groq manquante. Configurez GROQ_API_KEY."}), 200
            
            print("🚀 Utilisation de Groq (Llama 3)...")
            chat_completion = groq_client.chat.completions.create(
                messages=[{'role': 'system', 'content': context}, {'role': 'user', 'content': user_message}],
                model="llama-3.3-70b-versatile",
            )
            reply = chat_completion.choices[0].message.content
            
        else: # Default to Gemini
            if not GEMINI_API_KEY:
                 return jsonify({'reply': "⚠️ API Key Gemini manquante."}), 200
                 
            print("✨ Utilisation de Gemini...")
            model = genai.GenerativeModel('gemini-robotics-er-1.5-preview')
            response = model.generate_content(f"{context}\n\nQuestion Utilisateur : {user_message}")
            reply = response.text

        return jsonify({'reply': reply})
        
    except Exception as e:
        error_msg = str(e)
        print(f"Erreur IA: {error_msg}")
        return jsonify({'reply': f"Erreur technique ({provider}) : {error_msg}"}), 200

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🚀 API DE PRÉDICTION D'ATTRITION DES EMPLOYÉS")
    print("="*60 + "\n")
    
    if not load_model():
        print("\n⚠️  L'API va démarrer mais les prédictions ne fonctionneront pas.")
    
    print("\n📡 Endpoints disponibles:")
    print("   GET  /health  - Vérifier le statut de l'API")
    print("   POST /predict - Prédire l'attrition")
    print("   POST /chat    - Discuter avec l'Assistant RH")
    
    print("\n🌐 L'API démarre sur http://localhost:5000")
    print("="*60 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
