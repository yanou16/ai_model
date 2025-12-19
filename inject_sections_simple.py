#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import os

notebook_path = "liverable_final.ipynb"

print("Lecture du notebook...")
with open(notebook_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

print(f"Cellules actuelles: {len(nb['cells'])}")

# Trouver où insérer
insert_idx = None
for i, cell in enumerate(nb['cells']):
    source_text = ''.join(cell.get('source', []))
    if 'Encodage de la variable cible' in source_text or 'Encodage de l\'Attrition' in source_text:
        insert_idx = i + 1
        break

if insert_idx is None:
    insert_idx = len(nb['cells']) - 5

print(f"Insertion a l'index {insert_idx}")

# Cellule markdown
markdown_cell = {
    "cell_type": "markdown",
    "id": "bonus-time-features",
    "metadata": {},
    "source": [
        "---\\n",
        "## 📊 BONUS: Features Temporelles\\n",
        "\\n",
        "### 💡 5 Nouvelles Features\\n",
        "\\n",
        "| Feature | Description |\\n",
        "|---------|-------------|\\n",
        "| AvgWorkingHours | Moyenne heures/jour |\\n",
        "| LateArrivals | Nombre retards |\\n",
        "| AvgOvertime | Heures supplémentaires |\\n",
        "| AbsenceRate | Taux absence |\\n",
        "| WorkHoursVariance | Variance heures |"
    ]
}

# Cellule code extraction
code_cell = {
    "cell_type": "code",
    "execution_count": None,
    "id": "extract-time-features",
    "metadata": {},
    "outputs": [],
    "source": [
        "def extract_time_features():\\n",
        "    in_time = pd.read_csv('data/in_time.csv')\\n",
        "    out_time = pd.read_csv('data/out_time.csv')\\n",
        "    \\n",
        "    emp_col = in_time.columns[0]\\n",
        "    dates = in_time.columns[1:]\\n",
        "    features = []\\n",
        "    \\n",
        "    for idx, row in in_time.iterrows():\\n",
        "        emp_id = row[emp_col]\\n",
        "        in_dt = pd.to_datetime(row[dates], errors='coerce')\\n",
        "        out_dt = pd.to_datetime(out_time.iloc[idx][dates], errors='coerce')\\n",
        "        \\n",
        "        hours = []\\n",
        "        late = 0\\n",
        "        overtime = []\\n",
        "        \\n",
        "        for i, o in zip(in_dt, out_dt):\\n",
        "            if pd.notna(i) and pd.notna(o):\\n",
        "                h = (o - i).total_seconds() / 3600\\n",
        "                hours.append(h)\\n",
        "                if i.hour > 9 or (i.hour == 9 and i.minute > 0):\\n",
        "                    late += 1\\n",
        "                if h > 8:\\n",
        "                    overtime.append(h - 8)\\n",
        "        \\n",
        "        features.append({\\n",
        "            'EmployeeID': emp_id,\\n",
        "            'AvgWorkingHours': round(np.mean(hours) if hours else 8.0, 2),\\n",
        "            'LateArrivals': late,\\n",
        "            'AvgOvertime': round(np.mean(overtime) if overtime else 0.0, 2),\\n",
        "            'AbsenceRate': round((len(dates) - len(hours)) / len(dates) * 100, 2),\\n",
        "            'WorkHoursVariance': round(np.var(hours) if len(hours) > 1 else 0.0, 2)\\n",
        "        })\\n",
        "    \\n",
        "    return pd.DataFrame(features)\\n",
        "\\n",
        "time_feat = extract_time_features()\\n",
        "df = df.merge(time_feat, on='EmployeeID', how='left')\\n",
        "print(f'Features temporelles ajoutees: {df.shape}')\\n",
        "time_feat.head()"
    ]
}

# Cellule visualisation
viz_cell = {
    "cell_type": "code",
    "execution_count": None,
    "id": "viz-time-features",
    "metadata": {},
    "outputs": [],
    "source": [
        "if df['Attrition'].dtype == 'object':\\n",
        "    df['Attrition'] = df['Attrition'].map({'Yes': 1, 'No': 0})\\n",
        "\\n",
        "new_feat = ['AvgWorkingHours', 'LateArrivals', 'AvgOvertime', 'AbsenceRate', 'WorkHoursVariance']\\n",
        "\\n",
        "fig, axes = plt.subplots(2, 3, figsize=(18, 10))\\n",
        "fig.suptitle('Features Temporelles', fontsize=16)\\n",
        "\\n",
        "for i, feat in enumerate(new_feat):\\n",
        "    ax = axes[i//3, i%3]\\n",
        "    ax.hist(df[feat], bins=30, color='skyblue')\\n",
        "    ax.set_title(feat)\\n",
        "\\n",
        "ax = axes[1, 2]\\n",
        "corr = df[new_feat + ['Attrition']].corr()['Attrition'].drop('Attrition')\\n",
        "ax.barh(corr.index, corr.values)\\n",
        "ax.set_title('Correlation Attrition')\\n",
        "\\n",
        "plt.tight_layout()\\n",
        "plt.show()"
    ]
}

# Insertion
nb['cells'].insert(insert_idx, markdown_cell)
nb['cells'].insert(insert_idx + 1, code_cell)
nb['cells'].insert(insert_idx + 2, viz_cell)

print(f"Ajout de 3 cellules a l'index {insert_idx}")
print(f"Total cellules: {len(nb['cells'])}")

# Sauvegarde
with open(notebook_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=2, ensure_ascii=False)

print("TERMINE! Features temporelles ajoutees au notebook!")
