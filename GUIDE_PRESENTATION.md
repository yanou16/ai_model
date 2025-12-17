# 📊 Guide Complet des Slides - Soutenance IA HumanForYou

**Durée totale : 20 minutes**

---

## SLIDE 1 - Titre (30 secondes)

### Contenu visuel :
```
🏢 PRÉDICTION D'ATTRITION DES EMPLOYÉS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Projet IA - HumanForYou

[Logo entreprise / École]

Présenté par : [Ton nom]
Date : Décembre 2025

PGE A3 FISE INFO - Intelligence Artificielle
```

### Ce que tu dois dire :
> "Bonjour, je vais vous présenter notre projet de prédiction d'attrition pour l'entreprise HumanForYou."

---

## SLIDE 2 - Contexte & Problématique (1 minute)

### Contenu visuel :
```
🏭 CONTEXTE

• Entreprise : HumanForYou (pharmaceutique, Inde)
• Effectif : ~4000 employés
• Problème : 15% de turnover annuel

⚠️ IMPACTS DU TURNOVER

┌─────────────────┬──────────────────────────────┐
│ Retards projets │ Réputation client dégradée   │
│ Coûts RH élevés │ Recrutement + Formation      │
│ Productivité ↓  │ Temps d'adaptation nouveaux  │
└─────────────────┴──────────────────────────────┘

🎯 OBJECTIF : Prédire quels employés vont partir
```

### Ce que tu dois dire :
> "HumanForYou est une entreprise pharmaceutique de 4000 employés en Inde. Chaque année, 15% des employés quittent l'entreprise, ce qui cause des retards sur les projets, des coûts de recrutement importants, et une perte de productivité. Notre objectif est de développer un modèle capable d'identifier les employés à risque de départ."

---

## SLIDE 3 - Données Disponibles (1 minute)

### Contenu visuel :
```
📁 DONNÉES FOURNIES PAR LES RH

┌────────────────────────┬─────────────────────────────┐
│ Fichier                │ Contenu                     │
├────────────────────────┼─────────────────────────────┤
│ general_data.csv       │ 24 variables RH générales   │
│                        │ (âge, salaire, ancienneté)  │
├────────────────────────┼─────────────────────────────┤
│ manager_survey_data.csv│ Évaluation par le manager   │
│                        │ (performance, implication)  │
├────────────────────────┼─────────────────────────────┤
│ employee_survey_data.csv│ Enquête satisfaction       │
│                        │ (environnement, équilibre)  │
├────────────────────────┼─────────────────────────────┤
│ in_time / out_time.csv │ Horaires badgeuse 2015      │
│                        │ (heures travail, retards)   │
└────────────────────────┴─────────────────────────────┘

📊 Total : ~4400 employés × 31 variables
```

### Ce que tu dois dire :
> "Nous avons reçu 4 fichiers CSV du service RH : les données générales des employés, l'évaluation des managers, une enquête de satisfaction, et les horaires de badgeuse. Au total, nous avons 31 variables pour environ 4400 employés."

---

## SLIDE 4 - Préparation des Données (1.5 minutes)

### Contenu visuel :
```
🔧 PRÉPARATION DES DONNÉES

1️⃣ FUSION DES DATASETS
   general + manager + employee + time → Dataset unifié

2️⃣ NETTOYAGE
   • Suppression colonnes inutiles (EmployeeCount, Over18)
   • Gestion des valeurs manquantes (NA)
   • Encodage variable cible (Attrition: Yes→1, No→0)

3️⃣ EXTRACTION FEATURES TEMPORELLES
   Depuis in_time et out_time :
   • AvgWorkingHours (heures moyennes/jour)
   • LateArrivals (nombre de retards)
   • AvgOvertime (heures supplémentaires)
   • AbsenceRate (taux d'absence)

[Screenshot du code de fusion]
```

### Ce que tu dois dire :
> "Nous avons fusionné les 4 fichiers sur l'EmployeeID, nettoyé les données en supprimant les colonnes inutiles et en gérant les valeurs manquantes. Nous avons aussi extrait des features temporelles depuis les fichiers d'horaires, comme les heures moyennes travaillées et le nombre de retards."

---

## SLIDE 5 - Dataset Final (30 secondes)

### Contenu visuel :
```
📋 DATASET FINAL : 31 VARIABLES

┌─────────────────────────────────────────────────────┐
│ CATÉGORIE          │ VARIABLES                      │
├────────────────────┼────────────────────────────────┤
│ Démographie        │ Age, Gender, MaritalStatus     │
│ Poste              │ Department, JobRole, JobLevel  │
│ Rémunération       │ MonthlyIncome, PercentSalaryHike│
│ Expérience         │ TotalWorkingYears, YearsAtCompany│
│ Satisfaction       │ JobSatisfaction, WorkLifeBalance│
│ Temporelles (NEW!) │ AvgWorkingHours, LateArrivals  │
└────────────────────┴────────────────────────────────┘

🎯 Variable cible : Attrition (Yes/No)
   Distribution : 84% No | 16% Yes (déséquilibré)
```

### Ce que tu dois dire :
> "Notre dataset final contient 31 variables réparties en plusieurs catégories. La variable cible est l'attrition, avec un déséquilibre important : seulement 16% des employés ont quitté l'entreprise."

---

## SLIDE 6 - Analyse Exploratoire EDA (2 minutes)

### Contenu visuel :
```
📊 ANALYSE EXPLORATOIRE

[Graphique 1: Distribution Attrition - Pie Chart]
   Yes: 16% | No: 84%

[Graphique 2: Heatmap Corrélations]
   Variables les plus corrélées à l'attrition

[Graphique 3: Boxplot salaire par attrition]
   Les employés qui partent ont un salaire plus bas
```

### Ce que tu dois dire :
> "L'analyse exploratoire nous montre que l'attrition est déséquilibrée avec 16% de Yes. La heatmap révèle les corrélations entre variables. On observe par exemple que les employés qui partent ont généralement un salaire plus bas et moins d'années dans l'entreprise."

---

## SLIDE 7 - Choix des Algorithmes (1.5 minutes)

### Contenu visuel :
```
🤖 ALGORITHMES TESTÉS

┌─────────────────────────────────────────────────────┐
│ MODÈLE                 │ TYPE                       │
├────────────────────────┼────────────────────────────┤
│ Régression Logistique  │ Linéaire, interprétable    │
│ Random Forest          │ Ensemble, robuste          │
│ SVM                    │ Kernel, frontières complexes│
└────────────────────────┴────────────────────────────┘

📋 PIPELINE DE PRÉTRAITEMENT

1. StandardScaler → Variables numériques (normalisation)
2. OneHotEncoder → Variables catégorielles (encodage)
3. Train/Test Split → 80% / 20% (stratifié)
```

### Ce que tu dois dire :
> "Nous avons testé 3 algorithmes de classification : la Régression Logistique pour sa simplicité, Random Forest pour sa robustesse, et SVM pour sa capacité à trouver des frontières complexes. Le prétraitement inclut une normalisation des variables numériques et un encodage one-hot des catégorielles."

---

## SLIDE 8 - Comparaison des Modèles (2 minutes)

### Contenu visuel :
```
📊 TABLEAU COMPARATIF DES PERFORMANCES

┌───────────────────┬──────────┬───────────┬────────┬──────────┬─────────┐
│ Modèle            │ Accuracy │ Precision │ Recall │ F1-Score │ AUC-ROC │
├───────────────────┼──────────┼───────────┼────────┼──────────┼─────────┤
│ Logistic Regression│   85%   │    60%    │  45%   │   52%    │  0.78   │
│ SVM               │   87%   │    65%    │  50%   │   56%    │  0.82   │
│ Random Forest ✅  │  97.8%  │    95%    │  98%   │   96%    │  0.99   │
└───────────────────┴──────────┴───────────┴────────┴──────────┴─────────┘

🎯 MEILLEUR MODÈLE : RANDOM FOREST

[Graphique barres comparant les 3 modèles]
```

### Ce que tu dois dire :
> "Voici la comparaison des performances. Random Forest surpasse largement les autres modèles avec 97.8% d'accuracy et surtout un recall de 98%, ce qui est crucial car on ne veut pas manquer les employés à risque. Le F1-score de 96% confirme un excellent équilibre."

---

## SLIDE 9 - Modèle Retenu : Random Forest (1 minute)

### Contenu visuel :
```
✅ POURQUOI RANDOM FOREST ?

┌─────────────────────────────────────────────────────┐
│ AVANTAGES                                           │
├─────────────────────────────────────────────────────┤
│ 🎯 Haute Accuracy (97.8%)                           │
│ 🔍 Recall élevé (98%) - Crucial pour les RH        │
│ 🛡️ Robuste à l'overfitting                         │
│ 📊 Feature Importance - Interprétable              │
│ ⚡ Rapide à entraîner                               │
└─────────────────────────────────────────────────────┘

💡 PRINCIPE : Moyenne de 200 arbres de décision
   → Réduit la variance et améliore la généralisation
```

### Ce que tu dois dire :
> "Nous avons retenu Random Forest pour plusieurs raisons : une accuracy de 97.8%, un recall de 98% crucial pour ne pas manquer les employés à risque, une robustesse à l'overfitting, et surtout la possibilité d'interpréter le modèle grâce au feature importance."

---

## SLIDE 10 - Overfitting & Hyperparamètres (1.5 minutes)

### Contenu visuel :
```
🔧 OPTIMISATION DU MODÈLE

⚠️ PROBLÈME : OVERFITTING
   Le modèle "mémorise" au lieu d'apprendre
   → Bonnes perfs train, mauvaises sur test

✅ SOLUTIONS RANDOM FOREST
   • Bagging : moyenne de 200 arbres
   • Feature sampling : variables aléatoires
   • Profondeur limitée : évite mémorisation

⚙️ HYPERPARAMÈTRES OPTIMISÉS
┌────────────────────┬─────────┬──────────────────────┐
│ Paramètre          │ Valeur  │ Effet                │
├────────────────────┼─────────┼──────────────────────┤
│ n_estimators       │ 200     │ Nombre d'arbres      │
│ max_depth          │ 10      │ Anti-overfitting     │
│ min_samples_split  │ 5       │ Régularisation       │
│ class_weight       │balanced │ Gère déséquilibre    │
└────────────────────┴─────────┴──────────────────────┘

📊 VALIDATION : Train 98% | Test 97.8% → Écart <1% ✅
```

### Ce que tu dois dire :
> "L'overfitting est un problème majeur en ML où le modèle mémorise au lieu d'apprendre. Random Forest le gère naturellement avec le bagging et le feature sampling. Nous avons optimisé les hyperparamètres : 200 arbres, profondeur max de 10, et un class_weight balanced pour gérer le déséquilibre des classes. L'écart train/test inférieur à 1% confirme qu'il n'y a pas d'overfitting."

---

## SLIDE 11 - Feature Importance (2 minutes)

### Contenu visuel :
```
🎯 VARIABLES LES PLUS INFLUENTES

[Graphique barres horizontales - Top 10 features]

1. YearsSinceLastPromotion ████████████████ 0.18
2. MonthlyIncome           ██████████████ 0.15
3. Age                     ████████████ 0.12
4. TotalWorkingYears       ██████████ 0.10
5. AvgWorkingHours         █████████ 0.09
6. JobSatisfaction         ████████ 0.08
7. WorkLifeBalance         ███████ 0.07
8. DistanceFromHome        ██████ 0.06
9. NumCompaniesWorked      █████ 0.05
10. EnvironmentSatisfaction ████ 0.04

💡 INSIGHT : Les promotions et le salaire sont les facteurs clés !
```

### Ce que tu dois dire :
> "Le feature importance de Random Forest révèle que les années depuis la dernière promotion est le facteur le plus influent, suivi du salaire et de l'âge. Les heures de travail que nous avons extraites des données de badgeuse apparaissent aussi comme un facteur significatif. Cette information est précieuse pour les RH."

---

## SLIDE 12 - SHAP Explainability (2 minutes)

### Contenu visuel :
```
🔍 EXPLICABILITÉ AVEC SHAP

POURQUOI SHAP ?
• Transparence des décisions (exigence éthique)
• Explication individuelle par employé
• Basé sur la théorie des jeux (valeurs de Shapley)

EXEMPLE - Employé à 45% de risque :

FACTEURS DE RISQUE (rouge) ────────────────────▶
████████████ YearsSincePromo = 8 ans (+15%)
█████████ JobSatisfaction = 1 (+12%)
██████ MonthlyIncome = 3000$ (+8%)

FACTEURS PROTECTEURS (vert) ◀──────────────────
████████ StockOptions = 2 (-10%)
█████ Experience = 15 ans (-8%)

[Screenshot du dashboard SHAP]
```

### Ce que tu dois dire :
> "Pour assurer la transparence, nous avons implémenté SHAP. Cette technique décompose chaque prédiction en contributions de chaque variable. Par exemple, pour un employé à 45% de risque, SHAP montre que son manque de promotion contribue à +15%, tandis que ses stock options réduisent le risque de 10%. Cela permet aux RH de savoir exactement quoi améliorer."

---

## SLIDE 13 - Interface Web Dashboard (2 minutes)

### Contenu visuel :
```
🖥️ DASHBOARD WEB DÉVELOPPÉ

[Screenshots ou démo live]

FONCTIONNALITÉS :
┌─────────────────────────────────────────────────────┐
│ 📝 Formulaire 31 variables                          │
│ 📊 Prédiction avec niveau de risque                 │
│ 🎚️ Simulateur temps réel (sliders)                  │
│ 📈 Graphique SHAP interactif                        │
│ 💬 Chatbot RH (Assistant IA)                        │
└─────────────────────────────────────────────────────┘

TECHNOLOGIES :
• Frontend : Next.js + React + Recharts
• Backend : Flask + Python
• ML : Scikit-learn + SHAP
```

### Ce que tu dois dire :
> "Nous avons développé un dashboard web complet. Il permet de saisir les données d'un employé, obtenir une prédiction avec le niveau de risque, visualiser les explications SHAP, et même simuler en temps réel l'impact des changements. Un chatbot RH est aussi intégré pour répondre aux questions."

---

## SLIDE 14 - Recommandations RH (2 minutes)

### Contenu visuel :
```
🎯 RECOMMANDATIONS POUR HUMANFORYOU

🔴 COURT TERME (0-3 mois)
• Déployer le dashboard pour identifier les employés à risque
• Organiser des entretiens individuels urgents
• Réviser les grilles salariales

🟡 MOYEN TERME (3-12 mois)
• Mettre en place un système d'alerte automatique
• Développer des parcours de carrière clairs
• Améliorer l'équilibre vie pro/perso

🟢 LONG TERME (1-3 ans)
• Réentraîner le modèle annuellement
• Objectif : Réduire attrition de 15% → 8%
• Intégrer enquêtes satisfaction régulières
```

### Ce que tu dois dire :
> "Nos recommandations pour HumanForYou se déclinent en 3 horizons. À court terme : déployer le dashboard et mener des entretiens urgents. À moyen terme : mettre en place des alertes automatiques et améliorer les parcours de carrière. À long terme : réentraîner le modèle régulièrement avec l'objectif de réduire l'attrition de 15% à 8%."

---

## SLIDE 15 - Conclusion (1 minute)

### Contenu visuel :
```
✅ LIVRABLES DU PROJET

┌─────────────────────────────────────────────────────┐
│ 📓 Notebook Jupyter complet (analyse + modélisation)│
│ 🔌 API Flask fonctionnelle                          │
│ 🖥️ Dashboard Web interactif                         │
│ 📚 Documentation (Bibliographie, Éthique)           │
└─────────────────────────────────────────────────────┘

🎯 RÉSULTATS CLÉS
• Modèle Random Forest : 97.8% accuracy
• Top facteurs : Promotion, Salaire, Age
• Interface déployable en production

💡 VALEUR AJOUTÉE
Permettre aux RH de passer d'une approche réactive
à une approche prédictive de la gestion des talents
```

### Ce que tu dois dire :
> "En conclusion, nous avons livré un notebook complet, une API Flask, un dashboard web interactif, et la documentation. Notre modèle Random Forest atteint 97.8% d'accuracy et permet aux RH de passer d'une approche réactive à une approche prédictive de la gestion des talents."

---

## SLIDE 16 - Questions (30 secondes)

### Contenu visuel :
```
❓ QUESTIONS ?

Merci pour votre attention !

───────────────────────────────────────

[Ton nom / Email]
[Lien GitHub si applicable]

───────────────────────────────────────

PGE A3 FISE INFO - Intelligence Artificielle
Décembre 2025
```

### Ce que tu dois dire :
> "Merci pour votre attention. Je suis maintenant disponible pour répondre à vos questions."

---

## 📋 RÉCAPITULATIF

| # | Slide | Durée |
|---|-------|-------|
| 1 | Titre | 30s |
| 2 | Contexte | 1 min |
| 3 | Données | 1 min |
| 4 | Préparation | 1.5 min |
| 5 | Dataset Final | 30s |
| 6 | EDA | 2 min |
| 7 | Choix Algorithmes | 1.5 min |
| 8 | Comparaison | 2 min |
| 9 | Random Forest | 1 min |
| 10 | Overfitting & Tuning | 1.5 min |
| 11 | Feature Importance | 2 min |
| 12 | SHAP | 2 min |
| 13 | Dashboard | 2 min |
| 14 | Recommandations | 2 min |
| 15 | Conclusion | 1 min |
| 16 | Questions | 30s |
| **TOTAL** | | **~20 min** |

---

## 💡 CONSEILS POUR LA SOUTENANCE

1. **Entraîne-toi** : Répète au moins 3 fois avec chrono
2. **Pas trop de texte** : 5-6 points max par slide
3. **Graphiques** : Montre les visuels du notebook
4. **Démo live** : Si possible, montre le dashboard en action
5. **Anticipe les questions** :
   - "Pourquoi Random Forest et pas XGBoost ?"
   - "Comment gérez-vous le déséquilibre des classes ?"
   - "Y a-t-il des biais dans le modèle ?"
   - "Comment le modèle sera-t-il mis à jour ?"

Bonne soutenance ! 🎓
