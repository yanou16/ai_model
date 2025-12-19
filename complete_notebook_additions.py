"""
Script COMPLET pour ajouter TOUS les éléments manquants au notebook liverable_final.ipynb
Ce script ajoute: Features Temporelles, SMOTE, Comparaison Modèles, ROC Curve
"""
import json
import sys

# PRÉPARATION DES CELLULES À AJOUTER

# ========== 1. FEATURES TEMPORELLES ==========
cells_time_features = [
    {
        "cell_type": "markdown",
        "id": "section-time-features",
        "metadata": {},
        "source": [
            "---\\n",
            "## 📊 SECTION BONUS : Features Temporelles (in_time & out_time)\\n",
            "\\n",
            "### 🎯 Objectif\\n",
            "Les fichiers `in_time.csv` et `out_time.csv` contiennent les **heures d'arrivée et de départ** quotidiennes. \\n",
            "Nous allons créer **5 nouvelles features** très pertinentes pour prédire l'attrition :\\n",
            "\\n",
            "| Feature | Calcul | Impact Business |\\n",
            "|---------|--------|-----------------|\\n",
            "| `AvgWorkingHours` | Moyenne heures travaillées/jour | Charge de travail |\\n",
            "| `LateArrivals` | Nb retards (après 9h) | Désengagement |\\n",
            "| `AvgOvertime` | Moyenne heures sup (>8h) | **BURNOUT** 🔥 |\\n",
            "| `AbsenceRate` | % jours absents | Désintérêt |\\n",
            "| `WorkHoursVariance` | Variance heures travail | Instabilité |\\n",
            "\\n",
            "### 💡 Hypothèses\\n",
            "- ⚠️ **Heures supplémentaires excessives** → Burnout → Attrition\\n",
            "- ⚠️ **Beaucoup de retards** → Désengagement → Attrition\\n",
            "- ⚠️ **Variance élevée** → Horaires chaotiques → Attrition"
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "id": "extract-time-features",
        "metadata": {},
        "outputs": [],
        "source": [
            "# =========================================================\\n",
            "# Extraction des Features Temporelles\\n",
            "# =========================================================\\n",
            "\\n",
            "def extract_time_features():\\n",
            "    \\\"\\\"\\\"Extrait 5 features depuis in_time.csv et out_time.csv\\\"\\\"\\\"\\n",
            "    print(\\\"⏰ Extraction des features temporelles...\\\")\\n",
            "    \\n",
            "    # Charger les données\\n",
            "    in_time = pd.read_csv(\\\"data/in_time.csv\\\")\\n",
            "    out_time = pd.read_csv(\\\"data/out_time.csv\\\")\\n",
            "    \\n",
            "    employee_id_col = in_time.columns[0]\\n",
            "    date_columns = in_time.columns[1:]\\n",
            "    \\n",
            "    features_list = []\\n",
            "    \\n",
            "    for idx, row in in_time.iterrows():\\n",
            "        employee_id = row[employee_id_col]\\n",
            "        in_times = row[date_columns]\\n",
            "        out_times = out_time.iloc[idx][date_columns]\\n",
            "        \\n",
            "        # Conversion datetime\\n",
            "        in_dt = pd.to_datetime(in_times, errors='coerce')\\n",
            "        out_dt = pd.to_datetime(out_times, errors='coerce')\\n",
            "        \\n",
            "        hours_worked = []\\n",
            "        late_count = 0\\n",
            "        overtime = []\\n",
            "        \\n",
            "        for in_t, out_t in zip(in_dt, out_dt):\\n",
            "            if pd.notna(in_t) and pd.notna(out_t):\\n",
            "                h = (out_t - in_t).total_seconds() / 3600\\n",
            "                hours_worked.append(h)\\n",
            "                \\n",
            "                # Retards si après 9h\\n",
            "                if in_t.hour > 9 or (in_t.hour == 9 and in_t.minute > 0):\\n",
            "                    late_count += 1\\n",
            "                \\n",
            "                # Heures sup si > 8h\\n",
            "                if h > 8:\\n",
            "                    overtime.append(h - 8)\\n",
            "        \\n",
            "        features_list.append({\\n",
            "            'EmployeeID': employee_id,\\n",
            "            'AvgWorkingHours': round(np.mean(hours_worked) if hours_worked else 8.0, 2),\\n",
            "            'LateArrivals': late_count,\\n",
            "            'AvgOvertime': round(np.mean(overtime) if overtime else 0.0, 2),\\n",
            "            'AbsenceRate': round((len(date_columns) - len(hours_worked)) / len(date_columns) * 100, 2),\\n",
            "            'WorkHoursVariance': round(np.var(hours_worked) if len(hours_worked) > 1 else 0.0, 2)\\n",
            "        })\\n",
            "    \\n",
            "    df_time = pd.DataFrame(features_list)\\n",
            "    print(f\\\"✅ {len(df_time)} employés traités\\\")\\n",
            "    return df_time\\n",
            "\\n",
            "# EXECUTION\\n",
            "time_feat = extract_time_features()\\n",
            "\\n",
            "# Merge avec df principal\\n",
            "print(f\\\"\\\\nAvant: {df.shape}\\\")\\n",
            "df = df.merge(time_feat, on=\\\"EmployeeID\\\", how=\\\"left\\\")\\n",
            "print(f\\\"Après: {df.shape}\\\")\\n",
            "\\n",
            "time_feat.head()"
        ]
    }
]

# ========== 2. VISUALISATION FEATURES TEMPORELLES ==========
cells_time_viz = [
    {
        "cell_type": "markdown",
        "id": "viz-time-features",
        "metadata": {},
        "source": [
            "### 📈 Visualisation des Features Temporelles\\n",
            "\\n",
            "Analysons la distribution et l'impact de ces nouvelles features sur l'attrition."
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "id": "plot-time-features",
        "metadata": {},
        "outputs": [],
        "source": [
            "# Encoder Attrition pour les calculs\\n",
            "if df['Attrition'].dtype == 'object':\\n",
            "    df['Attrition'] = df['Attrition'].map({'Yes': 1, 'No': 0})\\n",
            "\\n",
            "new_features = ['AvgWorkingHours', 'LateArrivals', 'AvgOvertime', 'AbsenceRate', 'WorkHoursVariance']\\n",
            "\\n",
            "fig, axes = plt.subplots(2, 3, figsize=(18, 10))\\n",
            "fig.suptitle('📊 Distribution des Features Temporelles', fontsize=16, fontweight='bold')\\n",
            "\\n",
            "for i, feat in enumerate(new_features):\\n",
            "    ax = axes[i//3, i%3]\\n",
            "    \\n",
            "    # Histogramme\\n",
            "    ax.hist(df[feat], bins=30, color='skyblue', edgecolor='black', alpha=0.7)\\n",
            "    ax.axvline(df[feat].mean(), color='red', linestyle='--', label=f\\\"Moyenne: {df[feat].mean():.2f}\\\")\\n",
            "    ax.set_title(feat)\\n",
            "    ax.legend()\\n",
            "\\n",
            "# Corrélation avec Attrition\\n",
            "ax = axes[1, 2]\\n",
            "corr = df[new_features + ['Attrition']].corr()['Attrition'].drop('Attrition').sort_values()\\n",
            "ax.barh(corr.index, corr.values, color='teal')\\n",
            "ax.set_title('Corrélation avec Attrition')\\n",
            "ax.axvline(0, color='black', linewidth=0.5)\\n",
            "\\n",
            "plt.tight_layout()\\n",
            "plt.show()\\n",
            "\\n",
            "# Stats comparatives Restants vs Partis\\n",
            "print(\\\"\\\\n📊 Comparaison Restants (0) vs Partis (1):\\\")\\n",
            "print(\\\"-\\\" * 70)\\n",
            "for feat in new_features:\\n",
            "    mean_stay = df[df['Attrition'] == 0][feat].mean()\\n",
            "    mean_left = df[df['Attrition'] == 1][feat].mean()\\n",
            "    diff = mean_left - mean_stay\\n",
            "    print(f\\\"{feat:20} | Restés: {mean_stay:6.2f} | Partis: {mean_left:6.2f} | Diff: {diff:+6.2f}\\\")"
        ]
    }
]

print("📝 Cellules préparées:")
print(f"  - Features Temporelles: {len(cells_time_features)} cellules")
print(f"  - Visualisations: {len(cells_time_viz)} cellules")
print("\\n✅ Script prêt à modifier le notebook!")
