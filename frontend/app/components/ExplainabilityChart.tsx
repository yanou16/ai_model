'use client';

import React from 'react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell, ReferenceLine } from 'recharts';

interface Factor {
    feature: string;
    impact: number;
    value: any;
}

interface ExplainabilityProps {
    data: {
        risk_factors: Factor[];
        protective_factors: Factor[];
    };
}

export default function ExplainabilityChart({ data }: ExplainabilityProps) {
    if (!data || (!data.risk_factors.length && !data.protective_factors.length)) {
        return null;
    }

    // Combine and sort data for the chart
    // We want Protective (Negative) on left, Risk (Positive) on right
    // Or simply a list sorted by impact

    // Let's create a combined dataset
    const combinedData = [
        ...data.protective_factors,
        ...data.risk_factors
    ].sort((a, b) => a.impact - b.impact);

    return (
        <div className="bg-white dark:bg-gray-800 rounded-3xl shadow-xl p-8 border border-gray-100 dark:border-gray-700 mt-8">
            <h2 className="text-2xl font-bold mb-6 text-gray-800 dark:text-white flex items-center gap-2">
                🧠 Comprendre la Décision (SHAP)
                <span className="text-xs font-normal px-2 py-1 bg-purple-100 text-purple-800 rounded-full">Explicabilité</span>
            </h2>

            <div className="h-[400px] w-full">
                <ResponsiveContainer width="100%" height="100%">
                    <BarChart
                        layout="vertical"
                        data={combinedData}
                        margin={{ top: 5, right: 30, left: 100, bottom: 5 }}
                    >
                        <ReferenceLine x={0} stroke="#9ca3af" />
                        <XAxis type="number" hide />
                        <YAxis
                            dataKey="feature"
                            type="category"
                            width={150}
                            tick={{ fill: '#6b7280', fontSize: 12 }}
                        />
                        <Tooltip
                            cursor={{ fill: 'transparent' }}
                            content={({ active, payload }) => {
                                if (active && payload && payload.length) {
                                    const d = payload[0].payload;
                                    return (
                                        <div className="bg-white p-3 border border-gray-200 shadow-lg rounded-lg">
                                            <p className="font-bold">{d.feature}</p>
                                            <p className={`text-sm ${d.impact > 0 ? 'text-red-500' : 'text-green-500'}`}>
                                                Impact: {d.impact > 0 ? '+' : ''}{d.impact.toFixed(2)}
                                            </p>
                                            <p className="text-xs text-gray-500">Valeur : {d.value}</p>
                                        </div>
                                    );
                                }
                                return null;
                            }}
                        />
                        <Bar dataKey="impact" radius={[4, 4, 4, 4]}>
                            {combinedData.map((entry, index) => (
                                <Cell key={`cell-${index}`} fill={entry.impact > 0 ? '#EF4444' : '#10B981'} />
                            ))}
                        </Bar>
                    </BarChart>
                </ResponsiveContainer>
            </div>

            <div className="mt-4 flex justify-between text-sm text-gray-500 px-10">
                <span className="flex items-center gap-2">
                    <div className="w-3 h-3 bg-green-500 rounded"></div>
                    Réduit le Risque (Positif)
                </span>
                <span className="flex items-center gap-2">
                    Augmente le Risque (Négatif)
                    <div className="w-3 h-3 bg-red-500 rounded"></div>
                </span>
            </div>
            <p className="mt-4 text-center text-xs text-gray-400">
                * Les valeurs SHAP indiquent l'importance de chaque critère dans la décision finale du modèle.
            </p>
        </div>
    );
}
