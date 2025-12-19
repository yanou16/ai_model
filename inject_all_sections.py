#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script pour ajouter TOUS les éléments manquants au notebook liverable_final.ipynb
Exécuter: python inject_all_sections.py
"""

import json
import os

def inject_all_sections():
    notebook_path = "liverable_final.ipynb"
    
    if not os.path.exists(notebook_path):
        print(f"❌ Erreur: {notebook_path} introuvable!")
        return
    
    print(f"📖 Lecture de {notebook_path}...")
    with open(notebook_path, 'r', encoding='utf-8') as f:
        nb = json.load(f)
    
    print(f"✅ Notebook chargé: {len(nb['cells'])} cellules actuelles")
    
    # Trouver l'index d'insertion (après l'encodage de la variable cible)
    insert_idx = None
    for i, cell in enumerate(nb['cells']):
        if cell.get('id') == 'encode-target' or 'Encodage de l\'Attrition' in ''.join(cell.get('source', [])):
            insert_idx = i + 1
            break
    
    if insert_idx is None:
        # Chercher après la section de nettoyage
        for i, cell in enumerate(nb['cells']):
            if 'Suppression des colonnes' in ''.join(cell.get('source', [])):
                insert_idx = i + 2
                break
    
    if insert_idx is None:
        insert_idx = len(nb['cells']) - 5  # Avant les dernières cellules
    
    print(f"📍 Insertion à l'index {insert_idx}")
    
    # ========== SECTION 1: FEATURES TEMPORELLES ==========
    sections = []
    
    # Markdown intro
    sections.append({
        "cell_type": "markdown",
        "id": "bonus-time-features",
        "metadata": {},
        "source": [
            "---\n",
            "## 📊 BONUS: Features Temporelles (in_time & out_time)\n",
            "\n",
            "### 🎯 Contexte\n",
            "Les fichiers `in_time.csv` et `out_time.csv` contiennent les **heures d'arrivée et de départ** quotidiennes.\n",
            "\n",
            "### 💡 5 Nouvelles Features Créées\n",
            "\n",
            "| Feature | Calcul | Impact Business |\n",
            "|---------|--------|----------------|\n",
            "| `AvgWorkingHours` | Moyenne heures/jour | Charge de travail |\n",
            "| `LateArrivals` | Nombre de retards (>9h) | Désengagement |\n",
            "| `AvgOvertime` | Moyenne heures sup (>8h) | **BURNOUT** 🔥 |\n",
            "| `AbsenceRate` | % jours absents | Désintérêt |\n",
            "| `WorkHoursVariance` | Variance heures | Instabilité |\n"
        ]
    })
    
    # Code extraction
    sections.append({
        "cell_type": "code",
        "execution_count": None,
        "id": "extract-time-feat",
        "metadata": {},
        "outputs": [],
        "source": [
            "# =========================================================\n",
            "# Extraction Features Temporelles\n",
            "# =========================================================\n",
            "\n",
            "def extract_time_features():\n",
            "    print(\"⏰ Extraction des features temporelles...\")\n",
            "    \n",
            "    in_time = pd.read_csv(\"data/in_time.csv\")\n",
            "    out_time = pd.read_csv(\"data/out_time.csv\")\n",
            "    \n",
            "    emp_col = in_time.columns[0]\n",
            "    dates = in_time.columns[1:]\n",
            "    \n",
            "    features = []\n",
            "    \n",
            "    for idx, row in in_time.iterrows():\n",
            "        emp_id = row[emp_col]\n",
            "        in_dt = pd.to_datetime(row[dates], errors='coerce')\n",
            "        out_dt = pd.to_datetime(out_time.iloc[idx][dates], errors='coerce')\n",
            "        \n",
            "        hours = []\n",
            "        late = 0\n",
            "        overtime = []\n",
            "        \n",
            "        for i, o in zip(in_dt, out_dt):\n",
            "            if pd.notna(i) and pd.notna(o):\n",
            "                h = (o - i).total_seconds() / 3600\n",
            "                hours.append(h)\n",
            "                if i.hour > 9 or (i.hour == 9 and i.minute > 0):\n",
            "                    late += 1\n",
            "                if h > 8:\n",
            "                    overtime.append(h - 8)\n",
            "        \n",
            "        features.append({\n",
            "            'EmployeeID': emp_id,\n",
            "            'AvgWorkingHours': round(np.mean(hours) if hours else 8.0, 2),\n",
            "            'LateArrivals': late,\n",
            "            'AvgOvertime': round(np.mean(overtime) if overtime else 0.0, 2),\n",
            "            'AbsenceRate': round((len(dates) - len(hours)) / len(dates) * 100, 2),\n",
            "            'WorkHoursVariance': round(np.var(hours) if len(hours) > 1 else 0.0, 2)\n",
            "        })\n",
            "    \n",
            "    return pd.DataFrame(features)\n",
            "\n",
            "# Extraction et merge\n",
            "time_feat = extract_time_features()\n",
            "print(f\"\\nAvant merge: {df.shape}\")\n",
            "df = df.merge(time_feat, on=\"EmployeeID\", how=\"left\")\n",
            "print(f\"Après merge: {df.shape}\")\n",
            "print(f\"✅ {len(time_feat)} employés traités\")\n",
            "\n",
            "time_feat.head()"
        ]
    })
    
    # Visualisation
    sections.append({
        "cell_type": "code",
        "execution_count": None,
        "id": "viz-time-feat",
        "metadata": {},
        "outputs": [],
        "source": [
            "# Encoder Attrition si nécessaire\n",
            "if df['Attrition'].dtype == 'object':\n",
            "    df['Attrition'] = df['Attrition'].map({'Yes': 1, 'No': 0})\n",
            "\n",
            "new_feat = ['AvgWorkingHours', 'LateArrivals', 'AvgOvertime', 'AbsenceRate', 'WorkHoursVariance']\n",
            "\n",
            "fig, axes = plt.subplots(2, 3, figsize=(18, 10))\n",
            "fig.suptitle('📊 Distribution Features Temporelles', fontsize=16, fontweight='bold')\n",
            "\n",
            "for i, feat in enumerate(new_feat):\n",
            "    ax = axes[i//3, i%3]\n",
            "    ax.hist(df[feat], bins=30, color='skyblue', edgecolor='black', alpha=0.7)\n",
            "    ax.axvline(df[feat].mean(), color='red', linestyle='--', \n",
            "               label=f\"Moy: {df[feat].mean():.2f}\")\n",
            "    ax.set_title(feat, fontweight='bold')\n",
            "    ax.legend()\n",
            "    ax.grid(alpha=0.3)\n",
            "\n",
            "# Corrélation\n",
            "ax = axes[1, 2]\n",
            "corr = df[new_feat + ['Attrition']].corr()['Attrition'].drop('Attrition').sort_values()\n",
            "ax.barh(corr.index, corr.values, color='teal')\n",
            "ax.set_title('Corrélation avec Attrition', fontweight='bold')\n",
            "ax.axvline(0, color='black', linewidth=1)\n",
            "\n",
            "plt.tight_layout()\n",
            "plt.show()\n",
            "\n",
            "# Stats comparatives\n",
            "print(\"\\n📊 Restés (0) vs Partis (1):\")\n",
            "print(\"-\" * 70)\n",
            "for f in new_feat:\n",
            "    m0 = df[df['Attrition']==0][f].mean()\n",
            "    m1 = df[df['Attrition']==1][f].mean()\n",
            "    print(f\"{f:20} | Restés: {m0:6.2f} | Partis: {m1:6.2f} | Diff: {m1-m0:+6.2f}\")"
        ]
    })
    
    # Insérer toutes les sections
    for i, section in enumerate(sections):
        nb['cells'].insert(insert_idx + i, section)
    
    print(f\"✅ {len(sections)} cellules ajoutées")
    print(f"📊 Total cellules: {len(nb['cells'])}")
    
    # Sauvegarder
    print(f"\n💾 Sauvegarde de {notebook_path}...")
    with open(notebook_path, 'w', encoding='utf-8') as f:
        json.dump(nb, f, indent=2, ensure_ascii=False)
    
    print("✅ TERMINÉ!")
    print("\n🎉 Notebook mis à jour avec succès!")
    print("📝 Ouvrez liverable_final.ipynb pour voir les modifications")

if __name__ == "__main__":
    inject_all_sections()
