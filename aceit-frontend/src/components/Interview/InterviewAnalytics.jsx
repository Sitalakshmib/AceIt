import React, { useState, useEffect } from 'react';
import {
    ArrowLeft,
    TrendingUp,
    TrendingDown,
    Minus,
    Target,
    Award,
    Zap,
    MessageSquare,
    Users,
    Video,
    BarChart2,
    AlertCircle
} from 'lucide-react';
import axios from 'axios';

// API Base URL
const API_BASE_URL = 'http://localhost:8000';

const InterviewAnalytics = ({ userId, onBack, onStartPractice }) => {
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [analytics, setAnalytics] = useState(null);

    useEffect(() => {
        fetchAnalytics();
    }, [userId]);

    const fetchAnalytics = async () => {
        try {
            setLoading(true);
            const response = await axios.get(`${API_BASE_URL}/interview/analytics/${userId}`);
            setAnalytics(response.data);
            setError(null);
        } catch (err) {
            console.error("Error fetching analytics:", err);
            setError("Failed to load analytics. Please try again later.");
        } finally {
            setLoading(false);
        }
    };

    const getTrendIcon = (trend) => {
        if (trend === 'improving' || trend === 'Improving') return <TrendingUp className="h-4 w-4 text-green-500" />;
        if (trend === 'declining' || trend === 'Needs Focus') return <TrendingDown className="h-4 w-4 text-red-500" />;
        return <Minus className="h-4 w-4 text-gray-400" />;
    };

    const getPerformanceColor = (score) => {
        if (score >= 80) return 'text-green-600 bg-green-50';
        if (score >= 60) return 'text-yellow-600 bg-yellow-50';
        return 'text-red-600 bg-red-50';
    };

    const getProgressColor = (score) => {
        if (score >= 80) return 'bg-green-500';
        if (score >= 60) return 'bg-yellow-500';
        return 'bg-red-500';
    };

    if (loading) {
        return (
            <div className="flex flex-col items-center justify-center min-h-[60vh]">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600 mb-4"></div>
                <p className="text-gray-500">Analysing your interview performance...</p>
            </div>
        );
    }

    if (error) {
        return (
            <div className="flex flex-col items-center justify-center min-h-[60vh] text-center p-8">
                <AlertCircle className="h-16 w-16 text-red-100 text-red-500 mb-4" />
                <h3 className="text-xl font-bold text-gray-900 mb-2">Something went wrong</h3>
                <p className="text-gray-600 mb-6">{error}</p>
                <button
                    onClick={fetchAnalytics}
                    className="px-6 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition"
                >
                    Try Again
                </button>
            </div>
        );
    }

    // Handle empty state
    if (!analytics || !analytics.has_data) {
        return (
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 animate-fade-in">
                {/* Header with Back Button */}
                <div className="flex items-center mb-8">
                    <button
                        onClick={onBack}
                        className="p-2 mr-4 rounded-full hover:bg-gray-100 transition-colors"
                    >
                        <ArrowLeft className="h-6 w-6 text-gray-600" />
                    </button>
                    <div>
                        <h1 className="text-2xl font-bold text-gray-900">Interview Performance Analytics</h1>
                        <p className="text-gray-500">Track your progress across all interview types</p>
                    </div>
                </div>

                <div className="bg-white rounded-[2rem] shadow-xl p-12 text-center max-w-2xl mx-auto">
                    <div className="bg-indigo-50 w-20 h-20 rounded-full flex items-center justify-center mx-auto mb-6">
                        <BarChart2 className="h-10 w-10 text-indigo-600" />
                    </div>
                    <h2 className="text-2xl font-bold text-gray-900 mb-3">No Interview Data Yet</h2>
                    <p className="text-gray-600 mb-8 max-w-md mx-auto">
                        Start your first mock interview to see detailed analytics, strengths, and improvement areas here.
                    </p>

                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                        <button
                            onClick={() => onStartPractice('technical')}
                            className="flex flex-col items-center p-4 border-2 border-gray-100 rounded-xl hover:border-blue-500 hover:bg-blue-50 transition-all group"
                        >
                            <Zap className="h-8 w-8 text-blue-500 mb-2 group-hover:scale-110 transition-transform" />
                            <span className="font-semibold text-gray-900">Technical</span>
                        </button>
                        <button
                            onClick={() => onStartPractice('hr')}
                            className="flex flex-col items-center p-4 border-2 border-gray-100 rounded-xl hover:border-purple-500 hover:bg-purple-50 transition-all group"
                        >
                            <Users className="h-8 w-8 text-purple-500 mb-2 group-hover:scale-110 transition-transform" />
                            <span className="font-semibold text-gray-900">HR Behavioral</span>
                        </button>
                        <button
                            onClick={() => onStartPractice('video')}
                            className="flex flex-col items-center p-4 border-2 border-gray-100 rounded-xl hover:border-rose-500 hover:bg-rose-50 transition-all group"
                        >
                            <Video className="h-8 w-8 text-rose-500 mb-2 group-hover:scale-110 transition-transform" />
                            <span className="font-semibold text-gray-900">Video Presence</span>
                        </button>
                    </div>
                </div>
            </div>
        );
    }

    const { overall, technical, hr, video_presence, skill_insights, recommendations } = analytics;

    return (
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 animate-fade-in font-sans">
            {/* Header */}
            <div className="flex flex-col md:flex-row md:items-center justify-between mb-8 gap-4">
                <div className="flex items-center">
                    <button
                        onClick={onBack}
                        className="p-2 mr-4 rounded-full hover:bg-gray-100 transition-colors"
                    >
                        <ArrowLeft className="h-6 w-6 text-gray-600" />
                    </button>
                    <div>
                        <h1 className="text-3xl font-bold text-gray-900">Interview Performance</h1>
                        <p className="text-gray-500">Holistic view of your interview readiness</p>
                    </div>
                </div>

                {/* Last Interview Badge */}
                {overall.last_interview && (
                    <div className="bg-white px-4 py-2 rounded-full shadow-sm border border-gray-100 text-sm text-gray-600 flex items-center">
                        <span className="w-2 h-2 rounded-full bg-green-500 mr-2"></span>
                        Last activity: {new Date(overall.last_interview).toLocaleDateString()}
                    </div>
                )}
            </div>

            {/* Main Grid Layout */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 mb-8">

                {/* Left Column: Overall Stats */}
                <div className="lg:col-span-1 space-y-6">
                    {/* Overall Score Card */}
                    <div className="bg-white rounded-2xl shadow-lg p-6 border border-gray-100 overflow-hidden relative">
                        <div className="absolute top-0 right-0 w-32 h-32 bg-indigo-50 rounded-full -mr-16 -mt-16 opacity-50"></div>

                        <h3 className="text-lg font-bold text-gray-800 mb-4 flex items-center">
                            <Award className="h-5 w-5 text-indigo-600 mr-2" />
                            Overall Rating
                        </h3>

                        <div className="flex items-end mb-4">
                            <span className="text-5xl font-black text-gray-900">{overall.combined_score}</span>
                            <span className="text-xl text-gray-400 mb-1 ml-1">/100</span>
                        </div>

                        <div className="flex items-center justify-between mb-6">
                            <div className="px-3 py-1 rounded-full bg-gray-100 text-sm font-medium text-gray-700">
                                {overall.performance_rating}
                            </div>
                            <div className="flex items-center text-sm font-medium">
                                {getTrendIcon(overall.overall_trend)}
                                <span className={`ml-1 ${overall.overall_trend === 'Improving' ? 'text-green-600' :
                                        overall.overall_trend === 'Needs Focus' ? 'text-red-600' : 'text-gray-600'
                                    }`}>
                                    {overall.overall_trend}
                                </span>
                            </div>
                        </div>

                        <div className="pt-4 border-t border-gray-100 grid grid-cols-2 gap-4">
                            <div>
                                <p className="text-xs text-gray-500 uppercase font-semibold">Total Sessions</p>
                                <p className="text-xl font-bold text-gray-900">{overall.total_interviews}</p>
                            </div>
                            <div>
                                <p className="text-xs text-gray-500 uppercase font-semibold">Modules Used</p>
                                <p className="text-xl font-bold text-gray-900">
                                    {(technical.has_data ? 1 : 0) + (hr.has_data ? 1 : 0) + (video_presence.has_data ? 1 : 0)}/3
                                </p>
                            </div>
                        </div>
                    </div>

                    {/* Focus Areas Card */}
                    <div className="bg-gradient-to-br from-indigo-600 to-purple-700 rounded-2xl shadow-lg p-6 text-white">
                        <h3 className="text-lg font-bold mb-4 flex items-center">
                            <Target className="h-5 w-5 mr-2" />
                            Focus Areas
                        </h3>

                        <ul className="space-y-3 mb-6">
                            {recommendations.focus_areas.map((area, idx) => (
                                <li key={idx} className="flex items-start text-indigo-100 text-sm">
                                    <span className="bg-indigo-500/30 rounded-full w-5 h-5 flex items-center justify-center text-xs mr-2 mt-0.5 flex-shrink-0">
                                        {idx + 1}
                                    </span>
                                    {area}
                                </li>
                            ))}
                        </ul>

                        <div className="pt-4 border-t border-indigo-500/30">
                            <p className="text-xs text-indigo-200 uppercase font-bold mb-3">Recommended Practice</p>
                            <div className="space-y-2">
                                {recommendations.cta_buttons.slice(0, 2).map((btn, idx) => (
                                    <button
                                        key={idx}
                                        onClick={() => {
                                            const type = btn.action.replace('start_', '').replace('video', 'video-practice');
                                            // Map internal types to user-friendly types if needed
                                            let mappedType = type;
                                            if (type === 'video-practice') mappedType = 'video-practice'; // Keep consistent
                                            onStartPractice(mappedType);
                                        }}
                                        className={`w-full py-2 px-3 rounded-lg text-sm font-semibold flex items-center justify-center transition-colors ${idx === 0
                                                ? 'bg-white text-indigo-700 hover:bg-gray-50'
                                                : 'bg-indigo-800/50 text-white hover:bg-indigo-800'
                                            }`}
                                    >
                                        {btn.label}
                                        <ArrowLeft className="h-4 w-4 ml-2 rotate-180" />
                                    </button>
                                ))}
                            </div>
                        </div>
                    </div>
                </div>

                {/* Right Column: Detailed Breakdown */}
                <div className="lg:col-span-2 space-y-8">

                    {/* Category Cards Row */}
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                        {/* Technical Card */}
                        <div className="bg-white p-5 rounded-2xl shadow-sm border border-gray-100 hover:shadow-md transition-shadow">
                            <div className="flex justify-between items-start mb-3">
                                <div className="bg-blue-50 p-2 rounded-lg">
                                    <Zap className="h-5 w-5 text-blue-600" />
                                </div>
                                {technical.has_data && (
                                    <div className={`px-2 py-0.5 rounded text-xs font-bold ${getPerformanceColor(technical.average_score)}`}>
                                        {technical.average_score}
                                    </div>
                                )}
                            </div>
                            <h4 className="font-bold text-gray-900">Technical</h4>
                            <p className="text-sm text-gray-500 mb-3">{technical.sessions_count} sessions</p>

                            {technical.has_data ? (
                                <div className="space-y-1">
                                    <p className="text-xs text-gray-500 flex items-center">
                                        Trend: {getTrendIcon(technical.trend)}
                                        <span className="ml-1 capitalize">{technical.trend}</span>
                                    </p>
                                </div>
                            ) : (
                                <div className="text-xs text-gray-400 italic">No data yet</div>
                            )}
                        </div>

                        {/* HR Card */}
                        <div className="bg-white p-5 rounded-2xl shadow-sm border border-gray-100 hover:shadow-md transition-shadow">
                            <div className="flex justify-between items-start mb-3">
                                <div className="bg-purple-50 p-2 rounded-lg">
                                    <Users className="h-5 w-5 text-purple-600" />
                                </div>
                                {hr.has_data && (
                                    <div className={`px-2 py-0.5 rounded text-xs font-bold ${getPerformanceColor(hr.average_score)}`}>
                                        {hr.average_score}
                                    </div>
                                )}
                            </div>
                            <h4 className="font-bold text-gray-900">HR</h4>
                            <p className="text-sm text-gray-500 mb-3">{hr.sessions_count} sessions</p>

                            {hr.has_data ? (
                                <div className="space-y-1">
                                    <p className="text-xs text-gray-500 flex items-center">
                                        Trend: {getTrendIcon(hr.trend)}
                                        <span className="ml-1 capitalize">{hr.trend}</span>
                                    </p>
                                </div>
                            ) : (
                                <div className="text-xs text-gray-400 italic">No data yet</div>
                            )}
                        </div>

                        {/* Video Presence Card */}
                        <div className="bg-white p-5 rounded-2xl shadow-sm border border-gray-100 hover:shadow-md transition-shadow">
                            <div className="flex justify-between items-start mb-3">
                                <div className="bg-rose-50 p-2 rounded-lg">
                                    <Video className="h-5 w-5 text-rose-600" />
                                </div>
                                {video_presence.has_data && (
                                    <div className={`px-2 py-0.5 rounded text-xs font-bold ${getPerformanceColor(video_presence.average_score)}`}>
                                        {video_presence.average_score}
                                    </div>
                                )}
                            </div>
                            <h4 className="font-bold text-gray-900">Presence</h4>
                            <p className="text-sm text-gray-500 mb-3">{video_presence.sessions_count} sessions</p>

                            {video_presence.has_data ? (
                                <div className="space-y-1">
                                    <p className="text-xs text-gray-500 flex items-center">
                                        Trend: {getTrendIcon(video_presence.trend)}
                                        <span className="ml-1 capitalize">{video_presence.trend}</span>
                                    </p>
                                </div>
                            ) : (
                                <div className="text-xs text-gray-400 italic">No data yet</div>
                            )}
                        </div>
                    </div>

                    {/* Skill Breakdown */}
                    <div className="bg-white rounded-2xl shadow-lg p-6 border border-gray-100">
                        <h3 className="text-lg font-bold text-gray-900 mb-6 flex items-center">
                            <BarChart2 className="h-5 w-5 text-gray-500 mr-2" />
                            Skill-Level Insights
                        </h3>

                        <div className="space-y-5">
                            {skill_insights.map((skill, idx) => (
                                <div key={idx} className="relative">
                                    <div className="flex justify-between items-end mb-1">
                                        <span className="text-sm font-medium text-gray-700">{skill.skill}</span>
                                        <span className="text-sm font-bold text-gray-900">
                                            {skill.has_data ? `${skill.score}%` : 'N/A'}
                                        </span>
                                    </div>
                                    <div className="h-2 w-full bg-gray-100 rounded-full overflow-hidden">
                                        {skill.has_data && (
                                            <div
                                                className={`h-full rounded-full transition-all duration-1000 ${getProgressColor(skill.score)}`}
                                                style={{ width: `${skill.score}%` }}
                                            ></div>
                                        )}
                                    </div>
                                    {!skill.has_data && (
                                        <p className="text-xs text-gray-400 mt-1">Not enough data to calculate</p>
                                    )}
                                </div>
                            ))}
                        </div>
                    </div>

                    {/* Detailed Feedback Categories */}
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                        {/* Strengths */}
                        <div className="bg-green-50 rounded-2xl p-6 border border-green-100">
                            <h4 className="font-bold text-green-800 mb-4 flex items-center">
                                <TrendingUp className="h-4 w-4 mr-2" /> Key Strengths
                            </h4>
                            <ul className="space-y-2">
                                {[
                                    ...(technical.strengths || []),
                                    ...(hr.strengths || []),
                                    ...(video_presence.strengths || [])
                                ].slice(0, 4).map((strength, idx) => (
                                    <li key={idx} className="flex items-start text-sm text-green-700">
                                        <span className="w-1.5 h-1.5 bg-green-500 rounded-full mt-1.5 mr-2 flex-shrink-0"></span>
                                        {strength}
                                    </li>
                                ))}
                                {(!technical.has_data && !hr.has_data && !video_presence.has_data) && (
                                    <li className="text-sm text-green-600/70 italic">Based on your best performances</li>
                                )}
                            </ul>
                        </div>

                        {/* Areas to Improve */}
                        <div className="bg-orange-50 rounded-2xl p-6 border border-orange-100">
                            <h4 className="font-bold text-orange-800 mb-4 flex items-center">
                                <Target className="h-4 w-4 mr-2" /> Improvement Areas
                            </h4>
                            <ul className="space-y-2">
                                {[
                                    ...(technical.improvement_areas || []),
                                    ...(hr.improvement_areas || []),
                                    ...(video_presence.improvement_areas || [])
                                ].slice(0, 4).map((area, idx) => (
                                    <li key={idx} className="flex items-start text-sm text-orange-700">
                                        <span className="w-1.5 h-1.5 bg-orange-500 rounded-full mt-1.5 mr-2 flex-shrink-0"></span>
                                        {area}
                                    </li>
                                ))}
                                {(!technical.has_data && !hr.has_data && !video_presence.has_data) && (
                                    <li className="text-sm text-orange-600/70 italic">Based on recurring feedback patterns</li>
                                )}
                            </ul>
                        </div>
                    </div>

                </div>
            </div>
        </div>
    );
};

export default InterviewAnalytics;
