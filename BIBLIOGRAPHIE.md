# 📚 Bibliographie - Projet IA HumanForYou

Cette bibliographie regroupe l’ensemble des sources académiques, techniques et éthiques
ayant servi à construire, justifier et évaluer la démarche de prédiction d’attrition des
employés dans le cadre du projet IA HumanForYou.


## Prédiction d'Attrition des Employés

*Document réalisé dans le cadre du cours Intelligence Artificielle - PGE A3 FISE INFO*

---

## 1. Sources Méthodologiques et Théoriques

### Machine Learning - Fondamentaux

| Référence | Apport au projet |
|-----------|------------------|
| **Hastie, T., Tibshirani, R., & Friedman, J.** (2009). *The Elements of Statistical Learning*. Springer. | Base théorique pour la compréhension des algorithmes de classification supervisée. |
| **Bishop, C. M.** (2006). *Pattern Recognition and Machine Learning*. Springer. | Fondements du prétraitement des données et de l'évaluation des modèles. |

### Random Forest

| Référence | Apport au projet |
|-----------|------------------|
| **Breiman, L.** (2001). *Random Forests*. Machine Learning, 45(1), 5-32. | Article fondateur de l'algorithme Random Forest, choisi pour notre modèle final. Justifie les avantages en termes de robustesse et réduction de l'overfitting. |

### Explicabilité (SHAP)

| Référence | Apport au projet |
|-----------|------------------|
| **Lundberg, S. M., & Lee, S. I.** (2017). *A Unified Approach to Interpreting Model Predictions*. NeurIPS. | Base théorique pour l'implémentation des valeurs SHAP, permettant d'expliquer les prédictions du modèle aux RH. |
| **Molnar, C.** (2022). *Interpretable Machine Learning*. [interpretable-ml-book.org](https://christophm.github.io/interpretable-ml-book/) | Guide pratique pour l'interprétation des modèles ML, utilisé pour la visualisation des facteurs de risque. |

---

## 2. Sources Techniques

### Scikit-learn

| Référence | Apport au projet |
|-----------|------------------|
| **Pedregosa, F., et al.** (2011). *Scikit-learn: Machine Learning in Python*. JMLR, 12, 2825-2830. | Bibliothèque principale utilisée pour le prétraitement (StandardScaler, OneHotEncoder), l'entraînement (RandomForestClassifier) et l'évaluation des modèles. |
| **Documentation Scikit-learn**. [scikit-learn.org](https://scikit-learn.org/) | Référence pour l'implémentation du Pipeline et ColumnTransformer. |

### Flask & API

| Référence | Apport au projet |
|-----------|------------------|
| **Grinberg, M.** (2018). *Flask Web Development*. O'Reilly Media. | Guide pour la création de l'API REST de prédiction. |
| **Documentation Flask**. [flask.palletsprojects.com](https://flask.palletsprojects.com/) | Référence pour les endpoints POST et la gestion CORS. |

### Frontend - Next.js & React

| Référence | Apport au projet |
|-----------|------------------|
| **Documentation Next.js**. [nextjs.org/docs](https://nextjs.org/docs) | Framework utilisé pour le dashboard web interactif. |
| **Documentation Recharts**. [recharts.org](https://recharts.org/) | Bibliothèque de graphiques pour la visualisation des prédictions et SHAP. |

---

## 3. Sources Éthiques et Sociétales

| Référence | Apport au projet |
|-----------|------------------|
| **Commission Européenne** (2019). *Lignes directrices en matière d'éthique pour une IA digne de confiance*. [ec.europa.eu](https://ec.europa.eu/digital-single-market/en/news/ethics-guidelines-trustworthy-ai) | Cadre de référence pour les 7 exigences éthiques : autonomie humaine, robustesse, confidentialité, transparence, non-discrimination, bien-être sociétal, responsabilité. |
| **Barocas, S., & Selbst, A. D.** (2016). *Big Data's Disparate Impact*. California Law Review. | Sensibilisation aux biais potentiels dans les modèles prédictifs RH (genre, âge). |
| **CNIL** (2022). *Guide pratique RGPD*. [cnil.fr](https://www.cnil.fr/) | Conformité au règlement européen sur la protection des données personnelles des employés. |

---

## 4. Sources Spécifiques au Projet

### Dataset & Contexte

| Référence | Apport au projet |
|-----------|------------------|
| **Choudhary, V.** (2018). *HR Analytics Case Study*. Kaggle. [kaggle.com/vjchoudhary7/hr-analytics-case-study](https://www.kaggle.com/vjchoudhary7/hr-analytics-case-study) | Source du dataset original utilisé pour l'entraînement du modèle. |
| **IBM HR Analytics**. *Employee Attrition and Performance*. Kaggle. | Dataset similaire utilisé comme référence pour la validation des approches. |

### Études sur l'Attrition

| Référence | Apport au projet |
|-----------|------------------|
| **Hausknecht, J. P., & Trevor, C. O.** (2011). *Collective Turnover at the Group, Unit, and Organizational Levels*. Journal of Management. | Compréhension des facteurs organisationnels influençant le turnover. |
| **Holtom, B. C., et al.** (2008). *Turnover and Retention Research*. Academy of Management Annals. | Base théorique pour l'identification des variables clés (satisfaction, promotion, salaire). |

---

## 5. Outils et Technologies Utilisés

| Outil | Version | Usage |
|-------|---------|-------|
| Python | 3.11+ | Langage principal |
| Scikit-learn | 1.3+ | ML Pipeline |
| SHAP | 0.42+ | Explicabilité |
| Flask | 2.3+ | API Backend |
| Next.js | 15.0 | Frontend |
| Pandas | 2.0+ | Manipulation données |
| NumPy | 1.24+ | Calculs numériques |

---

## Licence et Droits d'Auteur

Toutes les sources citées sont utilisées dans un cadre académique conformément aux principes du *fair use*. Les datasets utilisés sont sous licence open-source (Kaggle Public Domain). Le code développé est original et les bibliothèques utilisées respectent leurs licences respectives (MIT, BSD, Apache 2.0).

---

*Document généré le 16 décembre 2025*
