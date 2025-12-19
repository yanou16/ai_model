"""
Script pour nettoyer les conflits Git dans le notebook data_cleaning.ipynb
en utilisant une approche texte brute
"""
import re

# Lire le fichier comme texte brut
with open('data_cleaning.ipynb', 'r', encoding='utf-8') as f:
    content = f.read()

print("📖 Fichier chargé")
print(f"   Taille: {len(content)} caractères")

# Compter les conflits
conflicts_count = content.count('<<<<<<< HEAD')
print(f"\n🔍 Conflits trouvés: {conflicts_count}")

# Nettoyer le premier conflit (lignes 366-370 : execution_count)
# On garde execution_count: 4 (séquentiel après cell 3)
print("\n🔧 Nettoyage du conflit 1 (execution_count)...")
pattern1 = r'<<<<<<< HEAD\s*\n\s*"execution_count": null,\s*\n=======\s*\n\s*"execution_count": 1,\s*\n>>>>>>> b30d25963bb3c4d106735f8bb9e4433455685870'
replacement1 = '"execution_count": 4,'
content = re.sub(pattern1, replacement1, content)

# Nettoyer le deuxième conflit (lignes 569-574 : message final)  
# On garde les deux messages combinés
print("🔧 Nettoyage du conflit 2 (messages finaux)...")
pattern2 = r'<<<<<<< HEAD\s*\n\s*"print\(\\\\"\\\\\\\\n✅ Features temporelles intégrées avec succès!\\\\"\),\\\\n",\s*\n\s*"print\(f\\\\"   Le DataFrame contient maintenant \{df\.shape\[1\]\} colonnes\\\\"\)"\s*\n=======\s*\n\s*"print\(\\\\"\\\\\\\\n✅ Analyse terminée avec succès !\\\\"\)"\s*\n>>>>>>> b30d25963bb3c4d106735f8bb9e4433455685870'
replacement2 = '"print(\\"\\\\n✅ Features temporelles intégrées avec succès!\\"),\\n",\n     "print(f\\"   Le DataFrame contient maintenant {df.shape[1]} colonnes\\")"'
content = re.sub(pattern2, replacement2, content, flags=re.MULTILINE)

# Approche plus simple : supprimer tous les marqueurs de conflit
# et garder uniquement le contenu entre HEAD et =======
print("\n🔧 Nettoyage des marqueurs restants...")

lines = content.split('\n')
cleaned_lines = []
skip_mode = False
in_conflict = False

for i, line in enumerate(lines):
    # Détecter les marqueurs
    if '<<<<<<< HEAD' in line:
        in_conflict = True
        continue
    elif '=======' in line and in_conflict:
        # Commencer à ignorer après le ======
        skip_mode = True
        continue
    elif '>>>>>>>' in line and in_conflict:
        # Fin du conflit
        in_conflict = False
        skip_mode = False
        continue
    
    # Garder les lignes en dehors des zones à ignorer
    if not skip_mode:
        cleaned_lines.append(line)

content = '\n'.join(cleaned_lines)

# Vérifier qu'on a bien nettoyé
remaining_conflicts = content.count('<<<<<<< HEAD')
print(f"\n✅ Conflits restants: {remaining_conflicts}")

# Sauvegarder le fichier nettoyé
with open('data_cleaning.ipynb', 'w', encoding='utf-8') as f:
    f.write(content)

print(f"\n✨ Notebook nettoyé avec succès!")
print(f"   Fichier sauvegardé: data_cleaning.ipynb")
