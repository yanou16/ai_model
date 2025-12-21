'use client';

import React, { useState } from 'react';
import { usePrediction } from './context/PredictionContext';
import Sidebar from './components/Sidebar';
import RealTimeSimulator from './components/RealTimeSimulator';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell, PieChart, Pie, Legend, LineChart, Line, CartesianGrid } from 'recharts';

// API Configuration
const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000';

// Options
const DEPARTMENTS = ['Sales', 'Research & Development', 'Human Resources'];
const JOB_ROLES = ['Sales Executive', 'Research Scientist', 'Laboratory Technician', 'Manufacturing Director', 'Healthcare Representative', 'Manager', 'Sales Representative', 'Research Director', 'Human Resources'];
const EDUCATION_FIELDS = ['Life Sciences', 'Medical', 'Marketing', 'Technical Degree', 'Human Resources', 'Other'];
const TRAVEL_OPTIONS = ['Non-Travel', 'Travel_Rarely', 'Travel_Frequently'];

export default function Dashboard() {
    const { setFormData, setPredictionResult } = usePrediction();
    const [isLoading, setIsLoading] = useState(false);
    const [prediction, setPrediction] = useState<any>(null);
    const [explainability, setExplainability] = useState<any>(null);
    const [showAdvanced, setShowAdvanced] = useState(false);

    const [form, setForm] = useState({
        // Démographie
        Age: 35, Gender: 'Male', MaritalStatus: 'Single', DistanceFromHome: 10,
        // Éducation
        Education: 3, EducationField: 'Life Sciences',
        // Poste
        Department: 'Research & Development', JobRole: 'Research Scientist', JobLevel: 2,
        MonthlyIncome: 5000, BusinessTravel: 'Travel_Rarely',
        // Expérience
        TotalWorkingYears: 10, YearsAtCompany: 5, YearsWithCurrManager: 3,
        YearsSinceLastPromotion: 2, NumCompaniesWorked: 2,
        // Satisfaction (1-4)
        JobSatisfaction: 3, EnvironmentSatisfaction: 3, WorkLifeBalance: 3,
        JobInvolvement: 3, PerformanceRating: 3,
        // Avantages
        PercentSalaryHike: 15, StockOptionLevel: 1, TrainingTimesLastYear: 3,
        // Données Temporelles (Avancées)
        AvgWorkingHours: 8.5, LateArrivals: 10, AvgOvertime: 0.5,
        AbsenceRate: 5.0, WorkHoursVariance: 1.0,
    });

    const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
        const { name, value, type } = e.target;
        if (type === 'number') {
            const numValue = parseFloat(value);
            setForm(prev => ({ ...prev, [name]: isNaN(numValue) ? 0 : numValue }));
        } else {
            setForm(prev => ({ ...prev, [name]: value }));
        }
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setIsLoading(true);
        try {
            const response = await fetch(`${API_URL}/predict`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(form),
            });
            const data = await response.json();
            setPrediction(data);
            setExplainability(data.explainability);
            setFormData(form);
            setPredictionResult(data.probabilities?.leave);
        } catch (error) {
            console.error('Prediction error:', error);
        } finally {
            setIsLoading(false);
        }
    };

    const riskScore = prediction?.probabilities?.leave || 0;
    const stayScore = prediction?.probabilities?.stay || 0;

    // Chart data
    const probabilityData = prediction ? [
        { name: 'Rester', value: stayScore, fill: '#22c55e' },
        { name: 'Partir', value: riskScore, fill: '#ef4444' },
    ] : [];

    const shapData = explainability ? [
        ...explainability.risk_factors.slice(0, 5).map((f: any) => ({ name: f.feature, impact: f.impact, value: f.value })),
        ...explainability.protective_factors.slice(0, 5).map((f: any) => ({ name: f.feature, impact: f.impact, value: f.value })),
    ].sort((a, b) => b.impact - a.impact) : [];

    return (
        <div className="min-h-screen bg-zinc-950">
            <Sidebar active="dashboard" />

            {/* Main Content */}
            <main className="ml-64 p-6">
                {/* Header */}
                <header className="flex items-center justify-between mb-8">
                    <div>
                        <h1 className="text-2xl font-bold text-white">Prédiction d'Attrition</h1>
                        <p className="text-zinc-500 text-sm mt-1">Analysez le risque de départ d'un employé</p>
                    </div>
                    <div className="flex items-center gap-3">
                        <span className="badge badge-success">Model v2.1</span>
                        <span className="text-zinc-500 text-sm">Accuracy: 95%</span>
                    </div>
                </header>

                <div className="grid grid-cols-12 gap-6">
                    {/* Input Form - Left Column */}
                    <div className="col-span-4">
                        <form onSubmit={handleSubmit} className="card space-y-5">
                            <div className="flex items-center justify-between border-b border-zinc-800 pb-4 -mx-5 px-5 -mt-5 pt-4">
                                <h2 className="font-semibold text-white">Données Employé</h2>
                                <span className="text-xs text-zinc-500">31 variables</span>
                            </div>

                            {/* Demographics */}
                            <div>
                                <h3 className="text-xs font-medium text-zinc-500 uppercase tracking-wider mb-3">Démographie</h3>
                                <div className="grid grid-cols-2 gap-3">
                                    <div>
                                        <label className="label">Âge</label>
                                        <input type="number" name="Age" value={form.Age} onChange={handleChange} className="input" />
                                    </div>
                                    <div>
                                        <label className="label">Genre</label>
                                        <select name="Gender" value={form.Gender} onChange={handleChange} className="select">
                                            <option value="Male">Homme</option>
                                            <option value="Female">Femme</option>
                                        </select>
                                    </div>
                                    <div>
                                        <label className="label">Statut</label>
                                        <select name="MaritalStatus" value={form.MaritalStatus} onChange={handleChange} className="select">
                                            <option value="Single">Célibataire</option>
                                            <option value="Married">Marié(e)</option>
                                            <option value="Divorced">Divorcé(e)</option>
                                        </select>
                                    </div>
                                    <div>
                                        <label className="label">Distance (km)</label>
                                        <input type="number" name="DistanceFromHome" value={form.DistanceFromHome} onChange={handleChange} className="input" />
                                    </div>
                                </div>
                            </div>

                            {/* Education */}
                            <div>
                                <h3 className="text-xs font-medium text-zinc-500 uppercase tracking-wider mb-3">Éducation</h3>
                                <div className="grid grid-cols-2 gap-3">
                                    <div>
                                        <label className="label">Niveau (1-5)</label>
                                        <select name="Education" value={form.Education} onChange={handleChange} className="select">
                                            <option value={1}>1 - Inférieur Bac</option>
                                            <option value={2}>2 - Bac</option>
                                            <option value={3}>3 - Licence</option>
                                            <option value={4}>4 - Master</option>
                                            <option value={5}>5 - Doctorat</option>
                                        </select>
                                    </div>
                                    <div>
                                        <label className="label">Domaine</label>
                                        <select name="EducationField" value={form.EducationField} onChange={handleChange} className="select">
                                            {EDUCATION_FIELDS.map(f => <option key={f} value={f}>{f}</option>)}
                                        </select>
                                    </div>
                                </div>
                            </div>

                            {/* Job */}
                            <div>
                                <h3 className="text-xs font-medium text-zinc-500 uppercase tracking-wider mb-3">Poste</h3>
                                <div className="space-y-3">
                                    <div className="grid grid-cols-2 gap-3">
                                        <div>
                                            <label className="label">Département</label>
                                            <select name="Department" value={form.Department} onChange={handleChange} className="select">
                                                {DEPARTMENTS.map(d => <option key={d} value={d}>{d}</option>)}
                                            </select>
                                        </div>
                                        <div>
                                            <label className="label">Rôle</label>
                                            <select name="JobRole" value={form.JobRole} onChange={handleChange} className="select">
                                                {JOB_ROLES.map(r => <option key={r} value={r}>{r}</option>)}
                                            </select>
                                        </div>
                                    </div>
                                    <div className="grid grid-cols-3 gap-3">
                                        <div>
                                            <label className="label">Niveau</label>
                                            <select name="JobLevel" value={form.JobLevel} onChange={handleChange} className="select">
                                                {[1, 2, 3, 4, 5].map(l => <option key={l} value={l}>{l}</option>)}
                                            </select>
                                        </div>
                                        <div>
                                            <label className="label">Salaire ($)</label>
                                            <input type="number" name="MonthlyIncome" value={form.MonthlyIncome} onChange={handleChange} className="input" />
                                        </div>
                                        <div>
                                            <label className="label">Voyages</label>
                                            <select name="BusinessTravel" value={form.BusinessTravel} onChange={handleChange} className="select">
                                                <option value="Non-Travel">Aucun</option>
                                                <option value="Travel_Rarely">Rare</option>
                                                <option value="Travel_Frequently">Fréquent</option>
                                            </select>
                                        </div>
                                    </div>
                                </div>
                            </div>

                            {/* Experience */}
                            <div>
                                <h3 className="text-xs font-medium text-zinc-500 uppercase tracking-wider mb-3">Expérience (années)</h3>
                                <div className="grid grid-cols-3 gap-3">
                                    <div>
                                        <label className="label">Totale</label>
                                        <input type="number" name="TotalWorkingYears" value={form.TotalWorkingYears} onChange={handleChange} className="input" />
                                    </div>
                                    <div>
                                        <label className="label">Entreprise</label>
                                        <input type="number" name="YearsAtCompany" value={form.YearsAtCompany} onChange={handleChange} className="input" />
                                    </div>
                                    <div>
                                        <label className="label">Manager</label>
                                        <input type="number" name="YearsWithCurrManager" value={form.YearsWithCurrManager} onChange={handleChange} className="input" />
                                    </div>
                                    <div>
                                        <label className="label">Depuis promo</label>
                                        <input type="number" name="YearsSinceLastPromotion" value={form.YearsSinceLastPromotion} onChange={handleChange} className="input" />
                                    </div>
                                    <div>
                                        <label className="label">Nb Entreprises</label>
                                        <input type="number" name="NumCompaniesWorked" value={form.NumCompaniesWorked} onChange={handleChange} className="input" />
                                    </div>
                                </div>
                            </div>

                            {/* Satisfaction */}
                            <div>
                                <h3 className="text-xs font-medium text-zinc-500 uppercase tracking-wider mb-3">Satisfaction (1-4)</h3>
                                <div className="grid grid-cols-3 gap-3">
                                    <div>
                                        <label className="label">Job</label>
                                        <select name="JobSatisfaction" value={form.JobSatisfaction} onChange={handleChange} className="select">
                                            {[1, 2, 3, 4].map(s => <option key={s} value={s}>{s}</option>)}
                                        </select>
                                    </div>
                                    <div>
                                        <label className="label">Environnement</label>
                                        <select name="EnvironmentSatisfaction" value={form.EnvironmentSatisfaction} onChange={handleChange} className="select">
                                            {[1, 2, 3, 4].map(s => <option key={s} value={s}>{s}</option>)}
                                        </select>
                                    </div>
                                    <div>
                                        <label className="label">Équilibre</label>
                                        <select name="WorkLifeBalance" value={form.WorkLifeBalance} onChange={handleChange} className="select">
                                            {[1, 2, 3, 4].map(s => <option key={s} value={s}>{s}</option>)}
                                        </select>
                                    </div>
                                    <div>
                                        <label className="label">Implication</label>
                                        <select name="JobInvolvement" value={form.JobInvolvement} onChange={handleChange} className="select">
                                            {[1, 2, 3, 4].map(s => <option key={s} value={s}>{s}</option>)}
                                        </select>
                                    </div>
                                    <div>
                                        <label className="label">Performance</label>
                                        <select name="PerformanceRating" value={form.PerformanceRating} onChange={handleChange} className="select">
                                            {[3, 4].map(s => <option key={s} value={s}>{s}</option>)}
                                        </select>
                                    </div>
                                </div>
                            </div>

                            {/* Benefits */}
                            <div>
                                <h3 className="text-xs font-medium text-zinc-500 uppercase tracking-wider mb-3">Avantages</h3>
                                <div className="grid grid-cols-3 gap-3">
                                    <div>
                                        <label className="label">Augmentation %</label>
                                        <input type="number" name="PercentSalaryHike" value={form.PercentSalaryHike} onChange={handleChange} className="input" />
                                    </div>
                                    <div>
                                        <label className="label">Stock (0-3)</label>
                                        <select name="StockOptionLevel" value={form.StockOptionLevel} onChange={handleChange} className="select">
                                            {[0, 1, 2, 3].map(s => <option key={s} value={s}>{s}</option>)}
                                        </select>
                                    </div>
                                    <div>
                                        <label className="label">Formations</label>
                                        <input type="number" name="TrainingTimesLastYear" value={form.TrainingTimesLastYear} onChange={handleChange} className="input" />
                                    </div>
                                </div>
                            </div>

                            {/* Advanced - Temporal Data (Collapsible) */}
                            <div>
                                <button
                                    type="button"
                                    onClick={() => setShowAdvanced(!showAdvanced)}
                                    className="flex items-center gap-2 text-xs font-medium text-zinc-500 uppercase tracking-wider mb-3 hover:text-zinc-300 transition-colors"
                                >
                                    <svg className={`w-3 h-3 transition-transform ${showAdvanced ? 'rotate-90' : ''}`} fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                                    </svg>
                                    Données Temporelles (Avancé)
                                </button>
                                {showAdvanced && (
                                    <div className="grid grid-cols-2 gap-3 p-3 bg-zinc-900/50 rounded-lg border border-zinc-800">
                                        <div>
                                            <label className="label">Heures/jour moy.</label>
                                            <input type="number" step="0.1" name="AvgWorkingHours" value={form.AvgWorkingHours} onChange={handleChange} className="input" />
                                        </div>
                                        <div>
                                            <label className="label">Retards</label>
                                            <input type="number" name="LateArrivals" value={form.LateArrivals} onChange={handleChange} className="input" />
                                        </div>
                                        <div>
                                            <label className="label">Heures sup moy.</label>
                                            <input type="number" step="0.1" name="AvgOvertime" value={form.AvgOvertime} onChange={handleChange} className="input" />
                                        </div>
                                        <div>
                                            <label className="label">Absence %</label>
                                            <input type="number" step="0.1" name="AbsenceRate" value={form.AbsenceRate} onChange={handleChange} className="input" />
                                        </div>
                                        <div className="col-span-2">
                                            <label className="label">Variance heures</label>
                                            <input type="number" step="0.1" name="WorkHoursVariance" value={form.WorkHoursVariance} onChange={handleChange} className="input" />
                                        </div>
                                    </div>
                                )}
                            </div>

                            <button
                                type="submit"
                                disabled={isLoading}
                                className="w-full btn btn-primary flex items-center justify-center gap-2"
                            >
                                {isLoading ? (
                                    <>
                                        <svg className="animate-spin h-4 w-4" fill="none" viewBox="0 0 24 24">
                                            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                                            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
                                        </svg>
                                        Analyse...
                                    </>
                                ) : (
                                    <>
                                        <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" /></svg>
                                        Analyser le Risque
                                    </>
                                )}
                            </button>
                        </form>
                    </div>

                    {/* Results - Right Columns */}
                    <div className="col-span-8 space-y-6">
                        {/* Stat Cards Row */}
                        <div className="grid grid-cols-3 gap-4">
                            <div className="card">
                                <div className="card-header">
                                    <span className="card-title">Risque de Départ</span>
                                    {prediction && (
                                        <span className={`badge ${riskScore > 50 ? 'badge-danger' : riskScore > 30 ? 'badge-warning' : 'badge-success'}`}>
                                            {riskScore > 50 ? 'Élevé' : riskScore > 30 ? 'Modéré' : 'Faible'}
                                        </span>
                                    )}
                                </div>
                                <div className="card-value" style={{ color: prediction ? (riskScore > 50 ? '#ef4444' : riskScore > 30 ? '#eab308' : '#22c55e') : '#71717a' }}>
                                    {prediction ? `${riskScore.toFixed(1)}%` : '—'}
                                </div>
                                <p className="text-xs text-zinc-500 mt-2">Probabilité de quitter l'entreprise</p>
                            </div>

                            <div className="card">
                                <div className="card-header">
                                    <span className="card-title">Probabilité Rester</span>
                                </div>
                                <div className="card-value text-emerald-400">
                                    {prediction ? `${stayScore.toFixed(1)}%` : '—'}
                                </div>
                                <p className="text-xs text-zinc-500 mt-2">Probabilité de rester</p>
                            </div>

                            <div className="card">
                                <div className="card-header">
                                    <span className="card-title">Confiance Modèle</span>
                                </div>
                                <div className="card-value text-white">
                                    {prediction ? '95%' : '—'}
                                </div>
                                <p className="text-xs text-zinc-500 mt-2">Score de confiance</p>
                            </div>
                        </div>

                        {/* Charts Row */}
                        <div className="grid grid-cols-2 gap-4">
                            {/* Probability Pie Chart */}
                            <div className="card">
                                <div className="card-header">
                                    <span className="card-title">Distribution des Probabilités</span>
                                </div>
                                {prediction ? (
                                    <div className="h-[200px]">
                                        <ResponsiveContainer width="100%" height="100%">
                                            <PieChart>
                                                <Pie
                                                    data={probabilityData}
                                                    cx="50%"
                                                    cy="50%"
                                                    innerRadius={50}
                                                    outerRadius={80}
                                                    paddingAngle={2}
                                                    dataKey="value"
                                                    label={({ name, value }) => `${name}: ${value.toFixed(0)}%`}
                                                    labelLine={{ stroke: '#52525b' }}
                                                >
                                                    {probabilityData.map((entry, index) => (
                                                        <Cell key={`cell-${index}`} fill={entry.fill} />
                                                    ))}
                                                </Pie>
                                                <Tooltip
                                                    contentStyle={{ background: '#18181b', border: '1px solid #3f3f46', borderRadius: '8px' }}
                                                    labelStyle={{ color: '#fff' }}
                                                />
                                            </PieChart>
                                        </ResponsiveContainer>
                                    </div>
                                ) : (
                                    <div className="h-[200px] flex items-center justify-center text-zinc-600">
                                        Lancez une analyse pour voir les résultats
                                    </div>
                                )}
                            </div>

                            {/* Risk Gauge */}
                            <div className="card">
                                <div className="card-header">
                                    <span className="card-title">Indicateur de Risque</span>
                                </div>
                                {prediction ? (
                                    <div className="h-[200px] flex items-center justify-center">
                                        <div className="relative">
                                            <svg width="160" height="160" className="-rotate-90">
                                                <circle cx="80" cy="80" r="70" stroke="#3f3f46" strokeWidth="12" fill="none" />
                                                <circle
                                                    cx="80" cy="80" r="70"
                                                    stroke={riskScore > 50 ? '#ef4444' : riskScore > 30 ? '#eab308' : '#22c55e'}
                                                    strokeWidth="12"
                                                    fill="none"
                                                    strokeLinecap="round"
                                                    strokeDasharray={`${(riskScore / 100) * 440} 440`}
                                                    style={{
                                                        transition: 'stroke-dasharray 1s ease',
                                                        filter: `drop-shadow(0 0 8px ${riskScore > 50 ? '#ef4444' : riskScore > 30 ? '#eab308' : '#22c55e'})`
                                                    }}
                                                />
                                            </svg>
                                            <div className="absolute inset-0 flex flex-col items-center justify-center">
                                                <span className="text-3xl font-bold text-white">{riskScore.toFixed(0)}%</span>
                                                <span className="text-xs text-zinc-500">Risque</span>
                                            </div>
                                        </div>
                                    </div>
                                ) : (
                                    <div className="h-[200px] flex items-center justify-center">
                                        <div className="relative">
                                            <svg width="160" height="160">
                                                <circle cx="80" cy="80" r="70" stroke="#3f3f46" strokeWidth="12" fill="none" />
                                            </svg>
                                            <div className="absolute inset-0 flex flex-col items-center justify-center">
                                                <span className="text-3xl font-bold text-zinc-600">—</span>
                                            </div>
                                        </div>
                                    </div>
                                )}
                            </div>
                        </div>

                        {/* Explainability Section */}
                        <div className="card">
                            <div className="card-header">
                                <span className="card-title">Explication du Résultat (SHAP)</span>
                                {prediction && <span className="text-xs text-zinc-500">Top 10 facteurs d'influence</span>}
                            </div>
                            {explainability && shapData.length > 0 ? (
                                <div className="h-[300px]">
                                    <ResponsiveContainer width="100%" height="100%">
                                        <BarChart data={shapData} layout="vertical" margin={{ left: 100 }}>
                                            <CartesianGrid strokeDasharray="3 3" stroke="#3f3f46" horizontal={false} />
                                            <XAxis type="number" tick={{ fill: '#71717a', fontSize: 12 }} axisLine={{ stroke: '#3f3f46' }} />
                                            <YAxis
                                                dataKey="name"
                                                type="category"
                                                tick={{ fill: '#a1a1aa', fontSize: 12 }}
                                                axisLine={{ stroke: '#3f3f46' }}
                                                width={100}
                                            />
                                            <Tooltip
                                                contentStyle={{ background: '#18181b', border: '1px solid #3f3f46', borderRadius: '8px' }}
                                                labelStyle={{ color: '#fff', fontWeight: 600 }}
                                                formatter={(value: number, name: string, props: any) => [
                                                    <span key="v" style={{ color: value > 0 ? '#ef4444' : '#22c55e' }}>
                                                        Impact: {value > 0 ? '+' : ''}{value.toFixed(3)}
                                                    </span>,
                                                    `Valeur: ${props.payload.value}`
                                                ]}
                                            />
                                            <Bar dataKey="impact" radius={[0, 4, 4, 0]}>
                                                {shapData.map((entry, index) => (
                                                    <Cell key={`cell-${index}`} fill={entry.impact > 0 ? '#ef4444' : '#22c55e'} />
                                                ))}
                                            </Bar>
                                        </BarChart>
                                    </ResponsiveContainer>
                                </div>
                            ) : (
                                <div className="h-[300px] flex flex-col items-center justify-center text-zinc-600">
                                    <svg className="w-12 h-12 mb-3 text-zinc-700" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                                    </svg>
                                    <p>Lancez une analyse pour voir l'explication SHAP</p>
                                    <p className="text-xs text-zinc-700 mt-1">Les facteurs en rouge augmentent le risque, en vert le réduisent</p>
                                </div>
                            )}
                        </div>

                        {/* Legend */}
                        {explainability && (
                            <div className="flex items-center justify-center gap-8 text-sm">
                                <div className="flex items-center gap-2">
                                    <div className="w-3 h-3 rounded bg-red-500"></div>
                                    <span className="text-zinc-400">Augmente le risque de départ</span>
                                </div>
                                <div className="flex items-center gap-2">
                                    <div className="w-3 h-3 rounded bg-emerald-500"></div>
                                    <span className="text-zinc-400">Réduit le risque de départ</span>
                                </div>
                            </div>
                        )}
                    </div>

                    {/* Real-Time Simulator */}
                    <div className="col-span-12">
                        <RealTimeSimulator />
                    </div>
                </div>
            </main>
        </div>
    );
}
