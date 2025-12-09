import pandas as pd
import numpy as np
import pickle
import sys

def analyze_model():
    output = []
    output.append("🕵️‍♀️ Analyse du modèle et des données...")
    
    # 1. Charger les données pour voir la distribution
    output.append("\n1. Chargement des données...")
    try:
        general = pd.read_csv("data/general_data(1).csv")
        dist = general['Attrition'].value_counts(normalize=True)
        output.append(f"Distribution de la cible 'Attrition':\n{dist}")
    except Exception as e:
        output.append(f"Erreur chargement données: {str(e)}")
    
    # 2. Charger le modèle actuel
    output.append("\n2. Chargement du modèle...")
    try:
        with open('models/attrition_model.pkl', 'rb') as f:
            model = pickle.load(f)
            
        # 3. Vérifier les paramètres du Random Forest
        rf = model.named_steps['classifier']
        output.append("\n3. Paramètres du modèle actuel:")
        output.append(f"- Class Weight: {rf.class_weight}")
        output.append(f"- N Estimators: {rf.n_estimators}")
        output.append(f"- Max Depth: {rf.max_depth}")
        output.append(f"- Features total: {rf.n_features_in_}")

        # 4. Vérifier l'importance des features
        output.append("\n4. Top 15 Features les plus importantes:")
        
        preprocessor = model.named_steps['preprocessor']
        numeric_features = preprocessor.transformers_[0][2]
        importances = rf.feature_importances_
        
        # On suppose que les numériques sont les premières features
        # (c'est le cas si transformer 'num' est premier dans ColumnTransformer)
        num_len = len(numeric_features)
        
        # Créons un mapping approximatif
        # On va lister toutes les features numériques avec leur importance
        if num_len <= len(importances):
            num_importances = importances[:num_len]
            imp_df = pd.DataFrame({
                'Feature': numeric_features,
                'Importance': num_importances
            }).sort_values('Importance', ascending=False)
            
            output.append(imp_df.head(15).to_string())
            
            # Vérifier spécifiquement les features temporelles
            time_features = ['AvgWorkingHours', 'LateArrivals', 'AvgOvertime', 'AbsenceRate', 'WorkHoursVariance']
            output.append("\n\nImportance des features temporelles:")
            for feat in time_features:
                if feat in imp_df['Feature'].values:
                    val = imp_df[imp_df['Feature'] == feat]['Importance'].values[0]
                    output.append(f"- {feat}: {val:.6f}")
                else:
                    output.append(f"- {feat}: NON TROUVÉ")
                    
    except Exception as e:
        output.append(f"Erreur modèle: {str(e)}")

    # Sauvegarder dans un fichier
    with open('analysis_report.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(output))
    
    print("Analyse terminée. Résultats sauvegardés dans analysis_report.txt")

if __name__ == "__main__":
    analyze_model()
