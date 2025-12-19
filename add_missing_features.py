"""
Script pour ajouter les éléments manquants au notebook liverable_final.ipynb
"""
import json
import sys

def add_time_features_section(notebook_path):
    """
    Ajoute la section d'extraction des features temporelles au notebook
    """
    
    # Lire le notebook existant
    with open(notebook_path, 'r', encoding='utf-8') as f:
        notebook = json.load(f)
    
    # Cellule Markdown d'introduction
    markdown_cell = {
        "cell_type": "markdown",
        "id": "time-features-intro",
        "metadata": {},
        "source": [
            "---\n",
            "## 📊 Extraction et Analyse des Features Temporelles\n",
            "\n",
            "Les fichiers `in_time.csv` et `out_time.csv` contiennent les heures d'arrivée et de départ quotidiennes des employés. \n",
            "Nous allons extraire plusieurs **features importantes** :\n",
            "\n",
            "| Feature | Description | Impact Business |\n",
            "|---------|-------------|-----------------|\n",
            "| **AvgWorkingHours** | Moyenne des heures travaillées par jour | Indicateur de charge de travail |\n",
            "| **LateArrivals** | Nombre de retards (arrivée après 9h) | Signe de désengagement |\n",
            "| **AvgOvertime** | Moyenne des heures supplémentaires | Burnout potentiel |\n",
            "| **AbsenceRate** | Taux d'absence (%) | Désengagement |\n",
            "| **WorkHoursVariance** | Variance des heures de travail | Instabilité |\n",
            "\n",
            "### 🎯 Hypothèse :\n",
            "Les employés qui partent probablement :\n",
            "- Ont des heures irrégulières (variance élevée)\n",
            "- Font beaucoup d'heures supplémentaires (burnout)\n",
            "- Ont un taux d'absence élevé"
        ]
    }
    
    # Cellule de code pour extraire les features
    code_cell_extraction = {
        "cell_type": "code",
        "execution_count": None,
        "id": "extract-time-features",
        "metadata": {},
        "outputs": [],
        "source": [
            "# =========================================================\n",
            "# Extraction des Features Temporelles\n",
            "# =========================================================\n",
            "\n",
            "def extract_time_features():\n",
            '    """Extrait les features temporelles depuis in_time.csv et out_time.csv"""'\n",
            "    print(\"⏰ Extraction des features temporelles...\")\n",
            "    \n",
            "    # Charger les données temporelles\n",
            '    in_time = pd.read_csv("data/in_time.csv")\n',
            '    out_time = pd.read_csv("data/out_time.csv")\n',
            "    \n",
            "    # Identifier la colonne EmployeeID (première colonne)\n",
            "    employee_id_col = in_time.columns[0]\n",
            "    \n",
            "    # Extraire les colonnes de dates (toutes sauf la première)\n",
            "    date_columns = in_time.columns[1:]\n",
            "    \n",
            "    time_features = []\n",
            "    \n",
            "    for idx, row in in_time.iterrows():\n",
            "        employee_id = row[employee_id_col]\n",
            "        \n",
            "        # Récupérer les heures d'arrivée et de départ\n",
            "        in_times = row[date_columns]\n",
            "        out_times = out_time.iloc[idx][date_columns]\n",
            "        \n",
            "        # Convertir en datetime\n",
            "        in_times_dt = pd.to_datetime(in_times, errors='coerce')\n",
            "        out_times_dt = pd.to_datetime(out_times, errors='coerce')\n",
            "        \n",
            "        # Listes pour stocker les calculs du jour\n",
            "        working_hours = []\n",
            "        late_count = 0\n",
            "        overtime_hours = []\n",
            "        \n",
            "        for in_t, out_t in zip(in_times_dt, out_times_dt):\n",
            "            if pd.notna(in_t) and pd.notna(out_t):\n",
            "                # 1. Calcul des heures travaillées\n",
            "                hours = (out_t - in_t).total_seconds() / 3600\n",
            "                working_hours.append(hours)\n",
            "                \n",
            "                # 2. Retards (Arrivée après 09:00:00)\n",
            "                if in_t.hour > 9 or (in_t.hour == 9 and in_t.minute > 0):\n",
            "                    late_count += 1\n",
            "                \n",
            "                # 3. Heures supplémentaires (Seuil standard de 8h)\n",
            "                if hours > 8:\n",
            "                    overtime_hours.append(hours - 8)\n",
            "        \n",
            "        # Calculer les moyennes et agrégats\n",
            "        avg_working_hours = np.mean(working_hours) if working_hours else 8.0\n",
            "        avg_overtime = np.mean(overtime_hours) if overtime_hours else 0.0\n",
            "        absence_rate = (len(date_columns) - len(working_hours)) / len(date_columns) * 100\n",
            "        work_hours_variance = np.var(working_hours) if len(working_hours) > 1 else 0.0\n",
            "        \n",
            "        time_features.append({\n",
            "            'EmployeeID': employee_id,\n",
            "            'AvgWorkingHours': round(avg_working_hours, 2),\n",
            "            'LateArrivals': late_count,\n",
            "            'AvgOvertime': round(avg_overtime, 2),\n",
            "            'AbsenceRate': round(absence_rate, 2),\n",
            "            'WorkHoursVariance': round(work_hours_variance, 2)\n",
            "        })\n",
            "    \n",
            "    time_df = pd.DataFrame(time_features)\n",
            "    print(f\"✅ Features temporelles extraites pour {len(time_df)} employés\")\n",
            "    return time_df\n",
            "\n",
            "# Extraire les features\n",
            "time_features = extract_time_features()\n",
            "\n",
            "# Merger avec le DataFrame principal\n",
            "print(f\"\\n🔄 Avant merge: {df.shape[0]} lignes, {df.shape[1]} colonnes\")\n",
            "df = df.merge(time_features, on=\"EmployeeID\", how=\"left\")\n",
            "print(f\"✅ Après merge: {df.shape[0]} lignes, {df.shape[1]} colonnes\")\n",
            "\n",
            "# Afficher un aperçu\n",
            "print(\"\\n📋 Aperçu des nouvelles features:\")\n",
            "time_features.head()"
        ]
    }
    
    # Trouver l'index où insérer (après le nettoyage des données)
    # On cherche la cellule contenant "Suppression des colonnes inutiles"
    insert_index = None
    for i, cell in enumerate(notebook['cells']):
        if cell['cell_type'] == 'markdown':
            source = ''.join(cell.get('source', []))
            if 'Suppression des colonnes inutiles' in source or 'Encodage de la variable cible' in source:
                insert_index = i + 2  # Après la cellule de code correspondante
                break
    
    if insert_index is None:
        # Si on ne trouve pas, on insère après la section 6
        for i, cell in enumerate(notebook['cells']):
            if cell.get('id') == 'encode-target':
                insert_index = i + 1
                break
    
    if insert_index is None:
        insert_index = len(notebook['cells']) // 2  # Au milieu par défaut
    
    # Insérer les cellules
    notebook['cells'].insert(insert_index, markdown_cell)
    notebook['cells'].insert(insert_index + 1, code_cell_extraction)
    
    # Sauvegarder le notebook modifié
    with open(notebook_path, 'w', encoding='utf-8') as f:
        json.dump(notebook, f, indent=4, ensure_ascii=False)
    
    print(f"✅ Section des features temporelles ajoutée à l'index {insert_index}")
    return insert_index + 2

if __name__ == "__main__":
    notebook_path = "liverable_final.ipynb"
    add_time_features_section(notebook_path)
    print("\\n🎉 Modifications terminées!")
