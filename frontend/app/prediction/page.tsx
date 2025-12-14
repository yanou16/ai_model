'use client';

import { useState } from 'react';
import Link from 'next/link';
import { usePrediction } from '../context/PredictionContext';

interface PredictionResult {
    prediction: {
        will_leave: boolean;
        label: string;
    };
    probabilities: {
        stay: number;
        leave: number;
    };
    risk_level: string;
    recommendations: string[];
}

export default function PredictionPage() {
    const { setFormData, predictionResult, setPredictionResult } = usePrediction();
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
    // const [result, setResult] = useState<PredictionResult | null>(null); // Use context instead

    const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        setLoading(true);
        setError('');
        setPredictionResult(null);

        const formData = new FormData(e.currentTarget);
        const data: Record<string, any> = {};
        const intFields = ['Age', 'DistanceFromHome', 'Education', 'JobLevel', 'MonthlyIncome',
            'TotalWorkingYears', 'YearsAtCompany', 'YearsWithCurrManager',
            'YearsSinceLastPromotion', 'NumCompaniesWorked', 'PercentSalaryHike',
            'StockOptionLevel', 'TrainingTimesLastYear', 'EnvironmentSatisfaction',
            'JobSatisfaction', 'WorkLifeBalance', 'JobInvolvement',
            'PerformanceRating', 'LateArrivals'];

        const floatFields = ['AvgWorkingHours', 'AvgOvertime', 'AbsenceRate', 'WorkHoursVariance'];

        formData.forEach((value, key) => {
            if (intFields.includes(key)) {
                data[key] = parseInt(value as string);
            } else if (floatFields.includes(key)) {
                data[key] = parseFloat(value as string);
            } else {
                data[key] = value;
            }
        });

        // Store in context for Chatbot
        setFormData(data);

        try {
            const response = await fetch('http://localhost:5000/predict', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });

            if (!response.ok) throw new Error(`Erreur HTTP: ${response.status}`);

            const result = await response.json();
            setPredictionResult(result);
        } catch (err: any) {
            setError(`❌ Erreur: ${err.message}. Assurez-vous que l'API est démarrée (python api.py)`);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="min-h-screen pb-20">
            {/* Navigation */}
            <nav className="fixed top-0 w-full bg-dark/80 backdrop-blur-lg border-b border-emerald/20 z-50">
                <div className="max-w-7xl mx-auto px-6 py-4 flex justify-between items-center">
                    <Link href="/" className="text-2xl font-bold bg-gradient-to-r from-emerald to-emerald-light bg-clip-text text-transparent">
                        AttritionAI
                    </Link>
                    <Link href="/" className="text-light/70 hover:text-emerald-light transition-colors">
                        ← Retour à l'accueil
                    </Link>
                </div>
            </nav>

            {/* Main Content */}
            <div className="max-w-5xl mx-auto px-6 pt-32">
                <div className="bg-dark-light/50 border border-emerald/20 rounded-3xl p-10">
                    <h1 className="text-4xl font-bold mb-3 bg-gradient-to-r from-emerald to-emerald-light bg-clip-text text-transparent">
                        🎯 Prédiction d'Attrition
                    </h1>
                    <p className="text-light/70 mb-8 text-lg">
                        Entrez les informations de l'employé pour obtenir une prédiction éthique et des recommandations humaines
                    </p>

                    <form onSubmit={handleSubmit} className="space-y-8">
                        {/* Informations Démographiques */}
                        <Section title="👤 Informations Démographiques">
                            <div className="grid md:grid-cols-2 gap-6">
                                <Input label="Âge" name="Age" type="number" defaultValue="35" min="18" max="70" />
                                <Select label="Genre" name="Gender" options={[
                                    { value: 'Male', label: 'Homme' },
                                    { value: 'Female', label: 'Femme' }
                                ]} />
                                <Select label="Statut Marital" name="MaritalStatus" options={[
                                    { value: 'Single', label: 'Célibataire' },
                                    { value: 'Married', label: 'Marié(e)' },
                                    { value: 'Divorced', label: 'Divorcé(e)' }
                                ]} defaultValue="Married" />
                                <Input label="Distance du domicile (km)" name="DistanceFromHome" type="number" defaultValue="10" min="0" />
                            </div>
                        </Section>

                        {/* Éducation */}
                        <Section title="🎓 Éducation">
                            <div className="grid md:grid-cols-2 gap-6">
                                <Select label="Niveau d'éducation" name="Education" options={[
                                    { value: '1', label: '1 - Below College' },
                                    { value: '2', label: '2 - College' },
                                    { value: '3', label: '3 - Bachelor' },
                                    { value: '4', label: '4 - Master' },
                                    { value: '5', label: '5 - Doctor' }
                                ]} defaultValue="3" />
                                <Select label="Domaine d'études" name="EducationField" options={[
                                    { value: 'Life Sciences', label: 'Life Sciences' },
                                    { value: 'Medical', label: 'Medical' },
                                    { value: 'Marketing', label: 'Marketing' },
                                    { value: 'Technical Degree', label: 'Technical Degree' },
                                    { value: 'Other', label: 'Other' }
                                ]} />
                            </div>
                        </Section>

                        {/* Informations Professionnelles */}
                        <Section title="💼 Informations Professionnelles">
                            <div className="grid md:grid-cols-2 gap-6">
                                <Select label="Département" name="Department" options={[
                                    { value: 'Sales', label: 'Sales' },
                                    { value: 'Research & Development', label: 'Research & Development' },
                                    { value: 'Human Resources', label: 'Human Resources' }
                                ]} defaultValue="Research & Development" />
                                <Input label="Poste" name="JobRole" defaultValue="Research Scientist" />
                                <Input label="Niveau de poste (1-5)" name="JobLevel" type="number" defaultValue="2" min="1" max="5" />
                                <Input label="Revenu mensuel ($)" name="MonthlyIncome" type="number" defaultValue="5000" min="0" />
                            </div>
                        </Section>

                        {/* Expérience */}
                        <Section title="⏱️ Expérience">
                            <div className="grid md:grid-cols-2 gap-6">
                                <Input label="Années d'expérience totales" name="TotalWorkingYears" type="number" defaultValue="10" min="0" />
                                <Input label="Années dans l'entreprise" name="YearsAtCompany" type="number" defaultValue="5" min="0" />
                                <Input label="Années avec le manager actuel" name="YearsWithCurrManager" type="number" defaultValue="3" min="0" />
                                <Input label="Années depuis dernière promotion" name="YearsSinceLastPromotion" type="number" defaultValue="1" min="0" />
                                <Input label="Nombre d'entreprises précédentes" name="NumCompaniesWorked" type="number" defaultValue="2" min="0" />
                                <Select label="Voyages d'affaires" name="BusinessTravel" options={[
                                    { value: 'Non-Travel', label: 'Non-Travel' },
                                    { value: 'Travel_Rarely', label: 'Travel_Rarely' },
                                    { value: 'Travel_Frequently', label: 'Travel_Frequently' }
                                ]} defaultValue="Travel_Rarely" />
                            </div>
                        </Section>

                        {/* Conditions de Travail */}
                        <Section title="🏢 Conditions de Travail">
                            <div className="grid md:grid-cols-2 gap-6">
                                <Input label="Augmentation salariale (%)" name="PercentSalaryHike" type="number" defaultValue="15" min="0" />
                                <Input label="Niveau d'options d'achat (0-3)" name="StockOptionLevel" type="number" defaultValue="1" min="0" max="3" />
                                <Input label="Formations l'année dernière" name="TrainingTimesLastYear" type="number" defaultValue="3" min="0" />
                                <Input label="Évaluation de performance (3-4)" name="PerformanceRating" type="number" defaultValue="3" min="3" max="4" />
                            </div>
                        </Section>

                        {/* Satisfaction */}
                        <Section title="😊 Satisfaction (échelle 1-4)">
                            <div className="grid md:grid-cols-2 gap-6">
                                <Input label="Satisfaction environnement" name="EnvironmentSatisfaction" type="number" defaultValue="3" min="1" max="4" />
                                <Input label="Satisfaction du travail" name="JobSatisfaction" type="number" defaultValue="4" min="1" max="4" />
                                <Input label="Équilibre vie pro/perso" name="WorkLifeBalance" type="number" defaultValue="3" min="1" max="4" />
                                <Input label="Implication dans le travail" name="JobInvolvement" type="number" defaultValue="3" min="1" max="4" />
                            </div>
                        </Section>

                        {/* Données Temporelles */}
                        <Section title="⏰ Données Temporelles (Optionnel)" subtitle="Ces données sont optionnelles. Des valeurs moyennes seront utilisées si non renseignées.">
                            <div className="grid md:grid-cols-2 gap-6">
                                <Input label="Heures moyennes travaillées/jour" name="AvgWorkingHours" type="number" step="0.1" defaultValue="8.5" min="0" max="24" />
                                <Input label="Nombre de retards (après 9h)" name="LateArrivals" type="number" defaultValue="10" min="0" />
                                <Input label="Heures supplémentaires moyennes/jour" name="AvgOvertime" type="number" step="0.1" defaultValue="0.5" min="0" max="10" />
                                <Input label="Taux d'absence (%)" name="AbsenceRate" type="number" step="0.1" defaultValue="5.0" min="0" max="100" />
                                <Input label="Variance des heures (régularité)" name="WorkHoursVariance" type="number" step="0.1" defaultValue="1.0" min="0" />
                            </div>
                        </Section>

                        {/* Submit Button */}
                        <button
                            type="submit"
                            disabled={loading}
                            className="w-full py-4 bg-gradient-to-r from-emerald to-emerald-dark rounded-xl font-bold text-lg hover:shadow-xl hover:shadow-emerald/40 transition-all transform hover:-translate-y-1 disabled:opacity-60 disabled:cursor-not-allowed disabled:transform-none"
                        >
                            {loading ? '⏳ Analyse en cours...' : '🔍 Prédire l\'Attrition'}
                        </button>
                    </form>

                    {/* Error Message */}
                    {error && (
                        <div className="mt-8 p-6 bg-red-500/10 border border-red-500/30 rounded-xl text-red-400">
                            {error}
                        </div>
                    )}

                    {/* Result */}
                    {predictionResult && (
                        <div className={`mt-8 p-8 rounded-2xl border-2 ${predictionResult.prediction.will_leave
                            ? 'bg-red-500/10 border-red-500/30'
                            : 'bg-emerald/10 border-emerald/30'
                            }`}>
                            <div className={`text-3xl font-bold mb-4 ${predictionResult.prediction.will_leave ? 'text-red-400' : 'text-emerald-light'
                                }`}>
                                {predictionResult.prediction.will_leave ? '⚠️ Risque d\'Attrition: OUI' : '✅ Risque d\'Attrition: NON'}
                            </div>
                            <div className={`text-6xl font-bold my-6 ${predictionResult.prediction.will_leave ? 'text-red-400' : 'text-emerald'
                                }`}>
                                {predictionResult.prediction.will_leave ? predictionResult.probabilities.leave : predictionResult.probabilities.stay}%
                            </div>
                            <div className="mt-6">
                                <h3 className="text-xl font-bold mb-3 text-light">💡 Recommandations:</h3>
                                <ul className="space-y-2">
                                    {predictionResult.recommendations.map((rec: string, i: number) => (
                                        <li key={i} className="flex gap-3 text-light/80">
                                            <span className="text-emerald-light">→</span>
                                            <span>{rec}</span>
                                        </li>
                                    ))}
                                </ul>
                            </div>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}

// Helper Components
function Section({ title, subtitle, children }: { title: string; subtitle?: string; children: React.ReactNode }) {
    return (
        <div>
            <h2 className="text-2xl font-bold text-emerald-light mb-2">{title}</h2>
            {subtitle && <p className="text-light/60 text-sm mb-4">{subtitle}</p>}
            {children}
        </div>
    );
}

function Input({ label, name, type = 'text', defaultValue, ...props }: any) {
    return (
        <div>
            <label className="block text-sm font-semibold text-light/90 mb-2">{label}</label>
            <input
                name={name}
                type={type}
                defaultValue={defaultValue}
                required
                className="w-full px-4 py-3 bg-dark-light border border-emerald/20 rounded-lg text-light focus:outline-none focus:border-emerald focus:ring-2 focus:ring-emerald/20 transition-all"
                {...props}
            />
        </div>
    );
}

function Select({ label, name, options, defaultValue }: any) {
    return (
        <div>
            <label className="block text-sm font-semibold text-light/90 mb-2">{label}</label>
            <select
                name={name}
                defaultValue={defaultValue || options[0].value}
                required
                className="w-full px-4 py-3 bg-dark-light border border-emerald/20 rounded-lg text-light focus:outline-none focus:border-emerald focus:ring-2 focus:ring-emerald/20 transition-all"
            >
                {options.map((opt: any) => (
                    <option key={opt.value} value={opt.value} className="bg-dark-light">
                        {opt.label}
                    </option>
                ))}
            </select>
        </div>
    );
}
