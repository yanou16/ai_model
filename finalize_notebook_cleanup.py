"""
Script pour finaliser le nettoyage du notebook:
1. Supprimer le code dupliqué (ligne 513)
2. Vider les outputs avec erreur
"""
import json

print("📖 Chargement du notebook...")
with open('data_cleaning.ipynb', 'r', encoding='utf-8') as f:
    notebook = json.load(f)

print(f"   {len(notebook['cells'])} cellules trouvées\n")

fixes_applied = 0

# Parcourir les cellules
for i, cell in enumerate(notebook['cells']):
    if cell['cell_type'] == 'code':
        source = cell.get('source', [])
        source_str = ''.join(source)
        
        # Vérifier si c'est la cellule avec le code dupliqué (contient extract_time_features)
        if 'extract_time_features' in source_str:
            print(f"🔍 Cellule {i} identifiée (extraction features temporelles)")
            
            # Supprimer la ligne dupliquée
            cleaned_source = []
            skip_next = False
            
            for j, line in enumerate(source):
                # Détecter le commentaire avant la duplication
                if "# Convertir Attrition en numérique pour les calculs (FIX)" in line:
                    skip_next = True  # Marquer pour skip
                    continue  # Ne pas ajouter cette ligne
                # Skip la ligne de duplication
                elif skip_next and "df['Attrition'] = df['Attrition'].map({'Yes': 1, 'No': 0})" in line:
                    skip_next = False  # Réinitialiser
                    continue # Ne pas ajouter cette ligne non plus
                else:
                    cleaned_source.append(line)
                    skip_next = False
            
            cell['source'] = cleaned_source
            fixes_applied += 1
            print(f"   ✅ Code dupliqué supprimé")
            
            # Vider les outputs avec erreur
            cell['outputs'] = []
            print(f"   ✅ Outputs avec erreur supprimés")

# Sauvegarder
print(f"\n💾 Sauvegarde du notebook...")
with open('data_cleaning.ipynb', 'w', encoding='utf-8') as f:
    json.dump(notebook, f, ensure_ascii=False, indent=1)

print(f"\n✨ Nettoyage finalisé!")
print(f"   {fixes_applied} corrections appliquées")
print(f"   Le notebook est maintenant propre et professionnel!")
print(f"\n📌 Note: Cette cellule devra être réexécutée APRÈS avoir exécuté")
print(f"   les cellules qui créent le DataFrame 'df'")
