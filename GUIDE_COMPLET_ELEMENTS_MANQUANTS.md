# 📊 GUIDE COMPLET: Éléments Manquants dans liverable_final.ipynb

## 🎯 Vue d'Ensemble

Voici les **5 éléments majeurs** à ajouter à votre notebook final:

1. **Features Temporelles** (AvgWorkingHours, LateArrivals, etc.)
2. **SMOTE** (Gestion du déséquilibre des classes)
3. **Comparaison de Modèles** (Logistic Regression, Random Forest, SVM)
4. **Courbe ROC + AUC Score**
5. **Tableau Récapitulatif Final**

---

## 1️⃣ FEATURES TEMPORELLES

### 📝 Explication

Les fichiers `in_time.csv` et `out_time.csv` contiennent les heures d'arrivée/départ quotidiennes des employés.  
On va créer **5 nouvelles features** très pertinentes:

| Feature | Description | Pourquoi c'est important |
|---------|-------------|--------------------------|
| **AvgWorkingHours** | Moyenne des heures travaillées par jour | Mesure la charge de travail|
| **LateArrivals** | Nombre total de retards (arrivée après 9h) | Indicateur de désengagement |
| **AvgOvertime** | Moyenne des heures supplémentaires (> 8h) | **BURNOUT** 🔥 Principal prédicteur d'attrition |
| **AbsenceRate** | Pourcentage de jours absents | Signe de désintérêt |
| **WorkHoursVariance** | Variance des heures de travail | Instabilité/horaires chaotiques |

### 💡 Hypothèses Business

- ⚠️ **Beaucoup d'heures sup** → Burnout → L'employé part
- ⚠️ **Nombreux retards** → Désengagement → L'employé part  
- ⚠️ **Variance élevée** → Horaires instables → L'employé part

### 📋 Code à Ajouter (Section 7.5 - Après le nettoyage)

```python
# =========================================================
# SECTION BONUS: Extraction Features Temporelles
# =========================================================

def extract_time_features():
    """
    Extrait 5 features depuis les fichiers in_time.csv et out_time.csv
    
    Returns:
        DataFrame avec EmployeeID + 5 nouvelles colonnes
    """
    print("⏰ Extraction des features temporelles...")
    
    # Charger les données
    in_time = pd.read_csv("data/in_time.csv")
    out_time = pd.read_csv("data/out_time.csv")
    
    employee_id_col = in_time.columns[0]
    date_columns = in_time.columns[1:]  # Toutes les dates
    
    features_list = []
    
    for idx, row in in_time.iterrows():
        employee_id = row[employee_id_col]
        
        # Récupérer les heures d'arrivée et de départ
        in_times = row[date_columns]
        out_times = out_time.iloc[idx][date_columns]
        
        # Convertir en datetime
        in_dt = pd.to_datetime(in_times, errors='coerce')
        out_dt = pd.to_datetime(out_times, errors='coerce')
        
        # Variables de calcul
        hours_worked = []
        late_count = 0
        overtime = []
        
        for in_t, out_t in zip(in_dt, out_dt):
            if pd.notna(in_t) and pd.notna(out_t):
                # Calcul heures travaillées
                hours = (out_t - in_t).total_seconds() / 3600
                hours_worked.append(hours)
                
                # Retards (après 9h00)
                if in_t.hour > 9 or (in_t.hour == 9 and in_t.minute > 0):
                    late_count += 1
                
                # Heures supplémentaires (> 8h)
                if hours > 8:
                    overtime.append(hours - 8)
        
        # Créer le dictionnaire de features
        features_list.append({
            'EmployeeID': employee_id,
            'AvgWorkingHours': round(np.mean(hours_worked) if hours_worked else 8.0, 2),
            'LateArrivals': late_count,
            'AvgOvertime': round(np.mean(overtime) if overtime else 0.0, 2),
            'AbsenceRate': round((len(date_columns) - len(hours_worked)) / len(date_columns) * 100, 2),
            'WorkHoursVariance': round(np.var(hours_worked) if len(hours_worked) > 1 else 0.0, 2)
        })
    
    df_time = pd.DataFrame(features_list)
    print(f"✅ Features extraites pour {len(df_time)} employés")
    return df_time

# EXECUTION
time_features = extract_time_features()

# Merge avec le DataFrame principal
print(f"\nAvant merge: {df.shape}")
df = df.merge(time_features, on="EmployeeID", how="left")
print(f"Après merge: {df.shape}")

# Afficher un aperçu
time_features.head()
```

### 📊 Visualisation des Features Temporelles

```python
# S'assurer qu'Attrition est encodé en numérique
if df['Attrition'].dtype == 'object':
    df['Attrition'] = df['Attrition'].map({'Yes': 1, 'No': 0})

new_features = ['AvgWorkingHours', 'LateArrivals', 'AvgOvertime', 'AbsenceRate', 'WorkHoursVariance']

# Graphiques de distribution
fig, axes = plt.subplots(2, 3, figsize=(18, 10))
fig.suptitle('📊 Distribution des Features Temporelles', fontsize=16, fontweight='bold')

for i, feat in enumerate(new_features):
    ax = axes[i//3, i%3]
    ax.hist(df[feat], bins=30, color='skyblue', edgecolor='black', alpha=0.7)
    ax.axvline(df[feat].mean(), color='red', linestyle='--', 
               label=f"Moyenne: {df[feat].mean():.2f}")
    ax.set_title(feat)
    ax.set_xlabel(feat)
    ax.set_ylabel('Fréquence')
    ax.legend()
    ax.grid(alpha=0.3)

# Corrélation avec Attrition
ax = axes[1, 2]
corr = df[new_features + ['Attrition']].corr()['Attrition'].drop('Attrition').sort_values()
colors = ['red' if x < 0 else 'green' for x in corr.values]
ax.barh(corr.index, corr.values, color=colors, alpha=0.7)
ax.set_title('Corrélation avec Attrition', fontweight='bold')
ax.set_xlabel('Corrélation')
ax.axvline(0, color='black', linewidth=1)
ax.grid(alpha=0.3)

plt.tight_layout()
plt.show()

# Tableau comparatif Restés vs Partis
print("\n📊 Analyse Comparative: Employés Restés vs Partis")
print("=" * 75)
print(f"{'Feature':<20} | {'Restés (0)':<12} | {'Partis (1)':<12} | {'Différence':<12}")
print("-" * 75)

for feat in new_features:
    mean_stay = df[df['Attrition'] == 0][feat].mean()
    mean_left = df[df['Attrition'] == 1][feat].mean()
    diff = mean_left - mean_stay
    print(f"{feat:<20} | {mean_stay:>11.2f} | {mean_left:>11.2f} | {diff:>+11.2f}")

print("=" * 75)
```

### ✅ Résultat Attendu

- **AvgOvertime** : Les employés partis font significativement **plus d'heures sup**
- **LateArrivals** : Plus de retards chez ceux qui partent → désengagement
- **WorkHoursVariance** : Variance plus élevée → instabilité

---

## 2️⃣ SMOTE (Gestion du Déséquilibre)

### 📝 Explication

Le dataset est **déséquilibré** : seulement ~16% d'attrition (Yes).  
SMOTE = **Synthetic Minority Over-sampling Technique**  
→ Créé des exemples synthétiques de la classe minoritaire pour équilibrer

### 💡 Pourquoi c'est Important

Sans SMOTE, le modèle va avoir tendance à trop prédire "No" (classe majoritaire).  
Avec SMOTE, on améliore la détection des vrais cas d'attrition.

### 📋 Code à Ajouter (Juste avant l'entraînement du modèle)

```python
# =========================================================
# SMOTE: Gestion du Déséquilibre des Classes
# =========================================================

from imblearn.over_sampling import SMOTE

# Séparer features (X) et target (y)
X = df.drop(['Attrition', 'EmployeeID'], axis=1, errors='ignore')
y = df['Attrition']

# Encodage des variables catégorielles
le = LabelEncoder()
for col in X.select_dtypes(include='object').columns:
    X[col] = le.fit_transform(X[col].astype(str))

# Split Train/Test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# AVANT SMOTE
print("📊 Distribution AVANT SMOTE:")
print(f"  Classe 0 (No):  {(y_train == 0).sum()} ({(y_train == 0).sum() / len(y_train) * 100:.1f}%)")
print(f"  Classe 1 (Yes): {(y_train == 1).sum()} ({(y_train == 1).sum() / len(y_train) * 100:.1f}%)")

# Application de SMOTE
smote = SMOTE(sampling_strategy=0.7, random_state=42)  # 70% de la classe majoritaire
X_train_smote, y_train_smote = smote.fit_resample(X_train, y_train)

# APRÈS SMOTE
print("\n📊 Distribution APRÈS SMOTE:")
print(f"  Classe 0 (No):  {(y_train_smote == 0).sum()} ({(y_train_smote == 0).sum() / len(y_train_smote) * 100:.1f}%)")
print(f"  Classe 1 (Yes): {(y_train_smote == 1).sum()} ({(y_train_smote == 1).sum() / len(y_train_smote) * 100:.1f}%)")

# Visualisation
fig, axes = plt.subplots(1, 2, figsize=(12, 4))

axes[0].bar(['No', 'Yes'], [(y_train == 0).sum(), (y_train == 1).sum()], color=['green', 'red'])
axes[0].set_title('Avant SMOTE', fontweight='bold')
axes[0].set_ylabel('Nombre d\'employés')

axes[1].bar(['No', 'Yes'], [(y_train_smote == 0).sum(), (y_train_smote == 1).sum()], color=['green', 'red'])
axes[1].set_title('Après SMOTE', fontweight='bold')
axes[1].set_ylabel('Nombre d\'employés')

plt.tight_layout()
plt.show()
```

---

## 3️⃣ COMPARAISON DE MODÈLES

### 📝 Explication

On va tester **3 algorithmes** différents et comparer leurs performances:

1. **Logistic Regression** (Simple, interprétable)
2. **Random Forest** (Déjà dans le notebook, performances élevées)
3. **SVM** (Support Vector Machine, bon pour classification binaire)

### 📋 Code à Ajouter

```python
# =========================================================
# Comparaison de 3 Modèles de Classification
# =========================================================

from sklearn.metrics import roc_auc_score, roc_curve

# Standardisation (importante pour SVM et Logistic Regression)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train_smote)
X_test_scaled = scaler.transform(X_test)

# Dictionnaire pour stocker les résultats
results = {}

# -------------------- 1. LOGISTIC REGRESSION --------------------
print("🔹 Entraînement Logistic Regression...")
lr = LogisticRegression(max_iter=1000, random_state=42, class_weight='balanced')
lr.fit(X_train_scaled, y_train_smote)

y_pred_lr = lr.predict(X_test_scaled)
y_proba_lr = lr.predict_proba(X_test_scaled)[:, 1]

results['Logistic Regression'] = {
    'model': lr,
    'y_pred': y_pred_lr,
    'y_proba': y_proba_lr,
    'accuracy': accuracy_score(y_test, y_pred_lr),
    'precision': precision_score(y_test, y_pred_lr),
    'recall': recall_score(y_test, y_pred_lr),
    'f1': f1_score(y_test, y_pred_lr),
    'auc': roc_auc_score(y_test, y_proba_lr)
}

# -------------------- 2. RANDOM FOREST --------------------
print("🔹 Entraînement Random Forest...")
rf = RandomForestClassifier(n_estimators=100, random_state=42, class_weight='balanced')
rf.fit(X_train_smote, y_train_smote)

y_pred_rf = rf.predict(X_test)
y_proba_rf = rf.predict_proba(X_test)[:, 1]

results['Random Forest'] = {
    'model': rf,
    'y_pred': y_pred_rf,
    'y_proba': y_proba_rf,
    'accuracy': accuracy_score(y_test, y_pred_rf),
    'precision': precision_score(y_test, y_pred_rf),
    'recall': recall_score(y_test, y_pred_rf),
    'f1': f1_score(y_test, y_pred_rf),
    'auc': roc_auc_score(y_test, y_proba_rf)
}

# -------------------- 3. SVM --------------------
print("🔹 Entraînement SVM...")
svm = SVC(kernel='rbf', probability=True, random_state=42, class_weight='balanced')
svm.fit(X_train_scaled, y_train_smote)

y_pred_svm = svm.predict(X_test_scaled)
y_proba_svm = svm.predict_proba(X_test_scaled)[:, 1]

results['SVM'] = {
    'model': svm,
    'y_pred': y_pred_svm,
    'y_proba': y_proba_svm,
    'accuracy': accuracy_score(y_test, y_pred_svm),
    'precision': precision_score(y_test, y_pred_svm),
    'recall': recall_score(y_test, y_pred_svm),
    'f1': f1_score(y_test, y_pred_svm),
    'auc': roc_auc_score(y_test, y_proba_svm)
}

# -------------------- TABLEAU COMPARATIF --------------------
print("\n" + "="*80)
print("📊 TABLEAU COMPARATIF DES MODÈLES")
print("="*80)
print(f"{'Modèle':<20} | {'Accuracy':<10} | {'Precision':<10} | {'Recall':<10} | {'F1-Score':<10} | {'AUC':<10}")
print("-"*80)

for model_name, metrics in results.items():
    print(f"{model_name:<20} | {metrics['accuracy']:>9.3f} | {metrics['precision']:>9.3f} | "
          f"{metrics['recall']:>9.3f} | {metrics['f1']:>9.3f} | {metrics['auc']:>9.3f}")

print("="*80)

# Identifier le meilleur modèle (basé sur F1-Score)
best_model = max(results, key=lambda x: results[x]['f1'])
print(f"\n🏆 MEILLEUR MODÈLE: {best_model} (F1-Score = {results[best_model]['f1']:.3f})")
```

### 📊 Graphique Comparatif

```python
# Visualisation comparative
metrics_to_plot = ['accuracy', 'precision', 'recall', 'f1', 'auc']
model_names = list(results.keys())

fig, ax = plt.subplots(figsize=(14, 6))

x = np.arange(len(metrics_to_plot))
width = 0.25

for i, model_name in enumerate(model_names):
    values = [results[model_name][metric] for metric in metrics_to_plot]
    ax.bar(x + i*width, values, width, label=model_name, alpha=0.8)

ax.set_ylabel('Score', fontsize=12)
ax.set_title('Comparaison des Performances des Modèles', fontsize=14, fontweight='bold')
ax.set_xticks(x + width)
ax.set_xticklabels([m.capitalize() for m in metrics_to_plot])
ax.legend()
ax.grid(axis='y', alpha=0.3)
ax.set_ylim([0, 1])

plt.tight_layout()
plt.show()
```

---

## 4️⃣ COURBE ROC + AUC SCORE

### 📝 Explication

**ROC Curve** (Receiver Operating Characteristic):
- Montre le compromis entre **True Positive Rate** (Recall) et **False Positive Rate**
- Plus la courbe est proche du coin supérieur gauche, meilleur est le modèle

**AUC** (Area Under the Curve):
- Score entre 0 et 1
- **AUC = 0.5** → Modèle aléatoire (comme lancer une pièce)
- **AUC = 1.0** → Modèle parfait
- **AUC > 0.8** → Très bon modèle

### 📋 Code à Ajouter

```python
# =========================================================
# COURBE ROC + AUC SCORE
# =========================================================

fig, ax = plt.subplots(figsize=(10, 8))

colors = ['blue', 'green', 'red']

for (model_name, metrics), color in zip(results.items(), colors):
    # Calculer la courbe ROC
    fpr, tpr, thresholds = roc_curve(y_test, metrics['y_proba'])
    auc_score = metrics['auc']
    
    # Tracer la courbe
    ax.plot(fpr, tpr, color=color, lw=2, 
            label=f'{model_name} (AUC = {auc_score:.3f})')

# Ligne de référence (modèle aléatoire)
ax.plot([0, 1], [0, 1], 'k--', lw=2, label='Modèle Aléatoire (AUC = 0.500)')

# Configuration du graphique
ax.set_xlabel('False Positive Rate (1 - Spécificité)', fontsize=12)
ax.set_ylabel('True Positive Rate (Sensibilité / Recall)', fontsize=12)
ax.set_title('📈 Courbe ROC - Comparaison des Modèles', fontsize=14, fontweight='bold')
ax.legend(loc='lower right', fontsize=11)
ax.grid(alpha=0.3)
ax.set_xlim([0.0, 1.0])
ax.set_ylim([0.0, 1.05])

# Ajouter la zone optimale
ax.fill_between([0, 0, 1], [0, 1, 1], alpha=0.1, color='green', 
                 label='Zone Optimale')

plt.tight_layout()
plt.show()

# Interprétation
print("\n📊 INTERPRÉTATION DES RÉSULTATS:")
print("="*60)
for model_name, metrics in results.items():
    auc = metrics['auc']
    if auc >= 0.9:
        qualite = "🌟 EXCELLENT"
    elif auc >= 0.8:
        qualite = "✅ TRÈS BON"
    elif auc >= 0.7:
        qualite = "👍 BON"
    elif auc >= 0.6:
        qualite = "⚠️ MOYEN"
    else:
        qualite = "❌ FAIBLE"
    
    print(f"{model_name:<20} | AUC = {auc:.3f} | {qualite}")
print("="*60)
```

---

## 5️⃣ TABLEAU RÉCAPITULATIF FINAL

```python
# =========================================================
# SYNTHÈSE FINALE DU PROJET
# =========================================================

print("\n" + "="*80)
print(" "*25 + "📊 SYNTHÈSE DU PROJET" + " "*25)
print("="*80)

print("\n1️⃣ DONNÉES:")
print(f"   • Dataset fusionné: {df.shape[0]} employés, {df.shape[1]} variables")
print(f"   • Taux d'attrition: {df['Attrition'].mean()*100:.1f}%")
print(f"   • Features temporelles ajoutées: 5")

print("\n2️⃣ PRÉTRAITEMENT:")
print(f"   • Valeurs manquantes: TRAITÉES (médiane/mode)")
print(f"   • SMOTE appliqué: OUI (ratio 70%)")
print(f"   • Standardisation: OUI (pour LR et SVM)")

print("\n3️⃣ MODÈLES TESTÉS:")
best_auc = max([results[m]['auc'] for m in results])
for model_name in results:
    auc = results[model_name]['auc']
    marker = "🏆" if auc == best_auc else "  "
    print(f"   {marker} {model_name}: AUC = {auc:.3f}")

print("\n4️⃣ MEILLEUR MODÈLE:")
print(f"   • Algorithme: {best_model}")
print(f"   • AUC Score: {results[best_model]['auc']:.3f}")
print(f"   • F1-Score: {results[best_model]['f1']:.3f}")
print(f"   • Recall: {results[best_model]['recall']:.3f}")

print("\n5️⃣ FEATURES LES PLUS IMPORTANTES (Random Forest):")
if 'Random Forest' in results:
    importances = results['Random Forest']['model'].feature_importances_
    feature_names = X.columns
    top_features = sorted(zip(feature_names, importances), key=lambda x: x[1], reverse=True)[:5]
    for i, (feat, imp) in enumerate(top_features, 1):
        print(f"   {i}. {feat:<25} {imp:.4f}")

print("\n6️⃣ RECOMMANDATIONS BUSINESS:")
print("   ✅ Surveiller les employés avec beaucoup d'heures supplémentaires")
print("   ✅ Améliorer l'équilibre vie pro/perso (WorkLifeBalance)")
print("   ✅ Offrir des promotions régulières (YearsSinceLastPromotion)")
print("   ✅ Réduire la distance domicile-travail (télétravail)")

print("\n" + "="*80)
```

---

## 📝 INSTRUCTIONS D'INSTALLATION

Ajoutez ces cellules dans votre notebook dans cet ordre:

1. **Section 7.5** → Features Temporelles (après nettoyage données)
2. **Section 8** → SMOTE (juste avant entraînement modèle)
3. **Section 9** → Comparaison Modèles (remplacer l'entraînement actuel)
4. **Section 10** → Courbe ROC
5. **Section 11** → Tableau Récapitulatif

---

## ✅ CHECKLIST FINALE

- [ ] Features temporelles extraites et visualisées
- [ ] SMOTE appliqué sur données d'entraînement
- [ ] 3 modèles comparés (LR, RF, SVM)
- [ ] Courbe ROC tracée avec AUC pour chaque modèle
- [ ] Tableau récapitulatif ajouté
- [ ] Explications détaillées en Markdown
- [ ] Modèle sauvegardé avec joblib

---

🎉 **VOILÀ! Votre notebook est maintenant COMPLET et professionnel!**
