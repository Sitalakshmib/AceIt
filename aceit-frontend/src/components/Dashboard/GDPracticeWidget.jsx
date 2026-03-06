import React, { useState } from 'react';
import axios from 'axios';
import { Copy, Check, MessageSquare, ThumbsUp, ThumbsDown, X } from 'lucide-react';

const GDPracticeWidget = () => {
    const [topic, setTopic] = useState('');
    const [loading, setLoading] = useState(false);
    const [result, setResult] = useState(null);
    const [error, setError] = useState(null);
    const [copiedIndex, setCopiedIndex] = useState(null);

    const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

    const handleGenerate = async () => {
        if (!topic.trim()) return;

        setLoading(true);
        setError(null);
        setResult(null);

        try {
            const response = await axios.post(`${API_URL}/gd-practice/generate`, { topic });

            if (response.data.status === 'error') {
                setError(response.data.message);
            } else {
                setResult(response.data);
            }
        } catch (err) {
            console.error(err);
            setError('Failed to generate points. Please check your connection.');
        } finally {
            setLoading(false);
        }
    };

    const copyToClipboard = (text, index) => {
        navigator.clipboard.writeText(text);
        setCopiedIndex(index);
        setTimeout(() => setCopiedIndex(null), 2000);
    };

    return (
        <div className="bg-white rounded-2xl shadow-lg p-6 mb-8 border border-gray-100">
            <div className="flex items-center mb-6">
                <div className="bg-indigo-100 p-2 rounded-lg mr-3">
                    <MessageSquare className="h-6 w-6 text-indigo-600" />
                </div>
                <div>
                    <h3 className="text-xl font-bold text-gray-900">Group Discussion (GD) Practice</h3>
                    <p className="text-sm text-gray-500">Quickly generate balanced points for any topic</p>
                </div>
            </div>

            {/* Input Area */}
            <div className="flex gap-4 mb-6">
                <input
                    type="text"
                    value={topic}
                    onChange={(e) => setTopic(e.target.value)}
                    placeholder="Enter GD Topic (e.g., 'Remote Work: Boon or Bane')"
                    className="flex-1 px-4 py-3 rounded-xl border border-gray-200 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200 outline-none transition-all"
                    onKeyDown={(e) => e.key === 'Enter' && handleGenerate()}
                />
                <button
                    onClick={handleGenerate}
                    disabled={loading || !topic.trim()}
                    className={`px-6 py-3 rounded-xl font-bold text-white transition-all transform hover:scale-105 active:scale-95 flex items-center gap-2
                        ${loading || !topic.trim() ? 'bg-gray-400 cursor-not-allowed' : 'bg-indigo-600 hover:bg-indigo-700 shadow-md'}`}
                >
                    {loading ? (
                        <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin" />
                    ) : (
                        'Generate Points'
                    )}
                </button>
            </div>

            {/* Error Message */}
            {error && (
                <div className="mb-6 p-4 bg-red-50 text-red-700 rounded-xl border border-red-100 flex items-center">
                    <span className="mr-2"></span> {error}
                </div>
            )}

            {/* Results */}
            {result && (
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6 animate-fadeIn">
                    {/* FOR Points */}
                    <div className="bg-white rounded-xl shadow-sm border-t-4 border-emerald-500 p-6 transition-all hover:shadow-md">
                        <div className="flex justify-between items-center mb-6 pb-4 border-b border-gray-100">
                            <div className="flex items-center gap-2">
                                <div className="p-2 bg-emerald-50 rounded-lg">
                                    <ThumbsUp size={20} className="text-emerald-600" />
                                </div>
                                <h4 className="font-bold text-gray-800 text-lg">Arguments <span className="text-emerald-600">FOR</span></h4>
                            </div>
                            <button
                                onClick={() => copyToClipboard(result.for_points.join('\n'), 'for')}
                                className="p-2 text-gray-400 hover:text-emerald-600 hover:bg-emerald-50 rounded-full transition-all"
                                title="Copy All"
                            >
                                {copiedIndex === 'for' ? <Check size={18} /> : <Copy size={18} />}
                            </button>
                        </div>
                        <ul className="space-y-4">
                            {result.for_points.map((point, i) => (
                                <li key={i} className="flex gap-3 text-gray-600 leading-relaxed">
                                    <div className="mt-1 flex-shrink-0">
                                        <Check size={16} className="text-emerald-500" />
                                    </div>
                                    <span>{point}</span>
                                </li>
                            ))}
                        </ul>
                    </div>

                    {/* AGAINST Points */}
                    <div className="bg-white rounded-xl shadow-sm border-t-4 border-rose-500 p-6 transition-all hover:shadow-md">
                        <div className="flex justify-between items-center mb-6 pb-4 border-b border-gray-100">
                            <div className="flex items-center gap-2">
                                <div className="p-2 bg-rose-50 rounded-lg">
                                    <ThumbsDown size={20} className="text-rose-600" />
                                </div>
                                <h4 className="font-bold text-gray-800 text-lg">Arguments <span className="text-rose-600">AGAINST</span></h4>
                            </div>
                            <button
                                onClick={() => copyToClipboard(result.against_points.join('\n'), 'against')}
                                className="p-2 text-gray-400 hover:text-rose-600 hover:bg-rose-50 rounded-full transition-all"
                                title="Copy All"
                            >
                                {copiedIndex === 'against' ? <Check size={18} /> : <Copy size={18} />}
                            </button>
                        </div>
                        <ul className="space-y-4">
                            {result.against_points.map((point, i) => (
                                <li key={i} className="flex gap-3 text-gray-600 leading-relaxed">
                                    <div className="mt-1 flex-shrink-0">
                                        <X size={16} className="text-rose-500" />
                                    </div>
                                    <span>{point}</span>
                                </li>
                            ))}
                        </ul>
                    </div>
                </div>
            )}
        </div>
    );
};

export default GDPracticeWidget;
