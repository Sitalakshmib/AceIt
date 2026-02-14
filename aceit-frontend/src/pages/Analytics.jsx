import React, { useState, useEffect } from 'react';
import { analyticsAPI, API_BASE_URL } from '../services/api';
import { useNavigate } from 'react-router-dom';
import { LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, Cell, AreaChart, Area } from 'recharts';
import {
    Trophy, Target, Zap, Brain, TrendingUp, AlertCircle,
    CheckCircle2, HelpCircle, ArrowUpRight, Sparkles,
    Mic, Send, X, Volume2, Square, Play, Pause, RotateCcw, ArrowLeft
} from 'lucide-react';

import AICoachChat from '../components/AICoachChat';

const Analytics = () => {
    const navigate = useNavigate();
    const [loading, setLoading] = useState(true);
    const [aiLoading, setAiLoading] = useState(false);
    const [error, setError] = useState('');
    const [dailyData, setDailyData] = useState([]);
    const [mockReport, setMockReport] = useState(null);
    const [aiAdvice, setAiAdvice] = useState(null);
    const [summary, setSummary] = useState(null);

    useEffect(() => {
        fetchAllData();
    }, []);

    const fetchAllData = async () => {
        try {
            setLoading(true);
            // Fetch core data first (instant DB queries)
            const [dailyRes, reportRes, summaryRes] = await Promise.all([
                analyticsAPI.getDailyProgress(7),
                analyticsAPI.getMockReport(),
                analyticsAPI.getOverallSummary()
            ]);

            setDailyData(dailyRes.data.data || []);
            setMockReport(reportRes.data.data || null);
            setSummary(summaryRes.data.data || null);
            setLoading(false);

            // Fetch AI Coach data asynchronously (slower LLM call)
            fetchAIInsight();
        } catch (err) {
            console.error('Failed to fetch analytics:', err);
            setError('Failed to load your latest performance data.');
            setLoading(false);
        }
    };

    const fetchAIInsight = async () => {
        try {
            setAiLoading(true);
            const aiRes = await analyticsAPI.getAICoach();
            setAiAdvice(aiRes.data.data || null);
        } catch (err) {
            console.error('AI Coach fetch failed:', err);
        } finally {
            setAiLoading(false);
        }
    };

    if (loading) {
        return (
            <div className="flex flex-col items-center justify-center py-20">
                <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500 mb-4"></div>
                <p className="text-gray-500 animate-pulse">Analyzing your mock performance...</p>
            </div>
        );
    }

    if (error) {
        return (
            <div className="p-8 bg-red-50 border border-red-200 rounded-2xl text-center">
                <AlertCircle className="h-12 w-12 text-red-500 mx-auto mb-4" />
                <h3 className="text-lg font-bold text-red-800 mb-2">Analysis Failed</h3>
                <p className="text-red-600 mb-6">{error}</p>
                <button onClick={fetchAllData} className="px-6 py-2 bg-red-600 text-white rounded-xl hover:bg-red-700 transition-colors">
                    Try Again
                </button>
            </div>
        );
    }

    return (
        <div className="p-8 max-w-7xl mx-auto space-y-8 animate-in fade-in duration-700 relative">
            {/* Back to Dashboard Button */}
            <button
                onClick={() => navigate('/')}
                className="absolute top-0 left-0 flex items-center gap-2 px-4 py-2 bg-white border border-gray-200 text-gray-600 font-bold rounded-xl hover:bg-gray-50 hover:text-blue-600 transition-all shadow-sm group mt-4 ml-4 z-50"
            >
                <ArrowLeft className="h-5 w-5 group-hover:-translate-x-1 transition-transform" />
                Dashboard
            </button>
            {/* AI Coach Floating Bot */}
            <AICoachChat summary={summary} />

            {/* 1. Header & Quick Stats */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div className="bg-white p-6 rounded-2xl shadow-sm border border-gray-100 flex items-center group hover:border-blue-200 transition-all">
                    <div className="p-4 bg-blue-50 rounded-xl mr-5 group-hover:scale-110 transition-transform">
                        <Trophy className="h-6 w-6 text-blue-600" />
                    </div>
                    <div>
                        <p className="text-sm font-semibold text-gray-400 uppercase tracking-wider">Exam Confidence</p>
                        <h3 className="text-2xl font-black text-gray-800">{summary?.exam_confidence || 0}%</h3>
                        <p className="text-xs text-blue-500 font-medium">Based on last 7 days</p>
                    </div>
                </div>

                <div className="bg-white p-6 rounded-2xl shadow-sm border border-gray-100 flex items-center group hover:border-green-200 transition-all">
                    <div className="p-4 bg-green-50 rounded-xl mr-5 group-hover:scale-110 transition-transform">
                        <Trophy className="h-6 w-6 text-green-600" />
                    </div>
                    <div>
                        <p className="text-sm font-semibold text-gray-400 uppercase tracking-wider">Total Tests</p>
                        <h3 className="text-2xl font-black text-gray-800">{summary?.total_mocks || 0}</h3>
                        <p className="text-xs text-green-500 font-medium">Completed</p>
                    </div>
                </div>

                <div className="bg-white p-6 rounded-2xl shadow-sm border border-gray-100 flex items-center group hover:border-orange-200 transition-all">
                    <div className="p-4 bg-orange-50 rounded-xl mr-5 group-hover:scale-110 transition-transform">
                        <Zap className="h-6 w-6 text-orange-600" />
                    </div>
                    <div>
                        <p className="text-sm font-semibold text-gray-400 uppercase tracking-wider">Day Streak</p>
                        <h3 className="text-2xl font-black text-gray-800">{summary?.current_streak || 0}</h3>
                        <p className="text-xs text-orange-500 font-medium text-nowrap">Current Streak</p>
                    </div>
                </div>
            </div>

            {/* 2. Main Analytics Row: Grid layout adapted for dashboard */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">

                {/* Daily Progress Histogram */}
                <div className="bg-white p-8 rounded-2xl shadow-sm border border-gray-100">
                    <div className="flex justify-between items-center mb-8">
                        <div>
                            <h3 className="text-xl font-bold text-gray-800">Daily Progress</h3>
                            <p className="text-sm text-gray-500">Your mock accuracy trend over the last 7 days</p>
                        </div>
                        <div className="bg-blue-50 text-blue-600 px-3 py-1 rounded-full text-xs font-bold">LIVE UPDATE</div>
                    </div>

                    <div className="h-72 w-full">
                        <ResponsiveContainer width="100%" height="100%">
                            <BarChart data={dailyData}>
                                <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#f0f0f0" />
                                <XAxis
                                    dataKey="date"
                                    axisLine={false}
                                    tickLine={false}
                                    tick={{ fontSize: 12, fill: '#94a3b8' }}
                                    tickFormatter={(val) => new Date(val).toLocaleDateString(undefined, { weekday: 'short' })}
                                />
                                <YAxis
                                    domain={[0, 100]}
                                    axisLine={false}
                                    tickLine={false}
                                    tick={{ fontSize: 12, fill: '#94a3b8' }}
                                />
                                <Tooltip
                                    cursor={{ fill: 'transparent' }}
                                    contentStyle={{ borderRadius: '12px', border: 'none', boxShadow: '0 10px 15px -3px rgb(0 0 0 / 0.1)' }}
                                />
                                <Bar dataKey="accuracy" radius={[8, 8, 8, 8]}>
                                    {dailyData.map((entry, index) => (
                                        <Cell key={`cell-${index}`} fill={['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#ec4899', '#06b6d4'][index % 7]} />
                                    ))}
                                </Bar>
                            </BarChart>
                        </ResponsiveContainer>
                    </div>
                </div>

                {/* AI Smart Coach */}
                <div className="bg-gradient-to-br from-pink-50 to-rose-100 p-8 rounded-2xl shadow-xl text-gray-800 relative overflow-hidden border border-pink-100">
                    <div className="absolute top-0 right-0 p-4 opacity-10">
                        <Sparkles className="h-32 w-32 text-pink-600" />
                    </div>

                    <div className="relative z-10">
                        <div className="flex items-center mb-6">
                            <div className="p-3 bg-white rounded-xl shadow-sm">
                                <Brain className="h-6 w-6 text-pink-500" />
                            </div>
                            <h3 className="ml-4 text-xl font-bold text-gray-900">Personalized Focus Plan</h3>
                        </div>

                        {aiLoading ? (
                            <div className="space-y-4 animate-pulse">
                                <div className="h-20 bg-white/50 rounded-2xl w-full"></div>
                                <div className="h-8 bg-white/50 rounded-xl w-3/4"></div>
                                <div className="h-8 bg-white/50 rounded-xl w-5/6"></div>
                                <div className="h-8 bg-white/50 rounded-xl w-1/2"></div>
                            </div>
                        ) : aiAdvice ? (
                            <div className="space-y-6">


                                <div>
                                    <h5 className="text-xs font-bold uppercase tracking-widest text-pink-500 mb-3 ml-1">Today's Focus Plan</h5>
                                    <div className="space-y-3">
                                        {aiAdvice.action_plan.map((item, idx) => (
                                            <div key={idx} className="flex items-center text-sm bg-white/40 p-3 rounded-xl border border-white/50">
                                                <div className="h-2 w-2 rounded-full bg-pink-500 mr-3 shrink-0"></div>
                                                {item}
                                            </div>
                                        ))}
                                    </div>
                                </div>
                            </div>
                        ) : (
                            <div className="text-center py-10">
                                <HelpCircle className="h-12 w-12 mx-auto mb-4 opacity-50 text-pink-400" />
                                <p className="text-pink-800">Take a few more mocks for the AI to build your strategy.</p>
                            </div>
                        )}
                    </div>
                </div>
            </div>

            {/* 3. Strength & Weakness Matrix */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                <div className="bg-white p-8 rounded-2xl shadow-sm border border-gray-100 relative group overflow-hidden">
                    <div className="absolute top-0 left-0 w-1 h-full bg-green-500"></div>
                    <div className="flex items-center justify-between mb-6">
                        <h3 className="text-xl font-bold text-gray-800 flex items-center">
                            <CheckCircle2 className="h-5 w-5 text-green-500 mr-2" />
                            Proven Strengths
                        </h3>
                        <span className="text-xs font-bold text-green-600 bg-green-50 px-2 py-1 rounded">MOCK DATA</span>
                    </div>

                    <div className="flex flex-wrap gap-3">
                        {mockReport?.strengths?.length > 0 ? (
                            mockReport.strengths.map((topic, idx) => (
                                <div key={idx} className="px-4 py-2 bg-green-50 text-green-700 rounded-xl text-sm font-semibold border border-green-100">
                                    {topic}
                                </div>
                            ))
                        ) : (
                            <div className="text-gray-400 italic text-sm py-4">Maintain 75%+ in mock tests to unlock strengths.</div>
                        )}
                    </div>
                </div>

                <div className="bg-white p-8 rounded-2xl shadow-sm border border-gray-100 relative group overflow-hidden">
                    <div className="absolute top-0 left-0 w-1 h-full bg-red-500"></div>
                    <div className="flex items-center justify-between mb-6">
                        <h3 className="text-xl font-bold text-gray-800 flex items-center">
                            <TrendingUp className="h-5 w-5 text-red-500 mr-2" />
                            Guidance Needed
                        </h3>
                        <span className="text-xs font-bold text-red-600 bg-red-50 px-2 py-1 rounded">TOP PRIORITY</span>
                    </div>

                    <div className="flex flex-wrap gap-3">
                        {mockReport?.weaknesses?.length > 0 ? (
                            mockReport.weaknesses.map((topic, idx) => (
                                <div key={idx} className="px-4 py-2 bg-red-50 text-red-700 rounded-xl text-sm font-semibold border border-red-100">
                                    {topic}
                                </div>
                            ))
                        ) : (
                            <div className="text-gray-400 italic text-sm py-4 text-nowrap">Great job! All topics are currently in stable zones.</div>
                        )}
                    </div>
                </div>
            </div>

            {/* 4. Empty State Fallback */}
            {
                dailyData.length === 0 && (
                    <div className="bg-gray-50 border border-dashed border-gray-300 rounded-3xl p-12 text-center">
                        <div className="bg-white w-20 h-20 rounded-full flex items-center justify-center mx-auto mb-6 shadow-sm">
                            <Target className="h-10 w-10 text-gray-300" />
                        </div>
                        <h3 className="text-xl font-bold text-gray-800 mb-2">No Mock Analytics Yet</h3>
                        <p className="text-gray-500 max-w-sm mx-auto mb-8">
                            Take your first full-length or topic test to see daily progress and AI insights.
                        </p>
                        <button
                            className="px-8 py-3 bg-blue-600 text-white rounded-xl font-bold hover:bg-blue-700 transition-all shadow-lg shadow-blue-200"
                            onClick={() => window.location.reload()}
                        >
                            Refresh Dashboard
                        </button>
                    </div>
                )
            }
        </div >
    );
};

export default Analytics;
