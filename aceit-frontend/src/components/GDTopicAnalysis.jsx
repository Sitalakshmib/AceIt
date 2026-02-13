import React, { useState } from 'react';
import axios from 'axios';
import { Copy, Check, MessageSquare, ThumbsUp, ThumbsDown, X, Search, Lightbulb, Info } from 'lucide-react';

const GDTopicAnalysis = () => {
    const [topic, setTopic] = useState('');
    const [loading, setLoading] = useState(false);
    const [result, setResult] = useState(null);
    const [error, setError] = useState(null);
    const [copiedIndex, setCopiedIndex] = useState(null);

    const API_URL = 'http://localhost:8000';

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

    const handleNewTopic = () => {
        setTopic('');
        setResult(null);
        setError(null);
    };

    return (
        <div className="p-6">

            {/* About Topic Analysis Section */}
            <div className="bg-gradient-to-br from-indigo-50 to-purple-50 rounded-3xl p-6 border border-indigo-200 mb-8">
                <div className="flex items-start space-x-4">
                    <div className="w-12 h-12 bg-indigo-600 rounded-xl flex items-center justify-center flex-shrink-0">
                        <Info className="w-6 h-6 text-white" />
                    </div>
                    <div className="flex-1">
                        <h3 className="text-xl font-bold text-slate-800 mb-2">About Topic Analysis</h3>
                        <p className="text-slate-700 leading-relaxed mb-4">
                            Enter any Group Discussion topic and our AI will generate balanced FOR and AGAINST arguments.
                            This helps you prepare comprehensively by understanding both sides of the debate, identify key talking points,
                            and build well-rounded perspectives for your GD sessions.
                        </p>
                        <div className="grid grid-cols-1 md:grid-cols-3 gap-3 text-sm">
                            <div className="flex items-start space-x-2">
                                <Lightbulb className="w-4 h-4 text-indigo-600 mt-0.5 flex-shrink-0" />
                                <span className="text-slate-600"><strong>Prepare Both Sides:</strong> Understand multiple perspectives</span>
                            </div>
                            <div className="flex items-start space-x-2">
                                <Lightbulb className="w-4 h-4 text-indigo-600 mt-0.5 flex-shrink-0" />
                                <span className="text-slate-600"><strong>Build Arguments:</strong> Get structured talking points</span>
                            </div>
                            <div className="flex items-start space-x-2">
                                <Lightbulb className="w-4 h-4 text-indigo-600 mt-0.5 flex-shrink-0" />
                                <span className="text-slate-600"><strong>Quick Reference:</strong> Copy points for later study</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            {/* Input Area */}
            <div className="bg-white rounded-3xl shadow-xl p-8 mb-8 border border-slate-200">
                <div className="flex items-center mb-6">
                    <div className="w-12 h-12 bg-indigo-100 rounded-xl flex items-center justify-center mr-4">
                        <MessageSquare className="h-6 w-6 text-indigo-600" />
                    </div>
                    <div>
                        <h3 className="text-2xl font-bold text-gray-900">Generate <span className="text-emerald-600">FOR</span>/<span className="text-rose-600">AGAINST</span> Points</h3>
                        <p className="text-sm text-gray-500">Enter a topic to generate balanced arguments</p>
                    </div>
                </div>

                <div className="flex gap-4">
                    <input
                        type="text"
                        value={topic}
                        onChange={(e) => setTopic(e.target.value)}
                        placeholder="Enter GD Topic (e.g., 'Remote Work: Boon or Bane')"
                        className="flex-1 px-5 py-4 rounded-xl border-2 border-gray-200 focus:border-indigo-500 focus:ring-4 focus:ring-indigo-100 outline-none transition-all text-lg"
                        onKeyDown={(e) => e.key === 'Enter' && handleGenerate()}
                    />
                    <button
                        onClick={handleGenerate}
                        disabled={loading || !topic.trim()}
                        className={`px-8 py-4 rounded-xl font-bold text-white transition-all transform hover:scale-105 active:scale-95 flex items-center gap-3 shadow-lg
                            ${loading || !topic.trim() ? 'bg-gray-400 cursor-not-allowed' : 'bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700'}`}
                    >
                        {loading ? (
                            <>
                                <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin" />
                                <span>Generating...</span>
                            </>
                        ) : (
                            <>
                                <Search className="w-5 h-5" />
                                <span>Generate Points</span>
                            </>
                        )}
                    </button>
                </div>
            </div>

            {/* Error Message */}
            {error && (
                <div className="mb-6 p-5 bg-red-50 text-red-700 rounded-2xl border border-red-200 flex items-center">
                    <X className="w-5 h-5 mr-3 flex-shrink-0" />
                    <span>{error}</span>
                </div>
            )}

            {/* Results */}
            {result && (
                <div className="animate-fadeIn">
                    <div className="flex items-center justify-between mb-6">
                        <div>
                            <h3 className="text-2xl font-bold text-slate-800">Analysis Results</h3>
                            <p className="text-slate-600 mt-1">Topic: <span className="font-semibold">{result.topic}</span></p>
                        </div>
                        <button
                            onClick={handleNewTopic}
                            className="px-6 py-3 bg-gradient-to-r from-blue-600 to-indigo-600 text-white rounded-xl hover:from-blue-700 hover:to-indigo-700 transition-all shadow-md hover:shadow-lg font-semibold"
                        >
                            New Topic
                        </button>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                        {/* FOR Points */}
                        <div className="bg-emerald-50 rounded-2xl shadow-lg border-2 border-emerald-200 p-8 transition-all hover:shadow-xl">
                            <div className="flex justify-between items-center mb-6 pb-4 border-b border-gray-100">
                                <div className="flex items-center gap-3">
                                    <div className="p-3 bg-emerald-50 rounded-xl">
                                        <ThumbsUp size={24} className="text-emerald-600" />
                                    </div>
                                    <h4 className="font-bold text-gray-800 text-xl">Arguments <span className="text-emerald-600">FOR</span></h4>
                                </div>
                                <button
                                    onClick={() => copyToClipboard(result.for_points.join('\n'), 'for')}
                                    className="p-3 text-gray-400 hover:text-emerald-600 hover:bg-emerald-50 rounded-xl transition-all"
                                    title="Copy All FOR Points"
                                >
                                    {copiedIndex === 'for' ? <Check size={20} /> : <Copy size={20} />}
                                </button>
                            </div>
                            <ul className="space-y-4">
                                {result.for_points.map((point, i) => (
                                    <li key={i} className="flex gap-3 text-gray-700 leading-relaxed">
                                        <div className="mt-1 flex-shrink-0">
                                            <Check size={18} className="text-emerald-500" />
                                        </div>
                                        <span className="text-base">{point}</span>
                                    </li>
                                ))}
                            </ul>
                        </div>

                        {/* AGAINST Points */}
                        <div className="bg-rose-50 rounded-2xl shadow-lg border-2 border-rose-200 p-8 transition-all hover:shadow-xl">
                            <div className="flex justify-between items-center mb-6 pb-4 border-b border-gray-100">
                                <div className="flex items-center gap-3">
                                    <div className="p-3 bg-rose-50 rounded-xl">
                                        <ThumbsDown size={24} className="text-rose-600" />
                                    </div>
                                    <h4 className="font-bold text-gray-800 text-xl">Arguments <span className="text-rose-600">AGAINST</span></h4>
                                </div>
                                <button
                                    onClick={() => copyToClipboard(result.against_points.join('\n'), 'against')}
                                    className="p-3 text-gray-400 hover:text-rose-600 hover:bg-rose-50 rounded-xl transition-all"
                                    title="Copy All AGAINST Points"
                                >
                                    {copiedIndex === 'against' ? <Check size={20} /> : <Copy size={20} />}
                                </button>
                            </div>
                            <ul className="space-y-4">
                                {result.against_points.map((point, i) => (
                                    <li key={i} className="flex gap-3 text-gray-700 leading-relaxed">
                                        <div className="mt-1 flex-shrink-0">
                                            <X size={18} className="text-rose-500" />
                                        </div>
                                        <span className="text-base">{point}</span>
                                    </li>
                                ))}
                            </ul>
                        </div>
                    </div>

                    {/* Usage Tips */}
                    <div className="mt-8 bg-gradient-to-br from-blue-50 to-indigo-50 rounded-2xl p-6 border border-blue-200">
                        <div className="flex items-start space-x-3">
                            <Lightbulb className="w-5 h-5 text-blue-600 mt-1 flex-shrink-0" />
                            <div>
                                <h4 className="font-bold text-slate-800 mb-2">How to Use These Points</h4>
                                <ul className="text-sm text-slate-700 space-y-1">
                                    <li>• Study both FOR and AGAINST points to understand the complete picture</li>
                                    <li>• Use these as a foundation to build your own arguments</li>
                                    <li>• Add supporting examples and data to make points more convincing</li>
                                    <li>• Practice articulating these points clearly and confidently</li>
                                    <li>• Be prepared to switch perspectives during the discussion</li>
                                </ul>
                            </div>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
};

export default GDTopicAnalysis;
