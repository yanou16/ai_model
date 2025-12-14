"""
🚀 Script d'Entraînement du Modèle d'Attrition
Utilisation: python train_model.py
"""

import pandas as pd
import numpy as np
import pickle
import os
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from imblearn.pipeline import Pipeline
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

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
    
    return time_df

def load_and_prepare_data():
    """Charge et prépare les données"""
    print("📂 Chargement des données...")
    
    # Charger les datasets
    general = pd.read_csv("data/general_data(1).csv")
    manager = pd.read_csv("data/manager_survey_data.csv")
    employee = pd.read_csv("data/employee_survey_data.csv")
    
    # Merger
    df = general.merge(manager, on="EmployeeID", how="left")
    df = df.merge(employee, on="EmployeeID", how="left")
    
    # Ajouter les features temporelles
    time_features = extract_time_features()
    df = df.merge(time_features, on="EmployeeID", how="left")
    
    return df

def clean_data(df):
    """Nettoie les données"""
    print("\n🧹 Nettoyage des données...")
    
    # Identifier colonnes numériques et catégorielles
    num_cols = df.select_dtypes(include=['int64','float64']).columns
    cat_cols = df.select_dtypes(include=['object']).columns
    
    # Remplir les valeurs manquantes
    df[num_cols] = df[num_cols].fillna(df[num_cols].median())
    df[cat_cols] = df[cat_cols].fillna(df[cat_cols].mode().iloc[0])
    
    # Supprimer colonnes inutiles
    df = df.drop(["EmployeeCount", "StandardHours", "Over18"], axis=1, errors='ignore')
    
    # Convertir Attrition en numérique
    df["Attrition"] = df["Attrition"].map({"Yes": 1, "No": 0})
    df["Attrition"] = df["Attrition"].astype(int)
    
    return df

def train_model(df):
    """Entraîne le modèle"""
    print("\n🤖 Entraînement du modèle...")
    
    # MANUEL OVERSAMPLING (Brutal but effective)
    print("   ⚠️ Application Oversampling Manuel (x4) sur la classe 'Yes'...")
    leavers = df[df['Attrition'] == 1]
    df = pd.concat([df, leavers, leavers, leavers], axis=0) # Duplicate 3 times -> Total 4x
    print(f"   Nouvelle taille du dataset: {df.shape}")

    # Séparer features et target
    X = df.drop(['Attrition', 'EmployeeID'], axis=1)
    y = df['Attrition']
    
    # Identifier colonnes
    numeric_features = X.select_dtypes(include=['int64', 'float64']).columns.tolist()
    categorical_features = X.select_dtypes(include=['object']).columns.tolist()
    
    # Split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # Créer le preprocessor
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), numeric_features),
            ('cat', OneHotEncoder(drop='first', handle_unknown='ignore'), categorical_features)
        ]
    )
    
    # Pipeline avec GradientBoosting
    model = Pipeline([
        ('preprocessor', preprocessor),
        ('classifier', GradientBoostingClassifier(
            n_estimators=300,
            learning_rate=0.1,
            max_depth=5,
            random_state=42
        ))
    ])
    
    # Entraîner
    print("\n⏳ Entraînement en cours...")
    model.fit(X_train, y_train)
    
    # Évaluer
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    
    print(f"\n✅ Modèle entraîné avec succès!")
    print(f"📊 Précision sur le test set: {accuracy:.2%}")
    
    print("\n📈 Rapport de classification:")
    print(classification_report(y_test, y_pred, target_names=['Reste', 'Quitte']))
    
    return model

def save_model(model):
    """Sauvegarde le modèle"""
    print("\n💾 Sauvegarde du modèle...")
    os.makedirs('models', exist_ok=True)
    model_path = 'models/attrition_model.pkl'
    with open(model_path, 'wb') as f:
        pickle.dump(model, f)
    print(f"✅ Modèle sauvegardé: {model_path}")

def main():
    """Fonction principale"""
    print("🚀 ENTRAÎNEMENT DU MODÈLE DE PRÉDICTION D'ATTRITION (Boosting)")
    
    # Charger et préparer
    df = load_and_prepare_data()
    df = clean_data(df)
    
    # Entraîner
    model = train_model(df)
    
    # Sauvegarder
    save_model(model)

if __name__ == "__main__":
    main()
