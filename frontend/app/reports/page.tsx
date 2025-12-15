'use client';

import React, { useState, useRef } from 'react';
import Sidebar from '../components/Sidebar';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell, PieChart, Pie, Legend, LineChart, Line, CartesianGrid, AreaChart, Area } from 'recharts';
import jsPDF from 'jspdf';
import autoTable from 'jspdf-autotable';

// Sample report data
const departmentData = [
    { name: 'Sales', employees: 45, avgRisk: 38, highRisk: 12 },
    { name: 'R&D', employees: 62, avgRisk: 22, highRisk: 5 },
    { name: 'HR', employees: 18, avgRisk: 31, highRisk: 4 },
    { name: 'Finance', employees: 25, avgRisk: 28, highRisk: 3 },
    { name: 'IT', employees: 35, avgRisk: 25, highRisk: 4 },
];

const trendData = [
    { month: 'Jan', risk: 28 },
    { month: 'Fév', risk: 32 },
    { month: 'Mar', risk: 29 },
    { month: 'Avr', risk: 35 },
    { month: 'Mai', risk: 33 },
    { month: 'Jun', risk: 30 },
];

const riskDistribution = [
    { name: 'Faible (<30%)', value: 65, fill: '#22c55e' },
    { name: 'Modéré (30-50%)', value: 25, fill: '#eab308' },
    { name: 'Élevé (>50%)', value: 10, fill: '#ef4444' },
];

const topRiskEmployees = [
    { name: 'Sophie Bernard', department: 'HR', risk: 72 },
    { name: 'Emma Robert', department: 'HR', risk: 68 },
    { name: 'Marc Leroy', department: 'Sales', risk: 61 },
    { name: 'Julie Blanc', department: 'Sales', risk: 58 },
    { name: 'Antoine Faure', department: 'Finance', risk: 54 },
];

export default function ReportsPage() {
    const [isGenerating, setIsGenerating] = useState(false);
    const [reportType, setReportType] = useState<'summary' | 'detailed' | 'department'>('summary');
    const reportRef = useRef<HTMLDivElement>(null);

    const generatePDF = async () => {
        setIsGenerating(true);

        const doc = new jsPDF();
        const pageWidth = doc.internal.pageSize.getWidth();
        
        // Header
        doc.setFillColor(79, 70, 229); // Indigo
        doc.rect(0, 0, pageWidth, 40, 'F');
        
        doc.setTextColor(255, 255, 255);
        doc.setFontSize(24);
        doc.setFont('helvetica', 'bold');
        doc.text('AttritionAI', 20, 25);
        
        doc.setFontSize(12);
        doc.setFont('helvetica', 'normal');
        doc.text('Rapport d\'Analyse d\'Attrition', 20, 35);
        
        doc.setFontSize(10);
        doc.text(`Généré le ${new Date().toLocaleDateString('fr-FR')}`, pageWidth - 60, 25);

        // Reset text color
        doc.setTextColor(0, 0, 0);
        
        let yPos = 55;

        // Executive Summary
        doc.setFontSize(16);
        doc.setFont('helvetica', 'bold');
        doc.text('Résumé Exécutif', 20, yPos);
        yPos += 10;

        doc.setFontSize(10);
        doc.setFont('helvetica', 'normal');
        const summaryText = [
            `• Total Employés Analysés: 185`,
            `• Risque Moyen Global: 29.2%`,
            `• Employés à Risque Élevé: 28 (15.1%)`,
            `• Département le Plus à Risque: Sales (38% risque moyen)`,
            `• Tendance: Légère amélioration (-2% vs mois dernier)`,
        ];
        
        summaryText.forEach(line => {
            doc.text(line, 25, yPos);
            yPos += 6;
        });

        yPos += 10;

        // Department Analysis Table
        doc.setFontSize(14);
        doc.setFont('helvetica', 'bold');
        doc.text('Analyse par Département', 20, yPos);
        yPos += 5;

        autoTable(doc, {
            startY: yPos,
            head: [['Département', 'Employés', 'Risque Moyen', 'Risque Élevé']],
            body: departmentData.map(d => [
                d.name,
                d.employees.toString(),
                `${d.avgRisk}%`,
                d.highRisk.toString()
            ]),
            theme: 'grid',
            headStyles: { fillColor: [79, 70, 229], textColor: 255 },
            styles: { fontSize: 9 },
            margin: { left: 20, right: 20 },
        });

        yPos = (doc as any).lastAutoTable.finalY + 15;

        // High Risk Employees
        doc.setFontSize(14);
        doc.setFont('helvetica', 'bold');
        doc.text('Employés à Risque Élevé (Top 5)', 20, yPos);
        yPos += 5;

        autoTable(doc, {
            startY: yPos,
            head: [['Nom', 'Département', 'Niveau de Risque']],
            body: topRiskEmployees.map(e => [
                e.name,
                e.department,
                `${e.risk}%`
            ]),
            theme: 'grid',
            headStyles: { fillColor: [239, 68, 68], textColor: 255 },
            styles: { fontSize: 9 },
            margin: { left: 20, right: 20 },
        });

        yPos = (doc as any).lastAutoTable.finalY + 15;

        // Recommendations
        if (yPos > 230) {
            doc.addPage();
            yPos = 20;
        }

        doc.setFontSize(14);
        doc.setFont('helvetica', 'bold');
        doc.text('Recommandations', 20, yPos);
        yPos += 10;

        doc.setFontSize(10);
        doc.setFont('helvetica', 'normal');
        const recommendations = [
            '1. Prioriser les entretiens individuels pour les 5 employés à risque élevé identifiés.',
            '2. Revoir les conditions de travail dans le département Sales (risque le plus élevé).',
            '3. Mettre en place un programme de rétention ciblé pour les employés avec < 2 ans d\'ancienneté.',
            '4. Améliorer la satisfaction au travail via des enquêtes de feedback régulières.',
            '5. Planifier des sessions de développement de carrière pour les talents clés.',
        ];

        recommendations.forEach(rec => {
            const lines = doc.splitTextToSize(rec, pageWidth - 45);
            lines.forEach((line: string) => {
                doc.text(line, 25, yPos);
                yPos += 5;
            });
            yPos += 3;
        });

        // Footer
        const pageCount = doc.getNumberOfPages();
        for (let i = 1; i <= pageCount; i++) {
            doc.setPage(i);
            doc.setFontSize(8);
            doc.setTextColor(128, 128, 128);
            doc.text(
                `Page ${i} sur ${pageCount} | AttritionAI - Rapport Confidentiel`,
                pageWidth / 2,
                doc.internal.pageSize.getHeight() - 10,
                { align: 'center' }
            );
        }

        // Save
        doc.save(`AttritionAI_Report_${new Date().toISOString().split('T')[0]}.pdf`);
        setIsGenerating(false);
    };

    return (
        <div className="min-h-screen bg-zinc-950">
            <Sidebar active="reports" />
            
            <main className="ml-64 p-6">
                {/* Header */}
                <header className="flex items-center justify-between mb-8">
                    <div>
                        <h1 className="text-2xl font-bold text-white">Reports</h1>
                        <p className="text-zinc-500 text-sm mt-1">Visualisez et exportez les analyses d'attrition</p>
                    </div>
                    <div className="flex items-center gap-3">
                        <select 
                            value={reportType}
                            onChange={(e) => setReportType(e.target.value as any)}
                            className="select w-48"
                        >
                            <option value="summary">Rapport Résumé</option>
                            <option value="detailed">Rapport Détaillé</option>
                            <option value="department">Par Département</option>
                        </select>
                        <button 
                            onClick={generatePDF}
                            disabled={isGenerating}
                            className="btn btn-primary flex items-center gap-2"
                        >
                            {isGenerating ? (
                                <>
                                    <svg className="animate-spin h-4 w-4" fill="none" viewBox="0 0 24 24">
                                        <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                                        <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
                                    </svg>
                                    Génération...
                                </>
                            ) : (
                                <>
                                    <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                                    </svg>
                                    Exporter PDF
                                </>
                            )}
                        </button>
                    </div>
                </header>

                {/* Stats Overview */}
                <div className="grid grid-cols-4 gap-4 mb-6">
                    <div className="card">
                        <p className="text-xs text-zinc-500 uppercase tracking-wider">Employés Analysés</p>
                        <p className="text-2xl font-bold text-white mt-1">185</p>
                        <p className="text-xs text-emerald-400 mt-1">+12 ce mois</p>
                    </div>
                    <div className="card">
                        <p className="text-xs text-zinc-500 uppercase tracking-wider">Risque Moyen</p>
                        <p className="text-2xl font-bold text-white mt-1">29.2%</p>
                        <p className="text-xs text-emerald-400 mt-1">-2% vs dernier mois</p>
                    </div>
                    <div className="card">
                        <p className="text-xs text-zinc-500 uppercase tracking-wider">Risque Élevé</p>
                        <p className="text-2xl font-bold text-red-400 mt-1">28</p>
                        <p className="text-xs text-zinc-500 mt-1">15.1% du total</p>
                    </div>
                    <div className="card">
                        <p className="text-xs text-zinc-500 uppercase tracking-wider">Départs Prédits</p>
                        <p className="text-2xl font-bold text-amber-400 mt-1">8-12</p>
                        <p className="text-xs text-zinc-500 mt-1">Prochains 6 mois</p>
                    </div>
                </div>

                <div ref={reportRef}>
                    {/* Charts Row */}
                    <div className="grid grid-cols-2 gap-6 mb-6">
                        {/* Risk by Department */}
                        <div className="card">
                            <div className="card-header">
                                <span className="card-title">Risque Moyen par Département</span>
                            </div>
                            <div className="h-[250px]">
                                <ResponsiveContainer width="100%" height="100%">
                                    <BarChart data={departmentData} layout="vertical">
                                        <CartesianGrid strokeDasharray="3 3" stroke="#3f3f46" horizontal={false} />
                                        <XAxis type="number" tick={{ fill: '#71717a', fontSize: 11 }} domain={[0, 50]} />
                                        <YAxis dataKey="name" type="category" tick={{ fill: '#a1a1aa', fontSize: 11 }} width={60} />
                                        <Tooltip
                                            contentStyle={{ background: '#18181b', border: '1px solid #3f3f46', borderRadius: '8px' }}
                                            formatter={(value: number) => [`${value}%`, 'Risque Moyen']}
                                        />
                                        <Bar dataKey="avgRisk" radius={[0, 4, 4, 0]}>
                                            {departmentData.map((entry, index) => (
                                                <Cell key={index} fill={entry.avgRisk > 35 ? '#ef4444' : entry.avgRisk > 25 ? '#eab308' : '#22c55e'} />
                                            ))}
                                        </Bar>
                                    </BarChart>
                                </ResponsiveContainer>
                            </div>
                        </div>

                        {/* Risk Distribution Pie */}
                        <div className="card">
                            <div className="card-header">
                                <span className="card-title">Distribution des Risques</span>
                            </div>
                            <div className="h-[250px]">
                                <ResponsiveContainer width="100%" height="100%">
                                    <PieChart>
                                        <Pie
                                            data={riskDistribution}
                                            cx="50%"
                                            cy="50%"
                                            innerRadius={60}
                                            outerRadius={90}
                                            paddingAngle={2}
                                            dataKey="value"
                                        >
                                            {riskDistribution.map((entry, index) => (
                                                <Cell key={index} fill={entry.fill} />
                                            ))}
                                        </Pie>
                                        <Tooltip
                                            contentStyle={{ background: '#18181b', border: '1px solid #3f3f46', borderRadius: '8px' }}
                                            formatter={(value: number) => [`${value}%`, 'Employés']}
                                        />
                                        <Legend 
                                            verticalAlign="bottom" 
                                            height={36}
                                            formatter={(value) => <span style={{ color: '#a1a1aa', fontSize: '12px' }}>{value}</span>}
                                        />
                                    </PieChart>
                                </ResponsiveContainer>
                            </div>
                        </div>
                    </div>

                    {/* Trend Chart */}
                    <div className="card mb-6">
                        <div className="card-header">
                            <span className="card-title">Évolution du Risque Moyen (6 derniers mois)</span>
                        </div>
                        <div className="h-[200px]">
                            <ResponsiveContainer width="100%" height="100%">
                                <AreaChart data={trendData}>
                                    <defs>
                                        <linearGradient id="riskGradient" x1="0" y1="0" x2="0" y2="1">
                                            <stop offset="5%" stopColor="#6366f1" stopOpacity={0.3}/>
                                            <stop offset="95%" stopColor="#6366f1" stopOpacity={0}/>
                                        </linearGradient>
                                    </defs>
                                    <CartesianGrid strokeDasharray="3 3" stroke="#3f3f46" />
                                    <XAxis dataKey="month" tick={{ fill: '#71717a', fontSize: 11 }} />
                                    <YAxis tick={{ fill: '#71717a', fontSize: 11 }} domain={[20, 40]} />
                                    <Tooltip
                                        contentStyle={{ background: '#18181b', border: '1px solid #3f3f46', borderRadius: '8px' }}
                                        formatter={(value: number) => [`${value}%`, 'Risque Moyen']}
                                    />
                                    <Area type="monotone" dataKey="risk" stroke="#6366f1" strokeWidth={2} fill="url(#riskGradient)" />
                                </AreaChart>
                            </ResponsiveContainer>
                        </div>
                    </div>

                    {/* High Risk Employees Table */}
                    <div className="card">
                        <div className="card-header">
                            <span className="card-title">Employés à Risque Élevé</span>
                            <span className="badge badge-danger">{topRiskEmployees.length} employés</span>
                        </div>
                        <table className="table">
                            <thead>
                                <tr>
                                    <th>Employé</th>
                                    <th>Département</th>
                                    <th>Niveau de Risque</th>
                                    <th>Action Recommandée</th>
                                </tr>
                            </thead>
                            <tbody>
                                {topRiskEmployees.map((emp, idx) => (
                                    <tr key={idx}>
                                        <td className="font-medium text-white">{emp.name}</td>
                                        <td>{emp.department}</td>
                                        <td>
                                            <div className="flex items-center gap-2">
                                                <div className="w-20 h-2 bg-zinc-800 rounded-full overflow-hidden">
                                                    <div 
                                                        className="h-full rounded-full bg-red-500"
                                                        style={{ width: `${emp.risk}%` }}
                                                    />
                                                </div>
                                                <span className="text-red-400 font-medium">{emp.risk}%</span>
                                            </div>
                                        </td>
                                        <td>
                                            <span className="text-amber-400 text-sm">Entretien urgent</span>
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                </div>
            </main>
        </div>
    );
}
