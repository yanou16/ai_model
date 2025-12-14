'use client';

import React, { createContext, useContext, useState, ReactNode } from 'react';

// Type pour les données du formulaire (partiel ou complet)
interface EmployeeData {
    [key: string]: any;
}

interface PredictionContextType {
    formData: EmployeeData;
    setFormData: (data: EmployeeData) => void;
    predictionResult: any;
    setPredictionResult: (result: any) => void;
}

const PredictionContext = createContext<PredictionContextType | undefined>(undefined);

export function PredictionProvider({ children }: { children: ReactNode }) {
    const [formData, setFormData] = useState<EmployeeData>({});
    const [predictionResult, setPredictionResult] = useState<any>(null);

    return (
        <PredictionContext.Provider value={{ formData, setFormData, predictionResult, setPredictionResult }}>
            {children}
        </PredictionContext.Provider>
    );
}

export function usePrediction() {
    const context = useContext(PredictionContext);
    if (context === undefined) {
        throw new Error('usePrediction must be used within a PredictionProvider');
    }
    return context;
}
