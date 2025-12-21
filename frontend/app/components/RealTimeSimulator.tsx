'use client';

import React, { useState, useEffect, useCallback } from 'react';
import { usePrediction } from '../context/PredictionContext';

// API Configuration
const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000';

// Debounce hook pour éviter trop de requêtes
function useDebounce<T>(value: T, delay: number): T {
    const [debouncedValue, setDebouncedValue] = useState<T>(value);
    useEffect(() => {
        const handler = setTimeout(() => setDebouncedValue(value), delay);
        return () => clearTimeout(handler);
    }, [value, delay]);
    return debouncedValue;
}

export default function RealTimeSimulator() {
    const { formData } = usePrediction();
    const [localForm, setLocalForm] = useState({
        Age: 35,
        JobSatisfaction: 3,
        EnvironmentSatisfaction: 3,
        WorkLifeBalance: 3,
        YearsSinceLastPromotion: 2,
        MonthlyIncome: 5000,
        TotalWorkingYears: 10,
        YearsAtCompany: 5,
        // Variables temporelles (importantes selon notebook)
        AvgWorkingHours: 8.5,
        LateArrivals: 10,
        AvgOvertime: 0.5,
    });

    const [prediction, setPrediction] = useState<number | null>(null);
    const [isLoading, setIsLoading] = useState(false);

    // Sync avec le formulaire principal quand il change
    useEffect(() => {
        if (Object.keys(formData).length > 0) {
            setLocalForm(prev => ({
                ...prev,
                Age: formData.Age || prev.Age,
                JobSatisfaction: formData.JobSatisfaction || prev.JobSatisfaction,
                EnvironmentSatisfaction: formData.EnvironmentSatisfaction || prev.EnvironmentSatisfaction,
                WorkLifeBalance: formData.WorkLifeBalance || prev.WorkLifeBalance,
                YearsSinceLastPromotion: formData.YearsSinceLastPromotion || prev.YearsSinceLastPromotion,
                MonthlyIncome: formData.MonthlyIncome || prev.MonthlyIncome,
                TotalWorkingYears: formData.TotalWorkingYears || prev.TotalWorkingYears,
                YearsAtCompany: formData.YearsAtCompany || prev.YearsAtCompany,
            }));
        }
    }, [formData]);

    // Debounce les changements (attend 300ms après le dernier changement)
    const debouncedForm = useDebounce(localForm, 300);

    // Appel API automatique quand les valeurs changent
    useEffect(() => {
        const fetchPrediction = async () => {
            setIsLoading(true);
            try {
                // Construire les données complètes en fusionnant avec formData
                const fullData = {
                    ...formData,
                    ...debouncedForm,
                    // Valeurs par défaut si formData est vide
                    Gender: formData.Gender || 'Male',
                    MaritalStatus: formData.MaritalStatus || 'Single',
                    Department: formData.Department || 'Research & Development',
                    JobRole: formData.JobRole || 'Research Scientist',
                    JobLevel: formData.JobLevel || 2,
                    DistanceFromHome: formData.DistanceFromHome || 10,
                    BusinessTravel: formData.BusinessTravel || 'Travel_Rarely',
                    Education: formData.Education || 3,
                    EducationField: formData.EducationField || 'Life Sciences',
                    NumCompaniesWorked: formData.NumCompaniesWorked || 2,
                    YearsWithCurrManager: formData.YearsWithCurrManager || 3,
                    JobInvolvement: formData.JobInvolvement || 3,
                    PerformanceRating: formData.PerformanceRating || 3,
                    PercentSalaryHike: formData.PercentSalaryHike || 15,
                    StockOptionLevel: formData.StockOptionLevel || 1,
                    TrainingTimesLastYear: formData.TrainingTimesLastYear || 3,
                };

                const response = await fetch(`${API_URL}/predict`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(fullData),
                });
                const data = await response.json();
                setPrediction(data.probabilities?.leave || 0);
            } catch (error) {
                console.error('Simulation error:', error);
            } finally {
                setIsLoading(false);
            }
        };

        fetchPrediction();
    }, [debouncedForm, formData]);

    const handleChange = (name: string, value: number) => {
        setLocalForm(prev => ({ ...prev, [name]: value }));
    };

    const getRiskColor = (score: number) => {
        // Seuils adaptés pour Random Forest
        if (score > 40) return '#ef4444';  // Rouge - Élevé
        if (score > 25) return '#eab308';  // Jaune - Moyen
        return '#22c55e';                   // Vert - Faible
    };

    return (
        <div className="card mt-6 border-2 border-dashed border-zinc-700">
            <div className="flex items-center justify-between border-b border-zinc-800 pb-3 -mx-5 px-5 -mt-5 pt-4 mb-4">
                <div className="flex items-center gap-2">
                    <svg className="w-4 h-4 text-emerald-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                    </svg>
                    <h2 className="font-semibold text-white">Simulateur Temps Réel</h2>
                </div>
                <span className="text-xs text-emerald-400">⚡ Auto-update</span>
            </div>

            <div className="grid grid-cols-4 gap-4 mb-4">
                {/* Sliders pour les variables clés */}
                <div>
                    <label className="label flex justify-between">
                        <span>Âge</span>
                        <span className="text-emerald-400">{localForm.Age}</span>
                    </label>
                    <input
                        type="range"
                        min="18" max="60"
                        value={localForm.Age}
                        onChange={(e) => handleChange('Age', parseInt(e.target.value))}
                        className="w-full accent-emerald-500"
                    />
                </div>

                <div>
                    <label className="label flex justify-between">
                        <span>Satisfaction Job</span>
                        <span className="text-emerald-400">{localForm.JobSatisfaction}/4</span>
                    </label>
                    <input
                        type="range"
                        min="1" max="4"
                        value={localForm.JobSatisfaction}
                        onChange={(e) => handleChange('JobSatisfaction', parseInt(e.target.value))}
                        className="w-full accent-emerald-500"
                    />
                </div>

                <div>
                    <label className="label flex justify-between">
                        <span>Environnement</span>
                        <span className="text-emerald-400">{localForm.EnvironmentSatisfaction}/4</span>
                    </label>
                    <input
                        type="range"
                        min="1" max="4"
                        value={localForm.EnvironmentSatisfaction}
                        onChange={(e) => handleChange('EnvironmentSatisfaction', parseInt(e.target.value))}
                        className="w-full accent-emerald-500"
                    />
                </div>

                <div>
                    <label className="label flex justify-between">
                        <span>Équilibre Vie</span>
                        <span className="text-emerald-400">{localForm.WorkLifeBalance}/4</span>
                    </label>
                    <input
                        type="range"
                        min="1" max="4"
                        value={localForm.WorkLifeBalance}
                        onChange={(e) => handleChange('WorkLifeBalance', parseInt(e.target.value))}
                        className="w-full accent-emerald-500"
                    />
                </div>

                <div>
                    <label className="label flex justify-between">
                        <span>Années sans promo</span>
                        <span className="text-emerald-400">{localForm.YearsSinceLastPromotion}</span>
                    </label>
                    <input
                        type="range"
                        min="0" max="15"
                        value={localForm.YearsSinceLastPromotion}
                        onChange={(e) => handleChange('YearsSinceLastPromotion', parseInt(e.target.value))}
                        className="w-full accent-emerald-500"
                    />
                </div>

                <div>
                    <label className="label flex justify-between">
                        <span>Salaire ($)</span>
                        <span className="text-emerald-400">{localForm.MonthlyIncome.toLocaleString()}</span>
                    </label>
                    <input
                        type="range"
                        min="1000" max="20000" step="500"
                        value={localForm.MonthlyIncome}
                        onChange={(e) => handleChange('MonthlyIncome', parseInt(e.target.value))}
                        className="w-full accent-emerald-500"
                    />
                </div>

                <div>
                    <label className="label flex justify-between">
                        <span>Exp. Totale</span>
                        <span className="text-emerald-400">{localForm.TotalWorkingYears} ans</span>
                    </label>
                    <input
                        type="range"
                        min="0" max="40"
                        value={localForm.TotalWorkingYears}
                        onChange={(e) => handleChange('TotalWorkingYears', parseInt(e.target.value))}
                        className="w-full accent-emerald-500"
                    />
                </div>

                <div>
                    <label className="label flex justify-between">
                        <span>Ancienneté</span>
                        <span className="text-emerald-400">{localForm.YearsAtCompany} ans</span>
                    </label>
                    <input
                        type="range"
                        min="0" max="30"
                        value={localForm.YearsAtCompany}
                        onChange={(e) => handleChange('YearsAtCompany', parseInt(e.target.value))}
                        className="w-full accent-emerald-500"
                    />
                </div>

                {/* Section Temporelle - Working Hours */}
                <div className="col-span-4 border-t border-zinc-800 pt-3 mt-2">
                    <p className="text-xs text-orange-400 uppercase mb-3">⏰ Données Temporelles (facteurs clés)</p>
                </div>

                <div>
                    <label className="label flex justify-between">
                        <span>Heures/jour</span>
                        <span className="text-orange-400">{localForm.AvgWorkingHours}h</span>
                    </label>
                    <input
                        type="range"
                        min="6" max="14" step="0.5"
                        value={localForm.AvgWorkingHours}
                        onChange={(e) => handleChange('AvgWorkingHours', parseFloat(e.target.value))}
                        className="w-full accent-orange-500"
                    />
                    <div className="flex justify-between text-xs text-zinc-600 mt-0.5">
                        <span>6h (relax)</span>
                        <span>14h (burnout)</span>
                    </div>
                </div>

                <div>
                    <label className="label flex justify-between">
                        <span>Retards/an</span>
                        <span className="text-orange-400">{localForm.LateArrivals}</span>
                    </label>
                    <input
                        type="range"
                        min="0" max="50"
                        value={localForm.LateArrivals}
                        onChange={(e) => handleChange('LateArrivals', parseInt(e.target.value))}
                        className="w-full accent-orange-500"
                    />
                    <div className="flex justify-between text-xs text-zinc-600 mt-0.5">
                        <span>0 (ponctuel)</span>
                        <span>50+ (désengagé)</span>
                    </div>
                </div>

                <div>
                    <label className="label flex justify-between">
                        <span>Heures sup/jour</span>
                        <span className="text-orange-400">{localForm.AvgOvertime}h</span>
                    </label>
                    <input
                        type="range"
                        min="0" max="4" step="0.5"
                        value={localForm.AvgOvertime}
                        onChange={(e) => handleChange('AvgOvertime', parseFloat(e.target.value))}
                        className="w-full accent-orange-500"
                    />
                    <div className="flex justify-between text-xs text-zinc-600 mt-0.5">
                        <span>0 (équilibré)</span>
                        <span>4h+ (surcharge)</span>
                    </div>
                </div>
            </div>

            {/* Résultat en temps réel */}
            <div className="flex items-center justify-center gap-6 p-4 bg-zinc-900/50 rounded-lg">
                <div className="text-center">
                    <p className="text-xs text-zinc-500 uppercase mb-1">Risque de Départ</p>
                    <div className="flex items-center gap-2">
                        {isLoading ? (
                            <svg className="animate-spin h-6 w-6 text-emerald-400" fill="none" viewBox="0 0 24 24">
                                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
                            </svg>
                        ) : (
                            <span
                                className="text-4xl font-bold"
                                style={{ color: getRiskColor(prediction || 0) }}
                            >
                                {prediction?.toFixed(1)}%
                            </span>
                        )}
                    </div>
                </div>

                {/* Barre de progression */}
                <div className="flex-1 max-w-xs">
                    <div className="h-3 bg-zinc-800 rounded-full overflow-hidden">
                        <div
                            className="h-full rounded-full transition-all duration-500"
                            style={{
                                width: `${prediction || 0}%`,
                                backgroundColor: getRiskColor(prediction || 0)
                            }}
                        />
                    </div>
                    <div className="flex justify-between text-xs text-zinc-500 mt-1">
                        <span>Faible</span>
                        <span>Élevé</span>
                    </div>
                </div>
            </div>
        </div>
    );
}
