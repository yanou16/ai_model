'use client';

import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';

interface SimulatorProps {
    initialData: any;
}

export default function RealTimeSimulator({ initialData }: SimulatorProps) {
    // Top 5 Features to simulate
    const [params, setParams] = useState({
        Age: initialData?.Age || 30,
        MonthlyIncome: initialData?.MonthlyIncome || 5000,
        TotalWorkingYears: initialData?.TotalWorkingYears || 5,
        YearsAtCompany: initialData?.YearsAtCompany || 3,
        DistanceFromHome: initialData?.DistanceFromHome || 10
    });

    const [riskScore, setRiskScore] = useState<number | null>(null);
    const [isLoading, setIsLoading] = useState(false);

    // Debounce logic
    useEffect(() => {
        const timer = setTimeout(() => {
            fetchPrediction();
        }, 500); // Wait 500ms after last slide

        return () => clearTimeout(timer);
    }, [params]);

    const fetchPrediction = async () => {
        setIsLoading(true);
        try {
            // Merge simulated params with original data
            const payload = { ...initialData, ...params };

            const response = await fetch('http://localhost:5000/predict', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });
            const data = await response.json();
            setRiskScore(data.probabilities.leave);
        } catch (error) {
            console.error("Simulation error:", error);
        } finally {
            setIsLoading(false);
        }
    };

    const handleChange = (key: string, value: number) => {
        setParams(prev => ({ ...prev, [key]: value }));
    };

    // Color logic for the Gauge
    const getColor = (score: number) => {
        if (score < 30) return 'bg-green-500';
        if (score < 60) return 'bg-yellow-500';
        return 'bg-red-600';
    };

    return (
        <div className="bg-white dark:bg-gray-800 rounded-3xl shadow-xl p-8 border border-gray-100 dark:border-gray-700 mt-8">
            <h2 className="text-2xl font-bold mb-6 text-gray-800 dark:text-white flex items-center gap-2">
                🎛️ Simulateur Temps Réel
                <span className="text-xs font-normal px-2 py-1 bg-blue-100 text-blue-800 rounded-full">Beta</span>
            </h2>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-12">

                {/* Sliders Zone */}
                <div className="space-y-6">
                    {/* Age */}
                    <div>
                        <div className="flex justify-between mb-2">
                            <label className="text-sm font-medium text-gray-600 dark:text-gray-300">Âge</label>
                            <span className="font-bold text-blue-600">{params.Age} ans</span>
                        </div>
                        <input
                            type="range" min="18" max="60"
                            value={params.Age}
                            onChange={(e) => handleChange('Age', parseInt(e.target.value))}
                            className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-blue-600"
                        />
                    </div>

                    {/* Income */}
                    <div>
                        <div className="flex justify-between mb-2">
                            <label className="text-sm font-medium text-gray-600 dark:text-gray-300">Salaire Mensuel ($)</label>
                            <span className="font-bold text-blue-600">${params.MonthlyIncome}</span>
                        </div>
                        <input
                            type="range" min="1000" max="20000" step="500"
                            value={params.MonthlyIncome}
                            onChange={(e) => handleChange('MonthlyIncome', parseInt(e.target.value))}
                            className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-blue-600"
                        />
                    </div>

                    {/* Experience */}
                    <div>
                        <div className="flex justify-between mb-2">
                            <label className="text-sm font-medium text-gray-600 dark:text-gray-300">Expérience Totale</label>
                            <span className="font-bold text-blue-600">{params.TotalWorkingYears} ans</span>
                        </div>
                        <input
                            type="range" min="0" max="40"
                            value={params.TotalWorkingYears}
                            onChange={(e) => handleChange('TotalWorkingYears', parseInt(e.target.value))}
                            className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-blue-600"
                        />
                    </div>

                    {/* YearsAtCompany */}
                    <div>
                        <div className="flex justify-between mb-2">
                            <label className="text-sm font-medium text-gray-600 dark:text-gray-300">Ancienneté Entreprise</label>
                            <span className="font-bold text-blue-600">{params.YearsAtCompany} ans</span>
                        </div>
                        <input
                            type="range" min="0" max="20"
                            value={params.YearsAtCompany}
                            onChange={(e) => handleChange('YearsAtCompany', parseInt(e.target.value))}
                            className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-blue-600"
                        />
                    </div>

                    {/* Distance */}
                    <div>
                        <div className="flex justify-between mb-2">
                            <label className="text-sm font-medium text-gray-600 dark:text-gray-300">Distance Domicile</label>
                            <span className="font-bold text-blue-600">{params.DistanceFromHome} km</span>
                        </div>
                        <input
                            type="range" min="1" max="30"
                            value={params.DistanceFromHome}
                            onChange={(e) => handleChange('DistanceFromHome', parseInt(e.target.value))}
                            className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-blue-600"
                        />
                    </div>
                </div>

                {/* Gauge Zone */}
                <div className="flex flex-col items-center justify-center p-6 bg-gray-50 dark:bg-gray-900 rounded-2xl border border-gray-200 dark:border-gray-700 relative overflow-hidden">
                    <h3 className="text-lg font-semibold text-gray-500 uppercase tracking-widest mb-8">Risque Estimé</h3>

                    <div className="relative w-48 h-48 flex items-center justify-center">
                        {/* Circle Background */}
                        <svg className="w-full h-full transform -rotate-90">
                            <circle cx="96" cy="96" r="88" stroke="currentColor" strokeWidth="12" fill="transparent" className="text-gray-200 dark:text-gray-700" />
                            {/* Progress Circle */}
                            {riskScore !== null && (
                                <motion.circle
                                    initial={{ strokeDasharray: "0 1000" }}
                                    animate={{ strokeDasharray: `${(riskScore / 100) * 552} 1000`, stroke: riskScore > 50 ? '#EF4444' : '#10B981' }}
                                    cx="96" cy="96" r="88"
                                    strokeWidth="12"
                                    fill="transparent"
                                    strokeLinecap="round"
                                    className={`${getColor(riskScore)} transition-colors duration-500`}
                                    style={{ stroke: 'currentColor' }}
                                />
                            )}
                        </svg>

                        {/* Value Text */}
                        <div className="absolute inset-0 flex flex-col items-center justify-center">
                            {isLoading ? (
                                <span className="text-sm text-gray-400 animate-pulse">Calcul...</span>
                            ) : (
                                <>
                                    <span className={`text-5xl font-black ${riskScore && riskScore > 50 ? 'text-red-500' : 'text-green-500'}`}>
                                        {riskScore?.toFixed(0)}%
                                    </span>
                                    <span className="text-sm text-gray-400">Probabilité</span>
                                </>
                            )}
                        </div>
                    </div>

                    <p className="mt-8 text-center text-sm text-gray-500 max-w-xs">
                        Modifiez les curseurs pour voir l'impact immédiat sur la prédiction grâce au modèle <b>Nuclear GradientBoosting</b>.
                    </p>
                </div>
            </div>
        </div>
    );
}
