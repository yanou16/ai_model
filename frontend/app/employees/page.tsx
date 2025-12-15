'use client';

import React, { useState } from 'react';
import Sidebar from '../components/Sidebar';

interface Employee {
    id: number;
    name: string;
    age: number;
    department: string;
    role: string;
    income: number;
    years: number;
    satisfaction: number;
    risk: number | null;
}

// Sample employee data
const SAMPLE_EMPLOYEES: Employee[] = [
    { id: 1, name: 'Marie Dupont', age: 32, department: 'Sales', role: 'Sales Executive', income: 5500, years: 4, satisfaction: 3, risk: null },
    { id: 2, name: 'Jean Martin', age: 45, department: 'R&D', role: 'Research Scientist', income: 8200, years: 12, satisfaction: 4, risk: null },
    { id: 3, name: 'Sophie Bernard', age: 28, department: 'HR', role: 'HR Specialist', income: 4200, years: 2, satisfaction: 2, risk: null },
    { id: 4, name: 'Pierre Durand', age: 38, department: 'Sales', role: 'Manager', income: 9500, years: 8, satisfaction: 3, risk: null },
    { id: 5, name: 'Claire Moreau', age: 29, department: 'R&D', role: 'Lab Technician', income: 3800, years: 3, satisfaction: 4, risk: null },
    { id: 6, name: 'Luc Petit', age: 52, department: 'Sales', role: 'Sales Director', income: 12000, years: 15, satisfaction: 3, risk: null },
    { id: 7, name: 'Emma Robert', age: 26, department: 'HR', role: 'HR Assistant', income: 3200, years: 1, satisfaction: 2, risk: null },
    { id: 8, name: 'Thomas Richard', age: 35, department: 'R&D', role: 'Senior Scientist', income: 7500, years: 6, satisfaction: 4, risk: null },
];

export default function EmployeesPage() {
    const [employees, setEmployees] = useState<Employee[]>(SAMPLE_EMPLOYEES);
    const [isAnalyzing, setIsAnalyzing] = useState(false);
    const [filter, setFilter] = useState('all');
    const [search, setSearch] = useState('');

    const analyzeAll = async () => {
        setIsAnalyzing(true);
        
        // Simulate batch analysis with random risk scores
        const updatedEmployees = employees.map(emp => ({
            ...emp,
            risk: Math.random() * 100
        }));
        
        // Simulate API delay
        await new Promise(resolve => setTimeout(resolve, 1500));
        
        setEmployees(updatedEmployees);
        setIsAnalyzing(false);
    };

    const filteredEmployees = employees.filter(emp => {
        const matchesSearch = emp.name.toLowerCase().includes(search.toLowerCase()) ||
                             emp.department.toLowerCase().includes(search.toLowerCase());
        
        if (filter === 'all') return matchesSearch;
        if (filter === 'high' && emp.risk !== null) return matchesSearch && emp.risk > 50;
        if (filter === 'medium' && emp.risk !== null) return matchesSearch && emp.risk >= 30 && emp.risk <= 50;
        if (filter === 'low' && emp.risk !== null) return matchesSearch && emp.risk < 30;
        return matchesSearch;
    });

    const getRiskBadge = (risk: number | null) => {
        if (risk === null) return <span className="text-zinc-500">—</span>;
        if (risk > 50) return <span className="badge badge-danger">{risk.toFixed(0)}% Élevé</span>;
        if (risk > 30) return <span className="badge badge-warning">{risk.toFixed(0)}% Modéré</span>;
        return <span className="badge badge-success">{risk.toFixed(0)}% Faible</span>;
    };

    const stats = {
        total: employees.length,
        analyzed: employees.filter(e => e.risk !== null).length,
        highRisk: employees.filter(e => e.risk !== null && e.risk > 50).length,
        avgRisk: employees.filter(e => e.risk !== null).length > 0 
            ? (employees.filter(e => e.risk !== null).reduce((sum, e) => sum + (e.risk || 0), 0) / employees.filter(e => e.risk !== null).length)
            : 0
    };

    return (
        <div className="min-h-screen bg-zinc-950">
            <Sidebar active="employees" />
            
            <main className="ml-64 p-6">
                {/* Header */}
                <header className="flex items-center justify-between mb-8">
                    <div>
                        <h1 className="text-2xl font-bold text-white">Employés</h1>
                        <p className="text-zinc-500 text-sm mt-1">Gérez et analysez le risque d'attrition de vos employés</p>
                    </div>
                    <div className="flex items-center gap-3">
                        <button className="btn btn-secondary">
                            <svg className="w-4 h-4 mr-2 inline" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
                            </svg>
                            Ajouter
                        </button>
                        <button 
                            onClick={analyzeAll}
                            disabled={isAnalyzing}
                            className="btn btn-primary flex items-center gap-2"
                        >
                            {isAnalyzing ? (
                                <>
                                    <svg className="animate-spin h-4 w-4" fill="none" viewBox="0 0 24 24">
                                        <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                                        <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
                                    </svg>
                                    Analyse...
                                </>
                            ) : (
                                <>
                                    <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                                    </svg>
                                    Analyser Tous
                                </>
                            )}
                        </button>
                    </div>
                </header>

                {/* Stats Cards */}
                <div className="grid grid-cols-4 gap-4 mb-6">
                    <div className="card">
                        <p className="text-xs text-zinc-500 uppercase tracking-wider">Total Employés</p>
                        <p className="text-2xl font-bold text-white mt-1">{stats.total}</p>
                    </div>
                    <div className="card">
                        <p className="text-xs text-zinc-500 uppercase tracking-wider">Analysés</p>
                        <p className="text-2xl font-bold text-white mt-1">{stats.analyzed}</p>
                    </div>
                    <div className="card">
                        <p className="text-xs text-zinc-500 uppercase tracking-wider">Risque Élevé</p>
                        <p className="text-2xl font-bold text-red-400 mt-1">{stats.highRisk}</p>
                    </div>
                    <div className="card">
                        <p className="text-xs text-zinc-500 uppercase tracking-wider">Risque Moyen</p>
                        <p className="text-2xl font-bold text-white mt-1">{stats.avgRisk.toFixed(0)}%</p>
                    </div>
                </div>

                {/* Filters */}
                <div className="card mb-6">
                    <div className="flex items-center gap-4">
                        <div className="flex-1">
                            <input
                                type="text"
                                placeholder="Rechercher par nom ou département..."
                                value={search}
                                onChange={(e) => setSearch(e.target.value)}
                                className="input"
                            />
                        </div>
                        <div className="flex items-center gap-2">
                            <span className="text-sm text-zinc-500">Filtrer:</span>
                            {['all', 'high', 'medium', 'low'].map(f => (
                                <button
                                    key={f}
                                    onClick={() => setFilter(f)}
                                    className={`px-3 py-1.5 rounded-lg text-sm font-medium transition-colors ${
                                        filter === f 
                                            ? 'bg-indigo-600 text-white' 
                                            : 'bg-zinc-800 text-zinc-400 hover:text-white'
                                    }`}
                                >
                                    {f === 'all' ? 'Tous' : f === 'high' ? 'Élevé' : f === 'medium' ? 'Modéré' : 'Faible'}
                                </button>
                            ))}
                        </div>
                    </div>
                </div>

                {/* Employees Table */}
                <div className="card p-0">
                    <table className="table">
                        <thead>
                            <tr>
                                <th>Employé</th>
                                <th>Département</th>
                                <th>Poste</th>
                                <th>Salaire</th>
                                <th>Ancienneté</th>
                                <th>Satisfaction</th>
                                <th>Risque</th>
                                <th></th>
                            </tr>
                        </thead>
                        <tbody>
                            {filteredEmployees.map(emp => (
                                <tr key={emp.id}>
                                    <td>
                                        <div className="flex items-center gap-3">
                                            <div className="w-8 h-8 rounded-full bg-zinc-700 flex items-center justify-center text-sm text-white">
                                                {emp.name.split(' ').map(n => n[0]).join('')}
                                            </div>
                                            <div>
                                                <p className="font-medium text-white">{emp.name}</p>
                                                <p className="text-xs text-zinc-500">{emp.age} ans</p>
                                            </div>
                                        </div>
                                    </td>
                                    <td>{emp.department}</td>
                                    <td>{emp.role}</td>
                                    <td>${emp.income.toLocaleString()}</td>
                                    <td>{emp.years} ans</td>
                                    <td>
                                        <div className="flex items-center gap-1">
                                            {[1,2,3,4].map(s => (
                                                <span key={s} className={s <= emp.satisfaction ? 'text-amber-400' : 'text-zinc-700'}>★</span>
                                            ))}
                                        </div>
                                    </td>
                                    <td>{getRiskBadge(emp.risk)}</td>
                                    <td>
                                        <button className="text-zinc-500 hover:text-white p-1">
                                            <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M5 12h.01M12 12h.01M19 12h.01M6 12a1 1 0 11-2 0 1 1 0 012 0zm7 0a1 1 0 11-2 0 1 1 0 012 0zm7 0a1 1 0 11-2 0 1 1 0 012 0z" />
                                            </svg>
                                        </button>
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            </main>
        </div>
    );
}
