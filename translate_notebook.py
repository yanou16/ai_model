"""
Script pour traduire les cellules Markdown anglaises en français
dans le notebook data_cleaning.ipynb
"""

import json

# Dictionnaire de traductions (titres et phrases courantes)
TRANSLATIONS = {
    # Titres de sections
    "Train-test split": "Séparation Train/Test",
    "Drop useless columns": "Suppression des colonnes inutiles",
    "Merge the datasets": "Fusion des jeux de données",
    "Model Comparison Visualization": "Visualisation de la Comparaison des Modèles",
    "Train and Compare Multiple Models": "Entraînement et Comparaison de Plusieurs Modèles",
    "Feature Importance": "Importance des Variables",
    "Loading the Cleaned Dataset": "Chargement du Dataset Nettoyé",
    "Saving the Cleaned Dataset": "Sauvegarde du Dataset Nettoyé",
    "Exploratory Data Analysis": "Analyse Exploratoire des Données",
    "Correlation Heatmap": "Carte de Corrélation",
    "Getting Started": "Pour Commencer",
    "Learn More": "En Savoir Plus",
    "Optional": "Optionnel",
    
    # Phrases courantes
    "We will": "Nous allons",
    "This is": "Ceci est",
    "The following": "Le suivant",
    "Let's": "Nous allons",
    "Now we will": "Maintenant nous allons",
    "First, we": "D'abord, nous",
    "Next, we": "Ensuite, nous",
    "Finally, we": "Enfin, nous",
    "We can see that": "Nous pouvons voir que",
    "As we can see": "Comme nous pouvons le voir",
    "preprocessing pipeline": "pipeline de prétraitement",
    "create the preprocessing pipeline": "créer le pipeline de prétraitement",
    "key factors driving attrition": "facteurs clés influençant l'attrition",
    "Employees Leaving": "Employés Quittant l'Entreprise",
    "This is the most": "C'est le plus",
    "Categorical variable distributions": "Distributions des variables catégorielles",
    "show how employees": "montrent comment les employés",
    
    # Termes techniques (garder certains en anglais avec explication)
    "ColumnTransformer": "ColumnTransformer (Transformateur de Colonnes)",
    "OneHotEncoder": "OneHotEncoder (Encodage One-Hot)",
    "StandardScaler": "StandardScaler (Normalisation)",
    "Random Forest": "Random Forest (Forêt Aléatoire)",
    "Logistic Regression": "Régression Logistique",
    "Support Vector Machine": "Machine à Vecteurs de Support (SVM)",
    
    # Conclusions
    "Conclusion": "Conclusion",
    "Summary": "Résumé",
    "Results": "Résultats",
    "Analysis": "Analyse",
}

# Charger le notebook
with open('data_cleaning.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

translated_count = 0

for i, cell in enumerate(nb['cells']):
    if cell['cell_type'] == 'markdown':
        source = ''.join(cell['source'])
        original = source
        
        # Appliquer les traductions
        for eng, fra in TRANSLATIONS.items():
            if eng in source:
                source = source.replace(eng, fra)
        
        # Si du texte a été traduit
        if source != original:
            # Reconstruire le source comme liste de lignes
            lines = source.split('\n')
            cell['source'] = [line + '\n' if j < len(lines)-1 else line for j, line in enumerate(lines)]
            translated_count += 1
            print(f"✅ Cellule {i} traduite")

# Sauvegarder
with open('data_cleaning.ipynb', 'w', encoding='utf-8') as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)

print(f"\n🎉 Traduction terminée!")
print(f"   {translated_count} cellules traduites")
