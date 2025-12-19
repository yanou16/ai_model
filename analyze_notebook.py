"""
Script pour analyser la structure et la qualité du notebook data_cleaning.ipynb
"""
import json

# Charger le notebook
with open('data_cleaning.ipynb', 'r', encoding='utf-8') as f:
    notebook = json.load(f)

cells = notebook['cells']

print("="*70)
print("ANALYSE PROFESSIONNELLE DU NOTEBOOK data_cleaning.ipynb")
print("="*70)

# 1. Statistiques générales
print(f"\n📊 STATISTIQUES GÉNÉRALES:")
print(f"   - Total de cellules: {len(cells)}")
markdown_cells = [c for c in cells if c['cell_type'] == 'markdown']
code_cells = [c for c in cells if c['cell_type'] == 'code']
print(f"   - Cellules markdown (documentation): {len(markdown_cells)}")
print(f"   - Cellules code: {len(code_cells)}")
print(f"   - Ratio documentation/code: {len(markdown_cells)/len(code_cells):.2f}")

# 2. Structure du notebook (titres principaux)
print(f"\n📋 STRUCTURE DU NOTEBOOK (Sections principales):")
section_count = 0
for i, cell in enumerate(markdown_cells):
    source = ''.join(cell['source'])
    # Détecter les titres de niveau 1 et 2
    if source.startswith('# ') or source.startswith('## '):
        section_count += 1
        title = source.split('\n')[0].replace('#', '').strip()
        level = source.count('#', 0, 3)
        indent = '  ' * (level - 1)
        if len(title) > 60:
            title = title[:60] + '...'
        print(f"   {indent}→ {title}")
        if section_count >= 25:  # Limiter l'affichage
            print("   ... (plus de sections)")
            break

# 3. Vérifier les erreurs dans les cellules
print(f"\n🔍 VÉRIFICATION DES ERREURS:")
cells_with_errors = 0
error_details = []
for i, cell in enumerate(code_cells):
    if 'outputs' in cell:
        for output in cell['outputs']:
            if output.get('output_type') == 'error':
                cells_with_errors += 1
                error_type = output.get('ename', 'Unknown')
                error_msg = output.get('evalue', '')[:50]
                error_details.append(f"Cellule {i}: {error_type} - {error_msg}")
                break

if cells_with_errors == 0:
    print("   ✅ Aucune erreur détectée dans les outputs!")
else:
    print(f"   ⚠️  {cells_with_errors} cellule(s) avec des erreurs:")
    for detail in error_details[:5]:
        print(f"      - {detail}")

# 4. Vérifier la présence de sections importantes
print(f"\n📌 SECTIONS CRITIQUES (Présence):")
required_sections = {
    'import': False,
    'chargement': False,
    'nettoyage': False,
    'eda': False,
    'modèle': False,
    'évaluation': False,
}

all_text = ' '.join([''.join(c['source']).lower() for c in cells])

if 'import' in all_text:
    required_sections['import'] = True
if 'chargement' in all_text or 'load' in all_text:
    required_sections['chargement'] = True
if 'nettoyage' in all_text or 'cleaning' in all_text:
    required_sections['nettoyage'] = True
if 'eda' in all_text or 'exploratoire' in all_text or 'visualization' in all_text:
    required_sections['eda'] = True
if 'modèle' in all_text or 'model' in all_text or 'randomforest' in all_text:
    required_sections['modèle'] = True
if 'évaluation' in all_text or 'accuracy' in all_text or 'f1' in all_text:
    required_sections['évaluation'] = True

for section, present in required_sections.items():
    status = "✅" if present else "❌"
    print(f"   {status} {section.capitalize()}")

# 5. Visualisations
print(f"\n📊 VISUALISATIONS:")
viz_count = sum(1 for c in code_cells 
                if 'plt.' in ''.join(c.get('source', [])) 
                or 'sns.' in ''.join(c.get('source', [])))
print(f"   - Cellules avec visualisations: {viz_count}")

# 6. Verdict final
print(f"\n{'='*70}")
print("VERDICT PROFESSIONNEL")
print(f"{'='*70}")

score = 0
max_score = 6

# Critères de notation
if len(markdown_cells) >= 10:
    score += 1
    print("✅ Documentation suffisante")
else:
    print("⚠️  Documentation insuffisante")

if cells_with_errors == 0:
    score += 1
    print("✅ Aucune erreur")
else:
    print("❌ Erreurs présentes")

if all(required_sections.values()):
    score += 2
    print("✅ Toutes les sections critiques présentes")
else:
    missing = [k for k, v in required_sections.items() if not v]
    print(f"⚠️  Sections manquantes: {', '.join(missing)}")

if viz_count >= 5:
    score += 1
    print("✅ Visualisations suffisantes")
else:
    print("⚠️  Peu de visualisations")

if len(cells) >= 50:
    score += 1
    print("✅ Notebook complet et détaillé")

print(f"\n🎯 SCORE FINAL: {score}/{max_score}")
if score >= 5:
    print("   ⭐⭐⭐ EXCELLENT - Notebook professionnel!")
elif score >= 4:
    print("   ⭐⭐ BON - Quelques améliorations possibles")
else:
    print("   ⭐ ACCEPTABLE - Travail à compléter")
