import React, { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { useNavigate } from 'react-router-dom';
import {
  BarChart, Bar, PieChart, Pie, Cell,
  XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer
} from 'recharts';
import {
  TrendingUp, Target, Clock, Award, Brain, Users,
  Calendar, Zap, Star, AlertCircle, Trophy,
  BarChart3, PieChart as PieChartIcon, Activity, LayoutDashboard
} from 'lucide-react';

import { analyticsAPI } from '../services/api';
import GDPracticeWidget from '../components/Dashboard/GDPracticeWidget';

const Dashboard = () => {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [progressData, setProgressData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchDashboard = async () => {
      if (!user?.id) {
        setLoading(false);
        return;
      }

      try {
        setLoading(true);
        const response = await analyticsAPI.getDashboard();
        // Handle wrapped response { status: "success", data: ... }
        if (response.data && response.data.data) {
          setProgressData(response.data.data);
        } else {
          setProgressData(response.data);
        }
      } catch (err) {
        console.error('Failed to fetch dashboard data:', err);
        setError('Failed to load dashboard. Showing limited info.');
        // Fallback or empty state handled by progressData being null
      } finally {
        setLoading(false);
      }
    };

    fetchDashboard();
  }, [user]);

  if (loading) {
    return (
      <div className="p-8 min-h-screen bg-gray-50">
        <div className="max-w-7xl mx-auto">
          <div className="bg-white rounded-[2rem] shadow-xl shadow-gray-100 p-12 text-center border border-gray-100 relative overflow-hidden">
            <div className="absolute top-0 right-0 w-32 h-32 bg-blue-50 rounded-bl-[4rem] opacity-50"></div>
            <div className="relative z-10">
              <div className="w-16 h-16 border-4 border-blue-600 border-t-transparent rounded-full animate-spin mx-auto mb-6"></div>
              <div className="text-xl font-bold text-gray-800">Welcome back, {user?.email || 'User'}!</div>
              <p className="text-gray-500 mt-2">Loading your personalized dashboard...</p>
            </div>
          </div>
        </div>
      </div>
    );
  }

  if (!progressData) {
    return (
      <div className="p-8 min-h-screen bg-gray-50">
        <div className="max-w-7xl mx-auto">
          <h1 className="text-4xl font-black text-gray-900 mb-8 text-center">Welcome to AceIt!</h1>
          <div className="bg-white rounded-[2rem] shadow-xl shadow-gray-100 p-12 text-center border border-gray-100 relative overflow-hidden">
            <div className="absolute top-0 right-0 w-48 h-48 bg-gradient-to-br from-blue-50 to-indigo-50 rounded-bl-full opacity-50"></div>
            <div className="relative z-10">
              <div className="w-24 h-24 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-6">
                <Brain className="h-12 w-12 text-blue-600" />
              </div>
              <h2 className="text-3xl font-black text-gray-900 mb-4">Start Your Learning Journey</h2>
              <p className="text-gray-600 mb-8 text-lg">No progress data yet. Start practicing to track your improvement!</p>
              <button
                onClick={() => navigate('/aptitude')}
                className="bg-gradient-to-r from-blue-600 to-indigo-600 text-white px-8 py-4 rounded-2xl font-bold hover:from-blue-700 hover:to-indigo-700 shadow-xl shadow-blue-200 hover:shadow-blue-300 transition-all transform hover:-translate-y-1"
              >
                Begin First Lesson
              </button>
            </div>
          </div>
        </div>
      </div>
    );
  }

  // Color palettes
  const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884D8', '#82CA9D'];
  const SKILL_COLORS = ['#3B82F6', '#10B981', '#8B5CF6', '#F59E0B', '#EF4444', '#06B6D4'];

  // Prepare weekly activity data for chart
  const weeklyData = progressData.weekly_activity.map(day => ({
    day: new Date(day.date).toLocaleDateString('en-US', { weekday: 'short' }),
    aptitude: day.aptitude,
    coding: day.coding,
    score: day.score
  }));

  // Prepare skill data for chart
  const skillData = progressData.skill_distribution;

  // Stats cards
  const stats = [
    {
      title: 'Overall Score',
      value: `${progressData.overall_score}%`,
      color: 'bg-gradient-to-r from-blue-500 to-cyan-500',
      icon: <TrendingUp className="h-6 w-6" />,
      description: 'Your overall performance'
    },
    {
      title: 'Daily Streak',
      value: `${progressData.daily_streak} days`,
      color: 'bg-gradient-to-r from-green-500 to-emerald-500',
      icon: <Zap className="h-6 w-6" />,
      description: 'Consecutive practice days'
    },
    {
      title: 'Total Practice',
      value: `${Math.round(progressData.total_time_spent / 60)}h`,
      color: 'bg-gradient-to-r from-purple-500 to-pink-500',
      icon: <Clock className="h-6 w-6" />,
      description: 'Time spent learning'
    },
    {
      title: 'Accuracy',
      value: `${progressData.aptitude.accuracy}%`,
      color: 'bg-gradient-to-r from-orange-500 to-red-500',
      icon: <Award className="h-6 w-6" />,
      description: 'Average success rate'
    },
  ];

  const moduleStats = [
    {
      title: 'Aptitude',
      score: progressData.aptitude.average_score,
      total: progressData.aptitude.tests_taken,
      color: 'bg-blue-100 text-blue-600',
      icon: '🧠',
      path: '/aptitude'
    },
    {
      title: 'Coding',
      score: progressData.coding.average_success_rate,
      total: progressData.coding.problems_attempted,
      color: 'bg-green-100 text-green-600',
      icon: '💻',
      path: '/coding'
    },
    {
      title: 'Interviews',
      score: 65,
      total: 3,
      color: 'bg-purple-100 text-purple-600',
      icon: '🎤',
      path: '/interview'
    },
  ];

  return (
    <div className="p-8 min-h-screen bg-gray-50">
      {/* Header */}
      <div className="max-w-7xl mx-auto mb-10 text-center">
        <div className="inline-block p-4 bg-blue-50 rounded-2xl mb-4">
          <LayoutDashboard className="h-10 w-10 text-blue-600" />
        </div>
        <h1 className="text-4xl font-black text-gray-900 mb-2 tracking-tight">Welcome back, {user?.username || user?.email || 'Learner'}</h1>
        <p className="text-lg text-gray-500 max-w-2xl mx-auto">
          Your personalized learning dashboard
          {progressData.overall_score === 0 && (
            <span className="ml-2 text-sm bg-blue-100 text-blue-800 px-3 py-1 rounded-full font-bold">
              Start Practicing!
            </span>
          )}
        </p>
        <div className="mt-3 text-sm text-gray-400">
          Last updated: {new Date().toLocaleDateString()}
        </div>
      </div>

      <div className="max-w-7xl mx-auto">

        {/* Stats Overview */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          {stats.map((stat, index) => (
            <div key={index} className="bg-white rounded-[2rem] shadow-xl shadow-gray-100 p-6 hover:scale-105 transition-transform duration-200 cursor-pointer border border-gray-100 hover:border-blue-200 relative overflow-hidden">
              <div className="absolute top-0 right-0 w-20 h-20 bg-gradient-to-br from-blue-50 to-indigo-50 rounded-bl-[3rem] opacity-40"></div>
              <div className="flex justify-between items-start relative z-10">
                <div>
                  <p className="text-gray-500 text-sm font-bold uppercase tracking-wide">{stat.title}</p>
                  <p className="text-3xl font-black mt-2 text-gray-900">{stat.value}</p>
                  <p className="text-gray-400 text-xs mt-1">{stat.description}</p>
                </div>
                <div className={`p-3 rounded-xl ${index === 0 ? 'bg-blue-50 text-blue-600' :
                  index === 1 ? 'bg-green-50 text-green-600' :
                    index === 2 ? 'bg-purple-50 text-purple-600' :
                      'bg-orange-50 text-orange-600'
                  }`}>
                  {stat.icon}
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* GD Practice Widget (New Feature) */}
        <GDPracticeWidget />

        {/* Charts Section */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
          {/* Weekly Activity Chart */}
          <div className="bg-white rounded-[2rem] shadow-xl shadow-gray-100 p-8 border border-gray-100 relative overflow-hidden">
            <div className="absolute top-0 right-0 w-32 h-32 bg-blue-50 rounded-bl-[4rem] opacity-40"></div>
            <div className="flex items-center mb-6 relative z-10">
              <Activity className="h-6 w-6 text-blue-600 mr-3" />
              <h3 className="text-xl font-black text-gray-900">Weekly Activity</h3>
            </div>
            <div className="h-72 w-full min-w-0 relative z-10">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={weeklyData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
                  <XAxis dataKey="day" stroke="#666" />
                  <YAxis stroke="#666" />
                  <Tooltip />
                  <Legend />
                  <Bar dataKey="aptitude" fill="#3B82F6" name="Aptitude Qs" radius={[8, 8, 0, 0]} />
                  <Bar dataKey="coding" fill="#10B981" name="Coding Problems" radius={[8, 8, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>

          {/* Skill Distribution Chart */}
          <div className="bg-white rounded-[2rem] shadow-xl shadow-gray-100 p-8 border border-gray-100 relative overflow-hidden">
            <div className="absolute top-0 right-0 w-32 h-32 bg-green-50 rounded-bl-[4rem] opacity-40"></div>
            <div className="flex items-center mb-6 relative z-10">
              <PieChartIcon className="h-6 w-6 text-green-600 mr-3" />
              <h3 className="text-xl font-black text-gray-900">Skill Distribution</h3>
            </div>
            <div className="h-72 w-full min-w-0 relative z-10">
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={skillData}
                    cx="50%"
                    cy="50%"
                    labelLine={false}
                    label={({ name, score }) => `${name}: ${score}%`}
                    outerRadius={80}
                    fill="#8884d8"
                    dataKey="score"
                  >
                    {skillData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={SKILL_COLORS[index % SKILL_COLORS.length]} />
                    ))}
                  </Pie>
                  <Tooltip formatter={(value) => [`${value}%`, 'Score']} />
                </PieChart>
              </ResponsiveContainer>
            </div>
          </div>
        </div>

        {/* Module Performance & Recent Activity */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 mb-8">
          {/* Module Performance */}
          <div className="bg-white rounded-[2rem] shadow-xl shadow-gray-100 p-8 lg:col-span-2 border border-gray-100 relative overflow-hidden">
            <div className="absolute top-0 right-0 w-32 h-32 bg-purple-50 rounded-bl-[4rem] opacity-40"></div>
            <div className="flex items-center mb-6 relative z-10">
              <BarChart3 className="h-6 w-6 text-purple-600 mr-3" />
              <h3 className="text-xl font-black text-gray-900">Module Performance</h3>
            </div>
            <div className="space-y-4 relative z-10">
              {moduleStats.map((module, index) => (
                <div
                  key={index}
                  onClick={() => navigate(module.path)}
                  className="flex items-center justify-between p-5 rounded-2xl hover:bg-gray-50 cursor-pointer transition-all border border-gray-100 hover:border-blue-200 hover:shadow-md"
                >
                  <div className="flex items-center">
                    <span className="text-3xl mr-4">{module.icon}</span>
                    <div>
                      <h4 className="font-bold text-gray-900">{module.title}</h4>
                      <div className="flex items-center mt-2">
                        <div className="w-48 bg-gray-200 rounded-full h-2.5">
                          <div
                            className="h-full rounded-full transition-all"
                            style={{
                              width: `${module.score}%`,
                              backgroundColor: module.color.includes('blue') ? '#3b82f6' :
                                module.color.includes('green') ? '#22c55e' : '#a855f7'
                            }}
                          ></div>
                        </div>
                        <span className="ml-3 text-sm font-bold text-gray-700">{module.score}%</span>
                      </div>
                    </div>
                  </div>
                  <div className="text-right">
                    <div className="text-3xl font-black text-gray-900">{module.total}</div>
                    <div className="text-xs text-gray-500 font-medium">attempts</div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Recent Activity */}
          <div className="bg-white rounded-[2rem] shadow-xl shadow-gray-100 p-8 border border-gray-100 relative overflow-hidden">
            <div className="absolute top-0 right-0 w-32 h-32 bg-orange-50 rounded-bl-[4rem] opacity-40"></div>
            <div className="flex items-center mb-6 relative z-10">
              <Calendar className="h-6 w-6 text-orange-600 mr-3" />
              <h3 className="text-xl font-black text-gray-900">Recent Activity</h3>
            </div>
            <div className="space-y-4 relative z-10">
              {progressData.recent_activity.length > 0 ? (
                progressData.recent_activity.map((activity, index) => (
                  <div key={index} className="flex items-start p-4 rounded-xl bg-gray-50 border border-gray-100">
                    <div className="flex-shrink-0 mt-1">
                      {activity.type === 'aptitude_test' && (
                        <div className="w-10 h-10 bg-blue-100 rounded-xl flex items-center justify-center">
                          <Brain className="h-5 w-5 text-blue-600" />
                        </div>
                      )}
                      {activity.type === 'coding_problem' && (
                        <div className="w-10 h-10 bg-green-100 rounded-xl flex items-center justify-center">
                          <Target className="h-5 w-5 text-green-600" />
                        </div>
                      )}
                      {activity.type === 'mock_interview' && (
                        <div className="w-10 h-10 bg-purple-100 rounded-xl flex items-center justify-center">
                          <Users className="h-5 w-5 text-purple-600" />
                        </div>
                      )}
                    </div>
                    <div className="ml-3">
                      <p className="font-bold text-gray-900">
                        {activity.type === 'coding_problem' ? activity.problem :
                          activity.type === 'aptitude_test' ? 'Aptitude Test' : 'Mock Interview'}
                      </p>
                      <p className="text-sm text-gray-600 mt-1">
                        Score: {activity.score}%
                        {activity.success !== undefined && (
                          <span className={`ml-2 px-2 py-0.5 rounded-full text-xs font-bold ${activity.success ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'}`}>
                            {activity.success ? '✓' : '✗'}
                          </span>
                        )}
                      </p>
                      <p className="text-xs text-gray-400 mt-1 font-medium">{activity.date}</p>
                    </div>
                  </div>
                ))
              ) : (
                <div className="text-center py-10">
                  <AlertCircle className="h-12 w-12 text-gray-300 mx-auto mb-3" />
                  <p className="text-gray-500 font-medium">No recent activity</p>
                  <p className="text-sm text-gray-400 mt-1">Start practicing to see your progress</p>
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Recommendations */}
        <div className="bg-white rounded-[2rem] shadow-xl shadow-gray-100 p-8 mb-8 border border-gray-100 relative overflow-hidden">
          <div className="absolute top-0 right-0 w-32 h-32 bg-indigo-50 rounded-bl-[4rem] opacity-40"></div>
          <div className="flex items-center mb-6 relative z-10">
            <Star className="h-6 w-6 text-indigo-600 mr-3" />
            <h3 className="text-xl font-black text-gray-900">Personalized Recommendations</h3>
          </div>
          <div className="space-y-3 relative z-10">
            {progressData.recommendations.map((recommendation, index) => (
              <div key={index} className="flex items-start p-4 rounded-xl bg-gradient-to-br from-indigo-50 to-blue-50 border border-indigo-100">
                <div className="flex-shrink-0 mt-1">
                  <div className="w-7 h-7 bg-indigo-600 rounded-full flex items-center justify-center">
                    <span className="text-white text-sm font-black">{index + 1}</span>
                  </div>
                </div>
                <p className="ml-3 text-sm text-gray-700 font-medium">{recommendation}</p>
              </div>
            ))}
          </div>
        </div>

        {/* Quick Action Buttons */}
        <div className="grid grid-cols-1 md:grid-cols-5 gap-4">
          <button
            onClick={() => navigate('/analytics/unified')}
            className="bg-gradient-to-r from-cyan-600 to-teal-700 text-white py-4 px-6 rounded-2xl font-bold hover:shadow-xl shadow-lg shadow-cyan-200 hover:shadow-cyan-300 transition-all transform hover:-translate-y-1 flex items-center justify-center"
          >
            <BarChart3 className="h-5 w-5 mr-2" />
            Unified Analytics
          </button>
          <button
            onClick={() => navigate('/aptitude')}
            className="bg-gradient-to-r from-blue-600 to-blue-700 text-white py-4 px-6 rounded-2xl font-bold hover:shadow-xl shadow-lg shadow-blue-200 hover:shadow-blue-300 transition-all transform hover:-translate-y-1 flex items-center justify-center"
          >
            <Brain className="h-5 w-5 mr-2" />
            Practice Aptitude
          </button>
          <button
            onClick={() => navigate('/coding')}
            className="bg-gradient-to-r from-green-600 to-emerald-700 text-white py-4 px-6 rounded-2xl font-bold hover:shadow-xl shadow-lg shadow-green-200 hover:shadow-green-300 transition-all transform hover:-translate-y-1 flex items-center justify-center"
          >
            <Target className="h-5 w-5 mr-2" />
            Solve Problems
          </button>
          <button
            onClick={() => navigate('/interview')}
            className="bg-gradient-to-r from-purple-600 to-purple-700 text-white py-4 px-6 rounded-2xl font-bold hover:shadow-xl shadow-lg shadow-purple-200 hover:shadow-purple-300 transition-all transform hover:-translate-y-1 flex items-center justify-center"
          >
            <Users className="h-5 w-5 mr-2" />
            Mock Interview
          </button>
          <button
            onClick={() => navigate('/resume')}
            className="bg-gradient-to-r from-indigo-600 to-indigo-700 text-white py-4 px-6 rounded-2xl font-bold hover:shadow-xl shadow-lg shadow-indigo-200 hover:shadow-indigo-300 transition-all transform hover:-translate-y-1 flex items-center justify-center"
          >
            <Award className="h-5 w-5 mr-2" />
            Analyze Resume
          </button>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;