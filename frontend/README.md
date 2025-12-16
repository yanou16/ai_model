# 🏢 HumanForYou - Dashboard de Prédiction d'Attrition

Interface web pour le modèle de prédiction d'attrition des employés de l'entreprise HumanForYou.

## 🚀 Démarrage

Lancer le serveur de développement :

```bash
npm run dev
```

Ouvrir [http://localhost:3000](http://localhost:3000) dans votre navigateur.

## 📋 Fonctionnalités

- **Formulaire de prédiction** : Saisie des 31 variables employé
- **Analyse de risque** : Probabilité de départ avec niveau (Faible/Moyen/Élevé)
- **Explainability SHAP** : Visualisation des facteurs influençant la prédiction
- **Simulateur temps réel** : Sliders pour tester différents scénarios instantanément
- **Chatbot RH** : Assistant IA pour questionner les résultats

## 🛠️ Technologies

- **Framework** : Next.js 15 (React)
- **Styling** : Tailwind CSS
- **Graphiques** : Recharts
- **API Backend** : Flask (Python)

## 📁 Structure

```
frontend/
├── app/
│   ├── page.tsx          # Dashboard principal
│   ├── components/       # Composants réutilisables
│   │   ├── Sidebar.tsx
│   │   └── RealTimeSimulator.tsx
│   └── context/          # État global React
│       └── PredictionContext.tsx
└── public/               # Assets statiques
```

## 🔗 API Backend

L'interface communique avec l'API Flask sur `http://localhost:5000` :
- `POST /predict` : Prédiction d'attrition
- `POST /chat` : Assistant RH
- `GET /health` : Status de l'API

---

*Projet IA - PGE A3 FISE INFO - Intelligence Artificielle*
