import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import {
    TrendingUp, Target, Clock, Award, Brain, Code, Users,
    Calendar, Zap, Star, AlertCircle, Trophy, Activity,
    BarChart3, ArrowRight, CheckCircle2, XCircle
} from 'lucide-react';

const UnifiedAnalytics = () => {
    const { user } = useAuth();
    const navigate = useNavigate();
    const [analytics, setAnalytics] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        fetchUnifiedAnalytics();
    }, [user]);

    const fetchUnifiedAnalytics = async () => {
        if (!user?.id) {
            setLoading(false);
            return;
        }

        try {
            setLoading(true);
            const response = await fetch(`http://localhost:8000/analytics/unified/${user.id}`);
            const data = await response.json();

            if (data.status === 'success') {
                setAnalytics(data.data);
            } else {
                setError('Failed to load analytics');
            }
        } catch (err) {
            console.error('Failed to fetch unified analytics:', err);
            setError('Failed to load analytics. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    if (loading) {
        return (
            <div className="p-6">
                <h1 className="text-3xl font-bold mb-6">Unified Practice Analytics</h1>
                <div className="text-center py-20">
                    <div className="inline-block animate-spin rounded-full h-16 w-16 border-t-4 border-b-4 border-blue-500"></div>
                    <p className="mt-4 text-gray-600">Loading your analytics...</p>
                </div>
            </div>
        );
    }

    if (error || !analytics) {
        return (
            <div className="p-6">
                <h1 className="text-3xl font-bold mb-6">Unified Practice Analytics</h1>
                <div className="bg-red-50 border border-red-200 rounded-2xl p-8 text-center">
                    <AlertCircle className="h-12 w-12 text-red-500 mx-auto mb-4" />
                    <h3 className="text-lg font-bold text-red-800 mb-2">Failed to Load Analytics</h3>
                    <p className="text-red-600 mb-6">{error || 'No data available'}</p>
                    <button
                        onClick={fetchUnifiedAnalytics}
                        className="px-6 py-2 bg-red-600 text-white rounded-xl hover:bg-red-700 transition-colors"
                    >
                        Try Again
                    </button>
                </div>
            </div>
        );
    }

    const { overall_summary, module_performance, skill_breakdown, weak_areas, recent_activity } = analytics;

    // Color scheme for modules
    const moduleColors = {
        'Aptitude': 'bg-blue-100 text-blue-600 border-blue-200',
        'Coding': 'bg-green-100 text-green-600 border-green-200',
        'Technical Interview': 'bg-purple-100 text-purple-600 border-purple-200',
        'HR Interview': 'bg-pink-100 text-pink-600 border-pink-200',
        'Video Presence': 'bg-orange-100 text-orange-600 border-orange-200',
        'GD Practice': 'bg-indigo-100 text-indigo-600 border-indigo-200'
    };

    const getModuleIcon = (module) => {
        switch (module) {
            case 'Aptitude': return <Brain className="h-5 w-5" />;
            case 'Coding': return <Code className="h-5 w-5" />;
            case 'Technical Interview':
            case 'HR Interview':
            case 'Video Presence':
            case 'GD Practice':
                return <Users className="h-5 w-5" />;
            default: return <Target className="h-5 w-5" />;
        }
    };

    const getTrendIcon = (trend) => {
        if (trend === 'up') return <TrendingUp className="h-4 w-4 text-green-500" />;
        if (trend === 'down') return <TrendingUp className="h-4 w-4 text-red-500 rotate-180" />;
        return <ArrowRight className="h-4 w-4 text-gray-400" />;
    };

    return (
        <div className="p-4 md:p-6 max-w-7xl mx-auto">
            {/* Header */}
            <div className="flex flex-col md:flex-row justify-between items-start md:items-center mb-8">
                <div>
                    <h1 className="text-3xl font-bold text-gray-900">Unified Practice Analytics</h1>
                    <p className="text-gray-600 mt-2">
                        Your complete practice summary across all modules
                    </p>
                </div>
                <button
                    onClick={() => navigate('/')}
                    className="mt-4 md:mt-0 px-4 py-2 bg-gray-100 text-gray-700 rounded-xl hover:bg-gray-200 transition-colors"
                >
                    ← Back to Dashboard
                </button>
            </div>

            {/* 1. Overall Practice Summary */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
                <div className="bg-white rounded-2xl shadow-lg p-6 border border-gray-100">
                    <div className="flex justify-between items-start">
                        <div>
                            <p className="text-gray-500 text-sm font-medium">Total Sessions</p>
                            <p className="text-3xl font-bold mt-2 text-slate-800">{overall_summary.total_sessions}</p>
                            <p className="text-gray-400 text-sm mt-1">All modules</p>
                        </div>
                        <div className="p-3 rounded-xl bg-blue-50 text-blue-600">
                            <Activity className="h-6 w-6" />
                        </div>
                    </div>
                </div>

                <div className="bg-white rounded-2xl shadow-lg p-6 border border-gray-100">
                    <div className="flex justify-between items-start">
                        <div>
                            <p className="text-gray-500 text-sm font-medium">Practice Time</p>
                            <p className="text-3xl font-bold mt-2 text-slate-800">{overall_summary.total_time_hours}h</p>
                            <p className="text-gray-400 text-sm mt-1">{overall_summary.total_time_minutes} minutes</p>
                        </div>
                        <div className="p-3 rounded-xl bg-green-50 text-green-600">
                            <Clock className="h-6 w-6" />
                        </div>
                    </div>
                </div>

                <div className="bg-white rounded-2xl shadow-lg p-6 border border-gray-100">
                    <div className="flex justify-between items-start">
                        <div>
                            <p className="text-gray-500 text-sm font-medium">Modules Used</p>
                            <p className="text-3xl font-bold mt-2 text-slate-800">{overall_summary.modules_count}</p>
                            <p className="text-gray-400 text-sm mt-1">{overall_summary.modules_used.join(', ')}</p>
                        </div>
                        <div className="p-3 rounded-xl bg-purple-50 text-purple-600">
                            <BarChart3 className="h-6 w-6" />
                        </div>
                    </div>
                </div>

                <div className="bg-white rounded-2xl shadow-lg p-6 border border-gray-100">
                    <div className="flex justify-between items-start">
                        <div>
                            <p className="text-gray-500 text-sm font-medium">Progress Trend</p>
                            <p className="text-3xl font-bold mt-2 text-slate-800 capitalize">{overall_summary.improvement_trend}</p>
                            <p className="text-gray-400 text-sm mt-1">Overall</p>
                        </div>
                        <div className="p-3 rounded-xl bg-orange-50 text-orange-600">
                            <TrendingUp className="h-6 w-6" />
                        </div>
                    </div>
                </div>
            </div>

            {/* 2. Module-Wise Performance */}
            <div className="bg-white rounded-2xl shadow-lg p-6 mb-8">
                <div className="flex items-center mb-6">
                    <Trophy className="h-5 w-5 text-yellow-500 mr-2" />
                    <h3 className="text-lg font-semibold text-gray-900">Module-Wise Performance</h3>
                </div>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                    {module_performance.map((module, index) => (
                        <div
                            key={index}
                            className={`p-4 rounded-xl border-2 ${moduleColors[module.module] || 'bg-gray-100 text-gray-600 border-gray-200'} ${!module.has_data ? 'opacity-50' : ''}`}
                        >
                            <div className="flex items-center justify-between mb-3">
                                <div className="flex items-center">
                                    {getModuleIcon(module.module)}
                                    <h4 className="ml-2 font-semibold">{module.module}</h4>
                                </div>
                                {getTrendIcon(module.trend)}
                            </div>
                            <div className="space-y-2">
                                <div className="flex justify-between text-sm">
                                    <span>Sessions:</span>
                                    <span className="font-bold">{module.sessions}</span>
                                </div>
                                <div className="flex justify-between text-sm">
                                    <span>Performance:</span>
                                    <span className="font-bold">{module.performance_level}</span>
                                </div>
                                {module.performance_score > 0 && (
                                    <div className="flex justify-between text-sm">
                                        <span>Score:</span>
                                        <span className="font-bold">{module.performance_score}%</span>
                                    </div>
                                )}
                                {module.last_practiced && (
                                    <div className="text-xs text-gray-500 mt-2">
                                        Last: {new Date(module.last_practiced).toLocaleDateString()}
                                    </div>
                                )}
                                {!module.has_data && (
                                    <div className="text-xs text-gray-500 mt-2">No practice yet</div>
                                )}
                            </div>
                        </div>
                    ))}
                </div>
            </div>

            {/* 3. Skill Breakdown */}
            <div className="bg-white rounded-2xl shadow-lg p-6 mb-8">
                <div className="flex items-center mb-6">
                    <Star className="h-5 w-5 text-indigo-500 mr-2" />
                    <h3 className="text-lg font-semibold text-gray-900">Skill Breakdown</h3>
                </div>
                <div className="space-y-4">
                    {skill_breakdown.map((skill, index) => (
                        <div key={index}>
                            <div className="flex justify-between items-center mb-2">
                                <span className="font-medium text-gray-700">{skill.skill}</span>
                                <span className="text-sm font-bold text-gray-600">{skill.score}% - {skill.level}</span>
                            </div>
                            <div className="w-full bg-gray-200 rounded-full h-3">
                                <div
                                    className={`h-full rounded-full ${skill.score >= 70 ? 'bg-green-500' :
                                        skill.score >= 50 ? 'bg-yellow-500' :
                                            'bg-red-500'
                                        }`}
                                    style={{ width: `${skill.score}%` }}
                                ></div>
                            </div>
                        </div>
                    ))}
                </div>
            </div>

            {/* 4. Weak Areas & Focus Suggestions */}
            <div className="bg-white rounded-2xl shadow-lg p-6 mb-8">
                <div className="flex items-center mb-6">
                    <AlertCircle className="h-5 w-5 text-red-500 mr-2" />
                    <h3 className="text-lg font-semibold text-gray-900">Focus Areas & Suggestions</h3>
                </div>
                {weak_areas.length > 0 ? (
                    <div className="space-y-4">
                        {weak_areas.map((area, index) => (
                            <div key={index} className="flex items-start justify-between p-4 bg-red-50 rounded-xl border border-red-100">
                                <div className="flex-1">
                                    <h4 className="font-semibold text-red-800">{area.area}</h4>
                                    <p className="text-sm text-red-600 mt-1">{area.module} • {area.suggestion}</p>
                                </div>
                                <button
                                    onClick={() => {
                                        if (area.action === 'practice_aptitude') navigate('/aptitude');
                                        else if (area.action === 'practice_coding') navigate('/coding');
                                        else if (area.action === 'practice_interview') navigate('/interview');
                                    }}
                                    className="ml-4 px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors text-sm font-medium"
                                >
                                    Practice Now
                                </button>
                            </div>
                        ))}
                    </div>
                ) : (
                    <div className="text-center py-8">
                        <CheckCircle2 className="h-12 w-12 text-green-500 mx-auto mb-3" />
                        <p className="text-gray-600">Great job! No major weak areas identified.</p>
                        <p className="text-sm text-gray-400 mt-1">Keep practicing to maintain your progress!</p>
                    </div>
                )}
            </div>

            {/* 5. Recent Activity Timeline */}
            <div className="bg-white rounded-2xl shadow-lg p-6">
                <div className="flex items-center mb-6">
                    <Calendar className="h-5 w-5 text-blue-500 mr-2" />
                    <h3 className="text-lg font-semibold text-gray-900">Recent Activity</h3>
                </div>
                {recent_activity.length > 0 ? (
                    <div className="space-y-3">
                        {recent_activity.map((activity, index) => (
                            <div key={index} className="flex items-start p-3 rounded-lg bg-gray-50 hover:bg-gray-100 transition-colors">
                                <div className="flex-shrink-0 mt-1">
                                    {activity.module === 'Aptitude' && (
                                        <div className="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center">
                                            <Brain className="h-4 w-4 text-blue-600" />
                                        </div>
                                    )}
                                    {activity.module === 'Coding' && (
                                        <div className="w-8 h-8 bg-green-100 rounded-full flex items-center justify-center">
                                            <Code className="h-4 w-4 text-green-600" />
                                        </div>
                                    )}
                                    {activity.module === 'Interview' && (
                                        <div className="w-8 h-8 bg-purple-100 rounded-full flex items-center justify-center">
                                            <Users className="h-4 w-4 text-purple-600" />
                                        </div>
                                    )}
                                </div>
                                <div className="ml-3 flex-1">
                                    <div className="flex items-center justify-between">
                                        <p className="font-medium text-gray-900">{activity.module} - {activity.type}</p>
                                        {activity.score >= 70 ? (
                                            <CheckCircle2 className="h-4 w-4 text-green-500" />
                                        ) : activity.score > 0 ? (
                                            <XCircle className="h-4 w-4 text-red-500" />
                                        ) : null}
                                    </div>
                                    <p className="text-sm text-gray-600">{activity.result}</p>
                                    <p className="text-xs text-gray-400 mt-1">
                                        {activity.date ? new Date(activity.date).toLocaleString() : 'Recently'}
                                    </p>
                                </div>
                            </div>
                        ))}
                    </div>
                ) : (
                    <div className="text-center py-8">
                        <Activity className="h-12 w-12 text-gray-300 mx-auto mb-3" />
                        <p className="text-gray-500">No recent activity</p>
                        <p className="text-sm text-gray-400 mt-1">Start practicing to see your progress here</p>
                    </div>
                )}
            </div>

            {/* Quick Action Buttons */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mt-8">
                <button
                    onClick={() => navigate('/aptitude')}
                    className="bg-gradient-to-r from-blue-600 to-blue-700 text-white py-3 px-4 rounded-xl font-medium hover:shadow-lg transition-all flex items-center justify-center"
                >
                    <Brain className="h-5 w-5 mr-2" />
                    Practice Aptitude
                </button>
                <button
                    onClick={() => navigate('/coding')}
                    className="bg-gradient-to-r from-green-600 to-emerald-700 text-white py-3 px-4 rounded-xl font-medium hover:shadow-lg transition-all flex items-center justify-center"
                >
                    <Code className="h-5 w-5 mr-2" />
                    Practice Coding
                </button>
                <button
                    onClick={() => navigate('/interview')}
                    className="bg-gradient-to-r from-purple-600 to-purple-700 text-white py-3 px-4 rounded-xl font-medium hover:shadow-lg transition-all flex items-center justify-center"
                >
                    <Users className="h-5 w-5 mr-2" />
                    Practice Interview
                </button>
            </div>
        </div>
    );
};

export default UnifiedAnalytics;
