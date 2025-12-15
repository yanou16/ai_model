'use client';

import React, { useState, useRef, useEffect } from 'react';
import { usePrediction } from '../context/PredictionContext';

interface Message {
    role: 'system' | 'user' | 'assistant';
    content: string;
}

export default function ChatAssistant() {
    const { formData, predictionResult } = usePrediction();
    const [isOpen, setIsOpen] = useState(false);
    const [messages, setMessages] = useState<Message[]>([
        { role: 'system', content: "Bonjour ! Je suis votre Expert RH IA. Je peux vous aider à interpréter les résultats ou répondre à vos questions." }
    ]);
    const [inputText, setInputText] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const [selectedProvider, setSelectedProvider] = useState<'gemini' | 'groq'>('gemini');
    const messagesEndRef = useRef<HTMLDivElement>(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages, isOpen]);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!inputText.trim()) return;

        const userMsg: Message = { role: 'user', content: inputText };
        setMessages(prev => [...prev, userMsg]);
        setInputText('');
        setIsLoading(true);

        try {
            const response = await fetch('http://localhost:5000/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    message: userMsg.content,
                    provider: selectedProvider,
                    employee_data: formData,
                    prediction_result: predictionResult
                }),
            });
            const data = await response.json();
            setMessages(prev => [...prev, { role: 'assistant', content: data.reply }]);
        } catch (error) {
            console.error("Erreur chat:", error);
            setMessages(prev => [...prev, { role: 'assistant', content: "Erreur de connexion au serveur." }]);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="fixed bottom-6 right-6 z-50 flex flex-col items-end">
            {isOpen && (
                <div className="mb-3 w-80 h-96 bg-zinc-900 rounded-xl border border-zinc-800 flex flex-col overflow-hidden shadow-2xl">
                    {/* Header */}
                    <div className="px-4 py-3 border-b border-zinc-800 flex items-center justify-between bg-zinc-900">
                        <div className="flex items-center gap-2">
                            <div className="w-7 h-7 rounded-lg bg-indigo-600 flex items-center justify-center text-sm">🤖</div>
                            <span className="font-medium text-white text-sm">Expert RH</span>
                        </div>
                        <div className="flex items-center gap-2">
                            <select
                                value={selectedProvider}
                                onChange={(e) => setSelectedProvider(e.target.value as 'gemini' | 'groq')}
                                className="text-xs bg-zinc-800 text-zinc-400 border border-zinc-700 rounded px-2 py-1"
                            >
                                <option value="gemini">Gemini</option>
                                <option value="groq">Groq</option>
                            </select>
                            <button onClick={() => setIsOpen(false)} className="text-zinc-500 hover:text-white text-lg">×</button>
                        </div>
                    </div>

                    {/* Messages */}
                    <div className="flex-1 overflow-y-auto p-3 space-y-3">
                        {messages.map((msg, idx) => (
                            <div key={idx} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                                <div className={`max-w-[80%] px-3 py-2 rounded-lg text-sm ${
                                    msg.role === 'user'
                                        ? 'bg-indigo-600 text-white'
                                        : 'bg-zinc-800 text-zinc-200'
                                }`}>
                                    {msg.content}
                                </div>
                            </div>
                        ))}
                        {isLoading && (
                            <div className="flex justify-start">
                                <div className="bg-zinc-800 px-3 py-2 rounded-lg text-sm text-zinc-400">
                                    <span className="animate-pulse">Réponse...</span>
                                </div>
                            </div>
                        )}
                        <div ref={messagesEndRef} />
                    </div>

                    {/* Input */}
                    <form onSubmit={handleSubmit} className="p-3 border-t border-zinc-800 flex gap-2">
                        <input
                            type="text"
                            value={inputText}
                            onChange={(e) => setInputText(e.target.value)}
                            placeholder="Posez une question..."
                            className="flex-1 px-3 py-2 rounded-lg bg-zinc-800 border border-zinc-700 text-sm text-white placeholder-zinc-500 focus:outline-none focus:border-indigo-500"
                        />
                        <button
                            type="submit"
                            disabled={isLoading}
                            className="px-3 py-2 rounded-lg bg-indigo-600 text-white text-sm hover:bg-indigo-500 disabled:opacity-50"
                        >
                            →
                        </button>
                    </form>
                </div>
            )}

            {/* Toggle Button */}
            <button
                onClick={() => setIsOpen(!isOpen)}
                className="w-12 h-12 rounded-xl bg-indigo-600 hover:bg-indigo-500 flex items-center justify-center text-white text-xl shadow-lg transition-colors"
            >
                {isOpen ? '×' : '💬'}
            </button>
        </div>
    );
}
