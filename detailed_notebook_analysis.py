"""
Analyse détaillée du contenu professionnel du notebook
"""
import json

with open('data_cleaning.ipynb', 'r', encoding='utf-8') as f:
    notebook = json.load(f)

cells = notebook['cells']

print("="*80)
print("RAPPORT D'ANALYSE PROFESSIONNELLE - data_cleaning.ipynb")
print("="*80)

# Extraire toutes les sections markdown
sections_found = []
for cell in cells:
    if cell['cell_type'] == 'markdown':
        source = ''.join(cell['source'])
        lines = source.split('\n')
        for line in lines:
            if line.startswith('# ') or line.startswith('## ') or line.startswith('### '):
                title = line.strip('#').strip()
                if title and len(title) > 3:
                    level = line.count('#', 0, 4)
                    sections_found.append((level, title[:70]))

print(f"\n📚 TABLE DES MATIÈRES ({len(sections_found)} sections):")
print("-" * 80)
for i, (level, title) in enumerate(sections_found[:35]):
    indent = "  " * (level - 1)
    print(f"{indent}{'→' if level > 1 else '■'} {title}")
if len(sections_found) > 35:
    print(f"  ... et {len(sections_found) - 35} autres sections")

# Liste de vérification professionnelle
print(f"\n{'='*80}")
print("CHECKLIST PROFESSIONNELLE")
print("="*80)

all_content = ' '.join([''.join(c.get('source', [])).lower() for c in cells])

checklist = [
    ("Contexte business HumanForYou", "humanforyou" in all_content),
    ("Objectif du projet clair", "objectif" in all_content or "goal" in all_content),
    ("Imports et librairies", "import pandas" in all_content),
    ("Chargement des données", "read_csv" in all_content),
    ("Fusion des datasets", "merge" in all_content),
    ("Gestion valeurs manquantes", "fillna" in all_content or "dropna" in all_content),
    ("Suppression colonnes inutiles", "drop" in all_content),
    ("Feature engineering temporel", "in_time" in all_content or "avgworkinghours" in all_content),
    ("Analyse exploratoire (EDA)", ("plt." in all_content or "sns." in all_content) and "distribution" in all_content),
    ("Préparation modélisation", "train_test_split" in all_content),
    ("Régression Logistique", "logisticregression" in all_content),
    ("Random Forest", "randomforest" in all_content),
    ("SVM", "svc" in all_content or "svm" in all_content),
    ("GridSearch/RandomSearch", "gridsearch" in all_content or "randomizedsearch" in all_content),
    ("Métriques (Accuracy, F1...)", "accuracy" in all_content and "f1" in all_content),
    ("Classification Report", "classification_report" in all_content),
    ("Confusion Matrix", "confusion_matrix" in all_content),
    ("Feature Importance", "feature_importances" in all_content or "importance" in all_content),
    ("Analyse employés à risque", "risk" in all_content or "risque" in all_content),
    ("Recommandations business", "recommand" in all_content),
]

passed = 0
for item, check in checklist:
    status = "✅" if check else "❌"
    print(f"{status} {item}")
    if check:
        passed += 1

progress_percent = (passed / len(checklist)) * 100

# Visualisations
viz_keywords = ['plt.show', 'sns.', 'plt.figure', 'plt.subplot']
viz_count = sum(all_content.count(kw) for kw in viz_keywords)

print(f"\n{'='*80}")
print("QUALITÉ DU CONTENU")
print("="*80)
print(f"📊 Visualisations estimées: ~{viz_count // 2} graphiques")
print(f"📝 Documentation: {len([c for c in cells if c['cell_type'] == 'markdown'])} cellules markdown")
print(f"💻 Code: {len([c for c in cells if c['cell_type'] == 'code'])} cellules")

# Score final
print(f"\n{'='*80}")
print("ÉVALUATION FINALE")
print("="*80)
print(f"🎯 Complétude: {progress_percent:.1f}% ({passed}/{len(checklist)} critères)")

if progress_percent >= 90:
    grade = "⭐⭐⭐ EXCELLENT"
    comment = "Notebook très professionnel et complet!"
elif progress_percent >= 75:
    grade = "⭐⭐ TRÈS BON"
    comment = "Notebook de qualité, quelques éléments mineurs à ajouter"
elif progress_percent >= 60:
    grade = "⭐ BON"
    comment = "Notebook correct, quelques sections importantes manquent"
else:
    grade = "⚠️  À AMÉLIORER"
    comment = "Travail à compléter significativement"

print(f"\n{grade}")
print(f"💬 {comment}")

# Recommandations
print(f"\n{'='*80}")
print("RECOMMANDATIONS")
print("="*80)
missing_items = [item for item, check in checklist if not check]
if missing_items:
    print("Éléments à ajouter:")
    for item in missing_items[:5]:
        print(f"  - {item}")
    if len(missing_items) > 5:
        print(f"  ... et {len(missing_items) - 5} autres")
else:
    print("✅ Aucune recommandation - Le notebook est complet!")

print(f"\n{'='*80}")
ready = "OUI ✅" if progress_percent >= 75 else "NON ❌ (compléter d'abord)"
print(f"PRÊT POUR PRÉSENTATION / SOUTENANCE: {ready}")
print("="*80)
