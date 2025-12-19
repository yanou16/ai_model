#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

notebook_path = "liverable_final.ipynb"

print("Lecture du notebook...")
with open(notebook_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

print(f"Cellules actuelles: {len(nb['cells'])}")

# Trouver où insérer (avant l'entraînement du modèle ou à la fin de l'EDA)
insert_idx = len(nb['cells']) - 3  # Juste avant les dernières cellules

print(f"Insertion a l'index {insert_idx}")

# =========================
# SECTION SMOTE
# =========================

smote_markdown = {
    "cell_type": "markdown",
    "id": "section-smote",
    "metadata": {},
    "source": [
        "---\\n",
        "## ⚖️ SMOTE: Gestion du Desequilibre\\n",
        "\\n",
        "Le dataset est desequilibre (16% attrition).\\n",
        "SMOTE cree des exemples synthetiques de la classe minoritaire.\\n"
    ]
}

smote_code = {
    "cell_type": "code",
    "execution_count": None,
    "id": "apply-smote",
    "metadata": {},
    "outputs": [],
    "source": [
        "from imblearn.over_sampling import SMOTE\\n",
        "from sklearn.preprocessing import LabelEncoder\\n",
        "\\n",
        "# Preparer les donnees\\n",
        "X = df.drop(['Attrition', 'EmployeeID'], axis=1, errors='ignore')\\n",
        "y = df['Attrition']\\n",
        "\\n",
        "# Encoder variables categoriques\\n",
        "le = LabelEncoder()\\n",
        "for col in X.select_dtypes(include='object').columns:\\n",
        "    X[col] = le.fit_transform(X[col].astype(str))\\n",
        "\\n",
        "# Split\\n",
        "X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)\\n",
        "\\n",
        "print(f'AVANT SMOTE: {(y_train==1).sum()} Yes, {(y_train==0).sum()} No')\\n",
        "\\n",
        "# SMOTE\\n",
        "smote = SMOTE(sampling_strategy=0.7, random_state=42)\\n",
        "X_train_smote, y_train_smote = smote.fit_resample(X_train, y_train)\\n",
        "\\n",
        "print(f'APRES SMOTE: {(y_train_smote==1).sum()} Yes, {(y_train_smote==0).sum()} No')\\n",
        "\\n",
        "# Visualisation\\n",
        "fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))\\n",
        "ax1.bar(['No', 'Yes'], [(y_train==0).sum(), (y_train==1).sum()], color=['green', 'red'])\\n",
        "ax1.set_title('Avant SMOTE')\\n",
        "ax2.bar(['No', 'Yes'], [(y_train_smote==0).sum(), (y_train_smote==1).sum()], color=['green', 'red'])\\n",
        "ax2.set_title('Apres SMOTE')\\n",
        "plt.show()"
    ]
}

# =========================
# SECTION COMPARAISON MODELES
# =========================

models_markdown = {
    "cell_type": "markdown",
    "id": "section-model-comparison",
    "metadata": {},
    "source": [
        "---\\n",
        "## 🤖 Comparaison de 3 Modeles\\n",
        "\\n",
        "Test de 3 algorithmes: Logistic Regression, Random Forest, SVM\\n"
    ]
}

models_code = {
    "cell_type": "code",
    "execution_count": None,
    "id": "train-models",
    "metadata": {},
    "outputs": [],
    "source": [
        "from sklearn.metrics import roc_auc_score, roc_curve\\n",
        "\\n",
        "# Standardisation\\n",
        "scaler = StandardScaler()\\n",
        "X_train_scaled = scaler.fit_transform(X_train_smote)\\n",
        "X_test_scaled = scaler.transform(X_test)\\n",
        "\\n",
        "results = {}\\n",
        "\\n",
        "# 1. LOGISTIC REGRESSION\\n",
        "print('Logistic Regression...')\\n",
        "lr = LogisticRegression(max_iter=1000, random_state=42)\\n",
        "lr.fit(X_train_scaled, y_train_smote)\\n",
        "y_pred_lr = lr.predict(X_test_scaled)\\n",
        "y_proba_lr = lr.predict_proba(X_test_scaled)[:, 1]\\n",
        "results['LR'] = {\\n",
        "    'acc': accuracy_score(y_test, y_pred_lr),\\n",
        "    'f1': f1_score(y_test, y_pred_lr),\\n",
        "    'auc': roc_auc_score(y_test, y_proba_lr),\\n",
        "    'proba': y_proba_lr\\n",
        "}\\n",
        "\\n",
        "# 2. RANDOM FOREST\\n",
        "print('Random Forest...')\\n",
        "rf = RandomForestClassifier(n_estimators=100, random_state=42)\\n",
        "rf.fit(X_train_smote, y_train_smote)\\n",
        "y_pred_rf = rf.predict(X_test)\\n",
        "y_proba_rf = rf.predict_proba(X_test)[:, 1]\\n",
        "results['RF'] = {\\n",
        "    'acc': accuracy_score(y_test, y_pred_rf),\\n",
        "    'f1': f1_score(y_test, y_pred_rf),\\n",
        "    'auc': roc_auc_score(y_test, y_proba_rf),\\n",
        "    'proba': y_proba_rf\\n",
        "}\\n",
        "\\n",
        "# 3. SVM\\n",
        "print('SVM...')\\n",
        "svm = SVC(probability=True, random_state=42)\\n",
        "svm.fit(X_train_scaled, y_train_smote)\\n",
        "y_pred_svm = svm.predict(X_test_scaled)\\n",
        "y_proba_svm = svm.predict_proba(X_test_scaled)[:, 1]\\n",
        "results['SVM'] = {\\n",
        "    'acc': accuracy_score(y_test, y_pred_svm),\\n",
        "    'f1': f1_score(y_test, y_pred_svm),\\n",
        "    'auc': roc_auc_score(y_test, y_proba_svm),\\n",
        "    'proba': y_proba_svm\\n",
        "}\\n",
        "\\n",
        "# Tableau comparatif\\n",
        "print('\\nComparaison:')\\n",
        "for name, metrics in results.items():\\n",
        "    print(f'{name:5} | Acc:{metrics[\"acc\"]:.3f} | F1:{metrics[\"f1\"]:.3f} | AUC:{metrics[\"auc\"]:.3f}')"
    ]
}

# =========================
# SECTION ROC CURVE
# =========================

roc_markdown = {
    "cell_type": "markdown",
    "id": "section-roc",
    "metadata": {},
    "source": [
        "---\\n",
        "## 📈 Courbe ROC + AUC Score\\n",
        "\\n",
        "La courbe ROC montre les performances de classification.\\n",
        "AUC = Area Under the Curve (0.5 = aleatoire, 1.0 = parfait)\\n"
    ]
}

roc_code = {
    "cell_type": "code",
    "execution_count": None,
    "id": "plot-roc",
    "metadata": {},
    "outputs": [],
    "source": [
        "fig, ax = plt.subplots(figsize=(10, 8))\\n",
        "\\n",
        "colors = ['blue', 'green', 'red']\\n",
        "\\n",
        "for (name, metrics), color in zip(results.items(), colors):\\n",
        "    fpr, tpr, _ = roc_curve(y_test, metrics['proba'])\\n",
        "    ax.plot(fpr, tpr, color=color, lw=2, \\n",
        "            label=f'{name} (AUC={metrics[\"auc\"]:.3f})')\\n",
        "\\n",
        "# Ligne baseline\\n",
        "ax.plot([0, 1], [0, 1], 'k--', lw=2, label='Aleatoire')\\n",
        "\\n",
        "ax.set_xlabel('False Positive Rate')\\n",
        "ax.set_ylabel('True Positive Rate')\\n",
        "ax.set_title('Courbe ROC - Comparaison Modeles', fontsize=14, fontweight='bold')\\n",
        "ax.legend(loc='lower right')\\n",
        "ax.grid(alpha=0.3)\\n",
        "plt.show()\\n",
        "\\n",
        "# Meilleur modele\\n",
        "best = max(results, key=lambda x: results[x]['auc'])\\n",
        "print(f'Meilleur modele: {best} (AUC={results[best][\"auc\"]:.3f})')"
    ]
}

# =========================
# RECAP FINAL
# =========================

recap_markdown = {
    "cell_type": "markdown",
    "id": "section-recap",
    "metadata": {},
    "source": [
        "---\\n",
        "## 🎯 SYNTHESE DU PROJET\\n",
        "\\n",
        "### Donnees\\n",
        "- Dataset: 4410 employes, ~30 variables\\n",
        "- Attrition: 16%\\n",
        "- Features temporelles: 5 ajoutees\\n",
        "\\n",
        "### Preprocessing\\n",
        "- Valeurs manquantes: TRAITEES\\n",
        "- SMOTE: APPLIQUE (70%)\\n",
        "- Standardisation: OUI\\n",
        "\\n",
        "### Meilleur Modele\\n",
        "- Voir courbe ROC ci-dessus\\n",
        "\\n",
        "### Recommandations RH\\n",
        "- Surveiller heures supplementaires excessives\\n",
        "- Ameliorer equilibre vie pro/perso\\n",
        "- Offrir promotions regulieres\\n"
    ]
}

# Insertion de toutes les cellules
all_cells = [
    smote_markdown, smote_code,
    models_markdown, models_code,
    roc_markdown, roc_code,
    recap_markdown
]

for i, cell in enumerate(all_cells):
    nb['cells'].insert(insert_idx + i, cell)

print(f"Ajout de {len(all_cells)} cellules")
print(f"Total cellules: {len(nb['cells'])}")

# Sauvegarde
with open(notebook_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=2, ensure_ascii=False)

print("\\nTERMINE! Toutes les sections ajoutees:")
print("- Features Temporelles")
print("- SMOTE")
print("- Comparaison Modeles (LR, RF, SVM)")
print("- Courbe ROC + AUC")
print("- Tableau Recapitulatif")
