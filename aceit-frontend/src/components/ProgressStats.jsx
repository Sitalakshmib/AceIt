import React, { useEffect, useState, forwardRef, useImperativeHandle } from 'react';
import { TrendingUp, Target, Flame, CheckCircle2 } from 'lucide-react';
import { codingAPI } from '../services/api';

const ProgressStats = forwardRef(({ userId }, ref) => {
    const [stats, setStats] = useState(null);
    const [loading, setLoading] = useState(true);

    const fetchStats = async () => {
        try {
            setLoading(true);
            const response = await codingAPI.getProgressStats(userId);
            setStats(response.data);
            setLoading(false);
        } catch (error) {
            console.error('Failed to fetch progress stats:', error);
            setLoading(false);
        }
    };

    useEffect(() => {
        if (userId) {
            fetchStats();
        } else {
            setLoading(false);
        }
    }, [userId]);

    // Expose refresh function to parent
    useImperativeHandle(ref, () => ({
        refresh: fetchStats
    }));

    // Show loading skeleton while fetching
    if (loading) {
        return (
            <div className="mb-8">
                <h2 className="text-2xl font-bold text-gray-800 mb-4 flex items-center gap-2">
                    <TrendingUp className="w-6 h-6 text-blue-600" />
                    Your Progress
                </h2>
                <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                    {[1, 2, 3, 4].map((i) => (
                        <div key={i} className="bg-gray-100 rounded-xl p-4 border border-gray-200 shadow-sm animate-pulse">
                            <div className="h-4 bg-gray-300 rounded w-20 mb-2"></div>
                            <div className="h-8 bg-gray-300 rounded w-16 mb-1"></div>
                            <div className="h-3 bg-gray-300 rounded w-12"></div>
                        </div>
                    ))}
                </div>
            </div>
        );
    }

    // Show actual stats or defaults
    const displayStats = stats || {
        total_solved: 0,
        total_problems: 100,
        completion_percentage: 0,
        current_streak: 0,
        solved_today: 0
    };

    return (
        <div className="mb-8">
            <h2 className="text-2xl font-bold text-gray-800 mb-4 flex items-center gap-2">
                <TrendingUp className="w-6 h-6 text-blue-600" />
                Your Progress
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                {/* Total Solved */}
                <div className="bg-gradient-to-br from-blue-50 to-blue-100 rounded-xl p-4 border border-blue-200 shadow-sm hover:shadow-md transition-shadow">
                    <div className="flex items-center justify-between">
                        <div>
                            <p className="text-sm text-blue-700 font-medium mb-1">Total Solved</p>
                            <p className="text-3xl font-bold text-blue-900">{displayStats.total_solved}</p>
                            <p className="text-xs text-blue-600 mt-1">of {displayStats.total_problems}</p>
                        </div>
                        <CheckCircle2 className="w-10 h-10 text-blue-600 opacity-30" />
                    </div>
                </div>

                {/* Completion Rate */}
                <div className="bg-gradient-to-br from-green-50 to-green-100 rounded-xl p-4 border border-green-200 shadow-sm hover:shadow-md transition-shadow">
                    <div className="flex items-center justify-between">
                        <div>
                            <p className="text-sm text-green-700 font-medium mb-1">Completion</p>
                            <p className="text-3xl font-bold text-green-900">{displayStats.completion_percentage}%</p>
                            <div className="w-full bg-green-200 rounded-full h-2 mt-2">
                                <div
                                    className="bg-green-600 h-2 rounded-full transition-all"
                                    style={{ width: `${displayStats.completion_percentage}%` }}
                                ></div>
                            </div>
                        </div>
                        <Target className="w-10 h-10 text-green-600 opacity-30" />
                    </div>
                </div>

                {/* Current Streak */}
                <div className="bg-gradient-to-br from-orange-50 to-orange-100 rounded-xl p-4 border border-orange-200 shadow-sm hover:shadow-md transition-shadow">
                    <div className="flex items-center justify-between">
                        <div>
                            <p className="text-sm text-orange-700 font-medium mb-1">Current Streak</p>
                            <p className="text-3xl font-bold text-orange-900">{displayStats.current_streak}</p>
                            <p className="text-xs text-orange-600 mt-1">days</p>
                        </div>
                        <Flame className="w-10 h-10 text-orange-600 opacity-30" />
                    </div>
                </div>

                {/* Solved Today */}
                <div className="bg-gradient-to-br from-purple-50 to-purple-100 rounded-xl p-4 border border-purple-200 shadow-sm hover:shadow-md transition-shadow">
                    <div className="flex items-center justify-between">
                        <div>
                            <p className="text-sm text-purple-700 font-medium mb-1">Solved Today</p>
                            <p className="text-3xl font-bold text-purple-900">{displayStats.solved_today || 0}</p>
                            <p className="text-xs text-purple-600 mt-1">Keep it up!</p>
                        </div>
                        <CheckCircle2 className="w-10 h-10 text-purple-600 opacity-30" />
                    </div>
                </div>
            </div>
        </div>
    );
});

export default ProgressStats;
