import React, { useEffect, useState } from 'react';
import { Chart as ChartJS, ArcElement, Tooltip, Legend, CategoryScale, LinearScale, BarElement, Title, PointElement, LineElement } from 'chart.js';
import { Doughnut, Bar, Line } from 'react-chartjs-2';
import { TrendingUp, Award, Target, Flame, Calendar, Clock, Trophy, Star, CheckCircle2 } from 'lucide-react';
import { codingAPI } from '../services/api';

// Register ChartJS components
ChartJS.register(ArcElement, Tooltip, Legend, CategoryScale, LinearScale, BarElement, Title, PointElement, LineElement);

const ProgressDashboard = ({ userId, onClose }) => {
    const [stats, setStats] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchStats = async () => {
            try {
                const response = await codingAPI.getProgressStats(userId);
                setStats(response.data);
            } catch (error) {
                console.error('Failed to fetch progress stats:', error);
            } finally {
                setLoading(false);
            }
        };

        if (userId) {
            fetchStats();
        }
    }, [userId]);

    if (loading) {
        return (
            <div className="flex items-center justify-center h-screen bg-gradient-to-br from-slate-50 to-blue-50">
                <div className="text-center">
                    <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
                    <p className="mt-4 text-gray-600">Loading your progress...</p>
                </div>
            </div>
        );
    }

    if (!stats) {
        return (
            <div className="flex items-center justify-center h-screen">
                <p className="text-gray-500">No progress data available</p>
            </div>
        );
    }

    // Difficulty Chart Data
    const difficultyData = {
        labels: ['Easy', 'Medium', 'Hard'],
        datasets: [
            {
                label: 'Solved',
                data: [
                    stats.difficulty_stats.Easy.solved,
                    stats.difficulty_stats.Medium.solved,
                    stats.difficulty_stats.Hard.solved,
                ],
                backgroundColor: ['#10b981', '#f59e0b', '#ef4444'],
                borderWidth: 0,
            },
        ],
    };

    const difficultyOptions = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                display: false,
            },
            tooltip: {
                callbacks: {
                    label: (context) => {
                        const level = context.label;
                        const solved = context.parsed;
                        const total = stats.difficulty_stats[level].total;
                        return `${solved}/${total} problems`;
                    },
                },
            },
        },
    };

    // Category Chart Data (top 8 categories)
    const sortedCategories = Object.entries(stats.category_stats)
        .sort((a, b) => b[1].total - a[1].total)
        .slice(0, 8);

    const categoryData = {
        labels: sortedCategories.map(([name]) => name),
        datasets: [
            {
                label: 'Solved',
                data: sortedCategories.map(([, data]) => data.solved),
                backgroundColor: '#3b82f6',
            },
            {
                label: 'Remaining',
                data: sortedCategories.map(([, data]) => data.total - data.solved),
                backgroundColor: '#e5e7eb',
            },
        ],
    };

    const categoryOptions = {
        indexAxis: 'y',
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                display: true,
                position: 'top',
            },
            tooltip: {
                callbacks: {
                    label: (context) => {
                        return `${context.dataset.label}: ${context.parsed.x}`;
                    },
                },
            },
        },
        scales: {
            x: {
                stacked: true,
            },
            y: {
                stacked: true,
            },
        },
    };

    // Activity Chart Data (Last 30 days)
    const activityData = {
        labels: stats.recent_activity.map((item) => {
            const date = new Date(item.date);
            return `${date.getMonth() + 1}/${date.getDate()}`;
        }),
        datasets: [
            {
                label: 'Problems Solved',
                data: stats.recent_activity.map((item) => item.count),
                borderColor: '#3b82f6',
                backgroundColor: 'rgba(59, 130, 246, 0.1)',
                tension: 0.4,
                fill: true,
            },
        ],
    };

    const activityOptions = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                display: false,
            },
        },
        scales: {
            y: {
                beginAtZero: true,
                ticks: {
                    stepSize: 1,
                },
            },
        },
    };

    return (
        <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50 p-6">
            <div className="max-w-7xl mx-auto">
                {/* Header */}
                <div className="flex justify-between items-center mb-8">
                    <div>
                        <h1 className="text-3xl font-bold text-gray-800 flex items-center gap-2">
                            <Trophy className="w-8 h-8 text-yellow-500" />
                            Your Progress Dashboard
                        </h1>
                        <p className="text-gray-600 mt-1">Track your coding journey and achievements</p>
                    </div>
                    {onClose && (
                        <button
                            onClick={onClose}
                            className="px-4 py-2 bg-white rounded-lg shadow hover:shadow-md transition-shadow text-gray-700 font-medium"
                        >
                            Back to Problems
                        </button>
                    )}
                </div>

                {/* Stats Cards */}
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
                    {/* Total Solved */}
                    <div className="bg-white rounded-xl shadow-md p-6 border-l-4 border-blue-500">
                        <div className="flex items-center justify-between">
                            <div>
                                <p className="text-sm text-gray-600 mb-1">Total Solved</p>
                                <p className="text-3xl font-bold text-gray-800">{stats.total_solved}</p>
                                <p className="text-xs text-gray-500 mt-1">out of {stats.total_problems}</p>
                            </div>
                            <CheckCircle2 className="w-12 h-12 text-blue-500 opacity-20" />
                        </div>
                    </div>

                    {/* Completion Rate */}
                    <div className="bg-white rounded-xl shadow-md p-6 border-l-4 border-green-500">
                        <div className="flex items-center justify-between">
                            <div>
                                <p className="text-sm text-gray-600 mb-1">Completion Rate</p>
                                <p className="text-3xl font-bold text-gray-800">{stats.completion_percentage}%</p>
                                <div className="w-full bg-gray-200 rounded-full h-2 mt-2">
                                    <div
                                        className="bg-green-500 h-2 rounded-full transition-all"
                                        style={{ width: `${stats.completion_percentage}%` }}
                                    ></div>
                                </div>
                            </div>
                            <Target className="w-12 h-12 text-green-500 opacity-20" />
                        </div>
                    </div>

                    {/* Current Streak */}
                    <div className="bg-white rounded-xl shadow-md p-6 border-l-4 border-orange-500">
                        <div className="flex items-center justify-between">
                            <div>
                                <p className="text-sm text-gray-600 mb-1">Current Streak</p>
                                <p className="text-3xl font-bold text-gray-800">{stats.current_streak} days</p>
                                <p className="text-xs text-gray-500 mt-1">Max: {stats.max_streak} days</p>
                            </div>
                            <Flame className="w-12 h-12 text-orange-500 opacity-20" />
                        </div>
                    </div>

                    {/* Solved Today */}
                    <div className="bg-white rounded-xl shadow-md p-6 border-l-4 border-purple-500">
                        <div className="flex items-center justify-between">
                            <div>
                                <p className="text-sm text-gray-600 mb-1">Solved Today</p>
                                <p className="text-3xl font-bold text-gray-800">{stats.solved_today}</p>
                                <p className="text-xs text-gray-500 mt-1">Keep it up!</p>
                            </div>
                            <Star className="w-12 h-12 text-purple-500 opacity-20" />
                        </div>
                    </div>
                </div>

                {/* Charts Grid */}
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
                    {/* Difficulty Distribution */}
                    <div className="bg-white rounded-xl shadow-md p-6">
                        <h2 className="text-xl font-semibold text-gray-800 mb-4 flex items-center gap-2">
                            <Award className="w-5 h-5 text-blue-600" />
                            Difficulty Breakdown
                        </h2>
                        <div className="h-64">
                            <Doughnut data={difficultyData} options={difficultyOptions} />
                        </div>
                        <div className="mt-4 grid grid-cols-3 gap-2">
                            <div className="text-center">
                                <p className="text-2xl font-bold text-green-600">
                                    {stats.difficulty_stats.Easy.solved}
                                </p>
                                <p className="text-sm text-gray-600">Easy</p>
                                <p className="text-xs text-gray-500">/{stats.difficulty_stats.Easy.total}</p>
                            </div>
                            <div className="text-center">
                                <p className="text-2xl font-bold text-yellow-600">
                                    {stats.difficulty_stats.Medium.solved}
                                </p>
                                <p className="text-sm text-gray-600">Medium</p>
                                <p className="text-xs text-gray-500">/{stats.difficulty_stats.Medium.total}</p>
                            </div>
                            <div className="text-center">
                                <p className="text-2xl font-bold text-red-600">
                                    {stats.difficulty_stats.Hard.solved}
                                </p>
                                <p className="text-sm text-gray-600">Hard</p>
                                <p className="text-xs text-gray-500">/{stats.difficulty_stats.Hard.total}</p>
                            </div>
                        </div>
                    </div>

                    {/* Activity Chart */}
                    <div className="bg-white rounded-xl shadow-md p-6">
                        <h2 className="text-xl font-semibold text-gray-800 mb-4 flex items-center gap-2">
                            <TrendingUp className="w-5 h-5 text-blue-600" />
                            Activity (Last 30 Days)
                        </h2>
                        <div className="h-64">
                            {stats.recent_activity.length > 0 ? (
                                <Line data={activityData} options={activityOptions} />
                            ) : (
                                <div className="flex items-center justify-center h-full text-gray-400">
                                    No activity in the last 30 days
                                </div>
                            )}
                        </div>
                    </div>
                </div>

                {/* Category Progress */}
                <div className="bg-white rounded-xl shadow-md p-6 mb-8">
                    <h2 className="text-xl font-semibold text-gray-800 mb-4 flex items-center gap-2">
                        <Calendar className="w-5 h-5 text-blue-600" />
                        Category Progress (Top 8)
                    </h2>
                    <div className="h-80">
                        <Bar data={categoryData} options={categoryOptions} />
                    </div>
                </div>

                {/* Recent Solved Problems */}
                <div className="bg-white rounded-xl shadow-md p-6">
                    <h2 className="text-xl font-semibold text-gray-800 mb-4 flex items-center gap-2">
                        <Clock className="w-5 h-5 text-blue-600" />
                        Recently Solved
                    </h2>
                    {stats.recent_solved.length > 0 ? (
                        <div className="space-y-2">
                            {stats.recent_solved.map((problem, idx) => (
                                <div
                                    key={idx}
                                    className="flex items-center justify-between p-3 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors"
                                >
                                    <div className="flex-1">
                                        <p className="font-medium text-gray-800">{problem.title}</p>
                                        <div className="flex items-center gap-2 mt-1">
                                            <span
                                                className={`text-xs px-2 py-1 rounded ${problem.difficulty === 'Easy'
                                                        ? 'bg-green-100 text-green-700'
                                                        : problem.difficulty === 'Medium'
                                                            ? 'bg-yellow-100 text-yellow-700'
                                                            : 'bg-red-100 text-red-700'
                                                    }`}
                                            >
                                                {problem.difficulty}
                                            </span>
                                            {problem.tags.slice(0, 2).map((tag, i) => (
                                                <span key={i} className="text-xs bg-blue-100 text-blue-700 px-2 py-1 rounded">
                                                    {tag}
                                                </span>
                                            ))}
                                        </div>
                                    </div>
                                    <p className="text-sm text-gray-500">
                                        {new Date(problem.solved_at).toLocaleDateString()}
                                    </p>
                                </div>
                            ))}
                        </div>
                    ) : (
                        <p className="text-gray-400 text-center py-8">No problems solved yet. Start coding!</p>
                    )}
                </div>
            </div>
        </div>
    );
};

export default ProgressDashboard;
