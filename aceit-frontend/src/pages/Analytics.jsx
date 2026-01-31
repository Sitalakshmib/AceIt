import React, { useState, useEffect } from 'react';
import { analyticsAPI } from '../services/api';

const Analytics = () => {
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');
    const [analytics, setAnalytics] = useState(null);

    useEffect(() => {
        fetchAnalytics();
    }, []);

    const fetchAnalytics = async () => {
        try {
            setLoading(true);
            setError('');
            const response = await analyticsAPI.getDashboard();
            setAnalytics(response.data);
        } catch (err) {
            console.error('Failed to fetch analytics:', err);
            setError('Failed to load analytics. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    if (loading) {
        return (
            <div className="p-6 max-w-6xl mx-auto text-center">
                <div className="bg-white p-8 rounded-lg shadow-md animate-pulse">Loading Analytics...</div>
            </div>
        );
    }

    if (error || !analytics) {
        return (
            <div className="p-6 max-w-6xl mx-auto text-center">
                <div className="bg-white p-8 rounded-lg shadow-md text-red-600">
                    <h3 className="text-xl font-bold mb-2">Error</h3>
                    <p>{error || 'No analytics data available'}</p>
                    <button onClick={fetchAnalytics} className="mt-4 bg-blue-600 text-white px-4 py-2 rounded">
                        Retry
                    </button>
                </div>
            </div>
        );
    }

    const { overall_stats, category_performance, strong_topics, weak_topics, mock_test_stats, recommendations } = analytics;

    return (
        <div className="p-6 max-w-6xl mx-auto">
            <h1 className="text-3xl font-bold text-gray-800 mb-6">Performance Analytics</h1>

            {/* Overall Stats */}
            {overall_stats && (
                <div className="grid md:grid-cols-3 gap-6 mb-8">
                    <div className="bg-gradient-to-br from-blue-500 to-blue-600 text-white p-6 rounded-lg shadow-lg">
                        <div className="text-sm opacity-90 mb-1">Total Attempted</div>
                        <div className="text-4xl font-bold">{overall_stats.total_attempted}</div>
                        <div className="text-xs opacity-75 mt-1">questions</div>
                    </div>

                    <div className="bg-gradient-to-br from-green-500 to-green-600 text-white p-6 rounded-lg shadow-lg">
                        <div className="text-sm opacity-90 mb-1">Total Correct</div>
                        <div className="text-4xl font-bold">{overall_stats.total_correct}</div>
                        <div className="text-xs opacity-75 mt-1">answers</div>
                    </div>

                    <div className="bg-gradient-to-br from-purple-500 to-purple-600 text-white p-6 rounded-lg shadow-lg">
                        <div className="text-sm opacity-90 mb-1">Overall Accuracy</div>
                        <div className="text-4xl font-bold">{overall_stats.overall_accuracy.toFixed(1)}%</div>
                        <div className="text-xs opacity-75 mt-1">success rate</div>
                    </div>
                </div>
            )}

            {/* Category Performance */}
            {category_performance && Object.keys(category_performance).length > 0 && (
                <div className="bg-white rounded-lg shadow-md p-6 mb-8">
                    <h2 className="text-2xl font-bold text-gray-800 mb-4">Category Performance</h2>
                    <div className="grid md:grid-cols-2 gap-6">
                        {Object.entries(category_performance).map(([category, stats]) => (
                            <div key={category} className="border border-gray-200 rounded-lg p-4">
                                <h3 className="font-bold text-lg text-gray-700 mb-3">{category}</h3>

                                {/* Accuracy Bar */}
                                <div className="mb-3">
                                    <div className="flex justify-between text-sm mb-1">
                                        <span className="text-gray-600">Accuracy</span>
                                        <span className="font-bold">{stats.accuracy.toFixed(1)}%</span>
                                    </div>
                                    <div className="w-full bg-gray-200 rounded-full h-2">
                                        <div
                                            className={`h-2 rounded-full ${stats.accuracy >= 80 ? 'bg-green-500' :
                                                stats.accuracy >= 60 ? 'bg-yellow-500' : 'bg-red-500'
                                                }`}
                                            style={{ width: `${stats.accuracy}%` }}
                                        ></div>
                                    </div>
                                </div>

                                {/* Stats */}
                                <div className="text-sm text-gray-600 space-y-1">
                                    <div className="flex justify-between">
                                        <span>Attempted:</span>
                                        <span className="font-semibold">{stats.attempted}</span>
                                    </div>
                                    <div className="flex justify-between">
                                        <span>Correct:</span>
                                        <span className="font-semibold text-green-600">{stats.correct}</span>
                                    </div>
                                </div>

                                {/* Topics */}
                                {stats.topics && Object.keys(stats.topics).length > 0 && (
                                    <div className="mt-4 pt-4 border-t border-gray-100">
                                        <div className="text-xs font-semibold text-gray-500 mb-2">Top Topics:</div>
                                        <div className="space-y-2">
                                            {Object.entries(stats.topics).slice(0, 3).map(([topic, topicStats]) => (
                                                <div key={topic} className="flex justify-between text-xs">
                                                    <span className="text-gray-600 truncate">{topic}</span>
                                                    <span className={`font-semibold ${topicStats.accuracy >= 70 ? 'text-green-600' : 'text-orange-600'
                                                        }`}>
                                                        {topicStats.accuracy.toFixed(0)}%
                                                    </span>
                                                </div>
                                            ))}
                                        </div>
                                    </div>
                                )}
                            </div>
                        ))}
                    </div>
                </div>
            )}

            {/* Strengths and Weaknesses */}
            <div className="grid md:grid-cols-2 gap-6 mb-8">
                {/* Strong Topics */}
                <div className="bg-green-50 border border-green-200 rounded-lg p-6">
                    <h3 className="text-xl font-bold text-green-800 mb-4 flex items-center">
                        <span className="mr-2">💪</span> Strong Topics
                    </h3>
                    {strong_topics && strong_topics.length > 0 ? (
                        <ul className="space-y-2">
                            {strong_topics.map((topic, idx) => (
                                <li key={idx} className="flex items-center text-green-700">
                                    <span className="mr-2">✓</span>
                                    <span className="font-medium">{topic}</span>
                                </li>
                            ))}
                        </ul>
                    ) : (
                        <p className="text-green-600 italic">Practice more to identify your strengths!</p>
                    )}
                </div>

                {/* Weak Topics */}
                <div className="bg-orange-50 border border-orange-200 rounded-lg p-6">
                    <h3 className="text-xl font-bold text-orange-800 mb-4 flex items-center">
                        <span className="mr-2">📚</span> Areas to Improve
                    </h3>
                    {weak_topics && weak_topics.length > 0 ? (
                        <ul className="space-y-2">
                            {weak_topics.map((topic, idx) => (
                                <li key={idx} className="flex items-center text-orange-700">
                                    <span className="mr-2">→</span>
                                    <span className="font-medium">{topic}</span>
                                </li>
                            ))}
                        </ul>
                    ) : (
                        <p className="text-orange-600 italic">Great job! Keep practicing consistently.</p>
                    )}
                </div>
            </div>

            {/* Mock Test Stats */}
            {mock_test_stats && mock_test_stats.total_tests > 0 && (
                <div className="bg-white rounded-lg shadow-md p-6 mb-8">
                    <h2 className="text-2xl font-bold text-gray-800 mb-4">Mock Test Performance</h2>
                    <div className="grid md:grid-cols-3 gap-6 mb-4">
                        <div className="text-center p-4 bg-blue-50 rounded-lg">
                            <div className="text-3xl font-bold text-blue-600">{mock_test_stats.total_tests}</div>
                            <div className="text-sm text-gray-600 mt-1">Tests Taken</div>
                        </div>
                        <div className="text-center p-4 bg-green-50 rounded-lg">
                            <div className="text-3xl font-bold text-green-600">{mock_test_stats.average_score.toFixed(1)}%</div>
                            <div className="text-sm text-gray-600 mt-1">Average Score</div>
                        </div>
                        <div className="text-center p-4 bg-purple-50 rounded-lg">
                            <div className="text-3xl font-bold text-purple-600">{mock_test_stats.best_score.toFixed(1)}%</div>
                            <div className="text-sm text-gray-600 mt-1">Best Score</div>
                        </div>
                    </div>

                    {/* Recent Tests */}
                    {mock_test_stats.recent_tests && mock_test_stats.recent_tests.length > 0 && (
                        <div className="mt-6">
                            <h3 className="font-semibold text-gray-700 mb-3">Recent Tests</h3>
                            <div className="space-y-2">
                                {mock_test_stats.recent_tests.map((test, idx) => (
                                    <div key={idx} className="flex justify-between items-center p-3 bg-gray-50 rounded">
                                        <div className="text-sm">
                                            <span className="font-medium">Test #{idx + 1}</span>
                                            <span className="text-gray-500 ml-2">
                                                {test.completed_at ? new Date(test.completed_at).toLocaleDateString() : 'N/A'}
                                            </span>
                                        </div>
                                        <div className="flex items-center gap-4">
                                            <span className="text-sm text-gray-600">{test.score}/{test.total}</span>
                                            <span className={`font-bold ${test.accuracy >= 80 ? 'text-green-600' :
                                                test.accuracy >= 60 ? 'text-yellow-600' : 'text-red-600'
                                                }`}>
                                                {test.accuracy.toFixed(1)}%
                                            </span>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        </div>
                    )}
                </div>
            )}

            {/* Recommendations */}
            {recommendations && recommendations.length > 0 && (
                <div className="bg-blue-50 border border-blue-200 rounded-lg p-6">
                    <h2 className="text-2xl font-bold text-blue-800 mb-4 flex items-center">
                        <span className="mr-2">💡</span> Personalized Recommendations
                    </h2>
                    <ul className="space-y-3">
                        {recommendations.map((rec, idx) => (
                            <li key={idx} className="flex items-start text-blue-900">
                                <span className="mr-3 mt-1 text-blue-500">•</span>
                                <span>{rec}</span>
                            </li>
                        ))}
                    </ul>
                </div>
            )}

            {/* No Data Message */}
            {(!overall_stats || overall_stats.total_attempted === 0) && (
                <div className="bg-gray-50 border border-gray-200 rounded-lg p-8 text-center">
                    <p className="text-gray-600 text-lg mb-4">No practice data available yet</p>
                    <p className="text-gray-500 text-sm">Start practicing to see your analytics!</p>
                </div>
            )}
        </div>
    );
};

export default Analytics;
